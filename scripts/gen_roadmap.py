#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate src/data/roadmap.ts — 30-day A1→A2-start self-study roadmap."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "src" / "data"
OUT = DATA / "roadmap.ts"

# Curated Day 1–30: people/greetings → sein/haben → home → food → daily → travel.
# Each day: 5 A1 vocab ids + 1 grammar + 1 reading (練習/A1). Days 10/20/30 add review.
DAYS: list[dict] = [
    {
        "day": 1,
        "titleZh": "打招呼",
        "focusZh": "禮貌開場：請、謝、抱歉與稱謂",
        "vocab": ["bitte", "dank", "entschuldigung", "herr", "frau"],
        "grammar": "a1-greeting-intro",
        "reading": "uebung-02",
        "vocabTitle": "禮貌與稱謂",
        "tipV": "先把 Bitte／Dank／Entschuldigung 練到脫口而出。",
        "tipG": "記住固定開場：Guten Tag、Hallo、Freut mich。",
        "tipR": "朗讀兩遍，標出招呼語出現的位置。",
    },
    {
        "day": 2,
        "titleZh": "自我介紹",
        "focusZh": "名字、來自哪裡、說什麼語言",
        "vocab": ["name", "heissen", "kommen", "deutsch", "englisch"],
        "grammar": "a1-personal-pronouns",
        "reading": "uebung-01",
        "vocabTitle": "介紹自己",
        "tipV": "搭配 Ich heiße…／Ich komme aus… 整句背。",
        "tipG": "先牢記 ich／du／er／sie／wir 主格。",
        "tipR": "把短文裡的人名換成你自己再讀一次。",
    },
    {
        "day": 3,
        "titleZh": "sein 與 haben",
        "focusZh": "最核心兩動詞：是／在、有",
        "vocab": ["sein", "haben", "wohnen", "deutschland", "stadt"],
        "grammar": "a1-sein-haben",
        "reading": "uebung-34",
        "vocabTitle": "sein／haben 核心詞",
        "tipV": "每天口頭變位：ich bin／du bist／ich habe／du hast。",
        "tipG": "這兩個動詞幾乎每天都會用到，務必熟練。",
        "tipR": "找出文中所有 sein／heißen 相關句。",
    },
    {
        "day": 4,
        "titleZh": "我的家人",
        "focusZh": "家庭成員與基本人際關係",
        "vocab": ["familie", "mutter", "vater", "eltern", "kind"],
        "grammar": "a1-articles-nom",
        "reading": "uebung-07",
        "vocabTitle": "家庭成員",
        "tipV": "替每位家人造句：Das ist meine Mutter.",
        "tipG": "邊記單詞邊標 der／die／das。",
        "tipR": "畫一張簡單家譜，標上德語稱謂。",
    },
    {
        "day": 5,
        "titleZh": "朋友與身分",
        "focusZh": "朋友、男孩女孩與人士說法",
        "vocab": ["freund", "freundin", "junge", "maedchen", "person"],
        "grammar": "a1-alphabet-pronunciation",
        "reading": "uebung-36",
        "vocabTitle": "朋友與身分",
        "tipV": "注意 Freund／Freundin 的性別差別。",
        "tipG": "把字母與常見發音對照讀一遍。",
        "tipR": "練習拼讀文中的名字與國名。",
    },
    {
        "day": 6,
        "titleZh": "住家空間",
        "focusZh": "房子、公寓與房間名稱",
        "vocab": ["haus", "wohnung", "zimmer", "kueche", "bad"],
        "grammar": "a1-noun-plural",
        "reading": "uebung-20",
        "vocabTitle": "住家空間",
        "tipV": "邊走邊指：Das ist die Küche.",
        "tipG": "複數常考，先記 -e／-en／-er 常見型。",
        "tipR": "標出文中所有房間名詞。",
    },
    {
        "day": 7,
        "titleZh": "家中物品",
        "focusZh": "門窗桌椅等日常名詞",
        "vocab": ["tuer", "fenster", "tisch", "stuhl", "bett"],
        "grammar": "a1-prasens-regular",
        "reading": "a1-03",
        "vocabTitle": "家具與物件",
        "tipV": "每個名詞都要連冠詞一起記。",
        "tipG": "規則動詞：字幹＋字尾，先練 machen／wohnen。",
        "tipR": "閱讀後用三個新詞描述你的房間。",
    },
    {
        "day": 8,
        "titleZh": "日常動作",
        "focusZh": "做、去、來、學、說",
        "vocab": ["machen", "gehen", "lernen", "sprechen", "verstehen"],
        "grammar": "a1-word-order",
        "reading": "uebung-12",
        "vocabTitle": "高頻日常動詞",
        "tipV": "每個動詞造一個「今天」句：Heute lerne ich Deutsch.",
        "tipG": "陳述句記住：第二位一定是變位動詞。",
        "tipR": "把文中動詞圈出來，核對是否在第二位。",
    },
    {
        "day": 9,
        "titleZh": "提問入門",
        "focusZh": "問與答：問、答、知道、說",
        "vocab": ["fragen", "antworten", "wissen", "sagen", "wiederholen"],
        "grammar": "a1-questions",
        "reading": "uebung-47",
        "vocabTitle": "問答動詞",
        "tipV": "練習 Was ist das?／Wie heißt du?",
        "tipG": "是非問句動詞開頭；W 問句疑問詞開頭。",
        "tipR": "把短文改成兩句問句再說一次。",
    },
    {
        "day": 10,
        "titleZh": "十日複習",
        "focusZh": "鞏固打招呼到基本動詞",
        "vocab": ["leute", "buch", "handy", "telefon", "geld"],
        "grammar": "a1-negation",
        "reading": "uebung-50",
        "review": True,
        "vocabTitle": "複習補充詞",
        "tipV": "把 Day 1–9 生詞快速過一輪 SRS。",
        "tipG": "分清 nicht（動詞／形容詞）與 kein（名詞）。",
        "tipR": "這篇是複習短文，盡量不查詞讀完。",
        "tipReview": "寫五句自我介紹，覆核冠詞與 sein／haben。",
    },
    {
        "day": 11,
        "titleZh": "數字基礎",
        "focusZh": "1–20 與常用數量",
        "vocab": ["eins", "zwei", "drei", "zehn", "zwanzig"],
        "grammar": "a1-time-numbers",
        "reading": "uebung-52",
        "vocabTitle": "基礎數字",
        "tipV": "大聲數到二十，再倒數回來。",
        "tipG": "數字與時間常一起考，連著練。",
        "tipR": "讀出文中所有數字。",
    },
    {
        "day": 12,
        "titleZh": "時間與一天",
        "focusZh": "早中晚、今天昨天明天",
        "vocab": ["uhr", "uhrzeit", "heute", "gestern", "morgen_2"],
        "grammar": "a1-prasens-irregular",
        "reading": "uebung-08",
        "vocabTitle": "時間詞",
        "tipV": "分清 Morgen（早上）與 morgen（明天）。",
        "tipG": "注意 fahren／lesen／sprechen 等母音變化。",
        "tipR": "用文中時間詞說出你的作息。",
    },
    {
        "day": 13,
        "titleZh": "一週七天",
        "focusZh": "星期與週末安排",
        "vocab": ["montag", "dienstag", "mittwoch", "freitag", "wochenende"],
        "grammar": "a1-coord-conj",
        "reading": "uebung-59",
        "vocabTitle": "星期",
        "tipV": "星期幾大寫：am Montag。",
        "tipG": "und／aber／oder／denn 連接兩個主句。",
        "tipR": "用 und／aber 改寫文中一句。",
    },
    {
        "day": 14,
        "titleZh": "飲食基礎",
        "focusZh": "吃喝與基本食物",
        "vocab": ["essen", "trinken", "wasser", "brot", "milch"],
        "grammar": "a1-accusative",
        "reading": "uebung-32",
        "vocabTitle": "吃喝入門",
        "tipV": "Ich esse Brot.／Ich trinke Wasser.",
        "tipG": "第四格常作直接受詞：Ich habe einen Apfel.",
        "tipR": "列出文中所有可點的食物。",
    },
    {
        "day": 15,
        "titleZh": "咖啡館與餐廳",
        "focusZh": "點餐場景常用詞",
        "vocab": ["kaffee", "tee", "apfel", "restaurant", "caf"],
        "grammar": "a1-modal-basic",
        "reading": "uebung-03",
        "vocabTitle": "咖啡廳詞彙",
        "tipV": "練習：Einen Kaffee, bitte.",
        "tipG": "情態動詞占第二位，主要動詞原形到句末。",
        "tipR": "扮演店員與客人各讀一遍。",
    },
    {
        "day": 16,
        "titleZh": "餐食與感覺",
        "focusZh": "三餐、飢渴與想要",
        "vocab": ["fruehstueck", "mittagessen", "abendessen", "hunger", "durst"],
        "grammar": "a1-possessive",
        "reading": "uebung-79",
        "vocabTitle": "三餐與感覺",
        "tipV": "Ich habe Hunger.／Ich habe Durst.",
        "tipG": "mein／dein 要隨名詞性別變格。",
        "tipR": "用 mein Frühstück 描述你的早餐。",
    },
    {
        "day": 17,
        "titleZh": "購物付款",
        "focusZh": "超市、價錢與付錢",
        "vocab": ["supermarkt", "markt", "kaufen", "bezahlen", "preis"],
        "grammar": "a1-imperative",
        "reading": "uebung-06",
        "vocabTitle": "購物動詞與場所",
        "tipV": "Was kostet das?／Das macht … Euro.",
        "tipG": "命令式：Komm!／Kommen Sie! 分清對象。",
        "tipR": "標出文中與價錢、商品有關的詞。",
    },
    {
        "day": 18,
        "titleZh": "想要與喜歡",
        "focusZh": "情態與喜好表達",
        "vocab": ["wollen", "moechten", "moegen", "koennen", "brauchen"],
        "grammar": "a1-separable",
        "reading": "uebung-17",
        "vocabTitle": "情態與喜好",
        "tipV": "Ich möchte …／Ich mag … 各造三句。",
        "tipG": "可分動詞前綴在陳述句跑到句末。",
        "tipR": "找出你喜歡／不喜歡的事物並說出來。",
    },
    {
        "day": 19,
        "titleZh": "日常作息",
        "focusZh": "睡、煮、等、找、幫",
        "vocab": ["schlafen", "kochen", "warten", "suchen", "helfen"],
        "grammar": "a1-local-prep",
        "reading": "a1-02",
        "vocabTitle": "作息動詞",
        "tipV": "用一天時間線串起五個動詞。",
        "tipG": "in／an／auf／zu 先記固定搭配。",
        "tipR": "畫出主角一天的動線。",
    },
    {
        "day": 20,
        "titleZh": "二十日複習",
        "focusZh": "飲食、時間與情態總複習",
        "vocab": ["laden", "kosten", "bestellen", "nehmen", "geben"],
        "grammar": "a1-adjectives-pred",
        "reading": "a1-50",
        "review": True,
        "vocabTitle": "複習：交易動詞",
        "tipV": "重溫 Day 11–19 錯最多的 20 個詞。",
        "tipG": "表語形容詞：Das Essen ist gut.（不加字尾）",
        "tipR": "長文複習：計時閱讀並寫三句摘要。",
        "tipReview": "自我小考：數字、星期、點餐各三題。",
    },
    {
        "day": 21,
        "titleZh": "城市問路",
        "focusZh": "街道、廣場與左右方向",
        "vocab": ["strasse", "platz", "park", "links", "rechts"],
        "grammar": "a1-local-prep",
        "reading": "uebung-16",
        "vocabTitle": "城市與方向",
        "tipV": "Wo ist …?／Links／Rechts／Hier／Dort。",
        "tipG": "複習地點介詞，搭配问路句型。",
        "tipR": "根據短文畫一張簡單路線圖。",
        "grammarTitle": "地點介詞再練",
    },
    {
        "day": 22,
        "titleZh": "交通工具",
        "focusZh": "公車火車與搭乘動詞",
        "vocab": ["bus", "zug", "auto", "bahnhof", "fahren"],
        "grammar": "a2-dative",
        "reading": "uebung-10",
        "vocabTitle": "交通詞彙",
        "tipV": "Ich fahre mit dem Bus／Zug.",
        "tipG": "A2 預告：mit 後面用第三格。",
        "tipR": "說出你平常怎麼上學／上班。",
    },
    {
        "day": 23,
        "titleZh": "旅行出發",
        "focusZh": "機場、飯店、行李與到達",
        "vocab": ["flughafen", "hotel", "koffer", "ticket", "ankommen"],
        "grammar": "a2-perfekt",
        "reading": "a1-04",
        "vocabTitle": "旅行場景",
        "tipV": "Ich bin angekommen. 先當整句記。",
        "tipG": "Perfekt：sein／haben + 過去分詞（先認再說）。",
        "tipR": "找出車票／時間相關資訊。",
    },
    {
        "day": 24,
        "titleZh": "學校學習",
        "focusZh": "學校、老師、學生與課程",
        "vocab": ["schule", "lehrer", "student", "kurs", "aufgabe"],
        "grammar": "a2-weil-dass",
        "reading": "uebung-21",
        "vocabTitle": "學校詞彙",
        "tipV": "Ich lerne Deutsch im Kurs.",
        "tipG": "weil／dass 從句動詞到句末（A2 起點）。",
        "tipR": "用 weil 說一句你學德語的原因。",
    },
    {
        "day": 25,
        "titleZh": "工作與健康",
        "focusZh": "工作場所與看醫生",
        "vocab": ["arbeit", "arbeiten", "arzt", "krank", "gesund"],
        "grammar": "a2-modal-full",
        "reading": "a1-01",
        "vocabTitle": "工作與健康",
        "tipV": "Ich bin krank.／Ich muss arbeiten.",
        "tipG": "複習並擴充情態動詞完整用法。",
        "tipR": "讀請假短文，標出情態動詞。",
    },
    {
        "day": 26,
        "titleZh": "天氣感覺",
        "focusZh": "天氣與冷熱疲倦",
        "vocab": ["wetter", "sonne", "regen", "kalt", "warm"],
        "grammar": "a1-adjectives-pred",
        "reading": "uebung-13",
        "vocabTitle": "天氣與感覺",
        "tipV": "Heute ist es kalt／warm／sonnig.",
        "tipG": "天氣句常用 es ist + 形容詞。",
        "tipR": "用三句描述今天天氣。",
        "grammarTitle": "形容詞再練（天氣）",
    },
    {
        "day": 27,
        "titleZh": "顏色與形容",
        "focusZh": "顏色與大小好壞",
        "vocab": ["rot", "blau", "gut", "schoen", "klein"],
        "grammar": "a2-comparative",
        "reading": "uebung-31",
        "vocabTitle": "顏色與形容詞",
        "tipV": "Das Buch ist blau.／Es ist schön.",
        "tipG": "比較級先認 größer／besser 等常見形。",
        "tipR": "描述你身邊三件物品的顏色。",
    },
    {
        "day": 28,
        "titleZh": "見面與邀約",
        "focusZh": "認識、碰面、拜訪、慶祝",
        "vocab": ["kennen", "treffen", "besuchen", "feiern", "einladen"],
        "grammar": "a2-wenn-als",
        "reading": "uebung-09",
        "vocabTitle": "社交動詞",
        "tipV": "Hast du Zeit?／Wir treffen uns um …",
        "tipG": "wenn（每當／如果）與 als（過去一次）。",
        "tipR": "根據短文寫一則簡易邀約簡訊。",
    },
    {
        "day": 29,
        "titleZh": "旅行進階",
        "focusZh": "搭乘轉換與旅行動詞",
        "vocab": ["reise", "einsteigen", "aussteigen", "umsteigen", "haltestelle"],
        "grammar": "a2-two-way-prep",
        "reading": "uebung-83",
        "vocabTitle": "搭乘與轉乘",
        "tipV": "Wo muss ich umsteigen?",
        "tipG": "兩用介詞：位置用三格、方向用四格。",
        "tipR": "說出一段「從家到車站」的路線。",
    },
    {
        "day": 30,
        "titleZh": "三十日總複習",
        "focusZh": "綜合運用，銜接 A2",
        "vocab": ["finden", "zeigen", "bringen", "holen", "bleiben"],
        "grammar": "a2-perfekt",
        "reading": "a1-36",
        "review": True,
        "vocabTitle": "複習：高頻動詞",
        "tipV": "總複習：隨機抽 30 詞，正確率目標 ≥80%。",
        "tipG": "用 Perfekt 說三件你今天做過的事。",
        "tipR": "閱讀學習策略短文，訂下一個 A2 小目標。",
        "tipReview": "重做 Day 10／20 的自我介紹與點餐對話。",
        "grammarTitle": "Perfekt 總複習",
    },
]

NOTE = (
    "零基礎 30 日路線：每天約 5 個 A1 單字＋1 則文法要點＋1 篇短閱讀。"
    "順序由打招呼／自我介紹 → sein／haben → 家庭住家 → 飲食購物 → 日常作息 → 交通旅行，"
    "第 10／20／30 日加強複習；後期導入少量 A2（第三格、Perfekt、weil）作為銜接。"
    "請搭配單字卡與朗讀，不必一次求快。"
)


def load_ids() -> tuple[set[str], set[str], set[str]]:
    vocab = {v["id"] for v in json.loads((DATA / "vocabulary.json").read_text(encoding="utf-8"))}
    grammar = {t["id"] for t in json.loads((DATA / "grammar.json").read_text(encoding="utf-8"))}
    reading_raw = json.loads((DATA / "reading.json").read_text(encoding="utf-8"))
    reading = {i["id"] for i in reading_raw["items"]}
    return vocab, grammar, reading


def validate(vocab: set[str], grammar: set[str], reading: set[str]) -> None:
    assert len(DAYS) == 30, f"expected 30 days, got {len(DAYS)}"
    days = [d["day"] for d in DAYS]
    assert days == list(range(1, 31)), f"days not 1..30: {days}"

    seen_vocab: set[str] = set()
    for d in DAYS:
        tasks_min = 3
        n_tasks = 3 + (1 if d.get("review") else 0)  # vocab+grammar+reading[+review]
        assert n_tasks >= 3
        assert len(d["vocab"]) == 5, f"day {d['day']} needs 5 vocab"
        for vid in d["vocab"]:
            assert vid in vocab, f"day {d['day']}: missing vocab id {vid}"
            assert vid not in seen_vocab, f"duplicate vocab across days: {vid}"
            seen_vocab.add(vid)
        assert d["grammar"] in grammar, f"day {d['day']}: missing grammar {d['grammar']}"
        assert d["reading"] in reading, f"day {d['day']}: missing reading {d['reading']}"
        # reading level check
        items = {
            i["id"]: i
            for i in json.loads((DATA / "reading.json").read_text(encoding="utf-8"))["items"]
        }
        lvl = items[d["reading"]]["level"]
        assert lvl in ("練習", "A1"), f"day {d['day']}: reading {d['reading']} level={lvl}"
        # vocab A1
        vmap = {
            v["id"]: v
            for v in json.loads((DATA / "vocabulary.json").read_text(encoding="utf-8"))
        }
        for vid in d["vocab"]:
            assert vmap[vid]["level"] == "A1", f"{vid} is not A1"


def ts_string(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def emit_ts() -> str:
    lines: list[str] = []
    lines.append("/** Auto-generated by scripts/gen_roadmap.py — 30-day beginner roadmap. */")
    lines.append("")
    lines.append(
        "export type RoadmapTaskKind = 'vocab' | 'grammar' | 'reading' | 'story' | 'review'"
    )
    lines.append("")
    lines.append("export type RoadmapTask = {")
    lines.append("  id: string")
    lines.append("  kind: RoadmapTaskKind")
    lines.append("  titleZh: string")
    lines.append("  titleDe?: string")
    lines.append("  /** vocab word ids from vocabulary.json */")
    lines.append("  vocabIds?: string[]")
    lines.append("  /** grammar topic id from grammar.json */")
    lines.append("  grammarId?: string")
    lines.append("  /** reading item id from reading.json (練習 or A1 preferred) */")
    lines.append("  readingId?: string")
    lines.append("  /** story chapter id if any */")
    lines.append("  storyId?: string")
    lines.append("  tipZh: string")
    lines.append("}")
    lines.append("")
    lines.append("export type RoadmapDay = {")
    lines.append("  day: number")
    lines.append("  titleZh: string")
    lines.append("  focusZh: string")
    lines.append("  tasks: RoadmapTask[]")
    lines.append("}")
    lines.append("")
    lines.append(f"export const ROADMAP_NOTE = {ts_string(NOTE)}")
    lines.append("")
    lines.append("export const ROADMAP_DAYS: RoadmapDay[] = [")

    # Load titles for optional titleDe
    gmap = {
        t["id"]: t
        for t in json.loads((DATA / "grammar.json").read_text(encoding="utf-8"))
    }
    rmap = {
        i["id"]: i
        for i in json.loads((DATA / "reading.json").read_text(encoding="utf-8"))["items"]
    }

    for d in DAYS:
        day = d["day"]
        dd = f"{day:02d}"
        lines.append("  {")
        lines.append(f"    day: {day},")
        lines.append(f"    titleZh: {ts_string(d['titleZh'])},")
        lines.append(f"    focusZh: {ts_string(d['focusZh'])},")
        lines.append("    tasks: [")

        # vocab task
        vids = ", ".join(ts_string(v) for v in d["vocab"])
        lines.append("      {")
        lines.append(f"        id: {ts_string(f'day{dd}-vocab')},")
        lines.append("        kind: 'vocab',")
        lines.append(f"        titleZh: {ts_string(d['vocabTitle'])},")
        lines.append(f"        vocabIds: [{vids}],")
        lines.append(f"        tipZh: {ts_string(d['tipV'])},")
        lines.append("      },")

        # grammar
        g = gmap[d["grammar"]]
        g_title = d.get("grammarTitle") or g["title"]
        lines.append("      {")
        lines.append(f"        id: {ts_string(f'day{dd}-grammar')},")
        lines.append("        kind: 'grammar',")
        lines.append(f"        titleZh: {ts_string(g_title)},")
        lines.append(f"        titleDe: {ts_string(g['titleDe'])},")
        lines.append(f"        grammarId: {ts_string(d['grammar'])},")
        lines.append(f"        tipZh: {ts_string(d['tipG'])},")
        lines.append("      },")

        # reading
        r = rmap[d["reading"]]
        r_title = r.get("titleZh") or r.get("title") or d["reading"]
        lines.append("      {")
        lines.append(f"        id: {ts_string(f'day{dd}-reading')},")
        lines.append("        kind: 'reading',")
        lines.append(f"        titleZh: {ts_string(r_title)},")
        if r.get("title"):
            lines.append(f"        titleDe: {ts_string(r['title'])},")
        lines.append(f"        readingId: {ts_string(d['reading'])},")
        lines.append(f"        tipZh: {ts_string(d['tipR'])},")
        lines.append("      },")

        if d.get("review"):
            lines.append("      {")
            lines.append(f"        id: {ts_string(f'day{dd}-review')},")
            lines.append("        kind: 'review',")
            lines.append(f"        titleZh: {ts_string('重點複習')},")
            lines.append(f"        tipZh: {ts_string(d['tipReview'])},")
            lines.append("      },")

        lines.append("    ],")
        lines.append("  },")

    lines.append("]")
    lines.append("")
    return "\n".join(lines)


def print_sample_day1(text: str) -> None:
    # lightweight parse from generated structure via DAYS
    d = DAYS[0]
    print("=== Day 1 sample ===")
    print(f"titleZh: {d['titleZh']}")
    print(f"focusZh: {d['focusZh']}")
    print(f"vocab ({len(d['vocab'])}): {d['vocab']}")
    print(f"grammar: {d['grammar']}")
    print(f"reading: {d['reading']}")
    print(f"tasks: vocab + grammar + reading = 3")
    print()
    print("=== Counts ===")
    print(f"days: {len(DAYS)}")
    print(f"vocab slots: {sum(len(x['vocab']) for x in DAYS)}")
    print(f"unique vocab: {len({v for x in DAYS for v in x['vocab']})}")
    print(f"review days: {[x['day'] for x in DAYS if x.get('review')]}")
    print(f"tasks total: {sum(3 + (1 if x.get('review') else 0) for x in DAYS)}")
    print(f"wrote: {OUT} ({len(text)} bytes)")


def main() -> None:
    vocab, grammar, reading = load_ids()
    validate(vocab, grammar, reading)
    text = emit_ts()
    OUT.write_text(text, encoding="utf-8")
    print_sample_day1(text)
    print("OK: roadmap validated and written.")


if __name__ == "__main__":
    main()
