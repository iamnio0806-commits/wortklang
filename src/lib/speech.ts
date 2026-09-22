let preferredVoice: SpeechSynthesisVoice | null = null

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
    // Fallback if event never fires
    setTimeout(ready, 500)
  })
}

export function speakGerman(text: string, rate = 0.9): void {
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

export function stopSpeaking(): void {
  if (typeof window === 'undefined' || !window.speechSynthesis) return
  window.speechSynthesis.cancel()
}
