#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reorder A1 (and lightly A2) vocabulary for beginner-friendly progression."""
from __future__ import annotations

import json
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "src" / "data" / "vocabulary.json"

# First-seen wins. Stages: people → home → city/school → food → travel →
# time/numbers → core verbs → basic adjectives → leftovers by category.
BEGINNER_PRIORITY: list[str] = [
    # people + family (best for articles)
    "Mann",
    "Frau",
    "Kind",
    "Vater",
    "Mutter",
    "Eltern",
    "Bruder",
    "Schwester",
    "Freund",
    "Freundin",
    "Familie",
    "Name",
    "Person",
    "Leute",
    "Junge",
    "Mädchen",
    "Lehrer",
    "Lehrerin",
    "Student",
    "Studentin",
    "Arzt",
    "Ärztin",
    # core verbs early — identity / existence first
    "sein",
    "haben",
    "heißen",
    "werden",
    "können",
    "müssen",
    "wollen",
    "möchten",
    "dürfen",
    "sollen",
    "mögen",
    "kommen",
    "gehen",
    "machen",
    "sprechen",
    "lernen",
    "verstehen",
    "wohnen",
    # home + everyday objects
    "Haus",
    "Wohnung",
    "Zimmer",
    "Küche",
    "Bad",
    "Badezimmer",
    "Tür",
    "Fenster",
    "Tisch",
    "Stuhl",
    "Bett",
    "Sofa",
    "Schrank",
    "Buch",
    "Handy",
    "Telefon",
    "Schlüssel",
    "Tasche",
    "Geld",
    "Papier",
    "Stift",
    # city / school
    "Stadt",
    "Dorf",
    "Land",
    "Schule",
    "Universität",
    "Klasse",
    "Straße",
    "Platz",
    "Adresse",
    "Weg",
    "Park",
    "Geschäft",
    "Supermarkt",
    "Markt",
    # food & drink
    "Brot",
    "Wasser",
    "Milch",
    "Kaffee",
    "Tee",
    "Apfel",
    "Banane",
    "Obst",
    "Gemüse",
    "Fleisch",
    "Fisch",
    "Käse",
    "Ei",
    "Reis",
    "Suppe",
    "Salat",
    "Essen",
    "Frühstück",
    "Mittagessen",
    "Abendessen",
    "Restaurant",
    "Café",
    # transport
    "Auto",
    "Bus",
    "Zug",
    "Bahn",
    "Fahrrad",
    "Ticket",
    "Fahrkarte",
    "Bahnhof",
    "Flughafen",
    "Taxi",
    "Haltestelle",
    # time
    "Tag",
    "Woche",
    "Monat",
    "Jahr",
    "Uhr",
    "Stunde",
    "Minute",
    "Morgen",
    "Abend",
    "Nacht",
    "Heute",
    "Zeit",
    "Termin",
    # numbers & money
    "eins",
    "zwei",
    "drei",
    "vier",
    "fünf",
    "sechs",
    "sieben",
    "acht",
    "neun",
    "zehn",
    "elf",
    "zwölf",
    "zwanzig",
    "hundert",
    "tausend",
    "Euro",
    "Cent",
    "Preis",
    # more everyday verbs
    "essen",
    "trinken",
    "lesen",
    "schreiben",
    "hören",
    "sehen",
    "fragen",
    "antworten",
    "arbeiten",
    "spielen",
    "kaufen",
    "brauchen",
    "finden",
    "geben",
    "nehmen",
    "helfen",
    "danken",
    "öffnen",
    "schließen",
    "warten",
    "fahren",
    "schlafen",
    "aufstehen",
    "ankommen",
    "einsteigen",
    "aussteigen",
    # basic adjectives
    "gut",
    "schlecht",
    "groß",
    "klein",
    "neu",
    "alt",
    "schön",
    "toll",
    "nett",
    "freundlich",
    "rot",
    "blau",
    "grün",
    "gelb",
    "schwarz",
    "weiß",
    "heiß",
    "kalt",
    "warm",
    "müde",
    "krank",
    "wichtig",
    "leicht",
    "schwer",
    "schnell",
    "langsam",
    "teuer",
    "billig",
    "richtig",
    "falsch",
    "offen",
    "zu",
]

CAT_REST = [
    "家庭",
    "日常",
    "飲食",
    "時間",
    "數字",
    "動詞",
    "形容詞",
    "旅行",
    "工作",
    "自然",
]


def reorder_level(entries: list[dict], level: str) -> list[dict]:
    level_words = [w for w in entries if w["level"] == level]
    others = [w for w in entries if w["level"] != level]

    by_word: dict[str, list[dict]] = {}
    for w in level_words:
        by_word.setdefault(w["word"], []).append(w)

    ordered: list[dict] = []
    used_ids: set[str] = set()

    for lemma in BEGINNER_PRIORITY:
        for w in by_word.get(lemma, []):
            if w["id"] not in used_ids:
                ordered.append(w)
                used_ids.add(w["id"])

    for cat in CAT_REST:
        for w in level_words:
            if w["id"] not in used_ids and w["category"] == cat:
                ordered.append(w)
                used_ids.add(w["id"])

    for w in level_words:
        if w["id"] not in used_ids:
            ordered.append(w)
            used_ids.add(w["id"])

    # Keep other levels in original relative order; splice this level back
    # as a contiguous block replacing its previous span.
    if not level_words:
        return entries

    first_idx = next(i for i, w in enumerate(entries) if w["level"] == level)
    # Remove all of this level, then insert ordered block at first_idx among remaining
    result = others[:]
    insert_at = min(first_idx, len(result))
    # Prefer: A1 block stays early — for A1 insert at 0; for A2 after A1 block
    if level == "A1":
        insert_at = 0
    elif level == "A2":
        insert_at = sum(1 for w in result if w["level"] == "A1")
    result[insert_at:insert_at] = ordered
    return result


def main() -> None:
    data = json.loads(PATH.read_text(encoding="utf-8"))
    before_a1 = [w["word"] for w in data if w["level"] == "A1"][:25]
    data = reorder_level(data, "A1")
    data = reorder_level(data, "A2")
    after_a1 = [w["word"] for w in data if w["level"] == "A1"][:25]
    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("A1 before:", before_a1)
    print("A1 after:", after_a1)
    print("total", len(data))


if __name__ == "__main__":
    main()
