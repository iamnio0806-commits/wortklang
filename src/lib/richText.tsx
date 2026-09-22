import type { ReactNode } from 'react'
import { classForArticle } from './articleColor'

export { genderClass } from './articleColor'

/** Part-of-speech colors */
export const posClass: Record<string, string> = {
  名詞: 'pos-noun',
  動詞: 'pos-verb',
  形容詞: 'pos-adj',
  副詞: 'pos-adv',
  介詞: 'pos-prep',
  冠詞: 'pos-art',
  代詞: 'pos-pron',
  連接詞: 'pos-conj',
  數詞: 'pos-num',
  情態動詞: 'pos-verb',
  助動詞: 'pos-verb',
  其他: 'pos-other',
}

const ARTICLE_RE =
  /\b(der|die|das|den|dem|des|ein|eine|einen|einem|einer|eines|Der|Die|Das|Den|Dem|Des|Ein|Eine|Einen|Einem|Einer|Eines)\b/g

const POS_RE =
  /(情態動詞|助動詞|名詞|動詞|形容詞|副詞|介詞|冠詞|代詞|連接詞|數詞)/g

/**
 * Color der/die/das (and common case forms) plus Chinese POS labels in text.
 * When a noun follows an article, prefer that noun's lemma gender for color
 * (requires optional resolveGender callback from vocab index).
 */
export function RichText({
  text,
  resolveGender,
}: {
  text: string
  resolveGender?: (nounToken: string) => 'der' | 'die' | 'das' | null
}): ReactNode {
  const combined = new RegExp(
    `${ARTICLE_RE.source}|${POS_RE.source}`,
    'g',
  )
  const parts = text.split(combined)

  return (
    <>
      {parts.map((part, i) => {
        if (!part) return null
        const a = classForArticle(part)
        if (a) {
          let cls = a
          if (resolveGender) {
            // look ahead for next alphabetic German-looking token
            for (let j = i + 1; j < parts.length; j++) {
              const nxt = parts[j]
              if (!nxt) continue
              if (
                /^(情態動詞|助動詞|名詞|動詞|形容詞|副詞|介詞|冠詞|代詞|連接詞|數詞)$/.test(
                  nxt,
                )
              ) {
                break
              }
              if (/^[A-Za-zÄÖÜäöüß]+$/.test(nxt)) {
                if (classForArticle(nxt)) continue
                const g = resolveGender(nxt)
                const better = classForArticle(part, g)
                if (better) cls = better
                break
              }
              if (nxt.trim()) break
            }
          }
          return (
            <span key={`${i}-${part}`} className={cls}>
              {part}
            </span>
          )
        }
        const p = posClass[part]
        if (p) {
          return (
            <span key={`${i}-${part}`} className={p}>
              {part}
            </span>
          )
        }
        return <span key={`${i}-${part}`}>{part}</span>
      })}
    </>
  )
}

/** @deprecated use RichText — kept as alias for call sites */
export function ArticleText({ text }: { text: string }) {
  return <RichText text={text} />
}

export function PosLabel({
  type,
  as: Tag = 'span',
}: {
  type: string
  as?: 'span' | 'dd' | 'strong'
}) {
  const cls = posClass[type] ?? 'pos-other'
  return (
    <Tag className={`type-pill pos-label ${cls}`}>{type}</Tag>
  )
}
