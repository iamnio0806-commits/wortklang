#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate a 2-year vocabulary path for Wortklang self-study.

Goal: solid B2, stretch toward C1 in ~104 weeks.
Pace: 8 new words × 6 study days / week (= 48 new/week), day 7 = review.
Total new lemmas ≈ 4,992 — covers all A1+A2, core B1/B2, C1 starter.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "src" / "data"
VOCAB = DATA / "vocabulary.json"
OUT_JSON = DATA / "vocabPath.json"
OUT_TS = DATA / "vocabPath.ts"

NEW_PER_DAY = 8
STUDY_DAYS = 6
WEEKS = 104
WORDS_PER_WEEK = NEW_PER_DAY * STUDY_DAYS  # 48
TOTAL = WORDS_PER_WEEK * WEEKS  # 4992

# B1+ within-level category preference (A1/A2 keep vocabulary.json beginner order).
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

# How many lemmas to pull from each level (priority fill).
LEVEL_QUOTA = {
    "A1": 1078,  # all — file order (beginner-friendly)
    "A2": 1162,  # all — file order
    "B1": 1500,  # core slice by category
    "B2": 1000,  # core slice by category
    "C1": 252,  # starter (~5 weeks)
}

PHASES = [
    (1, 22, "A1", "基礎扎根", "生活核心詞：人／家／食／行／高頻動詞"),
    (23, 46, "A2", "擴充輸出", "描述日常、計畫、意見與常見情境"),
    (47, 77, "B1", "獨立運用", "抽象詞、連接、工作學習與社會話題"),
    (78, 98, "B2", "流暢論述", "論點、細膩形容、正式場合用詞"),
    (99, 104, "C1", "精準表達", "學術／專業向進階詞（先打底）"),
]


def phase_for(week: int) -> tuple[str, str, str]:
    for a, b, level, title, focus in PHASES:
        if a <= week <= b:
            return level, title, focus
    return "C1", "精準表達", "進階詞"


def order_level(words: list[dict], level: str) -> list[dict]:
    """A1/A2: keep JSON order. B1+: category preference."""
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
    vocab = json.loads(VOCAB.read_text(encoding="utf-8"))
    by_level: dict[str, list[dict]] = {lv: [] for lv in LEVEL_QUOTA}
    for w in vocab:
        lv = w.get("level")
        if lv in by_level:
            by_level[lv].append(w)

    pipeline: list[dict] = []
    for lv, quota in LEVEL_QUOTA.items():
        ordered = order_level(by_level[lv], lv)
        take = ordered[:quota]
        pipeline.extend(take)

    if len(pipeline) < TOTAL:
        # top up from remaining B1→C1 not yet taken
        taken = {w["id"] for w in pipeline}
        for lv in ("B1", "B2", "C1"):
            for w in order_level(by_level[lv], lv):
                if w["id"] in taken:
                    continue
                pipeline.append(w)
                taken.add(w["id"])
                if len(pipeline) >= TOTAL:
                    break
            if len(pipeline) >= TOTAL:
                break

    pipeline = pipeline[:TOTAL]
    assert len(pipeline) == TOTAL, len(pipeline)

    weeks = []
    idx = 0
    for week in range(1, WEEKS + 1):
        level, phase_title, phase_focus = phase_for(week)
        week_words = pipeline[idx : idx + WORDS_PER_WEEK]
        idx += WORDS_PER_WEEK
        days = []
        for d in range(1, 8):
            if d <= STUDY_DAYS:
                chunk = week_words[(d - 1) * NEW_PER_DAY : d * NEW_PER_DAY]
                ids = [w["id"] for w in chunk]
                # title from dominant category
                cats = [w.get("category") or "單字" for w in chunk]
                top = max(set(cats), key=cats.count) if cats else "單字"
                days.append(
                    {
                        "week": week,
                        "day": d,
                        "kind": "learn",
                        "level": chunk[0]["level"] if chunk else level,
                        "titleZh": f"新字 · {top}",
                        "vocabIds": ids,
                        "tipZh": "每個名詞連冠詞一起記；標記已學會會進入 SRS（1→3→7 天複習）。",
                    }
                )
            else:
                ids = [w["id"] for w in week_words]
                days.append(
                    {
                        "week": week,
                        "day": d,
                        "kind": "review",
                        "level": level,
                        "titleZh": "本週複習日",
                        "vocabIds": ids,
                        "tipZh": "不要學新字：打開 SRS 到期卡，並把本週 48 字快速過一輪。",
                    }
                )

        # week title from first learn day categories
        weeks.append(
            {
                "week": week,
                "level": level,
                "phaseZh": phase_title,
                "titleZh": f"第 {week} 週 · {phase_title}",
                "focusZh": phase_focus,
                "newCount": len(week_words),
                "days": days,
            }
        )

    note = (
        "兩年單字路徑（目標 B2，衝刺 C1）：每週 6 天×8 個新字＝48 字，"
        "第 7 天只複習。順序 A1 全 → A2 全 → B1 核心 → B2 核心 → C1 打底。"
        "務必搭配 SRS：學會的字會自動回來重測。文法／閱讀之後再疊加，"
        "這一階段先把詞彙量與冠詞記牢。"
    )

    payload = {
        "note": note,
        "meta": {
            "weeks": WEEKS,
            "newPerDay": NEW_PER_DAY,
            "studyDaysPerWeek": STUDY_DAYS,
            "wordsPerWeek": WORDS_PER_WEEK,
            "totalNew": TOTAL,
            "phases": [
                {
                    "fromWeek": a,
                    "toWeek": b,
                    "level": lv,
                    "titleZh": t,
                    "focusZh": f,
                }
                for a, b, lv, t, f in PHASES
            ],
        },
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
  vocabIds: string[]
  tipZh: string
}

export type VocabPathWeek = {
  week: number
  level: string
  phaseZh: string
  titleZh: string
  focusZh: string
  newCount: number
  days: VocabPathDay[]
}

export type VocabPathPhase = {
  fromWeek: number
  toWeek: number
  level: string
  titleZh: string
  focusZh: string
}

type File = {
  note: string
  meta: {
    weeks: number
    newPerDay: number
    studyDaysPerWeek: number
    wordsPerWeek: number
    totalNew: number
    phases: VocabPathPhase[]
  }
  weeks: VocabPathWeek[]
}

const data = raw as File

export const VOCAB_PATH_NOTE = data.note
export const VOCAB_PATH_META = data.meta
export const VOCAB_PATH_WEEKS: VocabPathWeek[] = data.weeks
export const VOCAB_PATH_PHASES: VocabPathPhase[] = data.meta.phases

export function getVocabPathWeek(week: number): VocabPathWeek | undefined {
  return VOCAB_PATH_WEEKS.find((w) => w.week === week)
}

export function getVocabPathDay(
  week: number,
  day: number,
): VocabPathDay | undefined {
  return getVocabPathWeek(week)?.days.find((d) => d.day === day)
}
""",
        encoding="utf-8",
    )

    # summary
    from collections import Counter

    lv = Counter(w["level"] for w in pipeline)
    print("generated", TOTAL, "words across", WEEKS, "weeks")
    print("by level:", dict(lv))
    print("wrote", OUT_JSON, OUT_TS)


if __name__ == "__main__":
    main()
