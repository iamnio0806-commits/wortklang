import raw from './reading.json'
import type { Level } from './vocabulary'

/** 練習 = warm-up below A1; A1–B2 aligned to Goethe/ÖSD reading difficulty. */
export type ReadingLevel = '練習' | 'A1' | 'A2' | 'B1' | 'B2'

/** Map reading tier → vocab lookup preference (練習 has no vocab CEFR). */
export function readingPreferVocabLevel(level: ReadingLevel): Level {
  return level === '練習' ? 'A1' : level
}

export type ReadingKind =
  | 'dialogue'
  | 'card'
  | 'sign'
  | 'message'
  | 'email'
  | 'story'
  | 'notice'

export type ReadingNote = {
  span: string
  zh: string
  tip?: string
}

export type ReadingPattern = {
  pattern: string
  zh: string
  example: string
}

export type ReadingItem = {
  id: string
  level: ReadingLevel
  kind: ReadingKind
  topic: string
  title: string
  titleZh: string
  text: string
  textZh: string
  notes: ReadingNote[]
  patterns: ReadingPattern[]
  tips: string[]
  focus: string[]
}

type ReadingFile = {
  levels: ReadingLevel[]
  note: string
  items: ReadingItem[]
}

const data = raw as ReadingFile

export const readingItems: ReadingItem[] = data.items
export const readingLevels: ReadingLevel[] = data.levels
export const readingNote = data.note

export const READING_KIND_LABEL: Record<ReadingKind, string> = {
  dialogue: '對話',
  card: '小卡／短述',
  sign: '告示／標示',
  message: '訊息',
  email: '郵件',
  story: '短文',
  notice: '公告',
}

export function countReadingByLevel(level: ReadingLevel): number {
  return readingItems.filter((i) => i.level === level).length
}

export function readingTopicsFor(level: ReadingLevel | '全部'): string[] {
  const pool =
    level === '全部'
      ? readingItems
      : readingItems.filter((i) => i.level === level)
  return [...new Set(pool.map((i) => i.topic))]
}
