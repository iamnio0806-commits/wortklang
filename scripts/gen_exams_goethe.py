#!/usr/bin/env python3
"""Append Goethe-Format (考場版) mock exams to exams.json.

Loads existing papers (a1-m1…b2-m2), tags them format=compact if missing,
appends 8 new Goethe Teil-structured papers, updates note, asserts counts.
Does NOT rewrite existing paper content.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "src" / "data" / "exams.json"

NOTE = (
    "德檢取向模擬測驗：含練習版（compact，綜合分節＋Bausteine）與考場版"
    "（Goethe Teil 結構，對齊 Start Deutsch／Goethe-Zertifikat 分節，無獨立語法模組）。"
    "A1–B2 各兩份練習版＋兩份考場版。聚焦 Lesen＋Hören（TTS 朗讀腳本）＋Schreiben；"
    "Sprechen 為選練口說提示，不計入及格門檻。答完後可對照中文譯文與詳解。"
    "非官方試題，僅供練習。"
)

GOETHE_IDS = [
    "a1-g1",
    "a1-g2",
    "a2-g1",
    "a2-g2",
    "b1-g1",
    "b1-g2",
    "b2-g1",
    "b2-g2",
]


def mc(
    pid: str,
    n: int,
    prompt: str,
    options: list[str],
    answer: int,
    explain_zh: str,
    prompt_zh: str | None = None,
) -> dict[str, Any]:
    item: dict[str, Any] = {
        "id": f"{pid}-{n:02d}",
        "type": "mc",
        "prompt": prompt,
        "options": options,
        "answer": answer,
        "explainZh": explain_zh,
    }
    if prompt_zh:
        item["promptZh"] = prompt_zh
    return item


def tf(
    pid: str,
    n: int,
    prompt: str,
    answer: bool | str,
    explain_zh: str,
    prompt_zh: str | None = None,
) -> dict[str, Any]:
    item: dict[str, Any] = {
        "id": f"{pid}-{n:02d}",
        "type": "tf",
        "prompt": prompt,
        "answer": answer,
        "explainZh": explain_zh,
    }
    if prompt_zh:
        item["promptZh"] = prompt_zh
    return item


def gap(
    pid: str,
    n: int,
    prompt: str,
    answer: str,
    explain_zh: str,
    accept: list[str] | None = None,
    prompt_zh: str | None = None,
) -> dict[str, Any]:
    item: dict[str, Any] = {
        "id": f"{pid}-{n:02d}",
        "type": "gap",
        "prompt": prompt,
        "answer": answer,
        "explainZh": explain_zh,
    }
    if accept:
        item["accept"] = accept
    if prompt_zh:
        item["promptZh"] = prompt_zh
    return item


def schreiben_item(
    pid: str,
    n: int,
    prompt: str,
    prompt_zh: str,
    min_words: int,
    model_answer: str,
    checklist: list[str],
) -> dict[str, Any]:
    return {
        "id": f"{pid}-{n:02d}",
        "type": "schreiben",
        "prompt": prompt,
        "promptZh": prompt_zh,
        "minWords": min_words,
        "modelAnswer": model_answer,
        "checklist": checklist,
    }


def sprechen_item(
    pid: str,
    n: int,
    prompt: str,
    prompt_zh: str,
    cues: list[str],
    model_answer: str,
) -> dict[str, Any]:
    return {
        "id": f"{pid}-{n:02d}",
        "type": "sprechen",
        "prompt": prompt,
        "promptZh": prompt_zh,
        "cues": cues,
        "modelAnswer": model_answer,
    }


def section(
    sid: str,
    kind: str,
    title: str,
    title_zh: str,
    instructions: str,
    instructions_zh: str,
    items: list[dict[str, Any]],
    *,
    audio_text: str | None = None,
    passage: str | None = None,
    passage_zh: str | None = None,
) -> dict[str, Any]:
    sec: dict[str, Any] = {
        "id": sid,
        "kind": kind,
        "title": title,
        "titleZh": title_zh,
        "instructions": instructions,
        "instructionsZh": instructions_zh,
        "items": items,
    }
    if audio_text is not None:
        sec["audioText"] = audio_text
    if passage is not None:
        sec["passage"] = passage
    if passage_zh is not None:
        sec["passageZh"] = passage_zh
    return sec


def paper(
    pid: str,
    level: str,
    round_: int,
    title: str,
    title_zh: str,
    duration: int,
    sections: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "id": pid,
        "level": level,
        "round": round_,
        "format": "goethe",
        "title": title,
        "titleZh": title_zh,
        "durationMin": duration,
        "sections": sections,
    }


def scored_count(p: dict[str, Any]) -> int:
    n = 0
    for sec in p["sections"]:
        for it in sec["items"]:
            if it["type"] in ("mc", "tf", "gap"):
                n += 1
    return n


# ═══════════════════════════════════════════════════════════════════════════
# A1 · Goethe g1 — Sprachkurs / Anmeldung
# ═══════════════════════════════════════════════════════════════════════════


def a1_g1() -> dict[str, Any]:
    pid = "a1-g1"
    lesen1 = section(
        "lesen1",
        "lesen",
        "Lesen Teil 1",
        "閱讀 Teil 1",
        "Lesen Sie die Nachrichten. Kreuzen Sie die richtige Antwort an (a, b oder c).",
        "請閱讀簡訊／郵件，選出正確答案。",
        [
            mc(
                f"{pid}-lesen1",
                1,
                "Wann beginnt der Deutschkurs von Frau Chen?",
                ["Montag, 9 Uhr", "Dienstag, 10 Uhr", "Mittwoch, 18 Uhr"],
                1,
                "郵件寫：Dienstag um 10 Uhr.",
                "陳女士的德語課何時開始？",
            ),
            mc(
                f"{pid}-lesen1",
                2,
                "Was soll Frau Chen mitbringen?",
                ["Pass und Foto", "Wörterbuch und Stift", "Geld und Schlüssel"],
                1,
                "請帶 Wörterbuch und einen Stift。",
                "陳女士要帶什麼？",
            ),
            mc(
                f"{pid}-lesen1",
                3,
                "Wo ist der Kursraum?",
                ["Raum 12, 1. Stock", "Raum 2, EG", "Raum 20, 3. Stock"],
                0,
                "Kursraum 12 im 1. Stock。",
                "教室在哪？",
            ),
            tf(
                f"{pid}-lesen1",
                4,
                "Lisa kommt um 17 Uhr zum Café.",
                False,
                "簡訊寫 treffe dich um 16 Uhr，不是 17。",
                "Lisa 五點到咖啡館。",
            ),
            tf(
                f"{pid}-lesen1",
                5,
                "Tom braucht noch Brot.",
                True,
                "請買 Brot und Milch。",
                "Tom 還需要麵包。",
            ),
        ],
        passage=(
            "E-Mail von der Sprachschule Nova an Frau Chen:\n"
            "Sehr geehrte Frau Chen,\n"
            "Ihr Deutschkurs A1 beginnt am Dienstag um 10 Uhr. "
            "Bitte bringen Sie ein Wörterbuch und einen Stift mit. "
            "Der Kursraum ist Raum 12 im 1. Stock.\n"
            "Mit freundlichen Grüßen\nSekretariat Nova\n\n"
            "SMS von Lisa an Anna:\n"
            "Hallo Anna! Ich treffe dich um 16 Uhr vor dem Café Mitte. "
            "Bring bitte dein Buch mit. Bis später!\n\n"
            "WhatsApp von Tom an Mei:\n"
            "Mei, kannst du bitte Brot und Milch kaufen? "
            "Ich komme später nach Hause. Danke!"
        ),
        passage_zh=(
            "語言學校 Nova 寫給陳女士：A1 課週二 10 點開始，請帶詞典與筆，"
            "教室在 1 樓 12 室。Lisa 約 Anna 16 點在 Café Mitte。Tom 請 Mei 買麵包與牛奶。"
        ),
    )

    lesen2 = section(
        "lesen2",
        "lesen",
        "Lesen Teil 2",
        "閱讀 Teil 2",
        "Lesen Sie die Schilder und Aushänge. Welche Aussage passt? (a, b oder c)",
        "請閱讀告示與招牌，選出正確敘述。",
        [
            mc(
                f"{pid}-lesen2",
                1,
                "Schild Bibliothek: Wann ist geschlossen?",
                ["Samstag", "Sonntag", "Montag"],
                1,
                "So geschlossen。",
                "圖書館哪天公休？",
            ),
            mc(
                f"{pid}-lesen2",
                2,
                "Was bedeutet das Schild am Aufzug?",
                ["Aufzug defekt", "Nur Personal", "Kostenpflichtig"],
                0,
                "Außer Betrieb = 故障。",
                "電梯告示是什麼意思？",
            ),
            mc(
                f"{pid}-lesen2",
                3,
                "Supermarkt: Was gilt heute?",
                ["Alles 50 %", "Obst im Angebot", "Nur Online"],
                1,
                "Heute: Äpfel und Bananen im Angebot。",
                "超市今天有什麼？",
            ),
            mc(
                f"{pid}-lesen2",
                4,
                "Parkplatz: Wie lange darf man parken?",
                ["1 Stunde", "2 Stunden", "Ganzer Tag"],
                1,
                "Max. 2 Stunden。",
                "最多可停多久？",
            ),
            mc(
                f"{pid}-lesen2",
                5,
                "Kursraum: Was ist verboten?",
                ["Wasser trinken", "Handy nutzen", "Fragen stellen"],
                1,
                "Bitte Handys ausschalten。",
                "教室禁止什麼？",
            ),
        ],
        passage=(
            "Aushang Bibliothek Stadtmitte\n"
            "Mo–Fr 9–19 Uhr, Sa 10–14 Uhr, So geschlossen.\n\n"
            "Schild Aufzug: AUSSER BETRIEB – bitte Treppe benutzen.\n\n"
            "Supermarkt Frisch: Heute Äpfel und Bananen im Angebot.\n\n"
            "Parkplatz Schule: Max. 2 Stunden. Ticket erforderlich.\n\n"
            "Tür Kursraum 12: Bitte Handys ausschalten. Quiet please."
        ),
        passage_zh=(
            "圖書館週一至五 9–19、週六 10–14、週日休；電梯故障請走樓梯；"
            "超市蘋果香蕉特價；停車場最多 2 小時；教室請關手機。"
        ),
    )

    lesen3_passage = (
        "Mein neuer Deutschkurs\n"
        "Ich heiße Lin und komme aus Taiwan. Seit drei Wochen lerne ich Deutsch "
        "an der Sprachschule Nova in München. Der Kurs ist von Dienstag bis Freitag, "
        "jeden Morgen von 10 bis 12 Uhr. In der Klasse sind zwölf Personen aus "
        "verschiedenen Ländern. Unsere Lehrerin heißt Frau Weber. Sie spricht "
        "langsam und klar. Nach dem Kurs trinke ich oft einen Kaffee mit meiner "
        "Klassenkameradin Anna. Am Wochenende mache ich Hausaufgaben und wiederhole "
        "Wörter. Nächsten Monat möchte ich den A1-Test machen."
    )
    lesen3 = section(
        "lesen3",
        "lesen",
        "Lesen Teil 3",
        "閱讀 Teil 3",
        "Lesen Sie den Text. Kreuzen Sie an: Ja – Nein – Steht nicht im Text.",
        "請閱讀短文，勾選：對、錯、或文中未提及。",
        [
            tf(f"{pid}-lesen3", 1, "Lin lernt seit drei Wochen Deutsch.", True, "開頭寫 seit drei Wochen。", "Lin 學德語三週了。"),
            tf(f"{pid}-lesen3", 2, "Der Kurs ist auch am Montag.", False, "Dienstag bis Freitag，沒有週一。", "週一也有課。"),
            tf(f"{pid}-lesen3", 3, "Frau Weber ist die Lehrerin.", True, "Unsere Lehrerin heißt Frau Weber。", "老師是 Weber 女士。"),
            tf(f"{pid}-lesen3", 4, "Lin wohnt in der Nähe der Schule.", "nicht", "文中未提住處。", "Lin 住在學校附近。"),
            tf(f"{pid}-lesen3", 5, "Lin möchte nächsten Monat den A1-Test machen.", True, "文末明確寫到。", "Lin 下個月想考 A1。"),
        ],
        passage=lesen3_passage,
        passage_zh=(
            "Lin 來自台灣，在慕尼黑 Nova 學德語三週。課從週二到週五上午 10–12 點，"
            "班上十二人。老師 Weber 女士說得慢而清楚。課後常與 Anna 喝咖啡。"
            "週末做功課複習單字，下個月想考 A1。"
        ),
    )

    hoeren1_audio = (
        "Situation 1: Guten Tag, ich möchte einen Kaffee mit Milch, bitte. "
        "Situation 2: Entschuldigung, wo ist der Bahnhof? – Geradeaus und dann links. "
        "Situation 3: Hallo Peter, treffe ich dich um drei Uhr vor dem Kino? – Ja, gut. "
        "Situation 4: Die Apotheke schließt heute schon um 18 Uhr. "
        "Situation 5: Für den Kurs brauchen Sie Raum Nummer acht im Erdgeschoss."
    )
    hoeren1 = section(
        "hoeren1",
        "hoeren",
        "Hören Teil 1",
        "聽力 Teil 1",
        "Sie hören fünf kurze Situationen. Wählen Sie a, b oder c.",
        "您會聽到五則短情境，選 a、b 或 c。",
        [
            mc(f"{pid}-hoeren1", 1, "Was bestellt die Person?", ["Tee", "Kaffee mit Milch", "Wasser"], 1, "點了 Kaffee mit Milch。", "點了什麼？"),
            mc(f"{pid}-hoeren1", 2, "Wo ist der Bahnhof?", ["rechts", "geradeaus und links", "hinter dem Café"], 1, "geradeaus und dann links。", "車站在哪？"),
            mc(f"{pid}-hoeren1", 3, "Wann treffen sie sich?", ["um 2 Uhr", "um 3 Uhr", "um 4 Uhr"], 1, "um drei Uhr。", "幾點碰面？"),
            mc(f"{pid}-hoeren1", 4, "Wann schließt die Apotheke?", ["17 Uhr", "18 Uhr", "19 Uhr"], 1, "um 18 Uhr。", "藥局幾點關？"),
            mc(f"{pid}-hoeren1", 5, "Welcher Raum?", ["Raum 8, EG", "Raum 18, 1. Stock", "Raum 80"], 0, "Raum Nummer acht im Erdgeschoss。", "哪個教室？"),
        ],
        audio_text=hoeren1_audio,
    )

    hoeren2_audio = (
        "Frau: Guten Morgen, ich möchte einen Deutschkurs A1 buchen. "
        "Mann: Gerne. Der Kurs beginnt am Dienstag. Er kostet 180 Euro für vier Wochen. "
        "Frau: Kann ich bar bezahlen? "
        "Mann: Ja, bar oder mit Karte. Bitte bringen Sie Ihren Pass mit. "
        "Frau: Und wo ist der Kursraum? "
        "Mann: Im ersten Stock, Raum zwölf. Der Unterricht ist von zehn bis zwölf Uhr. "
        "Frau: Perfekt, danke!"
    )
    hoeren2 = section(
        "hoeren2",
        "hoeren",
        "Hören Teil 2",
        "聽力 Teil 2",
        "Sie hören ein Gespräch. Wählen Sie die richtige Antwort.",
        "請聽對話，選出正確答案。",
        [
            mc(f"{pid}-hoeren2", 1, "Welchen Kurs möchte die Frau?", ["A1", "A2", "B1"], 0, "Deutschkurs A1。", "想報哪一級？"),
            mc(f"{pid}-hoeren2", 2, "Was kostet der Kurs?", ["80 €", "180 €", "280 €"], 1, "180 Euro für vier Wochen。", "學費多少？"),
            mc(f"{pid}-hoeren2", 3, "Was soll sie mitbringen?", ["Pass", "Foto", "Laptop"], 0, "Ihren Pass。", "要帶什麼？"),
            mc(f"{pid}-hoeren2", 4, "Wann ist der Unterricht?", ["8–10 Uhr", "10–12 Uhr", "14–16 Uhr"], 1, "von zehn bis zwölf Uhr。", "上課時間？"),
        ],
        audio_text=hoeren2_audio,
    )

    hoeren3_audio = (
        "Achtung, liebe Fahrgäste: Der Zug nach München hat zehn Minuten Verspätung. "
        "Er fährt um 14 Uhr 20 ab Gleis drei. Bitte haben Sie Ihren Fahrschein bereit. "
        "Im Zug gibt es ein Restaurant. Rauchen ist nicht erlaubt. "
        "Bei Fragen gehen Sie bitte zum Informationsschalter neben dem Kiosk."
    )
    hoeren3 = section(
        "hoeren3",
        "hoeren",
        "Hören Teil 3",
        "聽力 Teil 3",
        "Sie hören eine Durchsage. Wählen Sie a, b oder c.",
        "請聽廣播，選出正確答案。",
        [
            mc(f"{pid}-hoeren3", 1, "Wohin fährt der Zug?", ["Berlin", "München", "Hamburg"], 1, "Zug nach München。", "火車開往哪？"),
            mc(f"{pid}-hoeren3", 2, "Wie viel Verspätung?", ["5 Minuten", "10 Minuten", "20 Minuten"], 1, "zehn Minuten Verspätung。", "延誤多久？"),
            mc(f"{pid}-hoeren3", 3, "Von welchem Gleis?", ["Gleis 2", "Gleis 3", "Gleis 4"], 1, "ab Gleis drei。", "幾號月台？"),
            mc(f"{pid}-hoeren3", 4, "Darf man rauchen?", ["Ja", "Nein", "Nur im Restaurant"], 1, "Rauchen ist nicht erlaubt。", "可以吸菸嗎？"),
        ],
        audio_text=hoeren3_audio,
    )

    schreiben1 = section(
        "schreiben1",
        "schreiben",
        "Schreiben Teil 1",
        "寫作 Teil 1",
        "Füllen Sie das Formular aus. Schreiben Sie die fehlenden Angaben.",
        "請填寫表格中的空缺項目。",
        [
            gap(f"{pid}-schreiben1", 1, "Nachname: ___ (Chen)", "Chen", "姓氏 Chen。", prompt_zh="姓"),
            gap(f"{pid}-schreiben1", 2, "Vorname: ___ (Mei)", "Mei", "名字 Mei。", prompt_zh="名"),
            gap(f"{pid}-schreiben1", 3, "Adresse: ___ Straße 12, München", "Hauptstraße", "Hauptstraße 12。", accept=["Hauptstrasse", "Hauptstraße"], prompt_zh="街名"),
            gap(f"{pid}-schreiben1", 4, "Telefon: ___", "089123456", "範例電話。", accept=["089-123456", "089 123456"], prompt_zh="電話"),
            gap(f"{pid}-schreiben1", 5, "Kurs: ___ (A1)", "A1", "課程等級 A1。", prompt_zh="課程"),
            gap(f"{pid}-schreiben1", 6, "Beginn: Dienstag, ___ Uhr", "10", "10 Uhr。", accept=["10:00", "10 Uhr"], prompt_zh="開始時間"),
        ],
        passage=(
            "Anmeldeformular Sprachschule Nova\n"
            "Nachname: ________\nVorname: ________\n"
            "Adresse: ________ Straße 12, 80331 München\n"
            "Telefon: ________\nKursniveau: ________\n"
            "Kursbeginn: Dienstag, ________ Uhr\n"
            "(Hinweis: Chen / Mei / Haupt / 089123456 / A1 / 10)"
        ),
        passage_zh="請依提示填寫：Chen、Mei、Haupt、電話、A1、10 點。",
    )

    schreiben2 = section(
        "schreiben2",
        "schreiben",
        "Schreiben Teil 2",
        "寫作 Teil 2",
        "Schreiben Sie eine kurze Mitteilung (30–40 Wörter).",
        "請寫一則簡短訊息（約 30–40 詞）。",
        [
            schreiben_item(
                f"{pid}-schreiben2",
                1,
                "Sie können nicht zum Deutschkurs kommen. Schreiben Sie eine Nachricht an Ihre Lehrerin:\n"
                "• Entschuldigung / Grund\n• Welcher Tag?\n• Wann kommen Sie wieder?",
                "你無法去上德語課。寫訊息給老師：道歉／原因、哪一天、何時再來？",
                30,
                "Liebe Frau Weber,\nleider kann ich am Dienstag nicht zum Kurs kommen, "
                "weil ich zum Arzt muss. Am Mittwoch bin ich wieder da.\nViele Grüße\nMei Chen",
                ["有道歉與原因", "提到哪一天缺席", "說明何時回來", "約 30 字、格式完整"],
            )
        ],
    )

    sprechen1 = section(
        "sprechen1",
        "sprechen",
        "Sprechen Teil 1",
        "口說 Teil 1",
        "Stellen Sie sich vor.",
        "請自我介紹。",
        [
            sprechen_item(
                f"{pid}-sprechen1",
                1,
                "Stellen Sie sich vor: Name, Herkunft, Wohnort, Beruf/Studium, Hobby.",
                "自我介紹：名字、出身、住處、工作／學習、嗜好。",
                ["Name", "Woher?", "Wohnort", "Beruf/Studium", "Hobby"],
                "Guten Tag, ich heiße Mei Chen. Ich komme aus Taiwan und wohne in München. "
                "Ich lerne Deutsch und arbeite Teilzeit. Mein Hobby ist Lesen.",
            )
        ],
    )
    sprechen2 = section(
        "sprechen2",
        "sprechen",
        "Sprechen Teil 2",
        "口說 Teil 2",
        "Stellen Sie Fragen.",
        "請依提示提問。",
        [
            sprechen_item(
                f"{pid}-sprechen2",
                1,
                "Sie möchten Informationen über einen Deutschkurs. Stellen Sie Fragen.",
                "你想了解德語課資訊，請提問。",
                ["Wann beginnt der Kurs?", "Was kostet er?", "Wo ist der Raum?", "Muss ich ein Buch kaufen?"],
                "Wann beginnt der Kurs? Was kostet der Kurs? Wo ist der Kursraum? Brauche ich ein Buch?",
            )
        ],
    )
    sprechen3 = section(
        "sprechen3",
        "sprechen",
        "Sprechen Teil 3",
        "口說 Teil 3",
        "Bitten Sie um etwas.",
        "請提出請求。",
        [
            sprechen_item(
                f"{pid}-sprechen3",
                1,
                "Bitten Sie die Lehrerin um Hilfe: Sie verstehen eine Hausaufgabe nicht.",
                "請老師幫忙：你不懂一道作業題。",
                ["Entschuldigung", "Hausaufgabe", "Können Sie bitte … erklären?", "Danke"],
                "Entschuldigung, Frau Weber. Ich verstehe die Hausaufgabe nicht. "
                "Können Sie bitte Aufgabe zwei noch einmal erklären? Vielen Dank.",
            )
        ],
    )

    return paper(
        pid,
        "A1",
        1,
        "Goethe-Format A1 · Modellsatz 1",
        "考場版 A1 · 第1回（對齊 Goethe Start Deutsch 1 分節）",
        65,
        [
            lesen1,
            lesen2,
            lesen3,
            hoeren1,
            hoeren2,
            hoeren3,
            schreiben1,
            schreiben2,
            sprechen1,
            sprechen2,
            sprechen3,
        ],
    )


# ═══════════════════════════════════════════════════════════════════════════
# A1 · Goethe g2 — Arzt / Apotheke / Alltag
# ═══════════════════════════════════════════════════════════════════════════


def a1_g2() -> dict[str, Any]:
    pid = "a1-g2"
    lesen1 = section(
        "lesen1",
        "lesen",
        "Lesen Teil 1",
        "閱讀 Teil 1",
        "Lesen Sie die Nachrichten. Kreuzen Sie die richtige Antwort an.",
        "請閱讀簡訊／郵件，選出正確答案。",
        [
            mc(
                f"{pid}-lesen1",
                1,
                "Wann hat Herr Park den Termin?",
                ["Montag 9 Uhr", "Dienstag 11 Uhr", "Freitag 15 Uhr"],
                1,
                "Dienstag um 11 Uhr。",
                "Park 先生何時看診？",
            ),
            mc(
                f"{pid}-lesen1",
                2,
                "Was soll er mitbringen?",
                ["Versichertenkarte", "Blutprobe", "Rezept"],
                0,
                "Bitte bringen Sie Ihre Versichertenkarte mit。",
                "要帶什麼？",
            ),
            tf(f"{pid}-lesen1", 3, "Die Apotheke ist am Sonntag geöffnet.", False, "So geschlossen。", "藥局週日營業。"),
            mc(
                f"{pid}-lesen1",
                4,
                "Was möchte Sara kaufen?",
                ["Brot und Käse", "Milch und Eier", "Wasser und Tee"],
                1,
                "Milch und Eier。",
                "Sara 要買什麼？",
            ),
            tf(f"{pid}-lesen1", 5, "Jonas kommt um 19 Uhr nach Hause.", True, "Ich komme um 19 Uhr。", "Jonas 七點到家。"),
        ],
        passage=(
            "E-Mail Praxis Dr. Klein an Herrn Park:\n"
            "Sehr geehrter Herr Park,\n"
            "Ihr Termin ist am Dienstag um 11 Uhr. Bitte bringen Sie Ihre "
            "Versichertenkarte mit. Die Praxis ist in der Bahnhofstraße 4.\n"
            "Mit freundlichen Grüßen\nEmpfang Praxis Klein\n\n"
            "Aushang Apotheke Nord: Mo–Fr 8:30–18:30, Sa 9–13, So geschlossen.\n\n"
            "SMS Sara an Tim: Tim, kauf bitte Milch und Eier. Danke!\n\n"
            "WhatsApp Jonas an Lea: Lea, ich komme um 19 Uhr nach Hause. Bis dann!"
        ),
        passage_zh=(
            "診所通知週二 11 點看診並帶保險卡；藥局週日休；Sara 請 Tim 買牛奶雞蛋；"
            "Jonas 說 19 點到家。"
        ),
    )

    lesen2 = section(
        "lesen2",
        "lesen",
        "Lesen Teil 2",
        "閱讀 Teil 2",
        "Lesen Sie die Schilder. Welche Aussage ist richtig?",
        "請閱讀告示，選出正確敘述。",
        [
            mc(f"{pid}-lesen2", 1, "Wartezimmer: Was gilt?", ["Handy laut ok", "Bitte leise", "Essen erlaubt"], 1, "Bitte ruhig sein。", "候診室規定？"),
            mc(f"{pid}-lesen2", 2, "Schild Notaufnahme:", ["Nur nach Termin", "24 Stunden offen", "Nur Kinder"], 1, "24 Stunden geöffnet。", "急診告示？"),
            mc(f"{pid}-lesen2", 3, "Parken vor der Praxis:", ["Frei", "Nur für Patienten, 1 Std.", "Busspur"], 1, "Nur Patienten, max. 1 Stunde。", "停車規定？"),
            mc(f"{pid}-lesen2", 4, "Apotheke: Was ist im Angebot?", ["Vitamine", "Sonnencreme", "Pflaster"], 0, "Heute: Vitamine –20 %。", "特價商品？"),
            mc(f"{pid}-lesen2", 5, "Tür Labor:", ["Zutritt frei", "Nur Personal", "Besucher willkommen"], 1, "Nur für Personal。", "實驗室門牌？"),
        ],
        passage=(
            "Wartezimmer: Bitte ruhig sein. Handys stumm schalten.\n\n"
            "Notaufnahme: 24 Stunden geöffnet.\n\n"
            "Parkplatz Praxis: Nur für Patienten, max. 1 Stunde.\n\n"
            "Apotheke Nord: Heute Vitamine –20 %.\n\n"
            "Labor: Zutritt nur für Personal."
        ),
        passage_zh="候診室請安靜；急診 24 小時；病患停車最多 1 小時；維他命八折；實驗室僅工作人員。",
    )

    lesen3_passage = (
        "Beim Arzt\n"
        "Gestern war ich bei Dr. Klein, weil ich Halsschmerzen hatte. "
        "In der Praxis waren viele Leute. Ich wartete ungefähr zwanzig Minuten. "
        "Die Ärztin untersuchte meinen Hals und maß meine Temperatur. "
        "Ich hatte leichtes Fieber. Sie gab mir ein Rezept für Medikamente "
        "und sagte, ich soll drei Tage zu Hause bleiben. In der Apotheke "
        "nebenan kaufte ich die Tabletten. Heute geht es mir schon besser. "
        "Morgen rufe ich die Arbeit an und sage Bescheid."
    )
    lesen3 = section(
        "lesen3",
        "lesen",
        "Lesen Teil 3",
        "閱讀 Teil 3",
        "Lesen Sie den Text. Ja – Nein – Steht nicht im Text.",
        "請閱讀短文：對、錯、或未提及。",
        [
            tf(f"{pid}-lesen3", 1, "Die Person hatte Halsschmerzen.", True, "weil ich Halsschmerzen hatte。", "有喉嚨痛。"),
            tf(f"{pid}-lesen3", 2, "Sie wartete eine Stunde.", False, "約二十分鐘，不是一小時。", "等了一小時。"),
            tf(f"{pid}-lesen3", 3, "Die Ärztin gab ein Rezept.", True, "Sie gab mir ein Rezept。", "開了處方。"),
            tf(f"{pid}-lesen3", 4, "Die Apotheke ist teuer.", "nicht", "未提價格。", "藥局很貴。"),
            tf(f"{pid}-lesen3", 5, "Heute geht es der Person besser.", True, "Heute geht es mir schon besser。", "今天好多了。"),
        ],
        passage=lesen3_passage,
        passage_zh=(
            "昨天因喉嚨痛去 Klein 診所，等約二十分鐘。醫生檢查並量體溫，有輕微發燒，"
            "開藥並囑咐在家休息三天。在隔壁藥局買藥。今天好多了，明天會通知工作單位。"
        ),
    )

    hoeren1 = section(
        "hoeren1",
        "hoeren",
        "Hören Teil 1",
        "聽力 Teil 1",
        "Fünf kurze Situationen. Wählen Sie a, b oder c.",
        "五則短情境，選 a、b 或 c。",
        [
            mc(f"{pid}-hoeren1", 1, "Was fehlt der Frau?", ["Kopfschmerzen", "Halsschmerzen", "Zahnschmerzen"], 1, "Ich habe Halsschmerzen。", "哪裡不舒服？"),
            mc(f"{pid}-hoeren1", 2, "Wann ist der Termin?", ["9 Uhr", "10 Uhr", "11 Uhr"], 2, "um elf Uhr。", "預約幾點？"),
            mc(f"{pid}-hoeren1", 3, "Was soll er nehmen?", ["Tee", "Tabletten dreimal täglich", "Nur Wasser"], 1, "dreimal täglich。", "怎麼吃藥？"),
            mc(f"{pid}-hoeren1", 4, "Wo ist die Apotheke?", ["links neben dem Café", "rechts vom Bahnhof", "im Park"], 0, "links neben dem Café。", "藥局在哪？"),
            mc(f"{pid}-hoeren1", 5, "Wann schließt die Praxis?", ["16 Uhr", "17 Uhr", "18 Uhr"], 1, "um siebzehn Uhr。", "診所幾點關？"),
        ],
        audio_text=(
            "Situation 1: Guten Tag, ich habe Halsschmerzen und Fieber. "
            "Situation 2: Ihr Termin ist morgen um elf Uhr. "
            "Situation 3: Nehmen Sie die Tabletten bitte dreimal täglich nach dem Essen. "
            "Situation 4: Die Apotheke ist links neben dem Café. "
            "Situation 5: Die Praxis schließt heute um siebzehn Uhr."
        ),
    )

    hoeren2 = section(
        "hoeren2",
        "hoeren",
        "Hören Teil 2",
        "聽力 Teil 2",
        "Gespräch in der Praxis. Wählen Sie die richtige Antwort.",
        "診所對話，選出正確答案。",
        [
            mc(f"{pid}-hoeren2", 1, "Warum ist der Mann da?", ["Kontrolle", "Halsschmerzen", "Impfung"], 1, "Wegen Halsschmerzen。", "為什麼來？"),
            mc(f"{pid}-hoeren2", 2, "Seit wann hat er Beschwerden?", ["seit gestern", "seit drei Tagen", "seit einer Woche"], 1, "seit drei Tagen。", "不適多久？"),
            mc(f"{pid}-hoeren2", 3, "Was misst die Ärztin?", ["Blutdruck", "Temperatur", "Gewicht"], 1, "Ihre Temperatur。", "量了什麼？"),
            mc(f"{pid}-hoeren2", 4, "Was soll er machen?", ["Sport", "Drei Tage zu Hause bleiben", "Zur Arbeit gehen"], 1, "drei Tage zu Hause bleiben。", "該做什麼？"),
        ],
        audio_text=(
            "Ärztin: Guten Tag, Herr Park. Was fehlt Ihnen? "
            "Patient: Ich habe seit drei Tagen Halsschmerzen. "
            "Ärztin: Ich messe jetzt Ihre Temperatur. Sie haben leichtes Fieber. "
            "Ich gebe Ihnen ein Rezept. Bitte bleiben Sie drei Tage zu Hause. "
            "Patient: Gut, danke schön."
        ),
    )

    hoeren3 = section(
        "hoeren3",
        "hoeren",
        "Hören Teil 3",
        "聽力 Teil 3",
        "Durchsage in der Apotheke.",
        "藥局廣播。",
        [
            mc(f"{pid}-hoeren3", 1, "Was ist im Angebot?", ["Schmerzmittel", "Hustensaft", "Pflaster"], 1, "Hustensaft。", "特價是？"),
            mc(f"{pid}-hoeren3", 2, "Bis wann gilt das Angebot?", ["heute", "diese Woche", "diesen Monat"], 1, "diese Woche。", "優惠多久？"),
            mc(f"{pid}-hoeren3", 3, "Wo holt man Rezepte ab?", ["Kasse 1", "Schalter 2", "Lager"], 1, "am Schalter zwei。", "處方在哪取？"),
            mc(f"{pid}-hoeren3", 4, "Wann schließt die Apotheke heute?", ["18 Uhr", "19 Uhr", "20 Uhr"], 1, "um 19 Uhr。", "今天幾點關？"),
        ],
        audio_text=(
            "Liebe Kundinnen und Kunden: Diese Woche ist unser Hustensaft im Angebot. "
            "Rezepte holen Sie bitte am Schalter zwei ab. "
            "Heute schließen wir um 19 Uhr. Vielen Dank für Ihren Besuch."
        ),
    )

    schreiben1 = section(
        "schreiben1",
        "schreiben",
        "Schreiben Teil 1",
        "寫作 Teil 1",
        "Füllen Sie das Patientenformular aus.",
        "請填寫病患資料表。",
        [
            gap(f"{pid}-schreiben1", 1, "Name: ___ (Park)", "Park", "姓 Park。", prompt_zh="姓"),
            gap(f"{pid}-schreiben1", 2, "Vorname: ___ (Minho)", "Minho", "名 Minho。", prompt_zh="名"),
            gap(f"{pid}-schreiben1", 3, "Geburtsdatum: ___ (12.05.1995)", "12.05.1995", "生日。", accept=["12.5.1995", "12/05/1995"], prompt_zh="生日"),
            gap(f"{pid}-schreiben1", 4, "Adresse: ___ 4, Berlin", "Bahnhofstraße", "Bahnhofstraße。", accept=["Bahnhofstrasse"], prompt_zh="街道"),
            gap(f"{pid}-schreiben1", 5, "Beschwerden: ___", "Halsschmerzen", "主訴 Halsschmerzen。", accept=["Hals"], prompt_zh="不適"),
            gap(f"{pid}-schreiben1", 6, "Termin: Dienstag, ___ Uhr", "11", "11 Uhr。", accept=["11:00", "11 Uhr"], prompt_zh="時間"),
        ],
        passage=(
            "Patientenformular Praxis Dr. Klein\n"
            "Nachname: ________  Vorname: ________\n"
            "Geburtsdatum: ________\nAdresse: ________ 4, 10115 Berlin\n"
            "Beschwerden: ________\nTermin: Dienstag, ________ Uhr\n"
            "(Park / Minho / 12.05.1995 / Bahnhofstraße / Halsschmerzen / 11)"
        ),
    )

    schreiben2 = section(
        "schreiben2",
        "schreiben",
        "Schreiben Teil 2",
        "寫作 Teil 2",
        "Kurze Mitteilung (30–40 Wörter).",
        "簡短訊息（約 30–40 詞）。",
        [
            schreiben_item(
                f"{pid}-schreiben2",
                1,
                "Sie sind krank und können nicht zur Arbeit kommen. Schreiben Sie an Ihren Kollegen:\n"
                "• Entschuldigung\n• Grund (krank)\n• Wann Sie wiederkommen",
                "你生病無法上班，寫訊息給同事：道歉、原因、何時回來。",
                30,
                "Hallo Tim,\nleider kann ich heute nicht zur Arbeit kommen, weil ich krank bin. "
                "Ich habe Halsschmerzen. Am Donnerstag bin ich wieder da.\nViele Grüße\nMinho",
                ["有道歉", "說明生病／原因", "提到回來日", "約 30 字"],
            )
        ],
    )

    sprechen1 = section(
        "sprechen1",
        "sprechen",
        "Sprechen Teil 1",
        "口說 Teil 1",
        "Stellen Sie sich vor.",
        "自我介紹。",
        [
            sprechen_item(
                f"{pid}-sprechen1",
                1,
                "Stellen Sie sich vor: Name, Alter, Wohnort, Familie, Freizeit.",
                "介紹：名字、年齡、住處、家庭、休閒。",
                ["Name", "Alter", "Wohnort", "Familie", "Freizeit"],
                "Ich heiße Minho Park. Ich bin dreißig Jahre alt und wohne in Berlin. "
                "Ich habe eine Schwester. In der Freizeit jogge ich gerne.",
            )
        ],
    )
    sprechen2 = section(
        "sprechen2",
        "sprechen",
        "Sprechen Teil 2",
        "口說 Teil 2",
        "Fragen stellen.",
        "提問。",
        [
            sprechen_item(
                f"{pid}-sprechen2",
                1,
                "Fragen Sie in der Apotheke nach einem Medikament.",
                "在藥局詢問藥品。",
                ["Haben Sie …?", "Wie oft nehmen?", "Nebenwirkungen?", "Preis?"],
                "Guten Tag, haben Sie etwas gegen Halsschmerzen? Wie oft soll ich die Tabletten nehmen? "
                "Gibt es Nebenwirkungen? Was kostet das bitte?",
            )
        ],
    )
    sprechen3 = section(
        "sprechen3",
        "sprechen",
        "Sprechen Teil 3",
        "口說 Teil 3",
        "Eine Bitte formulieren.",
        "提出請求。",
        [
            sprechen_item(
                f"{pid}-sprechen3",
                1,
                "Bitten Sie einen Freund, für Sie Medikamente aus der Apotheke zu holen.",
                "請朋友代取藥。",
                ["Könntest du bitte …?", "Rezept", "Apotheke nebenan", "Danke"],
                "Hallo Lea, könntest du bitte mein Rezept in der Apotheke nebenan abholen? "
                "Ich fühle mich nicht gut. Vielen Dank!",
            )
        ],
    )

    return paper(
        pid,
        "A1",
        2,
        "Goethe-Format A1 · Modellsatz 2",
        "考場版 A1 · 第2回（對齊 Goethe Start Deutsch 1 分節）",
        65,
        [lesen1, lesen2, lesen3, hoeren1, hoeren2, hoeren3, schreiben1, schreiben2, sprechen1, sprechen2, sprechen3],
    )


# ═══════════════════════════════════════════════════════════════════════════
# A2 · Goethe g1 — Arbeit / Teilzeit
# ═══════════════════════════════════════════════════════════════════════════


def a2_g1() -> dict[str, Any]:
    pid = "a2-g1"
    lesen1 = section(
        "lesen1",
        "lesen",
        "Lesen Teil 1",
        "閱讀 Teil 1",
        "Lesen Sie den Medientext. Richtig oder falsch? / Multiple Choice.",
        "閱讀媒體短文，判斷對錯或選擇。",
        [
            tf(f"{pid}-lesen1", 1, "Viele Studierende suchen einen Teilzeitjob.", True, "文首提到。", "許多學生找兼職。"),
            tf(f"{pid}-lesen1", 2, "Cafés zahlen immer den höchsten Lohn.", False, "文中說 Lohn unterschiedlich。", "咖啡廳薪資一定最高。"),
            mc(f"{pid}-lesen1", 3, "Was ist wichtig laut Text?", ["nur Spaß", "Arbeitszeiten und Vertrag", "nur Tipps"], 1, "Arbeitszeiten und einen klaren Vertrag。", "文中強調什麼？"),
            tf(f"{pid}-lesen1", 4, "Man darf maximal 20 Stunden pro Woche arbeiten.", "nicht", "未給明確上限數字。", "每週最多 20 小時。"),
            mc(f"{pid}-lesen1", 5, "Wo findet man Angebote?", ["nur Zeitung", "Jobportale und Aushänge", "nur Freunde"], 1, "Jobportalen und Aushängen。", "哪裡找職缺？"),
        ],
        passage=(
            "Stadtmagazin – Tipps für Studierende\n"
            "Immer mehr Studierende suchen einen Teilzeitjob. Beliebt sind Jobs im Café, "
            "im Einzelhandel oder als Nachhilfelehrer. Die Löhne sind unterschiedlich. "
            "Wichtig sind flexible Arbeitszeiten und ein klarer Vertrag. "
            "Angebote findet man auf Jobportalen und an Aushängen an der Uni."
        ),
        passage_zh="城市雜誌：愈來愈多學生找兼職，常見於咖啡廳、零售或家教；薪資不一，重點是彈性工時與明確合約，可在求職網與校園告示找到。",
    )

    lesen2 = section(
        "lesen2",
        "lesen",
        "Lesen Teil 2",
        "閱讀 Teil 2",
        "Programm / Tafel. Welche Antwort ist richtig?",
        "節目表／佈告欄，選正確答案。",
        [
            mc(f"{pid}-lesen2", 1, "Wann ist der Bewerbungsworkshop?", ["Mo 14 Uhr", "Di 16 Uhr", "Fr 10 Uhr"], 1, "Di 16:00。", "工作坊何時？"),
            mc(f"{pid}-lesen2", 2, "Wo findet der Workshop statt?", ["Raum A2", "Hörsaal 1", "Café Uni"], 0, "Raum A2。", "地點？"),
            mc(f"{pid}-lesen2", 3, "Was kostet die Teilnahme?", ["kostenlos", "5 €", "15 €"], 0, "kostenlos。", "費用？"),
            mc(f"{pid}-lesen2", 4, "Bis wann anmelden?", ["heute", "bis Freitag", "nächsten Monat"], 1, "Anmeldung bis Freitag。", "報名截止？"),
            mc(f"{pid}-lesen2", 5, "Wer leitet den Kurs?", ["Frau Berg", "Herr Lang", "Team Personal"], 0, "Frau Berg。", "誰主持？"),
        ],
        passage=(
            "Uni-Tafel – Diese Woche\n"
            "Bewerbungsworkshop mit Frau Berg\n"
            "Di 16:00–17:30 · Raum A2 · kostenlos\n"
            "Anmeldung bis Freitag im Career Center\n"
            "Do 18:00: Sprachcafé · EG Foyer"
        ),
        passage_zh="本週求職工作坊：週二 16–17:30，A2 教室，免費，週五前報名；週四語言咖啡在一樓大廳。",
    )

    lesen3 = section(
        "lesen3",
        "lesen",
        "Lesen Teil 3",
        "閱讀 Teil 3",
        "Lesen Sie die Korrespondenz.",
        "閱讀往來信件／郵件。",
        [
            mc(f"{pid}-lesen3", 1, "Warum schreibt Frau Nguyen?", ["Kündigung", "Bewerbung Teilzeit", "Urlaub"], 1, "bewerbe mich um die Stelle。", "為何寫信？"),
            mc(f"{pid}-lesen3", 2, "Wann kann sie arbeiten?", ["nur vormittags", "abends und Wochenende", "nur Mo"], 1, "abends und am Wochenende。", "何時可上班？"),
            mc(f"{pid}-lesen3", 3, "Welche Erfahrung hat sie?", ["keine", "Café und Kasse", "nur Büro"], 1, "im Café und an der Kasse。", "有何經驗？"),
            mc(f"{pid}-lesen3", 4, "Was schickt sie mit?", ["Zeugnis und Lebenslauf", "nur Foto", "nichts"], 0, "Lebenslauf und Zeugnis。", "附件？"),
            tf(f"{pid}-lesen3", 5, "Sie möchte Vollzeit arbeiten.", False, "Stelle als Aushilfe / Teilzeit。", "想要全職。"),
        ],
        passage=(
            "Betreff: Bewerbung als Aushilfe Café Sonne\n"
            "Sehr geehrte Frau Keller,\n"
            "hiermit bewerbe ich mich um die Teilzeitstelle in Ihrem Café. "
            "Ich kann abends und am Wochenende arbeiten. Ich habe Erfahrung "
            "im Café und an der Kasse. Im Anhang sende ich Lebenslauf und Zeugnis.\n"
            "Mit freundlichen Grüßen\nLinh Nguyen"
        ),
        passage_zh="Nguyen 應徵咖啡廳兼職，可晚上與週末上班，有咖啡廳與收銀經驗，附履歷與證書。",
    )

    lesen4 = section(
        "lesen4",
        "lesen",
        "Lesen Teil 4",
        "閱讀 Teil 4",
        "Welche Anzeige passt? Wählen Sie a, b oder c.",
        "哪則廣告符合需求？選 a、b 或 c。",
        [
            mc(f"{pid}-lesen4", 1, "Sie suchen Abendjob, Deutsch nicht nötig.", ["A", "B", "C"], 0, "Anzeige A：Abend，keine Deutschkenntnisse nötig。", "找晚班、不必德語？"),
            mc(f"{pid}-lesen4", 2, "Sie möchten im Büro tippen und telefonieren.", ["A", "B", "C"], 1, "Anzeige B：Büro，Tippen，Telefon。", "想做辦公室文書？"),
            mc(f"{pid}-lesen4", 3, "Sie suchen Nachhilfe Mathematik.", ["A", "B", "C"], 2, "Anzeige C：Nachhilfe Mathe。", "找數學家教？"),
            mc(f"{pid}-lesen4", 4, "Welche Stelle ist am Wochenende?", ["A", "B", "C"], 0, "A：auch Sa/So。", "週末有班？"),
            mc(f"{pid}-lesen4", 5, "Welche Stelle braucht gute Deutschkenntnisse?", ["A", "B", "C"], 1, "B：gute Deutschkenntnisse。", "哪則需良好德語？"),
        ],
        passage=(
            "Anzeige A: Lagerhelfer/in abends und Sa/So. Keine Deutschkenntnisse nötig. 14 €/Std.\n"
            "Anzeige B: Bürohilfe Mo–Fr 9–13. Tippen, Telefon. Gute Deutschkenntnisse. 15 €/Std.\n"
            "Anzeige C: Nachhilfe Mathematik für Schüler, flexibel nachmittags. 18 €/Std."
        ),
        passage_zh="A 倉儲晚班週末、不必德語；B 上午辦公室需良好德語；C 數學家教彈性下午。",
    )

    hoeren1 = section(
        "hoeren1",
        "hoeren",
        "Hören Teil 1",
        "聽力 Teil 1",
        "Radiobeitrag / Durchsage.",
        "廣播／通知。",
        [
            mc(f"{pid}-hoeren1", 1, "Worum geht es?", ["Wohnung", "Jobmesse Uni", "Sportfest"], 1, "Jobmesse an der Uni。", "主題？"),
            mc(f"{pid}-hoeren1", 2, "Wann?", ["Montag", "Mittwoch 10–16 Uhr", "Sonntag"], 1, "Mittwoch von zehn bis sechzehn。", "何時？"),
            mc(f"{pid}-hoeren1", 3, "Was kann man mitbringen?", ["Lebenslauf", "Fahrrad", "Essen"], 0, "Lebenslauf mitbringen。", "可帶什麼？"),
            mc(f"{pid}-hoeren1", 4, "Eintritt?", ["10 €", "kostenlos", "nur Studierende 5 €"], 1, "Der Eintritt ist frei。", "門票？"),
            tf(f"{pid}-hoeren1", 5, "Man muss sich online anmelden.", True, "Bitte online anmelden。", "需線上報名。"),
        ],
        audio_text=(
            "Radio Campus: Am Mittwoch von zehn bis sechzehn Uhr findet eine Jobmesse "
            "an der Uni statt. Viele Firmen suchen Teilzeitkräfte. Bitte bringen Sie "
            "Ihren Lebenslauf mit. Der Eintritt ist frei. Melden Sie sich bitte online an."
        ),
    )

    hoeren2 = section(
        "hoeren2",
        "hoeren",
        "Hören Teil 2",
        "聽力 Teil 2",
        "Gespräch: Bewerbungsgespräch kurz.",
        "簡短面試對話。",
        [
            mc(f"{pid}-hoeren2", 1, "Für welche Stelle?", ["Koch", "Service im Café", "Fahrer"], 1, "Servicekraft im Café。", "應徵什麼？"),
            mc(f"{pid}-hoeren2", 2, "Wann kann sie starten?", ["sofort", "nächste Woche", "in einem Monat"], 1, "nächste Woche。", "何時可上班？"),
            mc(f"{pid}-hoeren2", 3, "Wie viele Stunden?", ["8", "12", "20"], 2, "zwanzig Stunden pro Woche。", "每週幾小時？"),
            mc(f"{pid}-hoeren2", 4, "Probezeit?", ["keine", "zwei Wochen", "drei Monate"], 1, "Probezeit von zwei Wochen。", "試用期？"),
            mc(f"{pid}-hoeren2", 5, "Lohn pro Stunde?", ["12 €", "14 €", "16 €"], 1, "vierzehn Euro。", "時薪？"),
        ],
        audio_text=(
            "Frau Keller: Sie bewerben sich als Servicekraft im Café Sonne. "
            "Frau Nguyen: Ja. Ich kann nächste Woche anfangen und etwa zwanzig Stunden "
            "pro Woche arbeiten. "
            "Frau Keller: Gut. Die Probezeit beträgt zwei Wochen. Der Lohn ist vierzehn Euro "
            "pro Stunde. Willkommen im Team!"
        ),
    )

    hoeren3 = section(
        "hoeren3",
        "hoeren",
        "Hören Teil 3",
        "聽力 Teil 3",
        "Kurzgespräche. Wählen Sie die passende Antwort.",
        "短對話，選適當答案。",
        [
            mc(f"{pid}-hoeren3", 1, "Was möchte der Mann ändern?", ["Schicht tauschen", "kündigen", "Urlaub streichen"], 0, "Schicht tauschen。", "想改什麼？"),
            mc(f"{pid}-hoeren3", 2, "Wann braucht die Frau frei?", ["Freitag", "Samstag", "Sonntag"], 1, "Samstag。", "哪天要請假？"),
            mc(f"{pid}-hoeren3", 3, "Warum kommt Kollege später?", ["Zug Verspätung", "Krankheit", "Termin"], 0, "Zug hat Verspätung。", "同事為何遲到？"),
            mc(f"{pid}-hoeren3", 4, "Was fehlt in der Küche?", ["Milch", "Zucker", "Brot"], 0, "Keine Milch mehr。", "廚房缺什麼？"),
        ],
        audio_text=(
            "Gespräch 1: Kannst du mit mir die Schicht tauschen? Ich muss zum Arzt. – Ja, klar. "
            "Gespräch 2: Ich brauche am Samstag frei. Geht das? – Ich schaue im Plan. "
            "Gespräch 3: Entschuldigung, der Zug hat Verspätung. Ich komme in zehn Minuten. "
            "Gespräch 4: Wir haben keine Milch mehr. Kannst du welche holen?"
        ),
    )

    hoeren4 = section(
        "hoeren4",
        "hoeren",
        "Hören Teil 4",
        "聽力 Teil 4",
        "Kurzes Interview.",
        "短訪談。",
        [
            tf(f"{pid}-hoeren4", 1, "Linh arbeitet im Café Sonne.", True, "im Café Sonne。", "在 Café Sonne 工作。"),
            mc(f"{pid}-hoeren4", 2, "Was gefällt ihr?", ["nur Tipps", "Kontakt mit Gästen", "früher Feierabend"], 1, "Kontakt mit den Gästen。", "喜歡什麼？"),
            tf(f"{pid}-hoeren4", 3, "Sie arbeitet nur montags.", False, "vier Abende pro Woche。", "只週一上班。"),
            mc(f"{pid}-hoeren4", 4, "Ziel später?", ["Vollzeit Gastronomie", "Studium beenden, Bürojob", "Auswandern"], 1, "Studium beenden und Bürojob。", "之後目標？"),
        ],
        audio_text=(
            "Reporter: Linh, Sie arbeiten im Café Sonne. Was gefällt Ihnen? "
            "Linh: Der Kontakt mit den Gästen. Ich arbeite vier Abende pro Woche. "
            "Später möchte ich mein Studium beenden und einen Bürojob finden. "
            "Reporter: Danke für das Gespräch."
        ),
    )

    schreiben1 = section(
        "schreiben1",
        "schreiben",
        "Schreiben Teil 1",
        "寫作 Teil 1",
        "SMS (20–30 Wörter).",
        "簡訊（約 20–30 詞）。",
        [
            schreiben_item(
                f"{pid}-schreiben1",
                1,
                "Schreiben Sie eine SMS an Ihre Kollegin:\n• Sie kommen 20 Minuten später\n• Grund (Bus)\n• Bitte Schicht kurz übernehmen",
                "寫簡訊給同事：晚 20 分鐘、原因（公車）、請先代班。",
                20,
                "Hallo Anna, ich komme 20 Minuten später, der Bus hat Verspätung. "
                "Kannst du bitte kurz meine Schicht übernehmen? Danke! Linh",
                ["提到遲到時間", "說明原因", "提出請求", "約 20–30 詞"],
            )
        ],
    )

    schreiben2 = section(
        "schreiben2",
        "schreiben",
        "Schreiben Teil 2",
        "寫作 Teil 2",
        "E-Mail (30–40 Wörter).",
        "電子郵件（約 30–40 詞）。",
        [
            schreiben_item(
                f"{pid}-schreiben2",
                1,
                "Schreiben Sie eine E-Mail an Frau Keller:\n"
                "• Bedanken Sie sich für die Stelle\n• Fragen Sie nach der Arbeitskleidung\n• Nennen Sie Ihren Starttag",
                "寫信給 Keller：感謝錄取、詢問制服、說明上班日。",
                30,
                "Sehr geehrte Frau Keller,\nvielen Dank für die Stelle. "
                "Brauche ich Arbeitskleidung? Ich beginne am Montag.\n"
                "Mit freundlichen Grüßen\nLinh Nguyen",
                ["有感謝", "問制服／工作服", "提到開始日", "郵件格式"],
            )
        ],
    )

    sprechen1 = section(
        "sprechen1",
        "sprechen",
        "Sprechen Teil 1",
        "口說 Teil 1",
        "Personenaustausch.",
        "交換個人資訊。",
        [
            sprechen_item(
                f"{pid}-sprechen1",
                1,
                "Tauschen Sie Informationen: Name, Job, Arbeitszeiten, Wohnort.",
                "交換：姓名、工作、工時、住處。",
                ["Name", "Job", "Arbeitszeiten", "Wohnort"],
                "Ich heiße Linh. Ich arbeite abends im Café Sonne, etwa zwanzig Stunden "
                "pro Woche. Ich wohne in der Nähe der Uni.",
            )
        ],
    )
    sprechen2 = section(
        "sprechen2",
        "sprechen",
        "Sprechen Teil 2",
        "口說 Teil 2",
        "Über sich erzählen.",
        "談論自己。",
        [
            sprechen_item(
                f"{pid}-sprechen2",
                1,
                "Erzählen Sie von Ihrem Nebenjob: Was machen Sie? Was ist positiv/negativ?",
                "談兼職：做什麼、優缺點。",
                ["Tätigkeit", "positiv", "negativ", "Lohn/Zeit"],
                "In meinem Nebenjob bediene ich Gäste. Positiv ist der Kontakt mit Menschen. "
                "Negativ sind späte Arbeitszeiten. Der Lohn ist okay.",
            )
        ],
    )
    sprechen3 = section(
        "sprechen3",
        "sprechen",
        "Sprechen Teil 3",
        "口說 Teil 3",
        "Etwas planen.",
        "共同規劃。",
        [
            sprechen_item(
                f"{pid}-sprechen3",
                1,
                "Planen Sie mit einem Partner einen Schichttausch fürs Wochenende.",
                "與夥伴規劃週末換班。",
                ["Welcher Tag?", "Wer arbeitet wann?", "Bestätigung", "Alternative"],
                "Können wir am Samstag tauschen? Du arbeitest von 10 bis 14, ich von 14 bis 18. "
                "Wenn das nicht geht, nehmen wir Sonntag. Einverstanden?",
            )
        ],
    )

    return paper(
        pid,
        "A2",
        1,
        "Goethe-Format A2 · Modellsatz 1",
        "考場版 A2 · 第1回（對齊 Goethe-Zertifikat A2 分節）",
        90,
        [lesen1, lesen2, lesen3, lesen4, hoeren1, hoeren2, hoeren3, hoeren4, schreiben1, schreiben2, sprechen1, sprechen2, sprechen3],
    )


# ═══════════════════════════════════════════════════════════════════════════
# A2 · Goethe g2 — Reisen / Urlaub
# ═══════════════════════════════════════════════════════════════════════════


def a2_g2() -> dict[str, Any]:
    pid = "a2-g2"
    lesen1 = section(
        "lesen1",
        "lesen",
        "Lesen Teil 1",
        "閱讀 Teil 1",
        "Medientext zum Thema Reisen.",
        "旅遊主題媒體短文。",
        [
            tf(f"{pid}-lesen1", 1, "Viele Menschen buchen Reisen online.", True, "buchen ihre Reisen online。", "許多人線上訂旅行。"),
            tf(f"{pid}-lesen1", 2, "Früh buchen ist oft günstiger.", True, "Wer früh bucht, spart oft Geld。", "早訂常較便宜。"),
            mc(f"{pid}-lesen1", 3, "Was soll man prüfen?", ["nur Fotos", "Stornobedingungen", "nur Wetter"], 1, "Stornobedingungen。", "要檢查什麼？"),
            tf(f"{pid}-lesen1", 4, "Alle Hotels sind barrierefrei.", "nicht", "未提無障礙。", "所有旅館無障礙。"),
            mc(f"{pid}-lesen1", 5, "Tipp für Städtereisen?", ["Auto immer", "ÖPNV-Ticket", "kein Stadtplan"], 1, "ÖPNV-Ticket。", "城市旅行建議？"),
        ],
        passage=(
            "Reiseblog kompakt\n"
            "Immer mehr Menschen buchen ihre Reisen online. Wer früh bucht, spart oft Geld. "
            "Wichtig ist, die Stornobedingungen zu prüfen. Für Städtereisen lohnt sich "
            "ein ÖPNV-Ticket. Lesen Sie Bewertungen, aber vertrauen Sie nicht nur Fotos."
        ),
        passage_zh="愈來愈多人線上訂旅行；早訂常較省；要看取消條件；城市行建議大眾運輸票；評價可參考但別只信照片。",
    )

    lesen2 = section(
        "lesen2",
        "lesen",
        "Lesen Teil 2",
        "閱讀 Teil 2",
        "Fahrplan / Programmtafel.",
        "時刻表／節目板。",
        [
            mc(f"{pid}-lesen2", 1, "Zug nach Hamburg Abfahrt?", ["8:10", "9:45", "11:00"], 1, "9:45 Gleis 4。", "去漢堡幾點開？"),
            mc(f"{pid}-lesen2", 2, "Welches Gleis?", ["2", "4", "7"], 1, "Gleis 4。", "月台？"),
            mc(f"{pid}-lesen2", 3, "Stadtrundfahrt Start?", ["10 Uhr Rathaus", "12 Uhr Bahnhof", "16 Uhr Museum"], 0, "10:00 ab Rathaus。", "觀光巴士？"),
            mc(f"{pid}-lesen2", 4, "Museum geschlossen?", ["Mo", "Di", "So"], 0, "Mo geschlossen。", "博物館公休？"),
            mc(f"{pid}-lesen2", 5, "Waschsalon Öffnung Sa?", ["8–12", "9–18", "geschlossen"], 1, "Sa 9–18。", "洗衣店週六？"),
        ],
        passage=(
            "Bahnhofstafel: Hamburg Hbf – Abfahrt 9:45 – Gleis 4 – ICE 702\n"
            "Stadtrundfahrt: täglich 10:00 ab Rathaus, Dauer 90 Min.\n"
            "Stadtmuseum: Di–So 10–18, Mo geschlossen.\n"
            "Waschsalon Reisehostel: Mo–Fr 8–20, Sa 9–18, So 10–14."
        ),
        passage_zh="漢堡 ICE 9:45 月台 4；觀光 10 點市政廳出發；博物館週一休；旅舍洗衣週六 9–18。",
    )

    lesen3 = section(
        "lesen3",
        "lesen",
        "Lesen Teil 3",
        "閱讀 Teil 3",
        "Korrespondenz Hotel.",
        "旅館往來郵件。",
        [
            mc(f"{pid}-lesen3", 1, "Was möchte Herr Sato?", ["Zimmer stornieren", "Doppelzimmer buchen", "Restaurant"], 1, "Doppelzimmer reservieren。", "想做什麼？"),
            mc(f"{pid}-lesen3", 2, "Anreise?", ["1. Juni", "5. Juni", "10. Juni"], 1, "5. Juni。", "抵達日？"),
            mc(f"{pid}-lesen3", 3, "Wie viele Nächte?", ["2", "3", "5"], 1, "drei Nächte。", "幾晚？"),
            tf(f"{pid}-lesen3", 4, "Er möchte Frühstück.", True, "mit Frühstück。", "要早餐。"),
            mc(f"{pid}-lesen3", 5, "Ankunftszeit ungefähr?", ["vormittags", "gegen 18 Uhr", "nach Mitternacht"], 1, "gegen 18 Uhr。", "大約幾點到？"),
        ],
        passage=(
            "Betreff: Zimmerreservierung\n"
            "Sehr geehrte Damen und Herren,\n"
            "ich möchte ein Doppelzimmer vom 5. bis 8. Juni (drei Nächte) mit Frühstück "
            "reservieren. Wir kommen voraussichtlich gegen 18 Uhr an.\n"
            "Mit freundlichen Grüßen\nKenji Sato"
        ),
        passage_zh="Sato 預訂 6/5–8 雙人房含早餐三晚，約 18 點抵達。",
    )

    lesen4 = section(
        "lesen4",
        "lesen",
        "Lesen Teil 4",
        "閱讀 Teil 4",
        "Welche Anzeige passt zur Person?",
        "哪則廣告適合？",
        [
            mc(f"{pid}-lesen4", 1, "Familie mit Kind, günstig, Küche.", ["A", "B", "C"], 0, "A：Familienapartment mit Küche。", "有孩家庭要廚房？"),
            mc(f"{pid}-lesen4", 2, "Business, Zentrum, WLAN.", ["A", "B", "C"], 1, "B：Businesshotel Zentrum WLAN。", "商務住市中心？"),
            mc(f"{pid}-lesen4", 3, "Natur, Wandern, Halbpension.", ["A", "B", "C"], 2, "C：Berghotel Halbpension。", "想健行半膳？"),
            mc(f"{pid}-lesen4", 4, "Welches Angebot ist am See?", ["A", "B", "C"], 0, "A：am See。", "在湖邊？"),
            mc(f"{pid}-lesen4", 5, "Welches hat Fitnessraum?", ["A", "B", "C"], 1, "B：Fitnessraum。", "有健身室？"),
        ],
        passage=(
            "A: Familienapartment am See, Küche, ab 79 €, kinderfreundlich.\n"
            "B: Businesshotel im Zentrum, WLAN, Fitnessraum, ab 119 €.\n"
            "C: Berghotel mit Halbpension, Wanderwege, ab 99 €."
        ),
        passage_zh="A 湖邊家庭公寓含廚房；B 市中心商務旅館含健身；C 山區半膳旅館適合健行。",
    )

    hoeren1 = section(
        "hoeren1",
        "hoeren",
        "Hören Teil 1",
        "聽力 Teil 1",
        "Bahnhofsdurchsage.",
        "車站廣播。",
        [
            mc(f"{pid}-hoeren1", 1, "Wohin fährt der Zug?", ["Köln", "Hamburg", "Leipzig"], 1, "nach Hamburg。", "開往？"),
            mc(f"{pid}-hoeren1", 2, "Verspätung?", ["5 Min.", "15 Min.", "30 Min."], 1, "fünfzehn Minuten。", "延誤？"),
            mc(f"{pid}-hoeren1", 3, "Gleis?", ["3", "5", "8"], 1, "Gleis fünf。", "月台？"),
            tf(f"{pid}-hoeren1", 4, "Es gibt einen Speisewagen.", True, "Speisewagen。", "有餐車。"),
            mc(f"{pid}-hoeren1", 5, "Wo Infos?", ["Gleis 1", "Schalter neben Kiosk", "Parkplatz"], 1, "Informationsschalter neben dem Kiosk。", "詢問處？"),
        ],
        audio_text=(
            "Achtung: Der Zug nach Hamburg hat fünfzehn Minuten Verspätung. "
            "Abfahrt voraussichtlich um 10 Uhr von Gleis fünf. Im Zug gibt es einen Speisewagen. "
            "Informationen erhalten Sie am Schalter neben dem Kiosk."
        ),
    )

    hoeren2 = section(
        "hoeren2",
        "hoeren",
        "Hören Teil 2",
        "聽力 Teil 2",
        "Gespräch an der Rezeption.",
        "櫃檯對話。",
        [
            mc(f"{pid}-hoeren2", 1, "Reservierung auf welchen Namen?", ["Sato", "Müller", "Lee"], 0, "Sato。", "訂房姓名？"),
            mc(f"{pid}-hoeren2", 2, "Zimmernummer?", ["12", "214", "401"], 1, "zweihundertvierzehn。", "房號？"),
            mc(f"{pid}-hoeren2", 3, "Frühstück bis?", ["9 Uhr", "10 Uhr", "11 Uhr"], 1, "bis zehn Uhr。", "早餐到幾點？"),
            mc(f"{pid}-hoeren2", 4, "WLAN-Passwort?", ["hotel2024", "gast123", "wifi"], 0, "hotel2024。", "Wi‑Fi 密碼？"),
            mc(f"{pid}-hoeren2", 5, "Wann Check-out?", ["10 Uhr", "11 Uhr", "12 Uhr"], 2, "bis zwölf Uhr。", "退房？"),
        ],
        audio_text=(
            "Rezeption: Guten Tag, Reservierung auf den Namen Sato? Ihr Zimmer ist Nummer "
            "zweihundertvierzehn. Frühstück gibt es bis zehn Uhr. Das WLAN-Passwort ist "
            "hotel2024. Check-out ist bis zwölf Uhr. Schönen Aufenthalt!"
        ),
    )

    hoeren3 = section(
        "hoeren3",
        "hoeren",
        "Hören Teil 3",
        "聽力 Teil 3",
        "Kurzgespräche unterwegs.",
        "旅途短對話。",
        [
            mc(f"{pid}-hoeren3", 1, "Wohin möchten die beiden?", ["Museum", "Strand", "Markt"], 1, "zum Strand。", "想去哪？"),
            mc(f"{pid}-hoeren3", 2, "Wie kommen sie hin?", ["Taxi", "Bus Linie 7", "zu Fuß"], 1, "Bus Linie sieben。", "怎麼去？"),
            mc(f"{pid}-hoeren3", 3, "Was ist geschlossen?", ["Café", "Souvenirshop", "Park"], 1, "Souvenirshop zu。", "什麼關了？"),
            mc(f"{pid}-hoeren3", 4, "Wann zurück im Hotel?", ["17 Uhr", "18 Uhr", "19 Uhr"], 1, "um achtzehn Uhr。", "幾點回旅館？"),
        ],
        audio_text=(
            "1: Gehen wir zum Strand? – Ja, mit dem Bus Linie sieben. "
            "2: Der Souvenirshop ist heute zu. Gehen wir später nochmal. "
            "3: Wir sollten um achtzehn Uhr zurück im Hotel sein."
        ),
    )

    hoeren4 = section(
        "hoeren4",
        "hoeren",
        "Hören Teil 4",
        "聽力 Teil 4",
        "Interview mit einer Reisenden.",
        "旅客訪談。",
        [
            tf(f"{pid}-hoeren4", 1, "Mara war drei Tage in Hamburg.", True, "drei Tage in Hamburg。", "在漢堡待三天。"),
            mc(f"{pid}-hoeren4", 2, "Was hat ihr am besten gefallen?", ["Einkaufen", "Hafenrundfahrt", "Nachtclubs"], 1, "Hafenrundfahrt。", "最喜歡？"),
            tf(f"{pid}-hoeren4", 3, "Sie fand das Wetter schlecht.", False, "Das Wetter war gut。", "覺得天氣差。"),
            mc(f"{pid}-hoeren4", 4, "Nächstes Ziel?", ["Berlin", "Wien", "Rom"], 0, "Berlin。", "下次去哪？"),
        ],
        audio_text=(
            "Interviewer: Mara, Sie waren drei Tage in Hamburg. Was hat Ihnen am besten gefallen? "
            "Mara: Die Hafenrundfahrt. Das Wetter war gut. Nächstes Mal fahre ich nach Berlin. "
            "Interviewer: Danke und gute Reise!"
        ),
    )

    schreiben1 = section(
        "schreiben1",
        "schreiben",
        "Schreiben Teil 1",
        "寫作 Teil 1",
        "SMS (20–30 Wörter).",
        "簡訊（20–30 詞）。",
        [
            schreiben_item(
                f"{pid}-schreiben1",
                1,
                "SMS an Ihren Freund:\n• Zug hat Verspätung\n• neue Ankunftszeit\n• Treffpunkt Bahnhof",
                "簡訊給朋友：火車延誤、新抵達時間、車站碰面。",
                20,
                "Hallo Kenji, mein Zug hat 15 Minuten Verspätung. Ich bin gegen 18:15 da. "
                "Treffen wir uns am Bahnhof? Bis gleich! Mara",
                ["提到延誤", "新時間", "碰面地點", "約 20–30 詞"],
            )
        ],
    )

    schreiben2 = section(
        "schreiben2",
        "schreiben",
        "Schreiben Teil 2",
        "寫作 Teil 2",
        "E-Mail an das Hotel (30–40 Wörter).",
        "寫信給旅館（30–40 詞）。",
        [
            schreiben_item(
                f"{pid}-schreiben2",
                1,
                "E-Mail:\n• Späte Anreise (nach 21 Uhr)\n• Bitte Zimmerschlüssel hinterlegen\n• Frage nach Parkplatz",
                "郵件：晚到（21 點後）、請留房卡、詢問停車。",
                30,
                "Sehr geehrte Damen und Herren,\nwir kommen voraussichtlich nach 21 Uhr an. "
                "Können Sie bitte den Zimmerschlüssel hinterlegen? Gibt es einen Parkplatz?\n"
                "Mit freundlichen Grüßen\nKenji Sato",
                ["說明晚到", "請留鑰匙／房卡", "問停車", "禮貌結尾"],
            )
        ],
    )

    sprechen1 = section(
        "sprechen1",
        "sprechen",
        "Sprechen Teil 1",
        "口說 Teil 1",
        "Personenaustausch.",
        "交換資訊。",
        [
            sprechen_item(
                f"{pid}-sprechen1",
                1,
                "Sprechen Sie über: Name, Herkunft, Wohin reisen Sie?, Wie lange?",
                "談：名字、出身、去哪旅行、多久。",
                ["Name", "Herkunft", "Reiseziel", "Dauer"],
                "Ich heiße Mara. Ich komme aus Spanien. Ich reise drei Tage nach Hamburg. "
                "Danach fahre ich weiter nach Berlin.",
            )
        ],
    )
    sprechen2 = section(
        "sprechen2",
        "sprechen",
        "Sprechen Teil 2",
        "口說 Teil 2",
        "Über sich / Reisen erzählen.",
        "談旅行經驗。",
        [
            sprechen_item(
                f"{pid}-sprechen2",
                1,
                "Erzählen Sie von Ihrer letzten Reise: Wohin? Was haben Sie gemacht?",
                "談上次旅行：去哪、做了什麼。",
                ["Ort", "Transport", "Aktivitäten", "Essen"],
                "Letztes Jahr war ich in Wien. Ich bin mit dem Zug gefahren. "
                "Ich habe Museen besucht und Schnitzel gegessen. Es war schön.",
            )
        ],
    )
    sprechen3 = section(
        "sprechen3",
        "sprechen",
        "Sprechen Teil 3",
        "口說 Teil 3",
        "Einen Tagesausflug planen.",
        "規劃一日遊。",
        [
            sprechen_item(
                f"{pid}-sprechen3",
                1,
                "Planen Sie einen Tag in der Stadt: Vormittag, Mittagessen, Nachmittag.",
                "規劃城市一日：上午、午餐、下午。",
                ["Vormittag", "Mittagessen", "Nachmittag", "Treffpunkt"],
                "Am Vormittag gehen wir ins Museum. Zum Mittagessen essen wir im Café am Markt. "
                "Am Nachmittag machen wir eine Bootstour. Treffpunkt ist um 9 Uhr am Hotel.",
            )
        ],
    )

    return paper(
        pid,
        "A2",
        2,
        "Goethe-Format A2 · Modellsatz 2",
        "考場版 A2 · 第2回（對齊 Goethe-Zertifikat A2 分節）",
        90,
        [lesen1, lesen2, lesen3, lesen4, hoeren1, hoeren2, hoeren3, hoeren4, schreiben1, schreiben2, sprechen1, sprechen2, sprechen3],
    )


def _long(s: str) -> str:
    return " ".join(s.split())

# ═══════════════════════════════════════════════════════════════════════════
# B1 · Goethe g1 — Umwelt / Nachhaltigkeit
# ═══════════════════════════════════════════════════════════════════════════


def b1_g1() -> dict[str, Any]:
    pid = "b1-g1"
    lesen1_passage = _long(
        """
        Blog: Weniger Plastik im Alltag
        Viele Menschen wollen nachhaltiger leben, scheitern aber an kleinen Gewohnheiten.
        Plastiktüten, To-go-Becher und Online-Verpackungen summieren sich schnell.
        In meinem Viertel gibt es inzwischen Unverpackt-Läden und Pfandsysteme für Becher.
        Was wirklich hilft: einen Plan für den Wocheneinkauf, Mehrwegbehälter und den Mut,
        im Café nach Porzellan zu fragen. Kritikern ist das zu mühsam. Ich finde: Wer einmal
        umstellt, spart oft Geld und Müll. Die Stadt fördert seit diesem Jahr Mehrwegbecher
        mit einem kleinen Rabatt. Ob das reicht? Mindestens schafft es Bewusstsein.
        Leserkommentare zeigen: Die meisten wünschen sich mehr öffentliche Trinkbrunnen
        und bessere Radwege – nicht nur Appelle an den Einzelnen.
        """
    )
    lesen1 = section(
        "lesen1",
        "lesen",
        "Lesen Teil 1",
        "閱讀 Teil 1",
        "Blog/Meinung. Welche Aussage passt? / Richtig-Falsch.",
        "部落格／意見文。選符合的敘述或判斷對錯。",
        [
            mc(f"{pid}-lesen1", 1, "Worum geht es im Blog hauptsächlich?", ["Rezepte", "Plastik reduzieren im Alltag", "Autokauf"], 1, "Weniger Plastik。", "主題？"),
            tf(f"{pid}-lesen1", 2, "Im Viertel gibt es Unverpackt-Läden.", True, "Unverpackt-Läden。", "社區有散裝店。"),
            mc(f"{pid}-lesen1", 3, "Was fördert die Stadt?", ["Autobahnen", "Mehrwegbecher-Rabatt", "Flugtickets"], 1, "Mehrwegbecher mit Rabatt。", "城市補助？"),
            tf(f"{pid}-lesen1", 4, "Alle Leser lehnen Trinkbrunnen ab.", False, "多數希望更多飲水機。", "讀者都反對飲水機。"),
            mc(f"{pid}-lesen1", 5, "Was wünschen sich viele Leser zusätzlich?", ["nur Apps", "Radwege und Trinkbrunnen", "mehr Plastik"], 1, "Trinkbrunnen und bessere Radwege。", "讀者還想要？"),
        ],
        passage=lesen1_passage,
        passage_zh="部落格談日常減塑：散裝店、週採計畫、環保杯；城市有環保杯折扣；讀者盼更多飲水機與單車道。",
    )

    lesen2 = section(
        "lesen2",
        "lesen",
        "Lesen Teil 2",
        "閱讀 Teil 2",
        "Anzeigen zuordnen: Welche Anzeige passt?",
        "廣告配對：哪則適合？",
        [
            mc(f"{pid}-lesen2", 1, "Sie suchen gebrauchte Möbel günstig.", ["A", "B", "C", "D"], 0, "A：Möbel Flohmarkt。", "二手家具？"),
            mc(f"{pid}-lesen2", 2, "Sie möchten Fahrrad reparieren lernen.", ["A", "B", "C", "D"], 1, "B：Reparaturcafé Fahrrad。", "學修腳踏車？"),
            mc(f"{pid}-lesen2", 3, "Sie suchen Carsharing für Wochenende.", ["A", "B", "C", "D"], 2, "C：Carsharing。", "共乘汽車？"),
            mc(f"{pid}-lesen2", 4, "Sie wollen Lebensmittel retten.", ["A", "B", "C", "D"], 3, "D：Foodsharing。", "惜食？"),
            mc(f"{pid}-lesen2", 5, "Welche Anzeige ist kostenlos?", ["A", "B", "C", "D"], 1, "B：kostenlos。", "免費？"),
        ],
        passage=(
            "A: Flohmarkt Möbel & Haushalt, Sa 9–14, Halle 2, Eintritt 2 €.\n"
            "B: Reparaturcafé Fahrrad, So 11–15, kostenlos, Werkzeug vor Ort.\n"
            "C: Carsharing Wochenende Spezial, ab 29 €/Tag, inkl. Versicherung.\n"
            "D: Foodsharing Kühlschrank, EG Nachbarschaftszentrum, täglich 17–19 Uhr."
        ),
        passage_zh="A 二手家具市集；B 免費腳踏車維修咖啡；C 週末共乘車；D 社區惜食冰箱。",
    )

    lesen3_passage = _long(
        """
        Magazin: Grünes Wohnen in der Stadt
        Immer mehr Mieterinnen und Mieter achten auf Energieverbrauch und Mülltrennung.
        Ein Pilotprojekt in Leipzig zeigt, dass Hausgemeinschaften mit gemeinsamen
        Kompostanlagen und Lastenrädern den Restmüll um bis zu dreißig Prozent senken können.
        Voraussetzung sind klare Regeln und eine Ansprechperson im Haus. Die Verwaltung
        übernimmt die Anschaffungskosten für die ersten zwei Jahre; danach zahlen die
        Haushalte einen kleinen Beitrag. Kritiker bemängeln den Aufwand. Befürworter
        betonen neben der Umweltbilanz auch den sozialen Effekt: Nachbarn sprechen wieder
        miteinander. Ob sich das Modell bundesweit lohnt, soll eine Evaluation im Herbst
        klären. Bis dahin empfiehlt die Verbraucherzentrale einfache Schritte: Heizkörper
        entlüften, Stoßlüften und Geräte mit Energielabel A nutzen.
        """
    )
    lesen3 = section(
        "lesen3",
        "lesen",
        "Lesen Teil 3",
        "閱讀 Teil 3",
        "Magazinartikel. Ja/Nein/steht nicht bzw. Multiple Choice.",
        "雜誌文章：對／錯／未提及或選擇題。",
        [
            tf(f"{pid}-lesen3", 1, "Das Projekt läuft in Leipzig.", True, "Pilotprojekt in Leipzig。", "計畫在萊比錫。"),
            tf(f"{pid}-lesen3", 2, "Restmüll kann um bis zu 30 % sinken.", True, "um bis zu dreißig Prozent。", "垃圾可降約三成。"),
            mc(f"{pid}-lesen3", 3, "Wer zahlt die ersten zwei Jahre?", ["nur Mieter", "die Verwaltung", "der Bund allein"], 1, "Die Verwaltung。", "前兩年誰出錢？"),
            tf(f"{pid}-lesen3", 4, "Die Evaluation ist bereits abgeschlossen.", False, "soll … im Herbst klären。", "評估已完成。"),
            tf(f"{pid}-lesen3", 5, "Die Verbraucherzentrale empfiehlt Stoßlüften.", True, "Stoßlüften。", "建議短時間通風。"),
            mc(f"{pid}-lesen3", 6, "Was betonen Befürworter außer Umwelt?", ["Steuern", "sozialen Effekt", "Werbung"], 1, "sozialen Effekt。", "支持者還強調？"),
        ],
        passage=lesen3_passage,
        passage_zh="萊比錫試點：社區堆肥與貨運單車可降剩餘垃圾約三成；前兩年管理方出資；秋季評估；消保建議通風與高能效電器。",
    )

    lesen4_passage = _long(
        """
        Stadtwerke Musterstadt – Schreiben an Kundinnen und Kunden
        Sehr geehrte Kundin, sehr geehrter Kunde,
        ab dem 1. März stellen wir die Abrechnung auf monatliche Online-Rechnungen um.
        Papierformulare erhalten Sie nur noch auf Wunsch. Gleichzeitig starten wir ein
        Bonusprogramm für Haushalte, die ihren Stromverbrauch im Vergleich zum Vorjahr
        um mindestens fünf Prozent senken. Die Teilnahme ist freiwillig und endet nicht
        automatisch Ihren Vertrag. Bei Fragen erreichen Sie unser Serviceteam unter
        0800 123 456 oder per E-Mail an service@stadtwerke-muster.de. Bitte aktualisieren
        Sie Ihre Kontaktdaten im Kundenportal bis zum 15. Februar.
        Mit freundlichen Grüßen
        Kundenservice Stadtwerke
        """
    )
    lesen4 = section(
        "lesen4",
        "lesen",
        "Lesen Teil 4",
        "閱讀 Teil 4",
        "Formeller Brief/Schreiben. Wählen Sie die richtige Antwort.",
        "正式來信，選正確答案。",
        [
            mc(f"{pid}-lesen4", 1, "Ab wann Online-Rechnung?", ["1. Feb", "1. März", "1. April"], 1, "ab dem 1. März。", "何時改線上帳單？"),
            mc(f"{pid}-lesen4", 2, "Papierrechnung?", ["unmöglich", "nur auf Wunsch", "immer"], 1, "nur noch auf Wunsch。", "紙本？"),
            mc(f"{pid}-lesen4", 3, "Bonus bei Einsparung von …", ["2 %", "5 %", "15 %"], 1, "mindestens fünf Prozent。", "省多少有紅利？"),
            tf(f"{pid}-lesen4", 4, "Die Teilnahme am Bonus ist Pflicht.", False, "freiwillig。", "紅利計畫強制。"),
            mc(f"{pid}-lesen4", 5, "Kontaktdaten aktualisieren bis?", ["1. März", "15. Februar", "sofort offline"], 1, "bis zum 15. Februar。", "資料更新截止？"),
        ],
        passage=lesen4_passage,
        passage_zh="市營事業自 3/1 改月結線上帳單；紙本需申請；自願省電至少 5% 有紅利；2/15 前更新聯絡資料。",
    )

    lesen5 = section(
        "lesen5",
        "lesen",
        "Lesen Teil 5",
        "閱讀 Teil 5",
        "Forum: Welche Aussage trifft zu?",
        "論壇留言，選正確敘述。",
        [
            mc(f"{pid}-lesen5", 1, "User Alex …", ["hasst Radwege", "will mehr Radwege", "verkauft Autos"], 1, "mehr sichere Radwege。", "Alex 主張？"),
            mc(f"{pid}-lesen5", 2, "User Dana …", ["lobt Trinkbrunnen", "kritisiert fehlende Mülleimer", "plant Umzug"], 1, "zu wenig Mülleimer。", "Dana 批評？"),
            mc(f"{pid}-lesen5", 3, "User Omar …", ["organisiert Tauschparty", "kündigt Job", "reist ab"], 0, "Kleidertausch。", "Omar 做什麼？"),
            tf(f"{pid}-lesen5", 4, "Alle User sind gegen Mehrwegsysteme.", False, "Alex 支持環保措施。", "所有人反對環保杯。"),
            mc(f"{pid}-lesen5", 5, "Wer erwähnt den Unverpackt-Laden?", ["Alex", "Dana", "Omar"], 2, "Omar。", "誰提散裝店？"),
        ],
        passage=(
            "Forum Stadtgrün\n"
            "Alex: Wir brauchen mehr sichere Radwege, sonst bleibt das Auto attraktiv.\n"
            "Dana: In der Fußgängerzone fehlen Mülleimer – Littering nimmt zu.\n"
            "Omar: Am Samstag Kleidertausch im Unverpackt-Laden, 15 Uhr. Kommt vorbei!"
        ),
        passage_zh="Alex 要更多單車道；Dana 嫌行人區垃圾桶不足；Omar 週六散裝店辦舊衣交換。",
    )

    hoeren1_audio = _long(
        """
        Radio Nachrichten: In mehreren Städten starten nächste Woche Zero-Waste-Wochen.
        Märkte verzichten auf Einwegplastik, Schulen organisieren Müllsammelaktionen.
        Die Umweltbehörde meldet, dass die Menge an Plastikmüll im Vorjahr leicht gesunken ist.
        Gleichzeitig steigen die Kosten für die Müllentsorgung. Experten fordern deshalb
        verbindliche Mehrwegquoten für die Gastronomie. Am Freitag spricht die Umweltministerin
        im Landtag über ein neues Förderprogramm für Repair-Cafés. Das Wetter morgen: heiter bis wolkig.
        """
    )
    hoeren1 = section(
        "hoeren1",
        "hoeren",
        "Hören Teil 1",
        "聽力 Teil 1",
        "Radionachrichten.",
        "廣播新聞。",
        [
            mc(f"{pid}-hoeren1", 1, "Was startet nächste Woche?", ["Automes", "Zero-Waste-Wochen", "Musikfestival"], 1, "Zero-Waste-Wochen。", "下週開始？"),
            tf(f"{pid}-hoeren1", 2, "Plastikmüll ist leicht gesunken.", True, "leicht gesunken。", "塑膠垃圾略降。"),
            mc(f"{pid}-hoeren1", 3, "Was fordern Experten?", ["mehr Plastik", "Mehrwegquoten Gastronomie", "keine Regeln"], 1, "verbindliche Mehrwegquoten。", "專家要求？"),
            mc(f"{pid}-hoeren1", 4, "Wann spricht die Ministerin?", ["Montag", "Freitag", "Sonntag"], 1, "Am Freitag。", "部長何時發言？"),
            mc(f"{pid}-hoeren1", 5, "Thema der Rede?", ["Sport", "Förderprogramm Repair-Cafés", "Steuern allgemein"], 1, "Repair-Cafés。", "演講主題？"),
        ],
        audio_text=hoeren1_audio,
    )

    hoeren2_audio = _long(
        """
        Frau: Hast du schon von dem Mehrwegbecher-System in der Mensa gehört?
        Mann: Ja, man zahlt zwei Euro Pfand und bekommt sie zurück.
        Frau: Super. Ich bringe trotzdem oft meine eigene Flasche mit.
        Mann: Ich fahre jetzt mit dem Lastenrad zum Wochenmarkt. Willst du mitkommen?
        Frau: Gerne, aber erst nach dem Seminar um vier. Treffpunkt am Haupteingang?
        Mann: Einverstanden. Vergiss nicht den Stoffbeutel.
        """
    )
    hoeren2 = section(
        "hoeren2",
        "hoeren",
        "Hören Teil 2",
        "聽力 Teil 2",
        "Gespräch.",
        "對話。",
        [
            mc(f"{pid}-hoeren2", 1, "Pfand für Becher?", ["1 €", "2 €", "5 €"], 1, "zwei Euro Pfand。", "押金？"),
            tf(f"{pid}-hoeren2", 2, "Die Frau nutzt oft eigene Flasche.", True, "eigene Flasche。", "女生常用自備瓶。"),
            mc(f"{pid}-hoeren2", 3, "Wohin wollen sie?", ["Kino", "Wochenmarkt", "Büro"], 1, "Wochenmarkt。", "要去哪？"),
            mc(f"{pid}-hoeren2", 4, "Treffpunkt wann/wo?", ["vor Seminar, Café", "nach Seminar 16 Uhr Haupteingang", "morgens Bahnhof"], 1, "nach dem Seminar um vier, Haupteingang。", "碰面？"),
            mc(f"{pid}-hoeren2", 5, "Was soll sie mitbringen?", ["Laptop", "Stoffbeutel", "Ticket"], 1, "Stoffbeutel。", "要帶？"),
        ],
        audio_text=hoeren2_audio,
    )

    hoeren3_audio = _long(
        """
        Interviewerin: Herr Braun, Sie leiten ein Repair-Café. Was machen Sie genau?
        Braun: Ehrenamtliche helfen, Geräte zu reparieren statt wegzuwerfen. Jeden Samstag.
        Interviewerin: Wer kommt?
        Braun: Studierende, Familien, ältere Menschen. Viele bringen Lampen oder Mixer mit.
        Interviewerin: Finanzierung?
        Braun: Spenden und eine städtische Förderung. Wir suchen noch Elektrikerinnen und Elektriker.
        Interviewerin: Danke für das Gespräch.
        """
    )
    hoeren3 = section(
        "hoeren3",
        "hoeren",
        "Hören Teil 3",
        "聽力 Teil 3",
        "Interview.",
        "訪談。",
        [
            mc(f"{pid}-hoeren3", 1, "Wann geöffnet?", ["Mo–Fr", "jeden Samstag", "nur Feiertage"], 1, "Jeden Samstag。", "何時開放？"),
            tf(f"{pid}-hoeren3", 2, "Nur Profis dürfen reparieren.", False, "Ehrenamtliche helfen。", "只有專業人士可修。"),
            mc(f"{pid}-hoeren3", 3, "Wer kommt oft?", ["nur Firmen", "gemischte Gruppen", "nur Kinder"], 1, "Studierende, Familien, ältere Menschen。", "誰來？"),
            mc(f"{pid}-hoeren3", 4, "Finanzierung?", ["nur Eintritt", "Spenden und städtische Förderung", "Aktien"], 1, "Spenden und Förderung。", "經費？"),
            mc(f"{pid}-hoeren3", 5, "Wen suchen sie?", ["Köche", "Elektriker/innen", "Piloten"], 1, "Elektrikerinnen und Elektriker。", "徵求？"),
        ],
        audio_text=hoeren3_audio,
    )

    hoeren4_audio = _long(
        """
        Podcast Monolog: Ich habe angefangen, meinen Konsum zu dokumentieren.
        Jede Woche notiere ich, was ich neu kaufe und was ich repariere oder tausche.
        Nach zwei Monaten sehe ich: Kleidung war mein größtes Problem.
        Seitdem kaufe ich nur noch, wenn ich etwas wirklich brauche, und nutze den
        Kleidertausch im Viertel. Es ist nicht perfekt, aber der Mülleimer ist leichter.
        Nächste Woche besuche ich einen Workshop zum Thema Energiesparen zu Hause.
        """
    )
    hoeren4 = section(
        "hoeren4",
        "hoeren",
        "Hören Teil 4",
        "聽力 Teil 4",
        "Monolog / Podcast.",
        "獨白／Podcast。",
        [
            mc(f"{pid}-hoeren4", 1, "Was dokumentiert die Person?", ["Sport", "Konsum", "Reisen"], 1, "Konsum。", "記錄什麼？"),
            tf(f"{pid}-hoeren4", 2, "Kleidung war das größte Problem.", True, "Kleidung war mein größtes Problem。", "衣服是最大問題。"),
            mc(f"{pid}-hoeren4", 3, "Was nutzt sie im Viertel?", ["Taxi", "Kleidertausch", "Drive-in"], 1, "Kleidertausch。", "社區用什麼？"),
            mc(f"{pid}-hoeren4", 4, "Nächste Woche?", ["Umzug", "Workshop Energiesparen", "Prüfung Latein"], 1, "Workshop Energiesparen。", "下週？"),
        ],
        audio_text=hoeren4_audio,
    )

    schreiben1 = section(
        "schreiben1",
        "schreiben",
        "Schreiben Teil 1",
        "寫作 Teil 1",
        "E-Mail: Meinung äußern (ca. 80–100 Wörter).",
        "寫信表達意見（約 80–100 詞）。",
        [
            schreiben_item(
                f"{pid}-schreiben1",
                1,
                "Schreiben Sie an die Stadtverwaltung:\n"
                "• Mehr Trinkbrunnen und Radwege fordern\n"
                "• Kurzes Argument (Gesundheit/Umwelt)\n"
                "• Konkreter Vorschlag für Ihr Viertel",
                "寫信給市府：要求更多飲水機與單車道、簡短論點、提出社區具體建議。",
                80,
                "Sehr geehrte Damen und Herren,\n"
                "ich wünsche mir mehr Trinkbrunnen und sichere Radwege in unserem Viertel. "
                "Das verbessert die Gesundheit und reduziert Autoverkehr. "
                "Konkret schlage ich zwei Brunnen am Marktplatz und einen Radstreifen in der "
                "Schulstraße vor. Bitte prüfen Sie meinen Vorschlag.\n"
                "Mit freundlichen Grüßen\nAlex Berger",
                ["有禮貌抬頭結尾", "提出要求", "有論點", "有具體建議", "約 80 詞以上"],
            )
        ],
    )

    schreiben2 = section(
        "schreiben2",
        "schreiben",
        "Schreiben Teil 2",
        "寫作 Teil 2",
        "Auf eine Nachricht antworten (ca. 80–100 Wörter).",
        "回覆訊息（約 80–100 詞）。",
        [
            schreiben_item(
                f"{pid}-schreiben2",
                1,
                "Ihre Freundin fragt, ob Sie zum Repair-Café kommen. Antworten Sie:\n"
                "• Zusagen oder Absagen mit Grund\n• Was Sie mitbringen/reparieren möchten\n• Alternativtermin vorschlagen",
                "朋友問你是否去維修咖啡。回覆：答應／拒絕與原因、要修什麼、建議替代時間。",
                80,
                "Liebe Dana,\nvielen Dank für die Einladung. Am Samstag kann ich leider nicht, "
                "weil ich arbeiten muss. Nächsten Sonntag hätte ich Zeit. Ich möchte meine "
                "Schreibtischlampe reparieren lassen und bringe Werkzeug mit, falls nötig. "
                "Schreib mir bitte, ob Sonntag passt.\nLiebe Grüße\nOmar",
                ["明確回覆可否", "說明原因", "提到要修物品", "提出替代時間", "約 80 詞"],
            )
        ],
    )

    sprechen1 = section(
        "sprechen1",
        "sprechen",
        "Sprechen Teil 1",
        "口說 Teil 1",
        "Gemeinsam planen.",
        "共同規劃。",
        [
            sprechen_item(
                f"{pid}-sprechen1",
                1,
                "Planen Sie mit dem Partner eine Zero-Waste-Woche in der Wohngemeinschaft.",
                "與夥伴規劃共居零廢棄週。",
                ["Einkauf", "Mülltrennung", "Mehrweg", "Wer macht was?"],
                "Lass uns eine Einkaufsliste ohne Plastik machen. Ich hole Stoffebeutel, "
                "du organisierst die Mülltrennung. Abends kochen wir gemeinsam mit Resten.",
            )
        ],
    )
    sprechen2 = section(
        "sprechen2",
        "sprechen",
        "Sprechen Teil 2",
        "口說 Teil 2",
        "Zum Thema sprechen.",
        "主題談話。",
        [
            sprechen_item(
                f"{pid}-sprechen2",
                1,
                "Sprechen Sie 2–3 Minuten: Wie können Städte nachhaltiger werden?",
                "談 2–3 分鐘：城市如何更永續？",
                ["Verkehr", "Energie", "Müll", "Beispiel"],
                "Städte brauchen bessere Radwege und öffentlichen Verkehr. "
                "Außerdem helfen Solaranlagen und klare Müllregeln. "
                "In meinem Viertel gibt es schon ein Repair-Café – das motiviert.",
            )
        ],
    )
    sprechen3 = section(
        "sprechen3",
        "sprechen",
        "Sprechen Teil 3",
        "口說 Teil 3",
        "Diskussion.",
        "討論。",
        [
            sprechen_item(
                f"{pid}-sprechen3",
                1,
                "Diskutieren Sie: Sollten Einwegbecher in Cafés verboten werden?",
                "討論：咖啡廳是否該禁止一次性杯子？",
                ["Pro", "Contra", "Kompromiss", "persönliche Meinung"],
                "Ein Verbot schützt die Umwelt, aber kleine Cafés brauchen Übergangszeit. "
                "Ein Pfandsystem wäre ein guter Kompromiss. Ich persönlich nutze schon Mehrweg.",
            )
        ],
    )

    return paper(
        pid,
        "B1",
        1,
        "Goethe-Format B1 · Modellsatz 1",
        "考場版 B1 · 第1回（對齊 Goethe-Zertifikat B1 分節）",
        150,
        [lesen1, lesen2, lesen3, lesen4, lesen5, hoeren1, hoeren2, hoeren3, hoeren4, schreiben1, schreiben2, sprechen1, sprechen2, sprechen3],
    )


def b1_g2() -> dict[str, Any]:
    pid = "b1-g2"
    lesen1_passage = _long(
        """
        Blog: Weiterbildung neben dem Job
        Viele Berufstätige möchten neue Fähigkeiten lernen, haben aber wenig Zeit.
        Online-Kurse helfen, doch die Abbrecherquote ist hoch. Wer Ziele schriftlich
        festhält und feste Lernzeiten einplant, bleibt eher dran. Betriebe, die
        Weiterbildung teilweise finanzieren, berichten von höherer Motivation.
        Gleichzeitig warnt die Autorin vor Kursen ohne klare Zertifikate. Vor der
        Anmeldung sollte man prüfen: Ist der Anbieter seriös? Gibt es Praxisanteile?
        Leser schreiben, dass Lerngruppen und kurze Wochenziele wirksamer seien als
        stundenlange Videos am Stück. Flexibilität ja – Struktur aber auch.
        """
    )
    lesen1 = section(
        "lesen1",
        "lesen",
        "Lesen Teil 1",
        "閱讀 Teil 1",
        "Blog/Meinung zuordnen / MC.",
        "部落格意見，選擇／配對。",
        [
            mc(f"{pid}-lesen1", 1, "Hauptthema?", ["Urlaub", "Weiterbildung neben dem Job", "Kochen"], 1, "Weiterbildung。", "主題？"),
            tf(f"{pid}-lesen1", 2, "Online-Kurse haben oft hohe Abbrecherquote.", True, "Abbrecherquote ist hoch。", "線上課程常半途而廢。"),
            mc(f"{pid}-lesen1", 3, "Was hilft laut Text?", ["keine Ziele", "feste Lernzeiten", "nur Nachtlernen"], 1, "feste Lernzeiten。", "什麼有幫助？"),
            tf(f"{pid}-lesen1", 4, "Alle Zertifikate sind gleich wertvoll.", False, "warnt vor Kursen ohne klare Zertifikate。", "所有證書一樣。"),
            mc(f"{pid}-lesen1", 5, "Was empfehlen Leser?", ["nur lange Videos", "Lerngruppen und Wochenziele", "kein Plan"], 1, "Lerngruppen und kurze Wochenziele。", "讀者建議？"),
        ],
        passage=lesen1_passage,
        passage_zh="談在職進修：線上課放棄率高；訂目標與固定學習時間較能堅持；注意證書與實作；學習小組與週目標有效。",
    )

    lesen2 = section(
        "lesen2",
        "lesen",
        "Lesen Teil 2",
        "閱讀 Teil 2",
        "Anzeigen: Welche passt?",
        "哪則廣告適合？",
        [
            mc(f"{pid}-lesen2", 1, "Abendkurs Projektmanagement, Zertifikat.", ["A", "B", "C", "D"], 0, "A。", "專案管理晚間證書班？"),
            mc(f"{pid}-lesen2", 2, "Kostenloser Sprachtandem.", ["A", "B", "C", "D"], 1, "B。", "免費語言交換？"),
            mc(f"{pid}-lesen2", 3, "Intensiv IT am Wochenende.", ["A", "B", "C", "D"], 2, "C。", "週末 IT 密集？"),
            mc(f"{pid}-lesen2", 4, "Beratung Bildungsurlaub.", ["A", "B", "C", "D"], 3, "D。", "進修假諮詢？"),
            mc(f"{pid}-lesen2", 5, "Welche Anzeige nennt Preis 290 €?", ["A", "B", "C", "D"], 0, "A：290 €。", "哪則 290 歐？"),
        ],
        passage=(
            "A: Projektmanagement Abendkurs, 8 Wochen, Zertifikat, 290 €, Start 3. März.\n"
            "B: Sprachtandem Deutsch–Spanisch, kostenlos, Di 19 Uhr Bibliothek.\n"
            "C: IT-Intensiv Sa/So, Excel & Datenbanken, 180 €, Anmeldung online.\n"
            "D: Beratung Bildungsurlaub, Do 14–17, Agentur für Arbeit, Termin nötig."
        ),
        passage_zh="A 專案管理晚課；B 免費語言交換；C 週末 IT；D 進修假諮詢。",
    )

    lesen3_passage = _long(
        """
        Magazin Beruf & Bildung
        Digitale Kompetenzen gelten längst nicht mehr als Extra, sondern als Grundausstattung.
        Eine Umfrage unter 1200 Angestellten zeigt: Wer regelmäßig kurze Schulungen besucht,
        fühlt sich sicherer im Umgang mit neuen Tools. Gleichzeitig berichten viele von
        Zeitdruck. Erfolgreiche Unternehmen planen Lernzeiten fest im Wochenplan ein und
        belohnen den Abschluss mit internen Zertifikaten. Expertinnen raten, nicht nur
        Software zu lernen, sondern auch Soft Skills wie Feedback geben. Für Quereinsteiger
        gibt es zunehmend modulare Programme, die Berufserfahrung anerkennen. Die Autorin
        schließt: Weiterbildung ist kein Sprint, sondern ein Dauerlauf – mit Pausen.
        """
    )
    lesen3 = section(
        "lesen3",
        "lesen",
        "Lesen Teil 3",
        "閱讀 Teil 3",
        "Magazinartikel.",
        "雜誌文章。",
        [
            tf(f"{pid}-lesen3", 1, "Digitale Kompetenzen gelten als Grundausstattung.", True, "Grundausstattung。", "數位能力是基本配備。"),
            mc(f"{pid}-lesen3", 2, "Umfrage: Wie viele Angestellte?", ["120", "1200", "12 000"], 1, "1200。", "調查人數？"),
            tf(f"{pid}-lesen3", 3, "Zeitdruck ist kein Thema.", False, "berichten viele von Zeitdruck。", "完全沒有時間壓力。"),
            mc(f"{pid}-lesen3", 4, "Was raten Expertinnen zusätzlich?", ["nur Software", "auch Soft Skills", "keine Schulung"], 1, "Soft Skills。", "專家還建議？"),
            tf(f"{pid}-lesen3", 5, "Es gibt Programme für Quereinsteiger.", True, "modulare Programme。", "有轉職者方案。"),
            mc(f"{pid}-lesen3", 6, "Bild vom Lernen am Ende?", ["Sprint", "Dauerlauf mit Pausen", "Stillstand"], 1, "Dauerlauf – mit Pausen。", "結尾比喻？"),
        ],
        passage=lesen3_passage,
        passage_zh="數位能力成基本配備；1200 人調查顯示短訓有助；企業應排學習時間；也要軟實力；轉職有模組課程；進修如長跑需休息。",
    )

    lesen4_passage = _long(
        """
        Volkshochschule Claratal – Informationsschreiben
        Sehr geehrte Interessentin, sehr geehrter Interessent,
        im Sommersemester erweitern wir unser Angebot um Blended-Learning-Kurse.
        Präsenztermine finden jeweils dienstags statt; Online-Einheiten folgen asynchron.
        Die Prüfungsgebühr ist in der Kursgebühr enthalten. Stornierungen sind bis
        14 Tage vor Kursbeginn kostenfrei, danach behalten wir 30 Prozent ein.
        Ermäßigungen gelten für Studierende und Erwerbslose gegen Nachweis.
        Bitte bringen Sie zum ersten Termin einen Lichtbildausweis mit.
        Freundliche Grüße
        Kursverwaltung VHS Claratal
        """
    )
    lesen4 = section(
        "lesen4",
        "lesen",
        "Lesen Teil 4",
        "閱讀 Teil 4",
        "Formelles Schreiben.",
        "正式通知信。",
        [
            mc(f"{pid}-lesen4", 1, "Präsenztermine wann?", ["Mo", "Di", "Fr"], 1, "dienstags。", "面授哪天？"),
            tf(f"{pid}-lesen4", 2, "Prüfungsgebühr extra.", False, "in der Kursgebühr enthalten。", "考試費另計。"),
            mc(f"{pid}-lesen4", 3, "Kostenfreie Storno bis?", ["7 Tage", "14 Tage", "30 Tage"], 1, "bis 14 Tage。", "免費取消？"),
            mc(f"{pid}-lesen4", 4, "Danach einbehalten?", ["10 %", "30 %", "100 %"], 1, "30 Prozent。", "之後扣多少？"),
            tf(f"{pid}-lesen4", 5, "Man braucht einen Ausweis zum ersten Termin.", True, "Lichtbildausweis。", "第一次要帶證件。"),
        ],
        passage=lesen4_passage,
        passage_zh="暑期混成課程：週二面授＋非同步線上；考費含在學費；開課前 14 天可免費取消，之後扣 30%；學生／失業可減免；首堂帶證件。",
    )

    lesen5 = section(
        "lesen5",
        "lesen",
        "Lesen Teil 5",
        "閱讀 Teil 5",
        "Forumskommentare.",
        "論壇留言。",
        [
            mc(f"{pid}-lesen5", 1, "Nora …", ["hasst Onlinekurse", "braucht feste Zeiten", "zieht um"], 1, "feste Lernzeiten。", "Nora？"),
            mc(f"{pid}-lesen5", 2, "Ben …", ["finanziert vom Chef", "kündigt", "reist"], 0, "Chef zahlt Hälfte。", "Ben？"),
            mc(f"{pid}-lesen5", 3, "Sibel …", ["warnt vor Fake-Zertifikaten", "lobt alles", "schweigt"], 0, "unseriöse Anbieter。", "Sibel？"),
            tf(f"{pid}-lesen5", 4, "Alle drei lernen Chinesisch.", "nicht", "未提中文。", "三人都學中文。"),
            mc(f"{pid}-lesen5", 5, "Wer erwähnt Lerngruppe?", ["Nora", "Ben", "Sibel"], 0, "Nora。", "誰提學習小組？"),
        ],
        passage=(
            "Forum Lernen&Job\n"
            "Nora: Bei mir helfen nur feste Lernzeiten und eine Lerngruppe.\n"
            "Ben: Mein Chef zahlt die Hälfte vom Kurs – das motiviert enorm.\n"
            "Sibel: Vorsicht vor unseriösen Anbietern ohne echtes Zertifikat!"
        ),
        passage_zh="Nora 靠固定時間與小組；Ben 老闆付一半學費；Sibel 警告無證書的不可靠機構。",
    )

    hoeren1 = section(
        "hoeren1",
        "hoeren",
        "Hören Teil 1",
        "聽力 Teil 1",
        "Radionachrichten Bildung.",
        "教育新聞。",
        [
            mc(f"{pid}-hoeren1", 1, "Thema der Nachricht?", ["Sport", "Bildungsurlaub reformiert", "Wetter"], 1, "Bildungsurlaub。", "主題？"),
            tf(f"{pid}-hoeren1", 2, "Antrag online möglich.", True, "online stellen。", "可線上申請。"),
            mc(f"{pid}-hoeren1", 3, "Frist vor Kursbeginn?", ["3 Tage", "6 Wochen", "1 Jahr"], 1, "sechs Wochen。", "期限？"),
            mc(f"{pid}-hoeren1", 4, "Wer berät?", ["Polizei", "Volkshochschulen und Agentur", "nur Banken"], 1, "VHS und Agentur。", "誰諮詢？"),
            mc(f"{pid}-hoeren1", 5, "Neue App für?", ["Kochen", "Kursvergleich", "Parken"], 1, "Kursangebote vergleichen。", "App 用途？"),
        ],
        audio_text=_long(
            """
            Nachrichten: Ab April wird der Bildungsurlaub vereinfacht. Anträge können online
            gestellt werden, spätestens sechs Wochen vor Kursbeginn. Volkshochschulen und die
            Agentur für Arbeit beraten kostenlos. Zusätzlich startet eine App, mit der man
            Kursangebote vergleichen kann. Kritik kommt von kleinen Betrieben, die Personalengpässe fürchten.
            """
        ),
    )

    hoeren2 = section(
        "hoeren2",
        "hoeren",
        "Hören Teil 2",
        "聽力 Teil 2",
        "Gespräch Kollegen.",
        "同事對話。",
        [
            mc(f"{pid}-hoeren2", 1, "Welchen Kurs will Mira?", ["Kochen", "Projektmanagement", "Yoga"], 1, "Projektmanagement。", "Mira 想上？"),
            mc(f"{pid}-hoeren2", 2, "Wann findet er statt?", ["morgens", "dienstags abends", "nur So"], 1, "dienstags abends。", "何時？"),
            tf(f"{pid}-hoeren2", 3, "Jonas will mitmachen.", True, "Ich komme mit。", "Jonas 要一起。"),
            mc(f"{pid}-hoeren2", 4, "Wer zahlt teilweise?", ["niemand", "die Firma", "die Bank"], 1, "Die Firma zahlt die Hälfte。", "誰付一半？"),
            mc(f"{pid}-hoeren2", 5, "Anmeldung bis?", ["heute", "Freitag", "nächstes Jahr"], 1, "bis Freitag。", "報名截止？"),
        ],
        audio_text=_long(
            """
            Mira: Ich möchte den Projektmanagement-Kurs dienstags abends machen.
            Jonas: Ich komme mit. Die Firma zahlt die Hälfte, wenn wir ein Zertifikat bringen.
            Mira: Super. Dann melden wir uns bis Freitag an. Bringst du den Link mit?
            Jonas: Ja, ich schicke ihn dir nach der Pause.
            """
        ),
    )

    hoeren3 = section(
        "hoeren3",
        "hoeren",
        "Hören Teil 3",
        "聽力 Teil 3",
        "Interview Trainerin.",
        "培訓師訪談。",
        [
            mc(f"{pid}-hoeren3", 1, "Name der Trainerin?", ["Frau Lang", "Frau Keller", "Frau Berg"], 0, "Frau Lang。", "姓名？"),
            tf(f"{pid}-hoeren3", 2, "Kurse sind nur online.", False, "Präsenz und online。", "只有線上。"),
            mc(f"{pid}-hoeren3", 3, "Wichtigster Tipp?", ["alles auswendig", "kleine Wochenziele", "keine Pause"], 1, "kleine Wochenziele。", "最重要建議？"),
            mc(f"{pid}-hoeren3", 4, "Dauer typischer Kurs?", ["2 Tage", "6–8 Wochen", "2 Jahre"], 1, "sechs bis acht Wochen。", "課程長度？"),
            mc(f"{pid}-hoeren3", 5, "Für wen geeignet?", ["nur Manager", "auch Quereinsteiger", "nur Schüler"], 1, "auch Quereinsteiger。", "適合誰？"),
        ],
        audio_text=_long(
            """
            Moderator: Frau Lang, Sie trainieren berufliche Weiterbildung. Online oder Präsenz?
            Lang: Beides. Viele Kurse dauern sechs bis acht Wochen. Mein Tipp: kleine Wochenziele.
            Moderator: Für wen sind die Kurse?
            Lang: Auch für Quereinsteiger mit Berufserfahrung. Praxisanteile sind entscheidend.
            Moderator: Danke.
            """
        ),
    )

    hoeren4 = section(
        "hoeren4",
        "hoeren",
        "Hören Teil 4",
        "聽力 Teil 4",
        "Monolog Lernende.",
        "學習者獨白。",
        [
            tf(f"{pid}-hoeren4", 1, "Die Person lernt seit drei Monaten Excel.", True, "seit drei Monaten。", "學 Excel 三個月。"),
            mc(f"{pid}-hoeren4", 2, "Wann lernt sie?", ["nur Sonntag", "Dienstag und Donnerstag Abend", "morgens 5 Uhr"], 1, "Dienstag und Donnerstag。", "何時學？"),
            mc(f"{pid}-hoeren4", 3, "Ziel?", ["Urlaub", "interne Bewerbung", "Auswandern"], 1, "interne Bewerbung。", "目標？"),
            mc(f"{pid}-hoeren4", 4, "Was war schwierig?", ["Zeitmanagement", "Lehrer", "Raum"], 0, "Zeitmanagement。", "困難？"),
        ],
        audio_text=_long(
            """
            Seit drei Monaten lerne ich Excel in einem Abendkurs. Ich lerne dienstags und
            donnerstags. Mein Ziel ist eine interne Bewerbung in der Buchhaltung.
            Am Anfang war das Zeitmanagement schwierig, aber die Lerngruppe hilft.
            Nächsten Monat schreibe ich die Prüfung.
            """
        ),
    )

    schreiben1 = section(
        "schreiben1",
        "schreiben",
        "Schreiben Teil 1",
        "寫作 Teil 1",
        "Meinungs-E-Mail (80–120 Wörter).",
        "意見郵件（80–120 詞）。",
        [
            schreiben_item(
                f"{pid}-schreiben1",
                1,
                "Schreiben Sie an Ihren Arbeitgeber:\n"
                "• Bitte um Kostenübernahme für einen Kurs\n• Nutzen für die Firma\n• Zeitraum und Umfang",
                "寫信給雇主：請求補助課程、對公司益處、時間與範圍。",
                80,
                "Sehr geehrte Frau Meyer,\nich bitte um anteilige Kostenübernahme für einen "
                "Projektmanagement-Kurs (acht Wochen, dienstags abends). Der Kurs hilft mir, "
                "Projekte strukturierter zu planen und entlastet das Team. Die Prüfung ist "
                "im Juni. Über eine positive Antwort würde ich mich freuen.\n"
                "Mit freundlichen Grüßen\nMira Hofmann",
                ["明確請求", "說明對公司益處", "時間／範圍", "禮貌格式", "約 80 詞以上"],
            )
        ],
    )

    schreiben2 = section(
        "schreiben2",
        "schreiben",
        "Schreiben Teil 2",
        "寫作 Teil 2",
        "Antwort auf Nachricht (80–100 Wörter).",
        "回覆訊息（80–100 詞）。",
        [
            schreiben_item(
                f"{pid}-schreiben2",
                1,
                "Ein Freund fragt nach Tipps für Online-Lernen. Antworten Sie:\n"
                "• 2–3 konkrete Tipps\n• eigene Erfahrung\n• Angebot, gemeinsam zu lernen",
                "朋友問線上學習建議。回覆：2–3 點技巧、自身經驗、提議一起學。",
                80,
                "Hallo Ben,\nmeine Tipps: feste Zeiten, kurze Wochenziele und eine Lerngruppe. "
                "Bei mir hat das die Abbrechergefahr gesenkt. Wenn du magst, lernen wir "
                "dienstags online zusammen eine Stunde. Schreib mir einfach.\nLiebe Grüße\nNora",
                ["有具體建議", "提到自身經驗", "提出一起學", "語氣自然", "約 80 詞"],
            )
        ],
    )

    sprechen1 = section(
        "sprechen1",
        "sprechen",
        "Sprechen Teil 1",
        "口說 Teil 1",
        "Gemeinsam planen.",
        "共同規劃。",
        [
            sprechen_item(
                f"{pid}-sprechen1",
                1,
                "Planen Sie eine Lerngruppe: Wann, wo, welche Themen, Regeln.",
                "規劃學習小組：時間、地點、主題、規則。",
                ["Zeit", "Ort/Online", "Themen", "Regeln"],
                "Treffen wir uns dienstags um 19 Uhr online. Thema ist Excel. "
                "Jeder bereitet eine Aufgabe vor. Handys stumm, maximal 60 Minuten.",
            )
        ],
    )
    sprechen2 = section(
        "sprechen2",
        "sprechen",
        "Sprechen Teil 2",
        "口說 Teil 2",
        "Thema: Lernen im Beruf.",
        "主題：在職學習。",
        [
            sprechen_item(
                f"{pid}-sprechen2",
                1,
                "Sprechen Sie: Welche Weiterbildung brauchen Menschen heute?",
                "談：現今需要哪些進修？",
                ["digitale Skills", "Sprachen", "Soft Skills", "Beispiel"],
                "Heute braucht man digitale Kenntnisse, Sprachen und Soft Skills. "
                "Zum Beispiel hilft Projektmanagement in vielen Berufen. Wichtig ist, "
                "regelmäßig und realistisch zu lernen.",
            )
        ],
    )
    sprechen3 = section(
        "sprechen3",
        "sprechen",
        "Sprechen Teil 3",
        "口說 Teil 3",
        "Diskussion.",
        "討論。",
        [
            sprechen_item(
                f"{pid}-sprechen3",
                1,
                "Diskutieren Sie: Sollen Firmen Weiterbildung verpflichtend machen?",
                "討論：公司是否應強制進修？",
                ["Pro", "Contra", "Freiwilligkeit", "Ihre Meinung"],
                "Verpflichtung kann Standards sichern, aber Motivation sinkt manchmal. "
                "Besser sind Anreize und freie Wahl. Ich finde eine Mischform sinnvoll.",
            )
        ],
    )

    return paper(
        pid,
        "B1",
        2,
        "Goethe-Format B1 · Modellsatz 2",
        "考場版 B1 · 第2回（對齊 Goethe-Zertifikat B1 分節）",
        150,
        [lesen1, lesen2, lesen3, lesen4, lesen5, hoeren1, hoeren2, hoeren3, hoeren4, schreiben1, schreiben2, sprechen1, sprechen2, sprechen3],
    )

# ═══════════════════════════════════════════════════════════════════════════
# B2 · Goethe g1 — Digitalisierung / Medien
# ═══════════════════════════════════════════════════════════════════════════


def b2_g1() -> dict[str, Any]:
    pid = "b2-g1"
    lesen1_passage = _long(
        """
        Kommentar: Die Aufmerksamkeit als knappe Ressource
        Digitale Plattformen konkurrieren nicht nur um Nutzerzahlen, sondern um jede
        Sekunde Aufmerksamkeit. Algorithmen belohnen Inhalte, die Emotionen auslösen –
        Empörung oft stärker als Information. Das verändert öffentliche Debatten:
        Komplexe Themen werden verkürzt, Nuancen gehen verloren. Gleichzeitig eröffnen
        dieselben Technologien Zugang zu Wissen und Teilhabe, die früher Eliten vorbehalten
        waren. Die Frage ist daher nicht Technikfeindlichkeit oder blinder Fortschrittsglaube,
        sondern Gestaltung. Regulierungen wie Kennzeichnungspflichten für Werbung und
        klarere Regeln für Empfehlungssysteme sind Schritte, reichen aber nicht, wenn
        Medienkompetenz in Schulen und Betrieben fehlt. Wer nur Verbote fordert, unterschätzt
        die Innovationsdynamik; wer nur auf Selbstregulierung setzt, ignoriert Machtasymmetrien.
        Ein realistischer Mittelweg verbindet Transparenzpflichten mit Bildungsangeboten und
        einer kritischen Öffentlichkeit, die Plattformen nicht als Schicksal, sondern als
        verhandelbare Infrastruktur begreift.
        """
    )
    lesen1 = section(
        "lesen1",
        "lesen",
        "Lesen Teil 1",
        "閱讀 Teil 1",
        "Langer Kommentar. Wählen Sie die passende Aussage.",
        "長篇評論，選出符合的敘述。",
        [
            mc(f"{pid}-lesen1", 1, "Worum konkurrieren Plattformen laut Text?", ["nur Umsatz", "Aufmerksamkeit", "Parkplätze"], 1, "Aufmerksamkeit。", "平台競爭什麼？"),
            tf(f"{pid}-lesen1", 2, "Algorithmen belohnen oft emotionale Inhalte.", True, "Emotionen auslösen。", "演算法偏好情緒內容。"),
            mc(f"{pid}-lesen1", 3, "Was fordert der Text zusätzlich zu Regeln?", ["Medienkompetenz", "Technikverbot", "kein Internet"], 0, "Medienkompetenz。", "法規之外還要？"),
            tf(f"{pid}-lesen1", 4, "Der Autor lehnt jede Regulierung ab.", False, "Regulierungen … sind Schritte。", "作者拒絕一切規範。"),
            mc(f"{pid}-lesen1", 5, "Mittelweg umfasst …", ["nur Verbote", "Transparenz + Bildung", "nur Werbung"], 1, "Transparenzpflichten mit Bildungsangeboten。", "中間路線？"),
            mc(f"{pid}-lesen1", 6, "Plattformen werden verglichen mit …", ["Schicksal vs. verhandelbare Infrastruktur", "Naturgesetz", "Spielzeug"], 0, "verhandelbare Infrastruktur。", "平台被視為？"),
        ],
        passage=lesen1_passage,
        passage_zh="評論談注意力經濟、演算法與情緒內容；需規範＋媒體素養，非純禁止或純自律；平台是可協商的基礎設施。",
    )

    lesen2 = section(
        "lesen2",
        "lesen",
        "Lesen Teil 2",
        "閱讀 Teil 2",
        "Überschriften zuordnen (als MC).",
        "標題配對（選擇題）。",
        [
            mc(f"{pid}-lesen2", 1, "Text über Deepfakes in Nachrichten:", ["A Wahrheit unter Druck", "B Sportstatistik", "C Kochrezept"], 0, "A。", "假影片新聞？"),
            mc(f"{pid}-lesen2", 2, "Text über Homeoffice-Produktivität:", ["A", "B Arbeitsort neu denken", "C"], 1, "B。", "在家工作？"),
            mc(f"{pid}-lesen2", 3, "Text über Kinder und Bildschirmzeit:", ["A", "B", "C Grenzen mit Augenmaß"], 2, "C。", "兒童螢幕時間？"),
            mc(f"{pid}-lesen2", 4, "Welcher Titel passt zu Datenschutz am Arbeitsplatz?", ["D Daten, die mitarbeiten", "A", "B"], 0, "D。", "職場個資？"),
            mc(f"{pid}-lesen2", 5, "Titel zu digitaler Teilhabe Älterer?", ["E Mit statt über Senioren", "B", "C"], 0, "E。", "高齡數位參與？"),
        ],
        passage=(
            "Mögliche Überschriften:\n"
            "A Wahrheit unter Druck\n"
            "B Arbeitsort neu denken\n"
            "C Grenzen mit Augenmaß\n"
            "D Daten, die mitarbeiten\n"
            "E Mit statt über Senioren\n\n"
            "Kurztexte: (1) Deepfakes erschweren die Nachrichtenprüfung. "
            "(2) Hybride Arbeit verändert Büroflächen. "
            "(3) Pädagogen raten zu klaren, aber flexiblen Bildschirmregeln. "
            "(4) Monitoring-Software im Job wirft Datenschutzfragen auf. "
            "(5) Kurse, die ältere Menschen aktiv einbeziehen, wirken besser als Belehrung."
        ),
        passage_zh="將短文與標題配對：假影片、混合辦公、螢幕時間、職場監控、高齡參與。",
    )

    lesen3_passage = _long(
        """
        Meinung zuordnen – Forum Digitalpolitik
        Beitrag 1 (Lea): Empfehlungssysteme sollten standardmäßig chronologisch sortieren,
        nicht nach Engagement. Sonst verstärken sich Filterblasen.
        Beitrag 2 (Marc): Ohne personalisierte Empfehlungen finden Nutzer relevante Inhalte
        nicht. Transparenz und Opt-out reichen.
        Beitrag 3 (Noor): Schulen müssen Quellenkritik üben; Regulierung allein ändert
        Nutzungsverhalten nicht.
        Beitrag 4 (Tim): Große Plattformen gehören unter strengere Kartellaufsicht, weil
        Marktmacht Debatten prägt.
        """
    )
    lesen3 = section(
        "lesen3",
        "lesen",
        "Lesen Teil 3",
        "閱讀 Teil 3",
        "Meinungen zuordnen.",
        "意見歸屬。",
        [
            mc(f"{pid}-lesen3", 1, "Wer will chronologische Feeds?", ["Lea", "Marc", "Tim"], 0, "Lea。", "誰要時間軸？"),
            mc(f"{pid}-lesen3", 2, "Wer betont Opt-out?", ["Lea", "Marc", "Noor"], 1, "Marc。", "誰提可退出？"),
            mc(f"{pid}-lesen3", 3, "Wer betont Schulen/Quellenkritik?", ["Marc", "Noor", "Tim"], 1, "Noor。", "誰強調學校？"),
            mc(f"{pid}-lesen3", 4, "Wer fordert Kartellaufsicht?", ["Lea", "Noor", "Tim"], 2, "Tim。", "誰要反壟斷監管？"),
            tf(f"{pid}-lesen3", 5, "Alle vier lehnen jede Technik ab.", False, "討論的是規範與教育。", "四人全盤否定科技。"),
            mc(f"{pid}-lesen3", 6, "Filterblasen – wer erwähnt sie?", ["Lea", "Tim", "Marc"], 0, "Lea。", "誰提過濾氣泡？"),
        ],
        passage=lesen3_passage,
        passage_zh="論壇：Lea 要時間軸；Marc 要個人化＋退出；Noor 重學校；Tim 要卡特爾監管。",
    )

    lesen4_passage = _long(
        """
        Infotext: Digitale Barrierefreiheit in Behörden
        Seit der Novelle des Behindertengleichstellungsgesetzes müssen öffentliche Stellen
        Webangebote barrierefrei gestalten. Dazu gehören ausreichende Kontraste, Alternativtexte
        für Bilder, Tastaturbedienbarkeit und verständliche Sprache in zentralen Formularen.
        Fristen zur Umsetzung wurden gestaffelt; kleinere Kommunen erhalten Beratungsbudgets.
        Nutzerinnen und Nutzer können Mängel melden; die Aufsicht kann Nachbesserungen anordnen.
        Studien zeigen: Barrierefreie Angebote helfen nicht nur Menschen mit Behinderung,
        sondern auch mobil Nutzenden und älteren Personen. Dennoch bleiben Lücken –
        besonders bei PDF-Dokumenten und eingebetteten Videos ohne Untertitel. Fachleute
        empfehlen, Barrierefreiheit von Beginn an in Ausschreibungen zu verankern, statt sie
        nachträglich teuer nachzurüsten.
        """
    )
    lesen4 = section(
        "lesen4",
        "lesen",
        "Lesen Teil 4",
        "閱讀 Teil 4",
        "Informationstext.",
        "資訊文本。",
        [
            tf(f"{pid}-lesen4", 1, "Öffentliche Stellen müssen Webangebote barrierefrei gestalten.", True, "müssen … barrierefrei。", "公部門網站須無障礙。"),
            mc(f"{pid}-lesen4", 2, "Was gehört dazu?", ["nur Farbe", "Kontraste, Alt-Texte, Tastatur", "nur Apps"], 1, "Kontraste, Alternativtexte, Tastatur。", "包含？"),
            tf(f"{pid}-lesen4", 3, "Nur Menschen mit Behinderung profitieren.", False, "auch mobil Nutzenden und älteren。", "只有身障受益。"),
            mc(f"{pid}-lesen4", 4, "Wo bleiben oft Lücken?", ["Parkplätze", "PDFs und Videos ohne Untertitel", "Kantinen"], 1, "PDF und Videos。", "常見缺口？"),
            mc(f"{pid}-lesen4", 5, "Empfehlung der Fachleute?", ["nachträglich improvisieren", "von Beginn in Ausschreibungen", "ignorieren"], 1, "von Beginn an。", "專家建議？"),
        ],
        passage=lesen4_passage,
        passage_zh="公部門網站須無障礙：對比、替代文字、鍵盤操作；通報可要求改善；行動與高齡也受益；PDF／無字幕常有缺口，應在招標即納入。",
    )

    lesen5_passage = _long(
        """
        Kommentar: KI im Redaktionsalltag
        Redaktionen experimentieren mit Sprachmodellen beim Zusammenfassen von Agenturmeldungen
        und beim Übersetzen. Gewinne an Tempo sind messbar; Risiken ebenso: Halluzinationen,
        Bias und unklare Verantwortlichkeit. Einige Häuser verlangen, dass KI-gestützte Texte
        gekennzeichnet und von Menschen gegengelesen werden. Andere fürchten den Eindruck,
        Journalismus werde „automatisiert“ und verlieren Vertrauen. Ein Branchenkodex fordert
        Transparenz gegenüber dem Publikum und Schulungen für Redakteure. Ob KI Recherche
        ersetzt, ist die falsche Frage – sie verändert Arbeitsteilung. Entscheidend bleibt,
        wer Quellen prüft und ethische Grenzziehungen trifft.
        """
    )
    lesen5 = section(
        "lesen5",
        "lesen",
        "Lesen Teil 5",
        "閱讀 Teil 5",
        "Kommentar.",
        "評論。",
        [
            mc(f"{pid}-lesen5", 1, "Wofür wird KI u. a. genutzt?", ["Druckmaschinen", "Zusammenfassen/Übersetzen", "Sportwetten"], 1, "Zusammenfassen und Übersetzen。", "AI 用途？"),
            tf(f"{pid}-lesen5", 2, "Risiken umfassen Halluzinationen und Bias.", True, "Halluzinationen, Bias。", "風險含幻覺與偏誤。"),
            mc(f"{pid}-lesen5", 3, "Was verlangen einige Häuser?", ["keine Kontrolle", "Kennzeichnung + Gegenlesen", "Geheimhaltung"], 1, "gekennzeichnet und gegengelesen。", "部分媒體要求？"),
            tf(f"{pid}-lesen5", 4, "Der Kodex fordert Transparenz.", True, "Transparenz gegenüber dem Publikum。", "準則要求透明。"),
            mc(f"{pid}-lesen5", 5, "Was bleibt entscheidend?", ["nur Tempo", "Quellen prüfen und Ethik", "Klicks maximieren"], 1, "Quellen prüft und ethische Grenzziehungen。", "關鍵是？"),
            mc(f"{pid}-lesen5", 6, "Falsche Frage laut Text?", ["Ob KI Recherche ersetzt", "Ob Transparenz nötig", "Ob Bias existiert"], 0, "Ob KI Recherche ersetzt。", "錯誤問題？"),
        ],
        passage=lesen5_passage,
        passage_zh="新聞室用 AI 摘要／翻譯；有速度也有幻覺與偏誤；部分要求標示與人工覆核；準則要透明；關鍵仍是查證與倫理。",
    )

    hoeren1 = section(
        "hoeren1",
        "hoeren",
        "Hören Teil 1",
        "聽力 Teil 1",
        "Interview Medienforscherin.",
        "媒體研究者訪談。",
        [
            mc(f"{pid}-hoeren1", 1, "Thema des Interviews?", ["Kochen", "Empfehlungsalgorithmen", "Fußball"], 1, "Empfehlungsalgorithmen。", "主題？"),
            tf(f"{pid}-hoeren1", 2, "Sie fordert absolute Abschaltung aller Feeds.", False, "Transparenz und Wahlmöglichkeiten。", "要求關閉所有動態。"),
            mc(f"{pid}-hoeren1", 3, "Was sollen Nutzer sehen können?", ["Geheimcodes", "warum Inhalte empfohlen werden", "nur Werbung"], 1, "warum … empfohlen。", "使用者應能看到？"),
            mc(f"{pid}-hoeren1", 4, "Rolle der Schulen?", ["irrelevant", "Medienkompetenz vermitteln", "Geräte verbieten total"], 1, "Medienkompetenz。", "學校角色？"),
            mc(f"{pid}-hoeren1", 5, "Zeitrahmen Studie?", ["1 Monat", "drei Jahre", "50 Jahre"], 1, "drei Jahre。", "研究多久？"),
        ],
        audio_text=_long(
            """
            Moderator: Frau Dr. Keller, Sie forschen zu Empfehlungsalgorithmen. Was fordern Sie?
            Keller: Mehr Transparenz und Wahlmöglichkeiten. Nutzerinnen sollten verstehen,
            warum Inhalte empfohlen werden. Absolute Verbote greifen zu kurz.
            Moderator: Und die Schulen?
            Keller: Sie müssen Medienkompetenz vermitteln – Quellen prüfen, Emotionen erkennen.
            Unsere Studie lief über drei Jahre in fünf Ländern. Die Ergebnisse zeigen: Bildung
            und Regulierung greifen erst zusammen.
            """
        ),
    )

    hoeren2 = section(
        "hoeren2",
        "hoeren",
        "Hören Teil 2",
        "聽力 Teil 2",
        "Diskussion Rundfunk.",
        "廣播討論。",
        [
            mc(f"{pid}-hoeren2", 1, "Position von Herrn Vogt?", ["KI ersetzen Journalisten", "KI als Assistenz mit Kontrolle", "kein Internet"], 1, "Assistenz mit Kontrolle。", "Vogt 立場？"),
            mc(f"{pid}-hoeren2", 2, "Sorge von Frau Amin?", ["zu langsam", "Verlust von Vertrauen", "zu teuer Papier"], 1, "Vertrauen。", "Amin 擔心？"),
            tf(f"{pid}-hoeren2", 3, "Beide wollen Kennzeichnung.", True, "beide für Kennzeichnung。", "兩人都要標示。"),
            mc(f"{pid}-hoeren2", 4, "Wer erwähnt Schulungen?", ["nur Publikum", "Herr Vogt", "niemand"], 1, "Vogt：Schulungen。", "誰提培訓？"),
            mc(f"{pid}-hoeren2", 5, "Einigung am Ende?", ["Komplettverbot", "Pilotprojekte mit Regeln", "Abbruch"], 1, "Pilotprojekte。", "結論？"),
        ],
        audio_text=_long(
            """
            Vogt: KI kann Assistentin sein, wenn Menschen gegenlesen und kennzeichnen.
            Wir brauchen Schulungen in der Redaktion.
            Amin: Ich fürchte den Vertrauensverlust, wenn das Publikum denkt, Texte seien automatisch.
            Beide: Kennzeichnung ist Pflicht. Vielleicht starten wir Pilotprojekte mit klaren Regeln.
            Moderator: Danke für die klare Debatte.
            """
        ),
    )

    hoeren3 = section(
        "hoeren3",
        "hoeren",
        "Hören Teil 3",
        "聽力 Teil 3",
        "Vortrag Ausschnitt.",
        "演講節錄。",
        [
            mc(f"{pid}-hoeren3", 1, "Kernthese?", ["Apps sind Spielzeug", "digitale Infrastruktur ist politisch gestaltbar", "Technik ist Schicksal"], 1, "politisch gestaltbar。", "核心論點？"),
            tf(f"{pid}-hoeren3", 2, "Beispiel Barrierefreiheit wird genannt.", True, "Barrierefreiheit。", "提到無障礙。"),
            mc(f"{pid}-hoeren3", 3, "Was kritisiert der Vortrag?", ["nur Gerätepreise", "nachträgliche Flickschusterei", "zu viele Bücher"], 1, "nachträgliche Flickschusterei。", "批評什麼？"),
            mc(f"{pid}-hoeren3", 4, "Appell an wen?", ["nur Start-ups", "Politik, Verwaltung, Zivilgesellschaft", "nur Kinder"], 1, "Politik, Verwaltung, Zivilgesellschaft。", "呼籲對象？"),
            mc(f"{pid}-hoeren3", 5, "Metapher am Ende?", ["Wetter", "Architektur öffentlicher Räume", "Kochkunst"], 1, "Architektur öffentlicher Räume。", "結尾比喻？"),
        ],
        audio_text=_long(
            """
            Meine Damen und Herren: Digitale Infrastruktur ist politisch gestaltbar – kein Schicksal.
            Denken Sie an Barrierefreiheit: Wer sie nachträglich flickt, zahlt mehr und schließt Menschen aus.
            Deshalb appelliere ich an Politik, Verwaltung und Zivilgesellschaft, Standards früh zu setzen.
            Plattformen sind wie Architektur öffentlicher Räume: Zugänge, Sichtachsen, Regeln.
            Gestalten wir sie bewusst.
            """
        ),
    )

    hoeren4 = section(
        "hoeren4",
        "hoeren",
        "Hören Teil 4",
        "聽力 Teil 4",
        "Kurzbeiträge.",
        "短篇報導。",
        [
            mc(f"{pid}-hoeren4", 1, "Beitrag 1 Thema?", ["Fahrradhelm", "Deepfake-Warn-App", "Wein"], 1, "Deepfake-Warn-App。", "第 1 則？"),
            mc(f"{pid}-hoeren4", 2, "Beitrag 2: Was öffnet Stadtbibliothek?", ["Café", "Medialab für Jugendliche", "Parkhaus"], 1, "Medialab。", "第 2 則？"),
            tf(f"{pid}-hoeren4", 3, "Beitrag 3: Homeoffice-Studie zeigt nur Nachteile.", False, "gemischte Bilanz。", "在家工作只有缺點。"),
            mc(f"{pid}-hoeren4", 4, "Beitrag 4 Forderung?", ["Gratis-Smartphones für alle", "Kennzeichnung politischer Werbung", "Verbot von Radios"], 1, "Kennzeichnung politischer Werbung。", "第 4 則？"),
            mc(f"{pid}-hoeren4", 5, "Wann startet das Medialab?", ["sofort", "im Mai", "in zehn Jahren"], 1, "im Mai。", "媒體實驗室何時？"),
        ],
        audio_text=_long(
            """
            Beitrag 1: Eine Uni testet eine App, die Deepfakes in Social-Media-Clips markiert.
            Beitrag 2: Die Stadtbibliothek öffnet im Mai ein Medialab für Jugendliche.
            Beitrag 3: Eine Homeoffice-Studie zieht eine gemischte Bilanz – Produktivität steigt,
            Isolation nimmt bei manchen zu.
            Beitrag 4: Verbraucherschützer fordern klarere Kennzeichnung politischer Online-Werbung.
            """
        ),
    )

    schreiben1 = section(
        "schreiben1",
        "schreiben",
        "Schreiben Teil 1",
        "寫作 Teil 1",
        "Forumskommentar (ca. 100 Wörter).",
        "論壇留言（約 100 詞）。",
        [
            schreiben_item(
                f"{pid}-schreiben1",
                1,
                "Schreiben Sie einen Forumskommentar zum Thema „Empfehlungsalgorithmen“:\n"
                "• Ihre Position\n• ein Argument mit Beispiel\n• ein konstruktiver Vorschlag",
                "寫論壇評論：表明立場、舉例論證、提出建設性建議。",
                100,
                "Ich finde, Empfehlungsalgorithmen brauchen mehr Transparenz. "
                "Wenn Feeds nur Empörung belohnen, verlieren Debatten an Qualität – "
                "man sieht das an polarisierenden Kurzvideos. Ein Opt-out zu chronologischen "
                "Timelines und Kennzeichnung von Werbung wären konkrete Schritte. "
                "Zusätzlich sollten Schulen Quellenkritik üben. Technik ist gestaltbar, kein Schicksal.",
                ["明確立場", "有論點與例子", "有具體建議", "約 100 詞", "論壇語氣得體"],
            )
        ],
    )

    schreiben2 = section(
        "schreiben2",
        "schreiben",
        "Schreiben Teil 2",
        "寫作 Teil 2",
        "Formelle Stellungnahme / E-Mail (ca. 150 Wörter).",
        "正式意見書／郵件（約 150 詞）。",
        [
            schreiben_item(
                f"{pid}-schreiben2",
                1,
                "Schreiben Sie an eine Redaktion:\n"
                "• Forderung: KI-Texte kennzeichnen\n• Begründung (Vertrauen, Verantwortung)\n"
                "• Vorschlag für redaktionelle Leitlinien",
                "寫信給編輯部：要求標示 AI 文本、論證信任與責任、建議編輯準則。",
                150,
                "Sehr geehrte Redaktion,\n"
                "bitte kennzeichnen Sie KI-gestützte Texte klar. Leserinnen und Leser müssen "
                "einschätzen können, wer verantwortlich ist; sonst leidet das Vertrauen. "
                "Halluzinationen und Bias sind reale Risiken. Ich schlage Leitlinien vor: "
                "Pflicht zum menschlichen Gegenlesen, transparente Hinweise im Artikel und "
                "regelmäßige Schulungen. Gerne unterstütze ich eine öffentliche Debatte dazu.\n"
                "Mit freundlichen Grüßen\nLea Hartmann",
                ["正式抬頭結尾", "明確要求", "論證信任／責任", "提出準則要點", "約 150 詞"],
            )
        ],
    )

    sprechen1 = section(
        "sprechen1",
        "sprechen",
        "Sprechen Teil 1",
        "口說 Teil 1",
        "Partnerplanung.",
        "雙人規劃。",
        [
            sprechen_item(
                f"{pid}-sprechen1",
                1,
                "Planen Sie einen Workshop „Medienkompetenz“ für Studierende: Ziele, Format, Materialien.",
                "規劃大學生媒體素養工作坊：目標、形式、材料。",
                ["Ziele", "Ablauf", "Materialien", "Rollen"],
                "Ziel ist Quellenkritik. Format: 90 Minuten Input plus Gruppenarbeit. "
                "Materialien: Beispiel-Posts und Checklisten. Du moderierst, ich bereite Fälle vor.",
            )
        ],
    )
    sprechen2 = section(
        "sprechen2",
        "sprechen",
        "Sprechen Teil 2",
        "口說 Teil 2",
        "Kurzvortrag.",
        "短講。",
        [
            sprechen_item(
                f"{pid}-sprechen2",
                1,
                "Halten Sie einen Kurzvortrag: Chancen und Risiken von KI im Journalismus.",
                "短講：新聞業中 AI 的機會與風險。",
                ["Chancen", "Risiken", "Beispiel", "Fazit"],
                "KI beschleunigt Zusammenfassungen, birgt aber Halluzinationen und Vertrauensprobleme. "
                "Beispiel: ungeprüfte Agenturtexte. Fazit: Assistenz ja, Verantwortung bleibt menschlich.",
            )
        ],
    )

    return paper(
        pid,
        "B2",
        1,
        "Goethe-Format B2 · Modellsatz 1",
        "考場版 B2 · 第1回（對齊 Goethe-Zertifikat B2 分節）",
        170,
        [lesen1, lesen2, lesen3, lesen4, lesen5, hoeren1, hoeren2, hoeren3, hoeren4, schreiben1, schreiben2, sprechen1, sprechen2],
    )


def b2_g2() -> dict[str, Any]:
    pid = "b2-g2"
    lesen1_passage = _long(
        """
        Kommentar: Wohnraum als soziale Frage
        Steigende Mieten und knapper Wohnraum prägen Großstädte. Neubau allein löst das Problem
        nicht, wenn Flächen spekulativ brachliegen und Sozialwohnungen aus der Bindung fallen.
        Kommunen experimentieren mit Mietobergrenzen, Konzeptvergaben und Genossenschaften.
        Gegner warnen vor Investitionszurückhaltung; Befürworter verweisen auf Verdrängung
        einkommensschwacher Haushalte. Zwischen Marktglauben und staatlicher Steuerung braucht
        es instrumentelle Vielfalt: aktivierende Bodenpolitik, transparente Fördertöpfe und
        Schutz vor Eigenbedarfskündigungen, die nur vorgeschoben sind. Gleichzeitig müssen
        Verfahren schneller werden – ohne Qualitäts- und Klimastandards zu opfern. Wer Wohnen
        nur als Kapitalanlage denkt, verkennt seine Rolle als Voraussetzung für Teilhabe.
        Eine Stadt, die Pflegekräfte und Lehrkräfte nicht halten kann, verliert ihre Funktionsfähigkeit.
        """
    )
    lesen1 = section(
        "lesen1",
        "lesen",
        "Lesen Teil 1",
        "閱讀 Teil 1",
        "Langer Kommentar.",
        "長篇評論。",
        [
            mc(f"{pid}-lesen1", 1, "Kernthema?", ["Tourismus", "Wohnraum/Mieten", "Mode"], 1, "Wohnraum。", "主題？"),
            tf(f"{pid}-lesen1", 2, "Neubau allein reicht laut Text nicht.", True, "Neubau allein löst … nicht。", "僅靠新建不足。"),
            mc(f"{pid}-lesen1", 3, "Instrumente der Kommunen u. a.?", ["nur Werbeplakate", "Mietobergrenzen, Genossenschaften", "Flugverbote"], 1, "Mietobergrenzen … Genossenschaften。", "城市手段？"),
            tf(f"{pid}-lesen1", 4, "Der Text opfert Klimastandards für Tempo.", False, "ohne … Klimastandards zu opfern。", "為速度犧牲氣候標準。"),
            mc(f"{pid}-lesen1", 5, "Warnung am Ende bezieht sich auf …", ["Touristen", "Funktionsfähigkeit der Stadt", "Wetter"], 1, "Funktionsfähigkeit。", "結尾警告？"),
            mc(f"{pid}-lesen1", 6, "Wohnen wird beschrieben als …", ["nur Anlage", "Voraussetzung für Teilhabe", "Hobby"], 1, "Voraussetzung für Teilhabe。", "居住被視為？"),
        ],
        passage=lesen1_passage,
        passage_zh="評論住房社會問題：僅新建不足；租金上限、合作社等工具；需土地政策與防假自住解約；加速程序但不犧牲品質／氣候；住房是參與前提。",
    )

    lesen2 = section(
        "lesen2",
        "lesen",
        "Lesen Teil 2",
        "閱讀 Teil 2",
        "Überschriften zuordnen.",
        "標題配對。",
        [
            mc(f"{pid}-lesen2", 1, "Text über Leerstand von Büros → Wohnungen:", ["A Leerstand umwidmen", "B", "C"], 0, "A。", "空置辦公室？"),
            mc(f"{pid}-lesen2", 2, "Text über studentisches Wohnen:", ["A", "B Campus unter Druck", "C"], 1, "B。", "學生住房？"),
            mc(f"{pid}-lesen2", 3, "Text über Lärmschutz Neubau:", ["A", "B", "C Leise bauen"], 2, "C。", "噪音防護？"),
            mc(f"{pid}-lesen2", 4, "Text über Genossenschaftsanteile:", ["D Teilen statt spekulieren", "A", "B"], 0, "D。", "合作社股份？"),
            mc(f"{pid}-lesen2", 5, "Text über Pendler und Wohnortwahl:", ["E Nähe kostet Zeit und Geld", "C", "A"], 0, "E。", "通勤與居住？"),
        ],
        passage=(
            "A Leerstand umwidmen\nB Campus unter Druck\nC Leise bauen\n"
            "D Teilen statt spekulieren\nE Nähe kostet Zeit und Geld\n\n"
            "(1) Büroflächen sollen zu Wohnungen werden. "
            "(2) Studentenwerke melden Wartelisten. "
            "(3) Schallschutz im Neubau wird verschärft. "
            "(4) Genossenschaften begrenzen Rendite. "
            "(5) Lange Pendelwege belasten Haushalte."
        ),
        passage_zh="標題配對：辦公室轉住宅、學生住房、隔音、合作社、通勤成本。",
    )

    lesen3 = section(
        "lesen3",
        "lesen",
        "Lesen Teil 3",
        "閱讀 Teil 3",
        "Meinungen zuordnen.",
        "意見歸屬。",
        [
            mc(f"{pid}-lesen3", 1, "Wer will mehr Sozialwohnungen?", ["Iris", "Paul", "Samir"], 0, "Iris。", "誰要更多社會住宅？"),
            mc(f"{pid}-lesen3", 2, "Wer warnt vor Investitionsstopp?", ["Iris", "Paul", "Samir"], 1, "Paul。", "誰擔心投資停滯？"),
            mc(f"{pid}-lesen3", 3, "Wer betont Genossenschaften?", ["Paul", "Samir", "Iris"], 1, "Samir。", "誰強調合作社？"),
            tf(f"{pid}-lesen3", 4, "Alle drei lehnen Neubau ab.", False, "立場不同，並非全反新建。", "三人皆反新建。"),
            mc(f"{pid}-lesen3", 5, "Wer erwähnt Lehrkräfte/Pflege?", ["Iris", "Paul", "Samir"], 0, "Iris。", "誰提教師／護理？"),
            mc(f"{pid}-lesen3", 6, "Wer spricht von Konzeptvergabe?", ["Samir", "Paul", "Iris"], 0, "Samir。", "誰提概念標？"),
        ],
        passage=(
            "Iris: Ohne neue Sozialbindungen verlieren wir Lehrkräfte und Pflegepersonal.\n"
            "Paul: Deckel ohne Neubauanreize führen zu Investitionsstopp.\n"
            "Samir: Konzeptvergaben und Genossenschaften sichern langfristig bezahlbaren Wohnraum."
        ),
        passage_zh="Iris 要社會住宅綁定；Paul 怕投資停；Samir 挺概念標與合作社。",
    )

    lesen4_passage = _long(
        """
        Infotext: Förderprogramm „Bezahlbar Wohnen“
        Das Land fördert Kommunen und Genossenschaften bei Neubau und Sanierung mit
        zinsgünstigen Darlehen. Voraussetzung ist eine Mietpreisbindung von mindestens
        zwanzig Jahren sowie Energiestandard EH40 oder besser. Anträge sind digital zu stellen;
        Fristen enden jeweils zum Quartalsende. Bei Verstößen gegen die Bindung kann das Darlehen
        fällig gestellt werden. Beratungsstellen helfen bei der Tragfähigkeitsprüfung.
        Privatpersonen sind nicht direkt antragsberechtigt, können aber über Genossenschaftsanteile
        partizipieren. Eine Evaluation nach fünf Jahren soll prüfen, ob die Fördermittel
        tatsächlich bei Haushalten mit mittlerem und niedrigem Einkommen ankommen.
        """
    )
    lesen4 = section(
        "lesen4",
        "lesen",
        "Lesen Teil 4",
        "閱讀 Teil 4",
        "Informationstext Förderung.",
        "補助資訊文。",
        [
            mc(f"{pid}-lesen4", 1, "Wer wird gefördert?", ["nur Touristen", "Kommunen und Genossenschaften", "nur Banken"], 1, "Kommunen und Genossenschaften。", "補助對象？"),
            tf(f"{pid}-lesen4", 2, "Mietpreisbindung mind. 20 Jahre.", True, "mindestens zwanzig Jahren。", "租金綁定至少 20 年。"),
            mc(f"{pid}-lesen4", 3, "Energiestandard?", ["beliebig", "EH40 oder besser", "nur Kohle"], 1, "EH40 oder besser。", "能源標準？"),
            tf(f"{pid}-lesen4", 4, "Privatpersonen beantragen direkt.", False, "nicht direkt antragsberechtigt。", "個人可直接申請。"),
            mc(f"{pid}-lesen4", 5, "Evaluation nach?", ["1 Jahr", "5 Jahren", "50 Jahren"], 1, "nach fünf Jahren。", "何時評估？"),
        ],
        passage=lesen4_passage,
        passage_zh="邦補助市鎮／合作社新建整修：租金綁定≥20 年、EH40；季末截止；違約可收回貸款；個人不直接申請；五年後評估。",
    )

    lesen5_passage = _long(
        """
        Kommentar: Integration beginnt in der Nachbarschaft
        Sprachkurse und Arbeitsmarktzugang sind zentral – doch ohne bezahlbaren Wohnraum
        und Begegnungsmöglichkeiten bleiben Integrationsversprechen abstrakt. Quartierszentren,
        Sportvereine und gemeinsame Hofprojekte schaffen Alltagskontakte, die Vorurteile abbauen.
        Gleichzeitig dürfen strukturelle Diskriminierung auf dem Wohnungsmarkt nicht bagatellisiert
        werden. Kommunale Wohnungsgesellschaften sollten anonyme Bewerbungsverfahren testen.
        Wer Integration nur als Bringschuld der Zugewanderten formuliert, übergeht die
        Verantwortung der Mehrheitsgesellschaft für offenen Zugang zu Bildung und Wohnen.
        Erfolgreiche Beispiele zeigen: Verlässliche Finanzierung und längere Projektlaufzeiten
        wirken besser als symbolische Aktionswochen.
        """
    )
    lesen5 = section(
        "lesen5",
        "lesen",
        "Lesen Teil 5",
        "閱讀 Teil 5",
        "Kommentar Integration/Nachbarschaft.",
        "評論：融合與鄰里。",
        [
            tf(f"{pid}-lesen5", 1, "Wohnraum spielt für Integration eine Rolle.", True, "ohne bezahlbaren Wohnraum … abstrakt。", "住房對融合重要。"),
            mc(f"{pid}-lesen5", 2, "Was schafft Alltagskontakte?", ["nur Apps", "Quartierszentren, Sport, Hofprojekte", "nur Behördenbriefe"], 1, "Quartierszentren …。", "日常接觸？"),
            tf(f"{pid}-lesen5", 3, "Diskriminierung auf dem Wohnungsmarkt wird geleugnet.", False, "dürfen … nicht bagatellisiert。", "文中否認歧視。"),
            mc(f"{pid}-lesen5", 4, "Vorschlag für Wohnungsgesellschaften?", ["anonyme Bewerbungen", "höhere Kaution immer", "keine Vermietung"], 0, "anonyme Bewerbungsverfahren。", "建議？"),
            mc(f"{pid}-lesen5", 5, "Was wirkt besser als Aktionswochen?", ["kürzere Projekte", "verlässliche Finanzierung und längere Laufzeiten", "weniger Geld"], 1, "verlässliche Finanzierung。", "什麼更有效？"),
            mc(f"{pid}-lesen5", 6, "Kritik an „Bringschuld“-Narrativ?", ["ja, zu einseitig", "nein, völlig richtig", "irrelevant"], 0, "übergeht die Verantwortung der Mehrheitsgesellschaft。", "對「單向義務」？"),
        ],
        passage=lesen5_passage,
        passage_zh="融合需可负担住房與接觸機會；社區中心／運動有效；住房歧視不可淡化；建議匿名申請；穩定經費勝過象徵活動週。",
    )

    hoeren1 = section(
        "hoeren1",
        "hoeren",
        "Hören Teil 1",
        "聽力 Teil 1",
        "Interview Stadtplanerin.",
        "都市規劃訪談。",
        [
            mc(f"{pid}-hoeren1", 1, "Lösung laut Expertin?", ["nur Abriss", "Mix aus Neubau, Umbau, Bindungen", "keine Regeln"], 1, "Mix。", "解方？"),
            tf(f"{pid}-hoeren1", 2, "Sie lehnt Genossenschaften ab.", False, "Genossenschaften ausdrücklich erwähnt。", "她反對合作社。"),
            mc(f"{pid}-hoeren1", 3, "Problem Spekulation?", ["irrelevant", "Brachflächen und Leerstand", "nur Tourismus"], 1, "Brachflächen。", "投機問題？"),
            mc(f"{pid}-hoeren1", 4, "Zeitrahmen Masterplan?", ["Wochen", "zehn Jahre", "Jahrhundert"], 1, "zehn Jahre。", "總計畫時程？"),
            mc(f"{pid}-hoeren1", 5, "Bürgerbeteiligung?", ["unerwünscht", "früh und verbindlich", "nur online Spiele"], 1, "früh und verbindlich。", "公民參與？"),
        ],
        audio_text=_long(
            """
            Interviewer: Frau Roth, wie lösen wir die Wohnungskrise?
            Roth: Durch einen Mix aus Neubau, Umbau von Leerstand und langen Sozialbindungen.
            Genossenschaften gehören dazu. Spekulative Brachflächen müssen aktiviert werden.
            Unser Masterplan gilt für zehn Jahre. Bürgerbeteiligung muss früh und verbindlich sein,
            sonst scheitern Projekte am Widerstand.
            """
        ),
    )

    hoeren2 = section(
        "hoeren2",
        "hoeren",
        "Hören Teil 2",
        "聽力 Teil 2",
        "Diskussion Wohnpolitik.",
        "住房政策討論。",
        [
            mc(f"{pid}-hoeren2", 1, "Position Frau Delgado?", ["Mietendeckel sofort überall", "Deckel + Neubauanreize", "kein Staat"], 1, "Deckel und Anreize。", "Delgado？"),
            mc(f"{pid}-hoeren2", 2, "Herr Stein betont?", ["nur Abriss", "Planungssicherheit für Investoren", "Verbote von Fahrrädern"], 1, "Planungssicherheit。", "Stein？"),
            tf(f"{pid}-hoeren2", 3, "Beide wollen schnelleres Baurecht.", True, "schnellere Verfahren。", "雙方要更快程序。"),
            mc(f"{pid}-hoeren2", 4, "Streitpunkt?", ["Wetter", "wie stark regulieren", "Urlaub"], 1, "Regulierungsintensität。", "爭議？"),
            mc(f"{pid}-hoeren2", 5, "Kompromissidee?", ["Konzeptvergabe", "alles privat", "Baustopp"], 0, "Konzeptvergabe。", "折衷？"),
        ],
        audio_text=_long(
            """
            Delgado: Wir brauchen Mietobergrenzen und zugleich Anreize für sozialen Neubau.
            Stein: Investoren brauchen Planungssicherheit, sonst bleibt der Kran stehen.
            Beide: Verfahren müssen schneller werden. Ein Kompromiss könnte die Konzeptvergabe sein,
            bei der nicht der höchste Preis, sondern soziale Kriterien entscheiden.
            """
        ),
    )

    hoeren3 = section(
        "hoeren3",
        "hoeren",
        "Hören Teil 3",
        "聽力 Teil 3",
        "Vortrag Nachbarschaft.",
        "鄰里演講。",
        [
            mc(f"{pid}-hoeren3", 1, "These?", ["Integration nur Sprachtest", "Begegnung im Quartier ist zentral", "Wohnen egal"], 1, "Begegnung im Quartier。", "論點？"),
            tf(f"{pid}-hoeren3", 2, "Hofprojekte werden positiv erwähnt.", True, "Hofprojekte。", "提到庭院專案。"),
            mc(f"{pid}-hoeren3", 3, "Kritik an Aktionswochen?", ["zu teuer immer", "oft symbolisch und kurz", "verboten"], 1, "symbolisch und kurz。", "批評活動週？"),
            mc(f"{pid}-hoeren3", 4, "Forderung Finanzierung?", ["einmalig", "verlässlich und längerfristig", "abschaffen"], 1, "verlässlich und längerfristig。", "經費？"),
            mc(f"{pid}-hoeren3", 5, "Wer trägt Mitverantwortung?", ["nur Zugewanderte", "auch Mehrheitsgesellschaft", "niemand"], 1, "Mehrheitsgesellschaft。", "誰有責任？"),
        ],
        audio_text=_long(
            """
            Integration gelingt nicht allein durch Sprachtests. Begegnung im Quartier ist zentral –
            über Sport, Hofprojekte und offene Treffs. Aktionswochen sind oft symbolisch und zu kurz.
            Wir brauchen verlässliche, längerfristige Finanzierung. Die Mehrheitsgesellschaft trägt
            Mitverantwortung für offenen Zugang zu Wohnen und Bildung.
            """
        ),
    )

    hoeren4 = section(
        "hoeren4",
        "hoeren",
        "Hören Teil 4",
        "聽力 Teil 4",
        "Kurzbeiträge Wohnen/Gesellschaft.",
        "短訊：居住／社會。",
        [
            mc(f"{pid}-hoeren4", 1, "Beitrag 1?", ["Ski", "Büro-zu-Wohnung Pilot", "Weinmesse"], 1, "Büro zu Wohnung。", "第 1 則？"),
            mc(f"{pid}-hoeren4", 2, "Beitrag 2 Wartelisten?", ["Kindergarten nur", "Studentenwohnheime", "Flughafen"], 1, "Studentenwohnheime。", "第 2 則？"),
            tf(f"{pid}-hoeren4", 3, "Beitrag 3: Genossenschaft vergibt Anteile per Los.", True, "per Losverfahren。", "合作社抽籤配股。"),
            mc(f"{pid}-hoeren4", 4, "Beitrag 4 Thema?", ["anonymous Bewerbungen Test", "Formel 1", "Modewoche"], 0, "anonyme Bewerbungen。", "第 4 則？"),
            mc(f"{pid}-hoeren4", 5, "Wo startet der Pilot Büro→Wohnen?", ["Dorf", "Innenstadt Leipzig", "Ausland"], 1, "Innenstadt Leipzig。", "試點何處？"),
        ],
        audio_text=_long(
            """
            Beitrag 1: In der Leipziger Innenstadt startet ein Pilot, Büros zu Wohnungen umzubauen.
            Beitrag 2: Studentenwerke melden rekordlange Wartelisten für Wohnheime.
            Beitrag 3: Eine Genossenschaft vergibt neue Anteile per Losverfahren.
            Beitrag 4: Eine kommunale Wohnungsgesellschaft testet anonyme Bewerbungen gegen Diskriminierung.
            """
        ),
    )

    schreiben1 = section(
        "schreiben1",
        "schreiben",
        "Schreiben Teil 1",
        "寫作 Teil 1",
        "Forumskommentar (ca. 100 Wörter).",
        "論壇留言（約 100 詞）。",
        [
            schreiben_item(
                f"{pid}-schreiben1",
                1,
                "Forumsthema „Bezahlbares Wohnen“:\n"
                "• Position\n• Argument mit lokalem Bezug\n• Vorschlag (z. B. Genossenschaft/Umbau)",
                "論壇「可负担住房」：立場、在地論點、建議（合作社／改建等）。",
                100,
                "Bezahlbares Wohnen ist Voraussetzung für eine funktionierende Stadt. "
                "In meinem Viertel steigen die Mieten schneller als die Löhne, Pflegekräfte ziehen weg. "
                "Ich plädiere für mehr Genossenschaften und die Umwandlung von Leerstand. "
                "Mietobergrenzen allein reichen nicht, aber ohne Bindungen bleibt Neubau spekulativ. "
                "Politik muss Tempo und sozialen Nutzen verbinden.",
                ["明確立場", "有在地／具體論點", "有建議", "約 100 詞"],
            )
        ],
    )

    schreiben2 = section(
        "schreiben2",
        "schreiben",
        "Schreiben Teil 2",
        "寫作 Teil 2",
        "Formelle Stellungnahme (ca. 150 Wörter).",
        "正式意見書（約 150 詞）。",
        [
            schreiben_item(
                f"{pid}-schreiben2",
                1,
                "Schreiben Sie an die Stadtverwaltung:\n"
                "• Forderung nach Konzeptvergabe eines Grundstücks\n"
                "• soziale und klimatische Kriterien\n• Bitte um Bürgerbeteiligung",
                "寫信市府：要求土地採概念標、社會與氣候標準、公民參與。",
                150,
                "Sehr geehrte Damen und Herren,\n"
                "bitte vergeben Sie das Grundstück an der Schulstraße per Konzeptverfahren. "
                "Entscheidend sollten bezahlbare Mieten, Energieeffizienz und gemeinschaftliche "
                "Freiräume sein – nicht allein der Höchstpreis. Wir bitten um eine frühzeitige "
                "Bürgerbeteiligung mit verbindlichen Ergebnissen. Gerne bringen wir als Nachbarschaft "
                "Vorschläge für ein genossenschaftliches Modell ein.\n"
                "Mit freundlichen Grüßen\nSamir Haddad",
                ["正式格式", "明確要求概念標", "社會／氣候標準", "要求參與", "約 150 詞"],
            )
        ],
    )

    sprechen1 = section(
        "sprechen1",
        "sprechen",
        "Sprechen Teil 1",
        "口說 Teil 1",
        "Partnerplanung.",
        "雙人規劃。",
        [
            sprechen_item(
                f"{pid}-sprechen1",
                1,
                "Planen Sie eine Nachbarschaftsinitiative: Ziele, Termine, Aufgabenverteilung.",
                "規劃鄰里倡議：目標、時程、分工。",
                ["Ziel", "Termine", "Öffentlichkeitsarbeit", "Aufgaben"],
                "Ziel ist ein Hofprojekt mit Hochbeeten. Nächsten Samstag Treffen im Zentrum. "
                "Du machst den Flyer, ich kontaktiere die Wohnungsgesellschaft.",
            )
        ],
    )
    sprechen2 = section(
        "sprechen2",
        "sprechen",
        "Sprechen Teil 2",
        "口說 Teil 2",
        "Kurzvortrag.",
        "短講。",
        [
            sprechen_item(
                f"{pid}-sprechen2",
                1,
                "Kurzvortrag: Warum ist bezahlbarer Wohnraum eine Integrationsfrage?",
                "短講：為何可负担住房是融合議題？",
                ["These", "Beispiel", "Gegenargument", "Fazit"],
                "Ohne stabile Wohnung bleiben Sprachkurs und Job abstrakt. Beispiel: Familien in "
                "befristeten Unterkünften. Gegenargument Markt allein – greift zu kurz. "
                "Fazit: Wohnpolitik ist Sozial- und Integrationspolitik.",
            )
        ],
    )

    return paper(
        pid,
        "B2",
        2,
        "Goethe-Format B2 · Modellsatz 2",
        "考場版 B2 · 第2回（對齊 Goethe-Zertifikat B2 分節）",
        170,
        [lesen1, lesen2, lesen3, lesen4, lesen5, hoeren1, hoeren2, hoeren3, hoeren4, schreiben1, schreiben2, sprechen1, sprechen2],
    )


def main() -> None:
    data = json.loads(OUT.read_text(encoding="utf-8"))
    papers: list[dict[str, Any]] = data["papers"]

    # Preserve existing 8; tag compact if missing
    old_ids = [p["id"] for p in papers]
    assert old_ids == [
        "a1-m1",
        "a1-m2",
        "a2-m1",
        "a2-m2",
        "b1-m1",
        "b1-m2",
        "b2-m1",
        "b2-m2",
    ], f"Unexpected existing ids: {old_ids}"

    for p in papers:
        if "format" not in p:
            p["format"] = "compact"

    # Remove any previously appended goethe papers (idempotent re-run)
    papers[:] = [p for p in papers if p["id"] not in GOETHE_IDS]

    new_papers = [
        a1_g1(),
        a1_g2(),
        a2_g1(),
        a2_g2(),
        b1_g1(),
        b1_g2(),
        b2_g1(),
        b2_g2(),
    ]

    for np in new_papers:
        assert np["format"] == "goethe"
        assert all(sec["kind"] != "bausteine" for sec in np["sections"])
        papers.append(np)

    data["note"] = NOTE
    data["papers"] = papers
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("Updated", OUT)
    print(f"{'id':8} {'secs':>4} {'scored':>6} {'dur':>4}")
    mins = {"A1": 28, "A2": 32, "B1": 36, "B2": 38}
    for np in new_papers:
        sc = scored_count(np)
        print(f"{np['id']:8} {len(np['sections']):4} {sc:6} {np['durationMin']:4}")
        assert sc >= mins[np["level"]], f"{np['id']} scored {sc} < {mins[np['level']]}"

    ids = [p["id"] for p in papers]
    for gid in GOETHE_IDS:
        assert gid in ids, f"missing {gid}"
    assert len(papers) == 16, f"expected 16 papers, got {len(papers)}"

    goethe = [p for p in papers if p.get("format") == "goethe"]
    assert len(goethe) == 8
    for p in goethe:
        assert p["format"] == "goethe"
        assert all(s["kind"] != "bausteine" for s in p["sections"])

    print("OK: 8 Goethe papers appended; total papers == 16")


if __name__ == "__main__":
    main()
