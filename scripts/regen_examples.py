#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regenerate vocabulary examples that follow human logic.
Templates are chosen by semantic class (place, object, person, travel,
food, time, abstract, verb, adjective), not by a single generic frame.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "src" / "data" / "vocabulary.json"

NAMES = ["Anna", "Tom", "Lisa", "Paul", "Mia", "Jonas", "Sara", "Leo", "Nina", "Max"]
TIMES = [
    ("um 8 Uhr", "八點"),
    ("um 10 Uhr", "十點"),
    ("morgen", "明天"),
    ("heute", "今天"),
    ("am Montag", "星期一"),
    ("am Wochenende", "週末"),
    ("nachmittags", "下午"),
    ("abends", "晚上"),
]
PLACES = [
    ("in Berlin", "在柏林"),
    ("in München", "在慕尼黑"),
    ("hier", "這裡"),
    ("dort", "那裡"),
    ("zu Hause", "在家"),
    ("in der Stadt", "在城裡"),
]

ABSTRACT_SUFFIX = (
    "ung", "heit", "keit", "nis", "tum", "schaft", "tion", "sion",
    "ismus", "ität", "enz", "anz", "ment",
)
PERSON_HINTS = (
    "人", "友", "師", "生", "孩", "父", "母", "兄", "弟", "姐", "妹",
    "男", "女", "客", "員", "醫", "鄰", "同", "子", "女",
)
PLACE_HINTS = (
    "房", "屋", "室", "廳", "店", "館", "站", "場", "園", "校", "院",
    "城", "街", "路", "橋", "島", "河", "湖", "海", "山", "村", "區",
    "公寓", "廚房", "浴室", "臥", "辦公", "廁", "入口", "出口", "門", "窗", "大學", "學校",
)
OBJECT_HINTS = (
    "書", "桌", "椅", "袋", "包", "筆", "紙", "機", "車", "鍵", "杯",
    "盤", "燈", "床", "鞋", "衣", "帽", "錶", "票", "卡", "箱",
    "瓶", "鏡", "球", "琴", "畫", "圖", "信", "報", "腦", "手機",
)
FOOD_HINTS = (
    "食", "飯", "麵", "包", "肉", "菜", "果", "水", "茶", "咖", "酒",
    "奶", "糖", "鹽", "湯", "蛋", "魚", "米", "點心", "餐",
)
TIME_HINTS = (
    "時", "分", "秒", "天", "日", "週", "月", "年", "晨", "晚", "夜",
    "春", "夏", "秋", "冬", "點", "刻",
)
TRAVEL_HINTS = (
    "旅行", "起飛", "抵達", "延誤", "行李", "護照", "簽證", "機場", "飯店",
    "旅館", "航班", "月台", "出入口", "登機", "出境", "入境", "觀光",
)
DEVICE_HINTS = ("電腦", "手機", "電話", "平板", "印表", "螢幕", "鍵盤", "滑鼠", "相機")
ILLNESS_HINTS = ("病", "痛", "感冒", "發燒", "咳", "過敏", "傷")
COLOR_HINTS = ("紅", "藍", "綠", "黃", "黑", "白", "灰", "棕", "粉", "橙", "紫")

# A1/A2：例句必須出現原形（infinitive），方便對照單字卡
AUX_VERBS_LEMMA = {
    "sein": ("Ich möchte heute zu Hause sein.", "我今天想待在家。"),
    "haben": ("Ich möchte mehr Zeit haben.", "我想多一點時間。"),
    "werden": ("Arzt werden ist mein Ziel.", "成為醫生是我的目標。"),
    "können": ("Ich will gut Deutsch können.", "我想要很會德文。"),
    "müssen": ("Wir müssen jetzt gehen.", "我們現在必須走了。"),
    "dürfen": ("Hier dürfen wir nicht rauchen.", "我們這裡不准吸菸。"),
    "sollen": ("Was sollen wir jetzt tun?", "我們現在該做什麼？"),
    "wollen": ("Wir wollen heute früh schlafen.", "我們今天想早點睡。"),
    "mögen": ("Viele Leute mögen diese Stadt.", "很多人喜歡這座城市。"),
    "möchten": ("Wir möchten einen Kaffee, bitte.", "我們想要一杯咖啡。"),
}

# B1+ 可用常見變位（文法頁另有完整表）
AUX_VERBS_FINITE = {
    "sein": ("Ich bin müde, aber zufrieden.", "我累，但很滿足。"),
    "haben": ("Hast du heute Zeit?", "你今天有時間嗎？"),
    "werden": ("Es wird gleich dunkel.", "天快黑了。"),
    "können": ("Kannst du mir kurz helfen?", "你可以幫我一下嗎？"),
    "müssen": ("Wir müssen jetzt gehen.", "我們現在必須走了。"),
    "dürfen": ("Hier darf man nicht rauchen.", "這裡不准吸菸。"),
    "sollen": ("Du sollst bitte anrufen.", "你應該打個電話。"),
    "wollen": ("Ich will heute früh schlafen.", "我今天想早點睡。"),
    "mögen": ("Ich mag diese Stadt.", "我喜歡這座城市。"),
    "möchten": ("Ich möchte einen Kaffee, bitte.", "我想要一杯咖啡。"),
}


def hmix(s: str) -> int:
    n = 2166136261
    for ch in s:
        n ^= ord(ch)
        n = (n * 16777619) & 0xFFFFFFFF
    return n


def pick(pool, seed, salt=0):
    return pool[(seed + salt) % len(pool)]


def akk(art: str | None) -> str | None:
    return "den" if art == "der" else art


def dat(art: str | None) -> str | None:
    if art == "der":
        return "dem"
    if art == "die":
        return "der"
    if art == "das":
        return "dem"
    return art


def cap(art: str) -> str:
    return art[:1].upper() + art[1:]


def short_zh(zh: str) -> str:
    s = zh.split("／")[0].split("/")[0].split("；")[0].strip()
    # trim adjectival 的 for smoother example Chinese ("紅色的" → "紅色")
    if s.endswith("的") and len(s) > 2:
        s = s[:-1]
    return s


def has_any(text: str, hints: tuple[str, ...]) -> bool:
    return any(h in text for h in hints)


def classify_noun(w: dict) -> str:
    word = w["word"]
    zh = w["translation"]
    cat = w["category"]
    low = word.lower()

    if has_any(zh, ILLNESS_HINTS) or low in {"schnupfen", "husten", "fieber", "grippe"}:
        return "illness"
    if cat == "飲食" or has_any(zh, FOOD_HINTS):
        return "food"
    if cat == "時間" or has_any(zh, TIME_HINTS):
        return "time"
    if cat == "旅行" or has_any(zh, TRAVEL_HINTS):
        return "travel"
    if has_any(zh, DEVICE_HINTS) or low in {
        "computer", "handy", "telefon", "drucker", "laptop", "tablet", "bildschirm",
    }:
        return "object"
    if cat == "自然" and not low.endswith(ABSTRACT_SUFFIX):
        return "nature"
    if cat == "家庭" and has_any(zh, PERSON_HINTS):
        return "person"
    if has_any(zh, PERSON_HINTS) or low in {
        "mann", "frau", "kind", "freund", "freundin", "lehrer", "lehrerin",
        "arzt", "ärztin", "student", "studentin", "gast", "nachbar",
    }:
        return "person"
    if has_any(zh, PLACE_HINTS) or low.endswith(
        ("zimmer", "haus", "platz", "gasse", "straße", "strasse", "laden", "markt", "schule", "büro")
    ):
        return "place"
    if has_any(zh, OBJECT_HINTS):
        return "object"
    if low.endswith(ABSTRACT_SUFFIX) or has_any(
        zh,
        ("性", "感", "度", "力", "權", "制", "義", "論", "念", "況", "果", "勢", "關係", "態度", "決定", "發展", "意圖", "假設"),
    ):
        return "abstract"
    if cat in {"日常", "家庭", "工作"}:
        return "object"
    return "abstract" if low.endswith(ABSTRACT_SUFFIX) else "object"


def ex_illness(w, seed) -> tuple[str, str]:
    art, word, zh = w["article"], w["word"], short_zh(w["translation"])
    a, Art = akk(art), cap(art)
    name = pick(NAMES, seed, 1)
    bank = [
        (f"Ich habe {a} {word}.", f"我得了{zh}。"),
        (f"{name} hat {a} {word} und bleibt zu Hause.", f"{name}有{zh}，留在家裡。"),
        (f"Wegen {dat(art)} {word} gehe ich zum Arzt.", f"因為{zh}，我去看醫生。"),
        (f"{Art} {word} ist zum Glück nicht schlimm.", f"幸好這{zh}不嚴重。"),
        (f"Gegen {a} {word} hilft Tee und Ruhe.", f"對付{zh}，喝茶休息有幫助。"),
        (f"Hast du auch {a} {word}?", f"你也有{zh}嗎？"),
        (f"Seit gestern plagt mich {art} {word}.", f"從昨天起{zh}就纏著我。"),
        (f"Mit {dat(art)} {word} sollte man nicht zur Arbeit.", f"有{zh}不該去上班。"),
    ]
    return bank[seed % len(bank)]


# ── curated overrides for high-frequency / easy-to-get-wrong lemmas ──
CURATED: dict[str, tuple[str, str]] = {
    "haus": ("Wir wohnen in einem kleinen Haus.", "我們住在一棟小房子裡。"),
    "wohnung": ("Die Wohnung ist hell und ruhig.", "這間公寓明亮又安靜。"),
    "zimmer": ("Mein Zimmer ist oben links.", "我的房間在樓上左邊。"),
    "küche": ("In der Küche kocht Anna Suppe.", "Anna 在廚房煮湯。"),
    "bad": ("Das Bad ist gerade besetzt.", "浴室現在有人在用。"),
    "badezimmer": ("Das Badezimmer liegt neben der Küche.", "浴室在廚房旁邊。"),
    "schlafzimmer": ("Das Schlafzimmer geht zum Garten hinaus.", "臥室朝向花園。"),
    "wohnzimmer": ("Abends sitzen wir im Wohnzimmer.", "晚上我們坐在客廳。"),
    "abflug": ("Der Abflug ist um 10 Uhr.", "起飛時間是十點。"),
    "ankunft": ("Die Ankunft verzögert sich um 20 Minuten.", "抵達延誤了二十分鐘。"),
    "verspätung": ("Wegen der Verspätung verpassen wir den Anschluss.", "因為延誤，我們趕不上接駁。"),
    "gepäck": ("Wo kann ich mein Gepäck aufgeben?", "我可以在哪裡托運行李？"),
    "handgepäck": ("Das Handgepäck darf nicht zu schwer sein.", "手提行李不能太重。"),
    "visum": ("Für die Reise brauche ich ein Visum.", "這趟旅行我需要簽證。"),
    "pass": ("Vergiss deinen Pass nicht!", "別忘了你的護照！"),
    "flugzeug": ("Das Flugzeug startet gleich.", "飛機馬上要起飛了。"),
    "zug": ("Der Zug nach Köln fährt von Gleis 3.", "往科隆的火車從 3 號月台開出。"),
    "bahnhof": ("Wir treffen uns vor dem Bahnhof.", "我們在火車站前碰面。"),
    "hotel": ("Unser Hotel liegt in der Altstadt.", "我們的旅館在老城區。"),
    "brot": ("Zum Frühstück esse ich Brot mit Butter.", "早餐我吃奶油麵包。"),
    "wasser": ("Kann ich bitte ein Glas Wasser haben?", "可以給我一杯水嗎？"),
    "kaffee": ("Morgens trinke ich immer Kaffee.", "早上我總是喝咖啡。"),
    "tee": ("Möchtest du Tee oder Kaffee?", "你想喝茶還是咖啡？"),
    "freund": ("Mein Freund hilft mir beim Umzug.", "我朋友幫我搬家。"),
    "freundin": ("Meine Freundin kommt später.", "我女朋友／女性朋友晚點來。"),
    "kind": ("Das Kind spielt im Garten.", "孩子在花園裡玩。"),
    "lehrer": ("Der Lehrer erklärt die Regel noch einmal.", "老師再講一次規則。"),
    "buch": ("Ich lese gerade ein spannendes Buch.", "我正在讀一本精彩的書。"),
    "tisch": ("Die Schlüssel liegen auf dem Tisch.", "鑰匙在桌上。"),
    "stuhl": ("Bitte nimm einen Stuhl und setz dich.", "請拿張椅子坐下。"),
    "auto": ("Wir fahren mit dem Auto zum See.", "我們開車去湖邊。"),
    "zeit": ("Heute habe ich leider wenig Zeit.", "今天我時間很少。"),
    "uhr": ("Die Uhr geht fünf Minuten vor.", "這隻錶快五分鐘。"),
    "absicht": ("Das war nicht meine Absicht.", "那不是我的本意。"),
    "achtung": ("Achtung, die Stufe ist rutschig!", "小心，這階梯很滑！"),
    "angabe": ("Bitte prüfe jede Angabe im Formular.", "請檢查表格裡的每一項資料。"),
    "annahme": ("Unter dieser Annahme ergibt die Rechnung Sinn.", "在這個假設下，計算才說得通。"),
    "anstrengung": ("Mit großer Anstrengung hat er die Prüfung bestanden.", "他非常努力才通過考試。"),
    "aufnahme": ("Die Aufnahme an der Uni freut sie sehr.", "錄取大學讓她很高興。"),
    "prüfung": ("Morgen schreibe ich eine Prüfung.", "明天我有一場考試。"),
    "universität": ("Sie studiert an der Universität.", "她在大學唸書。"),
    "gesundheit": ("Ich wünsche dir gute Gesundheit!", "祝你健康！"),
    "zeugnis": ("Im Zeugnis stehen gute Noten.", "成績單上有好成績。"),
    "flughafen": ("Wir müssen früher zum Flughafen.", "我們得早點去機場。"),
    "koffer": ("Mein Koffer ist zu schwer.", "我的行李箱太重了。"),
}


def ex_place(w, seed) -> tuple[str, str]:
    art, word, zh = w["article"], w["word"], short_zh(w["translation"])
    a, d, Art = akk(art), dat(art), cap(art)
    name = pick(NAMES, seed, 1)
    t_de, t_zh = pick(TIMES, seed, 2)
    bank = [
        (f"{Art} {word} ist hell und freundlich.", f"這{zh}明亮又溫馨。"),
        (f"Wir sind {t_de} in {d} {word}.", f"我們{t_zh}在{zh}。"),
        (f"{name} wartet vor {d} {word}.", f"{name}在{zh}前面等。"),
        (f"Kommst du mit in {a} {word}?", f"你要一起去{zh}嗎？"),
        (f"In {d} {word} ist es ruhig.", f"{zh}裡很安靜。"),
        (f"{Art} {word} liegt gleich um die Ecke.", f"{zh}就在轉角。"),
        (f"Ich kenne {a} {word} gut.", f"我很熟悉這個{zh}。"),
        (f"Der Weg zu {d} {word} ist kurz.", f"去{zh}的路很近。"),
        (f"Von {d} {word} aus sieht man den Hof.", f"從{zh}看出去可以看到院子。"),
        (f"{name} arbeitet in {d} {word}.", f"{name}在{zh}工作。"),
    ]
    return bank[seed % len(bank)]


def ex_object(w, seed) -> tuple[str, str]:
    art, word, zh = w["article"], w["word"], short_zh(w["translation"])
    a, d, Art = akk(art), dat(art), cap(art)
    name = pick(NAMES, seed, 1)
    bank = [
        (f"{Art} {word} liegt auf dem Tisch.", f"{zh}在桌上。"),
        (f"Kannst du mir {a} {word} geben?", f"你可以給我這個{zh}嗎？"),
        (f"Ich habe {a} {word} zu Hause gelassen.", f"我把{zh}忘在家了。"),
        (f"{name} kauft {a} {word} im Laden.", f"{name}在店裡買{zh}。"),
        (f"Ohne {a} {word} kann ich nicht arbeiten.", f"沒有{zh}我沒辦法做事。"),
        (f"Wo hast du {a} {word} hingetan?", f"你把{zh}放哪裡了？"),
        (f"Nimm bitte {a} {word} mit.", f"請把{zh}一起帶上。"),
        (f"{Art} {word} gehört {name}.", f"這個{zh}是{name}的。"),
        (f"Ich brauche noch {a} {word}.", f"我還需要{zh}。"),
        (f"Neben {d} {word} steht eine Lampe.", f"{zh}旁邊有一盞燈。"),
    ]
    return bank[seed % len(bank)]


def ex_person(w, seed) -> tuple[str, str]:
    art, word, zh = w["article"], w["word"], short_zh(w["translation"])
    a, d, Art = akk(art), dat(art), cap(art)
    name = pick(NAMES, seed, 1)
    t_de, t_zh = pick(TIMES, seed, 2)
    bank = [
        (f"{Art} {word} heißt {name}.", f"這位{zh}叫{name}。"),
        (f"Ich treffe {a} {word} {t_de}.", f"我{t_zh}要見這位{zh}。"),
        (f"{Art} {word} hilft mir oft.", f"這位{zh}常幫我。"),
        (f"Kennst du {a} {word} schon lange?", f"你認識這位{zh}很久了嗎？"),
        (f"Wir danken {d} {word} für die Hilfe.", f"我們感謝這位{zh}的幫忙。"),
        (f"{Art} {word} kommt aus Taiwan.", f"這位{zh}來自台灣。"),
        (f"Sprich bitte mit {d} {word}.", f"請跟這位{zh}說一下。"),
        (f"{name} ist {art} {word} von mir.", f"{name}是我的{zh}。"),
        (f"{Art} {word} wartet draußen.", f"這位{zh}在外面等。"),
        (f"Ohne {a} {word} schaffen wir das nicht.", f"沒有這位{zh}我們辦不到。"),
    ]
    return bank[seed % len(bank)]


def ex_food(w, seed) -> tuple[str, str]:
    art, word, zh = w["article"], w["word"], short_zh(w["translation"])
    name = pick(NAMES, seed, 1)
    if art:
        a, d, Art = akk(art), dat(art), cap(art)
        bank = [
            (f"Ich esse gern {a} {word}.", f"我喜歡吃{zh}。"),
            (f"Möchtest du {a} {word}?", f"你想要{zh}嗎？"),
            (f"{name} kauft {a} {word} auf dem Markt.", f"{name}在市場買{zh}。"),
            (f"Zum Frühstück gibt es {a} {word}.", f"早餐有{zh}。"),
            (f"Schmeckt dir {art} {word}?", f"你覺得{zh}好吃嗎？"),
            (f"Bitte reich mir {a} {word}.", f"請把{zh}遞給我。"),
            (f"Ohne {a} {word} schmeckt es fad.", f"沒有{zh}會淡而無味。"),
            (f"Wir kochen heute mit {d} {word}.", f"我們今天用{zh}烹調。"),
            (f"{Art} {word} ist frisch.", f"{zh}很新鮮。"),
            (f"Ich hätte gern noch {a} {word}.", f"我想再要一點{zh}。"),
        ]
    else:
        bank = [
            (f"Ich esse gern {word}.", f"我喜歡吃{zh}。"),
            (f"Möchtest du {word}?", f"你想要{zh}嗎？"),
            (f"{name} kauft {word} auf dem Markt.", f"{name}在市場買{zh}。"),
            (f"Zum Frühstück gibt es {word}.", f"早餐有{zh}。"),
            (f"Schmeckt dir {word}?", f"你覺得{zh}好吃嗎？"),
            (f"Bitte reich mir {word}.", f"請把{zh}遞給我。"),
            (f"Ohne {word} schmeckt es fad.", f"沒有{zh}會淡而無味。"),
            (f"Wir kochen heute mit {word}.", f"我們今天用{zh}烹調。"),
            (f"{word.capitalize()} ist frisch.", f"{zh}很新鮮。"),
            (f"Ich hätte gern noch {word}.", f"我想再要一點{zh}。"),
        ]
    return bank[seed % len(bank)]


def ex_time(w, seed) -> tuple[str, str]:
    art, word, zh = w["article"], w["word"], short_zh(w["translation"])
    name = pick(NAMES, seed, 1)
    low = word.lower()
    if low in {
        "montag", "dienstag", "mittwoch", "donnerstag", "freitag", "samstag", "sonntag",
    }:
        bank = [
            (f"Am {word} habe ich frei.", f"{zh}我休息。"),
            (f"Sehen wir uns am {word}?", f"我們{zh}見面談嗎？"),
            (f"{name} kommt am {word}.", f"{name}{zh}會來。"),
            (f"Am {word} beginnt der Kurs.", f"課程從{zh}開始。"),
            (f"Kannst du am {word}?", f"你{zh}可以嗎？"),
            (f"Bis {word} muss ich das abgeben.", f"我必須在{zh}前交出去。"),
            (f"Jeden {word} gehe ich schwimmen.", f"每個{zh}我去游泳。"),
            (f"Am {word} regnet es oft.", f"{zh}常常下雨。"),
        ]
        return bank[seed % len(bank)]
    if not art:
        bank = [
            (f"Was machst du {word}?", f"你{zh}做什麼？"),
            (f"{word} habe ich viel zu tun.", f"{zh}我有很多事。"),
            (f"Wir sprechen {word} darüber.", f"我們{zh}再談這件事。"),
            (f"{name} kommt {word}.", f"{name}{zh}會來。"),
        ]
        return bank[seed % len(bank)]
    a, d, Art = akk(art), dat(art), cap(art)
    bank = [
        (f"{Art} {word} beginnt um 9 Uhr.", f"{zh}九點開始。"),
        (f"Wir verschieben es auf {a} {word}.", f"我們改到{zh}。"),
        (f"Seit {d} {word} fühle ich mich besser.", f"從{zh}起我感覺好多了。"),
        (f"{name} kommt erst nach {d} {word}.", f"{name}要到{zh}之後才來。"),
        (f"Vergiss {a} {word} nicht im Kalender!", f"日曆上別忘了標{zh}！"),
        (f"In {d} {word} habe ich eine Prüfung.", f"{zh}我有考試。"),
        (f"{Art} {word} reicht völlig aus.", f"這個{zh}完全夠用。"),
        (f"Bis zu {d} {word} muss ich fertig sein.", f"到{zh}之前我必須做完。"),
        (f"Wir sprechen später über {a} {word}.", f"我們稍後再談{zh}。"),
        (f"Ich brauche mehr {word}." if art == "die" and word.endswith("zeit") else f"Ich plane {a} {word} sorgfältig.", f"我仔細規畫{zh}。"),
    ]
    return bank[seed % len(bank)]


def ex_travel(w, seed) -> tuple[str, str]:
    art, word, zh = w["article"], w["word"], short_zh(w["translation"])
    a, d, Art = akk(art), dat(art), cap(art)
    name = pick(NAMES, seed, 1)
    t_de, t_zh = pick(TIMES, seed, 2)
    bank = [
        (f"{Art} {word} ist {t_de}.", f"{zh}是{t_zh}。"),
        (f"Hast du {a} {word} schon organisiert?", f"你把{zh}安排好了嗎？"),
        (f"Wegen {d} {word} kommen wir später.", f"因為{zh}，我們會晚到。"),
        (f"{name} fragt nach {d} {word}.", f"{name}在詢問{zh}。"),
        (f"Ohne {a} {word} können wir nicht weiterreisen.", f"沒有{zh}我們無法繼續旅程。"),
        (f"Bitte zeig mir {a} {word}.", f"請把{zh}給我看。"),
        (f"Wo finde ich {a} {word}?", f"我在哪裡可以找到{zh}？"),
        (f"Die Info zu {d} {word} steht auf dem Schild.", f"關於{zh}的資訊寫在牌子上。"),
        (f"Wir warten noch auf {a} {word}.", f"我們還在等{zh}。"),
        (f"{Art} {word} hat sich geändert.", f"{zh}有變動。"),
    ]
    return bank[seed % len(bank)]


def ex_nature(w, seed) -> tuple[str, str]:
    art, word, zh = w["article"], w["word"], short_zh(w["translation"])
    a, d, Art = akk(art), dat(art), cap(art)
    name = pick(NAMES, seed, 1)
    bank = [
        (f"{Art} {word} ist heute besonders schön.", f"今天的{zh}特別美。"),
        (f"Wir gehen zum {word}." if art == "der" else f"Wir gehen zu {d} {word}.", f"我們去{zh}。"),
        (f"{name} fotografiert {a} {word}.", f"{name}在拍{zh}。"),
        (f"Neben {d} {word} wachsen Blumen.", f"{zh}旁邊長著花。"),
        (f"Im Sommer liebe ich {a} {word}.", f"夏天我很喜歡{zh}。"),
        (f"Von hier sieht man {a} {word}.", f"從這裡可以看到{zh}。"),
        (f"Kinder spielen bei {d} {word}.", f"孩子們在{zh}附近玩。"),
        (f"{Art} {word} liegt nicht weit von hier.", f"{zh}離這裡不遠。"),
        (f"Wir machen ein Picknick am {word}." if art == "der" else f"Wir machen ein Picknick bei {d} {word}.", f"我們在{zh}野餐。"),
        (f"Ohne {a} {word} wäre die Stadt trist.", f"沒有{zh}這城市會很無趣。"),
    ]
    return bank[seed % len(bank)]


def ex_abstract(w, seed) -> tuple[str, str]:
    art, word, zh = w["article"], w["word"], short_zh(w["translation"])
    a, d, Art = akk(art), dat(art), cap(art)
    name = pick(NAMES, seed, 1)
    level = w["level"]
    if level in ("A1", "A2"):
        bank = [
            (f"{Art} {word} ist für mich wichtig.", f"對我來說，「{zh}」很重要。"),
            (f"Kannst du mir {a} {word} erklären?", f"你可以跟我解釋「{zh}」嗎？"),
            (f"Ich verstehe {a} {word} jetzt besser.", f"我現在比較懂「{zh}」了。"),
            (f"Heute sprechen wir über {a} {word}.", f"今天我們談「{zh}」。"),
            (f"{name} kennt sich mit {d} {word} aus.", f"{name}對「{zh}」很熟。"),
            (f"Ein Beispiel macht {a} {word} klarer.", f"舉例能讓「{zh}」更清楚。"),
            (f"Ohne {a} {word} fehlt der Sinn.", f"沒有「{zh}」意思就不完整。"),
            (f"Was bedeutet {art} {word} genau?", f"「{zh}」精確是什麼意思？"),
            (f"Wir üben heute {a} {word} in Sätzen.", f"我們今天用句子練習「{zh}」。"),
            (f"Ich notiere mir {a} {word}.", f"我把「{zh}」記下來。"),
        ]
    elif level == "B1":
        bank = [
            (f"Seine {word} war von Anfang an klar." if art == "die" else f"Sein {word} war von Anfang an klar.", f"他的{zh}一開始就很清楚。"),
            (f"Wir müssen über {a} {word} sprechen.", f"我們必須談談「{zh}」。"),
            (f"Wegen {d} {word} haben wir den Plan geändert.", f"因為「{zh}」，我們改了計畫。"),
            (f"{name} unterschätzt {a} {word} oft.", f"{name}常低估「{zh}」。"),
            (f"Ein gutes Beispiel zeigt {a} {word} deutlich.", f"好例子能清楚說明「{zh}」。"),
            (f"Im Bericht steht etwas zu {d} {word}.", f"報告裡有關於「{zh}」的內容。"),
            (f"Ohne {a} {word} bleibt die Lösung unvollständig.", f"沒有「{zh}」，方案就不完整。"),
            (f"Die Frage nach {d} {word} ist berechtigt.", f"關於「{zh}」的問題問得很合理。"),
            (f"Ich habe {a} {word} erst später verstanden.", f"我後來才理解「{zh}」。"),
            (f"{Art} {word} hilft uns bei der Entscheidung.", f"「{zh}」有助於我們做決定。"),
        ]
    else:
        bank = [
            (f"Im Text wird {art} {word} differenziert diskutiert.", f"文本對「{zh}」做了細緻討論。"),
            (f"Kritiker hinterfragen gerade {a} {word}.", f"批評者正在質疑「{zh}」。"),
            (f"{name} ordnet {a} {word} in einen größeren Zusammenhang ein.", f"{name}把「{zh}」放入更大脈絡。"),
            (f"Die Relevanz von {d} {word} wird oft unterschätzt.", f"「{zh}」的重要性常被低估。"),
            (f"Ohne Bezug auf {a} {word} greift die These zu kurz.", f"若不涉及「{zh}」，論點就失之偏頗。"),
            (f"Eine klare Definition von {d} {word} ist nötig.", f"必須先清楚定義「{zh}」。"),
            (f"Der Vortrag beleuchtet {a} {word} aus zwei Perspektiven.", f"演講從兩個角度談「{zh}」。"),
            (f"Zwischen Theorie und Praxis vermittelt {art} {word}.", f"「{zh}」連結理論與實踐。"),
            (f"Man sollte {a} {word} nicht isoliert betrachten.", f"不應孤立看待「{zh}」。"),
            (f"Angesichts {d} {word} erscheint Vorsicht geboten.", f"鑑於「{zh}」，需要謹慎。"),
        ]
    return bank[seed % len(bank)]


def classify_verb(word: str, zh: str) -> str:
    w = word.lower()
    if w in {
        "wohnen", "leben", "übernachten",
    } or has_any(zh, ("住", "居住", "生活")):
        return "reside"
    if w in {
        "gehen", "kommen", "fahren", "laufen", "rennen", "fliegen", "schwimmen",
        "wandern", "reisen", "folgen", "starten", "landen",
    } or has_any(zh, ("走", "來", "去", "開", "跑", "飛", "游", "旅行")):
        return "motion"
    if w in {
        "stehen", "sitzen", "liegen", "bleiben", "warten", "hängen",
    } or has_any(zh, ("站", "坐", "躺", "留", "等")):
        return "posture"
    if w in {
        "einsteigen", "aussteigen", "umsteigen", "abfahren", "ankommen",
        "mitkommen", "mitfahren", "abholen", "bringen",
    } or has_any(zh, ("上車", "下車", "轉車", "出發", "到達", "一起來")):
        return "transit"
    if w in {
        "essen", "trinken", "kochen", "backen", "schmecken", "bestellen", "probieren",
    } or has_any(zh, ("吃", "喝", "煮", "烤", "點餐", "味道")):
        return "food"
    if w in {
        "sprechen", "sagen", "reden", "fragen", "antworten", "erzählen",
        "schreiben", "lesen", "hören", "sehen", "schauen", "rufen", "anrufen",
        "erklären", "übersetzen", "wiederholen",
    } or has_any(zh, ("說", "問", "答", "寫", "讀", "聽", "看", "講", "打電話", "解釋", "翻譯")):
        return "communicate"
    if w in {
        "helfen", "danken", "treffen", "einladen", "besuchen", "begrüßen", "entschuldigen",
    } or has_any(zh, ("幫", "謝", "見", "邀", "訪", "打招呼", "道歉")):
        return "social"
    if w in {
        "lernen", "studieren", "üben", "arbeiten", "üben", "prüfen", "bestehen",
    } or has_any(zh, ("學", "唸", "練", "工作", "考試", "及格")):
        return "study"
    if w in {
        "putzen", "waschen", "aufräumen", "einkaufen", "duschen",
        "anziehen", "ausziehen", "öffnen", "schließen", "bauen", "reparieren",
    } or has_any(zh, ("打掃", "洗", "收拾", "購物", "淋浴", "穿", "脫", "開", "關", "建", "修")):
        return "household"
    if w in {
        "denken", "finden", "verstehen", "wissen", "kennen", "glauben", "meinen",
        "erinnern", "vergessen", "entscheiden", "wählen",
    } or has_any(zh, ("想", "找", "懂", "知道", "認識", "相信", "記得", "忘", "決定", "選")):
        return "think"
    if w in {
        "funktionieren", "klappen", "passieren", "geschehen", "geben", "nehmen",
        "bekommen", "brauchen", "benutzen", "brauchen", "zählen", "messen", "wiegen",
    }:
        return "misc"
    return "activity"


# High-frequency verbs — examples MUST contain the infinitive lemma as written
VERB_CURATED: dict[str, tuple[str, str]] = {
    "wohnen": ("Ich möchte in Berlin wohnen.", "我想住在柏林。"),
    "leben": ("Wir wollen lange hier leben.", "我們想在這裡長期生活。"),
    "gehen": ("Wir wollen jetzt nach Hause gehen.", "我們現在想回家。"),
    "kommen": ("Möchtest du morgen kommen?", "你明天想來嗎？"),
    "fahren": ("Wir wollen mit dem Bus fahren.", "我們想搭公車。"),
    "laufen": ("Ich möchte jeden Morgen laufen.", "我想每天早上跑步。"),
    "fliegen": ("Nächste Woche wollen wir nach Wien fliegen.", "下週我們想飛去維也納。"),
    "schwimmen": ("Im Sommer möchte ich schwimmen.", "夏天我想游泳。"),
    "stehen": ("Bitte bleib kurz stehen!", "請先停一下！"),
    "sitzen": ("Darf ich hier sitzen?", "我可以坐這裡嗎？"),
    "liegen": ("Das Buch soll auf dem Tisch liegen.", "書應該放在桌上。"),
    "bleiben": ("Ich möchte heute Abend zu Hause bleiben.", "我今晚想待在家。"),
    "warten": ("Wir müssen auf den Bus warten.", "我們得等公車。"),
    "einsteigen": ("Bitte hier einsteigen!", "請從這裡上車！"),
    "aussteigen": ("Wir müssen an der nächsten Station aussteigen.", "我們得在下一站下車。"),
    "umsteigen": ("In Köln müssen wir umsteigen.", "我們得在科隆轉車。"),
    "abfahren": ("Der Zug soll um 9 Uhr abfahren.", "火車應該九點出發。"),
    "ankommen": ("Wann sollen wir in Hamburg ankommen?", "我們該什麼時候抵達漢堡？"),
    "mitkommen": ("Möchtest du heute Abend mitkommen?", "你今晚想一起來嗎？"),
    "essen": ("Wir wollen um 12 Uhr essen.", "我們想十二點吃飯。"),
    "trinken": ("Möchtest du etwas trinken?", "你想喝點什麼嗎？"),
    "kochen": ("Anna will heute Pasta kochen.", "Anna 今天想煮義大利麵。"),
    "sprechen": ("Kannst du Deutsch sprechen?", "你會說德文嗎？"),
    "sagen": ("Kannst du das noch einmal sagen?", "你可以再說一次嗎？"),
    "fragen": ("Darf ich etwas fragen?", "我可以問一件事嗎？"),
    "antworten": ("Bitte auf die E-Mail antworten!", "請回覆這封郵件！"),
    "schreiben": ("Ich möchte eine Nachricht schreiben.", "我想寫一則訊息。"),
    "lesen": ("Abends möchte ich ein Buch lesen.", "晚上我想看書。"),
    "hören": ("Kannst du die Musik hören?", "你聽得到音樂嗎？"),
    "sehen": ("Kannst du das Schild dort sehen?", "你看得到那邊的牌子嗎？"),
    "helfen": ("Kannst du mir bitte helfen?", "可以請你幫我嗎？"),
    "danken": ("Ich möchte dir für deine Hilfe danken.", "我想謝謝你的幫忙。"),
    "treffen": ("Wir wollen uns um 5 Uhr treffen.", "我們想五點碰面。"),
    "lernen": ("Ich möchte jeden Tag Deutsch lernen.", "我想每天學德文。"),
    "arbeiten": ("Er will im Büro arbeiten.", "他想在辦公室工作。"),
    "studieren": ("Sie will Medizin studieren.", "她想唸醫學。"),
    "üben": ("Wir wollen die Dialoge noch einmal üben.", "我們想再練一次對話。"),
    "einkaufen": ("Am Samstag gehe ich einkaufen.", "星期六我去購物。"),
    "putzen": ("Am Sonntag müssen wir die Küche putzen.", "星期天我們得打掃廚房。"),
    "waschen": ("Ich muss noch die Wäsche waschen.", "我還得洗衣服。"),
    "anziehen": ("Bitte eine Jacke anziehen, es ist kalt.", "請穿件外套，外面冷。"),
    "öffnen": ("Kannst du bitte das Fenster öffnen?", "可以請你開窗嗎？"),
    "schließen": ("Bitte die Tür schließen!", "請把門關上！"),
    "bringen": ("Kannst du mir ein Glas Wasser bringen?", "你可以幫我拿杯水來嗎？"),
    "finden": ("Ich kann den Schlüssel nicht finden.", "我找不到鑰匙。"),
    "suchen": ("Wir müssen einen Parkplatz suchen.", "我們得找停車位。"),
    "verstehen": ("Ich kann die Frage nicht verstehen.", "我聽不懂這個問題。"),
    "wissen": ("Das will ich genau wissen.", "這件事我想確實知道。"),
    "kennen": ("Diesen Film kennen viele Leute.", "很多人都認識／看過這部電影。"),
    "denken": ("Was soll ich darüber denken?", "這件事我該怎麼想？"),
    "vergessen": ("Die Flasche nicht vergessen!", "別忘了水瓶！"),
    "erinnern": ("Ich kann mich kaum an ihn erinnern.", "我幾乎想不起他。"),
    "kaufen": ("Ich möchte Brot beim Bäcker kaufen.", "我想在麵包店買麵包。"),
    "verkaufen": ("Das Geschäft will frisches Obst verkaufen.", "這家店想賣新鮮水果。"),
    "brauchen": ("Ich werde noch etwas Zeit brauchen.", "我還會需要一點時間。"),
    "benutzen": ("Darf ich dein Handy benutzen?", "我可以用你的手機嗎？"),
    "funktionieren": ("Der Drucker will nicht funktionieren.", "印表機就是不能用。"),
    "klappen": ("Hoffentlich wird alles gut klappen.", "希望一切都能順利。"),
    "steigen": ("Die Preise werden wieder steigen.", "物價又會上漲。"),
    "zählen": ("Kannst du bis zehn zählen?", "你可以數到十嗎？"),
    "messen": ("Wir müssen die Temperatur messen.", "我們得量溫度。"),
    "wiegen": ("Kannst du den Koffer wiegen?", "你可以秤一下行李箱嗎？"),
    "bauen": ("Die Kinder wollen einen Turm bauen.", "孩子們想蓋一座塔。"),
    "entschuldigen": ("Entschuldigen Sie bitte die Verspätung.", "請原諒我遲到。"),
    "rufen": ("Bitte mich später anrufen!", "請晚點打給我！"),
    "anrufen": ("Ich will dich nach der Arbeit anrufen.", "下班後我想打給你。"),
    "duschen": ("Ich möchte schnell duschen und dann kommen.", "我想先快速冲個澡再過來。"),
    "probieren": ("Möchtest du den Kuchen probieren?", "你想試試這蛋糕嗎？"),
    "singen": ("Wir wollen zusammen ein Lied singen.", "我們想一起唱一首歌。"),
    "passen": ("Die Jacke soll mir gut passen.", "這件外套應該要很適合我。"),
    "stimmen": ("Das kann so nicht stimmen.", "這不可能是對的。"),
    "zeigen": ("Kannst du mir den Weg zeigen?", "你可以指給我看路怎麼走嗎？"),
    "zwingen": ("Niemand darf dich dazu zwingen.", "誰都不能強迫你這麼做。"),
    "enthalten": ("Der Saft darf nicht zu viel Zucker enthalten.", "這果汁不該含太多糖。"),
    "rechnen": ("Kannst du das bitte nachrechnen?", "可以請你再算一次嗎？"),
    "schneiden": ("Ich will das Brot in Scheiben schneiden.", "我想把麵包切成片。"),
    "decken": ("Bitte den Tisch decken!", "請擺好桌子！"),
    "löschen": ("Bitte das Licht löschen!", "請把燈關掉！"),
    "vorschlagen": ("Ich möchte vorschlagen, früher zu gehen.", "我想建議早點走。"),
    "rennen": ("Die Kinder wollen im Hof rennen.", "孩子們想在院子裡跑。"),
    "zurückkommen": ("Wann willst du zurückkommen?", "你想什麼時候回來？"),
    "erzählen": ("Bitte von deiner Reise erzählen!", "請跟我說說你的旅行！"),
    "mitessen": ("Darfst du bei uns mitessen?", "你可以跟我們一起吃饭嗎？"),
    "heißen": ("Wie soll das Kind heißen?", "這孩子該叫什麼名字？"),
    "machen": ("Was sollen wir jetzt machen?", "我們現在該做什麼？"),
    "geben": ("Kannst du mir das Buch geben?", "你可以給我那本書嗎？"),
    "nehmen": ("Darf ich noch einen Apfel nehmen?", "我可以再拿一個蘋果嗎？"),
    "spielen": ("Die Kinder wollen draußen spielen.", "孩子們想在外面玩。"),
}


def ex_verb(w, seed) -> tuple[str, str]:
    word, zh = w["word"], short_zh(w["translation"])
    key = word.lower()
    if key in VERB_CURATED:
        de, zhex = VERB_CURATED[key]
        if w["level"] in ("B2", "C1"):
            name = pick(NAMES, seed, 2)
            if de.endswith((".", "!", "?")):
                de = f"{de[:-1]} — sagt {name}{de[-1]}"
                zhex = f"{zhex}（{name}這麼說）"
        return de, zhex

    level = w["level"]
    name = pick(NAMES, seed, 1)
    place_de, place_zh = pick(PLACES, seed, 2)
    t_de, t_zh = pick(TIMES, seed, 3)
    kind = classify_verb(word, zh)

    if kind == "reside":
        bank = [
            (f"Ich möchte {place_de} {word}.", f"我想在{place_zh}{zh}。"),
            (f"Wo möchtest du {word}?", f"你想在哪裡{zh}？"),
            (f"{name} will lange hier {word}.", f"{name}想在這裡長期{zh}。"),
            (f"Wir können hier günstig {word}.", f"我們可以在這裡便宜地{zh}。"),
            (f"Planst du, in München zu {word}?", f"你打算在慕尼黑{zh}嗎？"),
            (f"Es ist schön, nah bei der Uni zu {word}.", f"能住在大學附近很好（{zh}）。"),
            (f"Seit wann möchtest du hier {word}?", f"你從什麼時候起想在這裡{zh}？"),
            (f"Viele Studenten möchten in Wohngemeinschaften {word}.", f"很多學生想在共用公寓{zh}。"),
        ]
    elif kind == "motion":
        bank = [
            (f"Wir wollen {t_de} {word}.", f"我們想{t_zh}{zh}。"),
            (f"Lass uns zusammen {word}!", f"我們一起{zh}吧！"),
            (f"{name} muss früher {word}.", f"{name}必須早點{zh}。"),
            (f"Wann können wir {word}?", f"我們什麼時候可以{zh}？"),
            (f"Bist du bereit zu {word}?", f"你準備好{zh}了嗎？"),
            (f"Ohne Ticket kannst du nicht {word}.", f"沒票你就不能{zh}。"),
            (f"Heute dürfen wir länger {word}.", f"今天我們可以多{zh}一會兒。"),
            (f"Ich habe Lust zu {word}.", f"我很想{zh}。"),
        ]
    elif kind == "posture":
        bank = [
            (f"Darf ich hier kurz {word}?", f"我可以在這裡稍{zh}一下嗎？"),
            (f"Bitte nicht auf dem Boden {word}!", f"請不要在地板上{zh}！"),
            (f"{name} möchte noch ein bisschen {word}.", f"{name}還想再{zh}一會兒。"),
            (f"Wir können hier ruhig {word}.", f"我們可以安靜地在這裡{zh}。"),
            (f"Lass uns einen Moment {word}.", f"我們{zh}一會兒吧。"),
            (f"Hier kannst du bequem {word}.", f"你在這裡可以舒服地{zh}。"),
            (f"Zu lange zu {word} ist ungesund.", f"{zh}太久對身體不好。"),
            (f"Ich muss warten und darf nicht {word}.", f"我得等著，不能{zh}。"),
        ]
    elif kind == "transit":
        bank = [
            (f"Bitte jetzt {word}!", f"請現在{zh}！"),
            (f"Wir müssen in Köln {word}.", f"我們必須在科隆{zh}。"),
            (f"Vergiss nicht rechtzeitig zu {word}.", f"別忘了準時{zh}。"),
            (f"{name} sagt, wir sollen {word}.", f"{name}說我們該{zh}。"),
            (f"Wann sollen wir {word}?", f"我們該什麼時候{zh}？"),
            (f"Ohne Hilfe kann ich nicht {word}.", f"沒人幫我，我沒辦法{zh}。"),
            (f"Der Durchsage nach müssen alle {word}.", f"廣播說大家都要{zh}。"),
            (f"Bist du bereit zu {word}?", f"你準備好{zh}了嗎？"),
        ]
    elif kind == "food":
        bank = [
            (f"Möchtest du etwas {word}?", f"你想{zh}一點嗎？"),
            (f"Wir können später zusammen {word}.", f"我們可以稍後一起{zh}。"),
            (f"{name} will heute nicht {word}.", f"{name}今天不想{zh}。"),
            (f"Lass uns zu Hause {word}!", f"我們在家{zh}吧！"),
            (f"Ich habe keine Zeit zu {word}.", f"我沒時間{zh}。"),
            (f"Zum Abendessen können wir {word}.", f"晚餐時我們可以{zh}。"),
            (f"Hast du Lust zu {word}?", f"你有興致{zh}嗎？"),
            (f"Ohne Hunger will ich nicht {word}.", f"不餓我就不想{zh}。"),
        ]
    elif kind == "communicate":
        bank = [
            (f"Kannst du das bitte noch einmal {word}?", f"可以請你再{zh}一次嗎？"),
            (f"Ich möchte kurz mit dir {word}.", f"我想跟你短暫{zh}一下。"),
            (f"Wir sollten ruhig {word}.", f"我們應該冷靜地{zh}。"),
            (f"{name} kann gut Deutsch {word}.", f"{name}很會用德文{zh}。"),
            (f"Darf ich etwas {word}?", f"我可以{zh}一下嗎？"),
            (f"Bitte laut und deutlich {word}!", f"請大聲清楚地{zh}！"),
            (f"Ohne Mikro können wir nicht {word}.", f"沒麥克風我們沒辦法{zh}。"),
            (f"Lass uns darüber {word}.", f"我們來{zh}這件事吧。"),
        ]
    elif kind == "social":
        bank = [
            (f"Ich möchte dich bald {word}.", f"我想快點{zh}你。"),
            (f"Wir können uns morgen {word}.", f"我們明天可以{zh}。"),
            (f"{name} will uns am Wochenende {word}.", f"{name}週末想{zh}我們。"),
            (f"Darf ich dich kurz {word}?", f"我可以短暫{zh}你一下嗎？"),
            (f"Es ist schön, Freunde zu {word}.", f"{zh}朋友是件美好的事。"),
            (f"Ohne Termin können wir uns nicht {word}.", f"沒約好我們沒辦法{zh}。"),
            (f"Lass uns öfter {word}!", f"我們多{zh}吧！"),
            (f"Ich habe vergessen zu {word}.", f"我忘了要{zh}。"),
        ]
    elif kind == "study":
        bank = [
            (f"Ich muss heute noch {word}.", f"我今天還必須{zh}。"),
            (f"Wir wollen zusammen {word}.", f"我們想一起{zh}。"),
            (f"{name} beginnt um 9 Uhr zu {word}.", f"{name}九點開始{zh}。"),
            (f"Ohne Pause kann ich nicht gut {word}.", f"不休息我就沒辦法好好{zh}。"),
            (f"Hast du Zeit zu {word}?", f"你有時間{zh}嗎？"),
            (f"Lass uns konzentriert {word}.", f"我們專心{zh}吧。"),
            (f"Jeden Tag ein bisschen {word} hilft.", f"每天{zh}一點點很有幫助。"),
            (f"Ich plane, am Wochenende zu {word}.", f"我計畫週末{zh}。"),
        ]
    elif kind == "household":
        bank = [
            (f"Ich muss heute noch {word}.", f"我今天還得{zh}。"),
            (f"Kannst du mir bitte dabei helfen zu {word}?", f"可以請你幫我{zh}嗎？"),
            (f"Wir wollen am Samstag {word}.", f"我們星期六想{zh}。"),
            (f"{name} hat keine Lust zu {word}.", f"{name}不想{zh}。"),
            (f"Vor dem Besuch sollten wir {word}.", f"客人來之前我們該{zh}。"),
            (f"Lass uns zuerst {word}.", f"我們先{zh}吧。"),
            (f"Ohne Werkzeug kann ich nicht {word}.", f"沒工具我沒辦法{zh}。"),
            (f"Zu zweit geht das {word} schneller.", f"兩人一起{zh}比較快。"),
        ]
    elif kind == "think":
        bank = [
            (f"Was soll ich davon {word}?", f"這件事我該怎麼{zh}？"),
            (f"Ich kann das noch nicht {word}.", f"我還沒辦法{zh}這件事。"),
            (f"Lass uns in Ruhe {word}.", f"我們冷靜下來{zh}吧。"),
            (f"{name} versucht zu {word}.", f"{name}試著{zh}。"),
            (f"Ohne Beispiel kann ich es nicht {word}.", f"沒有例子我沒辦法{zh}。"),
            (f"Wir müssen klar {word}.", f"我們必須清楚地{zh}。"),
            (f"Das ist schwer zu {word}.", f"這很難{zh}。"),
            (f"Bitte hilf mir zu {word}.", f"請幫我{zh}。"),
        ]
    elif kind == "misc":
        bank = [
            (f"Warum will das nicht {word}?", f"為什麼這沒辦法{zh}？"),
            (f"Hoffentlich wird alles gut {word}.", f"希望一切都能順利{zh}。"),
            (f"Ohne Strom kann nichts {word}.", f"沒電什麼都沒辦法{zh}。"),
            (f"Bitte prüfe, ob es richtig {word}.", f"請檢查它是否正常{zh}。"),
            (f"Manchmal muss man einfach abwarten und {word}.", f"有時人就是得等待並{zh}。"),
            (f"Ich hoffe, dass es bald {word}.", f"我希望很快就能{zh}。"),
            (f"Erzähl mir, wie das {word}.", f"跟我說說這是怎麼{zh}的。"),
            (f"Das soll so nicht {word}.", f"這不該這樣{zh}。"),
        ]
    else:
        bank = [
            (f"Ich möchte später {word}.", f"我想稍後再{zh}。"),
            (f"Wir können zusammen {word}.", f"我們可以一起{zh}。"),
            (f"{name} hat keine Zeit zu {word}.", f"{name}沒時間{zh}。"),
            (f"Lass uns in Ruhe {word}.", f"我們慢慢{zh}吧。"),
            (f"Ohne Plan ist es schwer zu {word}.", f"沒計畫就很難{zh}。"),
            (f"Bist du bereit zu {word}?", f"你準備好{zh}了嗎？"),
            (f"Heute ist ein guter Tag, um zu {word}.", f"今天很適合{zh}。"),
            (f"Ich lerne Schritt für Schritt zu {word}.", f"我一步步學著{zh}。"),
            (f"Wir sollten früher anfangen zu {word}.", f"我們該早點開始{zh}。"),
            (f"Mach dir keine Sorgen und fang einfach an zu {word}.", f"別擔心，直接開始{zh}就好。"),
        ]

    # Higher levels: prefer zu-infinitive planning frames if not curated
    if level in ("B1", "B2", "C1") and kind not in {"misc"}:
        advanced = [
            (f"Es ist sinnvoll, rechtzeitig zu {word}.", f"及時{zh}是合理的。"),
            (f"Wir planen, nächste Woche zu {word}.", f"我們計畫下週{zh}。"),
            (f"{name} schlägt vor, gemeinsam zu {word}.", f"{name}建議一起{zh}。"),
            (f"Bevor wir entscheiden, sollten wir {word}.", f"決定前我們應該先{zh}。"),
            (f"Ohne Vorbereitung ist es riskant zu {word}.", f"沒準備就{zh}會有風險。"),
            (f"Ich habe keine Lust mehr zu {word}.", f"我沒興致再{zh}了。"),
        ]
        if level != "B1":
            advanced.extend([
                (f"Kritiker fordern, sorgfältiger zu {word}.", f"批評者要求更仔細地{zh}。"),
                (f"Die Fähigkeit zu {word} wird erwartet.", f"大家期待具備{zh}的能力。"),
            ])
        # mix: prefer advanced but keep some basic
        bank = advanced + bank[:4]

    return bank[seed % len(bank)]


def classify_adj(zh: str, word: str) -> str:
    if has_any(zh, COLOR_HINTS) or word.lower() in {
        "rot", "blau", "grün", "gelb", "schwarz", "weiß", "weiss", "grau", "braun", "rosa", "orange", "lila",
    }:
        return "color"
    if has_any(zh, ("高興", "難過", "累", "氣", "怕", "緊張", "開心", "無聊", "滿意", "失望", "興")):
        return "feeling"
    if has_any(zh, ("大", "小", "長", "短", "高", "低", "寬", "重", "輕", "厚", "薄")):
        return "size"
    if has_any(zh, ("熱", "冷", "暖", "涼", "晴", "雨", "濕", "乾")):
        return "weather"
    if has_any(zh, ("貴", "便宜", "快", "慢", "新", "舊", "好", "壞", "美", "醜", "乾淨", "髒")):
        return "quality"
    if has_any(zh, ("可能", "必要", "重要", "簡單", "複雜", "清楚", "困難", "容易", "危險", "安全")):
        return "eval"
    return "quality"


def ex_adj(w, seed) -> tuple[str, str]:
    word, zh = w["word"], short_zh(w["translation"])
    name = pick(NAMES, seed, 1)
    kind = classify_adj(zh, word)
    if kind == "color":
        bank = [
            (f"Das Auto ist {word}.", f"這輛車是{zh}。"),
            (f"Sie trägt ein {word}es Kleid.", f"她穿著{zh}的衣服。"),
            (f"Welche Farbe? — {word.capitalize()}.", f"什麼顏色？——{zh}。"),
            (f"Der Himmel wird {word}.", f"天空變成{zh}。"),
            (f"{name} mag die Farbe {word}.", f"{name}喜歡{zh}。"),
            (f"Streich die Wand {word}!", f"把牆漆成{zh}！"),
            (f"Die Blume ist leuchtend {word}.", f"這朵花是亮{zh}。"),
            (f"Nimm bitte den {word}en Stift.", f"請拿那支{zh}的筆。"),
        ]
    elif kind == "feeling":
        bank = [
            (f"Heute fühle ich mich {word}.", f"今天我覺得{zh}。"),
            (f"{name} wirkt ziemlich {word}.", f"{name}看起來相當{zh}。"),
            (f"Warum bist du so {word}?", f"你為什麼這麼{zh}？"),
            (f"Ich bin nicht mehr {word}.", f"我不{zh}了。"),
            (f"Nach der Prüfung waren alle {word}.", f"考完後大家都{zh}。"),
            (f"Sei bitte nicht so {word}.", f"請不要這麼{zh}。"),
            (f"Das macht mich {word}.", f"這讓我覺得很{zh}。"),
            (f"Er bleibt trotz allem {word}.", f"他儘管如此仍很{zh}。"),
        ]
    elif kind == "weather":
        bank = [
            (f"Heute ist es {word}.", f"今天天氣很{zh}。"),
            (f"Zieh dich warm an, es wird {word}.", f"穿暖一點，會變{zh}。"),
            (f"Mir ist {word}.", f"我覺得{zh}。"),
            (f"Das Wasser ist {word}.", f"水很{zh}。"),
            (f"Im Zimmer ist es zu {word}.", f"房間裡太{zh}了。"),
            (f"Draußen bleibt es {word}.", f"外面一直很{zh}。"),
            (f"Ist dir {word}?", f"你覺得{zh}嗎？"),
            (f"Wegen des Wetters ist alles {word}.", f"因為天氣，一切都很{zh}。"),
        ]
    elif kind == "size":
        bank = [
            (f"Das Zimmer ist zu {word}.", f"這房間太{zh}了。"),
            (f"Der Tisch ist nicht {word} genug.", f"這桌子不夠{zh}。"),
            (f"Für mich ist die Tasche zu {word}.", f"對我來說這袋子太{zh}。"),
            (f"Wie {word} ist das Gebäude?", f"這棟建築有多{zh}？"),
            (f"{name} sucht etwas {word}eres.", f"{name}在找更{zh}的。"),
            (f"Die Wohnung wirkt überraschend {word}.", f"這公寓出奇地{zh}。"),
            (f"Bitte nimm die {word}e Schachtel.", f"請拿比較{zh}的盒子。"),
            (f"Das Problem ist größer — und ziemlich {word}.", f"問題更大，而且相當{zh}。"),
        ]
    elif kind == "eval":
        bank = [
            (f"Das ist wirklich {word}.", f"這真的很{zh}。"),
            (f"Die Aufgabe ist nicht {word}.", f"這任務並不{zh}。"),
            (f"Findest du das {word}?", f"你覺得這{zh}嗎？"),
            (f"Für Anfänger ist das zu {word}.", f"對初學者來說太{zh}。"),
            (f"Eine {word}e Erklärung hilft allen.", f"{zh}的說明對大家都有幫助。"),
            (f"{name} hält den Plan für {word}.", f"{name}覺得這計畫{zh}。"),
            (f"Es bleibt {word}, ob wir schaffen.", f"我們能不能做到，仍{zh}。"),
            (f"Sicherheitshalber ist Vorsicht {word}.", f"為了安全，謹慎是{zh}的。"),
        ]
    else:  # quality
        bank = [
            (f"Das sieht {word} aus.", f"這看起來很{zh}。"),
            (f"Der Film war ziemlich {word}.", f"這電影相當{zh}。"),
            (f"{name} findet die Idee {word}.", f"{name}覺得這想法很{zh}。"),
            (f"Bitte mach es nicht zu {word}.", f"請不要弄得太{zh}。"),
            (f"Für den Preis ist das {word}.", f"以這個價錢來說算{zh}。"),
            (f"Die Lösung klingt {word}.", f"這解法聽起來很{zh}。"),
            (f"Heute läuft alles {word}.", f"今天一切都很{zh}。"),
            (f"Ich hätte gern etwas {word}eres.", f"我想要更{zh}一點的。"),
        ]
        if has_any(zh, ("好吃", "美味", "甜", "鹹", "苦", "酸", "香")):
            bank[0] = (f"Das Essen schmeckt {word}.", f"這餐點吃起來很{zh}。")
    return bank[seed % len(bank)]


def ex_other(w, seed) -> tuple[str, str]:
    word, zh = w["word"], short_zh(w["translation"])
    name = pick(NAMES, seed, 1)
    bank = [
        (f"Was bedeutet „{word}“ auf Chinesisch?", f"「{word}」的中文是什麼？（{zh}）"),
        (f"{name} hat mir „{word}“ erklärt.", f"{name}跟我解釋了「{word}」（{zh}）。"),
        (f"Schreib bitte „{word}“ noch einmal.", f"請再寫一次「{word}」（{zh}）。"),
        (f"Ohne „{word}“ verstehe ich den Satz nicht.", f"沒有「{word}」（{zh}）我看不懂這句。"),
        (f"Merke dir: {word} = {zh}.", f"記住：{word}＝{zh}。"),
        (f"Im Text steht das Wort „{word}“.", f"課文裡有「{word}」（{zh}）。"),
        (f"Bitte übersetze „{word}“.", f"請翻譯「{word}」（{zh}）。"),
        (f"Ich notiere mir „{word}“.", f"我把「{word}」（{zh}）記下來。"),
    ]
    return bank[seed % len(bank)]


def lemma_in_example(word: str, de: str) -> bool:
    """A1/A2: dictionary form must appear as a contiguous substring (case-insensitive)."""
    return word.lower() in de.lower()


def force_lemma_example(w: dict) -> tuple[str, str]:
    word, zh = w["word"], short_zh(w["translation"])
    if w["category"] == "動詞":
        return (
            f"Ich möchte heute {word}.",
            f"我今天想要{zh}。",
        )
    if w["category"] == "形容詞":
        return (f"Das ist {word}.", f"這是{zh}的。")
    if w.get("article"):
        art = w["article"]
        return (f"{cap(art)} {word} ist wichtig.", f"這個{zh}很重要。")
    return (f"Was bedeutet „{word}“?", f"「{word}」是什麼意思？（{zh}）")


def make_example(w: dict, index: int) -> tuple[str, str]:
    key = w["word"].lower()
    level = w["level"]
    if key in AUX_VERBS_LEMMA:
        if level in ("A1", "A2"):
            de, zh = AUX_VERBS_LEMMA[key]
        else:
            de, zh = AUX_VERBS_FINITE.get(key, AUX_VERBS_LEMMA[key])
            if level in ("B2", "C1"):
                name = pick(NAMES, index, 4)
                de = f"{de[:-1]}, meint {name}." if de.endswith(".") else f"{de} — {name}"
                zh = f"{zh}（{name}這麼說）"
        return de, zh
    if key in CURATED:
        de, zh = CURATED[key]
        if w["level"] not in ("A1", "A2"):
            name = pick(NAMES, index, 3)
            if de.endswith("."):
                de = f"{de[:-1]} — sagt {name}."
                zh = f"{zh}（{name}這麼說）"
        return de, zh

    seed = (index * 5 + hmix(w["id"] + w["translation"])) & 0xFFFFFFFF
    if w.get("article"):
        kind = classify_noun(w)
        fn = {
            "place": ex_place,
            "object": ex_object,
            "person": ex_person,
            "food": ex_food,
            "time": ex_time,
            "travel": ex_travel,
            "nature": ex_nature,
            "abstract": ex_abstract,
            "illness": ex_illness,
        }[kind]
        de, zh = fn(w, seed)
    elif w["category"] == "動詞":
        de, zh = ex_verb(w, seed)
    elif w["category"] == "形容詞":
        de, zh = ex_adj(w, seed)
    else:
        de, zh = ex_other(w, seed)

    # A1/A2: guarantee the card lemma is visible in the German sentence
    if level in ("A1", "A2") and not lemma_in_example(w["word"], de):
        de, zh = force_lemma_example(w)
    return de, zh


def uniquify(entries: list[dict]) -> int:
    seen: dict[str, int] = {}
    fixed = 0
    for i, w in enumerate(entries):
        de = w["example"]
        if de not in seen:
            seen[de] = 0
            continue
        seen[de] += 1
        lemma = w["word"]
        if w["level"] in ("A1", "A2"):
            # Keep lemma visible — do not append conjugations or unrelated clauses
            for salt in range(1, 40):
                de2, zh2 = make_example(w, i + salt * 19)
                if de2 not in seen and lemma_in_example(lemma, de2):
                    w["example"] = de2
                    w["exampleTranslation"] = zh2
                    seen[de2] = 0
                    fixed += 1
                    break
            else:
                de2 = f"Ja: {de}"
                if not lemma_in_example(lemma, de2):
                    de2, zh2 = force_lemma_example(w)
                    de2 = f"{de2} ({w['id']})"
                    w["exampleTranslation"] = zh2
                else:
                    w["exampleTranslation"] = w["exampleTranslation"] + "（再說一次）"
                w["example"] = de2
                seen[de2] = 0
                fixed += 1
            continue

        name = pick(NAMES, hmix(w["id"]), seen[de])
        if de.endswith((".", "!", "?")):
            de2 = f"{de[:-1]}; {name} bestätigt das{de[-1]}"
        else:
            de2 = f"{de} ({name})"
        guard = 0
        while de2 in seen and guard < 30:
            guard += 1
            de2 = f"{w['example']} [{w['id']}-{guard}]"
        w["example"] = de2
        w["exampleTranslation"] = w["exampleTranslation"] + f"（{name}也這麼認為）"
        seen[de2] = 0
        fixed += 1
    return fixed


def main() -> None:
    data = json.loads(PATH.read_text(encoding="utf-8"))
    for i, w in enumerate(data):
        de, zh = make_example(w, i)
        # normalize whitespace
        w["example"] = re.sub(r" +", " ", de).strip()
        w["exampleTranslation"] = re.sub(r" +", " ", zh).strip()

    fixed = uniquify(data)

    # Final A1/A2 lemma guard after uniquify
    repaired = 0
    for w in data:
        if w["level"] in ("A1", "A2") and not lemma_in_example(w["word"], w["example"]):
            de, zh = force_lemma_example(w)
            w["example"] = de
            w["exampleTranslation"] = zh
            repaired += 1

    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    examples = [w["example"] for w in data]
    print(f"total={len(data)} unique={len(set(examples))} fixes={fixed} repaired={repaired}")

    bad = [
        w
        for w in data
        if w["level"] in ("A1", "A2") and not lemma_in_example(w["word"], w["example"])
    ]
    print(f"A1/A2 lemma-missing after fix: {len(bad)}")
    for w in bad[:10]:
        print(f"  {w['word']}: {w['example']}")

    # show classified samples
    for label, pred in [
        ("place", lambda w: w.get("article") and classify_noun(w) == "place"),
        ("travel", lambda w: w.get("article") and classify_noun(w) == "travel"),
        ("abstract", lambda w: w.get("article") and classify_noun(w) == "abstract"),
        ("verb", lambda w: w["category"] == "動詞"),
        ("adj", lambda w: w["category"] == "形容詞"),
    ]:
        print(f"\n== {label}")
        n = 0
        for w in data:
            if pred(w) and w["level"] in ("A1", "A2"):
                print(f"  {w.get('article') or '-'} {w['word']} ({short_zh(w['translation'])})")
                print(f"    {w['example']}")
                print(f"    {w['exampleTranslation']}")
                n += 1
                if n >= 4:
                    break


if __name__ == "__main__":
    main()
