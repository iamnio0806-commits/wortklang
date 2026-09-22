import raw from './exams.json'

export type ExamLevel = 'A1' | 'A2' | 'B1' | 'B2'

export type ExamKind =
  | 'lesen'
  | 'hoeren'
  | 'bausteine'
  | 'schreiben'
  | 'sprechen'

export type ExamItemMc = {
  id: string
  type: 'mc'
  prompt: string
  promptZh?: string
  options: string[]
  answer: number
  explainZh: string
}

export type ExamItemTf = {
  id: string
  type: 'tf'
  prompt: string
  promptZh?: string
  /** true / false / "nicht" (= Steht nicht im Text) */
  answer: true | false | 'nicht'
  explainZh: string
}

export type ExamItemGap = {
  id: string
  type: 'gap'
  prompt: string
  promptZh?: string
  answer: string
  accept?: string[]
  explainZh: string
}

export type ExamItemSchreiben = {
  id: string
  type: 'schreiben'
  prompt: string
  promptZh: string
  minWords: number
  modelAnswer: string
  checklist: string[]
}

export type ExamItemSprechen = {
  id: string
  type: 'sprechen'
  prompt: string
  promptZh: string
  cues: string[]
  modelAnswer: string
}

export type ExamItem =
  | ExamItemMc
  | ExamItemTf
  | ExamItemGap
  | ExamItemSchreiben
  | ExamItemSprechen

export type ExamSection = {
  id: string
  kind: ExamKind
  title: string
  titleZh: string
  instructions: string
  instructionsZh: string
  audioText?: string
  passage?: string
  passageZh?: string
  items: ExamItem[]
}

export type ExamPaper = {
  id: string
  level: ExamLevel
  round: 1 | 2
  title: string
  titleZh: string
  durationMin: number
  sections: ExamSection[]
}

type ExamFile = {
  note: string
  levels: ExamLevel[]
  papers: ExamPaper[]
}

const data = raw as ExamFile

export const examPapers: ExamPaper[] = data.papers
export const examLevels: ExamLevel[] = data.levels
export const examNote: string = data.note

export const EXAM_KIND_LABEL: Record<ExamKind, string> = {
  lesen: '閱讀',
  hoeren: '聽力',
  bausteine: '語法詞彙',
  schreiben: '寫作',
  sprechen: '口說',
}

export function papersForLevel(level: ExamLevel): ExamPaper[] {
  return examPapers.filter((p) => p.level === level)
}

export function getPaper(id: string): ExamPaper | undefined {
  return examPapers.find((p) => p.id === id)
}

export function countScoredItems(paper: ExamPaper): number {
  let n = 0
  for (const sec of paper.sections) {
    for (const it of sec.items) {
      if (it.type === 'mc' || it.type === 'tf' || it.type === 'gap') n += 1
    }
  }
  return n
}
