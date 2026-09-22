#!/usr/bin/env python3
"""Generate Goethe/ÖSD-style mock exam papers (A1–B2, 2 each) → src/data/exams.json."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "src" / "data" / "exams.json"

NOTE = (
    "德檢取向模擬測驗（Goethe／ÖSD 風格）：A1–B2 各兩份模考。"
    "聚焦 Lesen＋Hören（TTS 朗讀腳本）＋Bausteine＋Schreiben；"
    "Sprechen 為選練口說提示，不計入及格門檻。"
    "答完後可對照中文譯文與詳解。非官方試題，僅供練習。"
)


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
    level: str,
    round_: int,
    title: str,
    title_zh: str,
    duration: int,
    sections: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "id": f"{level.lower()}-m{round_}",
        "level": level,
        "round": round_,
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
# A1 · Modellsatz 1 — Café / Stadt
# ═══════════════════════════════════════════════════════════════════════════


def a1_m1() -> dict[str, Any]:
    pid = "a1-m1"
    lesen_pid = f"{pid}-lesen"
    passage = (
        "Café Sonne\n"
        "Öffnungszeiten: Mo–Fr 8:00–18:00, Sa 9:00–14:00, So geschlossen.\n"
        "Heute: Frische Brötchen und Kaffee für 3,50 €.\n"
        "WLAN gratis. Hunde willkommen.\n\n"
        "SMS von Lisa an Tom:\n"
        "Hallo Tom! Treffen wir uns um 15 Uhr vor dem Café Sonne? "
        "Ich habe Hunger. Bring bitte dein Buch mit. Bis später! Lisa"
    )
    passage_zh = (
        "太陽咖啡館\n"
        "營業時間：週一至週五 8:00–18:00，週六 9:00–14:00，週日公休。\n"
        "今日特價：新鮮麵包捲配咖啡 3,50 歐元。\n"
        "免費無線網路。歡迎帶狗。\n\n"
        "Lisa 傳給 Tom 的簡訊：\n"
        "哈囉 Tom！我們下午三點在太陽咖啡館前碰面好嗎？"
        "我餓了。請把你的書帶來。待會見！Lisa"
    )
    lesen = section(
        "lesen",
        "lesen",
        "Lesen",
        "閱讀",
        "Lesen Sie den Text. Kreuzen Sie an: Ja, Nein oder Steht nicht im Text.",
        "請閱讀短文。勾選：對、錯，或文中未提及。",
        [
            tf(lesen_pid, 1, "Das Café ist am Sonntag geöffnet.", False, "文中寫 So geschlossen，週日公休。", "咖啡館週日營業。"),
            tf(lesen_pid, 2, "Am Samstag öffnet das Café um 9 Uhr.", True, "Sa 9:00–14:00，週六九點開門。", "週六九點開門。"),
            tf(lesen_pid, 3, "Kaffee und Brötchen kosten heute 3,50 €.", True, "今日特價寫明 3,50 €。", "咖啡加麵包捲今天 3,50 歐。"),
            tf(lesen_pid, 4, "Es gibt kein WLAN im Café.", False, "寫明 WLAN gratis。", "館內沒有無線網路。"),
            tf(lesen_pid, 5, "Hunde dürfen nicht ins Café.", False, "Hunde willkommen＝歡迎帶狗。", "不准帶狗進館。"),
            tf(lesen_pid, 6, "Lisa und Tom treffen sich um 15 Uhr.", True, "簡訊寫 um 15 Uhr。", "兩人約三點碰面。"),
            tf(lesen_pid, 7, "Tom soll ein Buch mitbringen.", True, "Bring bitte dein Buch mit。", "Tom 要帶書來。"),
            tf(lesen_pid, 8, "Lisa wohnt neben dem Café.", "nicht", "簡訊沒說 Lisa 住哪。", "Lisa 住在咖啡館旁邊。"),
            tf(lesen_pid, 9, "Lisa hat Hunger.", True, "簡訊寫 Ich habe Hunger。", "Lisa 餓了。"),
        ],
        passage=passage,
        passage_zh=passage_zh,
    )

    audio = (
        "Kellnerin: Guten Tag und willkommen im Café Sonne! "
        "Was darf ich Ihnen bringen?\n"
        "Frau: Guten Tag! Einen Kaffee und ein Brötchen, bitte.\n"
        "Kellnerin: Gerne. Möchten Sie Milch oder Zucker im Kaffee?\n"
        "Frau: Ja, bitte mit Milch. Ohne Zucker.\n"
        "Kellnerin: Und zum Brötchen? Butter oder Marmelade?\n"
        "Frau: Butter, bitte. Und haben Sie auch Orangensaft?\n"
        "Kellnerin: Ja, frischen Saft. Möchten Sie ein kleines oder ein großes Glas?\n"
        "Frau: Ein kleines Glas, danke.\n"
        "Kellnerin: Das macht zusammen fünf Euro vierzig.\n"
        "Frau: Hier sind sechs Euro.\n"
        "Kellnerin: Danke. Hier ist Ihr Wechselgeld, sechzig Cent. "
        "Ihren Kaffee bringe ich gleich an den Tisch am Fenster. "
        "Das Brötchen kommt auch sofort.\n"
        "Frau: Super, vielen Dank!\n"
        "Kellnerin: Bitte sehr. Einen schönen Tag noch!"
    )
    hoeren_pid = f"{pid}-hoeren"
    hoeren = section(
        "hoeren",
        "hoeren",
        "Hören",
        "聽力",
        "Hören Sie den Dialog. Wählen Sie die richtige Antwort.",
        "請聽對話（可用語音播放），選出正確答案。",
        [
            mc(hoeren_pid, 1, "Was bestellt die Frau zuerst?", ["Tee und Kuchen", "Kaffee und ein Brötchen", "Wasser und Brot", "Saft und Käse"], 1, "她點了咖啡和麵包捲。"),
            mc(hoeren_pid, 2, "Möchte die Frau Milch im Kaffee?", ["Nein", "Ja, mit Milch", "Nur Zucker", "Sie sagt nichts"], 1, "她說 mit Milch。"),
            mc(hoeren_pid, 3, "Was möchte sie zum Brötchen?", ["Marmelade", "Käse", "Butter", "Honig"], 2, "她選 Butter。"),
            mc(hoeren_pid, 4, "Welchen Saft bestellt sie?", ["großes Glas", "kleines Glas Orangensaft", "keinen Saft", "Apfelsaft"], 1, "ein kleines Glas Orangensaft。"),
            mc(hoeren_pid, 5, "Wie viel kostet alles?", ["3,50 €", "5,40 €", "6,00 €", "0,60 €"], 1, "fünf Euro vierzig。"),
            mc(hoeren_pid, 6, "Wie viel gibt die Frau?", ["4 Euro", "6 Euro", "10 Euro", "2 Euro"], 1, "她給 sechs Euro。"),
            mc(hoeren_pid, 7, "Wo sitzt die Frau?", ["An der Tür", "Am Fenster", "Draußen", "An der Bar"], 1, "桌子在 am Fenster。"),
            mc(hoeren_pid, 8, "Wie viel Wechselgeld bekommt sie?", ["60 Cent", "80 Cent", "1 Euro", "kein Wechselgeld"], 0, "sechzig Cent。"),
        ],
        audio_text=audio,
    )

    bau_pid = f"{pid}-bausteine"
    bausteine = section(
        "bausteine",
        "bausteine",
        "Bausteine",
        "語法詞彙",
        "Ergänzen Sie oder wählen Sie die richtige Form.",
        "填空或選出正確形式。",
        [
            mc(bau_pid, 1, "___ Café ist neu.", ["Der", "Die", "Das", "Den"], 2, "Café 是中性 → das。"),
            mc(bau_pid, 2, "Ich ___ aus Taiwan.", ["komme", "kommst", "kommt", "kommen"], 0, "ich 用 komme。"),
            gap(bau_pid, 3, "Guten Tag! Wie ___ Sie?", "heißen", "詢問姓名：Wie heißen Sie？", accept=["heissen"]),
            mc(bau_pid, 4, "Das ist ___ Buch.", ["mein", "meine", "meiner", "meinen"], 0, "Buch 中性 → mein。"),
            gap(bau_pid, 5, "Wir treffen ___ um 15 Uhr.", "uns", "反身：sich treffen → uns。"),
            mc(bau_pid, 6, "Heute ___ das Café geschlossen.", ["ist", "bist", "sind", "seid"], 0, "單數主詞 → ist。"),
            gap(bau_pid, 7, "Ich habe ___ Hunger.", "keinen", "否定：kein + Akkusativ masculin → keinen。", accept=["kein"]),
            mc(bau_pid, 8, "Bring bitte ___ Buch mit!", ["dein", "deine", "deiner", "deinen"], 0, "Buch 中性 → dein。"),
            gap(bau_pid, 9, "Am Sonntag ist das Café ___.", "geschlossen", "geschlossen＝關閉。"),
        ],
    )

    schreib_pid = f"{pid}-schreiben"
    schreiben = section(
        "schreiben",
        "schreiben",
        "Schreiben",
        "寫作",
        "Schreiben Sie eine kurze E-Mail (ca. 30–40 Wörter).",
        "請寫一封短郵件（約 30–40 字）。",
        [
            schreiben_item(
                schreib_pid,
                1,
                "Sie möchten sich mit einem Freund im Café Sonne treffen. "
                "Schreiben Sie eine E-Mail: Begrüßung – Vorschlag (Tag und Uhrzeit) – "
                "Was möchten Sie trinken/essen? – Verabschiedung.",
                "你想約朋友在太陽咖啡館見面。寫信包含：問候、提議日期時間、想吃／喝什麼、結尾。",
                30,
                "Hallo Anna,\nvielen Dank für deine Nachricht. "
                "Treffen wir uns am Samstag um 11 Uhr im Café Sonne? "
                "Ich möchte einen Kaffee und ein Brötchen. "
                "Bis bald!\nLiebe Grüße\nTom",
                [
                    "有問候與結尾",
                    "有明確時間／地點",
                    "提到想吃或喝的東西",
                    "約 30 字以上、句子完整",
                ],
            )
        ],
    )

    sprech_pid = f"{pid}-sprechen"
    sprechen = section(
        "sprechen",
        "sprechen",
        "Sprechen",
        "口說",
        "Sprechen Sie zu den Themen. Optional mit Modellantwort üben.",
        "依題口述練習；可聽範例對照。",
        [
            sprechen_item(
                sprech_pid,
                1,
                "Stellen Sie sich vor: Name, Herkunft, Wohnort, Hobby.",
                "自我介紹：名字、出身、住處、嗜好。",
                ["Name", "Woher kommen Sie?", "Wo wohnen Sie?", "Hobby"],
                "Guten Tag, ich heiße Mei. Ich komme aus Taiwan und wohne in Berlin. "
                "Mein Hobby ist Lesen. Ich lerne Deutsch.",
            ),
            sprechen_item(
                sprech_pid,
                2,
                "Beschreiben Sie Ihr Lieblingscafé: Wo? Was bestellen Sie?",
                "描述最愛的咖啡館：在哪？常點什麼？",
                ["Ort", "Öffnungszeiten", "Getränk/Essen"],
                "Mein Lieblingscafé heißt Café Sonne. Es ist in der Stadtmitte. "
                "Ich bestelle oft einen Kaffee mit Milch und ein Brötchen.",
            ),
        ],
    )

    return paper(
        "A1",
        1,
        "Goethe-Format A1 · Modellsatz 1",
        "德檢模擬 A1 · 模考一（咖啡館／進城）",
        60,
        [lesen, hoeren, bausteine, schreiben, sprechen],
    )


# ═══════════════════════════════════════════════════════════════════════════
# A1 · Modellsatz 2 — Wohnung / Sprachkurs
# ═══════════════════════════════════════════════════════════════════════════


def a1_m2() -> dict[str, Any]:
    pid = "a1-m2"
    lesen_pid = f"{pid}-lesen"
    passage = (
        "Wohnung zu vermieten\n"
        "2 Zimmer, Küche, Bad. 45 m². 3. Etage, kein Aufzug.\n"
        "Miete: 650 € + 120 € Nebenkosten. Ab 1. Mai frei.\n"
        "Adresse: Parkstraße 12, 80331 München. Tel: 089-555-2211.\n\n"
        "E-Mail vom Sprachkurs:\n"
        "Liebe Kursteilnehmerinnen und Kursteilnehmer,\n"
        "unser Kurs beginnt am Montag, den 3. März um 9:00 Uhr in Raum 4. "
        "Bitte bringen Sie ein Heft und einen Stift mit. "
        "Am Freitag gibt es einen kurzen Test. Viele Grüße, Frau Weber"
    )
    passage_zh = (
        "出租公寓\n"
        "兩房、廚房、衛浴。45 平方公尺。三樓，無電梯。\n"
        "租金：650 歐 + 120 歐雜費。五月一日起可入住。\n"
        "地址：Parkstraße 12, 80331 慕尼黑。電話：089-555-2211。\n\n"
        "語言課郵件：\n"
        "親愛的學員們，\n"
        "課程於三月三日（週一）上午九點在 4 教室開始。"
        "請帶筆記本與筆。週五有小考。問候，Weber 老師"
    )
    lesen = section(
        "lesen",
        "lesen",
        "Lesen",
        "閱讀",
        "Lesen Sie die Texte. Ja / Nein / Steht nicht im Text.",
        "閱讀兩則短文，判斷對、錯或未提及。",
        [
            tf(lesen_pid, 1, "Die Wohnung hat zwei Zimmer.", True, "寫明 2 Zimmer。", "公寓有兩間房。"),
            tf(lesen_pid, 2, "Es gibt einen Aufzug.", False, "kein Aufzug＝沒有電梯。", "有電梯。"),
            tf(lesen_pid, 3, "Die Miete kostet 650 € ohne Nebenkosten.", True, "650 € + 120 € Nebenkosten。", "租金不含雜費是 650 歐。"),
            tf(lesen_pid, 4, "Die Wohnung ist ab Juni frei.", False, "Ab 1. Mai frei。", "六月才能入住。"),
            tf(lesen_pid, 5, "Die Wohnung liegt in Berlin.", False, "地址是 München。", "公寓在柏林。"),
            tf(lesen_pid, 6, "Der Sprachkurs beginnt um 9 Uhr.", True, "um 9:00 Uhr。", "語言課九點開始。"),
            tf(lesen_pid, 7, "Der Kurs ist in Raum 4.", True, "in Raum 4。", "在 4 教室。"),
            tf(lesen_pid, 8, "Man braucht ein Wörterbuch im Kurs.", "nicht", "只要求 Heft 和 Stift，沒提字典。", "課堂必須帶字典。"),
            tf(lesen_pid, 9, "Am Freitag gibt es einen Test.", True, "郵件寫 kurzener Test am Freitag。", "週五有考試。"),
        ],
        passage=passage,
        passage_zh=passage_zh,
    )

    audio = (
        "Mann: Entschuldigung, ich suche die Parkstraße Nummer zwölf. "
        "Können Sie mir bitte helfen?\n"
        "Frau: Die Parkstraße? Ja, natürlich. Gehen Sie hier geradeaus bis zur Ampel, "
        "dann links in die kleine Seitenstraße. Das Haus ist das dritte auf der rechten Seite. "
        "Es ist rot und hat einen Balkon.\n"
        "Mann: Ist das weit von hier?\n"
        "Frau: Nein, nur etwa fünf Minuten zu Fuß. Wenn Sie möchten, "
        "können Sie auch den Bus Linie vier nehmen.\n"
        "Mann: Und gibt es dort eine Bushaltestelle?\n"
        "Frau: Ja, die Haltestelle Parkstraße ist direkt vor dem Haus.\n"
        "Mann: Vielen Dank! Ich schaue mir heute Nachmittag eine Wohnung an. "
        "Ich hoffe, sie ist noch frei.\n"
        "Frau: Viel Erfolg bei der Besichtigung! Auf Wiedersehen.\n"
        "Mann: Auf Wiedersehen und schönen Tag noch!"
    )
    hoeren_pid = f"{pid}-hoeren"
    hoeren = section(
        "hoeren",
        "hoeren",
        "Hören",
        "聽力",
        "Hören Sie. Wählen Sie die richtige Antwort.",
        "聽對話後選答案。",
        [
            mc(hoeren_pid, 1, "Wohin möchte der Mann?", ["Bahnhof", "Parkstraße 12", "Schule", "Café"], 1, "他找 Parkstraße 12。"),
            mc(hoeren_pid, 2, "Was macht er an der Ampel?", ["rechts", "links", "geradeaus weiter", "zurück"], 1, "dann links。"),
            mc(hoeren_pid, 3, "Wie lange zu Fuß?", ["2 Minuten", "etwa 5 Minuten", "15 Minuten", "30 Minuten"], 1, "etwa fünf Minuten。"),
            mc(hoeren_pid, 4, "Welche Buslinie nennt die Frau?", ["Linie 2", "Linie 4", "Linie 12", "keinen Bus"], 1, "Bus Linie vier。"),
            mc(hoeren_pid, 5, "Wo ist die Bushaltestelle?", ["weit weg", "vor dem Haus", "hinter dem Park", "am Bahnhof"], 1, "direkt vor dem Haus。"),
            mc(hoeren_pid, 6, "Warum geht der Mann dorthin?", ["Arbeit", "Wohnung anschauen", "Einkaufen", "Arzt"], 1, "eine Wohnung anschauen。"),
            mc(hoeren_pid, 7, "Das Haus ist das ___ auf der rechten Seite.", ["erste", "zweite", "dritte", "vierte"], 2, "das dritte。"),
            mc(hoeren_pid, 8, "Wie verabschieden sie sich?", ["Tschüss", "Auf Wiedersehen", "Bis morgen", "Gute Nacht"], 1, "Auf Wiedersehen。"),
        ],
        audio_text=audio,
    )

    bau_pid = f"{pid}-bausteine"
    bausteine = section(
        "bausteine",
        "bausteine",
        "Bausteine",
        "語法詞彙",
        "Wählen oder ergänzen Sie.",
        "選擇或填空。",
        [
            mc(bau_pid, 1, "___ Wohnung ist schön.", ["Der", "Die", "Das", "Den"], 1, "Wohnung 陰性 → die。"),
            gap(bau_pid, 2, "Ich wohne ___ München.", "in", "城市用 in + 地名。"),
            mc(bau_pid, 3, "Der Kurs ___ am Montag.", ["beginnt", "beginne", "beginnen", "beginnst"], 0, "第三人稱單數 beginnt。"),
            gap(bau_pid, 4, "Bitte bringen Sie ein Heft ___.", "mit", "mitbringen 可分動詞：bringen … mit。"),
            mc(bau_pid, 5, "Die Nebenkosten betragen ___ Euro.", ["hundertzwanzig", "zweihundert", "fünfzig", "tausend"], 0, "120＝hundertzwanzig。"),
            gap(bau_pid, 6, "Gehen Sie ___ bis zur Ampel.", "geradeaus", "geradeaus＝直走。"),
            mc(bau_pid, 7, "Am Freitag gibt ___ einen Test.", ["es", "er", "sie", "ihn"], 0, "es gibt＝有。"),
            gap(bau_pid, 8, "Die Wohnung ist ab 1. Mai ___.", "frei", "frei＝可入住／空出。"),
            mc(bau_pid, 9, "___ Etage, kein Aufzug.", ["3.", "drei", "dritten", "3"], 0, "樓層寫法 3. Etage。"),
        ],
    )

    schreib_pid = f"{pid}-schreiben"
    schreiben = section(
        "schreiben",
        "schreiben",
        "Schreiben",
        "寫作",
        "Füllen Sie das Formular / schreiben Sie eine kurze Nachricht (ca. 30 Wörter).",
        "填寫簡訊／短訊息（約 30 字）。",
        [
            schreiben_item(
                schreib_pid,
                1,
                "Sie interessieren sich für die Wohnung in der Parkstraße. "
                "Schreiben Sie eine kurze E-Mail an den Vermieter: "
                "Wer sind Sie? Wann können Sie die Wohnung besichtigen? "
                "Stellen Sie eine Frage zur Wohnung.",
                "你對 Parkstraße 的公寓有興趣。寫短信給房東：自我介紹、何時可看房、問一個關於房子的問題。",
                30,
                "Guten Tag,\nich heiße Lin und arbeite in München. "
                "Kann ich die Wohnung am Samstag um 14 Uhr besichtigen? "
                "Gibt es Möbel in der Wohnung?\nMit freundlichen Grüßen\nLin Chen",
                [
                    "有稱呼與結尾",
                    "自我介紹",
                    "提出看房時間",
                    "至少一個問題",
                ],
            )
        ],
    )

    sprech_pid = f"{pid}-sprechen"
    sprechen = section(
        "sprechen",
        "sprechen",
        "Sprechen",
        "口說",
        "Sprechen Sie frei zu den Punkten.",
        "依提示自由口述。",
        [
            sprechen_item(
                sprech_pid,
                1,
                "Beschreiben Sie Ihre Wohnung oder Ihr Zimmer.",
                "描述你的住處或房間。",
                ["Wie groß?", "Welche Zimmer?", "Was ist wichtig?"],
                "Ich wohne in einer Zwei-Zimmer-Wohnung. Die Küche ist klein, "
                "aber hell. Mein Zimmer hat einen Schreibtisch und ein Bett.",
            ),
        ],
    )

    return paper(
        "A1",
        2,
        "Goethe-Format A1 · Modellsatz 2",
        "德檢模擬 A1 · 模考二（租屋／語言課）",
        60,
        [lesen, hoeren, bausteine, schreiben, sprechen],
    )


# ═══════════════════════════════════════════════════════════════════════════
# A2 · Modellsatz 1 — Sportverein / Freizeit
# ═══════════════════════════════════════════════════════════════════════════


def a2_m1() -> dict[str, Any]:
    pid = "a2-m1"
    lesen_pid = f"{pid}-lesen"
    passage = (
        "Sportverein Grün-Weiß – Neuigkeiten\n\n"
        "Ab April starten neue Kursangebote: Yoga (Di 18–19 Uhr), "
        "Fußball für Erwachsene (Mi 19–20:30 Uhr) und Schwimmen (Do 17–18 Uhr). "
        "Die Mitgliedschaft kostet 25 € im Monat. Neue Mitglieder bekommen "
        "im ersten Monat 50 % Rabatt. Anmeldung online oder im Büro "
        "(Mo–Fr 10–16 Uhr). Kinder unter 14 Jahren brauchen die Erlaubnis "
        "der Eltern. Bitte Sportkleidung und Handtuch mitbringen. "
        "Das Vereinsfest findet am 12. Mai im Stadtpark statt – Eintritt frei!"
    )
    passage_zh = (
        "綠白體育會 – 最新消息\n\n"
        "四月起新開課程：瑜珈（週二 18–19）、成人足球（週三 19–20:30）、"
        "游泳（週四 17–18）。會員月費 25 歐。新會員首月半價。"
        "可線上或辦公室報名（週一至五 10–16）。未滿 14 歲需家長同意。"
        "請自備運動服與毛巾。五月十二日市立公園有社團日，免費入場！"
    )
    lesen = section(
        "lesen",
        "lesen",
        "Lesen",
        "閱讀",
        "Lesen Sie den Text und beantworten Sie die Fragen.",
        "閱讀公告並作答（選擇／判斷）。",
        [
            mc(lesen_pid, 1, "Wann starten die neuen Kurse?", ["Im März", "Ab April", "Im Mai", "Im Juni"], 1, "Ab April。"),
            mc(lesen_pid, 2, "Wann ist Yoga?", ["Montag", "Dienstag", "Mittwoch", "Donnerstag"], 1, "Di 18–19。"),
            tf(lesen_pid, 3, "Fußball ist am Mittwochabend.", True, "Mi 19–20:30。"),
            tf(lesen_pid, 4, "Die Mitgliedschaft kostet 50 € im Monat.", False, "25 € im Monat。"),
            mc(lesen_pid, 5, "Was bekommen neue Mitglieder?", ["Gratis Sportschuhe", "50 % Rabatt im ersten Monat", "Kein Angebot", "Jahr gratis"], 1, "首月半價。"),
            tf(lesen_pid, 6, "Das Büro ist auch am Sonntag geöffnet.", False, "只寫 Mo–Fr。"),
            tf(lesen_pid, 7, "Kinder unter 14 brauchen die Erlaubnis der Eltern.", True, "文中明確寫出。"),
            mc(lesen_pid, 8, "Was soll man mitbringen?", ["Bücher", "Sportkleidung und Handtuch", "Essen", "Geldkarte"], 1, "運動服與毛巾。"),
            tf(lesen_pid, 9, "Das Vereinsfest kostet 10 € Eintritt.", False, "Eintritt frei。"),
            mc(lesen_pid, 10, "Wo findet das Fest statt?", ["In der Halle", "Im Stadtpark", "Im Büro", "Online"], 1, "im Stadtpark。"),
        ],
        passage=passage,
        passage_zh=passage_zh,
    )

    audio = (
        "Reporter: Hallo und willkommen beim Sportverein Grün-Weiß. "
        "Heute spreche ich mit Trainerin Anna Berger.\n"
        "Anna: Hallo! Schön, dass Sie da sind.\n"
        "Reporter: Anna, für wen ist der Yoga-Kurs?\n"
        "Anna: Für Anfänger und Fortgeschrittene. Man braucht keine Erfahrung.\n"
        "Reporter: Und der Fußballkurs?\n"
        "Anna: Der ist nur für Erwachsene ab 18 Jahren. Wir spielen auf dem Platz hinter der Halle.\n"
        "Reporter: Wie meldet man sich an?\n"
        "Anna: Am besten online. Oder kommen Sie persönlich ins Büro zwischen zehn und sechzehn Uhr.\n"
        "Reporter: Gibt es noch freie Plätze im Schwimmkurs?\n"
        "Anna: Ja, noch sechs Plätze. Der Kurs ist donnerstags.\n"
        "Reporter: Danke, Anna!\n"
        "Anna: Gerne. Bis bald beim Training!"
    )
    hoeren_pid = f"{pid}-hoeren"
    hoeren = section(
        "hoeren",
        "hoeren",
        "Hören",
        "聽力",
        "Hören Sie das Interview. Wählen Sie.",
        "聽訪談後選擇。",
        [
            mc(hoeren_pid, 1, "Mit wem spricht der Reporter?", ["Herrn Weber", "Anna Berger", "Frau Mai", "Trainer Paul"], 1, "Trainerin Anna Berger。"),
            mc(hoeren_pid, 2, "Braucht man Erfahrung für Yoga?", ["Ja, viel", "Nein", "Nur Zertifikat", "Nur Schwimmen"], 1, "keine Erfahrung nötig。"),
            mc(hoeren_pid, 3, "Ab welchem Alter ist Fußball?", ["14", "16", "18", "21"], 2, "ab 18 Jahren。"),
            mc(hoeren_pid, 4, "Wo spielt man Fußball?", ["In der Halle", "Hinter der Halle", "Im Park", "Im Büro"], 1, "Platz hinter der Halle。"),
            mc(hoeren_pid, 5, "Wann ist das Büro geöffnet?", ["8–12", "10–16", "14–20", "ganztags"], 1, "zwischen zehn und sechzehn。"),
            mc(hoeren_pid, 6, "Wie viele Plätze sind im Schwimmen frei?", ["zwei", "vier", "sechs", "zehn"], 2, "noch sechs Plätze。"),
            mc(hoeren_pid, 7, "Wann ist der Schwimmkurs?", ["Dienstag", "Mittwoch", "Donnerstag", "Freitag"], 2, "donnerstags。"),
            mc(hoeren_pid, 8, "Wie meldet man sich am besten an?", ["per Telefon", "online", "nur per Post", "gar nicht nötig"], 1, "Am besten online。"),
        ],
        audio_text=audio,
    )

    bau_pid = f"{pid}-bausteine"
    bausteine = section(
        "bausteine",
        "bausteine",
        "Bausteine",
        "語法詞彙",
        "Grammatik und Wortschatz.",
        "語法與詞彙。",
        [
            mc(bau_pid, 1, "Ich ___ seit zwei Jahren Mitglied.", ["bin", "habe", "werde", "muss"], 0, "Mitglied sein。"),
            gap(bau_pid, 2, "Der Kurs beginnt ___ April.", "ab", "ab + 時間點＝從…起。", accept=["im"]),
            mc(bau_pid, 3, "Neue Mitglieder bekommen ___ Rabatt.", ["einen", "eine", "ein", "eines"], 0, "Rabatt 陽性 Akk → einen。"),
            gap(bau_pid, 4, "Bitte ___ Sie Sportkleidung mit.", "bringen", "mitbringen 分離：bringen … mit。"),
            mc(bau_pid, 5, "Kinder ___ 14 Jahren brauchen Erlaubnis.", ["unter", "über", "seit", "gegen"], 0, "unter＝未滿。"),
            gap(bau_pid, 6, "Das Fest findet am 12. Mai ___.", "statt", "stattfinden → findet … statt。"),
            mc(bau_pid, 7, "Am besten meldet man sich ___ an.", ["online", "langsam", "nie", "gestern"], 0, "online。"),
            gap(bau_pid, 8, "Wir spielen ___ dem Platz hinter der Halle.", "auf", "auf dem Platz。"),
            mc(bau_pid, 9, "Der Eintritt ist ___.", ["frei", "teuer", "geschlossen", "voll"], 0, "Eintritt frei。"),
            gap(bau_pid, 10, "Ich gehe ___ Yoga-Kurs.", "zum", "zu dem → zum。", accept=["zu dem"]),
        ],
    )

    schreib_pid = f"{pid}-schreiben"
    schreiben = section(
        "schreiben",
        "schreiben",
        "Schreiben",
        "寫作",
        "Schreiben Sie eine E-Mail (ca. 40–60 Wörter).",
        "寫一封約 40–60 字的郵件。",
        [
            schreiben_item(
                schreib_pid,
                1,
                "Sie möchten Mitglied im Sportverein Grün-Weiß werden. "
                "Schreiben Sie eine E-Mail: Warum interessieren Sie sich? "
                "Welchen Kurs möchten Sie? Wann können Sie starten? "
                "Fragen Sie nach dem Preis.",
                "你想加入綠白體育會。說明興趣原因、想上哪門課、何時開始，並詢問費用。",
                40,
                "Guten Tag,\nich interessiere mich für Sport und möchte Mitglied werden. "
                "Besonders Yoga am Dienstag gefällt mir. Kann ich ab April starten? "
                "Wie viel kostet die Mitgliedschaft genau?\nVielen Dank\nSara Nguyen",
                [
                    "說明動機",
                    "點名課程",
                    "提出開始時間",
                    "詢問價格",
                    "禮貌問候與結尾",
                ],
            )
        ],
    )

    sprech_pid = f"{pid}-sprechen"
    sprechen = section(
        "sprechen",
        "sprechen",
        "Sprechen",
        "口說",
        "Sprechen Sie zu den Themen.",
        "依題口述。",
        [
            sprechen_item(
                sprech_pid,
                1,
                "Erzählen Sie von Ihrer Freizeit: Was machen Sie gerne?",
                "談談你的休閒：喜歡做什麼？",
                ["Wie oft?", "Mit wem?", "Warum?"],
                "In meiner Freizeit mache ich gerne Sport. Zweimal in der Woche gehe ich schwimmen. "
                "Manchmal treffe ich Freunde im Park. Sport hilft mir, mich zu entspannen.",
            ),
            sprechen_item(
                sprech_pid,
                2,
                "Möchten Sie in einem Verein Mitglied sein? Warum (nicht)?",
                "想不想加入社團？為什麼？",
                ["Vorteile", "Nachteile", "Ihre Meinung"],
                "Ja, ich möchte in einem Verein sein, weil man neue Leute kennenlernt "
                "und regelmäßig trainiert. Es kostet etwas Geld, aber es lohnt sich.",
            ),
        ],
    )

    return paper(
        "A2",
        1,
        "Goethe-Format A2 · Modellsatz 1",
        "德檢模擬 A2 · 模考一（體育社團／休閒）",
        70,
        [lesen, hoeren, bausteine, schreiben, sprechen],
    )


# ═══════════════════════════════════════════════════════════════════════════
# A2 · Modellsatz 2 — Reise / Bahnhof
# ═══════════════════════════════════════════════════════════════════════════


def a2_m2() -> dict[str, Any]:
    pid = "a2-m2"
    lesen_pid = f"{pid}-lesen"
    passage = (
        "Hinweise für Reisende – Bahnhof Süd\n\n"
        "Wegen Bauarbeiten fahren die Züge nach Hamburg ab Gleis 8 statt Gleis 3. "
        "Die Regionalbahn RB12 nach Leipzig hat heute 20 Minuten Verspätung. "
        "Der Fahrkartenautomat neben dem Kiosk akzeptiert nur Karten, kein Bargeld. "
        "Im Reisezentrum (Öffnung 6–21 Uhr) helfen wir bei Umbuchungen. "
        "Gepäckschließfächer stehen in der Unterführung. "
        "Achtung: Am Bahnsteig bitte hinter der gelben Linie warten. "
        "WLAN „BahnHotspot“ ist gratis für 60 Minuten."
    )
    passage_zh = (
        "南站旅客須知\n\n"
        "因施工，前往漢堡的列車改由 8 月台發車（原為 3 月台）。"
        "往萊比錫的區域列車 RB12 今天誤點 20 分鐘。"
        "售票機（報刊亭旁）只收卡、不收現金。"
        "旅遊服務中心（6–21 點）可協助改票。"
        "置物櫃在地下通道。月台請站在黃線後方。"
        "免費 Wi‑Fi「BahnHotspot」可用 60 分鐘。"
    )
    lesen = section(
        "lesen",
        "lesen",
        "Lesen",
        "閱讀",
        "Lesen Sie die Hinweise und antworten Sie.",
        "閱讀旅客須知並作答。",
        [
            mc(lesen_pid, 1, "Warum ändert sich das Gleis nach Hamburg?", ["Streik", "Bauarbeiten", "Wetter", "Fest"], 1, "Wegen Bauarbeiten。"),
            mc(lesen_pid, 2, "Von welchem Gleis fährt der Zug nach Hamburg?", ["Gleis 3", "Gleis 8", "Gleis 12", "Gleis 1"], 1, "ab Gleis 8。"),
            tf(lesen_pid, 3, "Die RB12 nach Leipzig hat Verspätung.", True, "20 Minuten Verspätung。"),
            tf(lesen_pid, 4, "Am Automaten kann man bar bezahlen.", False, "nur Karten, kein Bargeld。"),
            mc(lesen_pid, 5, "Wann öffnet das Reisezentrum?", ["um 5 Uhr", "um 6 Uhr", "um 8 Uhr", "um 9 Uhr"], 1, "6–21 Uhr。"),
            tf(lesen_pid, 6, "Gepäckschließfächer sind in der Unterführung.", True, "文中寫明。"),
            mc(lesen_pid, 7, "Wo soll man am Bahnsteig warten?", ["vor dem Zug", "hinter der gelben Linie", "im Restaurant", "auf dem Gleis"], 1, "hinter der gelben Linie。"),
            tf(lesen_pid, 8, "WLAN kostet 2 € pro Stunde.", False, "gratis für 60 Minuten。"),
            mc(lesen_pid, 9, "Wie heißt das WLAN?", ["FreeRail", "BahnHotspot", "SüdNet", "TrainFi"], 1, "BahnHotspot。"),
            tf(lesen_pid, 10, "Umbuchungen sind im Reisezentrum möglich.", True, "helfen wir bei Umbuchungen。"),
        ],
        passage=passage,
        passage_zh=passage_zh,
    )

    audio = (
        "Ansagerin: Sehr geehrte Fahrgäste, der Intercity nach Köln "
        "fährt heute von Gleis fünf. Die Abfahrt ist um vierzehn Uhr dreißig. "
        "Bitte haben Sie Ihre Fahrkarten bereit.\n"
        "Fahrgast: Entschuldigung, fährt dieser Zug auch nach Düsseldorf?\n"
        "Schaffner: Ja, Düsseldorf ist der zweite Halt. Ankunft dort gegen fünfzehn Uhr zehn.\n"
        "Fahrgast: Muss ich umsteigen?\n"
        "Schaffner: Nein, Sie bleiben sitzen. Der Zug fährt weiter nach Köln.\n"
        "Fahrgast: Gibt es einen Speisewagen?\n"
        "Schaffner: Ja, im Wagen sieben. Dort bekommen Sie Snacks und Getränke.\n"
        "Fahrgast: Danke schön!\n"
        "Schaffner: Gern geschehen. Gute Fahrt!"
    )
    hoeren_pid = f"{pid}-hoeren"
    hoeren = section(
        "hoeren",
        "hoeren",
        "Hören",
        "聽力",
        "Hören Sie Durchsage und Dialog.",
        "聽廣播與對話後作答。",
        [
            mc(hoeren_pid, 1, "Wohin fährt der Intercity?", ["Berlin", "Köln", "Hamburg", "Leipzig"], 1, "Intercity nach Köln。"),
            mc(hoeren_pid, 2, "Von welchem Gleis?", ["3", "5", "7", "8"], 1, "Gleis fünf。"),
            mc(hoeren_pid, 3, "Wann ist die Abfahrt?", ["14:00", "14:30", "15:10", "16:00"], 1, "vierzehn Uhr dreißig。"),
            mc(hoeren_pid, 4, "Ist Düsseldorf der erste Halt?", ["Ja", "Nein, der zweite", "Es hält nicht", "Nur Endstation"], 1, "der zweite Halt。"),
            mc(hoeren_pid, 5, "Wann Ankunft in Düsseldorf?", ["14:30", "15:10", "15:30", "16:10"], 1, "gegen fünfzehn Uhr zehn。"),
            mc(hoeren_pid, 6, "Muss der Fahrgast umsteigen?", ["Ja", "Nein", "Nur nach Köln", "In Wagen 7"], 1, "Nein, Sie bleiben sitzen。"),
            mc(hoeren_pid, 7, "Wo ist der Speisewagen?", ["Wagen 3", "Wagen 5", "Wagen 7", "kein Speisewagen"], 2, "im Wagen sieben。"),
            mc(hoeren_pid, 8, "Was gibt es im Speisewagen?", ["Nur Kaffee", "Snacks und Getränke", "Nur Zeitung", "Freie Plätze"], 1, "Snacks und Getränke。"),
        ],
        audio_text=audio,
    )

    bau_pid = f"{pid}-bausteine"
    bausteine = section(
        "bausteine",
        "bausteine",
        "Bausteine",
        "語法詞彙",
        "Ergänzen Sie korrekt.",
        "正確填空／選擇。",
        [
            mc(bau_pid, 1, "Der Zug ___ von Gleis 5.", ["fährt", "fahrt", "fahren", "fährst"], 0, "第三人稱 fährt。"),
            gap(bau_pid, 2, "Wegen ___ fährt der Zug von einem anderen Gleis.", "Bauarbeiten", "Wegen + Genitiv／複數名詞。"),
            mc(bau_pid, 3, "Die Bahn hat 20 Minuten ___.", ["Verspätung", "Verspätungen", "verspäten", "spät"], 0, "Verspätung haben。"),
            gap(bau_pid, 4, "Am Automaten kann man ___ bar bezahlen.", "nicht", "nicht＝不能。", accept=["kein"]),
            mc(bau_pid, 5, "Bitte ___ Sie hinter der Linie.", ["warten", "warte", "wartet", "wartest"], 0, "Sie 用 warten（命令式 warten Sie）。"),
            gap(bau_pid, 6, "WLAN ist ___ für 60 Minuten.", "gratis", "gratis＝免費。", accept=["kostenlos", "umsonst"]),
            mc(bau_pid, 7, "Düsseldorf ist der ___ Halt.", ["zwei", "zweite", "zweiten", "zweiter"], 1, "序數 der zweite。"),
            gap(bau_pid, 8, "Muss ich ___?", "umsteigen", "umsteigen＝換車。"),
            mc(bau_pid, 9, "Gute ___!", ["Fahrt", "Fahr", "Fahren", "Gefahren"], 0, "Gute Fahrt＝一路順風。"),
            gap(bau_pid, 10, "Der Zug fährt weiter ___ Köln.", "nach", "nach + 城市。"),
        ],
    )

    schreib_pid = f"{pid}-schreiben"
    schreiben = section(
        "schreiben",
        "schreiben",
        "Schreiben",
        "寫作",
        "Schreiben Sie eine Nachricht (ca. 50 Wörter).",
        "寫約 50 字訊息。",
        [
            schreiben_item(
                schreib_pid,
                1,
                "Ihr Zug hat Verspätung. Schreiben Sie einer Freundin: "
                "Welcher Zug? Wie viel Verspätung? Wann kommen Sie an? "
                "Was soll sie tun (warten / später kommen)?",
                "火車誤點。寫給朋友：哪班車、誤點多久、何時到、請她怎麼做。",
                40,
                "Liebe Mia,\nmein Zug RB12 nach Leipzig hat 20 Minuten Verspätung. "
                "Ich komme erst gegen 16:40 an. Bitte warte am Ausgang Süd "
                "oder komm etwas später. Bis gleich!\nJonas",
                [
                    "說明哪班車",
                    "說明誤點時間",
                    "給出新到達時間",
                    "給朋友明確指示",
                ],
            )
        ],
    )

    sprech_pid = f"{pid}-sprechen"
    sprechen = section(
        "sprechen",
        "sprechen",
        "Sprechen",
        "口說",
        "Sprechen Sie über Reisen.",
        "談談旅行。",
        [
            sprechen_item(
                sprech_pid,
                1,
                "Erzählen Sie von Ihrer letzten Reise: Wohin? Womit? Was war gut/schlecht?",
                "談談上次旅行：去哪、交通、優缺點。",
                ["Ziel", "Verkehrsmittel", "Erlebnis"],
                "Letzte Woche bin ich mit dem Zug nach Köln gefahren. "
                "Die Fahrt war bequem, aber wir hatten etwas Verspätung. "
                "In der Stadt habe ich den Dom besichtigt.",
            ),
        ],
    )

    return paper(
        "A2",
        2,
        "Goethe-Format A2 · Modellsatz 2",
        "德檢模擬 A2 · 模考二（旅行／火車站）",
        70,
        [lesen, hoeren, bausteine, schreiben, sprechen],
    )


# ═══════════════════════════════════════════════════════════════════════════
# B1 · Modellsatz 1 — Praktikum / Arbeit
# ═══════════════════════════════════════════════════════════════════════════


def b1_m1() -> dict[str, Any]:
    pid = "b1-m1"
    lesen_pid = f"{pid}-lesen"
    passage = (
        "Praktikum im Kulturbüro der Stadt Linden\n\n"
        "Das Kulturbüro sucht ab September eine Praktikantin / einen Praktikanten "
        "(Vollzeit, 3 Monate). Aufgaben: Unterstützung bei der Organisation von "
        "Stadtteilfesten, Pflege der Social-Media-Kanäle und Betreuung von Gästen "
        "bei Veranstaltungen. Voraussetzungen: gute Deutschkenntnisse (mindestens B1), "
        "Interesse an Kultur und zuverlässige Arbeitsweise. Erfahrungen mit "
        "Bildbearbeitung sind von Vorteil, aber nicht Pflicht. "
        "Vergütung: 450 € monatlich. Arbeitszeit: Mo–Fr 9–17 Uhr, gelegentlich "
        "Abend- oder Wochenendeinsätze (werden ausgeglichen). "
        "Bewerbung mit Lebenslauf und kurzem Motivationsschreiben bis 15. Juni "
        "an praktikum@kultur-linden.de. Spät eingesendete Unterlagen können "
        "leider nicht berücksichtigt werden."
    )
    passage_zh = (
        "林登市文化局實習\n\n"
        "文化局自九月起徵實習（全職三個月）。工作：協助籌辦街區活動、"
        "維護社群媒體、活動現場接待來賓。條件：德語至少 B1、對文化有興趣、"
        "做事可靠。影像處理經驗佳，非必須。月津貼 450 歐。工時週一至五 9–17，"
        "偶有晚間／週末（可補休）。請於六月十五日前將履歷與短動機信寄至 "
        "praktikum@kultur-linden.de。逾期恕不受理。"
    )
    lesen = section(
        "lesen",
        "lesen",
        "Lesen",
        "閱讀",
        "Lesen Sie die Stellenanzeige und wählen Sie.",
        "閱讀職缺公告並選擇。",
        [
            mc(lesen_pid, 1, "Wann beginnt das Praktikum?", ["Im Juni", "Im Juli", "Ab September", "Im Dezember"], 2, "ab September。"),
            mc(lesen_pid, 2, "Wie lange dauert es?", ["1 Monat", "3 Monate", "6 Monate", "1 Jahr"], 1, "3 Monate。"),
            mc(lesen_pid, 3, "Welche Aufgabe gehört dazu?", ["Buchhaltung führen", "Social Media pflegen", "Gebäude reinigen", "Tickets verkaufen nur"], 1, "Pflege der Social-Media-Kanäle。"),
            mc(lesen_pid, 4, "Welches Sprachniveau wird erwartet?", ["A2", "B1", "C1", "kein Deutsch"], 1, "mindestens B1。"),
            tf(lesen_pid, 5, "Bildbearbeitung ist Pflicht.", False, "von Vorteil, aber nicht Pflicht。"),
            mc(lesen_pid, 6, "Wie hoch ist die Vergütung?", ["unbezahlt", "450 € / Monat", "1000 € / Monat", "Stundenlohn 15 €"], 1, "450 € monatlich。"),
            tf(lesen_pid, 7, "Es gibt nie Arbeit am Wochenende.", False, "gelegentlich … Wochenendeinsätze。"),
            mc(lesen_pid, 8, "Bis wann muss man sich bewerben?", ["1. Juni", "15. Juni", "1. September", "15. September"], 1, "bis 15. Juni。"),
            tf(lesen_pid, 9, "Späte Bewerbungen werden trotzdem angenommen.", False, "können leider nicht berücksichtigt werden。"),
            mc(lesen_pid, 10, "Was soll die Bewerbung enthalten?", ["nur Foto", "Lebenslauf und Motivationsschreiben", "Zeugnis vom Sport", "Führerschein"], 1, "Lebenslauf und kurzes Motivationsschreiben。"),
            mc(lesen_pid, 11, "Wohin schickt man die Unterlagen?", ["per Post ans Rathaus", "an praktikum@kultur-linden.de", "nur WhatsApp", "ins Reisezentrum"], 1, "指定信箱。"),
        ],
        passage=passage,
        passage_zh=passage_zh,
    )

    audio = (
        "Moderatorin: Willkommen bei „Jobtalk“. Heute ist Markus Klein zu Gast. "
        "Er hat ein Praktikum im Kulturbüro gemacht.\n"
        "Markus: Hallo!\n"
        "Moderatorin: Markus, was hat Ihnen am besten gefallen?\n"
        "Markus: Die Abwechslung. An einem Tag habe ich Posts geschrieben, "
        "am nächsten habe ich Künstler empfangen.\n"
        "Moderatorin: Gab es auch schwierige Momente?\n"
        "Markus: Ja, bei einem Fest im Regen. Wir mussten schnell Zelte aufbauen. "
        "Aber das Team hat super zusammengearbeitet.\n"
        "Moderatorin: Würden Sie das Praktikum weiterempfehlen?\n"
        "Markus: Auf jeden Fall – besonders wenn man Organisation und Kultur mag. "
        "Man lernt viel über Termine und Kommunikation.\n"
        "Moderatorin: Ein Tipp für Bewerberinnen und Bewerber?\n"
        "Markus: Schreibt im Motivationsschreiben, warum euch die Stadt interessiert. "
        "Und seid pünktlich – das ist wichtig.\n"
        "Moderatorin: Danke, Markus!\n"
        "Markus: Danke Ihnen."
    )
    hoeren_pid = f"{pid}-hoeren"
    hoeren = section(
        "hoeren",
        "hoeren",
        "Hören",
        "聽力",
        "Hören Sie das Gespräch und wählen Sie.",
        "聽對談後選擇。",
        [
            mc(hoeren_pid, 1, "Wo hat Markus praktiziert?", ["Bank", "Kulturbüro", "Krankenhaus", "Schule"], 1, "im Kulturbüro。"),
            mc(hoeren_pid, 2, "Was gefiel ihm am besten?", ["Das Gehalt", "Die Abwechslung", "Die Ferien", "Das pendeln"], 1, "Die Abwechslung。"),
            mc(hoeren_pid, 3, "Was hat er unter anderem gemacht?", ["Posts geschrieben", "nur geputzt", "nur gekocht", "Autos repariert"], 0, "Posts geschrieben。"),
            mc(hoeren_pid, 4, "Was war schwierig?", ["Ein Fest im Regen", "Keine Aufgaben", "Zu viel Freizeit", "Sprachtest"], 0, "Fest im Regen。"),
            mc(hoeren_pid, 5, "Was musste das Team schnell machen?", ["Zelte aufbauen", "Tickets drucken", "Essen kochen", "Filme drehen"], 0, "Zelte aufbauen。"),
            mc(hoeren_pid, 6, "Für wen empfiehlt er das Praktikum besonders?", ["Nur für Lehrer", "Wer Organisation und Kultur mag", "Nur für Sportler", "Nur für Touristen"], 1, "Organisation und Kultur。"),
            mc(hoeren_pid, 7, "Was lernt man laut Markus?", ["nur Englisch", "Termine und Kommunikation", "nur Kochen", "Autofahren"], 1, "Termine und Kommunikation。"),
            mc(hoeren_pid, 8, "Sein Tipp fürs Motivationsschreiben?", ["Stadt weglassen", "warum die Stadt interessiert", "nur Humor", "kein Lebenslauf"], 1, "warum euch die Stadt interessiert。"),
            mc(hoeren_pid, 9, "Was ist ihm außerdem wichtig?", ["Pünktlichkeit", "Teure Kleidung", "Späte Ankunft", "Lange Pausen"], 0, "seid pünktlich。"),
        ],
        audio_text=audio,
    )

    bau_pid = f"{pid}-bausteine"
    bausteine = section(
        "bausteine",
        "bausteine",
        "Bausteine",
        "語法詞彙",
        "Wählen Sie die passende Form / Ergänzung.",
        "選出正確形式或填空。",
        [
            mc(bau_pid, 1, "Ich bewerbe mich ___ die Stelle.", ["um", "für", "an", "gegen"], 0, "sich bewerben um。"),
            gap(bau_pid, 2, "Die Unterlagen müssen bis 15. Juni ___ werden.", "eingesendet", "被動：eingesendet werden。", accept=["geschickt", "eingereicht"]),
            mc(bau_pid, 3, "___ ich Interesse an Kultur habe, passe ich gut.", ["Weil", "Obwohl", "Damit", "Ob"], 0, "Weil＝因為。"),
            gap(bau_pid, 4, "Erfahrungen ___ Bildbearbeitung sind von Vorteil.", "mit", "Erfahrungen mit。"),
            mc(bau_pid, 5, "Abendstunden ___ ausgeglichen.", ["werden", "wird", "wurde", "worden"], 0, "複數 Stunden → werden。"),
            gap(bau_pid, 6, "Bitte schicken Sie uns Ihren ___.", "Lebenslauf", "Lebenslauf＝履歷。"),
            mc(bau_pid, 7, "Späte Bewerbungen können nicht ___ werden.", ["berücksichtigt", "berücksichtigen", "berücksichtige", "berücksichtigtst"], 0, "被動過去分詞 berücksichtigt。"),
            gap(bau_pid, 8, "Man ___ viel über Kommunikation.", "lernt", "man lernt。"),
            mc(bau_pid, 9, "Schreiben Sie, ___ Sie die Stadt interessiert.", ["warum", "wann", "wohin", "wessen"], 0, "warum＝為何。"),
            gap(bau_pid, 10, "Seien Sie bitte ___.", "pünktlich", "pünktlich＝準時。"),
        ],
    )

    schreib_pid = f"{pid}-schreiben"
    schreiben = section(
        "schreiben",
        "schreiben",
        "Schreiben",
        "寫作",
        "Schreiben Sie ein Motivationsschreiben (ca. 80–100 Wörter).",
        "寫動機信約 80–100 字。",
        [
            schreiben_item(
                schreib_pid,
                1,
                "Bewerbung um das Praktikum im Kulturbüro Linden. "
                "Gehen Sie auf: Ihre Motivation, Ihre Stärken, "
                "verfügbare Zeit ab September, Abschlussformel.",
                "應徵林登文化局實習：動機、優勢、九月起可上班、正式結尾。",
                80,
                "Sehr geehrte Damen und Herren,\nich bewerbe mich um das Praktikum ab September. "
                "Kultur und Veranstaltungen interessieren mich sehr. "
                "Während meines Studiums habe ich bereits Social-Media-Beiträge gestaltet "
                "und bei einem Stadtfest geholfen. Ich arbeite zuverlässig und lerne schnell. "
                "Ab dem 1. September bin ich Vollzeit verfügbar.\n"
                "Über eine Einladung zum Gespräch würde ich mich freuen.\n"
                "Mit freundlichen Grüßen\nLea Hoffmann",
                [
                    "正式稱呼與結尾",
                    "說明動機",
                    "提到相關經驗／優勢",
                    "說明可開始時間",
                    "字數約 80 以上",
                ],
            )
        ],
    )

    sprech_pid = f"{pid}-sprechen"
    sprechen = section(
        "sprechen",
        "sprechen",
        "Sprechen",
        "口說",
        "Sprechen Sie zusammenhängend.",
        "連貫口述。",
        [
            sprechen_item(
                sprech_pid,
                1,
                "Was ist Ihnen bei einem Praktikum oder Job wichtig? Begründen Sie.",
                "實習／工作上什麼對你重要？請說明理由。",
                ["Team", "Lernchance", "Arbeitszeiten", "Vergütung"],
                "Mir ist ein gutes Team wichtig, weil man sich gegenseitig hilft. "
                "Außerdem möchte ich etwas Neues lernen. Flexible Arbeitszeiten wären schön, "
                "aber Pünktlichkeit finde ich genauso wichtig.",
            ),
            sprechen_item(
                sprech_pid,
                2,
                "Beschreiben Sie eine Situation, in der Sie organisiert haben oder helfen mussten.",
                "描述一次你必須組織或幫忙的經驗。",
                ["Was passierte?", "Was haben Sie getan?", "Ergebnis"],
                "Bei einem Schulfest hat es plötzlich geregnet. "
                "Ich habe mit anderen schnell Tische nach drinnen getragen. "
                "Am Ende konnte das Fest trotzdem stattfinden.",
            ),
        ],
    )

    return paper(
        "B1",
        1,
        "Goethe-Format B1 · Modellsatz 1",
        "德檢模擬 B1 · 模考一（實習／職場）",
        100,
        [lesen, hoeren, bausteine, schreiben, sprechen],
    )


# ═══════════════════════════════════════════════════════════════════════════
# B1 · Modellsatz 2 — Umwelt / Stadtplanung
# ═══════════════════════════════════════════════════════════════════════════


def b1_m2() -> dict[str, Any]:
    pid = "b1-m2"
    lesen_pid = f"{pid}-lesen"
    passage = (
        "Mehr Grün für die Innenstadt – Bürgerinformation\n\n"
        "Die Stadtverwaltung plant, zwei Parkplätze an der Marktstraße in "
        "eine kleine Grünfläche umzuwandeln. Dort sollen Bäume, Sitzbänke und "
        "eine Trinkwasserstelle entstehen. Ziel ist es, die Aufenthaltsqualität "
        "zu verbessern und im Sommer für Schatten zu sorgen. "
        "Kritikerinnen und Kritiker befürchten weniger Parkraum für Kundschaft "
        "der Geschäfte. Deshalb wird gleichzeitig ein Parkhaus am Bahnhof "
        "erweitert; die ersten 30 Minuten bleiben dort kostenlos. "
        "Eine Online-Umfrage läuft bis Ende des Monats. Die endgültige "
        "Entscheidung fällt im Stadtrat im Oktober. "
        "Informationsabend: 8. September, 19 Uhr, Rathaussaal – Eintritt frei, "
        "Anmeldung erwünscht."
    )
    passage_zh = (
        "市中心多一點綠意 – 市民資訊\n\n"
        "市政府計畫把市場街兩處停車格改成小綠地，設置樹木、座椅與飲水點，"
        "以提升停留品質並在夏天提供樹蔭。反對者擔心商家顧客停車位減少；"
        "因此車站旁停車場將擴建，且前 30 分鐘免費。線上問卷開放至月底，"
        "市議會十月做最終決定。說明會：九月八日晚七點市政廳大廳，免費，建議報名。"
    )
    lesen = section(
        "lesen",
        "lesen",
        "Lesen",
        "閱讀",
        "Lesen Sie den Text und beantworten Sie die Fragen.",
        "閱讀市民資訊並作答。",
        [
            mc(lesen_pid, 1, "Was soll an der Marktstraße entstehen?", ["Ein Einkaufszentrum", "Eine Grünfläche", "Ein Kino", "Ein Hotel"], 1, "kleine Grünfläche。"),
            mc(lesen_pid, 2, "Wie viele Parkplätze werden umgewandelt?", ["einer", "zwei", "zehn", "alle"], 1, "zwei Parkplätze。"),
            tf(lesen_pid, 3, "Es soll auch eine Trinkwasserstelle geben.", True, "文中列出。"),
            mc(lesen_pid, 4, "Was ist ein Ziel der Maßnahme?", ["Mehr Autolärm", "Mehr Schatten im Sommer", "Höhere Steuern", "Weniger Bäume"], 1, "für Schatten zu sorgen。"),
            tf(lesen_pid, 5, "Alle Geschäfte unterstützen den Plan ohne Kritik.", False, "Kritiker befürchten weniger Parkraum。"),
            mc(lesen_pid, 6, "Was passiert am Bahnhof?", ["Schließung", "Parkhaus wird erweitert", "Nur Fahrräder", "Keine Änderung"], 1, "Parkhaus … erweitert。"),
            tf(lesen_pid, 7, "Die ersten 30 Minuten im Parkhaus sind kostenlos.", True, "bleiben … kostenlos。"),
            mc(lesen_pid, 8, "Bis wann läuft die Umfrage?", ["bis Ende des Monats", "bis Oktober", "nur einen Tag", "gar nicht"], 0, "bis Ende des Monats。"),
            mc(lesen_pid, 9, "Wann entscheidet der Stadtrat?", ["Im August", "Im September", "Im Oktober", "Im Dezember"], 2, "im Oktober。"),
            tf(lesen_pid, 10, "Der Informationsabend kostet Eintritt.", False, "Eintritt frei。"),
            mc(lesen_pid, 11, "Wann ist der Informationsabend?", ["8.9., 19 Uhr", "8.10., 9 Uhr", "19.8., 8 Uhr", "nur online"], 0, "8. September, 19 Uhr。"),
        ],
        passage=passage,
        passage_zh=passage_zh,
    )

    audio = (
        "Nachbarin: Hast du die Pläne für die Marktstraße gelesen?\n"
        "Nachbar: Ja. Ich finde die Idee gut – endlich mehr Bäume. "
        "Im Sommer ist es dort viel zu heiß.\n"
        "Nachbarin: Stimmt. Aber meine Mutter kommt mit dem Auto zum Arzt. "
        "Wenn die Parkplätze weg sind, wird es für sie schwerer.\n"
        "Nachbar: Deshalb erweitern sie doch das Parkhaus. "
        "Und die ersten dreißig Minuten sind gratis.\n"
        "Nachbarin: Das hilft ein bisschen. Ich werde trotzdem zur Bürgerversammlung gehen "
        "und Fragen stellen.\n"
        "Nachbar: Gute Idee. Ich fülle auch die Online-Umfrage aus. "
        "Ich schlage vor, mehr Fahrradständer neben die Bänke zu stellen.\n"
        "Nachbarin: Super. Sollen wir zusammen am achten September hingehen?\n"
        "Nachbar: Ja, um viertel vor sieben vor dem Rathaus?\n"
        "Nachbarin: Passt. Bis dann!"
    )
    hoeren_pid = f"{pid}-hoeren"
    hoeren = section(
        "hoeren",
        "hoeren",
        "Hören",
        "聽力",
        "Hören Sie den Dialog der Nachbarn.",
        "聽鄰居對話後作答。",
        [
            mc(hoeren_pid, 1, "Was findet der Nachbar gut?", ["Weniger Bäume", "Mehr Bäume", "Mehr Autos", "Kein Parkhaus"], 1, "endlich mehr Bäume。"),
            mc(hoeren_pid, 2, "Warum ist die Marktstraße im Sommer problematisch?", ["zu kalt", "zu heiß", "zu dunkel", "zu laut nur nachts"], 1, "viel zu heiß。"),
            mc(hoeren_pid, 3, "Warum ist die Nachbarin unsicher?", ["Ihre Mutter kommt mit dem Auto", "Sie hasst Bänke", "Kein WLAN", "Zu viele Fahrräder"], 0, "Mutter kommt mit dem Auto。"),
            mc(hoeren_pid, 4, "Was erwähnt der Nachbar zum Parkhaus?", ["Es schließt", "Es wird erweitert; 30 Min gratis", "Nur für Busse", "Kosten 20 €"], 1, "erweitern … dreißig Minuten gratis。"),
            mc(hoeren_pid, 5, "Wohin will die Nachbarin gehen?", ["Zur Bürgerversammlung", "Zum Strand", "Nur online chatten", "Ins Kino"], 0, "zur Bürgerversammlung。"),
            mc(hoeren_pid, 6, "Was schlägt der Nachbar in der Umfrage vor?", ["Mehr Parkplätze in der Straße", "Mehr Fahrradständer", "Kein Trinkwasser", "Nachtclub"], 1, "mehr Fahrradständer。"),
            mc(hoeren_pid, 7, "Wann treffen sie sich?", ["8.9., 18:45", "8.9., 19:30", "9.8., 7:00", "nur online"], 0, "vierten vor sieben＝18:45。"),
            mc(hoeren_pid, 8, "Wo treffen sie sich?", ["vor dem Rathaus", "am Bahnhof", "im Parkhaus", "zu Hause"], 0, "vor dem Rathaus。"),
            mc(hoeren_pid, 9, "Füllen beide die Umfrage aus?", ["Nur sie", "Er will sie ausfüllen; sie geht zur Versammlung", "Niemand", "Nur die Mutter"], 1, "他填問卷、她去說明會。"),
        ],
        audio_text=audio,
    )

    bau_pid = f"{pid}-bausteine"
    bausteine = section(
        "bausteine",
        "bausteine",
        "Bausteine",
        "語法詞彙",
        "Grammatik passend zum Textniveau B1.",
        "B1 程度語法詞彙。",
        [
            mc(bau_pid, 1, "Zwei Parkplätze sollen ___ eine Grünfläche umgewandelt werden.", ["in", "an", "auf", "bei"], 0, "umwandeln in。"),
            gap(bau_pid, 2, "Ziel ist es, die Qualität ___.", "zu verbessern", "um … zu / Ziel ist es zu + Inf。", accept=["zu verbessern"]),
            mc(bau_pid, 3, "Kritiker ___ weniger Parkraum.", ["befürchten", "befürchtet", "befürchte", "befürchtest"], 0, "複數 Kritiker → befürchten。"),
            gap(bau_pid, 4, "Die ersten 30 Minuten bleiben ___.", "kostenlos", "kostenlos＝免費。", accept=["gratis", "umsonst"]),
            mc(bau_pid, 5, "Die Entscheidung fällt ___, Oktober.", ["im", "am", "um", "seit"], 0, "im Oktober。"),
            gap(bau_pid, 6, "Anmeldung ist ___.", "erwünscht", "erwünscht＝建議／希望報名。"),
            mc(bau_pid, 7, "___ die Parkplätze weg sind, wird es schwerer.", ["Wenn", "Als", "Bevor", "Damit"], 0, "Wenn＝如果／當。"),
            gap(bau_pid, 8, "Ich schlage ___, mehr Fahrradständer zu stellen.", "vor", "vorschlagen → schlage … vor。"),
            mc(bau_pid, 9, "Sollen wir ___ hingehen?", ["zusammen", "zusammenen", "zusammenes", "zusammens"], 0, "zusammen。"),
            gap(bau_pid, 10, "Treffen wir uns um Viertel ___ sieben?", "vor", "Viertel vor＝差一刻。"),
        ],
    )

    schreib_pid = f"{pid}-schreiben"
    schreiben = section(
        "schreiben",
        "schreiben",
        "Schreiben",
        "寫作",
        "Schreiben Sie einen Forumsbeitrag (ca. 80–100 Wörter).",
        "寫論壇留言約 80–100 字。",
        [
            schreiben_item(
                schreib_pid,
                1,
                "Forumsthema: Grünfläche statt Parkplätze – ja oder nein? "
                "Schreiben Sie Ihre Meinung, nennen Sie ein Argument dafür und eines dagegen, "
                "machen Sie einen Kompromissvorschlag.",
                "論壇：綠地取代車位？表達立場、正反各一論點，並提折衷方案。",
                80,
                "Meiner Meinung nach ist mehr Grün in der Innenstadt wichtig, "
                "weil Schatten und Sitzplätze die Straße lebendiger machen. "
                "Andererseits brauchen manche Kundinnen und Kunden kurze Parkmöglichkeiten. "
                "Ein guter Kompromiss wäre: die Grünfläche bauen und gleichzeitig "
                "das Parkhaus am Bahnhof klar ausschildern. Außerdem sollten mehr "
                "Fahrradständer entstehen.",
                [
                    "清楚表達立場",
                    "至少一個贊成理由",
                    "至少一個反對／顧慮",
                    "提出折衷建議",
                    "語句連貫、約 80 字",
                ],
            )
        ],
    )

    sprech_pid = f"{pid}-sprechen"
    sprechen = section(
        "sprechen",
        "sprechen",
        "Sprechen",
        "口說",
        "Nehmen Sie Stellung.",
        "發表看法。",
        [
            sprechen_item(
                sprech_pid,
                1,
                "Sollte Ihre Stadt mehr Grünflächen oder mehr Parkplätze haben? Begründen Sie.",
                "你的城市該多綠地還是多車位？請說明。",
                ["Ihre Stadt", "Vorteile", "Nachteile", "Kompromiss"],
                "Ich finde, wir brauchen mehr Grünflächen, weil die Sommer immer heißer werden. "
                "Parkplätze sind auch wichtig, aber man kann Parkhäuser nutzen. "
                "Ein Mix aus Bäumen, Bänken und guter ÖPNV-Anbindung wäre ideal.",
            ),
        ],
    )

    return paper(
        "B1",
        2,
        "Goethe-Format B1 · Modellsatz 2",
        "德檢模擬 B1 · 模考二（環境／都市計畫）",
        100,
        [lesen, hoeren, bausteine, schreiben, sprechen],
    )


# ═══════════════════════════════════════════════════════════════════════════
# B2 · Modellsatz 1 — Digitalisierung / Homeoffice
# ═══════════════════════════════════════════════════════════════════════════


def b2_m1() -> dict[str, Any]:
    pid = "b2-m1"
    lesen_pid = f"{pid}-lesen"
    passage = (
        "Homeoffice zwischen Freiheit und Entgrenzung\n\n"
        "Seit der Pandemie ist mobiles Arbeiten in vielen Branchen zur Normalität geworden. "
        "Befürworterinnen und Befürworter betonen die gestiegene Produktivität, kürzere "
        "Pendlerzeiten und eine bessere Vereinbarkeit von Beruf und Privatleben. "
        "Gleichzeitig warnen Arbeitspsychologinnen vor einer schleichenden Entgrenzung: "
        "Wer den Laptop auf dem Küchentisch stehen lässt, beantwortet abends leichter noch "
        "schnell eine Mail – und schläft schlechter. "
        "Unternehmen reagieren unterschiedlich. Während manche feste Kernarbeitszeiten und "
        "ein Recht auf Nichterreichbarkeit festschreiben, setzen andere auf Vertrauensarbeitszeit "
        "ohne klare Leitplanken. Studien deuten darauf hin, dass hybride Modelle – etwa drei "
        "Tage im Büro, zwei zu Hause – sowohl den Teamzusammenhalt als auch die individuelle "
        "Flexibilität stützen können, sofern Führungskräfte Ergebnisse statt Präsenz bewerten. "
        "Kritisch bleibt der Zugang: Nicht jede Wohnung bietet einen ruhigen Arbeitsplatz, "
        "und nicht jede Tätigkeit lässt sich digitalisieren. Eine gerechte Regelung müsse daher "
        "branchenspezifisch und sozial ausgewogen sein, fordern Gewerkschaften."
    )
    passage_zh = (
        "居家辦公：自由與界線模糊之間\n\n"
        "疫情以來，許多產業已把遠距工作視為常態。支持者強調生產力上升、通勤變短、"
        "工作與生活更易兼顧。另一方面，工作心理學家警告界線正慢慢消失：筆電放在餐桌上，"
        "晚上更容易「再回一封信」，睡眠也變差。企業反應不一：有的訂定核心工時與「有權不被聯絡」，"
        "有的採信任工時卻缺少清楚規範。研究顯示，混合模式（例如三天辦公室、兩天在家）"
        "若主管以成果而非出席評核，可同時維繫團隊與個人彈性。仍待解決的是公平近用："
        "並非每戶都有安靜工作角落，也非每種工作都能數位化。工會主張規範應依產業調整並兼顾社會公平。"
    )
    assert len(passage) >= 800
    lesen = section(
        "lesen",
        "lesen",
        "Lesen",
        "閱讀",
        "Lesen Sie den Kommentar. Wählen Sie die zutreffende Aussage.",
        "閱讀評論後選出正確理解。",
        [
            mc(lesen_pid, 1, "Was ist laut Text seit der Pandemie in vielen Branchen normal?", ["Nur Präsenzpflicht", "Mobiles Arbeiten", "Nachtarbeit für alle", "Kein Internet"], 1, "mobiles Arbeiten … Normalität。"),
            mc(lesen_pid, 2, "Welches Argument nennen Befürworter?", ["Längere Pendlerzeiten", "Bessere Vereinbarkeit", "Schlechterer Schlaf als Ziel", "Mehr Bürokratie"], 1, "bessere Vereinbarkeit。"),
            mc(lesen_pid, 3, "Wovor warnen Arbeitspsychologinnen?", ["Vor zu vielen Bäumen", "Vor Entgrenzung", "Vor zu kurzen Mails", "Vor Hybridmodellen generell"], 1, "schleichenden Entgrenzung。"),
            mc(lesen_pid, 4, "Was kann laut Text abends leichter passieren?", ["Man schläft sofort", "Man beantwortet noch eine Mail", "Man geht joggen", "Man löscht den Laptop"], 1, "beantwortet … noch schnell eine Mail。"),
            tf(lesen_pid, 5, "Alle Unternehmen haben identische Regeln zum Homeoffice.", False, "Unternehmen reagieren unterschiedlich。"),
            mc(lesen_pid, 6, "Was schreiben manche Firmen fest?", ["Recht auf Nichterreichbarkeit", "Verbot von Pausen", "24h-Erreichbarkeit Pflicht", "Kein Homeoffice"], 0, "Recht auf Nichterreichbarkeit。"),
            mc(lesen_pid, 7, "Was deuten Studien zu hybriden Modellen an?", ["Sie scheitern immer", "Sie können Zusammenhalt und Flexibilität stützen", "Nur Nachteile", "Nur für Schulen"], 1, "Teamzusammenhalt … Flexibilität stützen。"),
            mc(lesen_pid, 8, "Worauf sollten Führungskräfte achten?", ["Nur auf Präsenz", "Ergebnisse statt Präsenz", "Längere Meetings", "Privatleben der Mitarbeitenden kontrollieren"], 1, "Ergebnisse statt Präsenz。"),
            tf(lesen_pid, 9, "Jede Wohnung bietet idealen Arbeitsplatz.", False, "Nicht jede Wohnung …。"),
            mc(lesen_pid, 10, "Was fordern Gewerkschaften?", ["Einheitliche Regel ohne Ausnahme", "Branchenspezifische und sozial ausgewogene Regelung", "Abschaffung aller Büros", "Nur digitale Berufe"], 1, "branchenspezifisch und sozial ausgewogen。"),
            mc(lesen_pid, 11, "Was bedeutet „Entgrenzung“ im Kontext?", ["Mehr Grenzen im Büro", "Verschwimmen von Arbeits- und Privatzeit", "Mehr Urlaubstage", "Kürzere Arbeitsverträge"], 1, "工作與私領域界線模糊。"),
        ],
        passage=passage,
        passage_zh=passage_zh,
    )

    audio = (
        "Podcast-Host: Herzlich willkommen zu unserem Arbeitsleben-Podcast. "
        "Heute sprechen wir über Homeoffice-Regeln und gesunde Grenzen. Zu Gast ist "
        "Dr. Sabine Vogt, Arbeitsforscherin an der Universität Mainz.\n"
        "Vogt: Guten Tag, vielen Dank für die Einladung.\n"
        "Host: Frau Dr. Vogt, sinkt die Produktivität wirklich, wenn Leute zu Hause arbeiten?\n"
        "Vogt: Nicht zwangsläufig. Viele berichten von konzentrierterem Arbeiten, "
        "vor allem bei Aufgaben, die Ruhe und tiefe Konzentration brauchen. "
        "Problematisch wird es allerdings, wenn virtuelle Meetings den ganzen Tag füllen "
        "und keine echten Erholungspausen bleiben. Dann sinkt die Qualität spürbar.\n"
        "Host: Was empfehlen Sie Unternehmen konkret?\n"
        "Vogt: Klare Kernzeiten für gemeinsame Erreichbarkeit, zum Beispiel von zehn bis "
        "fünfzehn Uhr, und danach ein Recht, offline zu sein. Außerdem sollten Teams "
        "feste Präsenztage haben, damit informeller Austausch und spontane Ideen "
        "nicht verloren gehen. Führungskräfte müssen Ergebnisse bewerten, nicht nur Präsenz.\n"
        "Host: Und welchen Rat geben Sie Beschäftigten?\n"
        "Vogt: Richten Sie einen festen Arbeitsplatz zu Hause ein, nehmen Sie Pausen ernst "
        "und pflegen Sie Feierabend-Rituale – etwa den Laptop schließen und kurz spazieren gehen. "
        "Sprechen Sie Erwartungen im Team offen an.\n"
        "Host: Gibt es Gruppen, die besonders benachteiligt werden?\n"
        "Vogt: Ja. Menschen in kleinen Wohnungen oder mit Care-Aufgaben brauchen "
        "zusätzliche Unterstützung, etwa Zugang zu Coworking-Spaces oder flexible Kinderbetreuung. "
        "Ohne solche Angebote bleibt mobiles Arbeiten ungerecht verteilt.\n"
        "Host: Vielen Dank für diese klare Einschätzung.\n"
        "Vogt: Sehr gerne. Ich hoffe, mehr Betriebe setzen Leitplanken statt nur Freiheiten."
    )
    hoeren_pid = f"{pid}-hoeren"
    hoeren = section(
        "hoeren",
        "hoeren",
        "Hören",
        "聽力",
        "Hören Sie das Podcast-Gespräch.",
        "聽 Podcast 訪談後作答。",
        [
            mc(hoeren_pid, 1, "Wer ist zu Gast?", ["Ein Coach ohne Forschung", "Dr. Sabine Vogt", "Nur der Host allein", "Ein IT-Techniker"], 1, "Dr. Sabine Vogt。"),
            mc(hoeren_pid, 2, "Sinkt die Produktivität laut Vogt immer?", ["Ja, immer", "Nicht zwangsläufig", "Nur nachts", "Sie sagt nichts dazu"], 1, "Nicht zwangsläufig。"),
            mc(hoeren_pid, 3, "Wann arbeiten viele zu Hause besonders gut?", ["Bei Aufgaben, die Ruhe brauchen", "Nur in Großraumbüros", "Nur mit Dauer-Meetings", "Nur ohne Internet"], 0, "Aufgaben, die Ruhe brauchen。"),
            mc(hoeren_pid, 4, "Wann wird es problematisch?", ["Wenn Pausen zu lang sind", "Wenn Meetings den Tag füllen", "Wenn man spazieren geht", "Wenn Kernzeiten existieren"], 1, "Meetings den ganzen Tag füllen。"),
            mc(hoeren_pid, 5, "Welche Kernzeit nennt sie als Beispiel?", ["6–9 Uhr", "10–15 Uhr", "18–22 Uhr", "ganztags"], 1, "von zehn bis fünfzehn Uhr。"),
            mc(hoeren_pid, 6, "Was soll danach gelten?", ["Nochmal mehr Meetings", "Recht, offline zu sein", "Pflicht zu chatten", "Büroschließung"], 1, "Recht, offline zu sein。"),
            mc(hoeren_pid, 7, "Warum feste Präsenztage?", ["Damit niemand Urlaub nimmt", "Damit informeller Austausch bleibt", "Nur für Kontrolle", "Für mehr Pendeln"], 1, "informeller Austausch。"),
            mc(hoeren_pid, 8, "Welches Feierabend-Ritual nennt sie?", ["Laptop offen lassen", "Laptop schließen und spazieren", "Mails um Mitternacht", "Kein Ritual"], 1, "Laptop schließen und spazieren gehen。"),
            mc(hoeren_pid, 9, "Wer kann benachteiligt sein?", ["Nur Manager", "Menschen in kleinen Wohnungen / mit Care-Aufgaben", "Nur Studierende", "Niemand"], 1, "kleinen Wohnungen oder Care-Aufgaben。"),
            mc(hoeren_pid, 10, "Welche Unterstützung erwähnt sie?", ["Zugang zu Coworking-Spaces", "Kostenlose Autos", "Längere Nachtschichten", "Abschaffung von Pausen"], 0, "Coworking-Spaces。"),
        ],
        audio_text=audio,
    )

    bau_pid = f"{pid}-bausteine"
    bausteine = section(
        "bausteine",
        "bausteine",
        "Bausteine",
        "語法詞彙",
        "Präzise Formulierungen auf B2-Niveau.",
        "B2 精準表達。",
        [
            mc(bau_pid, 1, "Mobiles Arbeiten ist ___ Normalität geworden.", ["zur", "zum", "zur der", "in die"], 0, "zur Normalität werden。"),
            gap(bau_pid, 2, "Studien ___ darauf hin, dass Hybridmodelle helfen können.", "deuten", "darauf hindeuten。"),
            mc(bau_pid, 3, "___ Führungskräfte Ergebnisse bewerten, funktioniert Hybrid besser.", ["Sofern", "Seitdem ohne Sinn", "Bevor nie", "Ohne dass falsch"], 0, "sofern＝只要。"),
            gap(bau_pid, 4, "Manche schreiben ein Recht auf ___ fest.", "Nichterreichbarkeit", "Nichterreichbarkeit。"),
            mc(bau_pid, 5, "Nicht jede Tätigkeit lässt sich ___.", ["digitalisieren", "digitalisiert", "digitalisieren lassen falsch doppelt", "zu digital"], 0, "lässt sich + Inf。"),
            gap(bau_pid, 6, "Es besteht die Gefahr einer schleichenden ___.", "Entgrenzung", "Entgrenzung＝界線模糊。"),
            mc(bau_pid, 7, "Sie warnt ___, dass Erholung fehlt.", ["davor", "darauf", "davon", "damit"], 0, "warnen vor / davor, dass。"),
            gap(bau_pid, 8, "Pausen sollte man ___ nehmen.", "ernst", "ernst nehmen。"),
            mc(bau_pid, 9, "Gewerkschaften fordern ___ Regelungen.", ["ausgewogene", "ausgewogenen", "ausgewogenes", "ausgewogen"], 0, "Regelungen 複數 → ausgewogene。"),
            gap(bau_pid, 10, "Hybride Modelle können den Teamzusammenhalt ___.", "stützen", "stützen＝支撐。", accept=["fördern", "stärken"]),
            mc(bau_pid, 11, "___ die Produktivität sinkt, hängt von der Organisation ab.", ["Ob", "Als", "Seit", "Je"], 0, "Ob＝是否。"),
        ],
    )

    schreib_pid = f"{pid}-schreiben"
    schreiben = section(
        "schreiben",
        "schreiben",
        "Schreiben",
        "寫作",
        "Schreiben Sie eine Stellungnahme (ca. 150 Wörter).",
        "撰寫立場文約 150 字。",
        [
            schreiben_item(
                schreib_pid,
                1,
                "Thema: Sollte mobiles Arbeiten gesetzlich stärker geregelt werden? "
                "Einleitung – zwei Argumente – Gegenargument mit Entkräftung – "
                "Schlussfolgerung mit Empfehlung.",
                "題目：遠距工作是否應有更強法律規範？含引言、兩論點、反論與反駁、結論建議。",
                150,
                "Ob mobiles Arbeiten gesetzlich stärker geregelt werden sollte, "
                "ist umstritten. Einerseits schützen klare Regeln Beschäftigte vor "
                "ständiger Erreichbarkeit und fördern gesunde Arbeitszeiten. "
                "Andererseits brauchen Branchen Flexibilität; zu starre Gesetze könnten "
                "Innovation hemmen. Ein Gegenargument lautet, Unternehmen regelten das "
                "besser selbst – doch ohne Mindeststandards bleibt die Macht ungleich. "
                "Daher plädiere ich für Rahmenbedingungen: Recht auf Nichterreichbarkeit, "
                "hybride Leitlinien und Unterstützung für Menschen ohne geeigneten "
                "Arbeitsplatz zu Hause. Details sollten tariflich anpassbar bleiben.",
                [
                    "有引言與清楚立場",
                    "至少兩個支持論點",
                    "有反論並嘗試反駁",
                    "結論含具體建議",
                    "連接詞與複雜句運用得宜",
                    "約 150 字",
                ],
            )
        ],
    )

    sprech_pid = f"{pid}-sprechen"
    sprechen = section(
        "sprechen",
        "sprechen",
        "Sprechen",
        "口說",
        "Präsentieren Sie Ihre Meinung strukturiert.",
        "有結構地陳述看法。",
        [
            sprechen_item(
                sprech_pid,
                1,
                "Diskutieren Sie Vor- und Nachteile von Homeoffice. Kommen Sie zu einer Empfehlung.",
                "討論居家辦公優缺點並提出建議。",
                ["Vorteile", "Nachteile", "Für wen geeignet?", "Empfehlung"],
                "Homeoffice spart Pendelzeit und erhöht oft die Konzentration. "
                "Nachteilig sind Isolation und verschwommene Grenzen. "
                "Für Menschen mit ruhigem Platz und klaren Aufgaben eignet es sich gut. "
                "Ich empfehle hybride Modelle mit Kernzeiten und Präsenztagen.",
            ),
            sprechen_item(
                sprech_pid,
                2,
                "Wie schützen Sie Ihre Work-Life-Balance im Alltag?",
                "日常生活中你如何保護工作生活平衡？",
                ["Rituale", "Technik", "Kommunikation mit dem Team"],
                "Ich schließe den Laptop nach Feierabend und schalte Benachrichtigungen aus. "
                "Mit dem Team kläre ich Erreichbarkeitszeiten. Spaziergänge helfen mir abzuschalten.",
            ),
        ],
    )

    return paper(
        "B2",
        1,
        "Goethe-Format B2 · Modellsatz 1",
        "德檢模擬 B2 · 模考一（數位化／居家辦公）",
        110,
        [lesen, hoeren, bausteine, schreiben, sprechen],
    )


# ═══════════════════════════════════════════════════════════════════════════
# B2 · Modellsatz 2 — Bildung / Studiengebühren
# ═══════════════════════════════════════════════════════════════════════════


def b2_m2() -> dict[str, Any]:
    pid = "b2-m2"
    lesen_pid = f"{pid}-lesen"
    passage = (
        "Studiengebühren: Investition oder soziale Hürde?\n\n"
        "In der Debatte um die Finanzierung von Hochschulen prallen zwei Prinzipien aufeinander: "
        "Bildung als öffentliches Gut versus stärkere Eigenbeteiligung der Studierenden. "
        "Befürworter moderater Gebühren argumentieren, zusätzliche Mittel verbesserten "
        "Betreuungsrelationen, Bibliotheken und digitale Infrastruktur. Wer studiere, "
        "profitiere später von höheren Einkommen – eine Beteiligung sei daher fair. "
        "Gegnerinnen und Gegner entgegnen, Gebühren schreckten gerade Erstakademikerinnen "
        "und Studierende aus einkommensschwächeren Haushalten ab. Schon die Angst vor "
        "Verschuldung könne Bildungsentscheidungen verzerren. International zeige sich, "
        "dass Stipendienprogramme die Ungleichheit nur teilweise ausgleichen, weil "
        "Informationsbarrieren und Bürokratie weiterhin wirkten. "
        "Als Mittelweg diskutieren Expertinnen sozial gestaffelte Beiträge, "
        "nachgelagerte Einkommenssteuern für Absolventinnen und Absolventen sowie "
        "stärkere Investitionen in Studienberatung. Entscheidend sei nicht allein die Höhe "
        "einer Gebühr, sondern ob Zugänge transparent, Beratung frühzeitig und "
        "Unterstützung verlässlich seien. Andernfalls bleibe Chancengleichheit ein Versprechen "
        "ohne ausreichende Praxis."
    )
    passage_zh = (
        "學費：投資還是社會門檻？\n\n"
        "高教經費辯論中，兩個原則對撞：教育作為公共財，或是學生應有更多自付。"
        "贊成適度收費者認為，額外經費能改善師生比、圖書館與數位基礎建設；讀大學者日後收入較高，"
        "分擔成本較公平。反對者則說，學費會嚇跑第一代大學生與低收入家庭學生，光是懼怕負債"
        "就可能扭曲升學選擇。國際經驗顯示，獎學金只能部分弭平不平等，因為資訊落差與行政手續"
        "仍在作用。專家討論折衷：依收入分級繳費、畢業後依所得課徵、加強選課輔導。"
        "關鍵不只在學費高低，而在入學管道是否透明、輔導是否及早、支持是否可靠——"
        "否則機會平等只是口號。"
    )
    assert len(passage) >= 800
    lesen = section(
        "lesen",
        "lesen",
        "Lesen",
        "閱讀",
        "Lesen Sie den Essayauszug und wählen Sie.",
        "閱讀論說文節錄並選擇。",
        [
            mc(lesen_pid, 1, "Welche Prinzipien prallen aufeinander?", ["Nur Sportregeln", "Öffentliches Gut vs. Eigenbeteiligung", "Nur Sprachkurse", "Nur Online-Prüfungen"], 1, "Bildung als öffentliches Gut versus Eigenbeteiligung。"),
            mc(lesen_pid, 2, "Was sollen zusätzliche Mittel laut Befürwortern verbessern?", ["Nur Mensapreise", "Betreuung, Bibliotheken, digitale Infrastruktur", "Nur Parkplätze", "Nur Werbung"], 1, "Betreuungsrelationen, Bibliotheken und digitale Infrastruktur。"),
            mc(lesen_pid, 3, "Warum sei Beteiligung fair laut Befürwortern?", ["Weil niemand studiert", "Weil Studierende später oft höhere Einkommen haben", "Weil Bücher kostenlos sind", "Weil es keine Jobs gibt"], 1, "höhere Einkommen。"),
            mc(lesen_pid, 4, "Wen schrecken Gebühren laut Gegnern besonders ab?", ["Nur Professoren", "Erstakademiker / einkommensschwächere Haushalte", "Nur Touristen", "Nur Rentner"], 1, "Erstakademikerinnen … einkommensschwächeren Haushalten。"),
            tf(lesen_pid, 5, "Angst vor Verschuldung kann Entscheidungen beeinflussen.", True, "kann Bildungsentscheidungen verzerren。"),
            mc(lesen_pid, 6, "Was leisten Stipendien laut Text nur teilweise?", ["Ausgleich von Ungleichheit", "Abschaffung aller Hochschulen", "Kostenlose Flüge", "Mehr Parkraum"], 0, "Ungleichheit nur teilweise ausgleichen。"),
            mc(lesen_pid, 7, "Warum greifen Stipendien nicht vollständig?", ["Weil alle reich sind", "Informationsbarrieren und Bürokratie", "Weil es keine Bibliotheken gibt", "Weil niemand bewirbt"], 1, "Informationsbarrieren und Bürokratie。"),
            mc(lesen_pid, 8, "Welcher Mittelweg wird genannt?", ["Sofortige Schließung", "Sozial gestaffelte Beiträge / nachgelagerte Steuern / bessere Beratung", "Nur höhere Gebühren ohne Hilfe", "Verbot von Studium"], 1, "gestaffelte Beiträge、nachgelagerte Steuern、Studienberatung。"),
            tf(lesen_pid, 9, "Nur die Höhe der Gebühr entscheidet über Chancengleichheit.", False, "nicht allein die Höhe … sondern ob Zugänge …。"),
            mc(lesen_pid, 10, "Was bleibt ohne verlässliche Unterstützung?", ["Automatische Fairness", "Chancengleichheit als Versprechen ohne ausreichende Praxis", "Kostenlose Wohnungen für alle", "Keine Debatte mehr"], 1, "Versprechen ohne ausreichende Praxis。"),
            mc(lesen_pid, 11, "Was bedeutet „nachgelagerte Einkommenssteuern“ hier ungefähr?", ["Steuern vor dem Studium", "Abgaben später je nach Einkommen der Absolventen", "Steuern nur für Schulen", "Keine Steuern je"], 1, "畢業後依所得課徵。"),
            mc(lesen_pid, 12, "Was soll laut Text frühzeitig sein?", ["Nur Prüfungen", "Beratung", "Nur Gebührenbescheid", "Nur Feiern"], 1, "Beratung frühzeitig。"),
        ],
        passage=passage,
        passage_zh=passage_zh,
    )

    audio = (
        "Moderator: Willkommen zur heutigen Bildungsrunde im Studio. Am Tisch sitzen "
        "Prof. Elena Hartmann von der Hochschule und Studierendensprecher Jonas Meier.\n"
        "Hartmann: Guten Tag.\n"
        "Meier: Hallo, schön hier zu sein.\n"
        "Moderator: Frau Professorin, warum halten Sie begrenzte Studiengebühren für vertretbar?\n"
        "Hartmann: Weil die Qualität der Lehre unter anhaltendem Finanzdruck leidet. "
        "Moderate Beiträge, kombiniert mit großzügigen Stipendien, könnten Labore, "
        "Tutorien und digitale Infrastruktur sichern – vorausgesetzt, die Mittel kommen "
        "tatsächlich in der Lehre an und versickern nicht in der Verwaltung.\n"
        "Meier: Genau da liegt mein Zweifel. Versprechen werden leicht gegeben, "
        "aber Studierende aus Nichtakademikerfamilien scheuen Schulden oft stärker als andere. "
        "Lieber die öffentliche Grundfinanzierung stärken und Beratung früh ausbauen, "
        "statt Hürden aufzubauen.\n"
        "Moderator: Herr Meier, wäre eine nachgelagerte Abgabe für Sie akzeptabler?\n"
        "Meier: Eher ja – wer später viel verdient, zahlt mehr zurück. "
        "Aber die Regeln müssen einfach, transparent und bundesweit vergleichbar sein. "
        "Sonst entsteht wieder neue Ungleichheit zwischen den Bundesländern.\n"
        "Hartmann: Da sind wir nah beieinander. Transparenz und frühe Studienberatung "
        "sind für mich ebenso wichtig wie die reine Finanzierungsfrage. "
        "Ohne Information helfen weder Gebühren noch Stipendien wirklich.\n"
        "Moderator: Ein Satz zum Schluss von beiden, bitte.\n"
        "Hartmann: Investiert in Menschen und gute Lehre, nicht nur in Gebäude.\n"
        "Meier: Und macht Zugänge sichtbar – sonst bleibt Chancengleichheit reine Theorie.\n"
        "Moderator: Herzlichen Dank für dieses klare Gespräch."
    )
    hoeren_pid = f"{pid}-hoeren"
    hoeren = section(
        "hoeren",
        "hoeren",
        "Hören",
        "聽力",
        "Hören Sie die Diskussionsrunde.",
        "聽討論後作答。",
        [
            mc(hoeren_pid, 1, "Wer diskutiert mit?", ["Nur der Moderator", "Hartmann und Meier", "Nur Studierende ohne Prof", "Nur Politiker"], 1, "Elena Hartmann und Jonas Meier。"),
            mc(hoeren_pid, 2, "Warum hält Hartmann Gebühren für vertretbar?", ["Weil Studium sinnlos ist", "Weil Lehrqualität unter Finanzdruck leidet", "Weil niemand Stipendien will", "Weil Labore überflüssig sind"], 1, "Qualität der Lehre unter Finanzdruck。"),
            mc(hoeren_pid, 3, "Womit sollen Beiträge kombiniert werden?", ["Mit Werbeverbot", "Mit großzügigen Stipendien", "Mit weniger Tutorien", "Mit höheren Mieten nur"], 1, "großzügigen Stipendien。"),
            mc(hoeren_pid, 4, "Welche Bedingung nennt Hartmann?", ["Mittel kommen in der Lehre an", "Nur Neubauten", "Keine Beratung", "Sofortige Schulden"], 0, "Mittel … in der Lehre an。"),
            mc(hoeren_pid, 5, "Was bezweifelt Meier?", ["Dass Versprechen eingehalten werden", "Dass es Universitäten gibt", "Dass man studieren darf", "Dass Beratung existiert"], 0, "Versprechen werden leicht gegeben。"),
            mc(hoeren_pid, 6, "Wen erwähnt Meier besonders?", ["Nur Professoren", "Studierende aus Nichtakademikerfamilien", "Nur Touristen", "Nur Kinder"], 1, "Nichtakademikerfamilien。"),
            mc(hoeren_pid, 7, "Was fordert Meier statt Gebührenfokus?", ["Grundfinanzierung und Beratung stärken", "Sofortige Schließung", "Nur Online-Studium", "Mehr Parkgebühren"], 0, "Grundfinanzierung stärken und Beratung ausbauen。"),
            mc(hoeren_pid, 8, "Wie steht Meier zu nachgelagerter Abgabe?", ["Komplett dagegen", "Eher ja, wenn Regeln transparent", "Nur bar zahlen", "Nur für Schulen"], 1, "Eher ja … transparent。"),
            mc(hoeren_pid, 9, "Worin sind sich beide einig?", ["Transparenz und frühe Beratung wichtig", "Keine Finanzierung nötig", "Nur Gebäude bauen", "Stipendien abschaffen"], 0, "Transparenz und frühe Beratung。"),
            mc(hoeren_pid, 10, "Was sagt Meier zum Schluss über Chancengleichheit?", ["Sie ist automatisch da", "Ohne sichtbare Zugänge bleibt sie Theorie", "Sie betrifft nur Sport", "Sie braucht keine Beratung"], 1, "sonst bleibt … Theorie。"),
        ],
        audio_text=audio,
    )

    bau_pid = f"{pid}-bausteine"
    bausteine = section(
        "bausteine",
        "bausteine",
        "Bausteine",
        "語法詞彙",
        "Konnektoren und Nominalstil.",
        "連接詞與名詞化。",
        [
            mc(bau_pid, 1, "Zwei Prinzipien ___ aufeinander.", ["prallen", "prallt", "geprallt sein falsch", "prall"], 0, "prallen aufeinander。"),
            gap(bau_pid, 2, "Gebühren könnten Erstakademiker ___.", "abschrecken", "abschrecken＝嚇跑。", accept=["abschrecken"]),
            mc(bau_pid, 3, "___ die Mittel in der Lehre ankommen, lohnen sich Beiträge.", ["Vorausgesetzt", "Bevor ohne Sinn", "Während nie", "Ohne dass immer"], 0, "vorausgesetzt＝前提是。"),
            gap(bau_pid, 4, "Stipendien gleichen Ungleichheit nur ___ aus.", "teilweise", "teilweise＝部分。"),
            mc(bau_pid, 5, "Expertinnen diskutieren sozial ___ Beiträge.", ["gestaffelte", "gestaffelten", "gestaffeltes", "Staffel"], 0, "gestaffelte Beiträge。"),
            gap(bau_pid, 6, "Entscheidend ist, ___ Zugänge transparent sind.", "ob", "ob＝是否。"),
            mc(bau_pid, 7, "Andernfalls ___ Chancengleichheit Theorie.", ["bleibt", "bleiben", "blieb", "bleibst"], 0, "bleibt。"),
            gap(bau_pid, 8, "Man sollte in Menschen ___, nicht nur in Gebäude.", "investieren", "investieren in。"),
            mc(bau_pid, 9, "Die Angst ___ Verschuldung verzerrt Entscheidungen.", ["vor", "für", "um", "gegen"], 0, "Angst vor。"),
            gap(bau_pid, 10, "Nachgelagerte Abgaben hängen vom ___ ab.", "Einkommen", "Einkommen。", accept=["Verdienst"]),
            mc(bau_pid, 11, "___ Bürokratie wirkt weiterhin, greifen Stipendien nicht voll.", ["Weil", "Als", "Seit wann falsch", "Damit"], 0, "Weil。"),
            gap(bau_pid, 12, "Macht Zugänge ___, sonst bleibt Gleichheit Theorie.", "sichtbar", "sichtbar＝看得見。"),
        ],
    )

    schreib_pid = f"{pid}-schreiben"
    schreiben = section(
        "schreiben",
        "schreiben",
        "Schreiben",
        "寫作",
        "Schreiben Sie eine formale Stellungnahme (ca. 150–180 Wörter).",
        "撰寫正式立場文約 150–180 字。",
        [
            schreiben_item(
                schreib_pid,
                1,
                "Thema: Sollen Universitäten Studiengebühren erheben? "
                "Struktur: Einleitung mit These – Argumente – Gegenposition – "
                "Kompromiss/Empfehlung – Schluss.",
                "大學該不該收學費？含命題、論點、反論、折衷建議與結論。",
                150,
                "Die Frage, ob Universitäten Studiengebühren erheben sollten, "
                "berührt Gerechtigkeit und Qualität zugleich. Meiner Ansicht nach "
                "sind hohe Gebühren riskant, weil sie soziale Selektion verstärken. "
                "Zugleich braucht gute Lehre verlässliche Mittel. Ein Gegenargument "
                "lautet, Studierende profitierten später finanziell und sollten zahlen – "
                "doch ohne Beratung und Stipendien trifft das vor allem Unsichere. "
                "Als Kompromiss empfehle ich nachgelagerte einkommensabhängige Beiträge "
                "sowie transparente Stipendien und frühe Studienberatung. "
                "So bliebe Bildung zugänglich, während Absolventinnen und Absolventen "
                "mit hohem Einkommen einen fairen Anteil zurückgeben.",
                [
                    "正式語體與清楚命題",
                    "正反論兼具",
                    "提出具體折衷",
                    "連接手段豐富",
                    "約 150 字以上",
                ],
            )
        ],
    )

    sprech_pid = f"{pid}-sprechen"
    sprechen = section(
        "sprechen",
        "sprechen",
        "Sprechen",
        "口說",
        "Argumentieren Sie überzeugend.",
        "有說服力地論證。",
        [
            sprechen_item(
                sprech_pid,
                1,
                "Nehmen Sie Stellung: Bildung als öffentliches Gut – stimmen Sie zu?",
                "立場：教育是公共財——你同意嗎？",
                ["These", "Beispiel", "Einwand", "Schluss"],
                "Ja, Bildung sollte ein öffentliches Gut sein, weil Chancen nicht vom Geldbeutel "
                "der Eltern abhängen dürfen. Zum Beispiel brauchen Erstakademiker verlässliche "
                "Unterstützung. Ein Einwand ist die Finanzierung – dafür braucht der Staat "
                "klare Prioritäten. Am Ende zählt Zugänglichkeit mehr als Symbolpolitik.",
            ),
            sprechen_item(
                sprech_pid,
                2,
                "Wie sollten Stipendien fairer gestaltet werden?",
                "獎學金應如何設計得更公平？",
                ["Informationszugang", "Bürokratie", "Höhe / Dauer"],
                "Stipendien müssen leicht auffindbar und einfach beantragbar sein. "
                "Weniger Bürokratie und frühe Beratung in der Schule helfen. "
                "Die Förderung sollte lange genug dauern, damit Planungssicherheit entsteht.",
            ),
        ],
    )

    return paper(
        "B2",
        2,
        "Goethe-Format B2 · Modellsatz 2",
        "德檢模擬 B2 · 模考二（教育／學費）",
        110,
        [lesen, hoeren, bausteine, schreiben, sprechen],
    )


def build() -> dict[str, Any]:
    papers = [
        a1_m1(),
        a1_m2(),
        a2_m1(),
        a2_m2(),
        b1_m1(),
        b1_m2(),
        b2_m1(),
        b2_m2(),
    ]
    assert len(papers) == 8, f"expected 8 papers, got {len(papers)}"
    ids = [p["id"] for p in papers]
    assert ids == ["a1-m1", "a1-m2", "a2-m1", "a2-m2", "b1-m1", "b1-m2", "b2-m1", "b2-m2"]
    for p in papers:
        kinds = [s["kind"] for s in p["sections"]]
        assert kinds == ["lesen", "hoeren", "bausteine", "schreiben", "sprechen"], kinds
        for sec in p["sections"]:
            if sec["kind"] == "hoeren":
                assert sec.get("audioText"), f"{p['id']} hoeren missing audioText"
                words = len(sec["audioText"].split())
                if p["level"] == "A1":
                    assert 80 <= words <= 140, f"{p['id']} A1 audio words={words}"
                elif p["level"] == "B2":
                    assert 180 <= words <= 320, f"{p['id']} B2 audio words={words}"
        n = scored_count(p)
        lvl = p["level"]
        if lvl == "A1":
            assert 22 <= n <= 30, f"{p['id']} scored={n}"
        elif lvl == "A2":
            assert n == 28, f"{p['id']} scored={n}"
        elif lvl == "B1":
            assert 28 <= n <= 32, f"{p['id']} scored={n}"
        else:
            assert 28 <= n <= 34, f"{p['id']} scored={n}"
    return {
        "note": NOTE,
        "levels": ["A1", "A2", "B1", "B2"],
        "papers": papers,
    }


def main() -> None:
    data = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUT}")
    print(f"Papers: {len(data['papers'])}")
    for p in data["papers"]:
        by_kind: dict[str, int] = {}
        scored = 0
        for sec in p["sections"]:
            for it in sec["items"]:
                by_kind[it["type"]] = by_kind.get(it["type"], 0) + 1
                if it["type"] in ("mc", "tf", "gap"):
                    scored += 1
        print(
            f"  {p['id']} ({p['level']} R{p['round']}): "
            f"scored={scored}  items={by_kind}"
        )


if __name__ == "__main__":
    main()
