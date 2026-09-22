import raw from './stories.json'

export type StoryLevel = 'A1' | 'A2'

export type StoryNote = {
  span: string
  zh: string
  tip?: string
}

export type StoryChapter = {
  id: string
  order: number
  title: string
  titleZh: string
  text: string
  textZh: string
  focus: string[]
  notes: StoryNote[]
}

export type StorySeries = {
  id: string
  level: StoryLevel
  title: string
  titleZh: string
  blurbZh: string
  chapters: StoryChapter[]
}

type StoriesFile = {
  note: string
  series: StorySeries[]
}

const data = raw as StoriesFile

export const storySeries: StorySeries[] = data.series
export const storyNote: string = data.note

export function getSeries(id: string): StorySeries | undefined {
  return storySeries.find((s) => s.id === id)
}

export function getChapter(
  seriesId: string,
  chapterId: string,
): StoryChapter | undefined {
  return getSeries(seriesId)?.chapters.find((c) => c.id === chapterId)
}
