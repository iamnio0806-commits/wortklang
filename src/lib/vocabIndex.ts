import { vocabulary, type Level, type VocabWord } from '../data/vocabulary'
import { buildVerb } from './enrich'

export type VocabHit = {
  id: string
  word: string
  article: VocabWord['article']
  level: Level
  translation: string
}

type IndexBucket = VocabHit[]

const LEVEL_RANK: Record<Level, number> = {
  A1: 0,
  A2: 1,
  B1: 2,
  B2: 3,
  C1: 4,
}

/** Tokens we color as articles but never treat as lemma links. */
const ARTICLE_TOKENS = new Set([
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

/** Very common function words — skip even if present as lemmas. */
const SKIP = new Set([
  'ich',
  'du',
  'er',
  'sie',
  'es',
  'wir',
  'ihr',
  'mich',
  'dich',
  'ihn',
  'uns',
  'euch',
  'mir',
  'dir',
  'ihm',
  'ihr',
  'ihnen',
  'mein',
  'dein',
  'unser',
  'euer',
  'und',
  'oder',
  'aber',
  'denn',
  'wenn',
  'weil',
  'dass',
  'daß',
  'als',
  'ob',
  'mit',
  'ohne',
  'für',
  'von',
  'zu',
  'zum',
  'zur',
  'im',
  'ins',
  'am',
  'ans',
  'vom',
  'beim',
  'in',
  'an',
  'auf',
  'aus',
  'bei',
  'nach',
  'vor',
  'über',
  'unter',
  'neben',
  'zwischen',
  'durch',
  'gegen',
  'um',
  'nicht',
  'auch',
  'noch',
  'schon',
  'nur',
  'sehr',
  'hier',
  'dort',
  'wo',
  'was',
  'wer',
  'wie',
  'wann',
  'warum',
  'ja',
  'nein',
  'bitte',
  'mal',
  'so',
  'dann',
  'doch',
  'also',
  'alle',
  'alles',
  'etwas',
  'nichts',
  'man',
  'diese',
  'dieser',
  'dieses',
  'jenes',
  'mal',
  'so',
  'dann',
  'doch',
  'also',
  'alle',
  'alles',
  'etwas',
  'nichts',
  'man',
])

function addForm(map: Map<string, IndexBucket>, form: string, hit: VocabHit) {
  const key = form.trim().toLowerCase()
  if (!key || key.length < 2) return
  if (ARTICLE_TOKENS.has(key)) return
  const bucket = map.get(key)
  if (!bucket) {
    map.set(key, [hit])
    return
  }
  if (!bucket.some((h) => h.id === hit.id)) bucket.push(hit)
}

function addVerbForms(map: Map<string, IndexBucket>, hit: VocabHit, lemma: string) {
  const verb = buildVerb(lemma)
  if (!verb) return
  const forms = [
    verb.infinitive,
    verb.present.ich,
    verb.present.du,
    verb.present.er,
    verb.present.wir,
    verb.present.ihr,
    verb.present.sie,
    verb.preterite,
    verb.participle,
  ]
  for (const form of forms) {
    // "stehe auf" / "dankte (an)" → index full + first token
    const cleaned = form.replace(/\([^)]*\)/g, '').trim()
    if (!cleaned) continue
    addForm(map, cleaned, hit)
    for (const token of cleaned.split(/\s+/)) {
      addForm(map, token, hit)
    }
  }
  if (verb.separable) addForm(map, verb.separable, hit)
}

function buildIndex(): Map<string, IndexBucket> {
  const map = new Map<string, IndexBucket>()
  for (const w of vocabulary) {
    const hit: VocabHit = {
      id: w.id,
      word: w.word,
      article: w.article,
      level: w.level,
      translation: w.translation,
    }
    addForm(map, w.word, hit)
    if (w.plural) addForm(map, w.plural, hit)
    if (w.category === '動詞') addVerbForms(map, hit, w.word)
  }
  return map
}

const INDEX = buildIndex()

function pickHit(
  bucket: IndexBucket,
  preferLevel?: Level,
  preferId?: string,
): VocabHit {
  if (preferId) {
    const self = bucket.find((h) => h.id === preferId)
    if (self) return self
  }
  if (preferLevel) {
    const same = bucket.find((h) => h.level === preferLevel)
    if (same) return same
  }
  return [...bucket].sort(
    (a, b) => LEVEL_RANK[a.level] - LEVEL_RANK[b.level],
  )[0]
}

/** Light German ending strip to recover lemma from inflected forms. */
function formCandidates(raw: string): string[] {
  const t = raw.toLowerCase()
  const out: string[] = [t]
  const tryPush = (s: string) => {
    if (s.length >= 2 && !out.includes(s)) out.push(s)
  }

  if (t.endsWith('tem') && t.length > 5) tryPush(t.slice(0, -3)) // gutem → gut? weak
  if (t.endsWith('ten') && t.length > 5) tryPush(t.slice(0, -2))
  if (t.endsWith('tes') && t.length > 5) tryPush(t.slice(0, -2))
  if (t.endsWith('te') && t.length > 4) tryPush(t.slice(0, -2))
  if (t.endsWith('st') && t.length > 4) tryPush(t.slice(0, -2)) // gehst → geh
  if (t.endsWith('t') && t.length > 3) tryPush(t.slice(0, -1))
  if (t.endsWith('en') && t.length > 4) {
    tryPush(t.slice(0, -2))
    tryPush(t) // infinitive already
  }
  if (t.endsWith('es') && t.length > 4) tryPush(t.slice(0, -2))
  if (t.endsWith('er') && t.length > 4) tryPush(t.slice(0, -2))
  if (t.endsWith('em') && t.length > 4) tryPush(t.slice(0, -2))
  if (t.endsWith('en') && t.length > 4) tryPush(t.slice(0, -1)) // Knaben-style
  if (t.endsWith('n') && t.length > 3) tryPush(t.slice(0, -1))
  if (t.endsWith('s') && t.length > 3) tryPush(t.slice(0, -1))
  // separable verb particle leftovers ignored

  return out
}

export function lookupVocabToken(
  token: string,
  opts?: { preferLevel?: Level; preferId?: string },
): VocabHit | null {
  const cleaned = token.replace(/^[^A-Za-zÄÖÜäöüß]+|[^A-Za-zÄÖÜäöüß]+$/g, '')
  if (!cleaned) return null
  const lower = cleaned.toLowerCase()
  if (ARTICLE_TOKENS.has(lower) || SKIP.has(lower)) return null

  for (const cand of formCandidates(cleaned)) {
    if (SKIP.has(cand) || ARTICLE_TOKENS.has(cand)) continue
    const bucket = INDEX.get(cand)
    if (bucket?.length) {
      return pickHit(bucket, opts?.preferLevel, opts?.preferId)
    }
  }
  return null
}

export function getVocabById(id: string): VocabWord | undefined {
  return vocabulary.find((w) => w.id === id)
}
