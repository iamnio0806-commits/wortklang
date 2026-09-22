/** Spaced repetition (SM-2 lite) for Wortklang self-study. */

export type SrsGrade = 'again' | 'hard' | 'good' | 'easy'

export type SrsCard = {
  id: string
  ease: number
  interval: number
  repetitions: number
  due: number
  last: number
  mastered?: boolean
}

const SRS_KEY = 'wortklang-srs-v1'
const LEGACY_LEARNED_KEY = 'wortklang-learned'

const MIN_EASE = 1.3

function now(): number {
  return Date.now()
}

function dayMs(days: number): number {
  return days * 24 * 60 * 60 * 1000
}

export function loadSrsMap(): Record<string, SrsCard> {
  try {
    const raw = localStorage.getItem(SRS_KEY)
    if (raw) {
      const parsed = JSON.parse(raw) as Record<string, SrsCard>
      if (parsed && typeof parsed === 'object') return parsed
    }
  } catch {
    /* ignore */
  }

  try {
    const legacy = localStorage.getItem(LEGACY_LEARNED_KEY)
    if (legacy) {
      const ids = JSON.parse(legacy) as string[]
      if (Array.isArray(ids)) {
        const map: Record<string, SrsCard> = {}
        const t = now()
        for (const id of ids) {
          map[id] = {
            id,
            ease: 2.5,
            interval: 1,
            repetitions: 1,
            due: t + dayMs(1),
            last: t,
          }
        }
        saveSrsMap(map)
        return map
      }
    }
  } catch {
    /* ignore */
  }
  return {}
}

export function saveSrsMap(map: Record<string, SrsCard>): void {
  localStorage.setItem(SRS_KEY, JSON.stringify(map))
}

export function isDue(card: SrsCard, at = now()): boolean {
  if (card.mastered) return false
  return card.due <= at
}

export function listDueIds(
  map: Record<string, SrsCard>,
  at = now(),
  limit = 80,
): string[] {
  return Object.values(map)
    .filter((c) => isDue(c, at))
    .sort((a, b) => a.due - b.due)
    .slice(0, limit)
    .map((c) => c.id)
}

export function countDue(map: Record<string, SrsCard>, at = now()): number {
  return Object.values(map).filter((c) => isDue(c, at)).length
}

export function enrollCard(
  map: Record<string, SrsCard>,
  id: string,
): Record<string, SrsCard> {
  const t = now()
  const existing = map[id]
  if (existing && !existing.mastered) return map
  return {
    ...map,
    [id]: {
      id,
      ease: 2.5,
      interval: 1,
      repetitions: 1,
      due: t + dayMs(1),
      last: t,
      mastered: false,
    },
  }
}

export function unenrollCard(
  map: Record<string, SrsCard>,
  id: string,
): Record<string, SrsCard> {
  const next = { ...map }
  delete next[id]
  return next
}

export function reviewCard(
  map: Record<string, SrsCard>,
  id: string,
  grade: SrsGrade,
): Record<string, SrsCard> {
  const t = now()
  const prev =
    map[id] ??
    ({
      id,
      ease: 2.5,
      interval: 0,
      repetitions: 0,
      due: t,
      last: t,
    } satisfies SrsCard)

  let { ease, interval, repetitions } = prev

  if (grade === 'again') {
    return {
      ...map,
      [id]: {
        ...prev,
        ease,
        interval: 0,
        repetitions: 0,
        due: t + 15 * 60 * 1000,
        last: t,
        mastered: false,
      },
    }
  }

  if (grade === 'hard') {
    ease = Math.max(MIN_EASE, ease - 0.15)
    interval = repetitions === 0 ? 1 : Math.max(1, Math.round(interval * 1.2))
    repetitions += 1
  } else if (grade === 'good') {
    if (repetitions === 0) interval = 1
    else if (repetitions === 1) interval = 3
    else interval = Math.max(1, Math.round(interval * ease))
    repetitions += 1
  } else {
    ease = ease + 0.15
    if (repetitions === 0) interval = 3
    else if (repetitions === 1) interval = 7
    else interval = Math.max(1, Math.round(interval * ease * 1.3))
    repetitions += 1
  }

  interval = Math.min(interval, 120)

  return {
    ...map,
    [id]: {
      ...prev,
      ease,
      interval,
      repetitions,
      due: t + dayMs(interval),
      last: t,
      mastered: interval >= 60 && grade === 'easy',
    },
  }
}

export function formatDueLabel(card: SrsCard, at = now()): string {
  if (card.mastered) return '已熟記'
  const diff = card.due - at
  if (diff <= 0) return '今日到期'
  const days = Math.ceil(diff / dayMs(1))
  if (days <= 1) return '明天'
  return `${days} 天後`
}

export const SRS_GRADE_LABEL: Record<SrsGrade, string> = {
  again: '重來',
  hard: '困難',
  good: '記得',
  easy: '簡單',
}
