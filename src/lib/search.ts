import type { VocabWord } from '../data/vocabulary'

/** Fold German spelling variants for tolerant search. */
export function normalizeSearch(input: string): string {
  return input
    .trim()
    .toLowerCase()
    .replace(/ä/g, 'ae')
    .replace(/ö/g, 'oe')
    .replace(/ü/g, 'ue')
    .replace(/ß/g, 'ss')
    .replace(/à|á|â|ã/g, 'a')
    .replace(/è|é|ê/g, 'e')
    .replace(/ì|í|î/g, 'i')
    .replace(/ò|ó|ô/g, 'o')
    .replace(/ù|ú|û/g, 'u')
    .replace(/[^\p{L}\p{N}\s\-_/／·.]+/gu, ' ')
    .replace(/\s+/g, ' ')
    .trim()
}

/** Also accept plain a/o/u for ä/ö/ü when comparing. */
function looseFold(s: string): string {
  return normalizeSearch(s).replace(/ae/g, 'a').replace(/oe/g, 'o').replace(/ue/g, 'u')
}

function normPair(hay: string, needle: string): { h: string; n: string; hl: string; nl: string } {
  return {
    h: normalizeSearch(hay),
    n: normalizeSearch(needle),
    hl: looseFold(hay),
    nl: looseFold(needle),
  }
}

function equalsFold(a: string, b: string): boolean {
  const { h, n, hl, nl } = normPair(a, b)
  return h === n || hl === nl
}

function startsWithFold(hay: string, needle: string): boolean {
  const { h, n, hl, nl } = normPair(hay, needle)
  if (!n) return true
  return h.startsWith(n) || hl.startsWith(nl)
}

function containsFold(hay: string, needle: string): boolean {
  const { h, n, hl, nl } = normPair(hay, needle)
  if (!n) return true
  return h.includes(n) || hl.includes(nl)
}

/** True if needle matches a whole token or token prefix (avoids ich⊂begrifflich). */
function tokenPrefixMatch(hay: string, needle: string): boolean {
  const { n, nl } = normPair(hay, needle)
  if (!n) return true
  const tokens = normalizeSearch(hay).split(/[^a-z0-9äöü]+/i).filter(Boolean)
  for (const t of tokens) {
    if (equalsFold(t, needle) || startsWithFold(t, needle)) return true
    const tl = looseFold(t)
    if (tl === nl || tl.startsWith(nl)) return true
  }
  return false
}

/** Compound parts: only head or tail (Kaufhaus←Haus), not mid false positives (Schauspieler). */
function compoundAffixMatch(hay: string, needle: string): boolean {
  const n = normalizeSearch(needle)
  if (n.length < 4) return false
  return startsWithFold(hay, needle) || endsWithFold(hay, needle)
}

function endsWithFold(hay: string, needle: string): boolean {
  const { h, n, hl, nl } = normPair(hay, needle)
  if (!n) return true
  return h.endsWith(n) || hl.endsWith(nl)
}

function isMostlyLatin(s: string): boolean {
  const n = normalizeSearch(s).replace(/\s/g, '')
  if (!n) return false
  const latin = n.replace(/[^a-z]/g, '').length
  return latin / n.length >= 0.6
}

const ARTICLES = new Set([
  'der',
  'die',
  'das',
  'den',
  'dem',
  'des',
  'ein',
  'eine',
  'einen',
  'einem',
  'einer',
  'eines',
])

export type SearchHit = {
  word: VocabWord
  score: number
}

/**
 * Score how well a vocab entry matches a query.
 * Prefers lemma / translation over example sentences so results feel like「單字」.
 */
export function scoreVocabMatch(w: VocabWord, rawQuery: string): number {
  const q = normalizeSearch(rawQuery)
  if (!q) return 1

  const tokens = q.split(' ').filter(Boolean)
  let articleHint: string | null = null
  let coreTokens = tokens

  if (tokens.length >= 2 && ARTICLES.has(tokens[0]!)) {
    articleHint = tokens[0]!
    coreTokens = tokens.slice(1)
  }

  const core = coreTokens.join(' ')
  if (!core && articleHint) return 0

  const word = w.word
  const plural = w.plural ?? ''
  const lemma = w.article ? `${w.article} ${w.word}` : w.word
  const translation = w.translation
  const phonetic = w.phonetic ?? ''
  const id = w.id
  const latin = isMostlyLatin(core)

  const zhParts = translation
    .split(/[／/、,，;；|]+/)
    .map((s) => s.trim())
    .filter(Boolean)

  let score = 0

  // Exact lemma / plural
  if (equalsFold(word, core) || equalsFold(lemma, q) || equalsFold(lemma, core)) {
    score = Math.max(score, 100)
  } else if (equalsFold(plural, core)) {
    score = Math.max(score, 94)
  } else if (startsWithFold(word, core) || startsWithFold(plural, core)) {
    score = Math.max(score, 82)
  } else if (tokenPrefixMatch(word, core) || tokenPrefixMatch(plural, core)) {
    score = Math.max(score, 74)
  } else if (compoundAffixMatch(word, core) || compoundAffixMatch(plural, core)) {
    // Krankenhaus ← Haus, Hausaufgabe ← Haus
    score = Math.max(score, 48)
  }

  // Chinese / translation senses
  if (!latin) {
    for (const part of zhParts) {
      if (equalsFold(part, core)) score = Math.max(score, 90)
      else if (startsWithFold(part, core)) score = Math.max(score, 76)
      else if (containsFold(part, core) && core.length >= 1) score = Math.max(score, 68)
    }
    if (containsFold(translation, core)) score = Math.max(score, 62)
  } else {
    for (const part of zhParts) {
      if (equalsFold(part, core)) score = Math.max(score, 90)
      else if (startsWithFold(part, core) || tokenPrefixMatch(part, core)) {
        score = Math.max(score, 72)
      }
    }
    // Do not mid-match Latin crumbs inside German gloss strings (ich⊂streichen)
    if (tokenPrefixMatch(translation, core) && core.length >= 3) {
      score = Math.max(score, 50)
    }
  }

  if (equalsFold(id, core) || startsWithFold(id, core)) score = Math.max(score, 58)
  if (tokenPrefixMatch(phonetic, core)) score = Math.max(score, 52)

  // Multi-token (no article): each token must hit lemma fields, not examples
  if (!articleHint && tokens.length > 1) {
    const lemmaHay = [lemma, word, plural, translation, phonetic, id].join(' ')
    const allHit = tokens.every(
      (t) =>
        tokenPrefixMatch(lemmaHay, t) ||
        containsFold(translation, t) ||
        compoundAffixMatch(word, t) ||
        compoundAffixMatch(plural, t),
    )
    if (allHit) score = Math.max(score, 70)
    else return 0
  }

  if (articleHint) {
    const art = w.article
    const artOk =
      art !== null &&
      (equalsFold(art, articleHint) ||
        (['den', 'dem', 'des'].includes(articleHint) && art === 'der') ||
        (articleHint === 'die' && art === 'die') ||
        (['ein', 'einen', 'einem', 'eines'].includes(articleHint) &&
          (art === 'der' || art === 'das')) ||
        (['eine', 'einer'].includes(articleHint) && art === 'die'))
    if (!artOk) return 0
    if (score > 0) score += 10
  }

  // Examples intentionally ignored — search should return 單字, not sentence hits
  return score
}

export function searchVocabulary(
  words: VocabWord[],
  rawQuery: string,
): VocabWord[] {
  const q = rawQuery.trim()
  if (!q) return words

  const hits: SearchHit[] = []
  for (const w of words) {
    const score = scoreVocabMatch(w, q)
    if (score > 0) hits.push({ word: w, score })
  }

  hits.sort((a, b) => {
    if (b.score !== a.score) return b.score - a.score
    // Prefer shorter lemmas when scores tie (Haus before Krankenhaus)
    const len = a.word.word.length - b.word.word.length
    if (len !== 0) return len
    const lv = a.word.level.localeCompare(b.word.level)
    if (lv !== 0) return lv
    return a.word.word.localeCompare(b.word.word, 'de')
  })

  return hits.map((h) => h.word)
}

/** Grammar / free-text search: title first, examples last. */
export function scoreTextFields(
  rawQuery: string,
  fields: { primary: string[]; secondary?: string[]; weak?: string[] },
): number {
  const q = normalizeSearch(rawQuery)
  if (!q) return 1
  let score = 0
  for (const p of fields.primary) {
    if (equalsFold(p, q)) score = Math.max(score, 100)
    else if (startsWithFold(p, q) || tokenPrefixMatch(p, q)) score = Math.max(score, 80)
    else if (containsFold(p, q) && q.length >= 2) score = Math.max(score, 60)
  }
  for (const s of fields.secondary ?? []) {
    if (containsFold(s, q) && q.length >= 2) score = Math.max(score, 40)
  }
  if (score === 0 && q.length >= 4) {
    for (const w of fields.weak ?? []) {
      if (containsFold(w, q)) score = Math.max(score, 12)
    }
  }
  return score
}
