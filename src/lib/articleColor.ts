import type { Gender } from '../data/vocabulary'

/** Gender / article colors (shared CSS class names). */
export const genderClass: Record<'der' | 'die' | 'das', string> = {
  der: 'gender-der',
  die: 'gender-die',
  das: 'gender-das',
}

/** Definite / indefinite article tokens we color in German prose. */
export const ARTICLE_TOKEN_RE =
  /^(der|die|das|den|dem|des|ein|eine|einen|einem|einer|eines)$/i

const WORD_RE = /^[A-Za-zÄÖÜäöüß]+$/

/**
 * Find lemma gender of the noun this article belongs to.
 * Skips further articles and a few modifiers (adj / unknown) so
 * "mit der Frau" and "in einem kleinen Haus" both resolve correctly.
 *
 * Color must come from the noun's gender — never from the surface form
 * der/die/das alone when a noun gender is known.
 */
export function findFollowingNounGender(
  tokens: string[],
  articleIndex: number,
  lookupNounGender: (token: string) => Gender | null | undefined,
): Gender | null {
  let skippedModifiers = 0
  for (let j = articleIndex + 1; j < tokens.length; j++) {
    const p = tokens[j]
    if (!p) continue
    if (!WORD_RE.test(p)) {
      if (p.trim() === '') continue
      break
    }
    if (ARTICLE_TOKEN_RE.test(p)) continue

    const g = lookupNounGender(p)
    if (g === 'der' || g === 'die' || g === 'das') return g

    // Adjective / verb / unknown between article and noun
    skippedModifiers += 1
    if (skippedModifiers >= 3) break
  }
  return null
}

/**
 * CSS class for an article token.
 * Prefer following noun gender; surface-form is fallback only.
 */
export function classForArticle(
  token: string,
  followingGender?: Gender | null,
): string | null {
  if (
    followingGender === 'der' ||
    followingGender === 'die' ||
    followingGender === 'das'
  ) {
    return genderClass[followingGender]
  }

  const lower = token.toLowerCase()
  if (lower === 'die' || lower === 'eine') return genderClass.die
  if (lower === 'das') return genderClass.das
  if (lower === 'einer') return genderClass.die
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
  return null
}
