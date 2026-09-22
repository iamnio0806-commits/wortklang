import raw from './vocabulary.json'

export type Gender = 'der' | 'die' | 'das' | null
export type Level = 'A1' | 'A2'
export type Category =
  | '日常'
  | '飲食'
  | '旅行'
  | '家庭'
  | '自然'
  | '工作'
  | '時間'
  | '動詞'
  | '形容詞'
  | '數字'

export interface VocabWord {
  id: string
  article: Gender
  word: string
  plural?: string
  translation: string
  phonetic: string
  category: Category
  example: string
  exampleTranslation: string
  level: Level
}

export const categories: Category[] = [
  '日常',
  '飲食',
  '旅行',
  '家庭',
  '自然',
  '工作',
  '時間',
  '動詞',
  '形容詞',
  '數字',
]

export const levels: Level[] = ['A1', 'A2']

export const vocabulary = raw as VocabWord[]

export function countByLevel(level: Level): number {
  return vocabulary.filter((w) => w.level === level).length
}
