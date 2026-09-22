import type { ReactNode } from 'react'
import type { Level } from '../data/vocabulary'
import {
  ARTICLE_TOKEN_RE,
  classForArticle,
  findFollowingNounGender,
} from './articleColor'
import { lookupVocabToken, type VocabHit } from './vocabIndex'

/**
 * Render German text with:
 * - article colors from the **following noun's gender** (not surface der/die/das alone)
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
  const parts = text.split(/([A-Za-zÄÖÜäöüß]+)/)

  const lookupNounGender = (token: string) => {
    const hit = lookupVocabToken(token, { preferLevel, preferId })
    return hit?.article ?? null
  }

  return (
    <>
      {parts.map((part, i) => {
        if (!part) return null

        if (!/^[A-Za-zÄÖÜäöüß]+$/.test(part)) {
          return <span key={`${i}-t`}>{part}</span>
        }

        if (ARTICLE_TOKEN_RE.test(part)) {
          const g = findFollowingNounGender(parts, i, lookupNounGender)
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
