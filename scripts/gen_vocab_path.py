#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate a 2-year vocabulary path for Wortklang self-study.

Pace (study days Mon–Sat; day 7 = review):
  A1–B1:  8 new / day
  B2:    12 new / day
  C1:    14 new / day

Goal: cover all A1+A2, large B1/B2, and most C1 within 104 weeks.
Runtime skip of already-learned words is handled in vocabPath.ts
using pipeline + startIndex.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "src" / "data"
VOCAB = DATA / "vocabulary.json"
OUT_JSON = DATA / "vocabPath.json"
OUT_TS = DATA / "vocabPath.ts"

STUDY_DAYS = 6
WEEKS = 104

# (fromWeek, toWeek, level, titleZh, focusZh, newPerDay)
PHASES = [
    (1, 22, "A1", "基礎扎根", "生活核心詞：人／家／食／行／高頻動詞", 8),
    (23, 46, "A2", "擴充輸出", "描述日常、計畫、意見與常見情境", 8),
    (47, 74, "B1", "獨立運用", "抽象詞、連接、工作學習與社會話題", 8),
    (75, 92, "B2", "流暢論述", "論點、細膩形容、正式場合用詞（加量）", 12),
    (93, 104, "C1", "精準表達", "學術／專業向進階詞（加量衝刺）", 14),
]

LEVEL_QUOTA = {
    "A1": 1078,
    "A2": 1162,
    "B1": 1500,
    "B2": 1300,
    "C1": 1200,
}

CAT_ORDER = [
    "家庭",
    "動詞",
    "日常",
    "飲食",
    "時間",
    "數字",
    "工作",
    "旅行",
    "自然",
    "形容詞",
]


def phase_for(week: int) -> tuple[str, str, str, int]:
    for a, b, level, title, focus, n in PHASES:
        if a <= week <= b:
            return level, title, focus, n
    return "C1", "精準表達", "進階詞", 14


def words_needed() -> int:
    total = 0
    for a, b, _lv, _t, _f, n in PHASES:
        weeks = b - a + 1
        total += weeks * n * STUDY_DAYS
    return total


def order_level(words: list[dict], level: str) -> list[dict]:
    if level in ("A1", "A2"):
        return list(words)

    def key(w: dict):
        cat = w.get("category") or ""
        try:
            ci = CAT_ORDER.index(cat)
        except ValueError:
            ci = 99
        art_rank = 0 if w.get("article") else 1
        return (ci, art_rank, w.get("word", "").lower())

    return sorted(words, key=key)


def main() -> None:
    needed = words_needed()
    vocab = json.loads(VOCAB.read_text(encoding="utf-8"))
    by_level: dict[str, list[dict]] = {lv: [] for lv in LEVEL_QUOTA}
    for w in vocab:
        lv = w.get("level")
        if lv in by_level:
            by_level[lv].append(w)

    pipeline_words: list[dict] = []
    for lv, quota in LEVEL_QUOTA.items():
        ordered = order_level(by_level[lv], lv)
        pipeline_words.extend(ordered[:quota])

    taken = {w["id"] for w in pipeline_words}
    if len(pipeline_words) < needed:
        for lv in ("B1", "B2", "C1"):
            for w in order_level(by_level[lv], lv):
                if w["id"] in taken:
                    continue
                pipeline_words.append(w)
                taken.add(w["id"])
                if len(pipeline_words) >= needed:
                    break
            if len(pipeline_words) >= needed:
                break

    pipeline_words = pipeline_words[:needed]
    assert len(pipeline_words) == needed, (len(pipeline_words), needed)
    pipeline_ids = [w["id"] for w in pipeline_words]

    weeks = []
    idx = 0
    for week in range(1, WEEKS + 1):
        level, phase_title, phase_focus, new_per_day = phase_for(week)
        week_count = new_per_day * STUDY_DAYS
        week_slice = pipeline_words[idx : idx + week_count]
        week_start = idx
        days = []
        for d in range(1, 8):
            if d <= STUDY_DAYS:
                start = week_start + (d - 1) * new_per_day
                chunk = pipeline_words[start : start + new_per_day]
                cats = [w.get("category") or "單字" for w in chunk]
                top = max(set(cats), key=cats.count) if cats else "單字"
                days.append(
                    {
                        "week": week,
                        "day": d,
                        "kind": "learn",
                        "level": chunk[0]["level"] if chunk else level,
                        "titleZh": f"新字 · {top}",
                        "startIndex": start,
                        "targetCount": new_per_day,
                        "vocabIds": [w["id"] for w in chunk],
                        "tipZh": (
                            f"今日目標 {new_per_day} 個生字（已學會會自動跳過並往後補）。"
                            "名詞連冠詞記；標記已學會進入 SRS。"
                        ),
                    }
                )
            else:
                days.append(
                    {
                        "week": week,
                        "day": d,
                        "kind": "review",
                        "level": level,
                        "titleZh": "本週複習日",
                        "startIndex": week_start,
                        "targetCount": week_count,
                        "vocabIds": [w["id"] for w in week_slice],
                        "tipZh": "不學新字：先打 SRS 到期卡，再把本週字快速過一輪。",
                    }
                )

        weeks.append(
            {
                "week": week,
                "level": level,
                "phaseZh": phase_title,
                "titleZh": f"第 {week} 週 · {phase_title}",
                "focusZh": phase_focus,
                "newPerDay": new_per_day,
                "newCount": len(week_slice),
                "startIndex": week_start,
                "days": days,
            }
        )
        idx += week_count

    assert idx == needed, (idx, needed)

    note = (
        "兩年單字路徑（目標 C1）：A1–B1 每天 8 字；B2 起每天 12 字；C1 每天 14 字"
        "（一週 6 天新字＋1 天複習）。已學會的字輪到時會自動跳過並往後補。"
        "請搭配 SRS 標記已學會。文法／閱讀之後再疊加。"
    )

    payload = {
        "note": note,
        "meta": {
            "weeks": WEEKS,
            "studyDaysPerWeek": STUDY_DAYS,
            "totalNew": needed,
            "newPerDayByPhase": {
                "A1": 8,
                "A2": 8,
                "B1": 8,
                "B2": 12,
                "C1": 14,
            },
            "phases": [
                {
                    "fromWeek": a,
                    "toWeek": b,
                    "level": lv,
                    "titleZh": t,
                    "focusZh": f,
                    "newPerDay": n,
                }
                for a, b, lv, t, f, n in PHASES
            ],
        },
        "pipeline": pipeline_ids,
        "weeks": weeks,
    }

    OUT_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    OUT_TS.write_text(
        """/** Auto-generated by scripts/gen_vocab_path.py — 2-year vocab path. */
import raw from './vocabPath.json'

export type VocabPathDayKind = 'learn' | 'review'

export type VocabPathDay = {
  week: number
  day: number
  kind: VocabPathDayKind
  level: string
  titleZh: string
  /** Index into VOCAB_PATH_PIPELINE for this day's scheduled start. */
  startIndex: number
  /** How many *new* (not-yet-learned) words to collect today. */
  targetCount: number
  /** Default slice (before skip/backfill). */
  vocabIds: string[]
  tipZh: string
}

export type VocabPathWeek = {
  week: number
  level: string
  phaseZh: string
  titleZh: string
  focusZh: string
  newPerDay: number
  newCount: number
  startIndex: number
  days: VocabPathDay[]
}

export type VocabPathPhase = {
  fromWeek: number
  toWeek: number
  level: string
  titleZh: string
  focusZh: string
  newPerDay: number
}

type File = {
  note: string
  meta: {
    weeks: number
    studyDaysPerWeek: number
    totalNew: number
    newPerDayByPhase: Record<string, number>
    phases: VocabPathPhase[]
  }
  pipeline: string[]
  weeks: VocabPathWeek[]
}

const data = raw as File

export const VOCAB_PATH_NOTE = data.note
export const VOCAB_PATH_META = data.meta
export const VOCAB_PATH_WEEKS: VocabPathWeek[] = data.weeks
export const VOCAB_PATH_PHASES: VocabPathPhase[] = data.meta.phases
export const VOCAB_PATH_PIPELINE: string[] = data.pipeline

export function getVocabPathWeek(week: number): VocabPathWeek | undefined {
  return VOCAB_PATH_WEEKS.find((w) => w.week === week)
}

export function getVocabPathDay(
  week: number,
  day: number,
): VocabPathDay | undefined {
  return getVocabPathWeek(week)?.days.find((d) => d.day === day)
}

export type ResolvedVocabDay = {
  ids: string[]
  skippedIds: string[]
  /** True if pipeline ran out before filling targetCount. */
  shortfall: number
}

/**
 * Build today's list: skip ids already learned (in `knownIds`),
 * walk forward on the pipeline until `targetCount` fresh words.
 */
export function resolveVocabDay(
  day: VocabPathDay,
  knownIds: Set<string> | ReadonlySet<string>,
): ResolvedVocabDay {
  if (day.kind === 'review') {
    // Review: prefer words already enrolled; fall back to scheduled list.
    const enrolled = day.vocabIds.filter((id) => knownIds.has(id))
    const ids = enrolled.length ? enrolled : day.vocabIds
    return { ids, skippedIds: [], shortfall: 0 }
  }

  const ids: string[] = []
  const skippedIds: string[] = []
  let i = day.startIndex
  const pipe = VOCAB_PATH_PIPELINE
  while (ids.length < day.targetCount && i < pipe.length) {
    const id = pipe[i]
    i += 1
    if (knownIds.has(id)) {
      skippedIds.push(id)
      continue
    }
    ids.push(id)
  }
  return {
    ids,
    skippedIds,
    shortfall: Math.max(0, day.targetCount - ids.length),
  }
}
""",
        encoding="utf-8",
    )

    from collections import Counter

    print("needed", needed, "pipeline", len(pipeline_ids))
    print("by level", dict(Counter(w["level"] for w in pipeline_words)))
    for a, b, lv, _t, _f, n in PHASES:
        print(f"  W{a}-{b} {lv}: {n}/day → {(b-a+1)*n*STUDY_DAYS} words")
    print("wrote", OUT_JSON.name, OUT_TS.name)


if __name__ == "__main__":
    main()
