#!/usr/bin/env python3
"""Append Goethe-format 稍易／稍難 variant mock exams to exams.json.

- Tags existing compact + goethe papers with difficulty=\"standard\" if missing
- Appends 8 new papers (g3 leichter, g4 etwas_schwerer) for A1–B2
- Does NOT delete or rewrite the existing 16 papers' content
- Idempotent: replaces only the 8 variant ids on re-run
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
    "A1–B2 各兩份練習版＋四份考場版（含同級內稍易／標準／稍難變體；稍易≠下一級簡單，稍難≠上一級）。"
    "聚焦 Lesen＋Hören（TTS 朗讀腳本）＋Schreiben；Sprechen 為選練口說提示，不計入及格門檻。"
    "答完後可對照中文譯文與詳解。非官方試題，僅供練習。"
)

VARIANT_IDS = [
    "a1-g3",
    "a1-g4",
    "a2-g3",
    "a2-g4",
    "b1-g3",
    "b1-g4",
    "b2-g3",
    "b2-g4",
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
# A1-g3 · leichter — Supermarkt / Einkaufen / Wohnung
# ═══════════════════════════════════════════════════════════════════════════


def a1_g3() -> dict[str, Any]:
    pid = "a1-g3"
    lesen1 = section(
        "lesen1",
        "lesen",
        "Lesen Teil 1",
        "閱讀 Teil 1",
        "Lesen Sie die Nachrichten. Kreuzen Sie die richtige Antwort an (a, b oder c).",
        "請閱讀簡訊／郵件，選出正確答案。",
        [
            mc(f"{pid}-lesen1", 1, "Wann öffnet der Supermarkt?", ["7 Uhr", "8 Uhr", "9 Uhr"], 1, "Öffnung um 8 Uhr。", "超市幾點開門？"),
            mc(f"{pid}-lesen1", 2, "Was soll Anna kaufen?", ["Brot und Butter", "Käse und Wein", "Fisch"], 0, "Brot und Butter。", "Anna 要買什麼？"),
            mc(f"{pid}-lesen1", 3, "Wo ist die Wohnung?", ["Bahnhofstraße 5", "Parkstraße 5", "Marktplatz 1"], 0, "Bahnhofstraße 5。", "住哪？"),
            tf(f"{pid}-lesen1", 4, "Der Markt ist am Sonntag geöffnet.", False, "So geschlossen。", "週日有開。"),
            tf(f"{pid}-lesen1", 5, "Paul kommt um 18 Uhr nach Hause.", True, "um 18 Uhr zu Hause。", "Paul 六點回家。"),
        ],
        passage=(
            "E-Mail Supermarkt Frisch an Kundinnen:\n"
            "Hallo! Wir öffnen Mo–Sa um 8 Uhr. Sonntag geschlossen. "
            "Heute: Milch im Angebot.\n\n"
            "SMS von Paul an Anna:\n"
            "Anna, kauf bitte Brot und Butter. Ich bin um 18 Uhr zu Hause.\n\n"
            "WhatsApp von Vermieterin:\n"
            "Ihre neue Wohnung: Bahnhofstraße 5, 2. Stock. Schlüssel ab 14 Uhr."
        ),
        passage_zh="超市週一至六 8 點開、週日休；Paul 請 Anna 買麵包與奶油，六點回家；新住址火車站街 5 號。",
    )
    lesen2 = section(
        "lesen2",
        "lesen",
        "Lesen Teil 2",
        "閱讀 Teil 2",
        "Lesen Sie die Schilder. Welche Aussage passt?",
        "請閱讀告示，選出正確敘述。",
        [
            mc(f"{pid}-lesen2", 1, "Kasse: Was gilt?", ["Nur bar", "Karte und bar", "Nur Online"], 1, "Karte und bar。", "收銀台？"),
            mc(f"{pid}-lesen2", 2, "Obst: Was ist im Angebot?", ["Äpfel", "Ananas", "Avocado"], 0, "Äpfel heute günstig。", "特價水果？"),
            mc(f"{pid}-lesen2", 3, "Parkplatz: Max. Zeit?", ["30 Min.", "1 Stunde", "2 Stunden"], 1, "Max. 1 Stunde。", "停車多久？"),
            mc(f"{pid}-lesen2", 4, "Aufzug: Status?", ["OK", "Außer Betrieb", "Nur Personal"], 1, "AUSSER BETRIEB。", "電梯？"),
            mc(f"{pid}-lesen2", 5, "Tür: Was ist verboten?", ["Hunde", "Taschen", "Fotos"], 0, "Keine Hunde。", "禁止？"),
        ],
        passage=(
            "Kasse 3: Karte und bar willkommen.\n"
            "Obst: Äpfel heute günstig.\n"
            "Parkplatz Kunden: Max. 1 Stunde.\n"
            "Aufzug: AUSSER BETRIEB – bitte Treppe.\n"
            "Eingang: Keine Hunde."
        ),
        passage_zh="可刷卡現金；蘋果特價；停車最多 1 小時；電梯故障；禁止帶狗。",
    )
    lesen3 = section(
        "lesen3",
        "lesen",
        "Lesen Teil 3",
        "閱讀 Teil 3",
        "Lesen Sie den Text. Ja – Nein – Steht nicht im Text.",
        "請閱讀短文，勾選：對、錯、或文中未提及。",
        [
            tf(f"{pid}-lesen3", 1, "Mei wohnt seit einer Woche in der neuen Wohnung.", True, "seit einer Woche。", "Mei 搬來一週。"),
            tf(f"{pid}-lesen3", 2, "Der Supermarkt ist weit weg.", False, "nur fünf Minuten。", "超市很遠。"),
            tf(f"{pid}-lesen3", 3, "Mei kauft oft Brot und Obst.", True, "Brot und Obst。", "常買麵包水果。"),
            tf(f"{pid}-lesen3", 4, "Die Nachbarin heißt Frau Weber.", "nicht", "未提鄰居名字。", "鄰居叫 Weber。"),
            tf(f"{pid}-lesen3", 5, "Am Samstag ist der Markt bis 20 Uhr offen.", True, "bis 20 Uhr。", "週六開到 20 點。"),
        ],
        passage=(
            "Meine neue Wohnung\n"
            "Ich heiße Mei und wohne seit einer Woche in der Bahnhofstraße. "
            "Der Supermarkt ist nur fünf Minuten zu Fuß. Ich kaufe oft Brot und Obst. "
            "Am Samstag ist der Markt bis 20 Uhr offen. Die Nachbarin ist sehr nett."
        ),
        passage_zh="Mei 搬到火車站街一週，超市步行五分鐘，常買麵包水果；週六開到 20 點；鄰居很親切。",
    )
    hoeren1 = section(
        "hoeren1",
        "hoeren",
        "Hören Teil 1",
        "聽力 Teil 1",
        "Sie hören fünf kurze Situationen. Wählen Sie a, b oder c.",
        "您會聽到五則短情境，選 a、b 或 c。",
        [
            mc(f"{pid}-hoeren1", 1, "Was kostet die Milch?", ["1 €", "1,20 €", "2 €"], 1, "1,20 Euro。", "牛奶多少錢？"),
            mc(f"{pid}-hoeren1", 2, "Wo sind die Eier?", ["Regal 2", "Regal 4", "Kasse"], 1, "Regal vier。", "蛋在哪？"),
            mc(f"{pid}-hoeren1", 3, "Wann schließt der Laden?", ["19 Uhr", "20 Uhr", "21 Uhr"], 1, "um 20 Uhr。", "幾點關？"),
            mc(f"{pid}-hoeren1", 4, "Was fehlt noch?", ["Zucker", "Salz", "Öl"], 0, "Zucker。", "還缺什麼？"),
            mc(f"{pid}-hoeren1", 5, "Welches Stockwerk?", ["EG", "1. Stock", "2. Stock"], 0, "Erdgeschoss。", "幾樓？"),
        ],
        audio_text=(
            "Situation 1: Die Milch kostet heute 1,20 Euro. "
            "Situation 2: Die Eier finden Sie in Regal vier. "
            "Situation 3: Unser Laden schließt um 20 Uhr. "
            "Situation 4: Wir brauchen noch Zucker für den Kuchen. "
            "Situation 5: Die Kundentoilette ist im Erdgeschoss neben der Kasse."
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
            mc(f"{pid}-hoeren2", 1, "Was sucht die Frau?", ["Wohnung", "Auto", "Job"], 0, "eine Wohnung。", "找什麼？"),
            mc(f"{pid}-hoeren2", 2, "Wie viele Zimmer?", ["1", "2", "3"], 1, "zwei Zimmer。", "幾房？"),
            mc(f"{pid}-hoeren2", 3, "Wie hoch ist die Miete?", ["450 €", "550 €", "650 €"], 1, "550 Euro。", "租金？"),
            mc(f"{pid}-hoeren2", 4, "Wann kann sie besichtigen?", ["Montag", "Dienstag", "Freitag"], 1, "Dienstag。", "何時看房？"),
        ],
        audio_text=(
            "Frau: Guten Tag, ich suche eine Wohnung. "
            "Mann: Wir haben eine Wohnung mit zwei Zimmern. Die Miete ist 550 Euro. "
            "Frau: Kann ich die Wohnung besichtigen? "
            "Mann: Ja, am Dienstag um 16 Uhr. Bringen Sie bitte Ihren Ausweis mit."
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
            mc(f"{pid}-hoeren3", 1, "Was ist im Angebot?", ["Brot", "Käse", "Wein"], 0, "frisches Brot。", "特價？"),
            mc(f"{pid}-hoeren3", 2, "Bis wann gilt das Angebot?", ["12 Uhr", "14 Uhr", "18 Uhr"], 1, "bis 14 Uhr。", "特價到幾點？"),
            mc(f"{pid}-hoeren3", 3, "Wo ist die Bäckerei?", ["Eingang", "hinten links", "oben"], 1, "hinten links。", "麵包區？"),
            mc(f"{pid}-hoeren3", 4, "Gibt es Parkplätze?", ["Nein", "Ja, vor dem Markt", "Nur für Personal"], 1, "vor dem Markt。", "有停車位？"),
        ],
        audio_text=(
            "Liebe Kunden: Heute gibt es frisches Brot im Angebot bis 14 Uhr. "
            "Die Bäckerei finden Sie hinten links. "
            "Parkplätze gibt es vor dem Markt. Vielen Dank und schönen Tag!"
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
            gap(f"{pid}-schreiben1", 1, "Nachname: ___ (Wang)", "Wang", "姓 Wang。", prompt_zh="姓"),
            gap(f"{pid}-schreiben1", 2, "Vorname: ___ (Mei)", "Mei", "名 Mei。", prompt_zh="名"),
            gap(f"{pid}-schreiben1", 3, "Straße: ___ 5", "Bahnhofstraße", "Bahnhofstraße。", accept=["Bahnhofstrasse", "Bahnhofstraße"], prompt_zh="街名"),
            gap(f"{pid}-schreiben1", 4, "Telefon: ___", "0176123456", "手機號碼。", accept=["0176 123456", "0176-123456"], prompt_zh="電話"),
            gap(f"{pid}-schreiben1", 5, "Zimmer: ___", "2", "兩房。", accept=["zwei", "2 Zimmer"], prompt_zh="房間數"),
            gap(f"{pid}-schreiben1", 6, "Miete: ___ Euro", "550", "550 歐。", prompt_zh="租金"),
        ],
        passage=(
            "Wohnungsanmeldung\n"
            "Nachname: ________\nVorname: ________\n"
            "Adresse: ________ 5\nTelefon: ________\n"
            "Anzahl Zimmer: ________\nMiete: ________ Euro\n"
            "(Hinweis: Wang / Mei / Bahnhofstraße / 0176123456 / 2 / 550)"
        ),
        passage_zh="請依提示填寫：Wang、Mei、Bahnhofstraße、電話、2、550。",
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
                "Sie können nicht zum Einkaufen kommen. Schreiben Sie an Ihren Freund:\n"
                "• Entschuldigung / Grund\n• Was soll er kaufen?\n• Wann sehen Sie sich?",
                "你無法一起去買東西。寫給朋友：道歉／原因、要他買什麼、何時見面？",
                30,
                "Hallo Paul,\nleider kann ich heute nicht einkaufen gehen, weil ich arbeiten muss. "
                "Kauf bitte Milch und Brot. Wir sehen uns morgen um 19 Uhr.\nLiebe Grüße\nMei",
                ["有道歉與原因", "提到要買的東西", "約定見面時間", "約 30 字"],
            )
        ],
    )
    sprechen1 = section(
        "sprechen1", "sprechen", "Sprechen Teil 1", "口說 Teil 1",
        "Stellen Sie sich vor.", "請自我介紹。",
        [sprechen_item(f"{pid}-sprechen1", 1,
            "Stellen Sie sich vor: Name, Herkunft, Wohnort, Einkaufen / Alltag.",
            "自我介紹：名字、出身、住處、購物／日常。",
            ["Name", "Woher?", "Wohnort", "Wo kaufen Sie ein?"],
            "Guten Tag, ich heiße Mei Wang. Ich komme aus Taiwan und wohne in Köln. "
            "Ich kaufe oft im Supermarkt um die Ecke ein.")],
    )
    sprechen2 = section(
        "sprechen2", "sprechen", "Sprechen Teil 2", "口說 Teil 2",
        "Stellen Sie Fragen.", "請依提示提問。",
        [sprechen_item(f"{pid}-sprechen2", 1,
            "Sie möchten Informationen über eine Wohnung. Stellen Sie Fragen.",
            "你想了解一間公寓，請提問。",
            ["Wie viele Zimmer?", "Was kostet die Miete?", "Wo ist sie?", "Wann kann ich besichtigen?"],
            "Wie viele Zimmer hat die Wohnung? Was kostet die Miete? Wo liegt sie? Wann kann ich sie besichtigen?")],
    )
    sprechen3 = section(
        "sprechen3", "sprechen", "Sprechen Teil 3", "口說 Teil 3",
        "Bitten Sie um etwas.", "請提出請求。",
        [sprechen_item(f"{pid}-sprechen3", 1,
            "Bitten Sie eine Verkäuferin um Hilfe: Sie finden die Milch nicht.",
            "請店員幫忙：你找不到牛奶。",
            ["Entschuldigung", "Milch", "Welches Regal?", "Danke"],
            "Entschuldigung, wo finde ich die Milch? Können Sie mir bitte helfen? Vielen Dank.")],
    )
    return paper(
        pid, "A1", 3,
        "Goethe-Format A1 · Modellsatz 3 (leichter)",
        "考場版 A1 · 第3回（稍易）",
        65,
        [lesen1, lesen2, lesen3, hoeren1, hoeren2, hoeren3, schreiben1, schreiben2, sprechen1, sprechen2, sprechen3],
        difficulty="leichter",
    )


# ═══════════════════════════════════════════════════════════════════════════
# A1-g4 · etwas_schwerer — Fitnessstudio / Sportverein
# ═══════════════════════════════════════════════════════════════════════════


def a1_g4() -> dict[str, Any]:
    pid = "a1-g4"
    lesen1 = section(
        "lesen1", "lesen", "Lesen Teil 1", "閱讀 Teil 1",
        "Lesen Sie die Nachrichten. Kreuzen Sie die richtige Antwort an.",
        "請閱讀簡訊／郵件，選出正確答案。",
        [
            mc(f"{pid}-lesen1", 1, "Wann beginnt der Probetraining-Termin?", ["Mo 17 Uhr", "Di 18 Uhr", "Fr 9 Uhr"], 1, "Dienstag um 18 Uhr。", "體驗課何時？"),
            mc(f"{pid}-lesen1", 2, "Was soll Frau Li mitbringen?", ["Handtuch und Sportschuhe", "nur Geld", "Laptop"], 0, "Handtuch und Sportschuhe。", "要帶什麼？"),
            mc(f"{pid}-lesen1", 3, "Wo ist das Studio?", ["Parkstraße 8", "Bahnhof 8", "Markt 1"], 0, "Parkstraße 8。", "健身房在哪？"),
            tf(f"{pid}-lesen1", 4, "Das Studio ist sonntags geschlossen.", False, "auch So 10–14 Uhr。", "週日公休。"),
            tf(f"{pid}-lesen1", 5, "Tom will um 19 Uhr trainieren.", True, "um 19 Uhr trainieren。", "Tom 想七點練。"),
            tf(f"{pid}-lesen1", 6, "Frau Li braucht fürs Probetraining einen Mitgliedsausweis.", False, "僅需毛巾球鞋；未要求會員證。", "體驗課需要會員證。"),
        ],
        passage=(
            "E-Mail Fitnessstudio Aktiv an Frau Li:\n"
            "Sehr geehrte Frau Li,\n"
            "Ihr Probetraining ist am Dienstag um 18 Uhr. Bitte bringen Sie ein Handtuch "
            "und Sportschuhe mit. Adresse: Parkstraße 8. Öffnungszeiten: Mo–Sa 7–22 Uhr, "
            "So 10–14 Uhr. Umkleiden und Duschen sind im Erdgeschoss.\n"
            "Mit freundlichen Grüßen\nTeam Aktiv\n\n"
            "SMS von Tom an Sara:\n"
            "Sara, trainieren wir heute um 19 Uhr? Bring bitte Wasser mit."
        ),
        passage_zh="Aktiv 健身房給李女士：週二 18 點體驗課，帶毛巾與運動鞋，Parkstraße 8；週一至六 7–22、週日 10–14；Tom 約 Sara 19 點訓練。",
    )
    lesen2 = section(
        "lesen2", "lesen", "Lesen Teil 2", "閱讀 Teil 2",
        "Lesen Sie die Schilder. Welche Aussage passt?",
        "請閱讀告示，選出正確敘述。",
        [
            mc(f"{pid}-lesen2", 1, "Umkleide: Was gilt?", ["Handy laut", "Taschen in Spind", "Schuhe anbehalten"], 1, "Taschen in den Spind。", "更衣室規定？"),
            mc(f"{pid}-lesen2", 2, "Kurs Yoga: Wann?", ["Mo 8 Uhr", "Mi 19 Uhr", "So 21 Uhr"], 1, "Mi 19:00 Yoga。", "瑜珈何時？"),
            mc(f"{pid}-lesen2", 3, "Gerät: Status?", ["frei", "defekt", "nur Trainer"], 1, "Außer Betrieb。", "器材？"),
            mc(f"{pid}-lesen2", 4, "Parken: Wie lange?", ["30 Min.", "2 Stunden", "ganzer Tag"], 1, "Max. 2 Stunden。", "停車？"),
            mc(f"{pid}-lesen2", 5, "Was ist im Studio verboten?", ["Wasser trinken", "Rauchen", "Handtuch"], 1, "Rauchen verboten。", "禁止？"),
            mc(f"{pid}-lesen2", 6, "Wer darf den Kursraum zuerst nutzen?", ["alle Gäste", "nur mit Kurskarte", "nur Kinder"], 1, "Nur mit Kurskarte。", "誰可進教室？"),
        ],
        passage=(
            "Umkleide: Bitte Taschen in den Spind. Handy lautlos.\n"
            "Kursplan: Mi 19:00 Yoga · Raum 2 · Nur mit Kurskarte.\n"
            "Laufband 3: AUSSER BETRIEB – bitte anderes Gerät.\n"
            "Parkplatz: Max. 2 Stunden für Mitglieder.\n"
            "Eingang: Rauchen verboten. Bitte Sportschuhe tragen."
        ),
        passage_zh="置物櫃、週三瑜珈需課程卡、跑步機 3 故障、停車最多 2 小時、禁止吸菸。",
    )
    lesen3 = section(
        "lesen3", "lesen", "Lesen Teil 3", "閱讀 Teil 3",
        "Lesen Sie den Text. Ja – Nein – Steht nicht im Text.",
        "請閱讀短文，勾選：對、錯、或文中未提及。",
        [
            tf(f"{pid}-lesen3", 1, "Ken geht dreimal pro Woche ins Studio.", True, "drei Mal pro Woche。", "Ken 一週去三次。"),
            tf(f"{pid}-lesen3", 2, "Das Studio liegt neben dem Bahnhof.", True, "neben dem Bahnhof。", "在車站旁。"),
            tf(f"{pid}-lesen3", 3, "Der Trainer heißt Herr Müller.", True, "Trainer Herr Müller。", "教練是 Müller。"),
            tf(f"{pid}-lesen3", 4, "Ken zahlt 40 Euro im Monat.", "nicht", "未提月費金額。", "月費 40 歐。"),
            tf(f"{pid}-lesen3", 5, "Am Wochenende macht Ken Yoga.", False, "am Wochenende laufe ich；瑜珈是週三。", "週末做瑜珈。"),
            tf(f"{pid}-lesen3", 6, "Ken möchte nächstes Jahr einen Wettkampf machen.", True, "nächstes Jahr … Wettkampf。", "明年想參賽。"),
        ],
        passage=(
            "Mein Sportverein\n"
            "Ich heiße Ken und gehe drei Mal pro Woche ins Fitnessstudio Aktiv neben dem Bahnhof. "
            "Montags und freitags trainiere ich Kraft, mittwochs mache ich Yoga mit Trainer "
            "Herrn Müller. Er erklärt die Übungen langsam. Am Wochenende laufe ich im Park. "
            "Die Umkleiden sind sauber, aber abends oft voll. Nächstes Jahr möchte ich einen "
            "kleinen Lauf-Wettkampf machen. Ob ich gewinne, weiß ich nicht – wichtig ist, "
            "regelmäßig zu bleiben."
        ),
        passage_zh="Ken 每週三次去車站旁健身房：週一／五重訓、週三跟 Müller 練瑜珈，週末公園跑步；更衣室晚上常滿；明年想參加路跑。",
    )
    hoeren1 = section(
        "hoeren1", "hoeren", "Hören Teil 1", "聽力 Teil 1",
        "Sie hören kurze Situationen.", "短情境聽力。",
        [
            mc(f"{pid}-hoeren1", 1, "Was kostet die Monatskarte?", ["29 €", "39 €", "49 €"], 1, "39 Euro。", "月費？"),
            mc(f"{pid}-hoeren1", 2, "Wann ist Yoga?", ["18 Uhr", "19 Uhr", "20 Uhr"], 1, "um 19 Uhr。", "瑜珈？"),
            mc(f"{pid}-hoeren1", 3, "Wo duschen?", ["1. Stock", "EG", "Keller"], 1, "Erdgeschoss。", "淋浴在哪？"),
            mc(f"{pid}-hoeren1", 4, "Was fehlt Tom?", ["Handtuch", "Schuhe", "Trinkflasche"], 0, "mein Handtuch。", "缺什麼？"),
            mc(f"{pid}-hoeren1", 5, "Bis wann geöffnet?", ["21 Uhr", "22 Uhr", "23 Uhr"], 1, "bis 22 Uhr。", "開到幾點？"),
            mc(f"{pid}-hoeren1", 6, "Warum ist Kursraum 2 zu?", ["Putzen", "Kurs läuft", "Feuer"], 1, "Kurs läuft noch。", "為何關閉？"),
        ],
        audio_text=(
            "Situation 1: Die Monatskarte kostet 39 Euro. "
            "Situation 2: Der Yogakurs beginnt um 19 Uhr. "
            "Situation 3: Die Duschen sind im Erdgeschoss. "
            "Situation 4: Tom, hast du mein Handtuch gesehen? "
            "Situation 5: Das Studio ist heute bis 22 Uhr geöffnet. "
            "Situation 6: Kursraum 2 ist geschlossen, weil der Kurs noch läuft."
        ),
    )
    hoeren2 = section(
        "hoeren2", "hoeren", "Hören Teil 2", "聽力 Teil 2",
        "Sie hören ein Gespräch.", "請聽對話。",
        [
            mc(f"{pid}-hoeren2", 1, "Was möchte die Frau?", ["kündigen", "Mitglied werden", "nur duschen"], 1, "Mitglied werden。", "想做什麼？"),
            mc(f"{pid}-hoeren2", 2, "Probetraining wann?", ["heute", "morgen 17 Uhr", "nächste Woche"], 1, "morgen um 17 Uhr。", "體驗？"),
            mc(f"{pid}-hoeren2", 3, "Was braucht sie?", ["Ausweis", "Arztbrief", "Foto"], 0, "Ihren Ausweis。", "要帶？"),
            mc(f"{pid}-hoeren2", 4, "Gibt es Ermäßigung für Studierende?", ["Nein", "Ja, 10 %", "nur bar"], 1, "zehn Prozent。", "學生優惠？"),
            tf(f"{pid}-hoeren2", 5, "Sie muss heute schon bezahlen.", False, "erst nach dem Probetraining。", "今天就要付錢。"),
        ],
        audio_text=(
            "Frau: Guten Tag, ich möchte Mitglied werden. "
            "Mann: Gerne. Zuerst können Sie morgen um 17 Uhr ein Probetraining machen. "
            "Bitte bringen Sie Ihren Ausweis mit. Für Studierende gibt es zehn Prozent Rabatt. "
            "Frau: Muss ich heute bezahlen? "
            "Mann: Nein, erst nach dem Probetraining, wenn Sie möchten."
        ),
    )
    hoeren3 = section(
        "hoeren3", "hoeren", "Hören Teil 3", "聽力 Teil 3",
        "Sie hören eine Durchsage.", "請聽廣播。",
        [
            mc(f"{pid}-hoeren3", 1, "Was fällt aus?", ["Yoga", "Zumba", "Spinning"], 1, "Zumba fällt aus。", "哪堂取消？"),
            mc(f"{pid}-hoeren3", 2, "Ersatztermin?", ["Do 18 Uhr", "Fr 18 Uhr", "Sa 10 Uhr"], 0, "Donnerstag um 18 Uhr。", "補課？"),
            mc(f"{pid}-hoeren3", 3, "Wo Infos?", ["App", "Rezeption", "Parkplatz"], 1, "an der Rezeption。", "資訊在哪？"),
            mc(f"{pid}-hoeren3", 4, "Sauna heute?", ["geschlossen", "geöffnet", "nur Männer"], 1, "Sauna ist geöffnet。", "三溫暖？"),
            tf(f"{pid}-hoeren3", 5, "Man soll die Kurskarte an der Tür zeigen.", True, "Kurskarte an der Tür zeigen。", "要在門口出示課程卡。"),
        ],
        audio_text=(
            "Achtung Mitglieder: Der Zumba-Kurs heute Abend fällt aus. "
            "Ersatztermin ist Donnerstag um 18 Uhr. Bitte zeigen Sie Ihre Kurskarte an der Tür. "
            "Informationen bekommen Sie an der Rezeption. Die Sauna ist geöffnet."
        ),
    )
    schreiben1 = section(
        "schreiben1", "schreiben", "Schreiben Teil 1", "寫作 Teil 1",
        "Füllen Sie das Formular aus.", "請填寫表格。",
        [
            gap(f"{pid}-schreiben1", 1, "Nachname: ___ (Li)", "Li", "姓 Li。", prompt_zh="姓"),
            gap(f"{pid}-schreiben1", 2, "Vorname: ___ (Hua)", "Hua", "名 Hua。", prompt_zh="名"),
            gap(f"{pid}-schreiben1", 3, "Adresse: ___ 8", "Parkstraße", "Parkstraße。", accept=["Parkstrasse", "Parkstraße"], prompt_zh="街名"),
            gap(f"{pid}-schreiben1", 4, "Telefon: ___", "0151123456", "電話。", accept=["0151 123456"], prompt_zh="電話"),
            gap(f"{pid}-schreiben1", 5, "Kurs: ___", "Yoga", "瑜珈。", prompt_zh="課程"),
            gap(f"{pid}-schreiben1", 6, "Beginn: ___ Uhr", "19", "19 點。", accept=["19:00", "19 Uhr"], prompt_zh="開始"),
        ],
        passage=(
            "Anmeldeformular Fitnessstudio Aktiv\n"
            "Nachname: ________ Vorname: ________\n"
            "Adresse: ________ 8\nTelefon: ________\n"
            "Kurs: ________ Beginn: ________ Uhr\n"
            "(Hinweis: Li / Hua / Parkstraße / 0151123456 / Yoga / 19)"
        ),
        passage_zh="請填：Li、Hua、Parkstraße、電話、Yoga、19。",
    )
    schreiben2 = section(
        "schreiben2", "schreiben", "Schreiben Teil 2", "寫作 Teil 2",
        "Schreiben Sie eine kurze Mitteilung (30–40 Wörter).",
        "請寫短訊（約 30–40 詞）。",
        [
            schreiben_item(
                f"{pid}-schreiben2", 1,
                "Sie können nicht zum Training kommen. Schreiben Sie an Ihren Trainer:\n"
                "• Entschuldigung / Grund\n• Welcher Tag?\n• Wann kommen Sie wieder?",
                "你無法去訓練。寫給教練：道歉／原因、哪一天、何時再來？",
                30,
                "Lieber Herr Müller,\nleider kann ich am Mittwoch nicht zum Yoga kommen, "
                "weil ich krank bin. Nächste Woche bin ich wieder da.\nViele Grüße\nHua Li",
                ["道歉與原因", "缺席日期", "說明何時回來"],
            )
        ],
    )
    sprechen1 = section(
        "sprechen1", "sprechen", "Sprechen Teil 1", "口說 Teil 1",
        "Stellen Sie sich vor.", "請自我介紹。",
        [sprechen_item(f"{pid}-sprechen1", 1,
            "Stellen Sie sich vor: Name, Sport, wie oft, warum.",
            "自我介紹：名字、運動、頻率、原因。",
            ["Name", "Welche Sportart?", "Wie oft?", "Warum?"],
            "Ich heiße Hua Li. Ich mache Yoga und Krafttraining, drei Mal pro Woche, weil ich fit bleiben möchte.")],
    )
    sprechen2 = section(
        "sprechen2", "sprechen", "Sprechen Teil 2", "口說 Teil 2",
        "Stellen Sie Fragen.", "請提問。",
        [sprechen_item(f"{pid}-sprechen2", 1,
            "Fragen Sie an der Rezeption nach einem Fitnesskurs.",
            "在櫃檯詢問健身課程。",
            ["Wann?", "Was kostet?", "Probetraining?", "Was mitbringen?"],
            "Wann beginnt der Kurs? Was kostet die Mitgliedschaft? Gibt es ein Probetraining? Was soll ich mitbringen?")],
    )
    sprechen3 = section(
        "sprechen3", "sprechen", "Sprechen Teil 3", "口說 Teil 3",
        "Bitten Sie um etwas.", "請提出請求。",
        [sprechen_item(f"{pid}-sprechen3", 1,
            "Bitten Sie jemanden, Ihnen ein Gerät zu erklären.",
            "請人說明一台器材怎麼用。",
            ["Entschuldigung", "Gerät", "Können Sie … erklären?", "Danke"],
            "Entschuldigung, können Sie mir bitte dieses Gerät erklären? Ich bin neu hier. Danke!")],
    )
    return paper(
        pid, "A1", 4,
        "Goethe-Format A1 · Modellsatz 4 (etwas schwerer)",
        "考場版 A1 · 第4回（稍難）",
        65,
        [lesen1, lesen2, lesen3, hoeren1, hoeren2, hoeren3, schreiben1, schreiben2, sprechen1, sprechen2, sprechen3],
        difficulty="etwas_schwerer",
    )


# ═══════════════════════════════════════════════════════════════════════════
# A2-g3 · leichter — Kino / Freizeit / Kulturverein
# ═══════════════════════════════════════════════════════════════════════════


def a2_g3() -> dict[str, Any]:
    pid = "a2-g3"
    lesen1 = section(
        "lesen1", "lesen", "Lesen Teil 1", "閱讀 Teil 1",
        "Lesen Sie den Medientext.", "閱讀媒體短文。",
        [
            tf(f"{pid}-lesen1", 1, "Viele Leute gehen am Wochenende ins Kino.", True, "文首。", "週末很多人看電影。"),
            tf(f"{pid}-lesen1", 2, "Tickets sind immer teuer.", False, "Studentenrabatt mentioned。", "票一律很貴。"),
            mc(f"{pid}-lesen1", 3, "Was ist praktisch?", ["nur DVD", "Online-Reservierung", "nur Telefon"], 1, "online reservieren。", "什麼方便？"),
            tf(f"{pid}-lesen1", 4, "Das Kino hat 20 Säle.", "nicht", "未提廳數。", "有 20 廳。"),
            mc(f"{pid}-lesen1", 5, "Wann gibt es oft Rabatt?", ["Dienstag", "nur Feiertag", "nie"], 0, "dienstags。", "何時常有折扣？"),
        ],
        passage=(
            "Stadtmagazin – Freizeit\n"
            "Viele Leute gehen am Wochenende ins Kino. Online kann man Plätze reservieren. "
            "Studenten bekommen oft Rabatt, besonders dienstags. "
            "Vor dem Film kann man im Foyer Popcorn kaufen."
        ),
        passage_zh="週末多人看電影；可線上訂位；學生常有折扣，尤其週二；大廳可買爆米花。",
    )
    lesen2 = section(
        "lesen2", "lesen", "Lesen Teil 2", "閱讀 Teil 2",
        "Programm / Tafel.", "節目表／佈告。",
        [
            mc(f"{pid}-lesen2", 1, "Wann läuft „Sommerwind“?", ["18:00", "20:15", "22:00"], 1, "20:15。", "幾點放？"),
            mc(f"{pid}-lesen2", 2, "In welchem Saal?", ["Saal 1", "Saal 3", "Saal 5"], 1, "Saal 3。", "哪一廳？"),
            mc(f"{pid}-lesen2", 3, "Was kostet Studententicket?", ["6 €", "8 €", "12 €"], 1, "8 €。", "學生票？"),
            mc(f"{pid}-lesen2", 4, "Wann ist Filmgespräch?", ["Fr 17 Uhr", "Sa 17 Uhr", "So 10 Uhr"], 1, "Sa 17:00。", "映後座談？"),
            mc(f"{pid}-lesen2", 5, "Wo ist der Kulturverein?", ["EG Foyer", "Dach", "Parkplatz"], 0, "EG Foyer。", "文化社團？"),
        ],
        passage=(
            "Kino Luna – Heute\n"
            "„Sommerwind“ 20:15 · Saal 3 · Studententicket 8 €\n"
            "Sa 17:00: Filmgespräch im EG Foyer (Kulturverein)\n"
            "Mo–Do: alle Tickets −2 €"
        ),
        passage_zh="《夏風》20:15 第三廳，學生票 8 歐；週六 17 點大廳映後座談；週一至四全票減 2 歐。",
    )
    lesen3 = section(
        "lesen3", "lesen", "Lesen Teil 3", "閱讀 Teil 3",
        "Lesen Sie die Korrespondenz.", "閱讀郵件。",
        [
            mc(f"{pid}-lesen3", 1, "Warum schreibt Omar?", ["Beschwerde", "Ticketreservierung", "Job"], 1, "zwei Karten reservieren。", "為何寫？"),
            mc(f"{pid}-lesen3", 2, "Für welchen Film?", ["Sommerwind", "Nachtzug", "Sportshow"], 0, "Sommerwind。", "哪部片？"),
            mc(f"{pid}-lesen3", 3, "Wie viele Karten?", ["1", "2", "4"], 1, "zwei Karten。", "幾張？"),
            mc(f"{pid}-lesen3", 4, "Wann möchte er abholen?", ["18 Uhr", "19:30 Uhr", "21 Uhr"], 1, "19:30。", "何時取票？"),
            tf(f"{pid}-lesen3", 5, "Er will bar bezahlen.", True, "bar bezahlen。", "要付現金。"),
        ],
        passage=(
            "Betreff: Reservierung Sommerwind\n"
            "Guten Tag,\n"
            "ich möchte zwei Karten für „Sommerwind“ am Samstag reservieren. "
            "Ich hole die Karten um 19:30 Uhr ab und zahle bar.\n"
            "Viele Grüße\nOmar Hassan"
        ),
        passage_zh="Omar 訂兩張週六《夏風》，19:30 取票並付現金。",
    )
    lesen4 = section(
        "lesen4", "lesen", "Lesen Teil 4", "閱讀 Teil 4",
        "Welche Anzeige passt?", "哪則廣告符合？",
        [
            mc(f"{pid}-lesen4", 1, "Sie suchen günstiges Abendkino.", ["A", "B", "C"], 0, "A：Abend ab 6 €。", "便宜晚場？"),
            mc(f"{pid}-lesen4", 2, "Sie möchten Chor singen.", ["A", "B", "C"], 1, "B：Chor。", "合唱團？"),
            mc(f"{pid}-lesen4", 3, "Sie suchen Museumsführung.", ["A", "B", "C"], 2, "C：Museum。", "導覽？"),
            mc(f"{pid}-lesen4", 4, "Welche Aktivität ist sonntags?", ["A", "B", "C"], 2, "C：So 11 Uhr。", "週日？"),
            mc(f"{pid}-lesen4", 5, "Was ist kostenlos?", ["A", "B", "C"], 1, "B：kostenlos。", "免費？"),
        ],
        passage=(
            "A: Kino Luna Abendvorstellung ab 6 €, täglich ab 18 Uhr.\n"
            "B: Kulturverein Chor, Mi 19 Uhr, kostenlos zum Probieren.\n"
            "C: Museum Stadtmitte Führung, So 11 Uhr, 5 €."
        ),
        passage_zh="A 晚場電影；B 免費合唱團試唱；C 週日博物館導覽。",
    )
    hoeren1 = section(
        "hoeren1", "hoeren", "Hören Teil 1", "聽力 Teil 1",
        "Kurze Situationen.", "短情境。",
        [
            mc(f"{pid}-hoeren1", 1, "Wann beginnt der Film?", ["19 Uhr", "20 Uhr", "21 Uhr"], 1, "um 20 Uhr。", "開場？"),
            mc(f"{pid}-hoeren1", 2, "Wo treffen sie sich?", ["Kasse", "Café", "Park"], 0, "an der Kasse。", "碰面？"),
            tf(f"{pid}-hoeren1", 3, "Es gibt noch Karten.", True, "noch Karten frei。", "還有票。"),
            mc(f"{pid}-hoeren1", 4, "Was kostet Popcorn?", ["3 €", "4 €", "5 €"], 1, "4 Euro。", "爆米花？"),
            mc(f"{pid}-hoeren1", 5, "Welcher Saal?", ["2", "3", "4"], 1, "Saal drei。", "廳？"),
        ],
        audio_text=(
            "Situation 1: Der Film beginnt um 20 Uhr. "
            "Situation 2: Wir treffen uns an der Kasse. "
            "Situation 3: Es sind noch Karten frei. "
            "Situation 4: Ein großes Popcorn kostet 4 Euro. "
            "Situation 5: Bitte gehen Sie in Saal drei."
        ),
    )
    hoeren2 = section(
        "hoeren2", "hoeren", "Hören Teil 2", "聽力 Teil 2",
        "Gespräch.", "對話。",
        [
            mc(f"{pid}-hoeren2", 1, "Wohin wollen sie?", ["Museum", "Kino", "Sport"], 1, "ins Kino。", "去哪？"),
            mc(f"{pid}-hoeren2", 2, "Welcher Tag?", ["Fr", "Sa", "So"], 1, "Samstag。", "哪天？"),
            mc(f"{pid}-hoeren2", 3, "Wie kommen sie?", ["Auto", "Bus", "zu Fuß"], 1, "mit dem Bus。", "怎麼去？"),
            mc(f"{pid}-hoeren2", 4, "Wann abfahren?", ["17 Uhr", "18 Uhr", "19 Uhr"], 1, "um 18 Uhr。", "幾點出發？"),
            mc(f"{pid}-hoeren2", 5, "Wer holt die Karten?", ["Lisa", "Marco", "beide"], 0, "Lisa。", "誰取票？"),
        ],
        audio_text=(
            "Lisa: Lust auf Kino am Samstag? "
            "Marco: Ja, gerne. Wir fahren um 18 Uhr mit dem Bus. "
            "Lisa: Super, ich hole die Karten online. "
            "Marco: Perfekt, bis Samstag!"
        ),
    )
    hoeren3 = section(
        "hoeren3", "hoeren", "Hören Teil 3", "聽力 Teil 3",
        "Durchsage.", "廣播。",
        [
            mc(f"{pid}-hoeren3", 1, "Was hat Verspätung?", ["Bus", "Filmstart", "Chor"], 1, "Filmstart … 10 Minuten。", "什麼延遲？"),
            mc(f"{pid}-hoeren3", 2, "Neue Startzeit?", ["20:10", "20:25", "20:40"], 1, "20 Uhr 25。", "新時間？"),
            mc(f"{pid}-hoeren3", 3, "Wo Getränke?", ["draußen", "Foyer", "nur Saal"], 1, "im Foyer。", "飲料？"),
            mc(f"{pid}-hoeren3", 4, "Handy?", ["laut OK", "stumm schalten", "filmen OK"], 1, "stumm schalten。", "手機？"),
        ],
        audio_text=(
            "Liebe Gäste: Der Filmstart hat zehn Minuten Verspätung. "
            "Neuer Beginn ist 20 Uhr 25. Getränke gibt es im Foyer. "
            "Bitte schalten Sie Ihr Handy stumm. Vielen Dank."
        ),
    )
    hoeren4 = section(
        "hoeren4", "hoeren", "Hören Teil 4", "聽力 Teil 4",
        "Kurzes Interview / Meinungen.", "短訪談。",
        [
            tf(f"{pid}-hoeren4", 1, "Mara geht oft unter der Woche ins Kino.", False, "meist am Wochenende。", "Mara 平日常去。"),
            tf(f"{pid}-hoeren4", 2, "Sie mag Komödien.", True, "besonders Komödien。", "喜歡喜劇。"),
            mc(f"{pid}-hoeren4", 3, "Was findet sie zu teuer?", ["Bus", "Snacks", "Tickets immer"], 1, "Snacks zu teuer。", "太貴？"),
            mc(f"{pid}-hoeren4", 4, "Mit wem geht sie?", ["allein", "Freunden", "Chef"], 1, "mit Freunden。", "跟誰？"),
        ],
        audio_text=(
            "Mara: Ich gehe meist am Wochenende ins Kino, besonders zu Komödien. "
            "Die Snacks finde ich oft zu teuer. Ich gehe gerne mit Freunden."
        ),
    )
    schreiben1 = section(
        "schreiben1", "schreiben", "Schreiben Teil 1", "寫作 Teil 1",
        "Schreiben Sie eine SMS.", "請寫簡訊。",
        [
            schreiben_item(
                f"{pid}-schreiben1", 1,
                "Schreiben Sie eine SMS an Ihren Freund:\n"
                "• Film beginnt später\n• neue Uhrzeit\n• Treffpunkt",
                "寫簡訊給朋友：電影延後、新時間、碰面地點。",
                20,
                "Hi Marco, der Film beginnt erst um 20:25. Treffen wir uns um 20:10 an der Kasse? Bis gleich! Lisa",
                ["提到延後", "新時間", "碰面地點"],
            )
        ],
    )
    schreiben2 = section(
        "schreiben2", "schreiben", "Schreiben Teil 2", "寫作 Teil 2",
        "Schreiben Sie eine E-Mail.", "請寫電子郵件。",
        [
            schreiben_item(
                f"{pid}-schreiben2", 1,
                "Schreiben Sie an den Kulturverein:\n"
                "• Interesse am Chor\n• fragen nach Probetermin\n• Ihre Telefonnummer",
                "寫給文化社團：想參加合唱、問試唱時間、留下電話。",
                30,
                "Guten Tag,\nich interessiere mich für den Chor und möchte gerne einmal mittmachen. "
                "Wann ist der nächste Probetermin? Meine Telefonnummer ist 0176 1112233.\n"
                "Freundliche Grüße\nOmar Hassan",
                ["表達興趣", "詢問時間", "留下聯絡方式"],
            )
        ],
    )
    sprechen1 = section(
        "sprechen1", "sprechen", "Sprechen Teil 1", "口說 Teil 1",
        "Informationen tauschen.", "交換資訊。",
        [sprechen_item(f"{pid}-sprechen1", 1,
            "Tauschen Sie Informationen: Name, Freizeit, Lieblingsfilm, wie oft Kino.",
            "交換：名字、休閒、最愛電影、多久去一次電影院。",
            ["Name", "Freizeit", "Film", "Wie oft?"],
            "Ich heiße Lisa. In der Freizeit gehe ich ins Kino. Mein Lieblingsfilm ist eine Komödie. Ich gehe etwa zweimal im Monat.")],
    )
    sprechen2 = section(
        "sprechen2", "sprechen", "Sprechen Teil 2", "口說 Teil 2",
        "Erzählen Sie.", "請敘述。",
        [sprechen_item(f"{pid}-sprechen2", 1,
            "Erzählen Sie von einem Kinobesuch: Welcher Film? Mit wem? Wie war es?",
            "談一次看電影：哪部、跟誰、感覺如何？",
            ["Film", "Mit wem?", "Meinung"],
            "Letzte Woche war ich mit Marco im Kino. Wir haben eine Komödie gesehen. Es war lustig und entspannend.")],
    )
    sprechen3 = section(
        "sprechen3", "sprechen", "Sprechen Teil 3", "口說 Teil 3",
        "Planen Sie.", "一起規劃。",
        [sprechen_item(f"{pid}-sprechen3", 1,
            "Planen Sie einen Kulturabend: Film oder Chor? Wann? Treffpunkt?",
            "規劃文化之夜：電影或合唱、時間、碰面。",
            ["Aktivität", "Tag/Uhrzeit", "Treffpunkt"],
            "Lass uns am Samstag ins Kino gehen. Wir treffen uns um 19:30 an der Kasse.")],
    )
    return paper(
        pid, "A2", 3,
        "Goethe-Format A2 · Modellsatz 3 (leichter)",
        "考場版 A2 · 第3回（稍易）",
        90,
        [lesen1, lesen2, lesen3, lesen4, hoeren1, hoeren2, hoeren3, hoeren4, schreiben1, schreiben2, sprechen1, sprechen2, sprechen3],
        difficulty="leichter",
    )


# ═══════════════════════════════════════════════════════════════════════════
# A2-g4 · etwas_schwerer — Umzug / Wohnungssuche
# ═══════════════════════════════════════════════════════════════════════════


def a2_g4() -> dict[str, Any]:
    pid = "a2-g4"
    lesen1 = section(
        "lesen1", "lesen", "Lesen Teil 1", "閱讀 Teil 1",
        "Medientext.", "媒體短文。",
        [
            tf(f"{pid}-lesen1", 1, "Viele Menschen ziehen wegen Arbeit um.", True, "wegen eines Jobs。", "常因工作搬家。"),
            tf(f"{pid}-lesen1", 2, "Wohnungsbesichtigungen sind unnötig.", False, "frühzeitig Besichtigungen。", "看房多餘。"),
            mc(f"{pid}-lesen1", 3, "Was hilft laut Text?", ["nur Glück", "Checkliste und früh suchen", "nur Makler zwingend"], 1, "Checkliste … früh。", "什麼有幫助？"),
            tf(f"{pid}-lesen1", 4, "Kaution ist immer drei Monatsmieten.", "nicht", "未寫死金額。", "押金一定三個月。"),
            mc(f"{pid}-lesen1", 5, "Was sollte man vergleichen?", ["nur Farbe der Wände", "Miete, Lage, Nebenkosten", "nur Haustiere"], 1, "Miete, Lage, Nebenkosten。", "要比較？"),
            mc(f"{pid}-lesen1", 6, "Warum erwähnen viele den Nahverkehr?", ["egal", "spart Zeit und Geld", "nur Touristen"], 1, "可推知交通方便省時錢。", "為何提大眾運輸？"),
        ],
        passage=(
            "Stadtmagazin – Umziehen leicht gemacht?\n"
            "Immer mehr Menschen ziehen wegen eines Jobs in eine neue Stadt. "
            "Experten raten: Suchen Sie früh und machen Sie eine Checkliste für "
            "Besichtigungen. Vergleichen Sie Miete, Lage und Nebenkosten. "
            "Gute Anbindung an Bus und Bahn spart oft Zeit und Geld. "
            "Fotos der Wohnung und Fragen zur Kaution sollte man nicht vergessen."
        ),
        passage_zh="因工作搬家的人變多；建議提早找、列看房清單，比較租金、地段與雜費；交通方便省時錢；別忘拍照與問押金。",
    )
    lesen2 = section(
        "lesen2", "lesen", "Lesen Teil 2", "閱讀 Teil 2",
        "Tafel / Aushang.", "佈告。",
        [
            mc(f"{pid}-lesen2", 1, "Wann Beratung Wohnen?", ["Mo 10", "Di 16", "Fr 9"], 1, "Di 16:00。", "諮詢？"),
            mc(f"{pid}-lesen2", 2, "Wo?", ["Raum B1", "Café", "Hof"], 0, "Raum B1。", "地點？"),
            mc(f"{pid}-lesen2", 3, "Kosten?", ["kostenlos", "10 €", "50 €"], 0, "kostenlos。", "費用？"),
            mc(f"{pid}-lesen2", 4, "Anmeldung bis?", ["heute", "Donnerstag", "nächstes Jahr"], 1, "bis Donnerstag。", "報名？"),
            mc(f"{pid}-lesen2", 5, "Was noch am Do?", ["Umzugshilfe Treffen", "Konzert", "Markt"], 0, "Umzugshilfe。", "週四還有？"),
            mc(f"{pid}-lesen2", 6, "Für wen ist das Angebot gedacht?", ["nur Touristen", "Neuankömmlinge / Umziehende", "nur Kinder"], 1, "Wohnberatung／搬家者。", "對象？"),
        ],
        passage=(
            "Nachbarschaftszentrum – Diese Woche\n"
            "Wohnberatung mit Frau Stein\n"
            "Di 16:00–17:00 · Raum B1 · kostenlos\n"
            "Anmeldung bis Donnerstag an der Infotheke\n"
            "Do 18:00: Treffen Umzugshilfe · EG Foyer"
        ),
        passage_zh="Stein 女士住房諮詢週二 16–17 點 B1 免費，週四前報名；週四 18 點搬家互助聚會。",
    )
    lesen3 = section(
        "lesen3", "lesen", "Lesen Teil 3", "閱讀 Teil 3",
        "Korrespondenz.", "往來信件。",
        [
            mc(f"{pid}-lesen3", 1, "Warum schreibt Mira?", ["Urlaub", "Wohnungsanfrage", "Rechnung"], 1, "interessiere mich für die Wohnung。", "為何寫？"),
            mc(f"{pid}-lesen3", 2, "Ab wann braucht sie die Wohnung?", ["sofort", "1. März", "Sommer"], 1, "ab dem 1. März。", "何時入住？"),
            mc(f"{pid}-lesen3", 3, "Beruf?", ["Studentin", "Krankenschwester", "Lehrerin"], 1, "als Krankenschwester。", "職業？"),
            mc(f"{pid}-lesen3", 4, "Was schickt sie?", ["nur Foto", "Lebenslauf nicht – Einkommensnachweis", "nichts"], 1, "Einkommensnachweis。", "附件？"),
            tf(f"{pid}-lesen3", 5, "Sie hat ein Haustier.", False, "ohne Haustiere。", "有寵物。"),
            tf(f"{pid}-lesen3", 6, "Sie möchte am Freitag besichtigen.", True, "Freitag um 17 Uhr。", "週五想看房。"),
        ],
        passage=(
            "Betreff: Anfrage 3-Zimmer-Wohnung Lindenweg\n"
            "Sehr geehrte Frau Hoffmann,\n"
            "ich interessiere mich für Ihre Wohnung ab dem 1. März. Ich arbeite als "
            "Krankenschwester in Schicht und habe keine Haustiere. Anbei sende ich einen "
            "Einkommensnachweis. Können wir die Wohnung am Freitag um 17 Uhr besichtigen?\n"
            "Mit freundlichen Grüßen\nMira Novak"
        ),
        passage_zh="Mira 詢問 Lindenweg 三房，三月一日起，護理師輪班、無寵物，附收入證明，想週五 17 點看房。",
    )
    lesen4 = section(
        "lesen4", "lesen", "Lesen Teil 4", "閱讀 Teil 4",
        "Welche Anzeige passt?", "哪則符合？",
        [
            mc(f"{pid}-lesen4", 1, "Sie suchen ruhige Wohnung mit Balkon.", ["A", "B", "C"], 0, "A：Balkon, ruhig。", "安靜有陽台？"),
            mc(f"{pid}-lesen4", 2, "Sie brauchen Möbel und kurze Mietzeit.", ["A", "B", "C"], 1, "B：möbliert, 6 Monate。", "傢俱短租？"),
            mc(f"{pid}-lesen4", 3, "Sie suchen WG-Zimmer zentral.", ["A", "B", "C"], 2, "C：WG zentral。", "市中心雅房？"),
            mc(f"{pid}-lesen4", 4, "Welche ist am günstigsten?", ["A", "B", "C"], 2, "C：380 €。", "最便宜？"),
            mc(f"{pid}-lesen4", 5, "Welche erlaubt Haustiere?", ["A", "B", "C"], 0, "A：Haustiere OK。", "可養寵物？"),
            mc(f"{pid}-lesen4", 6, "Welche liegt nah am Krankenhaus?", ["A", "B", "C"], 1, "B：nah Krankenhaus。", "靠近醫院？"),
        ],
        passage=(
            "A: 2 Zi., Balkon, ruhig, Haustiere OK, 720 € + NK, ab sofort.\n"
            "B: 1 Zi. möbliert, 6 Monate, nah Krankenhaus, 650 € inkl., Nichtraucher.\n"
            "C: WG-Zimmer zentral, 380 € inkl. WLAN, Mitbewohner 2 Personen."
        ),
        passage_zh="A 兩房陽台可寵物；B 套房傢俱近醫院短租；C 市中心雅房最便宜。",
    )
    hoeren1 = section(
        "hoeren1", "hoeren", "Hören Teil 1", "聽力 Teil 1",
        "Kurze Situationen.", "短情境。",
        [
            mc(f"{pid}-hoeren1", 1, "Wann ist die Besichtigung?", ["15 Uhr", "16 Uhr", "17 Uhr"], 1, "um 16 Uhr。", "看房？"),
            mc(f"{pid}-hoeren1", 2, "Was mitbringen?", ["Ausweis", "Hund", "Farbe"], 0, "Ihren Ausweis。", "帶什麼？"),
            tf(f"{pid}-hoeren1", 3, "Der Aufzug funktioniert.", False, "Aufzug ist kaputt。", "電梯正常。"),
            mc(f"{pid}-hoeren1", 4, "Kaution?", ["1 Miete", "2 Mieten", "3 Mieten"], 2, "drei Monatsmieten。", "押金？"),
            mc(f"{pid}-hoeren1", 5, "Wer hat den Schlüssel?", ["Nachbar", "Hausmeister", "Polizei"], 1, "Hausmeister。", "鑰匙？"),
            mc(f"{pid}-hoeren1", 6, "Was soll man vor dem Einzug machen?", ["streichen lassen Pflicht", "Übergabeprotokoll", "Party"], 1, "Übergabeprotokoll。", "入住前？"),
        ],
        audio_text=(
            "Situation 1: Die Besichtigung ist um 16 Uhr. "
            "Situation 2: Bitte bringen Sie Ihren Ausweis mit. "
            "Situation 3: Achtung, der Aufzug ist kaputt – bitte Treppe. "
            "Situation 4: Die Kaution beträgt drei Monatsmieten. "
            "Situation 5: Den Schlüssel holen Sie beim Hausmeister. "
            "Situation 6: Vor dem Einzug machen wir ein Übergabeprotokoll."
        ),
    )
    hoeren2 = section(
        "hoeren2", "hoeren", "Hören Teil 2", "聽力 Teil 2",
        "Gespräch.", "對話。",
        [
            mc(f"{pid}-hoeren2", 1, "Warum zieht Jonas um?", ["Urlaub", "neuer Job", "Hochzeit"], 1, "wegen eines neuen Jobs。", "為何搬？"),
            mc(f"{pid}-hoeren2", 2, "Wohin?", ["Berlin", "Leipzig", "Hamburg"], 1, "nach Leipzig。", "搬去哪？"),
            mc(f"{pid}-hoeren2", 3, "Wann Umzug?", ["1. Feb", "1. März", "1. April"], 1, "am ersten März。", "何時？"),
            mc(f"{pid}-hoeren2", 4, "Wer hilft?", ["Firma", "Freunde", "niemand"], 1, "Freunde helfen。", "誰幫忙？"),
            mc(f"{pid}-hoeren2", 5, "Was ist noch offen?", ["Kartons", "Internetanschluss", "Sofa"], 1, "Internetanschluss。", "還沒搞定？"),
            tf(f"{pid}-hoeren2", 6, "Er hat schon eine Wohnung gefunden.", True, "Wohnung schon gefunden。", "已找到房子。"),
        ],
        audio_text=(
            "Nora: Jonas, warum ziehst du um? "
            "Jonas: Wegen eines neuen Jobs nach Leipzig. Am ersten März. "
            "Die Wohnung habe ich schon gefunden. Freunde helfen beim Tragen. "
            "Offen ist noch der Internetanschluss – das dauert oft länger."
        ),
    )
    hoeren3 = section(
        "hoeren3", "hoeren", "Hören Teil 3", "聽力 Teil 3",
        "Durchsage.", "廣播。",
        [
            mc(f"{pid}-hoeren3", 1, "Was ist gesperrt?", ["Eingang A", "Parkplatz Ost", "Fahrstuhl"], 1, "Parkplatz Ost。", "封閉？"),
            mc(f"{pid}-hoeren3", 2, "Warum?", ["Fest", "Umzugstransporter", "Schnee"], 1, "Umzugstransporter。", "原因？"),
            mc(f"{pid}-hoeren3", 3, "Alternative?", ["Parkplatz West", "Straße", "kein Parken"], 0, "Parkplatz West。", "替代？"),
            mc(f"{pid}-hoeren3", 4, "Bis wann?", ["12 Uhr", "15 Uhr", "18 Uhr"], 1, "bis 15 Uhr。", "到幾點？"),
            tf(f"{pid}-hoeren3", 5, "Bewohner sollen Transporter melden.", True, "melden Sie … an der Infotheke。", "要通報卡車。"),
        ],
        audio_text=(
            "Achtung Bewohner: Parkplatz Ost ist wegen Umzugstransportern bis 15 Uhr gesperrt. "
            "Bitte nutzen Sie Parkplatz West. Melden Sie Ihren Transporter an der Infotheke."
        ),
    )
    hoeren4 = section(
        "hoeren4", "hoeren", "Hören Teil 4", "聽力 Teil 4",
        "Meinungen.", "意見。",
        [
            tf(f"{pid}-hoeren4", 1, "Sina fand die Suche stressig.", True, "sehr stressig。", "覺得找房壓力大。"),
            tf(f"{pid}-hoeren4", 2, "Sie hat ohne Checkliste gesucht.", False, "mit Checkliste。", "沒有清單。"),
            mc(f"{pid}-hoeren4", 3, "Was war entscheidend?", ["nur Preis", "Lage zur Arbeit", "Farbe"], 1, "Lage zur Arbeit。", "關鍵？"),
            mc(f"{pid}-hoeren4", 4, "Tipp an andere?", ["spontan mieten", "früh anfangen", "nie fragen"], 1, "früh anfangen。", "建議？"),
            mc(f"{pid}-hoeren4", 5, "Was ärgerte sie bei manchen Anzeigen?", ["zu viele Fotos", "unklare Nebenkosten", "zu viel Text"], 1, "Nebenkosten unklar。", "惱人處？"),
        ],
        audio_text=(
            "Sina: Die Wohnungssuche war sehr stressig. Ich habe mit einer Checkliste gearbeitet. "
            "Entscheidend war die Lage zur Arbeit. Manche Anzeigen ärgern mich, weil die Nebenkosten unklar sind. "
            "Mein Tipp: Früh anfangen und alles schriftlich fragen."
        ),
    )
    schreiben1 = section(
        "schreiben1", "schreiben", "Schreiben Teil 1", "寫作 Teil 1",
        "SMS.", "簡訊。",
        [
            schreiben_item(
                f"{pid}-schreiben1", 1,
                "SMS an Ihren Freund:\n• Umzugswagen hat Verspätung\n• neue Ankunftszeit\n• bitte Schlüssel bereithalten",
                "簡訊：搬家貨車延誤、新到達時間、請準備鑰匙。",
                20,
                "Hi Nora, der Wagen hat Verspätung und kommt erst um 15:30. Hast du bitte den Schlüssel bereit? Danke! Jonas",
                ["延誤", "新時間", "鑰匙"],
            )
        ],
    )
    schreiben2 = section(
        "schreiben2", "schreiben", "Schreiben Teil 2", "寫作 Teil 2",
        "E-Mail.", "電子郵件。",
        [
            schreiben_item(
                f"{pid}-schreiben2", 1,
                "E-Mail an die Vermieterin:\n"
                "• Interesse an der Wohnung\n• Wunschtermin Besichtigung\n• Frage zu Nebenkosten und Kaution",
                "寫給房東：有興趣、希望看房時間、問雜費與押金。",
                40,
                "Sehr geehrte Frau Hoffmann,\nich interessiere mich für Ihre Wohnung im Lindenweg. "
                "Können wir am Freitag um 17 Uhr besichtigen? Bitte teilen Sie mir auch die Nebenkosten "
                "und die Höhe der Kaution mit.\nMit freundlichen Grüßen\nMira Novak",
                ["表達興趣", "提出看房時間", "詢問雜費／押金"],
            )
        ],
    )
    sprechen1 = section(
        "sprechen1", "sprechen", "Sprechen Teil 1", "口說 Teil 1",
        "Informationen.", "交換資訊。",
        [sprechen_item(f"{pid}-sprechen1", 1,
            "Tauschen Sie Infos: Name, warum Umzug, neue Stadt, was ist wichtig bei der Wohnung.",
            "交換：名字、為何搬、新城市、住房看重什麼。",
            ["Name", "Grund", "Stadt", "Kriterien"],
            "Ich heiße Mira. Ich ziehe wegen der Arbeit um. Mir sind Lage und ruhige Nachbarn wichtig.")],
    )
    sprechen2 = section(
        "sprechen2", "sprechen", "Sprechen Teil 2", "口說 Teil 2",
        "Erzählen.", "敘述。",
        [sprechen_item(f"{pid}-sprechen2", 1,
            "Erzählen Sie von einer Wohnungssuche oder einem Umzug.",
            "談找房或搬家經驗。",
            ["Was war schwer?", "Was hat geholfen?", "Tipp"],
            "Die Suche war stressig. Eine Checkliste und frühe Besichtigungen haben geholfen. Mein Tipp: Nebenkosten immer fragen.")],
    )
    sprechen3 = section(
        "sprechen3", "sprechen", "Sprechen Teil 3", "口說 Teil 3",
        "Planen.", "規劃。",
        [sprechen_item(f"{pid}-sprechen3", 1,
            "Planen Sie einen Umzugstag: Zeiten, wer hilft, Transport, Pausen.",
            "規劃搬家日：時間、幫手、運輸、休息。",
            ["Zeitplan", "Helfer", "Transporter", "Pause"],
            "Wir starten um 9 Uhr. Zwei Freunde helfen. Den Transporter holen wir um 8:30. Um 13 Uhr machen wir Pause.")],
    )
    return paper(
        pid, "A2", 4,
        "Goethe-Format A2 · Modellsatz 4 (etwas schwerer)",
        "考場版 A2 · 第4回（稍難）",
        90,
        [lesen1, lesen2, lesen3, lesen4, hoeren1, hoeren2, hoeren3, hoeren4, schreiben1, schreiben2, sprechen1, sprechen2, sprechen3],
        difficulty="etwas_schwerer",
    )


# Continue in part 2 for B1/B2 — appended below via second write if needed
# Placeholder marker for split; see functions b1_g3 etc. below.


def b1_g3() -> dict[str, Any]:
    """leichter — Gesundheit / Sport im Alltag (still B1)."""
    pid = "b1-g3"
    lesen1 = section(
        "lesen1", "lesen", "Lesen Teil 1", "閱讀 Teil 1",
        "Blog/Meinung.", "部落格／意見。",
        [
            mc(f"{pid}-lesen1", 1, "Worum geht es?", ["Diäten-Trends nur", "Bewegung im Alltag", "Autokauf"], 1, "Alltagsbewegung。", "主題？"),
            tf(f"{pid}-lesen1", 2, "Kurze Spaziergänge können helfen.", True, "kurze Spaziergänge。", "短散步有幫助。"),
            mc(f"{pid}-lesen1", 3, "Was kritisiert der Text?", ["Sportvereine", "nur extreme Programme", "Ärzte"], 1, "extreme Fitnessprogramme。", "批評？"),
            tf(f"{pid}-lesen1", 4, "Alle Firmen bieten Sportkurse an.", False, "manche Betriebe。", "所有公司都有課程。"),
            mc(f"{pid}-lesen1", 5, "Was wünschen sich viele Leser?", ["mehr Bildschirme", "sichere Radwege zur Arbeit", "längere Sitzzeiten"], 1, "Radwege。", "讀者想要？"),
        ],
        passage=_long(
            """
            Blog: Bewegung ohne Drama
            Viele wollen fitter werden, scheitern aber an zu strengen Plänen.
            Oft reichen schon kurze Spaziergänge, Treppen statt Aufzug und ein
            fester Termin mit Freunden zum Sport. Extreme Fitnessprogramme wirken
            kurz motivierend, führen aber schnell zu Abbruch. Manche Betriebe
            bieten mittlerweile Pausensport an – das senkt Stress. Leser wünschen
            sich vor allem sichere Radwege zur Arbeit, nicht nur Appelle.
            """
        ),
        passage_zh="部落格：不必極端計畫，短散步、走樓梯、固定運動約會更有效；部分公司有休息運動；讀者盼安全通勤單車道。",
    )
    lesen2 = section(
        "lesen2", "lesen", "Lesen Teil 2", "閱讀 Teil 2",
        "Anzeigen zuordnen.", "廣告配對。",
        [
            mc(f"{pid}-lesen2", 1, "Sie möchten abends Yoga für Anfänger.", ["A", "B", "C", "D"], 0, "A：Yoga Anfänger abends。", "初階瑜珈？"),
            mc(f"{pid}-lesen2", 2, "Sie suchen Nordic Walking Gruppe.", ["A", "B", "C", "D"], 1, "B：Nordic Walking。", "健走？"),
            mc(f"{pid}-lesen2", 3, "Sie brauchen Rücken-Kurs mittags.", ["A", "B", "C", "D"], 2, "C：Rücken mittags。", "午間背部課？"),
            mc(f"{pid}-lesen2", 4, "Sie wollen Schwimmen flexibel.", ["A", "B", "C", "D"], 3, "D：Schwimmbad。", "彈性游泳？"),
            mc(f"{pid}-lesen2", 5, "Welche ist kostenlos zum Probieren?", ["A", "B", "C", "D"], 1, "B：Probestunde gratis。", "免費體驗？"),
        ],
        passage=(
            "A: Yoga Anfänger, Mo/Mi 19 Uhr, Studio Balance, 12 €/Std.\n"
            "B: Nordic Walking Park Ost, Sa 10 Uhr, Probestunde gratis.\n"
            "C: Rückenkurs Betriebssport, Di/Do 12:15, Anmeldung Personalbüro.\n"
            "D: Stadtbad: Bahnen schwimmen, Mo–So, Tagesticket 5,50 €."
        ),
        passage_zh="A 初階瑜珈；B 免費體驗健走；C 公司背部課；D 泳池日票。",
    )
    lesen3 = section(
        "lesen3", "lesen", "Lesen Teil 3", "閱讀 Teil 3",
        "Magazinartikel.", "雜誌文章。",
        [
            tf(f"{pid}-lesen3", 1, "Schlafmangel beeinflusst die Konzentration.", True, "Konzentration leidet。", "睡眠不足影響專注。"),
            tf(f"{pid}-lesen3", 2, "Experten raten zu unregelmäßigen Zeiten.", False, "feste Schlafzeiten。", "建議不規律。"),
            mc(f"{pid}-lesen3", 3, "Was hilft am Abend?", ["mehr Koffein", "Bildschirmzeit reduzieren", "schwere Mahlzeiten spät"], 1, "Bildschirme reduzieren。", "晚上？"),
            tf(f"{pid}-lesen3", 4, "Das Projekt lief nur einen Tag.", False, "vier Wochen。", "只做一天。"),
            mc(f"{pid}-lesen3", 5, "Ergebnis der Studie?", ["keine Wirkung", "weniger Müdigkeit am Morgen", "mehr Unfälle"], 1, "weniger Müdigkeit。", "結果？"),
            tf(f"{pid}-lesen3", 6, "Alle Teilnehmer sportelten täglich zwei Stunden.", "nicht", "未寫兩小時。", "每天運動兩小時。"),
        ],
        passage=_long(
            """
            Magazin: Schlaf und Leistung
            Wer wenig schläft, merkt es oft zuerst an der Konzentration.
            Experten empfehlen feste Schlafzeiten und am Abend weniger Bildschirmzeit.
            In einem Betriebstest mit Schichtbeschäftigten zeigte sich nach vier Wochen:
            Wer kurze Bewegungspausen und klarere Feierabend-Routinen einbaute,
            berichtete von weniger Müdigkeit am Morgen. Die Evaluation läuft weiter.
            """
        ),
        passage_zh="睡眠不足傷專注；建議固定作息、少看螢幕；企業測試四週後晨間疲勞減少。",
    )
    lesen4 = section(
        "lesen4", "lesen", "Lesen Teil 4", "閱讀 Teil 4",
        "Schreiben einer Einrichtung.", "機構來信。",
        [
            mc(f"{pid}-lesen4", 1, "Was bietet die Krankenkasse?", ["nur Apps", "Präventionskurs Bewegung", "Autoreparatur"], 1, "Präventionskurs。", "提供？"),
            mc(f"{pid}-lesen4", 2, "Wie lange dauert der Kurs?", ["2 Wochen", "8 Wochen", "1 Jahr"], 1, "acht Wochen。", "多久？"),
            tf(f"{pid}-lesen4", 3, "Teilnahme ist komplett kostenpflichtig ohne Zuschuss.", False, "Zuschuss von 80%。", "完全自費無補助。"),
            mc(f"{pid}-lesen4", 4, "Anmeldung bis?", ["sofort Ende", "15. des Monats", "nur mündlich"], 1, "bis zum 15.。", "報名？"),
            mc(f"{pid}-lesen4", 5, "Wo findet der Kurs statt?", ["Online only", "Gesundheitszentrum Nord", "Flughafen"], 1, "Gesundheitszentrum Nord。", "地點？"),
        ],
        passage=_long(
            """
            Krankenkasse Vita – Information
            Sehr geehrte Versicherte, wir fördern den Präventionskurs „Bewegung im Alltag“
            (8 Wochen, 1× pro Woche) im Gesundheitszentrum Nord. Der Zuschuss beträgt 80 Prozent
            bei regelmäßiger Teilnahme. Anmeldung bitte bis zum 15. des Monats online.
            """
        ),
        passage_zh="Vita 健保補助「日常運動」八週課程 80%，地點北區健康中心，每月 15 日前線上報名。",
    )
    lesen5 = section(
        "lesen5", "lesen", "Lesen Teil 5", "閱讀 Teil 5",
        "Forum.", "論壇。",
        [
            mc(f"{pid}-lesen5", 1, "Timo's Problem?", ["zu viel Sport", "Rückenschmerzen am Schreibtisch", "kein Job"], 1, "Rückenschmerzen。", "問題？"),
            tf(f"{pid}-lesen5", 2, "Lea empfiehlt nur Medikamente.", False, "Pausen und Dehnen。", "只建議吃藥。"),
            mc(f"{pid}-lesen5", 3, "Was macht Sam?", ["ignoriert alles", "Betriebssport Rücken", "nur Marathon"], 1, "Betriebssport。", "Sam？"),
            tf(f"{pid}-lesen5", 4, "Alle stimmen gegen Radwege.", False, "Timo will Radwege。", "都反對單車道。"),
            mc(f"{pid}-lesen5", 5, "Konsens im Thread?", ["nie bewegen", "kleine Routinen helfen", "nur teure Studios"], 1, "kleine Routinen。", "共識？"),
        ],
        passage=(
            "Forum Gesund&Job\n"
            "Timo: Ich habe Rückenschmerzen vom Schreibtisch. Gibt es Tipps außer Schmerztabletten?\n"
            "Lea: Alle 60 Minuten aufstehen, dehnen, kurze Pause. Hilft mir mehr als Tabletten.\n"
            "Sam: Bei uns gibt es Betriebssport Rücken – echt sinnvoll.\n"
            "Timo: Danke! Und ja, sichere Radwege würden mich auch öfter bewegen lassen."
        ),
        passage_zh="Timo 久坐背痛；Lea 建議定時伸展；Sam 推公司背部課；也提到安全單車道。",
    )
    hoeren1 = section(
        "hoeren1", "hoeren", "Hören Teil 1", "聽力 Teil 1",
        "Interview.", "訪談。",
        [
            mc(f"{pid}-hoeren1", 1, "Thema der Expertin?", ["Zahnmedizin", "Alltagsbewegung", "Steuern"], 1, "Alltagsbewegung。", "主題？"),
            tf(f"{pid}-hoeren1", 2, "Sie rät zu extremen Plänen.", False, "gegen extreme Pläne。", "建議極端計畫。"),
            mc(f"{pid}-hoeren1", 3, "Beispiel für Einstieg?", ["10 Min. gehen", "sofort Marathon", "nichts"], 0, "zehn Minuten gehen。", "入門？"),
            mc(f"{pid}-hoeren1", 4, "Rolle von Kollegen?", ["egal", "Motivation durch Termine", "nur Konkurrenz"], 1, "feste Termine。", "同事？"),
            mc(f"{pid}-hoeren1", 5, "Was fordert sie von Städten?", ["mehr Parkplätze nur", "Radwege und Grün", "weniger Sport"], 1, "Radwege und Grünflächen。", "對城市？"),
        ],
        audio_text=(
            "Moderatorin: Was raten Sie Einsteigern? "
            "Expertin: Keine extremen Pläne. Zehn Minuten gehen ist besser als ein Plan, den man bricht. "
            "Feste Termine mit Kollegen motivieren. Städte brauchen Radwege und Grünflächen, nicht nur Appelle."
        ),
    )
    hoeren2 = section(
        "hoeren2", "hoeren", "Hören Teil 2", "聽力 Teil 2",
        "Gespräch Alltag.", "日常對話。",
        [
            mc(f"{pid}-hoeren2", 1, "Was planen Jana und Ole?", ["Party", "gemeinsames Laufen", "Umzug"], 1, "zusammen laufen。", "計畫？"),
            mc(f"{pid}-hoeren2", 2, "Wann?", ["Mo früh", "Di 18 Uhr", "So Nacht"], 1, "Dienstag um 18。", "何時？"),
            tf(f"{pid}-hoeren2", 3, "Ole hat neue Schuhe.", True, "neue Laufschuhe。", "Ole 有新鞋。"),
            mc(f"{pid}-hoeren2", 4, "Bei Regen?", ["absagen", "Halle / kürzer", "schwimmen Pflicht"], 1, "kürzer oder in die Halle。", "下雨？"),
            mc(f"{pid}-hoeren2", 5, "Treffpunkt?", ["Bahnhof", "Parkeingang Ost", "Büro"], 1, "Parkeingang Ost。", "碰面？"),
        ],
        audio_text=(
            "Jana: Ole, laufen wir Dienstag um 18 Uhr? "
            "Ole: Ja, ich habe neue Laufschuhe. Treffpunkt Parkeingang Ost. "
            "Bei Regen machen wir kürzer oder gehen in die Halle."
        ),
    )
    hoeren3 = section(
        "hoeren3", "hoeren", "Hören Teil 3", "聽力 Teil 3",
        "Durchsage / Info.", "廣播資訊。",
        [
            mc(f"{pid}-hoeren3", 1, "Was startet?", ["Kochkurs", "Betriebssport Aktion", "Prüfung"], 1, "Betriebssport-Aktion。", "開始？"),
            mc(f"{pid}-hoeren3", 2, "Dauer?", ["1 Tag", "vier Wochen", "1 Jahr"], 1, "vier Wochen。", "多久？"),
            tf(f"{pid}-hoeren3", 3, "Anmeldung per E-Mail an Personal.", True, "per E-Mail beim Personalbüro。", "向人事郵寄報名。"),
            mc(f"{pid}-hoeren3", 4, "Erste Einheit wann?", ["Mo 12:15", "Fr 20 Uhr", "Sa 6 Uhr"], 0, "Montag 12 Uhr 15。", "第一堂？"),
            mc(f"{pid}-hoeren3", 5, "Mitbringen?", ["Sportschuhe", "Laptop Pflicht", "nichts"], 0, "Sportschuhe。", "帶什麼？"),
        ],
        audio_text=(
            "Liebe Kolleginnen und Kollegen: Unsere Betriebssport-Aktion startet für vier Wochen. "
            "Erste Einheit: Montag 12 Uhr 15. Anmeldung per E-Mail beim Personalbüro. "
            "Bitte Sportschuhe mitbringen."
        ),
    )
    hoeren4 = section(
        "hoeren4", "hoeren", "Hören Teil 4", "聽力 Teil 4",
        "Diskussion / Meinungen.", "討論。",
        [
            mc(f"{pid}-hoeren4", 1, "Pia findet Pausensport …", ["nutzlos", "hilfreich gegen Verspannung", "zu laut"], 1, "gegen Verspannung。", "Pia？"),
            tf(f"{pid}-hoeren4", 2, "Ben hat keine Zeit mittags.", True, "mittags keine Zeit。", "Ben 中午沒時間。"),
            mc(f"{pid}-hoeren4", 3, "Kompromiss?", ["abschaffen", "kurze 10-Min-Einheiten", "nur Abendsport Pflicht"], 1, "zehn Minuten。", "折衷？"),
            mc(f"{pid}-hoeren4", 4, "Wer soll mitentscheiden?", ["nur Chef", "Belegschaft", "Kunden"], 1, "die Belegschaft。", "誰決定？"),
        ],
        audio_text=(
            "Pia: Pausensport hilft gegen Verspannung. "
            "Ben: Ich habe mittags keine Zeit. "
            "Pia: Dann lieber kurze zehn Minuten – und die Belegschaft soll mitentscheiden."
        ),
    )
    schreiben1 = section(
        "schreiben1", "schreiben", "Schreiben Teil 1", "寫作 Teil 1",
        "Formelle E-Mail.", "正式郵件。",
        [
            schreiben_item(
                f"{pid}-schreiben1", 1,
                "Schreiben Sie an Ihre Krankenkasse:\n"
                "• Interesse am Präventionskurs\n• Fragen zu Terminen und Zuschuss\n• Bitte um Anmeldebestätigung",
                "寫給健保：對預防課程有興趣、問時間與補助、請寄報名確認。",
                80,
                "Sehr geehrte Damen und Herren,\nich interessiere mich für den Kurs „Bewegung im Alltag“. "
                "Bitte teilen Sie mir die Termine und die Höhe des Zuschusses mit. "
                "Ich bitte um eine Anmeldebestätigung per E-Mail.\nMit freundlichen Grüßen",
                ["興趣", "詢問時間／補助", "請確認", "約 80 字"],
            )
        ],
    )
    schreiben2 = section(
        "schreiben2", "schreiben", "Schreiben Teil 2", "寫作 Teil 2",
        "Halboffizielle Nachricht.", "半正式回覆。",
        [
            schreiben_item(
                f"{pid}-schreiben2", 1,
                "Ein Freund fragt, ob Sie mitlaufen. Antworten Sie:\n"
                "• Zusagen / Absagen mit Grund\n• alternativer Vorschlag\n• Treffpunkt / Zeit",
                "朋友約跑步：答應或拒絕並說明、替代方案、時間地點。",
                80,
                "Hallo Ole,\ndanke für die Einladung! Am Dienstag kann ich leider nicht, weil ich Spätschicht habe. "
                "Können wir Donnerstag um 18 Uhr am Parkeingang Ost laufen?\nLiebe Grüße\nJana",
                ["明確回覆", "替代建議", "時間地點"],
            )
        ],
    )
    sprechen1 = section(
        "sprechen1", "sprechen", "Sprechen Teil 1", "口說 Teil 1",
        "Planen.", "規劃。",
        [sprechen_item(f"{pid}-sprechen1", 1,
            "Planen Sie eine Bewegungs-Woche im Team: Aktivitäten, Zeiten, Material.",
            "規劃團隊運動週：活動、時間、器材。",
            ["Aktivitäten", "Zeiten", "Material", "Wer organisiert?"],
            "Wir machen Mo und Mi kurze Pausengymnastik, Fr einen Lauf. Sportschuhe selbst mitbringen. Jana organisiert die Liste.")],
    )
    sprechen2 = section(
        "sprechen2", "sprechen", "Sprechen Teil 2", "口說 Teil 2",
        "Kurzvortrag.", "短講。",
        [sprechen_item(f"{pid}-sprechen2", 1,
            "Sprechen Sie 2–3 Minuten: Wie bleibt man trotz Job gesund?",
            "談如何在工作中保持健康。",
            ["Schlaf", "Bewegung", "Pausen", "Beispiel"],
            "Wichtig sind Schlaf, kurze Bewegungspausen und realistische Ziele. Ein Beispiel: zehn Minuten gehen nach dem Mittag.")],
    )
    sprechen3 = section(
        "sprechen3", "sprechen", "Sprechen Teil 3", "口說 Teil 3",
        "Diskutieren.", "討論。",
        [sprechen_item(f"{pid}-sprechen3", 1,
            "Diskutieren Sie: Sollen Firmen Pausensport anbieten?",
            "討論：公司該不該提供休息運動？",
            ["Pro", "Contra", "Kompromiss"],
            "Pro: weniger Verspannung. Contra: Zeitdruck. Kompromiss: kurze freiwillige Einheiten.")],
    )
    return paper(
        pid, "B1", 3,
        "Goethe-Format B1 · Modellsatz 3 (leichter)",
        "考場版 B1 · 第3回（稍易）",
        150,
        [lesen1, lesen2, lesen3, lesen4, lesen5, hoeren1, hoeren2, hoeren3, hoeren4, schreiben1, schreiben2, sprechen1, sprechen2, sprechen3],
        difficulty="leichter",
    )


def b1_g4() -> dict[str, Any]:
    """etwas_schwerer — Ehrenamt / Freiwilligenarbeit."""
    pid = "b1-g4"
    lesen1 = section(
        "lesen1", "lesen", "Lesen Teil 1", "閱讀 Teil 1",
        "Blog/Meinung.", "部落格。",
        [
            mc(f"{pid}-lesen1", 1, "Hauptthema?", ["Steuern", "Ehrenamt und soziale Teilhabe", "Mode"], 1, "Ehrenamt。", "主題？"),
            tf(f"{pid}-lesen1", 2, "Ehrenamt ersetzt laut Text den Sozialstaat.", False, "ersetzt nicht。", "志工取代社福。"),
            mc(f"{pid}-lesen1", 3, "Was motiviert viele?", ["nur Geld", "Sinn und Begegnung", "Zwang"], 1, "Sinn und Begegnung。", "動機？"),
            tf(f"{pid}-lesen1", 4, "Zeitmangel ist kein Thema.", False, "Zeitmangel。", "時間不是問題。"),
            mc(f"{pid}-lesen1", 5, "Forderung an Kommunen?", ["weniger Transparenz", "verlässliche Koordination und Räume", "Verbote"], 1, "Koordination und Räume。", "對市府？"),
            mc(f"{pid}-lesen1", 6, "Warum erwähnt der Text „Anerkennung“?", ["unnötig", "hält Engagement langfristig", "nur Feiern"], 1, "長期投入需要肯定。", "為何提肯定？"),
        ],
        passage=_long(
            """
            Blog: Ehrenamt – sinnvoll, aber nicht selbstverständlich
            Freiwilliges Engagement stärkt Nachbarschaften, ersetzt aber nicht den Sozialstaat.
            Viele suchen Sinn und Begegnung; gleichzeitig ist Zeitmangel real, besonders bei
            Schichtarbeit und Care-Aufgaben. Kommunen sollten Koordination, Räume und
            unbürokratische Aufwandsentschädigungen sichern. Anerkennung – etwa durch
            Zertifikate und öffentliche Würdigung – hält Engagement langfristig. Kritikern,
            die Ehrenamt nur als Lückenbüßer sehen, entgegne ich: Es braucht beides –
            starke öffentliche Strukturen und Raum für Freiwilligkeit.
            """
        ),
        passage_zh="志工強化鄰里但不能取代社福；動機是意義與相遇，但時間壓力真實；市府應提供協調、空間與簡化津貼；肯定有助長期投入。",
    )
    lesen2 = section(
        "lesen2", "lesen", "Lesen Teil 2", "閱讀 Teil 2",
        "Anzeigen.", "廣告。",
        [
            mc(f"{pid}-lesen2", 1, "Sie möchten mit Kindern lesen.", ["A", "B", "C", "D"], 0, "A：Vorlesen。", "童書朗讀？"),
            mc(f"{pid}-lesen2", 2, "Sie können abends telefonieren.", ["A", "B", "C", "D"], 1, "B：Telefonkette。", "晚間電話？"),
            mc(f"{pid}-lesen2", 3, "Sie wollen Garten mit Geflüchteten.", ["A", "B", "C", "D"], 2, "C：Interkultureller Garten。", "園藝？"),
            mc(f"{pid}-lesen2", 4, "Sie suchen einmalig Umzugshilfe.", ["A", "B", "C", "D"], 3, "D：Umzugshilfe。", "單次搬家？"),
            mc(f"{pid}-lesen2", 5, "Welche braucht Führerschein?", ["A", "B", "C", "D"], 3, "D：Führerschein。", "要駕照？"),
            mc(f"{pid}-lesen2", 6, "Welche ist am Wochenende vormittags?", ["A", "B", "C", "D"], 0, "A：Sa 10 Uhr。", "週末上午？"),
        ],
        passage=(
            "A: Vorlesen in der Stadtbibliothek, Sa 10–12, mit Kindern, Einführungskurs Pflicht.\n"
            "B: Telefonkette Senioren, Di/Do 18–20, ruhige Stimme, Schulung online.\n"
            "C: Interkultureller Garten, Mi 17 Uhr, Werkzeug vor Ort, keine Vorkenntnisse.\n"
            "D: Umzugshilfe Sozialwohnungen, nach Absprache, Führerschein nötig, Aufwandsentschädigung."
        ),
        passage_zh="A 圖書館朗讀；B 長者電話關懷；C 跨文化園圃；D 搬家協助需駕照。",
    )
    lesen3 = section(
        "lesen3", "lesen", "Lesen Teil 3", "閱讀 Teil 3",
        "Magazin.", "雜誌。",
        [
            tf(f"{pid}-lesen3", 1, "Mentoring kann Bildungschancen verbessern.", True, "Bildungschancen。", "師徒制有助機會。"),
            tf(f"{pid}-lesen3", 2, "Das Projekt läuft ohne Evaluation.", False, "Evaluation nach einem Jahr。", "沒有評估。"),
            mc(f"{pid}-lesen3", 3, "Wer wird gepaart?", ["nur CEOs", "Studierende und Schüler/innen", "nur Touristen"], 1, "Studierende und Schüler。", "配對？"),
            tf(f"{pid}-lesen3", 4, "Ehrenamtliche erhalten ein Gehalt wie Vollzeit.", False, "Aufwandsentschädigung klein。", "等同全職薪資。"),
            mc(f"{pid}-lesen3", 5, "Herausforderung?", ["zu viele Räume", "Verlässlichkeit der Termine", "kein Interesse"], 1, "Verlässlichkeit。", "挑戰？"),
            mc(f"{pid}-lesen3", 6, "Was zeigt die Zwischenbilanz?", ["Abbruch überall", "bessere Orientierung bei Bewerbungen", "sinnlos"], 1, "Orientierung bei Bewerbungen。", "期中結論？"),
            tf(f"{pid}-lesen3", 7, "Eltern dürfen nicht informiert werden.", "nicht", "未禁止通知家長。", "不可通知家長。"),
        ],
        passage=_long(
            """
            Magazin: Mentoring in der Bildung
            Ein städtisches Projekt paart Studierende mit Schülerinnen und Schülern,
            die bei Hausaufgaben und Bewerbungen Unterstützung brauchen. Nach einem Jahr
            Evaluation zeigt die Zwischenbilanz: bessere Orientierung bei Praktika und
            Bewerbungen. Ehrenamtliche erhalten eine kleine Aufwandsentschädigung und Schulungen.
            Größte Herausforderung bleibt die Verlässlichkeit der Termine – deshalb gibt es
            nun Vertretungsregeln und eine digitale Terminerinnerung.
            """
        ),
        passage_zh="城市師徒計畫配對學生與需要課業／申請協助的中學生；一年評估顯示申請方向更清楚；有小額津貼與培訓；挑戰是守時，已加代理人與提醒。",
    )
    lesen4 = section(
        "lesen4", "lesen", "Lesen Teil 4", "閱讀 Teil 4",
        "Informationsschreiben.", "通知信。",
        [
            mc(f"{pid}-lesen4", 1, "Absender?", ["Bank", "Freiwilligenagentur Claratal", "Flughafen"], 1, "Freiwilligenagentur。", "寄件？"),
            mc(f"{pid}-lesen4", 2, "Was ist neu?", ["Steuererhöhung", "Online-Matching Portal", "Parkverbot"], 1, "Online-Matching。", "新措施？"),
            tf(f"{pid}-lesen4", 3, "Führungszeugnis kann nötig sein.", True, "erweitertes Führungszeugnis。", "可能要良民證。"),
            mc(f"{pid}-lesen4", 4, "Infoabend wann?", ["Mo 19 Uhr", "Fr 6 Uhr", "nur online Chat"], 0, "Montag 19 Uhr。", "說明會？"),
            mc(f"{pid}-lesen4", 5, "Anmeldung?", ["nur Brief", "über Portal bis Sonntag", "gar nicht"], 1, "über das Portal。", "報名？"),
            tf(f"{pid}-lesen4", 6, "Kinderprojekte ohne Schulung erlaubt.", False, "Schulung Pflicht bei Kindern。", "兒童專案免培訓。"),
        ],
        passage=_long(
            """
            Freiwilligenagentur Claratal – Rundschreiben
            Ab März starten wir ein Online-Matching-Portal für Einsatzorte und Freiwillige.
            Für Tätigkeiten mit Kindern ist eine Schulung Pflicht; teils benötigen wir ein
            erweitertes Führungszeugnis. Infoabend: Montag 19 Uhr im Rathaussaal.
            Anmeldung zum Portal bitte bis Sonntag. Fragen: freiwillig@claratal.de
            """
        ),
        passage_zh="Claratal 志工中心三月上線媒合平台；兒童相關需培訓，部分要良民證；週一 19 點說明會，週日前報名。",
    )
    lesen5 = section(
        "lesen5", "lesen", "Lesen Teil 5", "閱讀 Teil 5",
        "Forum.", "論壇。",
        [
            mc(f"{pid}-lesen5", 1, "Nadjas Punkt?", ["Ehrenamt sinnlos", "Anerkennung und klare Aufgaben", "nur Geld"], 1, "Anerkennung … Aufgaben。", "Nadja？"),
            tf(f"{pid}-lesen5", 2, "Chris bricht oft Termine ab.", True, "zu oft absagen。", "Chris 常取消。"),
            mc(f"{pid}-lesen5", 3, "Lösung von Ines?", ["Verbote", "Vertretung und Erinnerungen", "mehr Chaos"], 1, "Vertretung。", "Ines？"),
            tf(f"{pid}-lesen5", 4, "Alle lehnen Zertifikate ab.", False, "Nadja findet Zertifikate gut。", "都反對證書。"),
            mc(f"{pid}-lesen5", 5, "Ton des Threads?", ["nur Streit", "konstruktiv mit Kritik", "Spam"], 1, "建設性批評。", "氛圍？"),
            mc(f"{pid}-lesen5", 6, "Was fehlt manchen Organisationen laut Chris?", ["Party", "klare Einarbeitung", "mehr Fotos"], 1, "klare Einarbeitung。", "缺什麼？"),
        ],
        passage=(
            "Forum Ehrenamt&Stadt\n"
            "Nadja: Ohne Anerkennung und klare Aufgaben verlieren wir Leute. Zertifikate helfen.\n"
            "Chris: Stimmt. Manche Organisationen erklären nichts – keine Einarbeitung. Und ich muss zugeben: "
            "Ich sage zu oft ab, das ist unfair.\n"
            "Ines: Deshalb Vertretungsregeln und Erinnerungs-Mails. Verlässlichkeit ist Teamwork."
        ),
        passage_zh="Nadja 強調肯定與清楚任務；Chris 坦承常取消且組織缺乏帶領；Ines 主張代理人與提醒。",
    )
    hoeren1 = section(
        "hoeren1", "hoeren", "Hören Teil 1", "聽力 Teil 1",
        "Interview.", "訪談。",
        [
            mc(f"{pid}-hoeren1", 1, "Rolle der Agentur?", ["nur Feiern", "vermitteln und schulen", "Steuern eintreiben"], 1, "vermitteln und schulen。", "角色？"),
            tf(f"{pid}-hoeren1", 2, "Jeder Einsatz braucht Führungszeugnis.", False, "nur bestimmte Bereiche。", "全部都要良民證。"),
            mc(f"{pid}-hoeren1", 3, "Größtes Problem?", ["zu viel Geld", "Zeitkonflikte", "kein Interesse"], 1, "Zeitkonflikte。", "最大問題？"),
            mc(f"{pid}-hoeren1", 4, "Was hilft?", ["keine Planung", "realistische Stundenangaben", "Dauerstress"], 1, "realistische Stunden。", "什麼有用？"),
            mc(f"{pid}-hoeren1", 5, "Digitales Matching?", ["abgelehnt", "ab März", "schon gestern Pflicht"], 1, "ab März。", "數位媒合？"),
            tf(f"{pid}-hoeren1", 6, "Sie sieht Ehrenamt als Ersatz für Fachkräfte.", False, "kein Ersatz für Fachkräfte。", "把志工當專業人力替代。"),
        ],
        audio_text=(
            "Reporter: Was macht die Freiwilligenagentur? "
            "Leiterin: Wir vermitteln und schulen. Führungszeugnisse nur in bestimmten Bereichen. "
            "Größtes Problem sind Zeitkonflikte – deshalb realistische Stundenangaben. "
            "Online-Matching startet ab März. Wichtig: Ehrenamt ist kein Ersatz für Fachkräfte."
        ),
    )
    hoeren2 = section(
        "hoeren2", "hoeren", "Hören Teil 2", "聽力 Teil 2",
        "Gespräch.", "對話。",
        [
            mc(f"{pid}-hoeren2", 1, "Was will Lara ausprobieren?", ["Vorlesen", "Steuerberatung", "Taxi"], 0, "Vorlesen。", "想試？"),
            mc(f"{pid}-hoeren2", 2, "Wann Einführung?", ["Sa 10 Uhr", "So 20 Uhr", "Fr 6 Uhr"], 0, "Samstag um 10。", "導覽？"),
            tf(f"{pid}-hoeren2", 3, "Ben hilft schon im Gartenprojekt.", True, "im Garten。", "Ben 已在園圃。"),
            mc(f"{pid}-hoeren2", 4, "Laras Sorge?", ["zu leicht", "ob sie Zeit hält", "kein Deutsch"], 1, "ob ich die Zeit schaffe。", "擔心？"),
            mc(f"{pid}-hoeren2", 5, "Bens Rat?", ["sofort 20 Std.", "klein starten", "abschrecken"], 1, "klein starten。", "建議？"),
            tf(f"{pid}-hoeren2", 6, "Sie treffen sich vor der Bibliothek.", True, "vor der Bibliothek。", "在圖書館前碰面。"),
        ],
        audio_text=(
            "Lara: Ich möchte Vorlesen ausprobieren. "
            "Ben: Die Einführung ist Samstag um 10. Wir treffen uns vor der Bibliothek. "
            "Ich helfe schon im Garten. Starte klein, wenn du unsicher bist, ob du die Zeit schaffst."
        ),
    )
    hoeren3 = section(
        "hoeren3", "hoeren", "Hören Teil 3", "聽力 Teil 3",
        "Durchsage.", "廣播。",
        [
            mc(f"{pid}-hoeren3", 1, "Was entfällt?", ["Garten", "Telefonkette heute", "Infoabend"], 1, "Telefonkette entfällt。", "取消？"),
            mc(f"{pid}-hoeren3", 2, "Grund?", ["Technikstörung", "Wetter", "Streik"], 0, "Technikstörung。", "原因？"),
            mc(f"{pid}-hoeren3", 3, "Ersatz?", ["Do 18 Uhr", "nie", "nur Brief"], 0, "Donnerstag 18 Uhr。", "補班？"),
            tf(f"{pid}-hoeren3", 4, "Man soll sich im Portal abmelden.", True, "im Portal abmelden。", "要在平台請假。"),
            mc(f"{pid}-hoeren3", 5, "Fragen an?", ["Polizei", "freiwillig@claratal.de", "niemanden"], 1, "E-Mail。", "詢問？"),
            mc(f"{pid}-hoeren3", 6, "Was bleibt geplant?", ["nichts", "Infoabend Montag", "nur Party"], 1, "Infoabend am Montag。", "仍進行？"),
        ],
        audio_text=(
            "Achtung Freiwillige: Die Telefonkette entfällt heute wegen einer Technikstörung. "
            "Ersatztermin ist Donnerstag um 18 Uhr. Bitte melden Sie sich im Portal ab. "
            "Der Infoabend am Montag findet wie geplant statt. Fragen an freiwillig@claratal.de."
        ),
    )
    hoeren4 = section(
        "hoeren4", "hoeren", "Hören Teil 4", "聽力 Teil 4",
        "Diskussion.", "討論。",
        [
            mc(f"{pid}-hoeren4", 1, "Kim fordert …", ["weniger Schulung", "bessere Einarbeitung", "Sofortgehalt"], 1, "bessere Einarbeitung。", "Kim？"),
            tf(f"{pid}-hoeren4", 2, "Paul sieht Zertifikate als sinnlos.", False, "Zertifikate sinnvoll。", "Paul 覺證書無用。"),
            mc(f"{pid}-hoeren4", 3, "Streitpunkt?", ["Farbe der T-Shirts", "ob Ehrenamt Lücken füllt", "Wetter"], 1, "Lückenbüßer。", "爭議？"),
            mc(f"{pid}-hoeren4", 4, "Kompromiss?", ["abschaffen", "Ehrenamt plus starke Fachstrukturen", "nur Zwang"], 1, "beides。", "折衷？"),
            tf(f"{pid}-hoeren4", 5, "Beide wollen komplett aufhören.", False, "weiter verbessern。", "兩人都要停。"),
        ],
        audio_text=(
            "Kim: Wir brauchen bessere Einarbeitung, sonst frustrieren Leute. "
            "Paul: Zertifikate sind sinnvoll. Aber Ehrenamt darf keine Lücken im Sozialstaat füllen. "
            "Kim: Einverstanden – Freiwilligkeit plus starke Fachstrukturen. Lass uns das verbessern, nicht aufgeben."
        ),
    )
    schreiben1 = section(
        "schreiben1", "schreiben", "Schreiben Teil 1", "寫作 Teil 1",
        "Formell.", "正式寫作。",
        [
            schreiben_item(
                f"{pid}-schreiben1", 1,
                "Schreiben Sie an die Freiwilligenagentur:\n"
                "• Interesse am Mentoring\n• Ihre zeitlichen Möglichkeiten\n• Fragen zu Schulung und Führungszeugnis",
                "寫給志工中心：對師徒制有興趣、可配合時間、問培訓與良民證。",
                100,
                "Sehr geehrte Damen und Herren,\nich interessiere mich für das Mentoring-Projekt. "
                "Ich könnte wöchentlich zwei Stunden am Abend einsetzen. Bitte informieren Sie mich "
                "über die Schulung und ob ein erweitertes Führungszeugnis nötig ist.\n"
                "Mit freundlichen Grüßen",
                ["興趣", "時間", "培訓／證明詢問", "約 100 字"],
            )
        ],
    )
    schreiben2 = section(
        "schreiben2", "schreiben", "Schreiben Teil 2", "寫作 Teil 2",
        "Antwort an Freund/in.", "回覆朋友。",
        [
            schreiben_item(
                f"{pid}-schreiben2", 1,
                "Ihre Freundin fragt, ob Ehrenamt neben dem Job machbar ist. Antworten Sie:\n"
                "• Ihre Meinung\n• 2 praktische Tipps\n• Angebot, gemeinsam Infoabend zu besuchen",
                "朋友問工作外當志工是否可行：給看法、兩點實用建議、邀一起去說明會。",
                100,
                "Liebe Nadja,\nich finde Ehrenamt machbar, wenn man klein startet und Termine realistisch plant. "
                "Tipp 1: feste Wochentage. Tipp 2: Vertretung klären. Gehen wir zusammen zum Infoabend am Montag?\n"
                "Liebe Grüße",
                ["看法", "兩點建議", "邀約"],
            )
        ],
    )
    sprechen1 = section(
        "sprechen1", "sprechen", "Sprechen Teil 1", "口說 Teil 1",
        "Planen.", "規劃。",
        [sprechen_item(f"{pid}-sprechen1", 1,
            "Planen Sie einen Ehrenamts-Infoabend: Zielgruppe, Programm, Materialien.",
            "規劃志工說明會：對象、流程、材料。",
            ["Zielgruppe", "Programm", "Material", "Nachkontakt"],
            "Zielgruppe: Berufstätige. Programm: Kurzvortrag, drei Einsatzbeispiele, Fragen. Flyer und Portal-Zugang bereitlegen.")],
    )
    sprechen2 = section(
        "sprechen2", "sprechen", "Sprechen Teil 2", "口說 Teil 2",
        "Kurzvortrag.", "短講。",
        [sprechen_item(f"{pid}-sprechen2", 1,
            "Warum ist Ehrenamt wichtig – und wo liegen Grenzen?",
            "為何志工重要、界線在哪？",
            ["Nutzen", "Grenzen", "Beispiel"],
            "Ehrenamt schafft Begegnung, ersetzt aber keine Fachkräfte. Beispiel: Mentoring ergänzt Schule, ersetzt sie nicht.")],
    )
    sprechen3 = section(
        "sprechen3", "sprechen", "Sprechen Teil 3", "口說 Teil 3",
        "Diskutieren.", "討論。",
        [sprechen_item(f"{pid}-sprechen3", 1,
            "Diskutieren Sie: Sollte Ehrenamt stärker anerkannt werden (Zertifikate, Freistellung)?",
            "討論：是否該更肯定志工（證書、公假）？",
            ["Pro", "Contra", "Kompromiss"],
            "Pro: Motivation. Contra: Bürokratie. Kompromiss: einfache Zertifikate, begrenzte Freistellung.")],
    )
    return paper(
        pid, "B1", 4,
        "Goethe-Format B1 · Modellsatz 4 (etwas schwerer)",
        "考場版 B1 · 第4回（稍難）",
        150,
        [lesen1, lesen2, lesen3, lesen4, lesen5, hoeren1, hoeren2, hoeren3, hoeren4, schreiben1, schreiben2, sprechen1, sprechen2, sprechen3],
        difficulty="etwas_schwerer",
    )


def b2_g3() -> dict[str, Any]:
    """leichter — Nachhaltige Mobilität / ÖPNV."""
    pid = "b2-g3"
    lesen1 = section(
        "lesen1", "lesen", "Lesen Teil 1", "閱讀 Teil 1",
        "Kommentar.", "評論。",
        [
            mc(f"{pid}-lesen1", 1, "Kernthese?", ["Autos immer besser", "ÖPNV braucht Verlässlichkeit", "Flugzwang"], 1, "Verlässlichkeit。", "核心？"),
            tf(f"{pid}-lesen1", 2, "Ticketpreise allein lösen alles.", False, "nicht allein。", "票價就能解決。"),
            mc(f"{pid}-lesen1", 3, "Was frustriert Nutzende?", ["zu viele Züge", "Ausfälle und unklare Infos", "zu viel Personal"], 1, "Ausfälle。", "挫折？"),
            tf(f"{pid}-lesen1", 4, "Radverkehr wird erwähnt.", True, "Radwege。", "提到單車。"),
            mc(f"{pid}-lesen1", 5, "Politische Konsequenz?", ["nur Appelle", "Investition und Taktverdichtung", "Abbau"], 1, "Investition。", "政策？"),
            tf(f"{pid}-lesen1", 6, "Der Autor lehnt Umstiege grundsätzlich ab.", False, "Umsteigen OK wenn Anschlüsse stimmen。", "完全反對轉乘。"),
        ],
        passage=_long(
            """
            Kommentar: Mobilität jenseits des Statussymbols
            Wer den Autoverkehr reduzieren will, muss den öffentlichen Verkehr verlässlich machen.
            Günstige Tickets helfen, ersetzen aber keine dichten Takte und verständliche Störungenkommunikation.
            Ausfälle und unklare Ansagen treiben Menschen zurück ins Auto. Parallel brauchen Städte
            sichere Radwege und Park-and-Ride. Umsteigen ist akzeptabel, wenn Anschlüsse funktionieren.
            Das ist weniger Ideologie als Infrastrukturpolitik: Investition und Taktverdichtung statt Symbolik.
            """
        ),
        passage_zh="若要減汽車，大眾運輸須可靠；便宜票不能取代班次與清楚資訊；故障與不清廣播把人推回開車；需單車道與轉乘停車；轉乘可接受若接駁準時。",
    )
    lesen2 = section(
        "lesen2", "lesen", "Lesen Teil 2", "閱讀 Teil 2",
        "Überschriften zuordnen.", "標題配對。",
        [
            mc(f"{pid}-lesen2", 1, "Text über nächtliche Buslücken?", ["A", "B", "C", "D", "E"], 0, "A。", "夜間公車？"),
            mc(f"{pid}-lesen2", 2, "Text über Fahrradstraßen Streit?", ["A", "B", "C", "D", "E"], 1, "B。", "單車街爭議？"),
            mc(f"{pid}-lesen2", 3, "Text über Jobticket Unternehmen?", ["A", "B", "C", "D", "E"], 2, "C。", "通勤票？"),
            mc(f"{pid}-lesen2", 4, "Text über barrierefreie Bahnhöfe?", ["A", "B", "C", "D", "E"], 3, "D。", "無障礙車站？"),
            mc(f"{pid}-lesen2", 5, "Text über Carsharing in Vororten?", ["A", "B", "C", "D", "E"], 4, "E。", "郊區共享車？"),
        ],
        passage=(
            "Mögliche Überschriften:\n"
            "A Nachtnetz mit Lücken\n"
            "B Konflikt um Fahrradstraßen\n"
            "C Jobticket als Standortfaktor\n"
            "D Bahnhöfe ohne stufenfreien Zugang\n"
            "E Carsharing jenseits der Innenstadt"
        ),
        passage_zh="標題選項：夜間路網缺口、單車街衝突、通勤票、無障礙車站、郊區共享車。",
    )
    lesen3 = section(
        "lesen3", "lesen", "Lesen Teil 3", "閱讀 Teil 3",
        "Meinungen zuordnen.", "意見歸類。",
        [
            mc(f"{pid}-lesen3", 1, "Wer fordert dichtere Takte vor Preissenkung?", ["Lea", "Omar", "Sven"], 0, "Lea。", "誰先要班次？"),
            mc(f"{pid}-lesen3", 2, "Wer betont Sicherheit an Haltestellen?", ["Lea", "Omar", "Sven"], 1, "Omar。", "誰提安全？"),
            mc(f"{pid}-lesen3", 3, "Wer will mehr Parkraum in der City?", ["Lea", "Omar", "Sven"], 2, "Sven。", "誰要更多市區停車？"),
            tf(f"{pid}-lesen3", 4, "Lea lehnt ÖPNV ab.", False, "sie will dichtere Takte。", "Lea 反對大眾運輸。"),
            mc(f"{pid}-lesen3", 5, "Gemeinsamer Nenner Lea/Omar?", ["nur Autos", "Qualität vor Symbolpolitik", "Abbau"], 1, "品質優先。", "共同點？"),
            mc(f"{pid}-lesen3", 6, "Svens Kernargument?", ["Klimaschutz first", "Einzelhandel braucht Erreichbarkeit per Auto", "Fahrradzwang"], 1, "Einzelhandel。", "Sven？"),
        ],
        passage=_long(
            """
            Forum Mobilität
            Lea: Erst Takt und Verlässlichkeit, dann über Preise reden – sonst bleibt das Ticket symbolisch.
            Omar: Stimme zu. Und bitte Beleuchtung und Sicherheit an Haltestellen, sonst meiden viele den Bus abends.
            Sven: Ohne Parkplätze stirbt der Einzelhandel in der City. ÖPNV ist schön, aber nicht für alle Einkäufe.
            """
        ),
        passage_zh="Lea 要先班次可靠；Omar 強調候車安全；Sven 擔心市區停車影響零售。",
    )
    lesen4 = section(
        "lesen4", "lesen", "Lesen Teil 4", "閱讀 Teil 4",
        "Infotext.", "資訊文本。",
        [
            tf(f"{pid}-lesen4", 1, "Das Land fördert Taktverdichtung.", True, "fördert Taktverdichtung。", "邦補助加密班次。"),
            mc(f"{pid}-lesen4", 2, "Antragsfrist?", ["laufend ohne Ende", "jeweils Quartalsende", "nur 2030"], 1, "Quartalsende。", "申請截止？"),
            tf(f"{pid}-lesen4", 3, "Private Personen beantragen direkt.", False, "Kommunen und Verbünde。", "個人直接申請。"),
            mc(f"{pid}-lesen4", 4, "Schwerpunkt neben Bus?", ["nur Flug", "barrierefreie Stationen", "Autobahnen neu"], 1, "barrierefrei。", "重點？"),
            mc(f"{pid}-lesen4", 5, "Evaluation wann?", ["nie", "nach drei Jahren", "täglich"], 1, "nach drei Jahren。", "評估？"),
        ],
        passage=_long(
            """
            Infotext: Förderprogramm „Dichte Takte“
            Das Land fördert Kommunen und Verkehrsverbünde bei Taktverdichtung und barrierefreien Stationen.
            Anträge jeweils zum Quartalsende. Private Personen können nicht direkt beantragen.
            Nach drei Jahren folgt eine Evaluation zu Fahrgastzahlen und Pünktlichkeit.
            """
        ),
        passage_zh="邦補助市鎮／運輸聯盟加密班次與無障礙站點；季末申請；個人不可直接申請；三年後評估運量與準點。",
    )
    lesen5 = section(
        "lesen5", "lesen", "Lesen Teil 5", "閱讀 Teil 5",
        "Kommentar Vertiefung.", "進階評論。",
        [
            tf(f"{pid}-lesen5", 1, "Homeoffice macht Mobilitätspolitik irrelevant.", False, "ändert Muster, ersetzt nicht。", "在家上班讓交通政策無關。"),
            mc(f"{pid}-lesen5", 2, "Was verändert Hybridarbeit?", ["gar nichts", "Stoßzeiten und Nachfrage", "Geburtensrate"], 1, "Stoßzeiten。", "混合辦公？"),
            mc(f"{pid}-lesen5", 3, "Risiko laut Text?", ["zu viel Flexibilität planen", "Angebote an alten Spitzen ausrichten", "zu viele Züge nachts"], 1, "按舊尖峰配置。", "風險？"),
            tf(f"{pid}-lesen5", 4, "Datenbasierte Planung wird befürwortet.", True, "datenbasierte。", "支持數據規劃。"),
            mc(f"{pid}-lesen5", 5, "Fazit?", ["nur Auto", "Angebot an reale Nachfrage koppeln", "ÖPNV abschaffen"], 1, "Nachfrage。", "結論？"),
            mc(f"{pid}-lesen5", 6, "Tone?", ["polemisch gegen Fahrgäste", "abwägend, politikbezogen", "reines Marketing"], 1, "權衡政策。", "語氣？"),
        ],
        passage=_long(
            """
            Kommentar: Hybridarbeit und der Fahrplan
            Homeoffice macht Mobilitätspolitik nicht überflüssig – es verschiebt Stoßzeiten und Nachfrage.
            Wer Angebote weiter an alten morgendlichen Spitzen ausrichtet, riskiert leere Züge und volle Straßen mittags.
            Nötig sind datenbasierte Fahrpläne, flexiblere Anschlüsse und ehrliche Kommunikation bei Störungen.
            Kurz: Infrastruktur an reale Nutzung koppeln, nicht an Gewohnheiten von 2015.
            """
        ),
        passage_zh="在家上班改變尖峰而非取消交通政策；若仍按舊早高峰配置，可能列車空、中午塞車；需數據化班表與清楚故障資訊。",
    )
    hoeren1 = section(
        "hoeren1", "hoeren", "Hören Teil 1", "聽力 Teil 1",
        "Interview.", "訪談。",
        [
            mc(f"{pid}-hoeren1", 1, "Priorität der Expertin?", ["nur Billing", "Pünktlichkeit und Info", "Werbeclips"], 1, "Pünktlichkeit。", "優先？"),
            tf(f"{pid}-hoeren1", 2, "Sie hält Ticketpreise für irrelevant.", False, "wichtig, aber nicht allein。", "覺票價無關。"),
            mc(f"{pid}-hoeren1", 3, "Beispiel Maßnahme?", ["Takt 10 Min. Kernnetz", "alle Linien streichen", "nur Nachtflug"], 0, "Zehn-Minuten-Takt。", "措施？"),
            mc(f"{pid}-hoeren1", 4, "Bürgerbeteiligung?", ["unnötig", "früh bei Linienänderungen", "nur nach Bauende"], 1, "früh。", "參與？"),
            mc(f"{pid}-hoeren1", 5, "Haltung zu Autoverboten?", ["Dogma", "punktuell mit Alternativen", "immer flächendeckend sofort"], 1, "punktuell。", "禁車？"),
        ],
        audio_text=(
            "Moderator: Was ist Ihre Priorität? "
            "Expertin: Pünktlichkeit und klare Informationen. Preise sind wichtig, aber nicht allein. "
            "Im Kernnetz ein Zehn-Minuten-Takt. Bürgerbeteiligung früh bei Linienänderungen. "
            "Autoverbote nur punktuell, wenn Alternativen stehen."
        ),
    )
    hoeren2 = section(
        "hoeren2", "hoeren", "Hören Teil 2", "聽力 Teil 2",
        "Gespräch.", "對話。",
        [
            mc(f"{pid}-hoeren2", 1, "Problem von Nina?", ["Zug zu früh", "Anschluss verpasst", "kein Ticketwunsch"], 1, "Anschluss verpasst。", "問題？"),
            tf(f"{pid}-hoeren2", 2, "App zeigte korrekte Störung.", False, "App zeigte nichts。", "App 有正確資訊。"),
            mc(f"{pid}-hoeren2", 3, "Was fordert Nico?", ["mehr Werbung", "Echtzeitansagen", "weniger Personal"], 1, "Echtzeitansagen。", "Nico？"),
            mc(f"{pid}-hoeren2", 4, "Alternative heute?", ["Taxi teilen", "Leihfahrrad + S-Bahn", "Flug"], 1, "Leihfahrrad。", "替代？"),
            mc(f"{pid}-hoeren2", 5, "Ton?", ["nur Schimpfen", "ärgerlich aber lösungsorientiert", "gleichgültig"], 1, "想解法。", "語氣？"),
        ],
        audio_text=(
            "Nina: Ich habe den Anschluss verpasst, und die App zeigte keine Störung. "
            "Nico: Genau deshalb brauchen wir Echtzeitansagen. "
            "Nina: Heute nehme ich Leihfahrrad plus S-Bahn. Nervig – aber lösbar, wenn die Info stimmt."
        ),
    )
    hoeren3 = section(
        "hoeren3", "hoeren", "Hören Teil 3", "聽力 Teil 3",
        "Vortrag kurz.", "短講。",
        [
            mc(f"{pid}-hoeren3", 1, "Thema?", ["Kochrezepte", "Park-and-Ride Wirkung", "Mode"], 1, "Park-and-Ride。", "主題？"),
            tf(f"{pid}-hoeren3", 2, "Ohne gute Zubringer scheitert P+R.", True, "ohne Zubringer。", "沒接駁會失敗。"),
            mc(f"{pid}-hoeren3", 3, "Messgröße?", ["nur Likes", "Umstiegquote und Pkw-km", "Haarfarbe"], 1, "Umstiegquote。", "指標？"),
            mc(f"{pid}-hoeren3", 4, "Kritik?", ["zu billig immer", "manchmal zu weit außerhalb", "zu viele Züge"], 1, "zu weit。", "批評？"),
            tf(f"{pid}-hoeren3", 5, "Referent lehnt Evaluation ab.", False, "regelmäßig evaluieren。", "反對評估。"),
        ],
        audio_text=(
            "Referent: Park-and-Ride wirkt nur mit guten Zubringern. "
            "Wir messen Umstiegquote und eingesparte Pkw-Kilometer. "
            "Kritik: Manche Anlagen liegen zu weit außerhalb. Deshalb regelmäßig evaluieren und nachsteuern."
        ),
    )
    hoeren4 = section(
        "hoeren4", "hoeren", "Hören Teil 4", "聽力 Teil 4",
        "Podium.", "論壇。",
        [
            mc(f"{pid}-hoeren4", 1, "Ayse betont …", ["nur Autobahn", "soziale Tarife", "Fluglärm egal"], 1, "soziale Tarife。", "Ayse？"),
            tf(f"{pid}-hoeren4", 2, "Bert will ÖPNV privatisieren ohne Regeln.", False, "öffentliche Steuerung behalten。", "要無管制私有化。"),
            mc(f"{pid}-hoeren4", 3, "Konflikt?", ["Tarif vs. Flächenverteilung", "Frisur", "Kaffee"], 0, "Tarif und Fläche。", "衝突？"),
            mc(f"{pid}-hoeren4", 4, "Einigungspunkt?", ["nichts", "Daten offenlegen", "sofort alles verbieten"], 1, "Daten offenlegen。", "共識？"),
            tf(f"{pid}-hoeren4", 5, "Beide wollen Fahrgäste ignorieren.", False, "Fahrgastperspektive。", "都要忽略乘客。"),
        ],
        audio_text=(
            "Ayse: Soziale Tarife sind zentral, sonst bleibt Mobilität ungerecht. "
            "Bert: Einverstanden bei Transparenz – aber öffentliche Steuerung behalten, keine Privatisierung ohne Regeln. "
            "Ayse: Dann legen wir Daten offen und planen mit der Fahrgastperspektive. "
            "Bert: Ja – Tarif und Flächenverteilung gehören zusammen."
        ),
    )
    schreiben1 = section(
        "schreiben1", "schreiben", "Schreiben Teil 1", "寫作 Teil 1",
        "Forumskommentar.", "論壇評論。",
        [
            schreiben_item(
                f"{pid}-schreiben1", 1,
                "Forumsthema „ÖPNV zuerst?“:\n"
                "• Position\n• ein Argument mit lokalem Bezug\n• ein Einwand und kurze Replik",
                "論壇「大眾運輸優先？」：立場、一個在地論點、一個反方與簡短回應。",
                100,
                "Ich bin für ÖPNV-Priorität. In meiner Stadt scheitert Umstieg an Ausfällen, nicht nur am Preis. "
                "Einwand: Einzelhandel brauche Parkplätze. Replik: Erreichbarkeit ja – aber mit P+R und Takten, nicht mit Dauerstau.",
                ["立場", "在地論點", "反方與回應"],
            )
        ],
    )
    schreiben2 = section(
        "schreiben2", "schreiben", "Schreiben Teil 2", "寫作 Teil 2",
        "Formeller Brief.", "正式信。",
        [
            schreiben_item(
                f"{pid}-schreiben2", 1,
                "Schreiben Sie an den Verkehrsverbund:\n"
                "• Forderung nach Echtzeitinformationen\n• Beispiel einer Fehlkommunikation\n• Bitte um Stellungnahme und Zeitplan",
                "寫給運輸聯盟：要求即時資訊、舉一次失誤、請說明與時程。",
                150,
                "Sehr geehrte Damen und Herren,\nich fordere verlässliche Echtzeitinformationen bei Störungen. "
                "Kürzlich zeigte die App keine Verspätung, obwohl der Anschluss ausfiel. "
                "Bitte nehmen Sie Stellung und nennen Sie einen Zeitplan für Verbesserungen.\n"
                "Mit freundlichen Grüßen",
                ["要求", "實例", "請回覆時程", "約 150 字"],
            )
        ],
    )
    sprechen1 = section(
        "sprechen1", "sprechen", "Sprechen Teil 1", "口說 Teil 1",
        "Planen.", "規劃。",
        [sprechen_item(f"{pid}-sprechen1", 1,
            "Planen Sie eine Kampagne „Umsteigen leicht“: Zielgruppe, Kanäle, Kennzahlen.",
            "規劃「輕鬆轉乘」活動：對象、管道、指標。",
            ["Zielgruppe", "Kanäle", "Kennzahlen", "Pilotlinie"],
            "Zielgruppe: Pendler. Kanäle: App-Push und Haltestellen. Kennzahl: Umstiegquote. Pilot: eine S-Bahn-Linie.")],
    )
    sprechen2 = section(
        "sprechen2", "sprechen", "Sprechen Teil 2", "口說 Teil 2",
        "Kurzvortrag.", "短講。",
        [sprechen_item(f"{pid}-sprechen2", 1,
            "Kurzvortrag: Warum Verlässlichkeit wichtiger ist als Symboltickets.",
            "短講：為何可靠比象徵性票價更重要。",
            ["These", "Beispiel", "Fazit"],
            "Günstige Tickets ohne Takt bleiben Symbolik. Beispiel: leere Versprechen bei Ausfällen. Fazit: erst Qualität, dann Preis.")],
    )
    return paper(
        pid, "B2", 3,
        "Goethe-Format B2 · Modellsatz 3 (leichter)",
        "考場版 B2 · 第3回（稍易）",
        170,
        [lesen1, lesen2, lesen3, lesen4, lesen5, hoeren1, hoeren2, hoeren3, hoeren4, schreiben1, schreiben2, sprechen1, sprechen2],
        difficulty="leichter",
    )


def b2_g4() -> dict[str, Any]:
    """etwas_schwerer — Fernstudium / Bildungsgerechtigkeit."""
    pid = "b2-g4"
    lesen1 = section(
        "lesen1", "lesen", "Lesen Teil 1", "閱讀 Teil 1",
        "Kommentar.", "評論。",
        [
            mc(f"{pid}-lesen1", 1, "Kernthese?", ["Campus unnötig immer", "Fernstudium braucht didaktische Qualität", "nur Prestige"], 1, "didaktische Qualität。", "核心？"),
            tf(f"{pid}-lesen1", 2, "Zugang allein garantiert Erfolg.", False, "Zugang ≠ Erfolg。", "有入學就成功。"),
            mc(f"{pid}-lesen1", 3, "Risiko digitaler Angebote?", ["zu viel Betreuung", "Drop-out bei Isolation", "kein Internetproblem"], 1, "Isolation。", "風險？"),
            tf(f"{pid}-lesen1", 4, "Präsenzphasen werden abgelehnt.", False, "hybride Präsenz sinnvoll。", "拒絕面授。"),
            mc(f"{pid}-lesen1", 5, "Bildungsgerechtigkeit heißt laut Text …", ["nur Online-Videos", "Ressourcen und Begleitung", "Auswahl der Reichsten"], 1, "Ressourcen und Begleitung。", "教育公平？"),
            mc(f"{pid}-lesen1", 6, "Welche Implikation für Hochschulen?", ["Betreuung abbauen", "Tutorien und Feedback skalieren", "nur Marketing"], 1, "Tutorien。", "對高校？"),
            tf(f"{pid}-lesen1", 7, "Der Text hält Fernstudium für per se minderwertig.", False, "Qualität machbar。", "認定遠距本質低劣。"),
        ],
        passage=_long(
            """
            Kommentar: Fernstudium ist kein Automatismus für Bildungsgerechtigkeit
            Digitale Studienangebote öffnen Türen für Berufstätige und Care-Verantwortliche – doch Zugang
            allein garantiert keinen Abschluss. Isolation, unklare Arbeitsaufträge und fehlendes Feedback
            treiben Drop-outs. Hybride Präsenzphasen und verbindliche Tutorien sind keine Luxusbeigabe,
            sondern Voraussetzung, wenn Fernstudium Qualität beansprucht. Bildungsgerechtigkeit bedeutet
            deshalb: Ressourcen für Begleitung bereitstellen, nicht nur Videos hochladen. Hochschulen, die
            Betreuung abbauen und gleichzeitig „flexibel“ werben, verschieben Kosten auf Studierende.
            """
        ),
        passage_zh="遠距為在職／照顧者開門，但入學≠完成；孤立與缺乏回饋提高輟學；混成面授與輔導是品質前提；教育公平要資源陪伴，而非只上傳影片。",
    )
    lesen2 = section(
        "lesen2", "lesen", "Lesen Teil 2", "閱讀 Teil 2",
        "Überschriften.", "標題。",
        [
            mc(f"{pid}-lesen2", 1, "Text zu Studiengebühren und Teilzeit?", ["A", "B", "C", "D", "E"], 0, "A。", "學費兼職？"),
            mc(f"{pid}-lesen2", 2, "Text zu Proctoring-Kritik?", ["A", "B", "C", "D", "E"], 1, "B。", "線上監考？"),
            mc(f"{pid}-lesen2", 3, "Text zu Bibliothekszugang remote?", ["A", "B", "C", "D", "E"], 2, "C。", "遠端圖書館？"),
            mc(f"{pid}-lesen2", 4, "Text zu Anerkennung von Vorleistungen?", ["A", "B", "C", "D", "E"], 3, "D。", "學分抵免？"),
            mc(f"{pid}-lesen2", 5, "Text zu mentaler Gesundheit online?", ["A", "B", "C", "D", "E"], 4, "E。", "心理健康？"),
            mc(f"{pid}-lesen2", 6, "Welche Überschrift passt zu Datenschutz bei Prüfungen?", ["A", "B", "C", "D", "E"], 1, "B Proctoring。", "監考個資？"),
        ],
        passage=(
            "Mögliche Überschriften:\n"
            "A Gebührenfalle Teilzeitstudium\n"
            "B Proctoring unter Beobachtung\n"
            "C Fernleihe und digitale Bibliothek\n"
            "D Anrechnung bleibt Puzzle\n"
            "E Mentale Belastung jenseits des Campus"
        ),
        passage_zh="標題：兼職學費陷阱、線上監考、數位圖書館、學分抵免拼圖、校園外心理負擔。",
    )
    lesen3 = section(
        "lesen3", "lesen", "Lesen Teil 3", "閱讀 Teil 3",
        "Meinungen.", "意見。",
        [
            mc(f"{pid}-lesen3", 1, "Wer fordert bezahlte Lernzeit im Job?", ["Iris", "Tom", "Elena"], 0, "Iris。", "誰要帶薪學習？"),
            mc(f"{pid}-lesen3", 2, "Wer warnt vor Scheinflexibilität?", ["Iris", "Tom", "Elena"], 1, "Tom。", "誰警告假彈性？"),
            mc(f"{pid}-lesen3", 3, "Wer betont barrierefreie Plattformen?", ["Iris", "Tom", "Elena"], 2, "Elena。", "誰提無障礙？"),
            tf(f"{pid}-lesen3", 4, "Tom feiert reine Video-Uploads als Lösung.", False, "Scheinflexibilität。", "Tom 讚成只上傳影片。"),
            mc(f"{pid}-lesen3", 5, "Iris' Zusatzpunkt?", ["weniger Betreuung", "Kinderbetreuung an Präsenztagen", "höhere Hürden"], 1, "Kinderbetreuung。", "Iris 加點？"),
            mc(f"{pid}-lesen3", 6, "Gemeinsam ablehnen sie …", ["Tutorien", "reine Marketing-Flexibilität", "Stipendien"], 1, "行銷式彈性。", "共同反對？"),
            tf(f"{pid}-lesen3", 7, "Elena hält Technikfragen für nebensächlich.", False, "barrierefreie Plattformen zentral。", "Elena 覺技術無關。"),
        ],
        passage=_long(
            """
            Forum Studium&Arbeit
            Iris: Ohne bezahlte Lernzeit im Job bleibt Fernstudium Privilegierten vorbehalten. An Präsenztagen brauchen wir Kinderbetreuung.
            Tom: Flexibilität ohne Feedback ist Scheinflexibilität – dann droppen die Leute still.
            Elena: Und bitte barrierefreie Plattformen; sonst schließen wir Studierende mit Behinderung aus.
            """
        ),
        passage_zh="Iris 要帶薪學習時間與面授日托育；Tom 批沒有回饋的假彈性；Elena 強調無障礙平台。",
    )
    lesen4 = section(
        "lesen4", "lesen", "Lesen Teil 4", "閱讀 Teil 4",
        "Infotext Förderung.", "補助資訊。",
        [
            tf(f"{pid}-lesen4", 1, "Das Programm richtet sich an Berufstätige.", True, "Berufstätige。", "對象含在職。"),
            mc(f"{pid}-lesen4", 2, "Förderanteil Modulgebühren?", ["10 %", "bis 50 %", "100 % immer"], 1, "bis 50%。", "補助比例？"),
            tf(f"{pid}-lesen4", 3, "Nachweis der Betreuungspflicht ist irrelevant.", False, "Care-Nachweis möglich。", "照顧證明無關。"),
            mc(f"{pid}-lesen4", 4, "Frist?", ["monatlich rollierend", "jeweils 1. März / 1. Sept.", "nur Weihnachten"], 1, "März/Sept。", "期限？"),
            mc(f"{pid}-lesen4", 5, "Ausschluss?", ["Vollzeitpräsenz ohne Online-Anteil", "alle Fernstudis", "niemand"], 0, "reine Präsenz。", "排除？"),
            tf(f"{pid}-lesen4", 6, "Evaluation misst nur Marketing-Klicks.", False, "Abschluss- und Abbruchquoten。", "只看點擊。"),
        ],
        passage=_long(
            """
            Infotext: Förderlinie „Studium mit Verantwortung“
            Das Land bezuschusst Modulgebühren von Berufstätigen im Fern- oder Hybridstudium mit bis zu 50 Prozent.
            Care-Verantwortung kann durch Nachweis geltend gemacht werden und erhöht die Priorität.
            Antragsfristen: jeweils 1. März und 1. September. Rein präsenzbasierte Vollzeitstudiengänge ohne
            Online-Anteil sind ausgeschlossen. Die Evaluation erfasst Abschluss- und Abbruchquoten sowie
            Betreuungszufriedenheit – nicht Werbeklicks.
            """
        ),
        passage_zh="邦補助在職遠距／混成模組費最高 50%；照顧責任可加權；三月／九月申請；純面授全職排除；評估看畢業／輟學與輔導滿意度。",
    )
    lesen5 = section(
        "lesen5", "lesen", "Lesen Teil 5", "閱讀 Teil 5",
        "Kommentar Vertiefung.", "進階評論。",
        [
            tf(f"{pid}-lesen5", 1, "Algorithmen in Lernplattformen sind neutral.", False, "nicht neutral。", "演算法中立。"),
            mc(f"{pid}-lesen5", 2, "Problem automatischer Warnungen?", ["zu hilfreich immer", "stigmatisieren ohne Kontext", "kein Effekt"], 1, "stigmatisieren。", "自動警示？"),
            mc(f"{pid}-lesen5", 3, "Was fordert der Text?", ["nur Überwachung", "transparente Kriterien + menschliche Beratung", "Datenverkauf"], 1, "透明＋人工諮詢。", "要求？"),
            tf(f"{pid}-lesen5", 4, "Studierende sollen Einblick in genutzte Indikatoren erhalten.", True, "Einblick。", "應能了解指標。"),
            mc(f"{pid}-lesen5", 5, "Bezug zu Gerechtigkeit?", ["irrelevant", "ungleiche Ausgangsbedingungen beachten", "nur Noten"], 1, "Ausgangsungleichheit。", "公平？"),
            mc(f"{pid}-lesen5", 6, "Stil?", ["reißerisch", "kritisch-analytisch", "Werbebroschüre"], 1, "批判分析。", "風格？"),
            mc(f"{pid}-lesen5", 7, "Implizite Warnung vor …", ["mehr Tutorien", "technokratischer Scheinlösung", "Präsenz"], 1, "技術官僚假解方。", "警告？"),
        ],
        passage=_long(
            """
            Kommentar: Learning Analytics – Hilfe oder Kontrolle?
            Frühwarnsysteme in Lernplattformen können Drop-outs senken, sind aber nicht neutral:
            Indikatoren spiegeln oft Annahmen über „ideale“ Studierende. Automatische Warnungen
            stigmatisieren, wenn Kontext fehlt – etwa Care-Arbeit oder Schicht. Gerechtigkeit verlangt
            transparente Kriterien, Widerspruchsrechte und menschliche Beratung statt rein technokratischer
            Scheinlösungen. Studierende brauchen Einblick, welche Daten wie gewertet werden.
            """
        ),
        passage_zh="學習分析可降輟學但非中立；指標常假設「理想學生」；缺脈絡的警示會標籤化；公平需透明標準、救濟與真人諮詢。",
    )
    hoeren1 = section(
        "hoeren1", "hoeren", "Hören Teil 1", "聽力 Teil 1",
        "Interview.", "訪談。",
        [
            mc(f"{pid}-hoeren1", 1, "Rektorin priorisiert …", ["nur Videos", "Betreuungskapazität", "Campusparty"], 1, "Betreuung。", "優先？"),
            tf(f"{pid}-hoeren1", 2, "Sie hält Drop-out für rein individuelles Versagen.", False, "strukturell mitverursacht。", "純個人失敗。"),
            mc(f"{pid}-hoeren1", 3, "Maßnahme?", ["Tutorien verbindlich", "Feedback streichen", "Prüfungen abschaffen"], 0, "verbindliche Tutorien。", "措施？"),
            mc(f"{pid}-hoeren1", 4, "Zu Gebühren?", ["egal", "Transparenz und Förderzugang", "verdoppeln still"], 1, "Transparenz。", "學費？"),
            mc(f"{pid}-hoeren1", 5, "Präsenz?", ["abschaffen", "gezielt hybriden Blöcken", "nur täglich"], 1, "hybride Blöcke。", "面授？"),
            tf(f"{pid}-hoeren1", 6, "Sie will Learning Analytics ohne Transparenz.", False, "nur transparent。", "要不透明分析。"),
        ],
        audio_text=(
            "Interviewer: Was priorisieren Sie im Fernstudium? "
            "Rektorin: Betreuungskapazität. Drop-out ist oft strukturell mitverursacht. "
            "Wir machen Tutorien verbindlicher und setzen auf transparente Gebühren plus Förderzugang. "
            "Präsenz in gezielten hybriden Blöcken. Learning Analytics nur mit Transparenz."
        ),
    )
    hoeren2 = section(
        "hoeren2", "hoeren", "Hören Teil 2", "聽力 Teil 2",
        "Gespräch Studierende.", "學生對話。",
        [
            mc(f"{pid}-hoeren2", 1, "Mias Problem?", ["zu viel Feedback", "Isolation und unklare Aufgaben", "kein WLAN-Wunsch"], 1, "Isolation。", "問題？"),
            tf(f"{pid}-hoeren2", 2, "Jonas nutzt Lerngruppen online.", True, "Online-Lerngruppe。", "Jonas 有線上讀書會。"),
            mc(f"{pid}-hoeren2", 3, "Was ärgert Mia an Proctoring?", ["zu billig", "Überwachung und Stress", "zu wenig Kamera"], 1, "Überwachung。", "監考？"),
            mc(f"{pid}-hoeren2", 4, "Lösungsidee?", ["abschalten Studium", "mehr asynchrone Sprechstunden", "nur Chatbots"], 1, "asynchrone Sprechstunden。", "解方？"),
            mc(f"{pid}-hoeren2", 5, "Ton?", ["gleichgültig", "kritisch-konstruktiv", "nur Spott"], 1, "建設性批評。", "語氣？"),
            tf(f"{pid}-hoeren2", 6, "Sie halten Betreuung für überflüssig.", False, "fordern mehr Betreuung。", "覺輔導多餘。"),
        ],
        audio_text=(
            "Mia: Ich fühle mich isoliert, die Aufgaben sind unklar. Proctoring stresst mich wegen Überwachung. "
            "Jonas: Komm in unsere Online-Lerngruppe. Und die Hochschule sollte asynchrone Sprechstunden ausbauen. "
            "Mia: Ja – mehr Betreuung, nicht weniger."
        ),
    )
    hoeren3 = section(
        "hoeren3", "hoeren", "Hören Teil 3", "聽力 Teil 3",
        "Vortrag.", "短講。",
        [
            mc(f"{pid}-hoeren3", 1, "Thema?", ["Sportregeln", "Anrechnung von Vorleistungen", "Kochkunst"], 1, "Anrechnung。", "主題？"),
            tf(f"{pid}-hoeren3", 2, "Uneinheitliche Regeln belasten Wechselnde.", True, "uneinheitlich。", "規則不一加重負擔。"),
            mc(f"{pid}-hoeren3", 3, "Vorschlag?", ["alles ablehnen", "transparente Portfolios", "nur mündlich"], 1, "Portfolios。", "建議？"),
            mc(f"{pid}-hoeren3", 4, "Zeitfaktor?", ["egal", "Entscheidungen dauern zu lange", "sofort immer"], 1, "dauern zu lange。", "時間？"),
            tf(f"{pid}-hoeren3", 5, "Referentin will Willkür erhöhen.", False, "gegen Willkür。", "想增加任意性。"),
            mc(f"{pid}-hoeren3", 6, "Bezug Gerechtigkeit?", ["kein Bezug", "vermeidet Doppelarbeit für Berufstätige", "nur Elite"], 1, "避免重複。", "公平？"),
        ],
        audio_text=(
            "Referentin: Die Anrechnung von Vorleistungen ist oft uneinheitlich – das belastet Wechsler und Berufstätige. "
            "Ich plädiere für transparente Portfolios und kürzere Entscheidungsfristen. "
            "Ziel: weniger Willkür, weniger Doppelarbeit – das ist Bildungsgerechtigkeit praktisch."
        ),
    )
    hoeren4 = section(
        "hoeren4", "hoeren", "Hören Teil 4", "聽力 Teil 4",
        "Podium.", "論壇。",
        [
            mc(f"{pid}-hoeren4", 1, "Karim fordert …", ["Abbau von Stipendien", "sozial gestaffelte Förderung", "nur Kredite"], 1, "sozial gestaffelt。", "Karim？"),
            tf(f"{pid}-hoeren4", 2, "Beate will Betreuung durch KI ersetzen.", False, "KI ergänzt, ersetzt nicht。", "要用 AI 取代輔導。"),
            mc(f"{pid}-hoeren4", 3, "Streit?", ["ob Flexibilität Kosten externalisiert", "Kaffee", "Parkplätze nur"], 0, "成本外部化。", "爭議？"),
            mc(f"{pid}-hoeren4", 4, "Konsens?", ["Marketing erhöhen", "Kennzahlen zu Abbruch und Betreuung veröffentlichen", "schweigen"], 1, "公開指標。", "共識？"),
            tf(f"{pid}-hoeren4", 5, "Beide lehnen Evaluation ab.", False, "wollen veröffentlichen。", "都反對評估。"),
            mc(f"{pid}-hoeren4", 6, "Implizite Kritik an Hochschulmarketing?", ["nein", "ja, Flexibilitätsversprechen", "nur Design"], 1, "假彈性承諾。", "行銷批評？"),
        ],
        audio_text=(
            "Karim: Wir brauchen sozial gestaffelte Förderung, sonst bleibt Fernstudium ungerecht. "
            "Beate: Einverstanden – und KI darf Betreuung ergänzen, nicht ersetzen. "
            "Karim: Flexibilitätsversprechen externalisieren oft Kosten auf Studierende. "
            "Beate: Dann veröffentlichen wir Kennzahlen zu Abbruch und Betreuung – Schluss mit Marketingnebel."
        ),
    )
    schreiben1 = section(
        "schreiben1", "schreiben", "Schreiben Teil 1", "寫作 Teil 1",
        "Forum.", "論壇。",
        [
            schreiben_item(
                f"{pid}-schreiben1", 1,
                "Forumsthema „Ist Fernstudium gerecht?“:\n"
                "• Position\n• Argument zu Betreuung/Drop-out\n• Forderung an Hochschulen",
                "論壇「遠距是否公平？」：立場、輔導／輟學論點、對高校要求。",
                120,
                "Fernstudium kann Teilhabe erhöhen, ist aber nicht automatisch gerecht. "
                "Ohne Tutorien und Feedback steigen Drop-outs – besonders bei Care-Arbeit. "
                "Hochschulen müssen Betreuungskapazität ausweisen und Learning Analytics transparent machen.",
                ["立場", "輔導論點", "具體要求"],
            )
        ],
    )
    schreiben2 = section(
        "schreiben2", "schreiben", "Schreiben Teil 2", "寫作 Teil 2",
        "Formeller Brief.", "正式信。",
        [
            schreiben_item(
                f"{pid}-schreiben2", 1,
                "Schreiben Sie an die Hochschulleitung:\n"
                "• Kritik an unklarer Aufgabenstellung online\n• Vorschlag: asynchrone Sprechstunden + Anrechnungsfrist\n"
                "• Bitte um Antwort mit Zeitplan",
                "寫給校方：批評線上作業不清、建議非同步諮詢與抵免時限、請附時程回覆。",
                180,
                "Sehr geehrte Damen und Herren,\ndie Aufgabenstellungen im Online-Modul sind oft unklar, "
                "was Isolation und Abbruchrisiko erhöht. Ich schlage verbindliche asynchrone Sprechstunden "
                "sowie eine maximale Frist für Anrechnungsentscheidungen vor. Bitte antworten Sie mit einem Zeitplan.\n"
                "Mit freundlichen Grüßen",
                ["批評", "兩項建議", "請回覆時程"],
            )
        ],
    )
    sprechen1 = section(
        "sprechen1", "sprechen", "Sprechen Teil 1", "口說 Teil 1",
        "Planen.", "規劃。",
        [sprechen_item(f"{pid}-sprechen1", 1,
            "Planen Sie ein Unterstützungspaket für Fernstudierende: Maßnahmen, Zuständige, Kennzahlen.",
            "規劃遠距生支持方案：措施、負責人、指標。",
            ["Tutorien", "Sprechstunden", "Kennzahlen", "Verantwortung"],
            "Wöchentliche Tutorien, asynchrone Sprechstunden, Kennzahl Abbruchquote. Verantwortung: Studiendekanat.")],
    )
    sprechen2 = section(
        "sprechen2", "sprechen", "Sprechen Teil 2", "口說 Teil 2",
        "Kurzvortrag.", "短講。",
        [sprechen_item(f"{pid}-sprechen2", 1,
            "Kurzvortrag: Bildungsgerechtigkeit im digitalen Studium – Chancen und Fallstricke.",
            "短講：數位學習的教育公平——機會與陷阱。",
            ["Chance", "Fallstrick", "Fazit"],
            "Chance: Zugang für Berufstätige. Fallstrick: Scheinflexibilität ohne Betreuung. Fazit: Ressourcen folgen Versprechen.")],
    )
    return paper(
        pid, "B2", 4,
        "Goethe-Format B2 · Modellsatz 4 (etwas schwerer)",
        "考場版 B2 · 第4回（稍難）",
        170,
        [lesen1, lesen2, lesen3, lesen4, lesen5, hoeren1, hoeren2, hoeren3, hoeren4, schreiben1, schreiben2, sprechen1, sprechen2],
        difficulty="etwas_schwerer",
    )


def main() -> None:
    data = json.loads(OUT.read_text(encoding="utf-8"))
    papers: list[dict[str, Any]] = data["papers"]

    # Tag existing papers with difficulty=standard when missing
    for p in papers:
        fmt = p.get("format")
        if fmt in ("compact", "goethe") and "difficulty" not in p:
            p["difficulty"] = "standard"

    # Idempotent: drop previous variants only
    papers[:] = [p for p in papers if p["id"] not in VARIANT_IDS]

    assert len(papers) == 16, f"expected 16 existing papers before append, got {len(papers)}"

    new_papers = [
        a1_g3(),
        a1_g4(),
        a2_g3(),
        a2_g4(),
        b1_g3(),
        b1_g4(),
        b2_g3(),
        b2_g4(),
    ]

    expected_sections = {"A1": 11, "A2": 13, "B1": 14, "B2": 13}
    expected_dur = {"A1": 65, "A2": 90, "B1": 150, "B2": 170}

    print(f"{'id':8} {'diff':16} {'secs':>4} {'scored':>6} {'dur':>4}")
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
    assert len(papers) == 24, f"expected 24 papers, got {len(papers)}"

    # Existing 16 tagged
    for p in papers:
        if p["id"] not in VARIANT_IDS:
            assert p.get("difficulty") == "standard", p["id"]

    print("OK: appended 8 Goethe variants; total papers == 24")
    print("Updated", OUT)


if __name__ == "__main__":
    main()
