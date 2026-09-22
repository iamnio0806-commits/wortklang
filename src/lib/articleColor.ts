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

/**
 * Color articles by the **lemma gender of the following noun** when known.
 * Fixes teaching bugs like "mit der Frau" (feminine dative) wrongly shown
 * in masculine blue just because the surface form is "der".
 *
 * Fallback: surface-form heuristic when no noun gender is available.
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
  // Without noun context, einer is usually feminine dative/genitive in A1 texts.
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
