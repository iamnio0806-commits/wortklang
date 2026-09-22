#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Clean junk Goethe-gap entries and add a few more essentials."""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

VOCAB = Path(__file__).resolve().parents[1] / "src" / "data" / "vocabulary.json"

JUNK = {
    "all",
    "ander",
    "best",
    "beantworter",
    "zum",
    "zur",
    "im",
    "dem",
    "den",
    "tiert",
    "alts",
    "du-",
    "Anruf-",
}


def fold(s: str) -> str:
    return s.lower().strip()


def main() -> None:
    vocab = json.loads(VOCAB.read_text(encoding="utf-8"))
    before = len(vocab)
    clean = [
        w
        for w in vocab
        if fold(w["word"]) not in JUNK and not w["word"].endswith("-")
    ]
    have = {fold(w["word"]) for w in clean}
    ids = {w["id"] for w in clean}
    extra: list[dict] = []

    def add(
        article: str | None,
        word: str,
        zh: str,
        cat: str,
        level: str,
        plural: str | None = None,
        example: str | None = None,
        example_zh: str | None = None,
    ) -> None:
        if fold(word) in have:
            return
        eid = (
            fold(word)
            .replace("ä", "ae")
            .replace("ö", "oe")
            .replace("ü", "ue")
            .replace("ß", "ss")
        )
        eid = re.sub(r"[^a-z0-9]+", "_", eid).strip("_") or "w"
        base = eid
        n = 1
        while eid in ids:
            n += 1
            eid = f"{base}_{n}"
        if example is None:
            if article:
                example = f"Hier ist {article} {word}."
                example_zh = f"這裡是{zh}。"
            else:
                example = f'Das Wort "{word}".'
                example_zh = f"「{zh}」。"
        entry = {
            "id": eid,
            "article": article,
            "word": word,
            "translation": zh,
            "phonetic": word,
            "category": cat,
            "example": example,
            "exampleTranslation": example_zh,
            "level": level,
        }
        if plural:
            entry["plural"] = plural
        extra.append(entry)
        have.add(fold(word))
        ids.add(eid)

    add("der", "Anrufbeantworter", "答錄機", "日常", "A1", "Anrufbeantworter")
    add("das", "Café", "咖啡館", "飲食", "A1", "Cafés")
    add(None, "oder", "或者", "日常", "A1")
    add(None, "auch", "也", "日常", "A1")
    add(None, "noch", "還", "日常", "A1")
    add(None, "nur", "只", "日常", "A1")
    add(None, "schon", "已經", "日常", "A1")
    add(None, "hier", "這裡", "日常", "A1")
    add(None, "dort", "那裡", "日常", "A1")
    add(None, "bitte", "請；不客氣", "日常", "A1")
    add(None, "über", "在…上方；關於", "日常", "A1")
    add("der", "Süden", "南方", "自然", "A1")
    add("der", "Osten", "東方", "自然", "A1")
    add("der", "Westen", "西方", "自然", "A1")
    add(None, "vielleicht", "也許", "日常", "A1")
    add(None, "natürlich", "當然", "日常", "A1")
    add(None, "eigentlich", "其實", "日常", "A2")
    add(None, "bestimmt", "一定", "日常", "A2")
    add(None, "sofort", "立刻", "日常", "A1")
    add(None, "manchmal", "有時候", "日常", "A1")
    add(None, "oft", "常常", "日常", "A1")
    add(None, "immer", "總是", "日常", "A1")
    add(None, "nie", "從不", "日常", "A1")
    add(None, "heute", "今天", "時間", "A1")
    add(None, "gestern", "昨天", "時間", "A1")
    add(None, "morgen", "明天；早晨", "時間", "A1")
    add(None, "jetzt", "現在", "時間", "A1")
    add(None, "bald", "很快；不久", "時間", "A1")
    add(None, "später", "稍後", "時間", "A1")
    add(None, "früh", "早", "時間", "A1")
    add(None, "spät", "晚", "時間", "A1")

    # Improve bare German-as-translation for newly added simple words if any remain
    zh_fix = {
        "Apartment": "套房公寓",
        "Ansage": "廣播通告",
        "Anschluss": "接駁／轉機",
        "Aussage": "陳述",
        "Automat": "自動販賣機／售票機",
        "Bahn": "火車／軌道",
        "Bahnsteig": "月台",
        "Beamte": "公務員",
        "Bogen": "表格／答題紙",
        "Buchstabe": "字母",
        "CD": "光碟",
        "Dame": "女士",
        "Disco": "迪斯可",
        "Doktor": "醫生（口語）",
        "Durchsage": "廣播通知",
        "Ehefrau": "妻子",
        "Ehemann": "丈夫",
        "Familienstand": "婚姻狀況",
        "Fax": "傳真",
        "Freizeit": "休閒時間",
        "Geburtsjahr": "出生年",
        "Geburtsort": "出生地",
        "Getränk": "飲料",
        "Gruß": "問候",
        "Halbpension": "半膳宿",
        "Halle": "大廳",
        "Hausfrau": "家庭主婦",
        "Hausmann": "家庭主夫",
        "Heimat": "家鄉",
        "Jugendliche": "青少年",
        "Kindergarten": "幼稚園",
        "Kiosk": "小賣部",
        "Licht": "燈／光",
        "Lkw": "貨車",
        "Lokal": "店家／餐廳",
        "Maschine": "機器",
        "Papiere": "證件文件",
        "Partnerin": "女夥伴",
        "Prospekt": "簡章",
        "Reisebüro": "旅行社",
        "Reiseführer": "旅遊指南",
        "Schild": "標誌／牌子",
        "Schinken": "火腿",
        "Schluss": "結束",
        "Studium": "大學學業",
        "Test": "測驗",
        "Vorsicht": "小心",
        "Welt": "世界",
        "Wiederhören": "通話再見",
        "Wiedersehen": "再見",
        "Zigarette": "香菸",
        "Wochentag": "星期幾",
        "Übernachtung": "過夜住宿",
        "Anrede": "稱呼（書信）",
        "Anruf": "來電",
        "Abfahrt": "出發",
        "Ausland": "國外",
        "Ausländer": "外國人",
        "Norden": "北方",
    }
    for w in clean:
        if w["word"] in zh_fix and w["translation"] in (w["word"], f"{w['word']}"):
            w["translation"] = zh_fix[w["word"]]
        elif w["word"] in zh_fix and w["translation"] == w["word"]:
            w["translation"] = zh_fix[w["word"]]
        # also fix when translation equals word (no zh yet)
        if w["translation"] == w["word"] and w["word"] in zh_fix:
            w["translation"] = zh_fix[w["word"]]

    for w in clean:
        if w["translation"] == w["word"] and w["word"] in zh_fix:
            w["translation"] = zh_fix[w["word"]]

    out = clean + extra
    VOCAB.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"before={before} after={len(out)} removed={before - len(clean)} "
        f"extra={len(extra)} levels={Counter(w['level'] for w in out)}"
    )
    for check in [
        "ja",
        "nein",
        "danke",
        "hallo",
        "tschüss",
        "ich",
        "Abfahrt",
        "Bahnsteig",
        "Ausland",
        "Café",
        "Anrufbeantworter",
    ]:
        ok = any(fold(w["word"]) == fold(check) for w in out)
        print(check, "OK" if ok else "MISSING")


if __name__ == "__main__":
    main()
