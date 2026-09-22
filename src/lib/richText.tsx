import type { ReactNode } from 'react'

/** Gender / article colors */
export const genderClass: Record<'der' | 'die' | 'das', string> = {
  der: 'gender-der',
  die: 'gender-die',
  das: 'gender-das',
}

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

const ARTICLE_RE = /\b(der|die|das|den|dem|des|ein|eine|einen|einem|einer|eines|Der|Die|Das|Den|Dem|Des|Ein|Eine|Einen|Einem|Einer|Eines)\b/g

const POS_RE =
  /(情態動詞|助動詞|名詞|動詞|形容詞|副詞|介詞|冠詞|代詞|連接詞|數詞)/g

function articleClass(token: string): string | null {
  const lower = token.toLowerCase()
  if (
    lower === 'der' ||
    lower === 'den' ||
    lower === 'dem' ||
    lower === 'des'
  ) {
    // den/dem/des often masculine or plural-dative; color by stem family:
    // der/den/dem/des → blue (陽性系列 / 定冠詞強標)
    if (lower === 'der' || lower === 'den' || lower === 'dem' || lower === 'des')
      return genderClass.der
  }
  if (lower === 'die') return genderClass.die
  if (lower === 'das') return genderClass.das
  // ein-forms: treat feminine eine/einer as die-color; others der-color for visibility
  if (lower === 'eine' || lower === 'einer') return genderClass.die
  if (
    lower === 'ein' ||
    lower === 'einen' ||
    lower === 'einem' ||
    lower === 'eines'
  )
    return genderClass.der
  return null
}

/**
 * Color der/die/das (and common case forms) plus Chinese POS labels in text.
 */
export function RichText({ text }: { text: string }): ReactNode {
  // Split by articles OR POS labels, keeping delimiters
  const combined = new RegExp(
    `${ARTICLE_RE.source}|${POS_RE.source}`,
    'g',
  )
  const parts = text.split(combined)
  return (
    <>
      {parts.map((part, i) => {
        if (!part) return null
        const a = articleClass(part)
        if (a) {
          return (
            <span key={`${i}-${part}`} className={a}>
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
