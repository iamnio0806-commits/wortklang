#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add missing Goethe A1/A2 exam lemmas into vocabulary.json.

Rules:
  - Only APPEND new entries (never delete / rewrite existing ones).
  - Prefer A1 over A2 when a lemma appears in both.
  - Source: official Goethe Wortlisten (Start Deutsch 1, Fit in Deutsch 1, A2).
"""
from __future__ import annotations

import json
import re
import unicodedata
from collections import OrderedDict, Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOCAB_PATH = ROOT / "src" / "data" / "vocabulary.json"
LIST_DIR = Path("/tmp/goethe-lists")

# Manual plurals / articles overrides when PDF is ambiguous
OVERRIDES: dict[str, dict] = {
    "café": {"article": "das", "word": "Café", "plural": "Cafés"},
    "cd": {"article": "die", "word": "CD", "plural": "CDs"},
    "lkw": {"article": "der", "word": "Lkw", "plural": "Lkws"},
    "papiere": {"article": "die", "word": "Papiere", "plural": None},
    "eltern": {"article": "die", "word": "Eltern", "plural": None},
    "geschwister": {"article": "die", "word": "Geschwister", "plural": None},
    "großeltern": {"article": "die", "word": "Großeltern", "plural": None},
    "leute": {"article": "die", "word": "Leute", "plural": None},
    "pommes frites": {"article": "die", "word": "Pommes frites", "plural": None},
}

# Chinese glosses for function words + common Goethe gaps
ZH: dict[str, str] = {
    "ab": "從…起",
    "aber": "但是",
    "abfahren": "出發／開走",
    "abfahrt": "出發（車次）",
    "abgeben": "交出去",
    "abholen": "去接／領取",
    "absender": "寄件人",
    "achtung": "注意",
    "adresse": "地址",
    "all": "全部的",
    "allein": "獨自",
    "also": "所以／那麼",
    "alt": "老的／舊的",
    "an": "在…旁／向",
    "ander": "別的",
    "anders": "不一樣",
    "anklicken": "點選",
    "ankreuzen": "打勾",
    "anrede": "稱呼（書信）",
    "anruf": "來電",
    "ansage": "廣播／通告",
    "anschluss": "接駁／轉機",
    "an sein": "開著（電源）",
    "apartment": "套房公寓",
    "appetit": "食慾",
    "arbeit": "工作",
    "arbeiten": "工作",
    "arbeitslos": "失業的",
    "arbeitsplatz": "工作崗位",
    "arm": "手臂；貧窮的",
    "arzt": "醫生",
    "auch": "也",
    "auf": "在…上／到…上",
    "aufgabe": "作業／任務",
    "aufhören": "停止",
    "auf sein": "開著／不在家",
    "aufstehen": "起床／站起來",
    "aufzug": "電梯",
    "auge": "眼睛",
    "aus": "從…出來／用…材料",
    "ausflug": "郊遊",
    "ausfüllen": "填寫",
    "ausgang": "出口",
    "auskunft": "詢問處／資訊",
    "ausland": "國外",
    "ausländer": "外國人",
    "ausländisch": "外國的",
    "aussage": "陳述／說法",
    "aus sein": "關著",
    "ausweis": "證件",
    "auto": "汽車",
    "autobahn": "高速公路",
    "automat": "自動販賣機／售票機",
    "automatisch": "自動的",
    "baby": "嬰兒",
    "bäckerei": "麵包店",
    "bad": "浴室",
    "bahn": "火車／軌道",
    "bahnhof": "火車站",
    "bahnsteig": "月台",
    "balkon": "陽台",
    "banane": "香蕉",
    "bank": "銀行；長椅",
    "bar": "酒吧；現金的",
    "bauch": "肚子",
    "baum": "樹",
    "beamte": "公務員",
    "bei": "在…旁邊／在…家",
    "bein": "腿",
    "beispiel": "例子",
    "bekommen": "得到",
    "Beruf": "職業",
    "besser": "更好",
    "best": "最好的",
    "besichtigen": "參觀",
    "bett": "床",
    "bier": "啤酒",
    "bild": "圖片／照片",
    "birne": "梨子",
    "bisschen": "一點點",
    "bitte": "請／不客氣",
    "bleib": "留下",
    "bleiben": "留下／保持",
    "bleistift": "鉛筆",
    "blick": "視線／景色",
    "blöd": "愚蠢的／糟糕的",
    "blond": "金髮的",
    "blume": "花",
    "bogen": "表格／答題紙",
    "böse": "生氣的／壞的",
    "brot": "麵包",
    "brötchen": "小麵包",
    "bruder": "兄弟",
    "buch": "書",
    "buchstabe": "字母",
    "bus": "公車",
    "butter": "奶油",
    "café": "咖啡館",
    "cd": "光碟",
    "chef": "老闆",
    "circa": "大約",
    "cool": "酷的",
    "da": "那裡／因為",
    "dame": "女士",
    "daneben": "旁邊",
    "dank": "感謝",
    "danke": "謝謝",
    "dann": "然後",
    "datum": "日期",
    "dein": "你的",
    "dich": "你（受格）",
    "dies": "這個",
    "dieser": "這個（陽性）",
    "dieses": "這個（中性）",
    "dir": "你（與格）",
    "disco": "迪斯可舞廳",
    "doch": "可是／偏偏",
    "doktor": "醫生（口語）",
    "doppelzimmer": "雙人房",
    "dorf": "村莊",
    "du": "你",
    "dumm": "笨的",
    "drucker": "印表機",
    "durch": "穿過／藉由",
    "durchsage": "廣播通知",
    "durst": "口渴",
    "dusche": "淋浴",
    "ecke": "角落",
    "ehefrau": "妻子",
    "ehemann": "丈夫",
    "ei": "蛋",
    "ein": "一個／一",
    "eine": "一個（陰）",
    "einen": "一個（陽受格）",
    "eingang": "入口",
    "einladung": "邀請",
    "einmal": "一次",
    "eintritt": "入場",
    "einzelzimmer": "單人房",
    "einverstanden sein": "同意",
    "eltern": "父母",
    "e-mail": "電子郵件",
    "empfänger": "收件人",
    "ende": "結束／盡頭",
    "entschuldigung": "對不起",
    "er": "他",
    "ergebnis": "結果",
    "erlaubt": "允許的",
    "Erwachsene": "大人",
    "es": "它",
    "essen": "吃；食物",
    "euer": "你們的",
    "fahrer": "駕駛",
    "fahrkarte": "車票",
    "fahrrad": "腳踏車",
    "familie": "家庭",
    "familienname": "姓",
    "familienstand": "婚姻狀況",
    "farbe": "顏色",
    "fax": "傳真",
    "fehler": "錯誤",
    "fertig sein": "做完了",
    "feuer": "火；打火機",
    "fieber": "發燒",
    "film": "電影",
    "firma": "公司",
    "fisch": "魚",
    "flasche": "瓶子",
    "fleisch": "肉",
    "flug": "航班",
    "abflug": "起飛",
    "flughafen": "機場",
    "flugzeug": "飛機",
    "formular": "表格",
    "foto": "照片",
    "frage": "問題",
    "frau": "女人／太太",
    "frei": "空閒的／自由的",
    "freizeit": "休閒時間",
    "freund": "朋友（男）",
    "frühstück": "早餐",
    "führung": "導覽",
    "für": "為了",
    "fuß": "腳",
    "fußball": "足球",
    "garten": "花園",
    "gast": "客人",
    "geboren": "出生",
    "geburtsjahr": "出生年",
    "geburtsort": "出生地",
    "geburtstag": "生日",
    "gegen": "對抗／大約",
    "Gehalt": "薪水",
    "geld": "錢",
    "gemüse": "蔬菜",
    "genug": "足夠",
    "gepäck": "行李",
    "gerade": "剛才／正好",
    "gern": "樂意",
    "geschäft": "商店",
    "geschenk": "禮物",
    "geschlossen sein": "關著",
    "geschwister": "兄弟姐妹",
    "gespräch": "談話",
    "gestorben": "已去世",
    "getränk": "飲料",
    "gewicht": "體重／重量",
    "glas": "杯子／玻璃",
    "gleis": "月台軌道",
    "glück": "幸運",
    "glückwunsch": "祝賀",
    "googeln": "用 Google 搜尋",
    "grillen": "烤肉",
    "größe": "尺寸／身高",
    "großeltern": "祖父母",
    "großmutter": "祖母",
    "großvater": "祖父",
    "gruppe": "小組",
    "gruß": "問候",
    "gut": "好的",
    "halbpension": "半膳宿",
    "halle": "大廳",
    "hallo": "哈囉",
    "haltestelle": "公車站",
    "hand": "手",
    "handy": "手機",
    "haus": "房子",
    "hausaufgabe": "家庭作業",
    "hausfrau": "家庭主婦",
    "hausmann": "家庭主夫",
    "heimat": "家鄉",
    "herd": "爐灶",
    "herr": "先生",
    "herzlich": "衷心的",
    "hilfe": "幫助",
    "hobby": "嗜好",
    "hochzeit": "婚禮",
    "hoffentlich": "但願",
    "hotel": "飯店",
    "hübsch": "好看的",
    "hund": "狗",
    "hunger": "飢餓",
    "ich": "我",
    "ihr": "你們；她的／他們的",
    "im": "在…裡（in dem）",
    "in": "在…裡",
    "information": "詢問處／資訊",
    "internet": "網路",
    "italienisch": "義大利語／義大利的",
    "ja": "是；對",
    "jacke": "外套",
    "jed": "每個",
    "job": "工作",
    "jugendliche": "青少年",
    "junge": "男孩",
    "kaffee": "咖啡",
    "karte": "卡片／地圖／菜單",
    "kartoffel": "馬鈴薯",
    "kasse": "收銀台",
    "kein": "沒有（任一）",
    "kennenlernen": "認識",
    "kind": "孩子",
    "kindergarten": "幼稚園",
    "kino": "電影院",
    "kiosk": "小賣部",
    "klasse": "班級",
    "kleidung": "衣服",
    "koffer": "行李箱",
    "kollege": "同事",
    "konto": "帳戶",
    "kopf": "頭",
    "küche": "廚房",
    "kuchen": "蛋糕",
    "kugelschreiber": "原子筆",
    "kühlschrank": "冰箱",
    "kümmern": "照顧（sich kümmern）",
    "sich kümmern": "照顧／操心",
    "kunde": "顧客",
    "kurs": "課程",
    "laden": "店舖",
    "land": "國家／鄉村",
    "lange": "很久",
    "leben": "生活／生命",
    "ledig": "未婚的",
    "leider": "可惜；不幸",
    "leid": "遺憾（tut mir leid）",
    "letzt": "最後的",
    "lehrer": "老師",
    "leute": "人們",
    "licht": "燈／光",
    "lieb": "親愛的",
    "lied": "歌曲",
    "lkw": "貨車",
    "lokal": "餐廳／店家",
    "lösung": "解答",
    "markieren": "標記",
    "maschine": "機器",
    "mein": "我的",
    "meist": "大多",
    "mich": "我（受格）",
    "mir": "我（與格）",
    "mit": "和／用",
    "möchte": "想要（會）",
    "nach": "在…之後／向",
    "nächst": "下一個",
    "name": "名字",
    "nein": "不；不是",
    "nicht": "不",
    "noch": "還",
    "norden": "北方",
    "nummer": "號碼",
    "obst": "水果",
    "ohne": "沒有",
    "öl": "油",
    "oma": "奶奶／外婆",
    "online": "線上",
    "opa": "爺爺／外公",
    "ordnung": "秩序／沒問題",
    "ort": "地方",
    "übernachtung": "過夜住宿",
    "übernachten": "過夜",
    "papier": "紙",
    "papiere": "證件文件",
    "partner": "夥伴",
    "partnerin": "女夥伴",
    "party": "派對",
    "pass": "護照",
    "pause": "休息",
    "physikarbeit": "物理作業／考卷",
    "plan": "計畫／地圖",
    "platz": "位子／廣場",
    "polizei": "警察",
    "post": "郵局",
    "postleitzahl": "郵遞區號",
    "praktikum": "實習",
    "praxis": "診所",
    "preis": "價格",
    "problem": "問題",
    "prospekt": "簡章／型錄",
    "prüfung": "考試",
    "raum": "房間／空間",
    "rechnung": "帳單",
    "recht haben": "說得對",
    "regen": "雨",
    "reis": "米",
    "reise": "旅行",
    "reisebüro": "旅行社",
    "reiseführer": "旅遊指南",
    "reiten": "騎馬",
    "reparatur": "修理",
    "restaurant": "餐廳",
    "rezeption": "櫃台",
    "sachen": "東西／衣物",
    "saft": "果汁",
    "salat": "沙拉",
    "salz": "鹽",
    "s-bahn": "郊區電車",
    "schade": "真可惜",
    "schalter": "窗口",
    "schild": "標誌／牌子",
    "schinken": "火腿",
    "schluss": "結束",
    "schlüssel": "鑰匙",
    "schrank": "櫃子",
    "schuh": "鞋子",
    "schule": "學校",
    "schüler": "學生",
    "schwester": "姊妹",
    "schwimmbad": "游泳池",
    "see": "湖",
    "sehr": "非常",
    "sehenswürdigkeit": "景點",
    "sein": "是；他的",
    "sie": "她／他們／您",
    "so": "如此／那麼",
    "sofa": "沙發",
    "sohn": "兒子",
    "sonne": "太陽",
    "spazieren gehen": "散步",
    "speisekarte": "菜單",
    "sport": "運動",
    "sprache": "語言",
    "stadt": "城市",
    "stelle": "職缺／地方",
    "studium": "大學學業",
    "surfen": "上網瀏覽",
    "sympathisch": "討人喜歡的",
    "tasche": "袋子／包包",
    "taxi": "計程車",
    "tee": "茶",
    "teil": "部分",
    "telefon": "電話",
    "termin": "預約／約定",
    "test": "測驗",
    "text": "文本",
    "thema": "主題",
    "ticket": "票",
    "tisch": "桌子",
    "tochter": "女兒",
    "toilette": "廁所",
    "tomate": "番茄",
    "tot": "死的",
    "treppe": "樓梯",
    "tschüss": "掰掰",
    "uhr": "鐘；點鐘",
    "um": "大約／為了；圍繞",
    "und": "和",
    "unser": "我們的",
    "unsere": "我們的（陰／複）",
    "unter": "在…下面",
    "unterricht": "上課",
    "unterschrift": "簽名",
    "urlaub": "休假",
    "vater": "父親",
    "verboten": "禁止的",
    "verein": "社團",
    "verkäufer": "售貨員",
    "vermieter": "房東",
    "verwandte": "親戚",
    "von": "從／屬於",
    "vor": "在…前面／之前",
    "vorname": "名字",
    "vorsicht": "小心",
    "vorwahl": "區碼",
    "wann": "什麼時候",
    "warum": "為什麼",
    "was": "什麼",
    "wasser": "水",
    "weg sein": "不在／離開了",
    "weh": "痛（weh tun）",
    "wein": "葡萄酒",
    "welch": "哪一個",
    "welt": "世界",
    "wer": "誰",
    "wetter": "天氣",
    "wie": "如何／多麼",
    "wiederhören": "通話再見",
    "wiedersehen": "再見",
    "wie viel": "多少",
    "wind": "風",
    "wir": "我們",
    "wo": "哪裡",
    "wochentag": "星期幾",
    "woher": "從哪裡",
    "wohin": "去哪裡",
    "wohnung": "公寓",
    "wort": "單字",
    "zeit": "時間",
    "zeitung": "報紙",
    "zigarette": "香菸",
    "zimmer": "房間",
    "zoll": "海關",
    "zu": "去；太",
    "zufrieden": "滿意的",
    "zuerst": "首先",
    "zug": "火車",
    "zum": "到（zu dem）",
    "zur": "到（zu der）",
    "zurück": "回去",
    "zusammen": "一起",
    "zurzeit": "目前",
    "zu sein": "關著／關閉",
    "zwischen": "在…之間",
}


def fold(s: str) -> str:
    s = unicodedata.normalize("NFC", s).lower().strip()
    return s


def parse_list(path: Path, level: str, start_line: int) -> OrderedDict[str, dict]:
    lines = path.read_text(encoding="utf-8").splitlines()
    entries: OrderedDict[str, dict] = OrderedDict()
    stop = re.compile(
        r"^(Literatur|Quellen|Anhang|Impressum|Hinweise zur|©\s*Goethe|Profile Deutsch)",
        re.I,
    )
    for raw in lines[start_line:]:
        line = unicodedata.normalize(
            "NFC", raw.replace("\t", " ").replace("\xa0", " ").replace("\u00ad", "")
        ).strip()
        if not line:
            continue
        if stop.match(line):
            break
        if re.match(r"^(Seite\s+\d+|VS_|WORTLISTE|GOETHE|A1\s+A2)", line, re.I):
            continue
        if "goethe.de" in line.lower():
            continue

        m = re.match(r"^(der|die|das)\s+([A-ZÄÖÜ][A-Za-zÄÖÜäöüß\-]+)", line)
        if m:
            art, word = m.group(1), m.group(2).rstrip(",.;:")
            if word.endswith("-") or len(word) < 2:
                continue
            key = fold(word)
            if key not in entries:
                entries[key] = {
                    "article": art,
                    "word": word,
                    "level": level,
                    "kind": "noun",
                }
            continue

        m = re.match(
            r"^([a-zäöüß][a-zäöüß\-]*(?:\s+(?:sein|haben|werden|gehen|machen|nehmen|lernen|haben))?)"
            r"(?=\s+[A-ZÄÖÜa-z(]|$)",
            line,
        )
        if not m:
            continue
        w = m.group(1).strip().rstrip("-")
        if len(w) < 2:
            continue
        if re.search(r"\d", w):
            continue
        # Skip hyphenated stem markers like all- / dies-
        if w.endswith("-") and len(w) <= 6:
            w = w.rstrip("-")
        garbage = {
            "wortgruppenliste",
            "alphabetische",
            "alphabetischer",
            "wortschatz",
            "tiere",
            "du-",
            "altes",
            "tiert",
            "war",
            "dem",
            "den",
            "der",
            "physikarbeit",  # keep actually - it's in Fit list as example compound; skip odd school compound noise if wanted
        }
        if fold(w) in {"wortgruppenliste", "alphabetische", "alphabetischer"}:
            continue
        key = fold(w)
        if key not in entries:
            last = w.split()[-1]
            kind = "verb" if re.search(r"(en|eln|ern)$", last) else "other"
            entries[key] = {
                "article": None,
                "word": w,
                "level": level,
                "kind": kind,
            }
    return entries


def slug_id(word: str, article: str | None, used: set[str]) -> str:
    base = (
        fold(word)
        .replace("ä", "ae")
        .replace("ö", "oe")
        .replace("ü", "ue")
        .replace("ß", "ss")
    )
    base = re.sub(r"[^a-z0-9]+", "_", base).strip("_")
    if not base:
        base = "w"
    cand = base
    n = 2
    while cand in used:
        cand = f"{base}_{n}"
        n += 1
    used.add(cand)
    return cand


def guess_category(word: str, kind: str, article: str | None) -> str:
    w = fold(word)
    if kind == "verb" or w.endswith(("en", "eln", "ern")) and " " not in w:
        return "動詞"
    food = {
        "banane",
        "bier",
        "brot",
        "brötchen",
        "butter",
        "ei",
        "fisch",
        "fleisch",
        "getränk",
        "kaffee",
        "kartoffel",
        "kuchen",
        "milch",
        "obst",
        "öl",
        "reis",
        "saft",
        "salat",
        "salz",
        "schinken",
        "tee",
        "tomate",
        "wasser",
        "wein",
        "frühstück",
        "essen",
    }
    if w in food:
        return "飲食"
    travel = {
        "abfahrt",
        "anschluss",
        "auto",
        "autobahn",
        "bahn",
        "bahnhof",
        "bahnsteig",
        "bus",
        "fahrkarte",
        "fahrrad",
        "flughafen",
        "flugzeug",
        "haltestelle",
        "hotel",
        "reise",
        "reisebüro",
        "reiseführer",
        "taxi",
        "ticket",
        "zug",
        "zoll",
        "ausland",
        "ausflug",
    }
    if w in travel:
        return "旅行"
    family = {
        "bruder",
        "ehefrau",
        "ehemann",
        "eltern",
        "familie",
        "freund",
        "großeltern",
        "großmutter",
        "großvater",
        "kind",
        "oma",
        "opa",
        "schwester",
        "sohn",
        "tochter",
        "vater",
        "verwandte",
        "geschwister",
    }
    if w in family:
        return "家庭"
    timew = {
        "datum",
        "uhr",
        "zeit",
        "termin",
        "pause",
        "wochentag",
        "urlaub",
        "geburtstag",
    }
    if w in timew:
        return "時間"
    work = {
        "arbeit",
        "arbeitsplatz",
        "beruf",
        "chef",
        "firma",
        "job",
        "kollege",
        "kunde",
        "praktikum",
        "stelle",
        "studium",
        "unterricht",
        "prüfung",
        "kurs",
    }
    if w in work:
        return "工作"
    nature = {"baum", "regen", "sonne", "wetter", "wind", "see", "welt"}
    if w in nature:
        return "自然"
    if article is None and kind == "other":
        # adjectives / particles
        if w.endswith(("ig", "lich", "isch", "sam", "bar", "los")) or w in {
            "gut",
            "alt",
            "neu",
            "groß",
            "klein",
            "schön",
            "böse",
            "tot",
            "frei",
            "gern",
            "leider",
            "sehr",
            "vielleicht",
        }:
            return "形容詞"
        return "日常"
    return "日常"


def make_example(word: str, article: str | None, zh: str, level: str) -> tuple[str, str]:
    if article:
        de = f"Ich brauche {article} {word}."
        zhex = f"我需要這個{zh}。"
    elif " " in word and word.endswith("sein"):
        de = f"Das Licht ist aus. / Bitte {word}."
        zhex = f"燈關了。／請確認：{zh}。"
    elif word in {"ja", "nein", "bitte", "danke", "hallo", "tschüss"}:
        de = f"{word.capitalize()}!"
        zhex = f"{zh}！"
    elif word in {"ich", "du", "er", "sie", "es", "wir", "ihr"}:
        de = f"Das Pronomen „{word}“."
        zhex = f"人稱代詞「{zh}」。"
    else:
        de = f"Das Wort „{word}“ ist wichtig."
        zhex = f"「{word}」（{zh}）很重要。"
    return de, zhex


def zh_for(word: str) -> str:
    k = fold(word)
    if k in ZH:
        return ZH[k]
    # stem forms all- / dies-
    if k.endswith("-"):
        return ZH.get(k.rstrip("-"), word)
    return ZH.get(k.rstrip("-"), f"{word}")


def main() -> None:
    a1 = parse_list(LIST_DIR / "a1.txt", "A1", 404)
    a2 = parse_list(LIST_DIR / "a2.txt", "A2", 450)
    fit = parse_list(LIST_DIR / "a1fit.txt", "A1", 376)

    merged: OrderedDict[str, dict] = OrderedDict()
    for src in (a1, fit, a2):
        for k, v in src.items():
            if k not in merged:
                merged[k] = dict(v)
            elif merged[k]["level"] == "A2" and v["level"] == "A1":
                merged[k] = dict(v)

    # Apply overrides
    for k, o in OVERRIDES.items():
        if k in merged:
            merged[k].update({kk: vv for kk, vv in o.items() if vv is not None or kk == "plural"})

    vocab: list[dict] = json.loads(VOCAB_PATH.read_text(encoding="utf-8"))
    before = len(vocab)
    have_words = {fold(w["word"]) for w in vocab}
    used_ids = {w["id"] for w in vocab}

    # Extra curated essentials often missing as standalone cards
    extras = [
        {"article": None, "word": "ja", "level": "A1", "kind": "other"},
        {"article": None, "word": "nein", "level": "A1", "kind": "other"},
        {"article": None, "word": "danke", "level": "A1", "kind": "other"},
        {"article": None, "word": "bitte", "level": "A1", "kind": "other"},
        {"article": None, "word": "hallo", "level": "A1", "kind": "other"},
        {"article": None, "word": "tschüss", "level": "A1", "kind": "other"},
        {"article": None, "word": "ich", "level": "A1", "kind": "other"},
        {"article": None, "word": "du", "level": "A1", "kind": "other"},
        {"article": None, "word": "er", "level": "A1", "kind": "other"},
        {"article": None, "word": "sie", "level": "A1", "kind": "other"},
        {"article": None, "word": "es", "level": "A1", "kind": "other"},
        {"article": None, "word": "wir", "level": "A1", "kind": "other"},
        {"article": None, "word": "ihr", "level": "A1", "kind": "other"},
        {"article": None, "word": "mein", "level": "A1", "kind": "other"},
        {"article": None, "word": "dein", "level": "A1", "kind": "other"},
        {"article": None, "word": "kein", "level": "A1", "kind": "other"},
        {"article": None, "word": "nicht", "level": "A1", "kind": "other"},
        {"article": None, "word": "und", "level": "A1", "kind": "other"},
        {"article": None, "word": "oder", "level": "A1", "kind": "other"},
        {"article": None, "word": "aber", "level": "A1", "kind": "other"},
        {"article": None, "word": "mit", "level": "A1", "kind": "other"},
        {"article": None, "word": "ohne", "level": "A1", "kind": "other"},
        {"article": None, "word": "für", "level": "A1", "kind": "other"},
        {"article": None, "word": "von", "level": "A1", "kind": "other"},
        {"article": None, "word": "bei", "level": "A1", "kind": "other"},
        {"article": None, "word": "nach", "level": "A1", "kind": "other"},
        {"article": None, "word": "aus", "level": "A1", "kind": "other"},
        {"article": None, "word": "in", "level": "A1", "kind": "other"},
        {"article": None, "word": "an", "level": "A1", "kind": "other"},
        {"article": None, "word": "auf", "level": "A1", "kind": "other"},
        {"article": None, "word": "über", "level": "A1", "kind": "other"},
        {"article": None, "word": "unter", "level": "A1", "kind": "other"},
        {"article": None, "word": "zwischen", "level": "A1", "kind": "other"},
        {"article": None, "word": "durch", "level": "A1", "kind": "other"},
        {"article": None, "word": "gegen", "level": "A1", "kind": "other"},
        {"article": None, "word": "um", "level": "A1", "kind": "other"},
        {"article": None, "word": "zu", "level": "A1", "kind": "other"},
        {"article": None, "word": "sehr", "level": "A1", "kind": "other"},
        {"article": None, "word": "auch", "level": "A1", "kind": "other"},
        {"article": None, "word": "noch", "level": "A1", "kind": "other"},
        {"article": None, "word": "nur", "level": "A1", "kind": "other"},
        {"article": None, "word": "schon", "level": "A1", "kind": "other"},
        {"article": None, "word": "hier", "level": "A1", "kind": "other"},
        {"article": None, "word": "dort", "level": "A1", "kind": "other"},
        {"article": None, "word": "wann", "level": "A1", "kind": "other"},
        {"article": None, "word": "wo", "level": "A1", "kind": "other"},
        {"article": None, "word": "was", "level": "A1", "kind": "other"},
        {"article": None, "word": "wer", "level": "A1", "kind": "other"},
        {"article": None, "word": "wie", "level": "A1", "kind": "other"},
        {"article": None, "word": "warum", "level": "A1", "kind": "other"},
        {"article": None, "word": "woher", "level": "A1", "kind": "other"},
        {"article": None, "word": "wohin", "level": "A1", "kind": "other"},
        {"article": "der", "word": "Norden", "level": "A1", "kind": "noun"},
        {"article": "der", "word": "Süden", "level": "A1", "kind": "noun"},
        {"article": "der", "word": "Osten", "level": "A1", "kind": "noun"},
        {"article": "der", "word": "Westen", "level": "A1", "kind": "noun"},
    ]
    # Add Süden/Osten/Westen ZH
    ZH.update(
        {
            "süden": "南方",
            "osten": "東方",
            "westen": "西方",
            "oder": "或者",
            "über": "在…上方／關於",
            "auch": "也",
            "noch": "還",
            "nur": "只",
            "schon": "已經",
            "hier": "這裡",
            "dort": "那裡",
            "bitte": "請；不客氣",
        }
    )

    candidates: list[dict] = []
    seen = set(have_words)
    for src in (list(merged.values()) + extras):
        key = fold(src["word"])
        if key in seen:
            continue
        # skip hyphen stems that are incomplete
        if src["word"].endswith("-"):
            continue
        seen.add(key)
        candidates.append(src)

    added = []
    for src in candidates:
        word = src["word"]
        article = src.get("article")
        level = src["level"]
        kind = src.get("kind", "other")
        ov = OVERRIDES.get(fold(word), {})
        if "article" in ov:
            article = ov["article"]
        if "word" in ov:
            word = ov["word"]
        plural = ov.get("plural")

        zh = zh_for(word)
        # If we only have the German as gloss, still add — better present than missing
        if zh == word and kind == "other" and len(word) <= 2 and word not in ZH:
            # skip ultra-short unknowns
            if word not in {"ab", "an", "da", "so", "zu", "um", "er", "es", "du"}:
                continue

        cat = guess_category(word, kind, article)
        de, zhex = make_example(word, article, zh, level)
        eid = slug_id(word, article, used_ids)
        entry = {
            "id": eid,
            "article": article,
            "word": word,
            "translation": zh,
            "phonetic": word,
            "category": cat,
            "example": de,
            "exampleTranslation": zhex,
            "level": level,
        }
        if plural:
            entry["plural"] = plural
        vocab.append(entry)
        added.append(entry)

    VOCAB_PATH.write_text(
        json.dumps(vocab, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"before={before} after={len(vocab)} added={len(added)} "
        f"by_level={Counter(e['level'] for e in added)} "
        f"goethe_merged={len(merged)} a1={len(a1)} a2={len(a2)} fit={len(fit)}"
    )
    print("sample added:", [e["word"] for e in added[:40]])


if __name__ == "__main__":
    main()
