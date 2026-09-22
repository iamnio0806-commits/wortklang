import raw from './grammar.json'
import type { Level } from './vocabulary'

export type GrammarLevel = Level

export interface GrammarExample {
  de: string
  zh: string
}

export interface GrammarFormTable {
  label: string
  headers: string[]
  rows: string[][]
}

export interface GrammarExerciseBase {
  id: string
  prompt: string
  hint: string
}

export interface GrammarMcq extends GrammarExerciseBase {
  type: 'mcq'
  options: string[]
  answer: string
}

export interface GrammarFill extends GrammarExerciseBase {
  type: 'fill'
  answer: string
  accept: string[]
}

export type GrammarExercise = GrammarMcq | GrammarFill

export interface GrammarTopic {
  id: string
  level: GrammarLevel
  category: string
  title: string
  titleDe: string
  summary: string
  points: string[]
  forms: GrammarFormTable[]
  examples: GrammarExample[]
  tips: string[]
  related: string[]
  exercises: GrammarExercise[]
}

export const grammarTopics = raw as GrammarTopic[]

export const grammarLevels: GrammarLevel[] = ['A1', 'A2', 'B1', 'B2', 'C1']

export const grammarCategories: string[] = [
  ...new Set(grammarTopics.map((t) => t.category)),
]

export function countGrammarByLevel(level: GrammarLevel): number {
  return grammarTopics.filter((t) => t.level === level).length
}

export function getGrammarTopic(id: string): GrammarTopic | undefined {
  return grammarTopics.find((t) => t.id === id)
}

export function normalizeFillAnswer(value: string): string {
  return value.trim().replace(/\s+/g, ' ')
}

export function checkFillAnswer(
  exercise: GrammarFill,
  value: string,
): boolean {
  const got = normalizeFillAnswer(value)
  const candidates = [
    exercise.answer,
    ...(exercise.accept ?? []),
  ].map(normalizeFillAnswer)
  return candidates.some(
    (c) => c === got || c.toLowerCase() === got.toLowerCase(),
  )
}
