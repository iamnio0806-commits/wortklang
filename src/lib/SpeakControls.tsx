import {
  SPEECH_RATE_NORMAL,
  SPEECH_RATE_SLOW,
  speakGerman,
} from './speech'

function prepareText(text: string, normalizeNewlines: boolean): string {
  return normalizeNewlines ? text.replace(/\n/g, '. ') : text
}

/** Single speak button — pass `slow` for the slower rate. */
export function SpeakButton({
  label,
  text,
  slow = false,
  normalizeNewlines = false,
}: {
  label: string
  text: string
  slow?: boolean
  /** Turn newlines into pauses (reading / listening scripts). */
  normalizeNewlines?: boolean
}) {
  return (
    <button
      type="button"
      className={`speak-btn ${slow ? 'speak-btn-slow' : ''}`}
      onClick={() =>
        speakGerman(
          prepareText(text, normalizeNewlines),
          slow ? SPEECH_RATE_SLOW : SPEECH_RATE_NORMAL,
        )
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

/** Normal + slow pair for every playback surface. */
export function SpeakPair({
  text,
  normalLabel = '聽',
  slowLabel = '慢速',
  normalizeNewlines = false,
}: {
  text: string
  normalLabel?: string
  slowLabel?: string
  normalizeNewlines?: boolean
}) {
  return (
    <>
      <SpeakButton
        label={normalLabel}
        text={text}
        normalizeNewlines={normalizeNewlines}
      />
      <SpeakButton
        label={slowLabel}
        text={text}
        slow
        normalizeNewlines={normalizeNewlines}
      />
    </>
  )
}
