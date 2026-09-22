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

export const DEFAULT_LLM_SETTINGS: LlmSettings = {
  apiKey: '',
  baseUrl: 'https://api.openai.com/v1',
  model: 'gpt-4o-mini',
}

export function loadLlmSettings(): LlmSettings {
  try {
    const raw = localStorage.getItem(SETTINGS_KEY)
    if (!raw) return { ...DEFAULT_LLM_SETTINGS }
    const parsed = JSON.parse(raw) as Partial<LlmSettings>
    return { ...DEFAULT_LLM_SETTINGS, ...parsed }
  } catch {
    return { ...DEFAULT_LLM_SETTINGS }
  }
}

export function saveLlmSettings(s: LlmSettings): void {
  localStorage.setItem(SETTINGS_KEY, JSON.stringify(s))
}

function extractJson(text: string): unknown {
  const fenced = text.match(/```(?:json)?\s*([\s\S]*?)```/)
  const raw = fenced ? fenced[1] : text
  const start = raw.indexOf('{')
  const end = raw.lastIndexOf('}')
  if (start < 0 || end < 0) throw new Error('模型未回傳 JSON')
  return JSON.parse(raw.slice(start, end + 1))
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
    throw new Error('請先設定 API Key（僅存在本機瀏覽器）')
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
    }),
  })

  if (!res.ok) {
    const errText = await res.text().catch(() => '')
    throw new Error(`API 錯誤 ${res.status}: ${errText.slice(0, 180)}`)
  }

  const data = (await res.json()) as {
    choices?: { message?: { content?: string } }[]
  }
  const content = data.choices?.[0]?.message?.content ?? ''
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
