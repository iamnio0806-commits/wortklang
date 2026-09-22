let preferredVoice: SpeechSynthesisVoice | null = null

/** Learner-friendly default (slightly under 1.0). */
export const SPEECH_RATE_NORMAL = 0.88
/**
 * Slow playback — deliberately slower than the old ~0.7 “慢速”
 * so beginners can catch word boundaries.
 */
export const SPEECH_RATE_SLOW = 0.5
/** Near native conversational tempo (browser TTS default ≈ 1.0). */
export const SPEECH_RATE_NATIVE = 1.05

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

export function speakGerman(
  text: string,
  rate: number = SPEECH_RATE_NORMAL,
): void {
  if (typeof window === 'undefined' || !window.speechSynthesis) return
  window.speechSynthesis.cancel()
  const utterance = new SpeechSynthesisUtterance(text)
  utterance.lang = 'de-DE'
  utterance.rate = rate
  utterance.pitch = 1
  const voice = preferredVoice ?? pickGermanVoice()
  if (voice) {
    preferredVoice = voice
    utterance.voice = voice
  }
  window.speechSynthesis.speak(utterance)
}

export function speakGermanPace(text: string, pace: SpeechPace): void {
  speakGerman(text, SPEECH_RATE_BY_PACE[pace])
}

export function speakGermanSlow(text: string): void {
  speakGerman(text, SPEECH_RATE_SLOW)
}

export function speakGermanNative(text: string): void {
  speakGerman(text, SPEECH_RATE_NATIVE)
}

export function stopSpeaking(): void {
  if (typeof window === 'undefined' || !window.speechSynthesis) return
  window.speechSynthesis.cancel()
}
