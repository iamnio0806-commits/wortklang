import type { ReactNode } from 'react'
import type { Level } from '../data/vocabulary'
import {
  ARTICLE_TOKEN_RE,
  classForArticle,
} from './articleColor'
import { lookupVocabToken, type VocabHit } from './vocabIndex'

/**
 * Render German text with:
 * - der/die/das colors (by following noun gender when known)
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

  function followingNounGender(fromIndex: number): VocabHit['article'] {
    for (let j = fromIndex + 1; j < parts.length; j++) {
      const p = parts[j]
      if (!p) continue
      if (!/^[A-Za-zÄÖÜäöüß]+$/.test(p)) {
        // skip pure whitespace; stop on punctuation that ends the NP
        if (p.trim() === '') continue
        if (/^[.,;:!?\-–—"'«»()[\]{}]+$/.test(p.trim())) break
        continue
      }
      if (ARTICLE_TOKEN_RE.test(p)) continue
      const hit = lookupVocabToken(p, { preferLevel, preferId })
      if (hit?.article) return hit.article
      // First content word without gender — stop so we don't pick a later noun
      break
    }
    return null
  }

  return (
    <>
      {parts.map((part, i) => {
        if (!part) return null

        // whitespace / punctuation
        if (!/^[A-Za-zÄÖÜäöüß]+$/.test(part)) {
          return <span key={`${i}-t`}>{part}</span>
        }

        if (ARTICLE_TOKEN_RE.test(part)) {
          const g = followingNounGender(i)
          const aClass = classForArticle(part, g)
          return (
            <span key={`${i}-a`} className={aClass ?? undefined}>
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
