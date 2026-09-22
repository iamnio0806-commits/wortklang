#!/usr/bin/env python3
"""Append Goethe-format 稍易／稍難 variant mock exams (round 5–6) to exams.json.

- Keeps all existing 24 papers
- Appends 8 new papers (g5 leichter, g6 etwas_schwerer) for A1–B2
- Idempotent: replaces only the 8 variant2 ids on re-run
- Asserts total papers == 32
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
    "A1–B2 各兩份練習版＋多份考場版（含同級內多套稍易／標準／稍難變體；稍易≠下一級簡單，稍難≠上一級）。"
    "聚焦 Lesen＋Hören（TTS 朗讀腳本）＋Schreiben；Sprechen 為選練口說提示，不計入及格門檻。"
    "答完後可對照中文譯文與詳解。非官方試題，僅供練習。"
)

VARIANT_IDS = [
    "a1-g5",
    "a1-g6",
    "a2-g5",
    "a2-g6",
    "b1-g5",
    "b1-g6",
    "b2-g5",
    "b2-g6",
]

MIN_SCORED = {"A1": 30, "A2": 34, "B1": 40, "B2": 44}


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
    *,
    difficulty: str,
) -> dict[str, Any]:
    return {
        "id": pid,
        "level": level,
        "round": round_,
        "format": "goethe",
        "difficulty": difficulty,
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


def _long(s: str) -> str:
    return " ".join(s.split())


# ═══════════════════════════════════════════════════════════════════════════
# A1-g5 · leichter — Bibliothek / Bücher ausleihen
# ═══════════════════════════════════════════════════════════════════════════


def a1_g5() -> dict[str, Any]:
    pid = "a1-g5"
    lesen1 = section(
        "lesen1",
        "lesen",
        "Lesen Teil 1",
        "閱讀 Teil 1",
        "Lesen Sie die Nachrichten. Kreuzen Sie die richtige Antwort an (a, b oder c).",
        "請閱讀簡訊／郵件，選出正確答案。",
        [
            mc(f"{pid}-lesen1", 1, "Wann öffnet die Bibliothek?", ["8 Uhr", "9 Uhr", "10 Uhr"], 1, "Öffnung um 9 Uhr。", "圖書館幾點開？"),
            mc(f"{pid}-lesen1", 2, "Was soll Lin mitbringen?", ["Ausweis", "Geld", "Laptop"], 0, "Ausweis。", "Lin 要帶什麼？"),
            mc(f"{pid}-lesen1", 3, "Wo ist die Bibliothek?", ["Schulstraße 2", "Markt 2", "Park 1"], 0, "Schulstraße 2。", "在哪？"),
            tf(f"{pid}-lesen1", 4, "Die Bibliothek ist sonntags geöffnet.", False, "So geschlossen。", "週日有開。"),
            tf(f"{pid}-lesen1", 5, "Lin holt das Buch um 16 Uhr.", True, "um 16 Uhr。", "Lin 四點取書。"),
        ],
        passage=(
            "E-Mail Stadtbibliothek an Lin:\n"
            "Hallo Lin! Wir öffnen Mo–Fr um 9 Uhr. Samstag 10–14 Uhr. Sonntag geschlossen. "
            "Bitte bringen Sie Ihren Ausweis mit. Adresse: Schulstraße 2.\n\n"
            "SMS von Lin an Sam:\n"
            "Sam, ich hole das Buch um 16 Uhr. Bis später!"
        ),
        passage_zh="市圖週一至五 9 點開、週六 10–14、週日休；請帶證件，Schulstraße 2；Lin 約 16 點取書。",
    )
    lesen2 = section(
        "lesen2",
        "lesen",
        "Lesen Teil 2",
        "閱讀 Teil 2",
        "Lesen Sie die Schilder. Welche Aussage passt?",
        "請閱讀告示，選出正確敘述。",
        [
            mc(f"{pid}-lesen2", 1, "Ausleihe: Wie lange?", ["1 Woche", "3 Wochen", "3 Monate"], 1, "3 Wochen。", "借閱多久？"),
            mc(f"{pid}-lesen2", 2, "WLAN: Status?", ["kostenlos", "nur Personal", "gesperrt"], 0, "WLAN gratis。", "無線網路？"),
            mc(f"{pid}-lesen2", 3, "Ruhezone: Was gilt?", ["Telefonieren OK", "leise bleiben", "Musik laut"], 1, "bitte leise。", "安靜區？"),
            mc(f"{pid}-lesen2", 4, "Drucker: Wo?", ["EG", "1. Stock", "Keller"], 1, "1. Stock。", "印表機？"),
            mc(f"{pid}-lesen2", 5, "Was ist verboten?", ["Lesen", "Essen am Platz", "Notizen"], 1, "Kein Essen。", "禁止？"),
        ],
        passage=(
            "Ausleihe: Bücher 3 Wochen.\n"
            "WLAN gratis für Gäste.\n"
            "Ruhezone: bitte leise.\n"
            "Drucker und Kopierer: 1. Stock.\n"
            "Lesesaal: Kein Essen am Platz."
        ),
        passage_zh="書可借 3 週；免費 Wi‑Fi；安靜區請小聲；印表機在 1 樓；閱覽室禁飲食。",
    )
    lesen3 = section(
        "lesen3",
        "lesen",
        "Lesen Teil 3",
        "閱讀 Teil 3",
        "Lesen Sie den Text. Ja – Nein – Steht nicht im Text.",
        "請閱讀短文，勾選：對、錯、或文中未提及。",
        [
            tf(f"{pid}-lesen3", 1, "Nora geht oft in die Bibliothek.", True, "oft in die Bibliothek。", "Nora 常去圖書館。"),
            tf(f"{pid}-lesen3", 2, "Die Bibliothek ist weit weg.", False, "nur zehn Minuten。", "很遠。"),
            tf(f"{pid}-lesen3", 3, "Nora liest gerne Krimis.", True, "gerne Krimis。", "喜歡推理。"),
            tf(f"{pid}-lesen3", 4, "Die Bibliothekarin heißt Frau Berg.", "nicht", "未提名字。", "館員叫 Berg。"),
            tf(f"{pid}-lesen3", 5, "Am Samstag schließt die Bibliothek um 14 Uhr.", True, "bis 14 Uhr。", "週六開到 14 點。"),
        ],
        passage=(
            "Meine Bibliothek\n"
            "Ich heiße Nora und gehe oft in die Stadtbibliothek. "
            "Sie ist nur zehn Minuten zu Fuß. Ich lese gerne Krimis. "
            "Am Samstag ist die Bibliothek bis 14 Uhr offen. Die Mitarbeiterin ist sehr hilfreich."
        ),
        passage_zh="Nora 常去步行十分鐘的市圖，愛看推理；週六開到 14 點；館員很幫忙。",
    )
    hoeren1 = section(
        "hoeren1",
        "hoeren",
        "Hören Teil 1",
        "聽力 Teil 1",
        "Sie hören fünf kurze Situationen. Wählen Sie a, b oder c.",
        "您會聽到五則短情境，選 a、b 或 c。",
        [
            mc(f"{pid}-hoeren1", 1, "Was kostet die Karte?", ["gratis", "5 €", "10 €"], 0, "Bibliothekskarte ist gratis。", "閱覽證多少錢？"),
            mc(f"{pid}-hoeren1", 2, "Wo sind die Kinderbücher?", ["EG", "1. Stock", "Keller"], 1, "ersten Stock。", "童書在哪？"),
            mc(f"{pid}-hoeren1", 3, "Wann schließt die Bibliothek?", ["17 Uhr", "18 Uhr", "19 Uhr"], 1, "um 18 Uhr。", "幾點關？"),
            mc(f"{pid}-hoeren1", 4, "Was sucht der Mann?", ["Zeitung", "Wörterbuch", "Karte"], 1, "ein Wörterbuch。", "找什麼？"),
            mc(f"{pid}-hoeren1", 5, "Welches Stockwerk Toilette?", ["EG", "2. Stock", "Dach"], 0, "Erdgeschoss。", "廁所幾樓？"),
        ],
        audio_text=(
            "Situation 1: Die Bibliothekskarte ist gratis. "
            "Situation 2: Die Kinderbücher finden Sie im ersten Stock. "
            "Situation 3: Heute schließt die Bibliothek um 18 Uhr. "
            "Situation 4: Entschuldigung, wo finde ich ein Wörterbuch? "
            "Situation 5: Die Toilette ist im Erdgeschoss neben dem Eingang."
        ),
    )
    hoeren2 = section(
        "hoeren2",
        "hoeren",
        "Hören Teil 2",
        "聽力 Teil 2",
        "Sie hören ein Gespräch. Wählen Sie die richtige Antwort.",
        "請聽對話，選出正確答案。",
        [
            mc(f"{pid}-hoeren2", 1, "Was möchte die Frau?", ["Buch verlängern", "Auto kaufen", "Job"], 0, "Buch verlängern。", "想做什麼？"),
            mc(f"{pid}-hoeren2", 2, "Wie lange Verlängerung?", ["1 Woche", "2 Wochen", "1 Monat"], 1, "zwei Wochen。", "延長多久？"),
            mc(f"{pid}-hoeren2", 3, "Gibt es Gebühr?", ["nein", "2 €", "10 €"], 0, "keine Gebühr。", "要錢嗎？"),
            mc(f"{pid}-hoeren2", 4, "Wann zurück?", ["Freitag", "Montag", "Sonntag"], 0, "bis Freitag。", "何時還？"),
        ],
        audio_text=(
            "Frau: Guten Tag, ich möchte dieses Buch verlängern. "
            "Mann: Gerne, zwei Wochen extra. Es gibt keine Gebühr. "
            "Frau: Super. Bis wann muss ich es zurückbringen? "
            "Mann: Bis Freitag. Auf Wiedersehen!"
        ),
    )
    hoeren3 = section(
        "hoeren3",
        "hoeren",
        "Hören Teil 3",
        "聽力 Teil 3",
        "Sie hören eine Durchsage. Wählen Sie a, b oder c.",
        "請聽廣播，選出正確答案。",
        [
            mc(f"{pid}-hoeren3", 1, "Was beginnt um 15 Uhr?", ["Lesung", "Konzert", "Sport"], 0, "Lesung für Kinder。", "15 點什麼？"),
            mc(f"{pid}-hoeren3", 2, "Wo findet sie statt?", ["Saal A", "Park", "Café"], 0, "Saal A。", "地點？"),
            mc(f"{pid}-hoeren3", 3, "Für wen?", ["nur Erwachsene", "Kinder", "nur Personal"], 1, "für Kinder。", "給誰？"),
            mc(f"{pid}-hoeren3", 4, "Anmeldung nötig?", ["nein", "ja, an der Infotheke", "nur online"], 1, "an der Infotheke。", "要報名？"),
        ],
        audio_text=(
            "Liebe Gäste: Um 15 Uhr beginnt eine Lesung für Kinder in Saal A. "
            "Bitte melden Sie sich kurz an der Infotheke an. "
            "Wir freuen uns auf Sie!"
        ),
    )
    schreiben1 = section(
        "schreiben1",
        "schreiben",
        "Schreiben Teil 1",
        "寫作 Teil 1",
        "Füllen Sie das Formular aus.",
        "請填寫表格中的空缺項目。",
        [
            gap(f"{pid}-schreiben1", 1, "Nachname: ___ (Chen)", "Chen", "姓 Chen。", prompt_zh="姓"),
            gap(f"{pid}-schreiben1", 2, "Vorname: ___ (Lin)", "Lin", "名 Lin。", prompt_zh="名"),
            gap(f"{pid}-schreiben1", 3, "Straße: ___ 2", "Schulstraße", "Schulstraße。", accept=["Schulstrasse", "Schulstraße"], prompt_zh="街名"),
            gap(f"{pid}-schreiben1", 4, "Telefon: ___", "0176987654", "電話。", accept=["0176 987654"], prompt_zh="電話"),
            gap(f"{pid}-schreiben1", 5, "Ausweisnummer: ___", "T1234567", "證件號。", prompt_zh="證件號"),
            gap(f"{pid}-schreiben1", 6, "Bücher: ___", "3", "三本。", accept=["drei", "3 Bücher"], prompt_zh="冊數"),
        ],
        passage=(
            "Anmeldung Stadtbibliothek\n"
            "Nachname: ________\nVorname: ________\n"
            "Adresse: ________ 2\nTelefon: ________\n"
            "Ausweisnummer: ________\nAnzahl Bücher heute: ________\n"
            "(Hinweis: Chen / Lin / Schulstraße / 0176987654 / T1234567 / 3)"
        ),
        passage_zh="請依提示填寫：Chen、Lin、Schulstraße、電話、證件號、3。",
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
                "Sie können ein Buch nicht rechtzeitig zurückbringen. Schreiben Sie an die Bibliothek:\n"
                "• Entschuldigung / Grund\n• Welches Buch?\n• Wann bringen Sie es zurück?",
                "你無法準時還書。寫給圖書館：道歉／原因、哪本書、何時歸還？",
                30,
                "Guten Tag,\nleider kann ich das Buch „Sommerregen“ heute nicht zurückbringen, "
                "weil ich krank bin. Ich komme am Montag wieder.\nViele Grüße\nLin Chen",
                ["有道歉與原因", "提到書名或書籍", "說明歸還時間", "約 30 字"],
            )
        ],
    )
    sprechen1 = section(
        "sprechen1", "sprechen", "Sprechen Teil 1", "口說 Teil 1",
        "Stellen Sie sich vor.", "請自我介紹。",
        [sprechen_item(f"{pid}-sprechen1", 1,
            "Stellen Sie sich vor: Name, Herkunft, Wohnort, Lesen / Bibliothek.",
            "自我介紹：名字、出身、住處、閱讀／圖書館。",
            ["Name", "Woher?", "Wohnort", "Lesen Sie gerne?"],
            "Guten Tag, ich heiße Lin Chen. Ich komme aus Taiwan und wohne in Bonn. "
            "Ich gehe oft in die Bibliothek und lese gerne Krimis.")],
    )
    sprechen2 = section(
        "sprechen2", "sprechen", "Sprechen Teil 2", "口說 Teil 2",
        "Stellen Sie Fragen.", "請依提示提問。",
        [sprechen_item(f"{pid}-sprechen2", 1,
            "Sie möchten Informationen über die Bibliothek. Stellen Sie Fragen.",
            "你想了解圖書館，請提問。",
            ["Öffnungszeiten?", "Wie lange ausleihen?", "WLAN?", "Wo Kinderbücher?"],
            "Wann haben Sie geöffnet? Wie lange kann ich Bücher ausleihen? Gibt es WLAN? Wo sind die Kinderbücher?")],
    )
    sprechen3 = section(
        "sprechen3", "sprechen", "Sprechen Teil 3", "口說 Teil 3",
        "Bitten Sie um etwas.", "請提出請求。",
        [sprechen_item(f"{pid}-sprechen3", 1,
            "Bitten Sie um Hilfe: Sie finden ein Wörterbuch nicht.",
            "請人幫忙：你找不到詞典。",
            ["Entschuldigung", "Wörterbuch", "Welches Regal?", "Danke"],
            "Entschuldigung, wo finde ich ein Wörterbuch? Können Sie mir bitte helfen? Vielen Dank.")],
    )
    return paper(
        pid, "A1", 5,
        "Goethe-Format A1 · Modellsatz 5 (leichter)",
        "考場版 A1 · 第5回（稍易）",
        65,
        [lesen1, lesen2, lesen3, hoeren1, hoeren2, hoeren3, schreiben1, schreiben2, sprechen1, sprechen2, sprechen3],
        difficulty="leichter",
    )


# ═══════════════════════════════════════════════════════════════════════════
# A1-g6 · etwas_schwerer — Hotel / Übernachtung
# ═══════════════════════════════════════════════════════════════════════════


def a1_g6() -> dict[str, Any]:
    pid = "a1-g6"
    lesen1 = section(
        "lesen1", "lesen", "Lesen Teil 1", "閱讀 Teil 1",
        "Lesen Sie die Nachrichten. Kreuzen Sie die richtige Antwort an.",
        "請閱讀簡訊／郵件，選出正確答案。",
        [
            mc(f"{pid}-lesen1", 1, "Wann ist der Check-in?", ["ab 12 Uhr", "ab 14 Uhr", "ab 16 Uhr"], 1, "ab 14 Uhr。", "何時入住？"),
            mc(f"{pid}-lesen1", 2, "Was soll Herr Kim mitbringen?", ["Ausweis und Buchungsnummer", "nur Geld", "Hund"], 0, "Ausweis und Buchungsnummer。", "要帶什麼？"),
            mc(f"{pid}-lesen1", 3, "Wo ist das Hotel?", ["Bahnhofsplatz 4", "Park 4", "Markt 1"], 0, "Bahnhofsplatz 4。", "飯店在哪？"),
            tf(f"{pid}-lesen1", 4, "Das Frühstück ist inklusive.", True, "Frühstück inklusive。", "含早餐。"),
            tf(f"{pid}-lesen1", 5, "Check-out ist um 10 Uhr.", False, "Check-out bis 11 Uhr。", "退房十點。"),
            tf(f"{pid}-lesen1", 6, "Herr Kim braucht fürs WLAN ein Passwort an der Rezeption.", True, "WLAN-Passwort an der Rezeption。", "Wi‑Fi 密碼在櫃檯。"),
        ],
        passage=(
            "E-Mail Hotel Nordstern an Herrn Kim:\n"
            "Sehr geehrter Herr Kim,\n"
            "Ihre Buchung ist bestätigt. Check-in ab 14 Uhr, Check-out bis 11 Uhr. "
            "Bitte bringen Sie Ausweis und Buchungsnummer mit. Adresse: Bahnhofsplatz 4. "
            "Frühstück ist inklusive (7–10 Uhr). WLAN-Passwort bekommen Sie an der Rezeption.\n"
            "Mit freundlichen Grüßen\nTeam Nordstern\n\n"
            "SMS von Kim an Lea:\n"
            "Lea, ich bin um 15 Uhr im Hotel. Bring bitte die Buchungsmail mit."
        ),
        passage_zh="Nordstern 飯店確認訂房：14 點入住、11 點前退房，帶證件與訂單號，Bahnhofsplatz 4；含早餐；Wi‑Fi 密碼在櫃檯；Kim 約 15 點到。",
    )
    lesen2 = section(
        "lesen2", "lesen", "Lesen Teil 2", "閱讀 Teil 2",
        "Lesen Sie die Schilder. Welche Aussage passt?",
        "請閱讀告示，選出正確敘述。",
        [
            mc(f"{pid}-lesen2", 1, "Parken: Was gilt?", ["gratis 24h", "Max. 2 Std. Gäste", "nur Personal"], 1, "Max. 2 Stunden。", "停車？"),
            mc(f"{pid}-lesen2", 2, "Aufzug: Status?", ["OK", "Außer Betrieb", "nur 22–6 Uhr"], 1, "AUSSER BETRIEB。", "電梯？"),
            mc(f"{pid}-lesen2", 3, "Frühstück: Wann?", ["6–8", "7–10", "9–12"], 1, "7:00–10:00。", "早餐？"),
            mc(f"{pid}-lesen2", 4, "Rauchverbot: Wo?", ["nur Zimmer", "gesamtes Hotel", "nur Lobby"], 1, "im ganzen Hotel。", "禁菸？"),
            mc(f"{pid}-lesen2", 5, "Handtücher: Was tun bei Bedarf?", ["wegwerfen", "Rezeption anrufen", "nichts"], 1, "Rezeption anrufen。", "要毛巾？"),
            mc(f"{pid}-lesen2", 6, "Safe: Wo?", ["EG Rezeption", "Dach", "Parkplatz"], 0, "an der Rezeption。", "保險箱？"),
        ],
        passage=(
            "Parkplatz Gäste: Max. 2 Stunden, Ticket an der Rezeption.\n"
            "Aufzug: AUSSER BETRIEB – bitte Treppe nutzen.\n"
            "Frühstück: 7:00–10:00 · Speisesaal EG.\n"
            "Rauchen im ganzen Hotel verboten.\n"
            "Extra Handtücher: bitte Rezeption anrufen (Taste 9).\n"
            "Safe und Wertgegenstände: an der Rezeption."
        ),
        passage_zh="訪客停車最多 2 小時；電梯故障；早餐 7–10；全館禁菸；加毛巾按 9；保險箱在櫃檯。",
    )
    lesen3 = section(
        "lesen3", "lesen", "Lesen Teil 3", "閱讀 Teil 3",
        "Lesen Sie den Text. Ja – Nein – Steht nicht im Text.",
        "請閱讀短文，勾選：對、錯、或文中未提及。",
        [
            tf(f"{pid}-lesen3", 1, "Yuna übernachtet zwei Nächte im Hotel.", True, "zwei Nächte。", "住兩晚。"),
            tf(f"{pid}-lesen3", 2, "Das Hotel liegt neben dem Bahnhof.", True, "neben dem Bahnhof。", "在車站旁。"),
            tf(f"{pid}-lesen3", 3, "Das Zimmer hat ein großes Bad.", True, "großes Bad。", "有大衛浴。"),
            tf(f"{pid}-lesen3", 4, "Yuna zahlt 89 Euro pro Nacht.", "nicht", "未提房價。", "一晚 89 歐。"),
            tf(f"{pid}-lesen3", 5, "Am Abend isst sie im Hotelrestaurant.", False, "in einem Restaurant in der Stadt。", "晚上在飯店餐廳吃。"),
            tf(f"{pid}-lesen3", 6, "Yuna möchte morgen früh frühstücken.", True, "morgen frühstücke ich。", "明天想吃早餐。"),
        ],
        passage=(
            "Mein Hotelbesuch\n"
            "Ich heiße Yuna und übernachte zwei Nächte im Hotel Nordstern neben dem Bahnhof. "
            "Mein Zimmer ist ruhig und hat ein großes Bad. Die Rezeption hilft mir mit dem Stadtplan. "
            "Am Abend esse ich in einem Restaurant in der Stadt, nicht im Hotel. "
            "Morgen frühstücke ich im Speisesaal und fahre dann weiter. Ob der Zug pünktlich ist, "
            "weiß ich noch nicht – wichtig ist, rechtzeitig einzuchecken und den Ausweis dabei zu haben."
        ),
        passage_zh="Yuna 在車站旁 Nordstern 住兩晚，房間安靜有大衛浴；晚上在城裡餐廳吃；明早在餐廳用早餐再出發。",
    )
    hoeren1 = section(
        "hoeren1", "hoeren", "Hören Teil 1", "聽力 Teil 1",
        "Sie hören kurze Situationen.", "短情境聽力。",
        [
            mc(f"{pid}-hoeren1", 1, "Welche Zimmernummer?", ["204", "214", "240"], 1, "Zimmer 214。", "房號？"),
            mc(f"{pid}-hoeren1", 2, "Wann Frühstück?", ["7 Uhr", "8 Uhr", "9 Uhr"], 0, "ab 7 Uhr。", "早餐？"),
            mc(f"{pid}-hoeren1", 3, "Wo WLAN-Passwort?", ["Zimmerzettel", "Rezeption", "App only"], 1, "an der Rezeption。", "密碼？"),
            mc(f"{pid}-hoeren1", 4, "Was fehlt dem Gast?", ["Handtuch", "Schlüssel", "Kaffee"], 0, "ein Handtuch。", "缺什麼？"),
            mc(f"{pid}-hoeren1", 5, "Taxi wann?", ["7:30", "8:30", "9:30"], 1, "um halb neun。", "計程車？"),
            mc(f"{pid}-hoeren1", 6, "Warum Speisesaal zu?", ["Putzen", "erst ab 7 Uhr", "Feier"], 1, "öffnet erst um 7 Uhr。", "為何關？"),
        ],
        audio_text=(
            "Situation 1: Ihr Zimmer ist Nummer 214, zweiter Stock. "
            "Situation 2: Das Frühstück beginnt ab 7 Uhr. "
            "Situation 3: Das WLAN-Passwort bekommen Sie an der Rezeption. "
            "Situation 4: Entschuldigung, ich brauche bitte noch ein Handtuch. "
            "Situation 5: Das Taxi kommt morgen um halb neun. "
            "Situation 6: Der Speisesaal öffnet erst um 7 Uhr."
        ),
    )
    hoeren2 = section(
        "hoeren2", "hoeren", "Hören Teil 2", "聽力 Teil 2",
        "Sie hören ein Gespräch.", "請聽對話。",
        [
            mc(f"{pid}-hoeren2", 1, "Was möchte der Gast?", ["verlängern", "nur duschen", "Job"], 0, "eine Nacht verlängern。", "想做什麼？"),
            mc(f"{pid}-hoeren2", 2, "Gibt es noch Zimmer?", ["nein", "ja, 215", "nur Suite"], 1, "Zimmer 215。", "還有房？"),
            mc(f"{pid}-hoeren2", 3, "Aufpreis?", ["0 €", "20 €", "50 €"], 1, "zwanzig Euro。", "加價？"),
            mc(f"{pid}-hoeren2", 4, "Frühstück dabei?", ["ja", "nein", "nur Kaffee"], 0, "Frühstück inklusive。", "含早餐？"),
            tf(f"{pid}-hoeren2", 5, "Er muss sofort bar zahlen.", False, "kann auch mit Karte。", "必須立刻付現金。"),
        ],
        audio_text=(
            "Gast: Guten Tag, kann ich eine Nacht verlängern? "
            "Rezeption: Ja, Zimmer 215 ist frei. Der Aufpreis ist zwanzig Euro, Frühstück inklusive. "
            "Gast: Muss ich bar zahlen? "
            "Rezeption: Nein, Sie können auch mit Karte zahlen."
        ),
    )
    hoeren3 = section(
        "hoeren3", "hoeren", "Hören Teil 3", "聽力 Teil 3",
        "Sie hören eine Durchsage.", "請聽廣播。",
        [
            mc(f"{pid}-hoeren3", 1, "Was ist gesperrt?", ["Lobby", "Parkplatz Ost", "Frühstück"], 1, "Parkplatz Ost。", "封閉？"),
            mc(f"{pid}-hoeren3", 2, "Alternative Parken?", ["West", "Bahnhof", "Straße nur"], 0, "Parkplatz West。", "改停哪？"),
            mc(f"{pid}-hoeren3", 3, "Wann wieder offen?", ["heute Abend", "morgen früh", "nächste Woche"], 1, "morgen früh。", "何時再開？"),
            mc(f"{pid}-hoeren3", 4, "Wo Infos?", ["App", "Rezeption", "Zimmer-TV"], 1, "an der Rezeption。", "資訊？"),
            tf(f"{pid}-hoeren3", 5, "Gäste sollen den Parkschein an der Rezeption holen.", True, "Parkschein an der Rezeption。", "要在櫃檯取停車單。"),
        ],
        audio_text=(
            "Liebe Gäste: Der Parkplatz Ost ist wegen Bauarbeiten gesperrt. "
            "Bitte parken Sie auf dem Parkplatz West und holen Sie Ihren Parkschein an der Rezeption. "
            "Ab morgen früh ist Ost wieder geöffnet. Informationen an der Rezeption."
        ),
    )
    schreiben1 = section(
        "schreiben1", "schreiben", "Schreiben Teil 1", "寫作 Teil 1",
        "Füllen Sie das Formular aus.", "請填寫表格。",
        [
            gap(f"{pid}-schreiben1", 1, "Nachname: ___ (Kim)", "Kim", "姓 Kim。", prompt_zh="姓"),
            gap(f"{pid}-schreiben1", 2, "Vorname: ___ (Yuna)", "Yuna", "名 Yuna。", prompt_zh="名"),
            gap(f"{pid}-schreiben1", 3, "Adresse Hotel: ___ 4", "Bahnhofsplatz", "Bahnhofsplatz。", accept=["Bahnhofplatz"], prompt_zh="地址"),
            gap(f"{pid}-schreiben1", 4, "Buchungsnummer: ___", "NS-8842", "訂單號。", prompt_zh="訂單號"),
            gap(f"{pid}-schreiben1", 5, "Nächte: ___", "2", "兩晚。", accept=["zwei"], prompt_zh="晚數"),
            gap(f"{pid}-schreiben1", 6, "Zimmer: ___", "214", "214。", prompt_zh="房號"),
        ],
        passage=(
            "Anmeldeformular Hotel Nordstern\n"
            "Nachname: ________ Vorname: ________\n"
            "Hoteladresse: ________ 4\nBuchungsnummer: ________\n"
            "Anzahl Nächte: ________ Zimmernummer: ________\n"
            "(Hinweis: Kim / Yuna / Bahnhofsplatz / NS-8842 / 2 / 214)"
        ),
        passage_zh="請填：Kim、Yuna、Bahnhofsplatz、訂單號、2、214。",
    )
    schreiben2 = section(
        "schreiben2", "schreiben", "Schreiben Teil 2", "寫作 Teil 2",
        "Schreiben Sie eine kurze Mitteilung (30–40 Wörter).",
        "請寫短訊（約 30–40 詞）。",
        [
            schreiben_item(
                f"{pid}-schreiben2", 1,
                "Sie kommen später an. Schreiben Sie an die Rezeption:\n"
                "• Entschuldigung / Grund\n• Neue Ankunftszeit\n• Bitte Zimmer freihalten",
                "你會晚到。寫給櫃檯：道歉／原因、新到達時間、請保留房間。",
                30,
                "Guten Tag,\nleider komme ich erst um 21 Uhr an, weil der Zug Verspätung hat. "
                "Bitte halten Sie mein Zimmer frei.\nViele Grüße\nYuna Kim",
                ["道歉與原因", "新時間", "請保留房間"],
            )
        ],
    )
    sprechen1 = section(
        "sprechen1", "sprechen", "Sprechen Teil 1", "口說 Teil 1",
        "Stellen Sie sich vor.", "請自我介紹。",
        [sprechen_item(f"{pid}-sprechen1", 1,
            "Stellen Sie sich vor: Name, Reise, Hotel, wie lange.",
            "自我介紹：名字、旅行、飯店、住多久。",
            ["Name", "Wohin?", "Hotel?", "Wie viele Nächte?"],
            "Ich heiße Yuna Kim. Ich reise nach Köln und übernachte zwei Nächte im Hotel Nordstern neben dem Bahnhof.")],
    )
    sprechen2 = section(
        "sprechen2", "sprechen", "Sprechen Teil 2", "口說 Teil 2",
        "Stellen Sie Fragen.", "請提問。",
        [sprechen_item(f"{pid}-sprechen2", 1,
            "Fragen Sie an der Rezeption nach dem Hotel.",
            "在櫃檯詢問飯店資訊。",
            ["Check-in?", "Frühstück?", "WLAN?", "Parkplatz?"],
            "Ab wann ist Check-in? Ist Frühstück inklusive? Wie bekomme ich WLAN? Wo kann ich parken?")],
    )
    sprechen3 = section(
        "sprechen3", "sprechen", "Sprechen Teil 3", "口說 Teil 3",
        "Bitten Sie um etwas.", "請提出請求。",
        [sprechen_item(f"{pid}-sprechen3", 1,
            "Bitten Sie um ein Extra-Handtuch und das WLAN-Passwort.",
            "請加一條毛巾並索取 Wi‑Fi 密碼。",
            ["Entschuldigung", "Handtuch", "WLAN-Passwort", "Danke"],
            "Entschuldigung, kann ich bitte noch ein Handtuch bekommen? Und wie lautet das WLAN-Passwort? Danke!")],
    )
    return paper(
        pid, "A1", 6,
        "Goethe-Format A1 · Modellsatz 6 (etwas schwerer)",
        "考場版 A1 · 第6回（稍難）",
        65,
        [lesen1, lesen2, lesen3, hoeren1, hoeren2, hoeren3, schreiben1, schreiben2, sprechen1, sprechen2, sprechen3],
        difficulty="etwas_schwerer",
    )


# ═══════════════════════════════════════════════════════════════════════════
# A2-g5 · leichter — Schwimmbad / Freizeitbad
# ═══════════════════════════════════════════════════════════════════════════


def a2_g5() -> dict[str, Any]:
    pid = "a2-g5"
    lesen1 = section(
        "lesen1", "lesen", "Lesen Teil 1", "閱讀 Teil 1",
        "Lesen Sie den Medientext.", "閱讀媒體短文。",
        [
            tf(f"{pid}-lesen1", 1, "Viele Leute gehen im Sommer ins Schwimmbad.", True, "文首。", "夏天很多人去泳池。"),
            tf(f"{pid}-lesen1", 2, "Tickets sind immer teuer.", False, "Familienkarten günstiger。", "票一律很貴。"),
            mc(f"{pid}-lesen1", 3, "Was ist praktisch?", ["nur bar", "Online-Ticket", "nur Telefon"], 1, "online kaufen。", "什麼方便？"),
            tf(f"{pid}-lesen1", 4, "Das Bad hat 12 Rutschen.", "nicht", "未提滑水道數量。", "有 12 條滑水道。"),
            mc(f"{pid}-lesen1", 5, "Wann ist oft weniger voll?", ["mittags", "früh morgens", "nie"], 1, "früh morgens。", "何時較空？"),
        ],
        passage=(
            "Stadtmagazin – Sommerbad\n"
            "Viele Leute gehen im Sommer ins Schwimmbad. Online kann man Tickets kaufen. "
            "Familienkarten sind oft günstiger. Früh morgens ist es meist weniger voll."
        ),
        passage_zh="夏天多人去泳池；可線上購票；家庭票較便宜；清晨較不擠。",
    )
    lesen2 = section(
        "lesen2", "lesen", "Lesen Teil 2", "閱讀 Teil 2",
        "Programm / Tafel.", "節目表／佈告。",
        [
            mc(f"{pid}-lesen2", 1, "Wann öffnet das Bad?", ["8:00", "9:00", "10:00"], 1, "9:00。", "幾點開？"),
            mc(f"{pid}-lesen2", 2, "Was kostet Erwachsenenticket?", ["4 €", "6 €", "9 €"], 1, "6 €。", "成人票？"),
            mc(f"{pid}-lesen2", 3, "Wann ist Bahnenschwimmen?", ["Mo 7 Uhr", "Di 18 Uhr", "So 22 Uhr"], 1, "Di 18:00。", "水道游泳？"),
            mc(f"{pid}-lesen2", 4, "Wo ist die Umkleide?", ["EG", "Dach", "Parkplatz"], 0, "EG。", "更衣室？"),
            mc(f"{pid}-lesen2", 5, "Was ist montags?", ["geschlossen", "bis 20 Uhr", "nur Sauna"], 1, "Mo–Fr bis 20 Uhr。", "週一？"),
        ],
        passage=(
            "Freizeitbad Aqua\n"
            "Öffnung: Mo–Fr 9:00–20:00 · Sa/So 9:00–18:00\n"
            "Ticket Erwachsene 6 € · Kind 3,50 €\n"
            "Di 18:00 Bahnenschwimmen · Umkleide EG"
        ),
        passage_zh="Aqua 泳池：平日 9–20、週末 9–18；成人 6 歐；週二 18 點水道；更衣室在一樓。",
    )
    lesen3 = section(
        "lesen3", "lesen", "Lesen Teil 3", "閱讀 Teil 3",
        "Lesen Sie die Korrespondenz.", "閱讀郵件。",
        [
            mc(f"{pid}-lesen3", 1, "Warum schreibt Mira?", ["Beschwerde", "Gruppenkarte", "Job"], 1, "Gruppenkarte。", "為何寫？"),
            mc(f"{pid}-lesen3", 2, "Für welchen Tag?", ["Fr", "Sa", "So"], 1, "Samstag。", "哪天？"),
            mc(f"{pid}-lesen3", 3, "Wie viele Personen?", ["4", "6", "10"], 1, "sechs Personen。", "幾人？"),
            mc(f"{pid}-lesen3", 4, "Wann möchte sie kommen?", ["10 Uhr", "11 Uhr", "15 Uhr"], 1, "um 11 Uhr。", "何時到？"),
            tf(f"{pid}-lesen3", 5, "Sie will bar bezahlen.", True, "bar bezahlen。", "要付現金。"),
        ],
        passage=(
            "Betreff: Gruppenkarte Samstag\n"
            "Guten Tag,\n"
            "ich möchte eine Gruppenkarte für sechs Personen am Samstag reservieren. "
            "Wir kommen um 11 Uhr und zahlen bar.\n"
            "Viele Grüße\nMira Novak"
        ),
        passage_zh="Mira 訂週六六人家庭／團體票，11 點到並付現金。",
    )
    lesen4 = section(
        "lesen4", "lesen", "Lesen Teil 4", "閱讀 Teil 4",
        "Welche Anzeige passt?", "哪則廣告符合？",
        [
            mc(f"{pid}-lesen4", 1, "Sie suchen günstiges Abendschwimmen.", ["A", "B", "C"], 0, "A：Abend ab 4 €。", "便宜晚場？"),
            mc(f"{pid}-lesen4", 2, "Sie möchten Wassergymnastik.", ["A", "B", "C"], 1, "B：Wassergymnastik。", "水中健身？"),
            mc(f"{pid}-lesen4", 3, "Sie suchen Sauna am Sonntag.", ["A", "B", "C"], 2, "C：Sauna So。", "週日三溫暖？"),
            mc(f"{pid}-lesen4", 4, "Welche Aktivität ist kostenlos zum Probieren?", ["A", "B", "C"], 1, "B：Probestunde gratis。", "免費體驗？"),
            mc(f"{pid}-lesen4", 5, "Was ist abends?", ["A", "B", "C"], 0, "A：ab 18 Uhr。", "晚上？"),
        ],
        passage=(
            "A: Abendschwimmen ab 18 Uhr, Ticket 4 €.\n"
            "B: Wassergymnastik Mi 10 Uhr, Probestunde gratis.\n"
            "C: Sauna So 11–17 Uhr, 12 € inkl. Handtuch."
        ),
        passage_zh="A 晚間游泳；B 免費體驗水中健身；C 週日三溫暖。",
    )
    hoeren1 = section(
        "hoeren1", "hoeren", "Hören Teil 1", "聽力 Teil 1",
        "Kurze Situationen.", "短情境。",
        [
            mc(f"{pid}-hoeren1", 1, "Wann öffnet das Bad?", ["8 Uhr", "9 Uhr", "10 Uhr"], 1, "um 9 Uhr。", "開門？"),
            mc(f"{pid}-hoeren1", 2, "Wo Umkleide?", ["links", "rechts", "oben"], 0, "links。", "更衣室？"),
            tf(f"{pid}-hoeren1", 3, "Es gibt noch Spinde frei.", True, "noch Spinde frei。", "還有置物櫃。"),
            mc(f"{pid}-hoeren1", 4, "Was kostet Schließfach?", ["1 €", "2 €", "5 €"], 1, "2 Euro。", "置物櫃？"),
            mc(f"{pid}-hoeren1", 5, "Welches Becken?", ["Kinder", "Sport", "Sprudel"], 1, "Sportbecken。", "哪個池？"),
        ],
        audio_text=(
            "Situation 1: Das Bad öffnet um 9 Uhr. "
            "Situation 2: Die Umkleiden finden Sie links vom Eingang. "
            "Situation 3: Es sind noch Spinde frei. "
            "Situation 4: Ein Schließfach kostet 2 Euro. "
            "Situation 5: Bahnenschwimmen ist im Sportbecken."
        ),
    )
    hoeren2 = section(
        "hoeren2", "hoeren", "Hören Teil 2", "聽力 Teil 2",
        "Gespräch.", "對話。",
        [
            mc(f"{pid}-hoeren2", 1, "Wohin wollen sie?", ["Kino", "Schwimmbad", "Museum"], 1, "ins Schwimmbad。", "去哪？"),
            mc(f"{pid}-hoeren2", 2, "Welcher Tag?", ["Fr", "Sa", "So"], 1, "Samstag。", "哪天？"),
            mc(f"{pid}-hoeren2", 3, "Wie kommen sie?", ["Auto", "Bus", "zu Fuß"], 1, "mit dem Bus。", "怎麼去？"),
            mc(f"{pid}-hoeren2", 4, "Wann treffen?", ["9 Uhr", "10 Uhr", "11 Uhr"], 1, "um 10 Uhr。", "碰面？"),
            mc(f"{pid}-hoeren2", 5, "Wer holt Tickets?", ["Nina", "Paul", "beide"], 0, "Nina。", "誰買票？"),
        ],
        audio_text=(
            "Nina: Lust auf Schwimmbad am Samstag? "
            "Paul: Ja, gerne. Wir fahren um 10 Uhr mit dem Bus. "
            "Nina: Super, ich hole die Tickets online. "
            "Paul: Perfekt!"
        ),
    )
    hoeren3 = section(
        "hoeren3", "hoeren", "Hören Teil 3", "聽力 Teil 3",
        "Durchsage.", "廣播。",
        [
            mc(f"{pid}-hoeren3", 1, "Was ist geschlossen?", ["Kasse", "Rutsche", "Umkleide"], 1, "Rutsche geschlossen。", "關閉？"),
            mc(f"{pid}-hoeren3", 2, "Warum?", ["Reinigung", "Sturm", "Party"], 0, "wegen Reinigung。", "原因？"),
            mc(f"{pid}-hoeren3", 3, "Wann wieder offen?", ["14 Uhr", "16 Uhr", "morgen"], 1, "ab 16 Uhr。", "何時再開？"),
            mc(f"{pid}-hoeren3", 4, "Wo Infos?", ["App", "Kasse", "Parkplatz"], 1, "an der Kasse。", "資訊？"),
        ],
        audio_text=(
            "Liebe Gäste: Die große Rutsche ist wegen Reinigung geschlossen. "
            "Ab 16 Uhr ist sie wieder geöffnet. Informationen bekommen Sie an der Kasse."
        ),
    )
    hoeren4 = section(
        "hoeren4", "hoeren", "Hören Teil 4", "聽力 Teil 4",
        "Kurzes Interview / Meinungen.", "短訪談。",
        [
            tf(f"{pid}-hoeren4", 1, "Jonas geht oft unter der Woche schwimmen.", False, "meist am Wochenende。", "Jonas 平日常去。"),
            tf(f"{pid}-hoeren4", 2, "Er mag Bahnenschwimmen.", True, "gerne Bahnen。", "喜歡水道。"),
            mc(f"{pid}-hoeren4", 3, "Was findet er zu teuer?", ["Bus", "Getränke", "Ticket immer"], 1, "Getränke。", "太貴？"),
            mc(f"{pid}-hoeren4", 4, "Mit wem geht er?", ["allein", "Freunden", "Chef"], 1, "mit Freunden。", "跟誰？"),
        ],
        audio_text=(
            "Jonas: Ich gehe meist am Wochenende schwimmen, gerne Bahnen. "
            "Die Getränke im Bad finde ich oft zu teuer. Ich gehe gerne mit Freunden."
        ),
    )
    schreiben1 = section(
        "schreiben1", "schreiben", "Schreiben Teil 1", "寫作 Teil 1",
        "Schreiben Sie eine E-Mail (ca. 40–50 Wörter).",
        "請寫一封電子郵件（約 40–50 詞）。",
        [
            schreiben_item(
                f"{pid}-schreiben1", 1,
                "Sie möchten mit Freunden ins Freizeitbad. Schreiben Sie an das Bad:\n"
                "• Datum / Uhrzeit\n• Anzahl Personen\n• Fragen Sie nach Gruppenkarte",
                "你想和朋友去泳池。寫信：日期／時間、人數、詢問團體票。",
                40,
                "Guten Tag,\nich möchte am Samstag um 11 Uhr mit fünf Freunden ins Bad kommen. "
                "Gibt es eine Gruppenkarte? Bitte antworten Sie mir.\nViele Grüße\nMira Novak",
                ["日期時間", "人數", "詢問團體票"],
            )
        ],
    )
    schreiben2 = section(
        "schreiben2", "schreiben", "Schreiben Teil 2", "寫作 Teil 2",
        "Schreiben Sie eine kurze Nachricht (ca. 30–40 Wörter).",
        "請寫短訊（約 30–40 詞）。",
        [
            schreiben_item(
                f"{pid}-schreiben2", 1,
                "Sie können nicht zum Schwimmen kommen. Schreiben Sie an Ihren Freund:\n"
                "• Entschuldigung / Grund\n• Neuer Vorschlag\n• Wann melden?",
                "你無法去游泳。寫給朋友：道歉／原因、新提議、何時聯絡。",
                30,
                "Hallo Paul,\nleider kann ich am Samstag nicht schwimmen gehen, weil ich arbeiten muss. "
                "Haben wir Sonntag Zeit? Ich melde mich heute Abend.\nLiebe Grüße\nMira",
                ["道歉原因", "新提議", "聯絡時間"],
            )
        ],
    )
    sprechen1 = section(
        "sprechen1", "sprechen", "Sprechen Teil 1", "口說 Teil 1",
        "Stellen Sie sich vor.", "請自我介紹。",
        [sprechen_item(f"{pid}-sprechen1", 1,
            "Name, Freizeit, Schwimmen / Sport.",
            "名字、休閒、游泳／運動。",
            ["Name", "Hobby", "Wie oft?", "Mit wem?"],
            "Ich heiße Mira. In der Freizeit gehe ich gerne schwimmen, oft am Wochenende mit Freunden.")],
    )
    sprechen2 = section(
        "sprechen2", "sprechen", "Sprechen Teil 2", "口說 Teil 2",
        "Planen Sie etwas.", "一起規劃。",
        [sprechen_item(f"{pid}-sprechen2", 1,
            "Planen Sie einen Badbesuch: Tag, Ticket, Treffpunkt.",
            "規劃去泳池：日期、票、碰面點。",
            ["Wann?", "Ticket online?", "Treffpunkt?", "Wie lange?"],
            "Sollen wir am Samstag um 10 Uhr vor der Kasse treffen? Ich kaufe die Tickets online.")],
    )
    sprechen3 = section(
        "sprechen3", "sprechen", "Sprechen Teil 3", "口說 Teil 3",
        "Ihre Meinung.", "表達意見。",
        [sprechen_item(f"{pid}-sprechen3", 1,
            "Was ist besser: Schwimmbad oder See? Warum?",
            "泳池和湖哪個較好？為什麼？",
            ["Vorteil Bad", "Vorteil See", "Ihre Wahl"],
            "Im Schwimmbad gibt es Umkleiden und Aufsicht. Am See ist es natürlicher. Ich mag beides, aber im Bad fühle ich mich sicherer.")],
    )
    return paper(
        pid, "A2", 5,
        "Goethe-Format A2 · Modellsatz 5 (leichter)",
        "考場版 A2 · 第5回（稍易）",
        90,
        [lesen1, lesen2, lesen3, lesen4, hoeren1, hoeren2, hoeren3, hoeren4, schreiben1, schreiben2, sprechen1, sprechen2, sprechen3],
        difficulty="leichter",
    )


# ═══════════════════════════════════════════════════════════════════════════
# A2-g6 · etwas_schwerer — Handyvertrag / Mobilfunk
# ═══════════════════════════════════════════════════════════════════════════


def a2_g6() -> dict[str, Any]:
    pid = "a2-g6"
    lesen1 = section(
        "lesen1", "lesen", "Lesen Teil 1", "閱讀 Teil 1",
        "Lesen Sie den Medientext.", "閱讀媒體短文。",
        [
            tf(f"{pid}-lesen1", 1, "Viele wechseln den Handyvertrag wegen des Preises.", True, "wegen Preis。", "很多人因價格換約。"),
            tf(f"{pid}-lesen1", 2, "Alle Verträge sind monatlich kündbar ohne Frist.", False, "oft Kündigungsfrist。", "都可隨時解約。"),
            mc(f"{pid}-lesen1", 3, "Was rät der Text?", ["nur teuerste Flat", "Vergleich von Datenvolumen", "kein Internet"], 1, "Datenvolumen vergleichen。", "建議？"),
            tf(f"{pid}-lesen1", 4, "Roaming in der EU ist immer kostenlos ohne Limit.", "nicht", "未寫無限免費用。", "歐盟漫遊永遠無限免費。"),
            mc(f"{pid}-lesen1", 5, "Wo kann man oft sparen?", ["nur im Flugzeug", "beim Online-Vergleich", "nie"], 1, "Online-Vergleich。", "哪裡省？"),
            mc(f"{pid}-lesen1", 6, "Was ist laut Text riskant?", ["Rechnung lesen", "Verträge ohne Datenlimit-Check", "Shop öffnen"], 1, "ohne Datenlimit zu prüfen。", "風險？"),
        ],
        passage=_long(
            """
            Stadtmagazin – Handyvertrag verstehen
            Viele Menschen wechseln den Anbieter, weil der Preis steigt oder das Datenvolumen
            nicht reicht. Vor dem Abschluss sollte man Laufzeit und Kündigungsfrist prüfen.
            Online-Vergleiche helfen, aber man muss auf Kleingedrucktes achten: Drosselung nach
            dem Highspeed-Kontingent ist üblich. Wer viel im Ausland telefoniert, fragt extra
            nach Roaming-Regeln.
            """
        ),
        passage_zh="許多人因價格或流量換約；簽前要看約期與解約期限；線上比較有用但要注意降速條款與漫遊規定。",
    )
    lesen2 = section(
        "lesen2", "lesen", "Lesen Teil 2", "閱讀 Teil 2",
        "Tarife / Tafel.", "資費表。",
        [
            mc(f"{pid}-lesen2", 1, "Welcher Tarif hat 20 GB?", ["A", "B", "C"], 1, "B：20 GB。", "20GB？"),
            mc(f"{pid}-lesen2", 2, "Was kostet Tarif A?", ["9,99 €", "14,99 €", "24,99 €"], 0, "9,99。", "A 多少？"),
            mc(f"{pid}-lesen2", 3, "Welcher hat EU-Roaming inkl.?", ["A", "B", "C"], 2, "C inkl. EU。", "含歐盟漫遊？"),
            mc(f"{pid}-lesen2", 4, "Mindestlaufzeit B?", ["1 Monat", "12 Monate", "24 Monate"], 1, "12 Monate。", "B 最短？"),
            mc(f"{pid}-lesen2", 5, "Wer braucht viel Daten?", ["A", "B", "C"], 2, "C：40 GB。", "流量大？"),
            mc(f"{pid}-lesen2", 6, "Welcher ist am günstigsten?", ["A", "B", "C"], 0, "A 最便宜。", "最便宜？"),
        ],
        passage=(
            "Mobilfunk Shop – Tarife\n"
            "A: 5 GB · 9,99 €/Monat · Laufzeit 1 Monat\n"
            "B: 20 GB · 14,99 €/Monat · Laufzeit 12 Monate\n"
            "C: 40 GB · 24,99 €/Monat · EU-Roaming inkl. · 24 Monate"
        ),
        passage_zh="A 5GB 9.99／月約；B 20GB 14.99／12 月；C 40GB 含歐盟漫遊／24 月。",
    )
    lesen3 = section(
        "lesen3", "lesen", "Lesen Teil 3", "閱讀 Teil 3",
        "Lesen Sie die Korrespondenz.", "閱讀郵件。",
        [
            mc(f"{pid}-lesen3", 1, "Warum schreibt Omar?", ["Beschwerde Daten", "Job", "Hotel"], 0, "zu wenig Daten。", "為何寫？"),
            mc(f"{pid}-lesen3", 2, "Welcher Tarif?", ["A", "B Start", "C"], 1, "Tarif B Start。", "哪個資費？"),
            mc(f"{pid}-lesen3", 3, "Was möchte er?", ["kündigen sofort", "Upgrade auf mehr GB", "nur SIM"], 1, "mehr Datenvolumen。", "想要？"),
            tf(f"{pid}-lesen3", 4, "Er will heute noch den Shop besuchen.", True, "heute Nachmittag。", "今天下午要去門市。"),
            tf(f"{pid}-lesen3", 5, "Die Kundennummer steht in der Mail.", True, "KD-55210。", "有客戶編號。"),
            tf(f"{pid}-lesen3", 6, "Omar verlangt eine Rückzahlung von 100 €.", False, "未要求退 100。", "要求退 100 歐。"),
        ],
        passage=_long(
            """
            Betreff: Datenvolumen Tarif B Start
            Guten Tag, ich habe den Tarif B Start (Kundennummer KD-55210).
            Seit zwei Monaten reicht mein Datenvolumen nicht. Bitte informieren Sie mich
            über ein Upgrade. Ich komme heute Nachmittag in die Filiale Bahnhofstraße.
            Mit freundlichen Grüßen
            Omar Hassan
            """
        ),
        passage_zh="Omar（KD-55210）反映 B Start 流量不夠，詢問升級，今天下午去火車站街門市。",
    )
    lesen4 = section(
        "lesen4", "lesen", "Lesen Teil 4", "閱讀 Teil 4",
        "Welche Anzeige passt?", "哪則廣告符合？",
        [
            mc(f"{pid}-lesen4", 1, "Sie brauchen Prepaid ohne Laufzeit.", ["A", "B", "C"], 0, "A：Prepaid。", "預付？"),
            mc(f"{pid}-lesen4", 2, "Sie wollen Familienvertrag.", ["A", "B", "C"], 1, "B：Familie。", "家庭？"),
            mc(f"{pid}-lesen4", 3, "Sie brauchen Business mit Hotline.", ["A", "B", "C"], 2, "C：Business。", "商務？"),
            mc(f"{pid}-lesen4", 4, "Was ist nur online?", ["A", "B", "C"], 0, "A：nur online。", "僅線上？"),
            mc(f"{pid}-lesen4", 5, "Wo gibt es 24h Hotline?", ["A", "B", "C"], 2, "C。", "24 小時？"),
            mc(f"{pid}-lesen4", 6, "Welche Aktion gilt nur bis Freitag?", ["A", "B", "C"], 1, "B bis Freitag。", "週五前？"),
        ],
        passage=(
            "A: Prepaid Flex – nur online, keine Laufzeit, 8 € Startguthaben.\n"
            "B: Familientarif 3 SIMs – Aktion bis Freitag, Beratung in der Filiale.\n"
            "C: Business Plus – 24h Hotline, Rechnung per E-Mail."
        ),
        passage_zh="A 線上預付；B 家庭三卡週五前優惠；C 商務含 24 小時專線。",
    )
    hoeren1 = section(
        "hoeren1", "hoeren", "Hören Teil 1", "聽力 Teil 1",
        "Kurze Situationen.", "短情境。",
        [
            mc(f"{pid}-hoeren1", 1, "Was kostet der Tarif?", ["9,99", "14,99", "19,99"], 1, "14,99 Euro。", "資費？"),
            mc(f"{pid}-hoeren1", 2, "Wie viele GB?", ["10", "20", "30"], 1, "zwanzig Gigabyte。", "多少 GB？"),
            tf(f"{pid}-hoeren1", 3, "Die Filiale hat samstags geöffnet.", True, "auch samstags。", "週六有開。"),
            mc(f"{pid}-hoeren1", 4, "Kündigungsfrist?", ["1 Monat", "2 Monate", "3 Monate"], 0, "einen Monat。", "解約期？"),
            mc(f"{pid}-hoeren1", 5, "Wo SIM abholen?", ["Post", "Filiale", "Freund"], 1, "in der Filiale。", "SIM？"),
            mc(f"{pid}-hoeren1", 6, "Warum Netz langsam?", ["Störung", "Limit erreicht", "Regen"], 1, "Datenlimit erreicht。", "為何慢？"),
        ],
        audio_text=(
            "Situation 1: Der Tarif kostet 14,99 Euro im Monat. "
            "Situation 2: Sie haben zwanzig Gigabyte Highspeed. "
            "Situation 3: Unsere Filiale hat auch samstags geöffnet. "
            "Situation 4: Die Kündigungsfrist beträgt einen Monat. "
            "Situation 5: Bitte holen Sie die SIM-Karte in der Filiale ab. "
            "Situation 6: Das Internet ist langsam, weil Ihr Datenlimit erreicht ist."
        ),
    )
    hoeren2 = section(
        "hoeren2", "hoeren", "Hören Teil 2", "聽力 Teil 2",
        "Gespräch.", "對話。",
        [
            mc(f"{pid}-hoeren2", 1, "Was möchte die Kundin?", ["neuen Tarif", "nur Handyhülle", "Job"], 0, "Tarif wechseln。", "想做什麼？"),
            mc(f"{pid}-hoeren2", 2, "Problem jetzt?", ["kein Netz", "zu wenig Daten", "Rechnung falsch"], 1, "zu wenig Daten。", "問題？"),
            mc(f"{pid}-hoeren2", 3, "Empfohlener Tarif?", ["A", "B Plus", "C"], 1, "B Plus。", "推薦？"),
            mc(f"{pid}-hoeren2", 4, "Aufpreis?", ["0 €", "5 €", "15 €"], 1, "fünf Euro mehr。", "加價？"),
            mc(f"{pid}-hoeren2", 5, "Ab wann gültig?", ["sofort", "nächster Monat", "nächstes Jahr"], 1, "ab nächstem Monat。", "何時生效？"),
            tf(f"{pid}-hoeren2", 6, "Sie muss ein neues Handy kaufen.", False, "kein neues Handy nötig。", "必須買新手機。"),
        ],
        audio_text=(
            "Kundin: Ich möchte den Tarif wechseln, ich habe zu wenig Daten. "
            "Berater: Dann empfehle ich B Plus – fünf Euro mehr, aber mehr Volumen. "
            "Es gilt ab nächstem Monat. Ein neues Handy brauchen Sie nicht."
        ),
    )
    hoeren3 = section(
        "hoeren3", "hoeren", "Hören Teil 3", "聽力 Teil 3",
        "Durchsage / Ansage.", "廣播／語音。",
        [
            mc(f"{pid}-hoeren3", 1, "Was ist gestört?", ["Festnetz", "Mobilfunknetz Ost", "WLAN Hotel"], 1, "Mobilfunknetz Ost。", "故障？"),
            mc(f"{pid}-hoeren3", 2, "Bis wann Reparatur?", ["12 Uhr", "18 Uhr", "morgen"], 1, "bis 18 Uhr。", "修到幾點？"),
            mc(f"{pid}-hoeren3", 3, "Was sollen Kunden tun?", ["nichts", "WLAN nutzen / später anrufen", "SIM wegwerfen"], 1, "WLAN … später。", "客戶？"),
            mc(f"{pid}-hoeren3", 4, "Hotline?", ["0800 111", "0900 999", "kein Telefon"], 0, "0800 111。", "專線？"),
            tf(f"{pid}-hoeren3", 5, "Die Störung betrifft ganz Deutschland.", False, "Region Ost。", "全國故障。"),
        ],
        audio_text=(
            "Achtung Kunden: Im Mobilfunknetz Ost gibt es eine Störung. "
            "Die Reparatur dauert voraussichtlich bis 18 Uhr. "
            "Bitte nutzen Sie WLAN oder rufen Sie später an unter 0800 111. "
            "Andere Regionen sind nicht betroffen."
        ),
    )
    hoeren4 = section(
        "hoeren4", "hoeren", "Hören Teil 4", "聽力 Teil 4",
        "Kurzes Interview.", "短訪談。",
        [
            tf(f"{pid}-hoeren4", 1, "Lea vergleicht Tarife oft online.", True, "oft online。", "Lea 常線上比較。"),
            tf(f"{pid}-hoeren4", 2, "Sie nimmt immer den teuersten Tarif.", False, "nicht den teuersten。", "總選最貴。"),
            mc(f"{pid}-hoeren4", 3, "Was ist ihr wichtig?", ["nur Farbe", "Preis und Daten", "nur Werbung"], 1, "Preis und Daten。", "重視？"),
            mc(f"{pid}-hoeren4", 4, "Was ärgert sie?", ["Freundlichkeit", "versteckte Kosten", "Öffnungszeiten"], 1, "versteckte Kosten。", "困擾？"),
            mc(f"{pid}-hoeren4", 5, "Tipp von Lea?", ["nie lesen", "Rechnung prüfen", "sofort kündigen immer"], 1, "Rechnung prüfen。", "建議？"),
        ],
        audio_text=(
            "Lea: Ich vergleiche Tarife oft online und nehme nicht immer den teuersten. "
            "Wichtig sind Preis und Datenvolumen. Versteckte Kosten ärgern mich. "
            "Mein Tipp: die Rechnung jeden Monat prüfen."
        ),
    )
    schreiben1 = section(
        "schreiben1", "schreiben", "Schreiben Teil 1", "寫作 Teil 1",
        "Schreiben Sie eine E-Mail (ca. 50–60 Wörter).",
        "請寫電子郵件（約 50–60 詞）。",
        [
            schreiben_item(
                f"{pid}-schreiben1", 1,
                "Ihr Datenvolumen reicht nicht. Schreiben Sie an den Anbieter:\n"
                "• Kundennummer nennen\n• Problem beschreiben\n• Upgrade / Termin in der Filiale fragen",
                "流量不夠。寫給電信商：客戶編號、問題、詢問升級／門市時間。",
                50,
                "Guten Tag,\nich habe die Kundennummer KD-55210 und zu wenig Datenvolumen. "
                "Bitte informieren Sie mich über ein Upgrade. Kann ich morgen um 16 Uhr in die Filiale kommen?\n"
                "Mit freundlichen Grüßen\nOmar Hassan",
                ["客戶編號", "問題說明", "升級或預約"],
            )
        ],
    )
    schreiben2 = section(
        "schreiben2", "schreiben", "Schreiben Teil 2", "寫作 Teil 2",
        "Schreiben Sie eine Nachricht (ca. 40 Wörter).",
        "請寫短訊（約 40 詞）。",
        [
            schreiben_item(
                f"{pid}-schreiben2", 1,
                "Sie können den Filialtermin nicht wahrnehmen. Schreiben Sie an einen Freund, der mitkommt:\n"
                "• Absage / Grund\n• Neuer Vorschlag\n• Bitte um Rückmeldung",
                "你無法赴門市之約。寫給同行朋友：取消／原因、新提議、請回覆。",
                40,
                "Hallo Lea,\nleider kann ich heute nicht in die Filiale, weil ich länger arbeiten muss. "
                "Schaffen wir morgen um 17 Uhr? Bitte schreib kurz zurück.\nGruß Omar",
                ["取消原因", "新時間", "請回覆"],
            )
        ],
    )
    sprechen1 = section(
        "sprechen1", "sprechen", "Sprechen Teil 1", "口說 Teil 1",
        "Stellen Sie sich vor.", "請自我介紹。",
        [sprechen_item(f"{pid}-sprechen1", 1,
            "Name, Handy-Nutzung, was ist Ihnen bei einem Tarif wichtig.",
            "名字、手機使用、資費重視什麼。",
            ["Name", "Wie nutzen?", "Daten?", "Preis?"],
            "Ich heiße Omar. Ich nutze viel mobiles Internet für Navigation und Nachrichten. Bei einem Tarif sind Preis und Datenvolumen wichtig.")],
    )
    sprechen2 = section(
        "sprechen2", "sprechen", "Sprechen Teil 2", "口說 Teil 2",
        "Fragen stellen.", "提問。",
        [sprechen_item(f"{pid}-sprechen2", 1,
            "Fragen Sie im Shop nach einem Tarif.",
            "在門市詢問資費。",
            ["GB?", "Preis?", "Laufzeit?", "Roaming?"],
            "Wie viele Gigabyte hat der Tarif? Was kostet er im Monat? Wie lange ist die Laufzeit? Gibt es EU-Roaming?")],
    )
    sprechen3 = section(
        "sprechen3", "sprechen", "Sprechen Teil 3", "口說 Teil 3",
        "Meinung.", "意見。",
        [sprechen_item(f"{pid}-sprechen3", 1,
            "Prepaid oder Laufzeitvertrag – was finden Sie besser?",
            "預付與約期合約哪個較好？",
            ["Vorteil Prepaid", "Vorteil Vertrag", "Ihre Wahl"],
            "Prepaid ist flexibel, aber oft teurer pro GB. Ein Vertrag kann günstiger sein, wenn man die Laufzeit kennt. Ich wähle nach meinem Bedarf.")],
    )
    return paper(
        pid, "A2", 6,
        "Goethe-Format A2 · Modellsatz 6 (etwas schwerer)",
        "考場版 A2 · 第6回（稍難）",
        90,
        [lesen1, lesen2, lesen3, lesen4, hoeren1, hoeren2, hoeren3, hoeren4, schreiben1, schreiben2, sprechen1, sprechen2, sprechen3],
        difficulty="etwas_schwerer",
    )


# ═══════════════════════════════════════════════════════════════════════════
# B1-g5 · leichter — Ernährung / Kantine / Kochen
# ═══════════════════════════════════════════════════════════════════════════


def b1_g5() -> dict[str, Any]:
    pid = "b1-g5"
    lesen1 = section(
        "lesen1", "lesen", "Lesen Teil 1", "閱讀 Teil 1",
        "Blog/Meinung.", "部落格／意見。",
        [
            mc(f"{pid}-lesen1", 1, "Worum geht es?", ["Autokauf", "Alltagsernährung", "Steuern"], 1, "Alltagsernährung。", "主題？"),
            tf(f"{pid}-lesen1", 2, "Meal-Prep kann Zeit sparen.", True, "Zeit sparen。", "備餐可省時。"),
            mc(f"{pid}-lesen1", 3, "Was kritisiert der Text?", ["Bauern", "nur extreme Diäten", "Kantinen"], 1, "extreme Diäten。", "批評？"),
            tf(f"{pid}-lesen1", 4, "Alle Firmen kochen täglich frisch für alle.", False, "manche Kantinen。", "每家公司都現煮。"),
            mc(f"{pid}-lesen1", 5, "Was wünschen sich viele?", ["mehr Zucker", "gesündere Kantinenangebote", "längere Warteschlangen"], 1, "gesündere Angebote。", "期望？"),
        ],
        passage=_long(
            """
            Blog: Essen ohne Stress
            Viele wollen sich gesünder ernähren, scheitern aber an zu strengen Diäten.
            Oft helfen schon einfache Rezepte, Meal-Prep am Wochenende und eine Kantine
            mit Salat-Option. Extreme Crash-Diäten wirken kurz, führen aber schnell zu
            Frust. Manche Betriebe verbessern ihre Menüs – das senkt die Versuchung,
            jeden Tag Fast Food zu holen. Leser wünschen sich vor allem transparente
            Kennzeichnung und günstige gesunde Gerichte.
            """
        ),
        passage_zh="部落格：不必極端減肥，簡單食譜與週末備餐更有效；部分公司改善餐廳菜單；讀者盼透明標示與平價健康餐。",
    )
    lesen2 = section(
        "lesen2", "lesen", "Lesen Teil 2", "閱讀 Teil 2",
        "Anzeigen zuordnen.", "廣告配對。",
        [
            mc(f"{pid}-lesen2", 1, "Sie möchten veganen Kochkurs abends.", ["A", "B", "C", "D"], 0, "A：vegan abends。", "純素課？"),
            mc(f"{pid}-lesen2", 2, "Sie suchen Mittagsmenü im Büroviertel.", ["A", "B", "C", "D"], 1, "B：Mittagsmenü。", "午餐？"),
            mc(f"{pid}-lesen2", 3, "Sie brauchen Foodsharing-Treffen.", ["A", "B", "C", "D"], 2, "C：Foodsharing。", "食物分享？"),
            mc(f"{pid}-lesen2", 4, "Sie wollen Brotback-Workshop.", ["A", "B", "C", "D"], 3, "D：Brot。", "烘焙？"),
            mc(f"{pid}-lesen2", 5, "Welche ist kostenlos?", ["A", "B", "C", "D"], 2, "C gratis。", "免費？"),
        ],
        passage=(
            "A: Vegan kochen für Einsteiger, Di 19 Uhr, Küche West, 15 €.\n"
            "B: Kantine Mitte Mittagsmenü ab 12 Uhr, Salatbuffet inkl.\n"
            "C: Foodsharing Treffen Do 18 Uhr Markt, Teilnahme gratis.\n"
            "D: Brotback-Workshop Sa 10 Uhr, Anmeldung Bäckerei Holm."
        ),
        passage_zh="A 純素烹飪；B 中午定食含沙拉；C 免費食物分享；D 麵包工作坊。",
    )
    lesen3 = section(
        "lesen3", "lesen", "Lesen Teil 3", "閱讀 Teil 3",
        "Magazinartikel.", "雜誌文章。",
        [
            tf(f"{pid}-lesen3", 1, "Zu viel Zucker beeinflusst die Konzentration.", True, "Konzentration。", "糖影響專注。"),
            tf(f"{pid}-lesen3", 2, "Experten raten zu nur Fast Food.", False, "gegen ständiges Fast Food。", "建議只吃速食。"),
            mc(f"{pid}-lesen3", 3, "Was hilft in der Pause?", ["nur Energy-Drinks", "Wasser und Obst", "nichts"], 1, "Wasser und Obst。", "休息？"),
            tf(f"{pid}-lesen3", 4, "Das Kantinenprojekt lief einen Tag.", False, "acht Wochen。", "只做一天。"),
            mc(f"{pid}-lesen3", 5, "Ergebnis?", ["keine Wirkung", "weniger Nachmittagstief", "mehr Unfälle"], 1, "weniger Tief。", "結果？"),
            tf(f"{pid}-lesen3", 6, "Alle aßen täglich zwei Stunden langsam.", "nicht", "未寫兩小時。", "每天慢吃兩小時。"),
        ],
        passage=_long(
            """
            Magazin: Pause mit Köpfchen
            Wer mittags nur Süßes isst, merkt oft ein Nachmittagstief.
            Experten empfehlen Wasser, Obst und eine echte Pause statt Bildschirm-Essen.
            In einem Betriebstest zeigten Kantinen nach acht Wochen: Wer ausgewogene Menüs
            und Kennzeichnung anbot, berichtete von weniger Müdigkeit am Nachmittag.
            Die Evaluation läuft weiter.
            """
        ),
        passage_zh="午餐過甜易午後低潮；建議水、水果與真正休息；企業餐廳八週測試後午後疲勞減少。",
    )
    lesen4 = section(
        "lesen4", "lesen", "Lesen Teil 4", "閱讀 Teil 4",
        "Schreiben einer Einrichtung.", "機構來信。",
        [
            mc(f"{pid}-lesen4", 1, "Was bietet die Firma?", ["nur Apps", "neue Kantinenkarte", "Autoreparatur"], 1, "Kantinenkarte。", "提供？"),
            mc(f"{pid}-lesen4", 2, "Ab wann gilt sie?", ["sofort gestern", "1. nächsten Monats", "nie"], 1, "ab 1.。", "何時生效？"),
            tf(f"{pid}-lesen4", 3, "Vegetarische Gerichte kosten extra 10 €.", False, "gleicher Preis。", "素食加 10 歐。"),
            mc(f"{pid}-lesen4", 4, "Feedback bis?", ["gestern", "15. des Monats", "nur mündlich"], 1, "bis zum 15.。", "回饋？"),
            mc(f"{pid}-lesen4", 5, "Wo Infos?", ["Parkplatz", "Intranet / Aushang", "Flughafen"], 1, "Intranet。", "資訊？"),
        ],
        passage=_long(
            """
            Personalbüro – Kantine Update
            Liebe Kolleginnen und Kollegen, ab dem 1. des nächsten Monats gilt unsere neue
            Kantinenkarte mit mehr vegetarischen Gerichten zum gleichen Preis.
            Feedback bitte bis zum 15. des Monats im Intranet oder am Aushang.
            """
        ),
        passage_zh="人事室：下月 1 日起新菜單，素食同價；請於每月 15 日前在內網或公佈欄回饋。",
    )
    lesen5 = section(
        "lesen5", "lesen", "Lesen Teil 5", "閱讀 Teil 5",
        "Forum.", "論壇。",
        [
            mc(f"{pid}-lesen5", 1, "Sams Problem?", ["zu viel Sport", "keine Zeit zum Kochen", "kein Job"], 1, "keine Zeit。", "問題？"),
            tf(f"{pid}-lesen5", 2, "Lea empfiehlt nur Fertiggerichte.", False, "Meal-Prep。", "只推調理包。"),
            mc(f"{pid}-lesen5", 3, "Was macht Timo?", ["ignoriert", "Kantinen-Salat", "nur Fast Food"], 1, "Salat in der Kantine。", "Timo？"),
            tf(f"{pid}-lesen5", 4, "Alle lehnen Kennzeichnung ab.", False, "Sam will Kennzeichnung。", "都反對標示。"),
            mc(f"{pid}-lesen5", 5, "Konsens?", ["nie kochen", "kleine Routinen helfen", "nur teure Restaurants"], 1, "kleine Routinen。", "共識？"),
        ],
        passage=(
            "Forum Essen&Job\n"
            "Sam: Ich habe keine Zeit zum Kochen unter der Woche. Tipps?\n"
            "Lea: Sonntags Meal-Prep – zwei Gerichte vorbereiten. Hilft mir mehr als Fertigprodukte.\n"
            "Timo: Ich nehme oft den Salat in der Kantine, wenn es stressig wird.\n"
            "Sam: Danke! Und ja, klare Kennzeichnung in der Kantine würde mir auch helfen."
        ),
        passage_zh="Sam 平日沒時間煮；Lea 建議週末備餐；Timo 忙時吃餐廳沙拉；也提到清楚標示。",
    )
    hoeren1 = section(
        "hoeren1", "hoeren", "Hören Teil 1", "聽力 Teil 1",
        "Interview.", "訪談。",
        [
            mc(f"{pid}-hoeren1", 1, "Thema der Expertin?", ["Steuern", "Alltagsernährung", "Zahnmedizin"], 1, "Ernährung im Alltag。", "主題？"),
            tf(f"{pid}-hoeren1", 2, "Sie rät zu Crash-Diäten.", False, "gegen Crash-Diäten。", "建議極端減肥。"),
            mc(f"{pid}-hoeren1", 3, "Beispiel für Einstieg?", ["Meal-Prep", "nur Süßes", "nichts"], 0, "Meal-Prep。", "入門？"),
            mc(f"{pid}-hoeren1", 4, "Rolle der Kantine?", ["egal", "wichtige Unterstützung", "nur teuer"], 1, "Unterstützung。", "餐廳？"),
            mc(f"{pid}-hoeren1", 5, "Was vermeiden?", ["Wasser", "ständiges Essen vor dem Bildschirm", "Obst"], 1, "vor dem Bildschirm。", "避免？"),
        ],
        audio_text=(
            "Moderatorin: Frau Berger, worum geht es heute? "
            "Expertin: Um Ernährung im Alltag – ohne Crash-Diäten. "
            "Ein guter Einstieg ist Meal-Prep. Die Kantine kann eine wichtige Unterstützung sein. "
            "Was ich rate zu vermeiden: ständig vor dem Bildschirm zu essen."
        ),
    )
    hoeren2 = section(
        "hoeren2", "hoeren", "Hören Teil 2", "聽力 Teil 2",
        "Gespräch am Arbeitsplatz.", "職場對話。",
        [
            mc(f"{pid}-hoeren2", 1, "Wohin gehen sie?", ["Kino", "Kantine", "Sport"], 1, "in die Kantine。", "去哪？"),
            mc(f"{pid}-hoeren2", 2, "Was nimmt Lena?", ["Burger", "Salatmenü", "nur Kaffee"], 1, "Salatmenü。", "Lena？"),
            tf(f"{pid}-hoeren2", 3, "Max will Fast Food holen.", False, "auch Kantine。", "Max 要買速食。"),
            mc(f"{pid}-hoeren2", 4, "Wann zurück?", ["in 20 Min.", "in 1 Std.", "morgen"], 0, "in zwanzig Minuten。", "何時回？"),
            mc(f"{pid}-hoeren2", 5, "Wer zahlt zuerst?", ["Lena", "Max", "Chef"], 1, "Max lädt ein。", "誰先付？"),
        ],
        audio_text=(
            "Lena: Gehen wir in die Kantine? Ich nehme das Salatmenü. "
            "Max: Ja, ich auch – kein Fast Food heute. Ich lade dich ein. "
            "Lena: Danke! In zwanzig Minuten sind wir zurück."
        ),
    )
    hoeren3 = section(
        "hoeren3", "hoeren", "Hören Teil 3", "聽力 Teil 3",
        "Durchsage / Radiobeitrag.", "廣播。",
        [
            mc(f"{pid}-hoeren3", 1, "Was startet nächste Woche?", ["Kochkurs", "Marathon", "Steuerkurs"], 0, "betrieblicher Kochkurs。", "下週？"),
            mc(f"{pid}-hoeren3", 2, "Wie oft?", ["1× Woche", "täglich", "nie"], 0, "einmal pro Woche。", "頻率？"),
            tf(f"{pid}-hoeren3", 3, "Anmeldung nur per Post.", False, "online im Intranet。", "只能郵寄報名。"),
            mc(f"{pid}-hoeren3", 4, "Kosten für Mitarbeitende?", ["0 €", "50 €", "200 €"], 0, "kostenlos。", "費用？"),
            mc(f"{pid}-hoeren3", 5, "Ort?", ["Küche EG", "Parkplatz", "Flughafen"], 0, "Küche im Erdgeschoss。", "地點？"),
        ],
        audio_text=(
            "Betriebsradio: Nächste Woche startet unser betrieblicher Kochkurs, einmal pro Woche. "
            "Er ist für Mitarbeitende kostenlos. Anmeldung online im Intranet. "
            "Treffpunkt ist die Küche im Erdgeschoss."
        ),
    )
    hoeren4 = section(
        "hoeren4", "hoeren", "Hören Teil 4", "聽力 Teil 4",
        "Meinungen.", "意見。",
        [
            mc(f"{pid}-hoeren4", 1, "Was stört Pia an der alten Kantine?", ["zu laut", "wenig Gemüse", "zu teuer immer"], 1, "wenig Gemüse。", "困擾？"),
            tf(f"{pid}-hoeren4", 2, "Ben kocht jeden Tag drei Stunden.", False, "oft Meal-Prep。", "每天煮三小時。"),
            mc(f"{pid}-hoeren4", 3, "Konsens?", ["nur Fast Food", "Auswahl und Kennzeichnung", "Kantinen abschaffen"], 1, "Auswahl und Kennzeichnung。", "共識？"),
            mc(f"{pid}-hoeren4", 4, "Was will Pia als Nächstes?", ["Feedback geben", "kündigen", "nichts"], 0, "Feedback geben。", "下一步？"),
        ],
        audio_text=(
            "Pia: Früher gab es in der Kantine zu wenig Gemüse. "
            "Ben: Ich mache oft Meal-Prep, aber Auswahl und Kennzeichnung in der Kantine helfen trotzdem. "
            "Pia: Genau – ich gebe nächste Woche Feedback im Intranet."
        ),
    )
    schreiben1 = section(
        "schreiben1", "schreiben", "Schreiben Teil 1", "寫作 Teil 1",
        "E-Mail an die Kantinenleitung (ca. 80 Wörter).",
        "寫給餐廳負責人（約 80 詞）。",
        [
            schreiben_item(
                f"{pid}-schreiben1", 1,
                "Schreiben Sie an die Kantine:\n"
                "• Lob für Salatbuffet\n• Wunsch: mehr vegetarische warme Gerichte\n• Frage nach Allergenkennzeichnung",
                "寫信：稱讚沙拉吧、希望更多熱素食、詢問過敏原標示。",
                80,
                "Sehr geehrte Damen und Herren,\nvielen Dank für das Salatbuffet – das nutze ich oft. "
                "Könnten Sie bitte mehr warme vegetarische Gerichte anbieten? "
                "Außerdem wäre eine klarere Allergenkennzeichnung hilfreich.\n"
                "Mit freundlichen Grüßen\nSam Lee",
                ["稱讚", "素食願望", "過敏原"],
            )
        ],
    )
    schreiben2 = section(
        "schreiben2", "schreiben", "Schreiben Teil 2", "寫作 Teil 2",
        "Forumsbeitrag (ca. 80 Wörter).",
        "論壇短文（約 80 詞）。",
        [
            schreiben_item(
                f"{pid}-schreiben2", 1,
                "Thema: Gesundes Essen trotz wenig Zeit. Schreiben Sie Ihre Meinung mit Beispiel.",
                "主題：時間少仍想吃得健康——寫意見並舉例。",
                80,
                "Ich finde Meal-Prep am Sonntag praktisch: Ich koche zwei Gerichte und nehme Reste mit. "
                "In stressigen Wochen helfe ich mir mit dem Kantinen-Salat. "
                "Wichtig ist für mich eine Routine, keine perfekte Diät.",
                ["意見", "例子", "約 80 詞"],
            )
        ],
    )
    sprechen1 = section(
        "sprechen1", "sprechen", "Sprechen Teil 1", "口說 Teil 1",
        "Kurzvortrag.", "短講。",
        [sprechen_item(f"{pid}-sprechen1", 1,
            "Erklären Sie, wie Sie sich unter der Woche ernähren.",
            "說明你平日如何飲食。",
            ["Frühstück", "Mittag", "Abend", "Snack"],
            "Unter der Woche frühstücke ich schnell, mittags oft in der Kantine, abends etwas Leichtes. Snacks versuche ich zu planen.")],
    )
    sprechen2 = section(
        "sprechen2", "sprechen", "Sprechen Teil 2", "口說 Teil 2",
        "Diskussion.", "討論。",
        [sprechen_item(f"{pid}-sprechen2", 1,
            "Diskutieren Sie: Sollte die Firma gesundes Essen subventionieren?",
            "討論：公司該不該補貼健康餐？",
            ["Pro", "Contra", "Kompromiss"],
            "Pro: Gesundheit und Konzentration. Contra: Kosten. Kompromiss: Zuschuss für ausgewogene Menüs.")],
    )
    sprechen3 = section(
        "sprechen3", "sprechen", "Sprechen Teil 3", "口說 Teil 3",
        "Gemeinsam planen.", "一起規劃。",
        [sprechen_item(f"{pid}-sprechen3", 1,
            "Planen Sie einen Kochabend mit Freunden.",
            "和朋友規劃烹飪之夜。",
            ["Menü", "Einkauf", "Zeit", "wer kocht"],
            "Wir kochen Pasta und Salat. Ich kaufe ein, du kochst, wir starten um 18 Uhr.")],
    )
    return paper(
        pid, "B1", 5,
        "Goethe-Format B1 · Modellsatz 5 (leichter)",
        "考場版 B1 · 第5回（稍易）",
        150,
        [lesen1, lesen2, lesen3, lesen4, lesen5, hoeren1, hoeren2, hoeren3, hoeren4, schreiben1, schreiben2, sprechen1, sprechen2, sprechen3],
        difficulty="leichter",
    )


# ═══════════════════════════════════════════════════════════════════════════
# B1-g6 · etwas_schwerer — Bewerbung / Vorstellungsgespräch
# ═══════════════════════════════════════════════════════════════════════════


def b1_g6() -> dict[str, Any]:
    pid = "b1-g6"
    lesen1 = section(
        "lesen1", "lesen", "Lesen Teil 1", "閱讀 Teil 1",
        "Blog/Meinung.", "部落格／意見。",
        [
            mc(f"{pid}-lesen1", 1, "Worum geht es?", ["Urlaubsbilder", "Bewerbungsprozess", "Kochen"], 1, "Bewerbung。", "主題？"),
            tf(f"{pid}-lesen1", 2, "Eine klare Motivationslage hilft.", True, "klare Motivation。", "清楚動機有幫助。"),
            mc(f"{pid}-lesen1", 3, "Was kritisiert der Text?", ["alle Firmen", "Standardfloskeln ohne Bezug", "Praktikumsstellen"], 1, "Standardfloskeln。", "批評？"),
            tf(f"{pid}-lesen1", 4, "Referenzen sind immer irrelevant.", False, "können hilfreich sein。", "推薦永遠無用。"),
            mc(f"{pid}-lesen1", 5, "Was rät der Autor vor dem Gespräch?", ["nichts vorbereiten", "Fragen zum Unternehmen vorbereiten", "nur Anzug kaufen"], 1, "Fragen vorbereiten。", "面談前？"),
            mc(f"{pid}-lesen1", 6, "Ton des Textes?", ["panisch", "pragmatisch", "zynisch nur"], 1, "pragmatisch。", "語氣？"),
        ],
        passage=_long(
            """
            Blog: Bewerben ohne Theater
            Viele schreiben Bewerbungen, die wie Kopien klingen. Wer Erfolg haben will,
            sollte Motivation und passende Erfahrungen klar benennen – ohne leere Floskeln.
            Vor dem Gespräch hilft Recherche zum Unternehmen und zwei bis drei eigene Fragen.
            Referenzen können unterstützen, ersetzen aber keine konkrete Leistung. Digitale
            Portfolios sind nützlich, wenn sie aktuell und übersichtlich bleiben.
            """
        ),
        passage_zh="部落格：避免空話，清楚寫動機與經驗；面談前研究公司並準備提問；推薦有幫助但不能取代實績。",
    )
    lesen2 = section(
        "lesen2", "lesen", "Lesen Teil 2", "閱讀 Teil 2",
        "Stellenanzeigen zuordnen.", "職缺配對。",
        [
            mc(f"{pid}-lesen2", 1, "Sie suchen Praktikum Marketing.", ["A", "B", "C", "D"], 0, "A：Marketing Praktikum。", "行銷實習？"),
            mc(f"{pid}-lesen2", 2, "Sie wollen Teilzeit Büro.", ["A", "B", "C", "D"], 1, "B：Teilzeit。", "兼職行政？"),
            mc(f"{pid}-lesen2", 3, "Sie brauchen Remote IT-Support.", ["A", "B", "C", "D"], 2, "C：Remote。", "遠端 IT？"),
            mc(f"{pid}-lesen2", 4, "Sie möchten Ausbildungsplatz Handwerk.", ["A", "B", "C", "D"], 3, "D：Ausbildung。", "技職？"),
            mc(f"{pid}-lesen2", 5, "Welche verlangt Deutsch B1+", ["A", "B", "C", "D"], 0, "A：B1+。", "要 B1+？"),
            mc(f"{pid}-lesen2", 6, "Welche startet sofort?", ["A", "B", "C", "D"], 1, "B sofort。", "立刻上班？"),
        ],
        passage=(
            "A: Praktikum Marketing 3 Monate, Deutsch B1+, Start Sept., Bewerbung bis 15.06.\n"
            "B: Büroassistenz Teilzeit 20 Std., sofort, Erfahrung mit Excel erwünscht.\n"
            "C: IT-Support Remote, flexible Zeiten, Englisch C1, Homeoffice.\n"
            "D: Ausbildung Schreiner/in, Beginn Aug., Bewerbung mit Zeugnissen."
        ),
        passage_zh="A 行銷實習需 B1+；B 兼職行政立刻；C 遠端 IT；D 木工學徒。",
    )
    lesen3 = section(
        "lesen3", "lesen", "Lesen Teil 3", "閱讀 Teil 3",
        "Magazinartikel.", "雜誌文章。",
        [
            tf(f"{pid}-lesen3", 1, "Probezeit dient auch dem Kennenlernen.", True, "Kennenlernen。", "試用期也是互相認識。"),
            tf(f"{pid}-lesen3", 2, "Feedbackgespräche sind überflüssig.", False, "wichtig。", "回饋多餘。"),
            mc(f"{pid}-lesen3", 3, "Was hilft neuen Mitarbeitenden?", ["Isolation", "Onboarding-Plan", "nur E-Mails"], 1, "Onboarding。", "幫助新人？"),
            tf(f"{pid}-lesen3", 4, "Die Studie umfasste nur einen Tag.", False, "sechs Monate。", "只做一天。"),
            mc(f"{pid}-lesen3", 5, "Ergebnis?", ["höhere Abbrüche ohne Mentoring", "kein Effekt", "weniger Bewerbungen nötig"], 0, "höhere Abbrüche。", "結果？"),
            mc(f"{pid}-lesen3", 6, "Was wird empfohlen?", ["Mentoring und klare Ziele", "nur Überstunden", "keine Fragen"], 0, "Mentoring。", "建議？"),
            tf(f"{pid}-lesen3", 7, "Alle Firmen hatten denselben Lohn.", "nicht", "未提薪資一致。", "薪資都一樣。"),
        ],
        passage=_long(
            """
            Magazin: Ankommen im Job
            Die Probezeit ist keine reine Prüfung, sondern ein gegenseitiges Kennenlernen.
            Betriebe mit strukturiertem Onboarding und Mentoring verzeichnen laut einer
            sechsmonatigen Erhebung weniger Abbrüche. Regelmäßige Feedbackgespräche und
            klare Ziele für die ersten Wochen senken Unsicherheit. Wer nur Aufgaben
            „nebenbei“ erklärt, riskiert Frustration auf beiden Seiten.
            """
        ),
        passage_zh="試用期是互相認識；有結構入職與導師的公司六個月內離職較少；定期回饋與清楚目標可降低不安。",
    )
    lesen4 = section(
        "lesen4", "lesen", "Lesen Teil 4", "閱讀 Teil 4",
        "Einladungsschreiben.", "邀請信。",
        [
            mc(f"{pid}-lesen4", 1, "Wozu wird eingeladen?", ["Party", "Vorstellungsgespräch", "Sport"], 1, "Vorstellungsgespräch。", "邀請？"),
            mc(f"{pid}-lesen4", 2, "Wann?", ["Mo 9 Uhr", "Di 10:30", "Fr 18 Uhr"], 1, "Dienstag 10:30。", "何時？"),
            tf(f"{pid}-lesen4", 3, "Man soll Zeugnisse mitbringen.", True, "Zeugnisse mitbringen。", "要帶成績／證書。"),
            mc(f"{pid}-lesen4", 4, "Dauer ca.?", ["10 Min.", "45 Min.", "5 Std."], 1, "45 Minuten。", "多久？"),
            mc(f"{pid}-lesen4", 5, "Wo?", ["Online only", "Raum 3.12 HQ", "Bahnhof"], 1, "Raum 3.12。", "地點？"),
            tf(f"{pid}-lesen4", 6, "Absage ist per SMS an die private Handynummer der Chefin erwünscht.", False, "per E-Mail an HR。", "用簡訊私訊老闆娘。"),
        ],
        passage=_long(
            """
            Firma Nova – Einladung
            Sehr geehrte Frau Park, wir laden Sie zum Vorstellungsgespräch am Dienstag um 10:30
            in Raum 3.12 (HQ) ein. Das Gespräch dauert ca. 45 Minuten. Bitte bringen Sie
            Zeugnisse und einen gültigen Ausweis mit. Bei Verhinderung melden Sie sich bitte
            per E-Mail an hr@nova.example.
            """
        ),
        passage_zh="Nova 邀請 Park 女士週二 10:30 於 3.12 室面談約 45 分鐘；請帶證書與證件；無法出席請寄信 HR。",
    )
    lesen5 = section(
        "lesen5", "lesen", "Lesen Teil 5", "閱讀 Teil 5",
        "Forum.", "論壇。",
        [
            mc(f"{pid}-lesen5", 1, "Ninas Problem?", ["zu viele Angebote", "Lampenfieber vor dem Gespräch", "kein CV"], 1, "Lampenfieber。", "問題？"),
            tf(f"{pid}-lesen5", 2, "Omar rät, Fragen auswendig zu schreien.", False, "laut üben，非喊叫。", "建議大吼。"),
            mc(f"{pid}-lesen5", 3, "Was macht Lea?", ["ignoriert", "Notizen zu Stärken", "kündigt"], 1, "Notizen。", "Lea？"),
            tf(f"{pid}-lesen5", 4, "Alle finden Vorbereitung nutzlos.", False, "finden Vorbereitung sinnvoll。", "都覺得多餘。"),
            mc(f"{pid}-lesen5", 5, "Konsens?", ["nur Glück", "Vorbereitung reduziert Stress", "nie üben"], 1, "Vorbereitung。", "共識？"),
            mc(f"{pid}-lesen5", 6, "Was will Nina als Nächstes?", ["Probe-Interview", "abschicken ohne Lesen", "absagen immer"], 0, "Probe-Interview。", "下一步？"),
        ],
        passage=(
            "Forum JobStart\n"
            "Nina: Ich habe Lampenfieber vor dem Vorstellungsgespräch. Tipps?\n"
            "Omar: Übe Antworten laut, aber natürlich – nicht auswendig schreien.\n"
            "Lea: Ich schreibe drei Stärken und ein Beispiel auf Karteikarten.\n"
            "Nina: Danke! Ich mache morgen ein Probe-Interview mit einer Freundin."
        ),
        passage_zh="Nina 面談緊張；Omar 建議自然練習；Lea 寫下優點例子；Nina 明天要模擬面談。",
    )
    hoeren1 = section(
        "hoeren1", "hoeren", "Hören Teil 1", "聽力 Teil 1",
        "Interview.", "訪談。",
        [
            mc(f"{pid}-hoeren1", 1, "Thema?", ["Kochen", "Vorstellungsgespräche", "Steuern"], 1, "Vorstellungsgespräche。", "主題？"),
            tf(f"{pid}-hoeren1", 2, "Die Expertin rät zu Lügen im CV.", False, "gegen Lügen。", "建議履歷造假。"),
            mc(f"{pid}-hoeren1", 3, "Was vorbereiten?", ["Firmenfragen", "nur Anzugfarbe", "nichts"], 0, "Fragen zum Unternehmen。", "準備？"),
            mc(f"{pid}-hoeren1", 4, "Zum Gehalt?", ["nie sprechen", "realistisch und vorbereitet", "sofort drohen"], 1, "realistisch。", "薪資？"),
            mc(f"{pid}-hoeren1", 5, "Nach dem Gespräch?", ["vergessen", "kurze Dankesmail", "Spam"], 1, "Dankesmail。", "之後？"),
            tf(f"{pid}-hoeren1", 6, "Pünktlichkeit ist egal.", False, "Pünktlichkeit wichtig。", "準時無關。"),
        ],
        audio_text=(
            "Moderator: Frau Keller, Thema heute? "
            "Expertin: Vorstellungsgespräche – ohne Lügen im Lebenslauf. "
            "Bereiten Sie Fragen zum Unternehmen vor und sprechen Sie über Gehalt realistisch. "
            "Nach dem Gespräch hilft eine kurze Dankesmail. Und: Pünktlichkeit ist wichtig."
        ),
    )
    hoeren2 = section(
        "hoeren2", "hoeren", "Hören Teil 2", "聽力 Teil 2",
        "Gespräch HR.", "與人資對話。",
        [
            mc(f"{pid}-hoeren2", 1, "Position?", ["Praktikantin Marketing", "Koch", "Fahrer"], 0, "Praktikum Marketing。", "職位？"),
            mc(f"{pid}-hoeren2", 2, "Beginn?", ["sofort", "1. September", "nächstes Jahr"], 1, "ersten September。", "開始？"),
            tf(f"{pid}-hoeren2", 3, "Homeoffice ist ausgeschlossen.", False, "teilweise Homeoffice möglich。", "完全不能在家。"),
            mc(f"{pid}-hoeren2", 4, "Probezeit?", ["keine", "drei Monate", "zwei Jahre"], 1, "drei Monate。", "試用？"),
            mc(f"{pid}-hoeren2", 5, "Nächster Schritt?", ["Absage", "Assessment Freitag", "Urlaub"], 1, "Assessment am Freitag。", "下一步？"),
            tf(f"{pid}-hoeren2", 6, "Zeugnisse sollen digital vorab geschickt werden.", True, "digital vorab。", "證書先寄電子檔。"),
        ],
        audio_text=(
            "HR: Für das Praktikum Marketing wäre der Start der erste September. "
            "Probezeit drei Monate, teilweise Homeoffice ist möglich. "
            "Nächster Schritt ist ein Assessment am Freitag. "
            "Bitte senden Sie Ihre Zeugnisse digital vorab."
        ),
    )
    hoeren3 = section(
        "hoeren3", "hoeren", "Hören Teil 3", "聽力 Teil 3",
        "Durchsage / Info.", "廣播／資訊。",
        [
            mc(f"{pid}-hoeren3", 1, "Was fällt aus?", ["Assessment A", "Kantine", "Bus"], 0, "Assessment Gruppe A。", "取消？"),
            mc(f"{pid}-hoeren3", 2, "Neuer Termin?", ["Mo 9", "Mi 14 Uhr", "So 20"], 1, "Mittwoch 14 Uhr。", "新時間？"),
            tf(f"{pid}-hoeren3", 3, "Man muss nichts bestätigen.", False, "Bitte bestätigen。", "不用確認。"),
            mc(f"{pid}-hoeren3", 4, "Wo Infos?", ["hr@nova", "Parkplatz", "Taxi"], 0, "E-Mail HR。", "資訊？"),
            mc(f"{pid}-hoeren3", 5, "Grund?", ["Technikproblem Raum", "Party", "Streik weltweit"], 0, "Technikproblem。", "原因？"),
            mc(f"{pid}-hoeren3", 6, "Wer ist betroffen?", ["nur Gruppe A", "alle Städte", "nur Praktikanten 2020"], 0, "Gruppe A。", "誰？"),
        ],
        audio_text=(
            "Achtung Bewerberinnen und Bewerber: Das Assessment Gruppe A fällt wegen eines "
            "Technikproblems im Raum aus. Neuer Termin ist Mittwoch um 14 Uhr. "
            "Bitte bestätigen Sie per E-Mail an hr@nova.example."
        ),
    )
    hoeren4 = section(
        "hoeren4", "hoeren", "Hören Teil 4", "聽力 Teil 4",
        "Erfahrungsberichte.", "經驗分享。",
        [
            mc(f"{pid}-hoeren4", 1, "Was half Ken am meisten?", ["Zufall", "Probe-Interview", "nichts"], 1, "Probe-Interview。", "最有幫助？"),
            tf(f"{pid}-hoeren4", 2, "Mara liest Stellenanzeigen nur einmal diagonal.", False, "genau lesen。", "只斜看一次。"),
            mc(f"{pid}-hoeren4", 3, "Was nervt Mara?", ["Freundlichkeit", "Fragen ohne Bezug zur Stelle", "Pünktlichkeit"], 1, "ohne Bezug。", "困擾？"),
            mc(f"{pid}-hoeren4", 4, "Tipp beider?", ["Vorbereitung und ehrlich bleiben", "übertreiben", "absagen"], 0, "vorbereiten und ehrlich。", "建議？"),
            tf(f"{pid}-hoeren4", 5, "Ken rät, Gehalt nie zu erwähnen.", False, "realistisch ansprechen。", "永遠別提薪資。"),
        ],
        audio_text=(
            "Ken: Ein Probe-Interview hat mir am meisten geholfen. Gehalt kann man realistisch ansprechen. "
            "Mara: Ich lese Stellenanzeigen genau. Fragen ohne Bezug zur Stelle nerven mich. "
            "Beide: Vorbereitung und ehrlich bleiben – das ist der beste Tipp."
        ),
    )
    schreiben1 = section(
        "schreiben1", "schreiben", "Schreiben Teil 1", "寫作 Teil 1",
        "Formelle E-Mail (ca. 100 Wörter).",
        "正式郵件（約 100 詞）。",
        [
            schreiben_item(
                f"{pid}-schreiben1", 1,
                "Bewerbung um ein Praktikum Marketing:\n"
                "• Bezug zur Anzeige\n• Motivation / Erfahrung kurz\n• Anlagen nennen\n• Gesprächsbereitschaft",
                "應徵行銷實習：提及職缺、動機／經驗、附件、願意面談。",
                100,
                "Sehr geehrte Damen und Herren,\nmit Interesse bewerbe ich mich um das Praktikum Marketing. "
                "Ich studiere Kommunikation und habe bereits Social-Media-Inhalte für einen Verein erstellt. "
                "Anbei sende ich Lebenslauf und Zeugnisse. Über eine Einladung zum Gespräch freue ich mich.\n"
                "Mit freundlichen Grüßen\nMina Park",
                ["職缺關聯", "動機經驗", "附件", "面談意願"],
            )
        ],
    )
    schreiben2 = section(
        "schreiben2", "schreiben", "Schreiben Teil 2", "寫作 Teil 2",
        "Forumsbeitrag (ca. 100 Wörter).",
        "論壇短文（約 100 詞）。",
        [
            schreiben_item(
                f"{pid}-schreiben2", 1,
                "Thema: Wie bereitet man sich auf ein Vorstellungsgespräch vor? Meinung + Beispiel.",
                "主題：如何準備面談——意見與例子。",
                100,
                "Ich finde Recherche und Probe-Interviews am hilfreichsten. "
                "Vor meinem letzten Gespräch habe ich drei Stärken mit Beispielen notiert und "
                "Fragen zum Team vorbereitet. Das hat Lampenfieber reduziert, weil ich wusste, "
                "worüber ich sprechen wollte – ohne den Text auswendig zu lernen.",
                ["意見", "例子", "論理"],
            )
        ],
    )
    sprechen1 = section(
        "sprechen1", "sprechen", "Sprechen Teil 1", "口說 Teil 1",
        "Kurzvortrag.", "短講。",
        [sprechen_item(f"{pid}-sprechen1", 1,
            "Stellen Sie Ihren Bildungsweg und ein Praktikumsziel vor.",
            "介紹學歷背景與實習目標。",
            ["Ausbildung/Studium", "Stärken", "Ziel", "Warum Firma"],
            "Ich studiere Kommunikation, arbeite gern im Team und möchte Marketing-Praxis sammeln, besonders Social Media.")],
    )
    sprechen2 = section(
        "sprechen2", "sprechen", "Sprechen Teil 2", "口說 Teil 2",
        "Diskussion.", "討論。",
        [sprechen_item(f"{pid}-sprechen2", 1,
            "Diskutieren Sie: Ist ein Assessment-Center fairer als ein Einzelgespräch?",
            "討論：評量中心是否比一對一面談更公平？",
            ["Pro Assessment", "Contra", "Kompromiss"],
            "Assessment zeigt Teamfähigkeit, kann aber stressig sein. Einzelgespräche sind persönlicher. Ideal ist eine Kombination.")],
    )
    sprechen3 = section(
        "sprechen3", "sprechen", "Sprechen Teil 3", "口說 Teil 3",
        "Planen.", "規劃。",
        [sprechen_item(f"{pid}-sprechen3", 1,
            "Planen Sie die Vorbereitung auf ein Gespräch am Freitag.",
            "規劃週五面談的準備。",
            ["Recherche", "Outfit", "Unterlagen", "Anfahrt"],
            "Mittwoch Recherche, Donnerstag Probe-Interview, Freitag früh Unterlagen checken und rechtzeitig ankommen.")],
    )
    return paper(
        pid, "B1", 6,
        "Goethe-Format B1 · Modellsatz 6 (etwas schwerer)",
        "考場版 B1 · 第6回（稍難）",
        150,
        [lesen1, lesen2, lesen3, lesen4, lesen5, hoeren1, hoeren2, hoeren3, hoeren4, schreiben1, schreiben2, sprechen1, sprechen2, sprechen3],
        difficulty="etwas_schwerer",
    )


# ═══════════════════════════════════════════════════════════════════════════
# B2-g5 · leichter — Städtischer Tourismus / Besucherlenkung
# ═══════════════════════════════════════════════════════════════════════════


def b2_g5() -> dict[str, Any]:
    pid = "b2-g5"
    lesen1 = section(
        "lesen1", "lesen", "Lesen Teil 1", "閱讀 Teil 1",
        "Kommentar.", "評論。",
        [
            mc(f"{pid}-lesen1", 1, "Kernthema?", ["Steuersätze EU", "Besucherlenkung in Städten", "Weltraum"], 1, "Besucherlenkung。", "主題？"),
            tf(f"{pid}-lesen1", 2, "Mehr Touristen bedeuten immer nur Gewinn ohne Kosten.", False, "Kosten für Infrastruktur。", "只有獲利無成本。"),
            mc(f"{pid}-lesen1", 3, "Was schlägt der Text vor?", ["alles sperren", "Zeitfenster und Infos", "nur Kreuzfahrten"], 1, "Zeitfenster。", "建議？"),
            tf(f"{pid}-lesen1", 4, "Anwohnerinteressen werden erwähnt.", True, "Anwohner。", "提到居民。"),
            mc(f"{pid}-lesen1", 5, "Ton?", ["alarmistisch panisch", "abwägend", "reißerisch tabloid"], 1, "abwägend。", "語氣？"),
            tf(f"{pid}-lesen1", 6, "Der Autor lehnt jede Informationstafel ab.", False, "Infos helfen。", "反對任何資訊牌。"),
        ],
        passage=_long(
            """
            Kommentar: Tourismus steuern, nicht nur werben
            Städte profitieren von Besuchern, zahlen aber auch für Reinigung, Verkehr und
            Wohnraumdruck. Statt pauschaler Verbote helfen oft Zeitfenster für Hotspots,
            klare Wegführung und ehrliche Information über Stoßzeiten. Anwohner brauchen
            Mitspracherechte, sonst wächst der Widerstand. Wer nur Marketing maximiert,
            riskiert, dass die Attraktivität der Stadt langfristig sinkt.
            """
        ),
        passage_zh="城市靠觀光獲利也付基礎設施成本；時段分流、動線與尖峰資訊優於一味禁止；居民需有發言權。",
    )
    lesen2 = section(
        "lesen2", "lesen", "Lesen Teil 2", "閱讀 Teil 2",
        "Maßnahmen zuordnen.", "措施配對。",
        [
            mc(f"{pid}-lesen2", 1, "Sie wollen Tickets mit Zeitslot.", ["A", "B", "C", "D"], 0, "A：Zeitslot。", "時段票？"),
            mc(f"{pid}-lesen2", 2, "Sie suchen Anwohnerkarte ÖPNV.", ["A", "B", "C", "D"], 1, "B：Anwohner。", "居民卡？"),
            mc(f"{pid}-lesen2", 3, "Sie brauchen Mehrsprachige Infotafeln.", ["A", "B", "C", "D"], 2, "C：Tafeln。", "多語標示？"),
            mc(f"{pid}-lesen2", 4, "Sie möchten Nachtlärm-Regeln für Bars.", ["A", "B", "C", "D"], 3, "D：Lärm。", "噪音？"),
            mc(f"{pid}-lesen2", 5, "Welche Maßnahme ist digital?", ["A", "B", "C", "D"], 0, "A App/Online。", "數位？"),
        ],
        passage=(
            "A: Altstadt-Zeitslot-Ticket online, max. 90 Min. Hotspot.\n"
            "B: Anwohner-Jahreskarte ÖPNV vergünstigt, Nachweis Meldeadresse.\n"
            "C: Mehrsprachige Infotafeln zu Stoßzeiten an Bahnhof und Hafen.\n"
            "D: Nachtlärm-Verordnung für Bars ab 23 Uhr, Bußgeld bei Verstoß."
        ),
        passage_zh="A 線上時段票；B 居民交通年票；C 多語尖峰資訊；D 酒吧夜間噪音規定。",
    )
    lesen3 = section(
        "lesen3", "lesen", "Lesen Teil 3", "閱讀 Teil 3",
        "Reportage / Studie.", "報導／研究。",
        [
            mc(f"{pid}-lesen3", 1, "Was wurde getestet?", ["Flugverbote weltweit", "Besucherlenkung in Altstadt", "Schulessen"], 1, "Besucherlenkung。", "測試？"),
            mc(f"{pid}-lesen3", 2, "Dauer?", ["1 Tag", "eine Saison", "10 Jahre"], 1, "eine Saison。", "多久？"),
            mc(f"{pid}-lesen3", 3, "Ergebnis Wartezeiten?", ["länger", "kürzer an Hotspots", "unbekannt"], 1, "kürzer。", "等候？"),
            tf(f"{pid}-lesen3", 4, "Alle Geschäfte meldeten Verluste.", False, "gemischt；einige profitierten。", "全部虧損。"),
            mc(f"{pid}-lesen3", 5, "Kritikpunkt?", ["zu viele Daten", "Kommunikation an Gäste unklar", "kein Wetter"], 1, "Kommunikation unklar。", "批評？"),
            mc(f"{pid}-lesen3", 6, "Nächster Schritt?", ["Abbruch", "bessere Beschilderung", "nur Kreuzfahrt"], 1, "Beschilderung。", "下一步？"),
        ],
        passage=_long(
            """
            Reportage: Pilotprojekt Altstadt
            Eine Saison lang lenkte die Stadt Besucher mit Zeitslots und Umleitungen.
            An den Hotspots sanken die Wartezeiten messbar. Einzelhändler abseits der
            Hauptgasse profitierten teils, während Souvenirshops gemischte Zahlen meldeten.
            Kritik: Die Kommunikation an Gäste war anfangs unklar. Als Nächstes sollen
            Beschilderung und App-Hinweise verbessert werden.
            """
        ),
        passage_zh="古城試點一季：時段分流縮短熱點等候；偏巷商家部分受益；初期對旅客溝通不清，下一步改善標示與 App。",
    )
    lesen4 = section(
        "lesen4", "lesen", "Lesen Teil 4", "閱讀 Teil 4",
        "Stellungnahme / Leserbrief.", "聲明／讀者來信。",
        [
            tf(f"{pid}-lesen4", 1, "Die Verfasserin wohnt in der Altstadt.", True, "wohne in der Altstadt。", "住在古城。"),
            mc(f"{pid}-lesen4", 2, "Hauptärger?", ["zu wenig Touristen", "Lärm und Müll abends", "fehlende Cafés"], 1, "Lärm und Müll。", "困擾？"),
            tf(f"{pid}-lesen4", 3, "Sie fordert ein totales Besuchsverbot.", False, "Lenkung statt Verbot。", "要求全面禁止。"),
            mc(f"{pid}-lesen4", 4, "Was unterstützt sie?", ["Zeitslots", "nur Werbeplakate", "mehr Nachtflüge"], 0, "Zeitslots。", "支持？"),
            mc(f"{pid}-lesen4", 5, "An wen adressiert?", ["Tourismusbehörde", "Weltraumamt", "Schule nur"], 0, "Tourismusbehörde。", "寫給？"),
        ],
        passage=_long(
            """
            Leserbrief an die Tourismusbehörde
            Als Anwohnerin der Altstadt begrüße ich Lenkung statt Totalverbot.
            Abends belasten Lärm und Müll unseren Alltag. Zeitslots und klarere Wege
            könnten helfen, wenn sie konsequent kommuniziert werden. Bitte beziehen Sie
            Anwohner frühzeitig ein.
            """
        ),
        passage_zh="古城居民支持分流而非全面禁止；夜間噪音與垃圾是主因；希望時段與動線並及早納入居民意見。",
    )
    lesen5 = section(
        "lesen5", "lesen", "Lesen Teil 5", "閱讀 Teil 5",
        "Forum / Kommentare.", "論壇。",
        [
            tf(f"{pid}-lesen5", 1, "Alex ist Souvenirhändler.", True, "Souvenirladen。", "Alex 賣紀念品。"),
            mc(f"{pid}-lesen5", 2, "Soras Sorge?", ["zu wenig Busse", "Verdrängung von Wohnraum", "kein WLAN"], 1, "Wohnraum。", "Sora？"),
            mc(f"{pid}-lesen5", 3, "Was will Kim?", ["nur Verbote", "Daten zu Stoßzeiten öffentlich", "alles geheim"], 1, "Daten öffentlich。", "Kim？"),
            tf(f"{pid}-lesen5", 4, "Alle lehnen Zeitslots ab.", False, "Alex offen，Sora vorsichtig。", "都反對時段票。"),
            mc(f"{pid}-lesen5", 5, "Konsensrichtung?", ["Kompromiss Lenkung + Wohnschutz", "Maximierung Besucher", "Stadt schließen"], 0, "Kompromiss。", "方向？"),
            mc(f"{pid}-lesen5", 6, "Wer fordert Mitbestimmung?", ["nur Touristen", "Sora / Anwohner", "niemand"], 1, "Sora。", "誰要參與？"),
        ],
        passage=(
            "Forum Stadt&Besuch\n"
            "Alex: Ich habe einen Souvenirladen – Zeitslots ok, wenn Kunden kommen.\n"
            "Sora: Wohnraum darf nicht weiter verdrängt werden. Anwohner müssen mitreden.\n"
            "Kim: Macht Stoßzeit-Daten öffentlich, dann planen Gäste besser.\n"
            "Alex: Einverstanden – Lenkung plus Wohnschutz klingt fair."
        ),
        passage_zh="Alex 開店可接受時段；Sora 憂住房並要求參與；Kim 主張公開尖峰數據；朝分流＋住房保障妥協。",
    )
    hoeren1 = section(
        "hoeren1", "hoeren", "Hören Teil 1", "聽力 Teil 1",
        "Interview.", "訪談。",
        [
            mc(f"{pid}-hoeren1", 1, "Thema?", ["Weltraumtour", "städtischer Tourismus", "Zahnmedizin"], 1, "städtischer Tourismus。", "主題？"),
            tf(f"{pid}-hoeren1", 2, "Die Expertin will alle Touristen verbieten.", False, "steuern，nicht verbieten。", "要全面禁止。"),
            mc(f"{pid}-hoeren1", 3, "Beispielmaßnahme?", ["Zeitslots", "Steuer auf Atmung", "nichts"], 0, "Zeitslots。", "措施？"),
            mc(f"{pid}-hoeren1", 4, "Wer soll einbezogen werden?", ["nur Hotels", "Anwohner und Gewerbe", "nur Influencer"], 1, "Anwohner und Gewerbe。", "誰？"),
            mc(f"{pid}-hoeren1", 5, "Risiko ohne Lenkung?", ["Attraktivität sinkt", "mehr Parks automatisch", "kein Risiko"], 0, "Attraktivität sinkt。", "風險？"),
        ],
        audio_text=(
            "Moderator: Frau Lang, Ihr Thema? "
            "Expertin: Städtischer Tourismus – steuern, nicht pauschal verbieten. "
            "Zeitslots sind ein Beispiel. Anwohner und Gewerbe müssen einbezogen werden. "
            "Ohne Lenkung riskieren Städte, dass ihre Attraktivität sinkt."
        ),
    )
    hoeren2 = section(
        "hoeren2", "hoeren", "Hören Teil 2", "聽力 Teil 2",
        "Podium / Gespräch.", "座談。",
        [
            mc(f"{pid}-hoeren2", 1, "Hotelier will?", ["mehr Nachtlärm", "verlässliche Planung", "Stadt schließen"], 1, "Planung。", "飯店業者？"),
            tf(f"{pid}-hoeren2", 2, "Die Anwohnerin lehnt jede Information ab.", False, "will Infos und Ruhe。", "拒絕一切資訊。"),
            mc(f"{pid}-hoeren2", 3, "Kompromiss?", ["Zeitslots + Lärmregeln", "nur Werbung", "keine Regeln"], 0, "Zeitslots und Lärm。", "妥協？"),
            mc(f"{pid}-hoeren2", 4, "Wer moderiert?", ["Tourismusamt", "Fußballclub", "Flughafen"], 0, "Tourismusamt。", "主持？"),
            mc(f"{pid}-hoeren2", 5, "Nächstes Treffen?", ["nächste Woche", "in 10 Jahren", "nie"], 0, "nächste Woche。", "下次？"),
        ],
        audio_text=(
            "Moderator Tourismusamt: Herr Meier, was brauchen Hotels? "
            "Hotelier: Verlässliche Planung. "
            "Anwohnerin: Wir brauchen Infos und abends mehr Ruhe. "
            "Moderator: Kompromiss könnten Zeitslots und Lärmregeln sein. Nächstes Treffen nächste Woche."
        ),
    )
    hoeren3 = section(
        "hoeren3", "hoeren", "Hören Teil 3", "聽力 Teil 3",
        "Radiobeitrag.", "廣播報導。",
        [
            mc(f"{pid}-hoeren3", 1, "Was startet Samstag?", ["Pilot Zeitslots", "Marathon Verbot", "Schulstreik"], 0, "Pilot。", "週六？"),
            tf(f"{pid}-hoeren3", 2, "Die App zeigt Stoßzeiten.", True, "Stoßzeiten in der App。", "App 顯示尖峰。"),
            mc(f"{pid}-hoeren3", 3, "Wo Infostände?", ["Bahnhof und Hafen", "nur Flughafen", "Wald"], 0, "Bahnhof und Hafen。", "資訊站？"),
            mc(f"{pid}-hoeren3", 4, "Feedback wie?", ["Online-Formular", "nur Fax", "gar nicht"], 0, "Online-Formular。", "回饋？"),
            tf(f"{pid}-hoeren3", 5, "Das Projekt gilt sofort landesweit.", False, "nur Altstadt-Pilot。", "全國立刻實施。"),
        ],
        audio_text=(
            "Radio Stadt: Am Samstag startet der Altstadt-Pilot mit Zeitslots. "
            "Eine App zeigt Stoßzeiten. Infostände stehen am Bahnhof und am Hafen. "
            "Feedback bitte über das Online-Formular. Es handelt sich um einen lokalen Pilot."
        ),
    )
    hoeren4 = section(
        "hoeren4", "hoeren", "Hören Teil 4", "聽力 Teil 4",
        "Meinungen Passanten.", "路人意見。",
        [
            mc(f"{pid}-hoeren4", 1, "Touristin Lara mag?", ["Chaos", "klare Wege", "kein Ticket"], 1, "klare Wege。", "Lara？"),
            tf(f"{pid}-hoeren4", 2, "Anwohner Ben will mehr Nachtlärm.", False, "weniger Lärm。", "要更多噪音。"),
            mc(f"{pid}-hoeren4", 3, "Händlerin Mia?", ["offen für Lenkung", "gegen alle Gäste", "gleichgültig"], 0, "offen。", "Mia？"),
            mc(f"{pid}-hoeren4", 4, "Gemeinsamer Wunsch?", ["Transparenz", "Geheimhaltung", "Verbote ohne Info"], 0, "Transparenz。", "共同？"),
            tf(f"{pid}-hoeren4", 5, "Lara findet Stoßzeit-Infos nutzlos.", False, "findet sie hilfreich。", "Lara 覺得多餘。"),
        ],
        audio_text=(
            "Lara: Als Touristin mag ich klare Wege und Stoßzeit-Infos. "
            "Ben: Als Anwohner will ich abends weniger Lärm. "
            "Mia: Als Händlerin bin ich offen für Lenkung, wenn sie transparent ist."
        ),
    )
    schreiben1 = section(
        "schreiben1", "schreiben", "Schreiben Teil 1", "寫作 Teil 1",
        "Stellungnahme (ca. 150 Wörter).",
        "發表意見（約 150 詞）。",
        [
            schreiben_item(
                f"{pid}-schreiben1", 1,
                "Thema: Sollen Städte Touristenströme aktiv lenken? Argumentieren Sie mit Beispielen.",
                "主題：城市是否應主動分流觀光客？請論證並舉例。",
                150,
                "Städte sollten Touristenströme aktiv lenken. Hotspots ohne Steuerung erzeugen Lärm, "
                "Müll und Wohnungsdruck. Zeitslots und transparente Stoßzeit-Infos entlasten "
                "Anwohner und verbessern das Erlebnis für Gäste. Gleichzeitig muss Gewerbe "
                "verlässlich planen können; pauschale Verbote schaden oft mehr als sie nutzen. "
                "Ein Pilot mit Evaluation und Mitbestimmung ist der pragmatische Weg.",
                ["立場", "論據", "例子", "結論"],
            )
        ],
    )
    schreiben2 = section(
        "schreiben2", "schreiben", "Schreiben Teil 2", "寫作 Teil 2",
        "Formelle E-Mail (ca. 120 Wörter).",
        "正式郵件（約 120 詞）。",
        [
            schreiben_item(
                f"{pid}-schreiben2", 1,
                "Schreiben Sie an die Tourismusbehörde:\n"
                "• Bezug Pilotprojekt\n• Lob / Kritikpunkt\n• konkreten Verbesserungsvorschlag",
                "寫給觀光局：提及試點、優缺點、具體改進建議。",
                120,
                "Sehr geehrte Damen und Herren,\nvielen Dank für den Altstadt-Pilot. Die kürzeren "
                "Wartezeiten sind positiv. Allerdings waren die Hinweise an Gäste anfangs unklar. "
                "Bitte verbessern Sie Beschilderung und App-Texte und beziehen Sie Anwohnerfrüh "
                "ein. Über eine kurze Rückmeldung freue ich mich.\nMit freundlichen Grüßen\nSora Tan",
                ["試點", "優缺", "建議"],
            )
        ],
    )
    sprechen1 = section(
        "sprechen1", "sprechen", "Sprechen Teil 1", "口說 Teil 1",
        "Kurzvortrag.", "短講。",
        [sprechen_item(f"{pid}-sprechen1", 1,
            "Erklären Sie Vor- und Nachteile des Massentourismus in Innenstädten.",
            "說明市中心大量觀光的利弊。",
            ["Vorteile", "Nachteile", "Fazit"],
            "Vorteile sind Einnahmen und Jobs. Nachteile sind Lärm, Müll und Wohnungsdruck. Deshalb braucht es Lenkung.")],
    )
    sprechen2 = section(
        "sprechen2", "sprechen", "Sprechen Teil 2", "口說 Teil 2",
        "Diskussion.", "討論。",
        [sprechen_item(f"{pid}-sprechen2", 1,
            "Diskutieren Sie Zeitslots für Hotspots: sinnvoll oder überreglementiert?",
            "討論熱點時段票：合理還是過度管制？",
            ["Pro", "Contra", "Kompromiss"],
            "Pro: Entlastung. Contra: Bürokratie. Kompromiss: nur an Spitzentagen mit klarer Kommunikation.")],
    )
    return paper(
        pid, "B2", 5,
        "Goethe-Format B2 · Modellsatz 5 (leichter)",
        "考場版 B2 · 第5回（稍易）",
        170,
        [lesen1, lesen2, lesen3, lesen4, lesen5, hoeren1, hoeren2, hoeren3, hoeren4, schreiben1, schreiben2, sprechen1, sprechen2],
        difficulty="leichter",
    )


# ═══════════════════════════════════════════════════════════════════════════
# B2-g6 · etwas_schwerer — KI am Arbeitsplatz / Datenschutz
# ═══════════════════════════════════════════════════════════════════════════


def b2_g6() -> dict[str, Any]:
    pid = "b2-g6"
    lesen1 = section(
        "lesen1", "lesen", "Lesen Teil 1", "閱讀 Teil 1",
        "Kommentar.", "評論。",
        [
            mc(f"{pid}-lesen1", 1, "Kernthema?", ["KI am Arbeitsplatz", "Weinbau", "Sportwetten"], 0, "KI am Arbeitsplatz。", "主題？"),
            tf(f"{pid}-lesen1", 2, "Automatisierung ersetzt laut Text jede menschliche Verantwortung.", False, "Verantwortung bleibt。", "機器取代一切責任。"),
            mc(f"{pid}-lesen1", 3, "Hauptforderung?", ["totale Geheimhaltung", "Transparenz und Mitbestimmung", "Verbote ohne Regeln"], 1, "Transparenz。", "訴求？"),
            tf(f"{pid}-lesen1", 4, "Schulungen werden als irrelevant abgetan.", False, "Schulungen nötig。", "認為訓練無用。"),
            mc(f"{pid}-lesen1", 5, "Risiko bei intransparenten Systemen?", ["Vertrauensverlust", "mehr Urlaub", "kein Risiko"], 0, "Vertrauensverlust。", "風險？"),
            mc(f"{pid}-lesen1", 6, "Stil?", ["sachlich-kritisch", "reißerisch", "rein lyrisch"], 0, "sachlich-kritisch。", "風格？"),
            tf(f"{pid}-lesen1", 7, "Der Autor lehnt jede KI-Nutzung ab.", False, "regeln，nicht pauschal ablehnen。", "全面反對 AI。"),
        ],
        passage=_long(
            """
            Kommentar: KI braucht Regeln, keine Mythen
            Künstliche Intelligenz beschleunigt Abläufe, entscheidet aber nicht „neutral“.
            Wer Scoring, Monitoring oder Textgenerierung einsetzt, muss Zweck, Datenquellen
            und Grenzen erklären. Sonst wächst Misstrauen – intern wie öffentlich.
            Betriebsräte und Datenschutzstellen gehören früh an den Tisch; Schulungen sind
            Pflicht, nicht Bonus. Automatisierung entbindet Führungskräfte nicht von
            Verantwortung für Fehler und Diskriminierungsrisiken.
            """
        ),
        passage_zh="AI 加速流程但非中立；須說明用途、資料與界線；勞資與個資單位應及早參與；訓練是義務；自動化不免除責任。",
    )
    lesen2 = section(
        "lesen2", "lesen", "Lesen Teil 2", "閱讀 Teil 2",
        "Regelungen zuordnen.", "規範配對。",
        [
            mc(f"{pid}-lesen2", 1, "Sie brauchen Opt-out bei Profiling.", ["A", "B", "C", "D"], 0, "A：Opt-out。", "退出剖析？"),
            mc(f"{pid}-lesen2", 2, "Sie suchen Schulungspflicht KI-Tools.", ["A", "B", "C", "D"], 1, "B：Schulung。", "訓練？"),
            mc(f"{pid}-lesen2", 3, "Sie wollen Audit-Logs für Entscheidungen.", ["A", "B", "C", "D"], 2, "C：Logs。", "稽核？"),
            mc(f"{pid}-lesen2", 4, "Sie brauchen Whistleblower-Kanal.", ["A", "B", "C", "D"], 3, "D：Hinweis。", "檢舉？"),
            mc(f"{pid}-lesen2", 5, "Welche betrifft Kundendaten klar?", ["A", "B", "C", "D"], 0, "A Profiling。", "客戶資料？"),
            mc(f"{pid}-lesen2", 6, "Welche ist intern technisch?", ["A", "B", "C", "D"], 2, "C Logs。", "技術內部？"),
        ],
        passage=(
            "A: Richtlinie Profiling: Zweckbindung, Opt-out für Beschäftigte und Kunden.\n"
            "B: Pflichtmodul KI-Kompetenz, 4 Std./Jahr, Nachweis Personalakte.\n"
            "C: Audit-Logs für automatisierte Entscheidungen, Aufbewahrung 12 Monate.\n"
            "D: Geschützter Hinweisgeberkanal bei Missbrauch von Monitoring-Tools."
        ),
        passage_zh="A 剖析與退出；B 每年 AI 訓練；C 自動決策稽核紀錄；D 監控濫用檢舉管道。",
    )
    lesen3 = section(
        "lesen3", "lesen", "Lesen Teil 3", "閱讀 Teil 3",
        "Studie / Report.", "研究報導。",
        [
            mc(f"{pid}-lesen3", 1, "Was untersuchte die Studie?", ["KI-Assistenz im Kundenservice", "Weinlese", "Straßenbau"], 0, "Kundenservice。", "研究？"),
            mc(f"{pid}-lesen3", 2, "Stichprobe?", ["12 Teams", "2 Personen", "ganz EU ohne Zahl"], 0, "zwölf Teams。", "樣本？"),
            mc(f"{pid}-lesen3", 3, "Effekt Bearbeitungszeit?", ["länger", "kürzer bei klaren Fällen", "unmessbar"], 1, "kürzer。", "處理時間？"),
            tf(f"{pid}-lesen3", 4, "Fehlerquote sank in allen Fällen auf null.", False, "sank，aber nicht null；Grenzfälle。", "錯誤歸零。"),
            mc(f"{pid}-lesen3", 5, "Problem?", ["Übernahme ungeprüfter Vorschläge", "kein Strom", "zu viel Urlaub"], 0, "ungeprüft。", "問題？"),
            mc(f"{pid}-lesen3", 6, "Empfehlung?", ["Human-in-the-loop", "alles automatisieren", "Tools verbieten"], 0, "Human-in-the-loop。", "建議？"),
            tf(f"{pid}-lesen3", 7, "Schulung korrelierte mit weniger Blindvertrauen.", True, "Schulung … weniger Blindvertrauen。", "訓練減少盲信。"),
        ],
        passage=_long(
            """
            Studie: Assistenzsysteme im Service
            Zwölf Kundenservice-Teams nutzten sechs Monate KI-Vorschläge für Antworten.
            Bei klaren Standardfällen sank die Bearbeitungszeit spürbar; die Fehlerquote
            ging zurück, blieb aber in Grenzfällen relevant. Kritisch war die ungeprüfte
            Übernahme von Formulierungen. Teams mit verpflichtender Schulung zeigten weniger
            Blindvertrauen. Die Autorinnen empfehlen Human-in-the-loop und sichtbare Unsicherheitswerte.
            """
        ),
        passage_zh="十二組客服用 AI 六個月：標準案加速、錯誤下降但邊界案仍有；未審核套用是問題；受訓組較少盲信，建議人機共決。",
    )
    lesen4 = section(
        "lesen4", "lesen", "Lesen Teil 4", "閱讀 Teil 4",
        "Stellungnahme Betriebsrat.", "企業工會聲明。",
        [
            tf(f"{pid}-lesen4", 1, "Der Betriebsrat lehnt jedes Tool ab.", False, "nicht pauschal ablehnen。", "全面拒絕工具。"),
            mc(f"{pid}-lesen4", 2, "Hauptforderung?", ["Geheimprojekt", "Mitbestimmung vor Roll-out", "nur Marketing"], 1, "Mitbestimmung。", "訴求？"),
            tf(f"{pid}-lesen4", 3, "Monitoring der Leistung per KI ist Thema.", True, "Leistungsmonitoring。", "提到績效監控。"),
            mc(f"{pid}-lesen4", 4, "Was soll dokumentiert werden?", ["Zweck und Datenquellen", "nur Logo", "Geburtstage"], 0, "Zweck und Quellen。", "文件化？"),
            mc(f"{pid}-lesen4", 5, "Ton?", ["kooperativ-kritisch", "feindselig", "gleichgültig"], 0, "kooperativ-kritisch。", "語氣？"),
            tf(f"{pid}-lesen4", 6, "Schulungen werden als Luxus bezeichnet.", False, "als Pflicht。", "訓練被稱奢侈。"),
        ],
        passage=_long(
            """
            Betriebsrat – Stellungnahme KI-Roll-out
            Wir lehnen digitale Tools nicht pauschal ab. Vor dem Roll-out fordern wir
            Mitbestimmung, Dokumentation von Zweck und Datenquellen sowie klare Grenzen
            für Leistungsmonitoring. Schulungen sind Pflicht. Ohne Transparenz fehlt die
            Akzeptanz – das schadet letztlich auch der Produktivität.
            """
        ),
        passage_zh="工會不全面反對；上線前要參與、用途與資料來源文件化、績效監控界線與義務訓練；無透明則缺接受度。",
    )
    lesen5 = section(
        "lesen5", "lesen", "Lesen Teil 5", "閱讀 Teil 5",
        "Diskussionsforum.", "討論論壇。",
        [
            tf(f"{pid}-lesen5", 1, "Nova arbeitet im Support.", True, "im Support。", "Nova 做客服。"),
            mc(f"{pid}-lesen5", 2, "Rils Sorge?", ["zu wenig KI", "intransparente Scores", "kein Kaffee"], 1, "Scores。", "Ril？"),
            mc(f"{pid}-lesen5", 3, "Was schlägt Kim vor?", ["Logs + Unsicherheitsanzeige", "alles geheim", "Tool löschen sofort"], 0, "Logs。", "Kim？"),
            tf(f"{pid}-lesen5", 4, "Alle fordern Totalverbot.", False, "regeln und prüfen。", "都要全面禁止。"),
            mc(f"{pid}-lesen5", 5, "Konsens?", ["Transparenz und Prüfung", "Maximierung Automation", "Ignorieren"], 0, "Transparenz。", "共識？"),
            mc(f"{pid}-lesen5", 6, "Wer erwähnt Schulung?", ["Nova", "nur Bots", "niemand"], 0, "Nova。", "誰提訓練？"),
            mc(f"{pid}-lesen5", 7, "Ton des Threads?", ["konstruktiv", "nur Beleidigung", "off-topic Sport"], 0, "konstruktiv。", "氛圍？"),
        ],
        passage=(
            "Forum Work&AI\n"
            "Nova: Im Support spart die KI Zeit – aber nur mit Schulung.\n"
            "Ril: Mich stören intransparente Scores bei der Fallpriorisierung.\n"
            "Kim: Zeigt Unsicherheitswerte und führt Audit-Logs – dann kann man prüfen.\n"
            "Nova: Genau: Transparenz und menschliche Prüfung, kein Blindflug."
        ),
        passage_zh="Nova 認 AI 省時但需訓練；Ril 憂不透明分數；Kim 主張不確定度與稽核紀錄；共識是透明與人工檢核。",
    )
    hoeren1 = section(
        "hoeren1", "hoeren", "Hören Teil 1", "聽力 Teil 1",
        "Interview.", "訪談。",
        [
            mc(f"{pid}-hoeren1", 1, "Thema?", ["KI und Arbeit", "Kochen", "Tourismus nur"], 0, "KI und Arbeit。", "主題？"),
            tf(f"{pid}-hoeren1", 2, "Die Expertin feiert Blindvertrauen.", False, "warnt vor Blindvertrauen。", "鼓吹盲信。"),
            mc(f"{pid}-hoeren1", 3, "Schlüsselbegriff?", ["Human-in-the-loop", "Totalautomation", "Zufall"], 0, "Human-in-the-loop。", "關鍵？"),
            mc(f"{pid}-hoeren1", 4, "Wer früh einbeziehen?", ["Datenschutz / Betriebsrat", "nur Marketing", "niemand"], 0, "Datenschutz。", "誰？"),
            mc(f"{pid}-hoeren1", 5, "Schulung?", ["Pflicht", "Hobby", "verboten"], 0, "Pflicht。", "訓練？"),
            tf(f"{pid}-hoeren1", 6, "Verantwortung bleibt bei Menschen.", True, "bleibt bei Menschen。", "責任在人。"),
        ],
        audio_text=(
            "Moderator: Frau Ortega, Ihr Thema? "
            "Expertin: KI und Arbeit. Ich warne vor Blindvertrauen. "
            "Schlüssel ist Human-in-the-loop. Datenschutz und Betriebsrat früh einbeziehen. "
            "Schulungen sind Pflicht. Die Verantwortung bleibt bei Menschen."
        ),
    )
    hoeren2 = section(
        "hoeren2", "hoeren", "Hören Teil 2", "聽力 Teil 2",
        "Podium.", "座談。",
        [
            mc(f"{pid}-hoeren2", 1, "IT-Leiter will?", ["schnellen Nutzen", "kein Logging", "Geheimprojekt"], 0, "schnellen Nutzen。", "IT？"),
            tf(f"{pid}-hoeren2", 2, "Datenschutz will Zweckbindung.", True, "Zweckbindung。", "要目的限定。"),
            mc(f"{pid}-hoeren2", 3, "Betriebsrat betont?", ["Mitbestimmung", "nur Feiern", "Abschaffung PC"], 0, "Mitbestimmung。", "工會？"),
            mc(f"{pid}-hoeren2", 4, "Kompromiss?", ["Pilot mit Evaluation", "sofort überall", "Abbruch"], 0, "Pilot。", "妥協？"),
            mc(f"{pid}-hoeren2", 5, "Nächster Schritt?", ["Risikoanalyse", "Party", "Löschen aller Daten blind"], 0, "Risikoanalyse。", "下一步？"),
            tf(f"{pid}-hoeren2", 6, "Alle lehnen Evaluation ab.", False, "wollen Evaluation。", "都反對評估。"),
        ],
        audio_text=(
            "IT-Leiter: Wir wollen schnellen Nutzen. "
            "Datenschutz: Aber mit Zweckbindung und klaren Logs. "
            "Betriebsrat: Mitbestimmung vor dem Roll-out. "
            "Moderatorin: Also ein Pilot mit Evaluation und vorheriger Risikoanalyse."
        ),
    )
    hoeren3 = section(
        "hoeren3", "hoeren", "Hören Teil 3", "聽力 Teil 3",
        "Radiobeitrag.", "廣播。",
        [
            mc(f"{pid}-hoeren3", 1, "Was startet Montag?", ["KI-Pilot Support", "Festival", "Streik weltweit"], 0, "KI-Pilot。", "週一？"),
            tf(f"{pid}-hoeren3", 2, "Unsicherheitswerte werden angezeigt.", True, "Unsicherheitswerte。", "顯示不確定度。"),
            mc(f"{pid}-hoeren3", 3, "Wer muss geschult werden?", ["alle Pilot-Teams", "nur Praktikanten", "niemand"], 0, "Pilot-Teams。", "誰受訓？"),
            mc(f"{pid}-hoeren3", 4, "Feedbackkanal?", ["Intranet-Form", "nur Fax", "gar nicht"], 0, "Intranet。", "回饋？"),
            tf(f"{pid}-hoeren3", 5, "Der Pilot gilt sofort für die ganze Konzernwelt.", False, "zwei Abteilungen。", "立刻全集團。"),
            mc(f"{pid}-hoeren3", 6, "Dauer Pilot?", ["acht Wochen", "acht Jahre", "ein Tag"], 0, "acht Wochen。", "多久？"),
        ],
        audio_text=(
            "Betriebsradio: Montag startet der KI-Pilot im Support in zwei Abteilungen, acht Wochen. "
            "Unsicherheitswerte werden angezeigt. Alle Pilot-Teams müssen vorher geschult werden. "
            "Feedback läuft über ein Intranet-Formular."
        ),
    )
    hoeren4 = section(
        "hoeren4", "hoeren", "Hören Teil 4", "聽力 Teil 4",
        "Erfahrungsberichte.", "經驗。",
        [
            mc(f"{pid}-hoeren4", 1, "Was half Mira?", ["Checkliste vor Senden", "Blindklick", "nichts"], 0, "Checkliste。", "Mira？"),
            tf(f"{pid}-hoeren4", 2, "Jonas ignoriert Unsicherheitswerte.", False, "achtet darauf。", "Jonas 忽略。"),
            mc(f"{pid}-hoeren4", 3, "Was stört Lea?", ["intransparente Scores", "zu viel Kaffee", "Öffnungszeiten"], 0, "Scores。", "Lea？"),
            mc(f"{pid}-hoeren4", 4, "Gemeinsamer Tipp?", ["prüfen statt blind übernehmen", "alles glauben", "Tool löschen"], 0, "prüfen。", "建議？"),
            tf(f"{pid}-hoeren4", 5, "Mira hält Schulung für überflüssig.", False, "Schulung war zentral。", "Mira 覺得多餘。"),
            mc(f"{pid}-hoeren4", 6, "Ton?", ["pragmatisch", "panisch", "gleichgültig"], 0, "pragmatisch。", "語氣？"),
        ],
        audio_text=(
            "Mira: Eine Checkliste vor dem Senden und die Schulung waren zentral. "
            "Jonas: Ich achte auf Unsicherheitswerte, bevor ich übernehme. "
            "Lea: Intransparente Scores stören mich. "
            "Alle: Prüfen statt blind übernehmen – das ist der Tipp."
        ),
    )
    schreiben1 = section(
        "schreiben1", "schreiben", "Schreiben Teil 1", "寫作 Teil 1",
        "Erörterung (ca. 180 Wörter).",
        "論說文（約 180 詞）。",
        [
            schreiben_item(
                f"{pid}-schreiben1", 1,
                "Thema: Soll KI am Arbeitsplatz stärker reguliert werden? Erörtern Sie Pro/Contra und beziehen Sie Stellung.",
                "主題：職場 AI 是否應加強規範？正反論證並表態。",
                180,
                "KI am Arbeitsplatz braucht klare Regeln. Pro: Transparenz schützt vor Diskriminierung "
                "und Blindvertrauen; Mitbestimmung erhöht Akzeptanz. Contra: Überregulierung kann "
                "Innovation bremsen und kleine Teams überfordern. Dennoch überwiegen die Risiken "
                "intransparenter Systeme. Ein Pilot mit Zweckbindung, Audit-Logs, Schulungspflicht "
                "und Human-in-the-loop ist der ausgewogene Weg – nicht Totalverbot, aber auch nicht "
                "laissez-faire.",
                ["正反", "立場", "論據", "結論"],
            )
        ],
    )
    schreiben2 = section(
        "schreiben2", "schreiben", "Schreiben Teil 2", "寫作 Teil 2",
        "Formelle E-Mail (ca. 140 Wörter).",
        "正式郵件（約 140 詞）。",
        [
            schreiben_item(
                f"{pid}-schreiben2", 1,
                "Schreiben Sie an die Geschäftsleitung zum KI-Pilot:\n"
                "• Bezug Ankündigung\n• Forderung Transparenz / Schulung\n• Vorschlag Evaluationkriterien",
                "寫給管理層：提及試點公告、要求透明／訓練、提出評估標準。",
                140,
                "Sehr geehrte Damen und Herren,\nvielen Dank für die Ankündigung des KI-Pilots. "
                "Bitte stellen Sie Zweck, Datenquellen und Unsicherheitsanzeigen transparent dar "
                "und sichern Sie Schulungen vor dem Start zu. Für die Evaluation schlage ich "
                "Fehlerquote, Bearbeitungszeit und Mitarbeiterfeedback vor. Gerne diskutiere ich "
                "Details mit Datenschutz und Betriebsrat.\nMit freundlichen Grüßen\nRil Nguyen",
                ["試點", "透明訓練", "評估"],
            )
        ],
    )
    sprechen1 = section(
        "sprechen1", "sprechen", "Sprechen Teil 1", "口說 Teil 1",
        "Kurzvortrag.", "短講。",
        [sprechen_item(f"{pid}-sprechen1", 1,
            "Erklären Sie Chancen und Risiken von KI am Arbeitsplatz.",
            "說明職場 AI 的機會與風險。",
            ["Chance", "Risiko", "Bedingung"],
            "Chancen sind Tempo und Entlastung. Risiken sind Fehler und Intransparenz. Bedingung: Human-in-the-loop und Schulung.")],
    )
    sprechen2 = section(
        "sprechen2", "sprechen", "Sprechen Teil 2", "口說 Teil 2",
        "Diskussion.", "討論。",
        [sprechen_item(f"{pid}-sprechen2", 1,
            "Diskutieren Sie Leistungsmonitoring per KI: vertretbar oder Grenzüberschreitung?",
            "討論 AI 績效監控：可接受還是越界？",
            ["Pro Kontrolle", "Contra Privatsphäre", "Kompromiss"],
            "Kontrolle kann Qualität sichern, verletzt aber schnell Privatsphäre. Kompromiss: Zweckbindung, Opt-out und Mitbestimmung.")],
    )
    return paper(
        pid, "B2", 6,
        "Goethe-Format B2 · Modellsatz 6 (etwas schwerer)",
        "考場版 B2 · 第6回（稍難）",
        170,
        [lesen1, lesen2, lesen3, lesen4, lesen5, hoeren1, hoeren2, hoeren3, hoeren4, schreiben1, schreiben2, sprechen1, sprechen2],
        difficulty="etwas_schwerer",
    )


def main() -> None:
    data = json.loads(OUT.read_text(encoding="utf-8"))
    papers: list[dict[str, Any]] = data["papers"]

    # Idempotent: drop previous variant2 only
    papers[:] = [p for p in papers if p["id"] not in VARIANT_IDS]

    assert len(papers) == 24, f"expected 24 existing papers before append, got {len(papers)}"

    new_papers = [
        a1_g5(),
        a1_g6(),
        a2_g5(),
        a2_g6(),
        b1_g5(),
        b1_g6(),
        b2_g5(),
        b2_g6(),
    ]

    expected_sections = {"A1": 11, "A2": 13, "B1": 14, "B2": 13}
    expected_dur = {"A1": 65, "A2": 90, "B1": 150, "B2": 170}

    print(f"{'id':8} {'diff':16} {'secs':>4} {'scored':>6} {'dur':>4}")
    print("-" * 44)
    for np in new_papers:
        assert np["format"] == "goethe"
        assert np["difficulty"] in ("leichter", "etwas_schwerer")
        assert all(sec["kind"] != "bausteine" for sec in np["sections"])
        assert len(np["sections"]) == expected_sections[np["level"]], np["id"]
        assert np["durationMin"] == expected_dur[np["level"]], np["id"]
        sc = scored_count(np)
        assert sc >= MIN_SCORED[np["level"]], f"{np['id']} scored {sc} < {MIN_SCORED[np['level']]}"
        print(f"{np['id']:8} {np['difficulty']:16} {len(np['sections']):4} {sc:6} {np['durationMin']:4}")
        papers.append(np)

    data["note"] = NOTE
    data["papers"] = papers
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    ids = [p["id"] for p in papers]
    for vid in VARIANT_IDS:
        assert vid in ids, f"missing {vid}"
    assert len(papers) == 32, f"expected 32 papers, got {len(papers)}"

    # Existing 24 untouched difficulty tags
    for p in papers:
        if p["id"] not in VARIANT_IDS:
            assert p.get("difficulty") in ("standard", "leichter", "etwas_schwerer"), p["id"]

    print("-" * 44)
    print("OK: appended 8 Goethe variants (g5/g6); total papers == 32")
    print("Updated", OUT)


if __name__ == "__main__":
    main()
