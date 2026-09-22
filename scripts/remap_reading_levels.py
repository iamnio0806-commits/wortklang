#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shift reading levels down one notch for exam alignment.

Current A1 → 練習, A2 → A1, B1 → A2, B2 → B1.
(New exam-length B2 is added by a separate generator.)
"""
from __future__ import annotations

import json
import re
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "src" / "data" / "reading.json"

LEVEL_MAP = {
    "A1": "練習",
    "A2": "A1",
    "B1": "A2",
    "B2": "B1",
}

ID_PREFIX = {
    "練習": "uebung",
    "A1": "a1",
    "A2": "a2",
    "B1": "b1",
}


def new_id(level: str, n: int) -> str:
    return f"{ID_PREFIX[level]}-{n:02d}"


def main() -> None:
    data = json.loads(PATH.read_text(encoding="utf-8"))
    items = data["items"]

    # Keep only levels that still exist after remap (no leftover B2 yet).
    remapped = []
    counters = {lv: 0 for lv in ("練習", "A1", "A2", "B1")}
    for it in items:
        old = it["level"]
        if old not in LEVEL_MAP:
            continue
        new_lv = LEVEL_MAP[old]
        counters[new_lv] += 1
        it = dict(it)
        it["level"] = new_lv
        it["id"] = new_id(new_lv, counters[new_lv])
        remapped.append(it)

    data["levels"] = ["練習", "A1", "A2", "B1"]
    data["note"] = (
        "對齊德檢閱讀難度：練習＝熱身短文；A1／A2／B1 各由原上一級內容下調。"
        "B2 另以考場長度重寫。"
    )
    data["items"] = remapped
    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("counts", counters, "total", len(remapped))


if __name__ == "__main__":
    main()
