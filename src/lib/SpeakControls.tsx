import { type SpeechPace, speakGermanPace } from './speech'

function prepareText(text: string, normalizeNewlines: boolean): string {
  return normalizeNewlines ? text.replace(/\n/g, '. ') : text
}

const PACE_CLASS: Record<SpeechPace, string> = {
  normal: '',
  slow: 'speak-btn-slow',
  native: 'speak-btn-native',
}

/** Single speak button for a given pace. */
export function SpeakButton({
  label,
  text,
  pace = 'normal',
  /** @deprecated use pace="slow" */
  slow = false,
  normalizeNewlines = false,
}: {
  label: string
  text: string
  pace?: SpeechPace
  slow?: boolean
  /** Turn newlines into pauses (reading / listening scripts). */
  normalizeNewlines?: boolean
}) {
  const resolved: SpeechPace = slow ? 'slow' : pace
  return (
    <button
      type="button"
      className={`speak-btn ${PACE_CLASS[resolved]}`.trim()}
      onClick={() =>
        speakGermanPace(prepareText(text, normalizeNewlines), resolved)
      }
      aria-label={label}
    >
      <span className="speak-icon" aria-hidden>
        ♪
      </span>
      {label}
    </button>
  )
}

/** Slow + learner + native pace for every playback surface. */
export function SpeakPair({
  text,
  normalLabel = '聽',
  slowLabel = '慢速',
  nativeLabel = '母語人士',
  normalizeNewlines = false,
  showNative = true,
}: {
  text: string
  normalLabel?: string
  slowLabel?: string
  nativeLabel?: string
  normalizeNewlines?: boolean
  showNative?: boolean
}) {
  return (
    <>
      <SpeakButton
        label={slowLabel}
        text={text}
        pace="slow"
        normalizeNewlines={normalizeNewlines}
      />
      <SpeakButton
        label={normalLabel}
        text={text}
        pace="normal"
        normalizeNewlines={normalizeNewlines}
      />
      {showNative && (
        <SpeakButton
          label={nativeLabel}
          text={text}
          pace="native"
          normalizeNewlines={normalizeNewlines}
        />
      )}
    </>
  )
}
