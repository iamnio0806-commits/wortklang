/** Optional LLM client for writing/speaking feedback (browser-side). */

export type LlmSettings = {
  apiKey: string
  baseUrl: string
  model: string
}

export type TutorCorrection = {
  corrected: string
  score: number
  summaryZh: string
  issues: { span: string; issueZh: string; fixZh: string }[]
  tipsZh: string[]
}

const SETTINGS_KEY = 'wortklang-llm-settings'

/** Gemini OpenAI-compatible endpoint + Gemini 3.1 Pro Preview. */
export const GEMINI_OPENAI_BASE =
  'https://generativelanguage.googleapis.com/v1beta/openai'
/** Official model id — bare `gemini-3.1-pro` returns 404. */
export const GEMINI_31_PRO = 'gemini-3.1-pro-preview'
/** Free-tier / cheaper fallbacks when Pro hits 429 quota. */
export const GEMINI_FLASH_FALLBACKS = [
  'gemini-3-flash-preview',
  'gemini-2.5-flash',
] as const


export const DEFAULT_LLM_SETTINGS: LlmSettings = {
  apiKey: '',
  baseUrl: GEMINI_OPENAI_BASE,
  model: GEMINI_31_PRO,
}

/** Map common typos / shorthand to the live API id. */
const MODEL_ALIASES: Record<string, string> = {
  'gemini-3.1-pro': GEMINI_31_PRO,
  'gemini-3.1-pro-latest': GEMINI_31_PRO,
  'gemini-3-pro': 'gemini-3-pro-preview',
  'gemini-3-pro-preview': 'gemini-3.1-pro-preview', // 3 Pro preview now points to 3.1
  'gemini-pro': GEMINI_31_PRO,
  'gemini-pro-latest': GEMINI_31_PRO,
  'gemini 3.1 pro': GEMINI_31_PRO,
  'gemini3.1pro': GEMINI_31_PRO,
}

export function normalizeGeminiModelId(model: string): string {
  const raw = model.trim()
  if (!raw) return GEMINI_31_PRO
  const key = raw.toLowerCase().replace(/\s+/g, ' ')
  if (MODEL_ALIASES[key]) return MODEL_ALIASES[key]
  // Strip accidental "models/" prefix
  const stripped = raw.replace(/^models\//i, '')
  if (MODEL_ALIASES[stripped.toLowerCase()]) {
    return MODEL_ALIASES[stripped.toLowerCase()]
  }
  return stripped
}

function migrateSettings(parsed: Partial<LlmSettings>): LlmSettings {
  const merged: LlmSettings = { ...DEFAULT_LLM_SETTINGS, ...parsed }
  const base = (merged.baseUrl || '').replace(/\/$/, '')

  // Upgrade leftover OpenAI defaults
  if (
    !parsed.baseUrl ||
    base === 'https://api.openai.com/v1' ||
    /api\.openai\.com/i.test(base)
  ) {
    if (!parsed.baseUrl || base === 'https://api.openai.com/v1') {
      merged.baseUrl = GEMINI_OPENAI_BASE
    }
  }
  if (
    !parsed.model ||
    parsed.model === 'gpt-4o-mini' ||
    parsed.model === 'gpt-4o' ||
    /^gpt-/i.test(parsed.model)
  ) {
    merged.model = GEMINI_31_PRO
    if (!parsed.baseUrl || /api\.openai\.com/i.test(base)) {
      merged.baseUrl = GEMINI_OPENAI_BASE
    }
  }

  merged.model = normalizeGeminiModelId(merged.model)
  merged.baseUrl = merged.baseUrl.replace(/\/$/, '')
  return merged
}

export function loadLlmSettings(): LlmSettings {
  try {
    const raw = localStorage.getItem(SETTINGS_KEY)
    if (!raw) return { ...DEFAULT_LLM_SETTINGS }
    const parsed = JSON.parse(raw) as Partial<LlmSettings>
    const next = migrateSettings(parsed)
    // Persist normalized model so UI stops showing the broken id
    if (parsed.model && parsed.model !== next.model) {
      saveLlmSettings(next)
    }
    return next
  } catch {
    return { ...DEFAULT_LLM_SETTINGS }
  }
}

export function saveLlmSettings(s: LlmSettings): void {
  localStorage.setItem(
    SETTINGS_KEY,
    JSON.stringify({
      ...s,
      model: normalizeGeminiModelId(s.model),
      baseUrl: s.baseUrl.replace(/\/$/, ''),
    }),
  )
}

function extractJson(text: string): unknown {
  const fenced = text.match(/```(?:json)?\s*([\s\S]*?)```/)
  const raw = fenced ? fenced[1] : text
  const start = raw.indexOf('{')
  const end = raw.lastIndexOf('}')
  if (start < 0 || end < 0) throw new Error('模型未回傳 JSON')
  return JSON.parse(raw.slice(start, end + 1))
}

function isGeminiEndpoint(baseUrl: string): boolean {
  return /generativelanguage\.googleapis\.com/i.test(baseUrl)
}

function friendlyApiError(status: number, errText: string): string {
  const short = errText.slice(0, 280)
  if (status === 429 || /exceeded your current quota|rate.?limit/i.test(errText)) {
    return (
      '配額／頻率已達上限（429）。Gemini 3.1 Pro 免費額度用完了，或打太快。' +
      '系統會自動改試 Flash；也可到 Google AI Studio 開帳單／看用量：' +
      'https://ai.google.dev/gemini-api/docs/rate-limits 。' +
      short
    )
  }
  if (
    status === 404 &&
    /gemini-3\.1-pro(?!-preview)/i.test(errText)
  ) {
    return `模型名稱錯誤：請用 ${GEMINI_31_PRO}（不能寫成 gemini-3.1-pro）。已可按「一鍵填入」自動修正。原文：${short}`
  }
  if (status === 404 && /not found/i.test(errText)) {
    return `模型不存在或無 generateContent 權限（404）。請確認 Model 為 ${GEMINI_31_PRO}。${short}`
  }
  return `API 錯誤 ${status}: ${short}`
}

function isQuotaError(err: unknown): boolean {
  const msg = err instanceof Error ? err.message : String(err)
  return /\b429\b|quota|rate.?limit|配額/i.test(msg)
}

async function sleep(ms: number): Promise<void> {
  await new Promise((r) => setTimeout(r, ms))
}

async function requestModelContent(opts: {
  settings: LlmSettings
  system: string
  user: string
}): Promise<string> {
  const { settings, system, user } = opts
  const base = settings.baseUrl.replace(/\/$/, '')

  if (isGeminiEndpoint(base)) {
    try {
      return await requestViaGeminiNative({ settings, system, user })
    } catch (nativeErr) {
      try {
        return await requestViaChatCompletions({
          settings: {
            ...settings,
            baseUrl: /openai/i.test(base) ? base : GEMINI_OPENAI_BASE,
          },
          system,
          user,
        })
      } catch {
        throw nativeErr instanceof Error
          ? nativeErr
          : new Error(String(nativeErr))
      }
    }
  }
  return requestViaChatCompletions({ settings, system, user })
}

/** Native Gemini generateContent via v1beta. */
async function requestViaGeminiNative(opts: {
  settings: LlmSettings
  system: string
  user: string
}): Promise<string> {
  const { settings, system, user } = opts
  const model = normalizeGeminiModelId(settings.model)
  const key = settings.apiKey.trim()
  const url = `https://generativelanguage.googleapis.com/v1beta/models/${encodeURIComponent(model)}:generateContent?key=${encodeURIComponent(key)}`

  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      systemInstruction: { parts: [{ text: system }] },
      contents: [{ role: 'user', parts: [{ text: user }] }],
      generationConfig: {
        temperature: 0.2,
        responseMimeType: 'application/json',
      },
    }),
  })

  if (!res.ok) {
    const errText = await res.text().catch(() => '')
    throw new Error(friendlyApiError(res.status, errText))
  }

  const data = (await res.json()) as {
    candidates?: { content?: { parts?: { text?: string }[] } }[]
    error?: { message?: string }
  }
  if (data.error?.message) {
    throw new Error(data.error.message)
  }
  const parts = data.candidates?.[0]?.content?.parts ?? []
  return parts.map((p) => p.text ?? '').join('')
}

/** OpenAI-compatible chat/completions (Gemini / OpenAI / proxies). */
async function requestViaChatCompletions(opts: {
  settings: LlmSettings
  system: string
  user: string
}): Promise<string> {
  const { settings, system, user } = opts
  const base = settings.baseUrl.replace(/\/$/, '')
  const model = normalizeGeminiModelId(settings.model)
  const body: Record<string, unknown> = {
    model,
    temperature: 0.2,
    messages: [
      { role: 'system', content: system },
      { role: 'user', content: user },
    ],
  }
  // response_format helps JSON; some proxies reject it — only send for Gemini/OpenAI-ish hosts
  if (isGeminiEndpoint(base) || /openai\.com/i.test(base)) {
    body.response_format = { type: 'json_object' }
  }

  const res = await fetch(`${base}/chat/completions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${settings.apiKey.trim()}`,
    },
    body: JSON.stringify(body),
  })

  if (!res.ok) {
    const errText = await res.text().catch(() => '')
    throw new Error(friendlyApiError(res.status, errText))
  }

  const data = (await res.json()) as {
    choices?: { message?: { content?: string | null } }[]
  }
  return data.choices?.[0]?.message?.content ?? ''
}

export async function requestGermanFeedback(opts: {
  settings: LlmSettings
  mode: 'schreiben' | 'sprechen'
  promptZh: string
  userText: string
  level: string
}): Promise<TutorCorrection> {
  const settings: LlmSettings = {
    ...opts.settings,
    model: normalizeGeminiModelId(opts.settings.model),
    baseUrl: opts.settings.baseUrl.replace(/\/$/, ''),
  }
  const { mode, promptZh, userText, level } = opts

  if (!settings.apiKey.trim()) {
    throw new Error('請先設定 Gemini API Key（僅存在本機瀏覽器）')
  }
  if (!userText.trim()) {
    throw new Error('請先輸入德文內容')
  }

  const system = `You are a strict but kind German tutor for CEFR ${level} learners.
Return ONLY valid JSON with this shape:
{
  "corrected": "corrected German text",
  "score": 0-100,
  "summaryZh": "Traditional Chinese short summary",
  "issues": [{"span":"wrong bit","issueZh":"...","fixZh":"..."}],
  "tipsZh": ["Traditional Chinese tip", "..."]
}
Focus on articles (der/die/das), verb position, case, and meaning.
Keep explanations in Traditional Chinese (Taiwan). Mode: ${mode}.`

  const user = `Task (zh): ${promptZh}\n\nLearner German:\n${userText}`

  const tried: string[] = []
  const queue = [
    settings.model,
    ...GEMINI_FLASH_FALLBACKS.filter((m) => m !== settings.model),
  ]

  let content = ''
  let usedModel = settings.model
  let lastErr: unknown

  for (let i = 0; i < queue.length; i++) {
    const model = normalizeGeminiModelId(queue[i])
    if (tried.includes(model)) continue
    tried.push(model)
    try {
      content = await requestModelContent({
        settings: { ...settings, model },
        system,
        user,
      })
      usedModel = model
      lastErr = null
      break
    } catch (err) {
      lastErr = err
      if (isQuotaError(err) && i < queue.length - 1) {
        // Brief pause then try a cheaper / free-tier model
        await sleep(600)
        continue
      }
      // Non-quota errors: one short retry on same model, then throw
      if (i === 0) {
        await sleep(800)
        try {
          content = await requestModelContent({
            settings: { ...settings, model },
            system,
            user,
          })
          usedModel = model
          lastErr = null
          break
        } catch (err2) {
          lastErr = err2
          if (isQuotaError(err2)) continue
          throw err2 instanceof Error ? err2 : new Error(String(err2))
        }
      }
      throw err instanceof Error ? err : new Error(String(err))
    }
  }

  if (lastErr || !content) {
    throw lastErr instanceof Error
      ? lastErr
      : new Error('所有模型皆無法回應（可能配額用盡）')
  }

  const parsed = extractJson(content) as TutorCorrection
  if (!parsed.corrected) throw new Error('回傳格式不完整')
  const fallbackNote =
    usedModel !== normalizeGeminiModelId(settings.model)
      ? `（Pro 額度不足，已改用 ${usedModel}）`
      : ''
  return {
    corrected: parsed.corrected,
    score: Number(parsed.score) || 0,
    summaryZh: `${parsed.summaryZh || ''}${fallbackNote}`,
    issues: Array.isArray(parsed.issues) ? parsed.issues : [],
    tipsZh: Array.isArray(parsed.tipsZh) ? parsed.tipsZh : [],
  }
}
