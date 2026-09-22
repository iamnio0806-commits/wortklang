let preferredVoice: SpeechSynthesisVoice | null = null

/** Learner-friendly default (slightly under 1.0). */
export const SPEECH_RATE_NORMAL = 0.88
/**
 * Slow body rate — slower than before (was 0.5).
 * The opening words use SPEECH_RATE_SLOW_START for an even slower lead-in.
 */
export const SPEECH_RATE_SLOW = 0.36
/** Extra-slow lead-in for the first words of slow playback. */
export const SPEECH_RATE_SLOW_START = 0.26
/** Near native conversational tempo. */
export const SPEECH_RATE_NATIVE = 1.12

export type SpeechPace = 'normal' | 'slow' | 'native'

export const SPEECH_RATE_BY_PACE: Record<SpeechPace, number> = {
  normal: SPEECH_RATE_NORMAL,
  slow: SPEECH_RATE_SLOW,
  native: SPEECH_RATE_NATIVE,
}

function pickGermanVoice(): SpeechSynthesisVoice | null {
  if (typeof window === 'undefined' || !window.speechSynthesis) return null
  const voices = window.speechSynthesis.getVoices()
  const de = voices.filter((v) => v.lang.toLowerCase().startsWith('de'))
  if (!de.length) return null
  return (
    de.find((v) => /google|microsoft|anna|helena|katja|petra/i.test(v.name)) ??
    de[0]
  )
}

function applyVoice(utterance: SpeechSynthesisUtterance): void {
  utterance.lang = 'de-DE'
  utterance.pitch = 1
  const voice = preferredVoice ?? pickGermanVoice()
  if (voice) {
    preferredVoice = voice
    utterance.voice = voice
  }
}

export function ensureVoicesLoaded(): Promise<SpeechSynthesisVoice | null> {
  return new Promise((resolve) => {
    if (typeof window === 'undefined' || !window.speechSynthesis) {
      resolve(null)
      return
    }
    const ready = () => {
      preferredVoice = pickGermanVoice()
      resolve(preferredVoice)
    }
    const voices = window.speechSynthesis.getVoices()
    if (voices.length) {
      ready()
      return
    }
    window.speechSynthesis.addEventListener('voiceschanged', ready, {
      once: true,
    })
    setTimeout(ready, 500)
  })
}

/** Split so the first 1–2 content words play extra-slow, then the rest. */
function splitSlowLead(text: string): { head: string; tail: string } {
  const tokens = text.split(/(\s+)/)
  let words = 0
  let splitAt = tokens.length
  for (let i = 0; i < tokens.length; i++) {
    if (/[A-Za-zÄÖÜäöüß0-9]/.test(tokens[i])) {
      words += 1
      if (words >= 2) {
        splitAt = i + 1
        break
      }
    }
  }
  if (words === 0) return { head: text, tail: '' }
  if (words === 1) splitAt = tokens.length
  return {
    head: tokens.slice(0, splitAt).join(''),
    tail: tokens.slice(splitAt).join(''),
  }
}

function enqueue(text: string, rate: number): void {
  if (!text.trim()) return
  const utterance = new SpeechSynthesisUtterance(text)
  utterance.rate = rate
  applyVoice(utterance)
  window.speechSynthesis.speak(utterance)
}

/** Slow playback with a clearly slower opening. */
export function speakGermanSlow(text: string): void {
  if (typeof window === 'undefined' || !window.speechSynthesis) return
  window.speechSynthesis.cancel()
  const { head, tail } = splitSlowLead(text)
  enqueue(head, SPEECH_RATE_SLOW_START)
  if (tail.trim()) enqueue(tail, SPEECH_RATE_SLOW)
}

export function speakGerman(
  text: string,
  rate: number = SPEECH_RATE_NORMAL,
): void {
  if (typeof window === 'undefined' || !window.speechSynthesis) return
  // Route dedicated slow calls through the ramped player
  if (rate <= SPEECH_RATE_SLOW + 0.02) {
    speakGermanSlow(text)
    return
  }
  window.speechSynthesis.cancel()
  enqueue(text, rate)
}

export function speakGermanPace(text: string, pace: SpeechPace): void {
  if (pace === 'slow') {
    speakGermanSlow(text)
    return
  }
  speakGerman(text, SPEECH_RATE_BY_PACE[pace])
}

export function speakGermanNative(text: string): void {
  speakGerman(text, SPEECH_RATE_NATIVE)
}

export function stopSpeaking(): void {
  if (typeof window === 'undefined' || !window.speechSynthesis) return
  window.speechSynthesis.cancel()
}
