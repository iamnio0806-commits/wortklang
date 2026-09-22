#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate a 2-year vocabulary path for Wortklang self-study.

Pace (6 study days / week; day 7 = review):
  A1–A2:  8 new / day
  B1:    12 new / day   ← ramp starts here
  B2:    16 new / day   ← finish B2 around week 76 (~530 days)
  C1:    12 new / day

Goal: B2 vocabulary done in ~500+ days; then C1 stretch.
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
# Week 76 ≈ day 532 — B2 complete within ~五百多天
PHASES = [
    (1, 22, "A1", "基礎扎根", "生活核心詞：人／家／食／行／高頻動詞", 8),
    (23, 46, "A2", "擴充輸出", "描述日常、計畫、意見與常見情境", 8),
    (47, 64, "B1", "加速衝刺", "抽象詞、連接、工作學習（開始加量）", 12),
    (65, 76, "B2", "達標 B2", "論述與正式用詞（約 500 多天內完成）", 16),
    (77, 104, "C1", "精準表達", "進階詞往 C1 推進", 12),
]

LEVEL_QUOTA = {
    "A1": 1240,
    "A2": 1300,
    "B1": 1600,
    "B2": 1500,
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
    return "C1", "精準表達", "進階詞", 12


def words_needed() -> int:
    total = 0
    for a, b, _lv, _t, _f, n in PHASES:
        total += (b - a + 1) * n * STUDY_DAYS
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

    # If still short, take any leftover from all levels
    if len(pipeline_words) < needed:
        for w in vocab:
            if w["id"] in taken:
                continue
            pipeline_words.append(w)
            taken.add(w["id"])
            if len(pipeline_words) >= needed:
                break

    if len(pipeline_words) < needed:
        raise SystemExit(
            f"Not enough vocabulary: have {len(pipeline_words)}, need {needed}"
        )

    pipeline_words = pipeline_words[:needed]
    pipeline_ids = [w["id"] for w in pipeline_words]

    grammar_topics = json.loads((DATA / "grammar.json").read_text(encoding="utf-8"))
    reading_file = json.loads((DATA / "reading.json").read_text(encoding="utf-8"))
    reading_items = reading_file["items"]

    grammar_by_level: dict[str, list[dict]] = {}
    for t in grammar_topics:
        grammar_by_level.setdefault(t["level"], []).append(t)

    reading_by_level: dict[str, list[dict]] = {}
    for it in reading_items:
        reading_by_level.setdefault(it["level"], []).append(it)

    def reading_queue_for_phase(phase_level: str, week: int) -> list[dict]:
        """Pick graded readings for the phase (C1 reuses B2; A1 early uses 練習)."""
        if phase_level == "A1":
            if week <= 8:
                return reading_by_level.get("練習", []) + reading_by_level.get("A1", [])
            return reading_by_level.get("A1", []) + reading_by_level.get("練習", [])
        if phase_level == "C1":
            return reading_by_level.get("B2", []) + reading_by_level.get("B1", [])
        return reading_by_level.get(phase_level, []) + reading_by_level.get("B2", [])

    # Round-robin cursors per level key
    grammar_cursor: dict[str, int] = {}
    reading_cursor: dict[str, int] = {}

    def next_grammar(phase_level: str) -> dict | None:
        # C1 phase still studies C1 grammar topics
        key = phase_level if phase_level in grammar_by_level else "B2"
        pool = grammar_by_level.get(key) or grammar_by_level.get("B2") or []
        if not pool:
            return None
        i = grammar_cursor.get(key, 0)
        topic = pool[i % len(pool)]
        grammar_cursor[key] = i + 1
        return topic

    def next_reading(phase_level: str, week: int) -> dict | None:
        pool = reading_queue_for_phase(phase_level, week)
        if not pool:
            return None
        key = f"{phase_level}:{week // 10}"  # soft bucket so early A1 prefers 練習
        # Use phase_level as cursor key for stable advance
        ckey = phase_level
        i = reading_cursor.get(ckey, 0)
        item = pool[i % len(pool)]
        reading_cursor[ckey] = i + 1
        return item

    weeks = []
    idx = 0
    for week in range(1, WEEKS + 1):
        level, phase_title, phase_focus, new_per_day = phase_for(week)
        week_count = new_per_day * STUDY_DAYS
        week_slice = pipeline_words[idx : idx + week_count]
        week_start = idx
        days = []
        week_grammar_ids: list[str] = []
        week_reading_ids: list[str] = []
        for d in range(1, 8):
            if d <= STUDY_DAYS:
                start = week_start + (d - 1) * new_per_day
                chunk = pipeline_words[start : start + new_per_day]
                cats = [w.get("category") or "單字" for w in chunk]
                top = max(set(cats), key=cats.count) if cats else "單字"

                # Reading every study day; grammar on Mon/Wed/Fri (1/3/5)
                reading = next_reading(level, week)
                grammar = next_grammar(level) if d in (1, 3, 5) else None
                if grammar:
                    week_grammar_ids.append(grammar["id"])
                if reading:
                    week_reading_ids.append(reading["id"])

                tip_parts = [
                    f"今日 {new_per_day} 個字",
                ]
                if reading:
                    tip_parts.append("＋閱讀")
                if grammar:
                    tip_parts.append("＋文法")
                tip_parts.append("。學會了請自己按「標記已學會」。")

                day_obj: dict = {
                    "week": week,
                    "day": d,
                    "kind": "learn",
                    "level": chunk[0]["level"] if chunk else level,
                    "titleZh": f"新字 · {top}",
                    "startIndex": start,
                    "targetCount": new_per_day,
                    "vocabIds": [w["id"] for w in chunk],
                    "tipZh": "".join(tip_parts),
                }
                if grammar:
                    day_obj["grammarId"] = grammar["id"]
                    day_obj["grammarTitleZh"] = grammar.get("title") or grammar["id"]
                if reading:
                    day_obj["readingId"] = reading["id"]
                    day_obj["readingTitleZh"] = (
                        reading.get("titleZh") or reading.get("title") or reading["id"]
                    )
                days.append(day_obj)
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
                        "grammarIds": week_grammar_ids,
                        "readingIds": week_reading_ids,
                        "tipZh": "不學新字：SRS 到期卡 → 快速過本週單字 → 重看本週文法／閱讀。",
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
        "兩年路徑：單字為主（A1–A2 每天 8；B1 起 12；B2 每天 16，約 500 多天達 B2），"
        "學習日另配 1 篇閱讀；週一／三／五再加 1 則文法。"
        "單字清單不會自動消失——學會了請自己按「標記已學會」才進 SRS。"
        "第 7 天複習到期卡＋本週文法／閱讀。"
    )

    payload = {
        "note": note,
        "meta": {
            "weeks": WEEKS,
            "studyDaysPerWeek": STUDY_DAYS,
            "totalNew": needed,
            "b2TargetWeek": 76,
            "b2TargetDaysApprox": 76 * 7,
            "newPerDayByPhase": {
                "A1": 8,
                "A2": 8,
                "B1": 12,
                "B2": 16,
                "C1": 12,
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

    # Keep TS wrapper in sync
    ts = '''/** Auto-generated by scripts/gen_vocab_path.py — 2-year study path. */
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
  grammarId?: string
  grammarTitleZh?: string
  readingId?: string
  readingTitleZh?: string
  /** Review day: grammar touched this week */
  grammarIds?: string[]
  /** Review day: readings touched this week */
  readingIds?: string[]
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
    b2TargetWeek: number
    b2TargetDaysApprox: number
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
 * Prefer fixed day.vocabIds. Kept for API compatibility — never auto-skips.
 */
export function resolveVocabDay(
  day: VocabPathDay,
  knownIds: Set<string> | ReadonlySet<string>,
): ResolvedVocabDay {
  void knownIds
  return {
    ids: [...day.vocabIds],
    skippedIds: [],
    shortfall: Math.max(0, day.targetCount - day.vocabIds.length),
  }
}
'''
    OUT_TS.write_text(ts, encoding="utf-8")

    from collections import Counter

    print("needed", needed, "pipeline", len(pipeline_ids))
    print("by level", dict(Counter(w["level"] for w in pipeline_words)))
    for a, b, lv, _t, _f, n in PHASES:
        words = (b - a + 1) * n * STUDY_DAYS
        print(f"  W{a}-{b} {lv}: {n}/day → {words} words (end ~day {b * 7})")
    # sample day 1
    d1 = weeks[0]["days"][0]
    print("sample W1D1", {k: d1.get(k) for k in ("vocabIds", "grammarId", "grammarTitleZh", "readingId", "readingTitleZh")})
    print("B2 done by week 76 (~532 days)")
    print("wrote", OUT_JSON.name, OUT_TS.name)


if __name__ == "__main__":
    main()
