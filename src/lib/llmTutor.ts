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

/** Gemini OpenAI-compatible endpoint + Gemini 3.1 Pro. */
export const GEMINI_OPENAI_BASE =
  'https://generativelanguage.googleapis.com/v1beta/openai'
export const GEMINI_31_PRO = 'gemini-3.1-pro-preview'

export const DEFAULT_LLM_SETTINGS: LlmSettings = {
  apiKey: '',
  baseUrl: GEMINI_OPENAI_BASE,
  model: GEMINI_31_PRO,
}

const LEGACY_OPENAI_DEFAULTS = {
  baseUrl: 'https://api.openai.com/v1',
  model: 'gpt-4o-mini',
}

function migrateSettings(parsed: Partial<LlmSettings>): LlmSettings {
  const merged: LlmSettings = { ...DEFAULT_LLM_SETTINGS, ...parsed }

  // Upgrade leftover OpenAI defaults from older builds to Gemini 3.1 Pro.
  const base = (merged.baseUrl || '').replace(/\/$/, '')
  const legacyBase = LEGACY_OPENAI_DEFAULTS.baseUrl.replace(/\/$/, '')
  if (
    !parsed.baseUrl ||
    base === legacyBase ||
    base.includes('api.openai.com')
  ) {
    if (!parsed.baseUrl || base === legacyBase) {
      merged.baseUrl = GEMINI_OPENAI_BASE
    }
  }
  if (
    !parsed.model ||
    parsed.model === LEGACY_OPENAI_DEFAULTS.model ||
    parsed.model === 'gpt-4o' ||
    parsed.model.startsWith('gpt-')
  ) {
    // Only auto-switch when they were still on the old default / GPT family
    // and had not explicitly set a non-GPT model.
    if (
      !parsed.model ||
      parsed.model === LEGACY_OPENAI_DEFAULTS.model ||
      (parsed.model.startsWith('gpt-') &&
        (base === legacyBase || !parsed.baseUrl))
    ) {
      merged.model = GEMINI_31_PRO
      merged.baseUrl = GEMINI_OPENAI_BASE
    }
  }

  // Normalize trailing slash
  merged.baseUrl = merged.baseUrl.replace(/\/$/, '')
  return merged
}

export function loadLlmSettings(): LlmSettings {
  try {
    const raw = localStorage.getItem(SETTINGS_KEY)
    if (!raw) return { ...DEFAULT_LLM_SETTINGS }
    const parsed = JSON.parse(raw) as Partial<LlmSettings>
    return migrateSettings(parsed)
  } catch {
    return { ...DEFAULT_LLM_SETTINGS }
  }
}

export function saveLlmSettings(s: LlmSettings): void {
  localStorage.setItem(
    SETTINGS_KEY,
    JSON.stringify({
      ...s,
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

/** Native Gemini generateContent (when not using the OpenAI-compat path). */
async function requestViaGeminiNative(opts: {
  settings: LlmSettings
  system: string
  user: string
}): Promise<string> {
  const { settings, system, user } = opts
  const model = settings.model.trim() || GEMINI_31_PRO
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
    throw new Error(`Gemini API 錯誤 ${res.status}: ${errText.slice(0, 220)}`)
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
  const res = await fetch(`${base}/chat/completions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${settings.apiKey.trim()}`,
    },
    body: JSON.stringify({
      model: settings.model,
      temperature: 0.2,
      messages: [
        { role: 'system', content: system },
        { role: 'user', content: user },
      ],
      // Helps Gemini / newer OpenAI models stick to JSON
      response_format: { type: 'json_object' },
    }),
  })

  if (!res.ok) {
    const errText = await res.text().catch(() => '')
    throw new Error(`API 錯誤 ${res.status}: ${errText.slice(0, 220)}`)
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
  const { settings, mode, promptZh, userText, level } = opts
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

  // Prefer OpenAI-compat when baseUrl points at Gemini openai bridge or any chat endpoint.
  // If baseUrl is empty/default Gemini host without /openai, use native generateContent.
  const base = settings.baseUrl.replace(/\/$/, '')
  let content: string
  if (
    isGeminiEndpoint(base) &&
    !/\/openai$/i.test(base) &&
    !/openai/i.test(base)
  ) {
    content = await requestViaGeminiNative({ settings, system, user })
  } else {
    content = await requestViaChatCompletions({ settings, system, user })
  }

  const parsed = extractJson(content) as TutorCorrection
  if (!parsed.corrected) throw new Error('回傳格式不完整')
  return {
    corrected: parsed.corrected,
    score: Number(parsed.score) || 0,
    summaryZh: parsed.summaryZh || '',
    issues: Array.isArray(parsed.issues) ? parsed.issues : [],
    tipsZh: Array.isArray(parsed.tipsZh) ? parsed.tipsZh : [],
  }
}
