import type { ReactNode } from 'react'
import type { Level } from '../data/vocabulary'
import { genderClass } from './richText'
import { lookupVocabToken, type VocabHit } from './vocabIndex'

const ARTICLE_RE =
  /^(der|die|das|den|dem|des|ein|eine|einen|einem|einer|eines)$/i

function articleClass(token: string): string | null {
  const lower = token.toLowerCase()
  if (
    lower === 'der' ||
    lower === 'den' ||
    lower === 'dem' ||
    lower === 'des' ||
    lower === 'ein' ||
    lower === 'einen' ||
    lower === 'einem' ||
    lower === 'eines'
  ) {
    return genderClass.der
  }
  if (lower === 'die' || lower === 'eine' || lower === 'einer') {
    return genderClass.die
  }
  if (lower === 'das') return genderClass.das
  return null
}

/**
 * Render German text with:
 * - der/die/das colors
 * - clickable links for tokens found in the vocabulary
 */
export function LinkedGermanText({
  text,
  preferLevel,
  preferId,
  currentId,
  onOpenWord,
}: {
  text: string
  preferLevel?: Level
  preferId?: string
  /** Highlight but still allow click (self). */
  currentId?: string
  onOpenWord?: (hit: VocabHit) => void
}): ReactNode {
  // Split into words / whitespace / punctuation, keep delimiters
  const parts = text.split(/([A-Za-zÄÖÜäöüß]+)/)

  return (
    <>
      {parts.map((part, i) => {
        if (!part) return null

        // whitespace / punctuation
        if (!/^[A-Za-zÄÖÜäöüß]+$/.test(part)) {
          return <span key={`${i}-t`}>{part}</span>
        }

        const aClass = ARTICLE_RE.test(part) ? articleClass(part) : null
        if (aClass) {
          return (
            <span key={`${i}-a`} className={aClass}>
              {part}
            </span>
          )
        }

        const hit = onOpenWord
          ? lookupVocabToken(part, { preferLevel, preferId })
          : null

        if (hit && onOpenWord) {
          const isCurrent = currentId === hit.id
          return (
            <button
              key={`${i}-l-${hit.id}`}
              type="button"
              className={`vocab-link ${isCurrent ? 'current' : ''}`}
              title={`查看：${hit.article ? hit.article + ' ' : ''}${hit.word}（${hit.translation}）· ${hit.level}`}
              onClick={(ev) => {
                ev.preventDefault()
                ev.stopPropagation()
                onOpenWord(hit)
              }}
            >
              {part}
            </button>
          )
        }

        return <span key={`${i}-w`}>{part}</span>
      })}
    </>
  )
}
