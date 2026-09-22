#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Append 20 NEW reading items per level (練習/A1/A2/B1/B2) → 100 total.

Does NOT remove or rewrite existing items. IDs continue from 51–70 per level.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "src" / "data" / "reading.json"

NOTE = (
    "對齊德檢（Goethe／ÖSD）閱讀難度：練習＝熱身短文；A1／A2／B1 循序銜接；"
    "B2＝考場長度論述／正式郵件／公告與訪談，含反論、名詞化與複合句。"
    "各級各 70 篇（練習＋A1–B2），共 350 篇分級閱讀。"
)


def item(id, level, kind, topic, title, title_zh, text, text_zh, notes, patterns, tips, focus):
    return {
        "id": id,
        "level": level,
        "kind": kind,
        "topic": topic,
        "title": title,
        "titleZh": title_zh,
        "text": text.strip(),
        "textZh": text_zh.strip(),
        "notes": notes,
        "patterns": patterns,
        "tips": tips,
        "focus": focus,
    }


def n(span, zh, tip=""):
    d = {"span": span, "zh": zh}
    if tip:
        d["tip"] = tip
    return d


def p(pattern, zh, example):
    return {"pattern": pattern, "zh": zh, "example": example}


# ═══════════════════════════════════════════════════════════════════
# 練習 51–70  (~70–130 chars)
# ═══════════════════════════════════════════════════════════════════
UEBUNG = [
    item(
        "uebung-51", "練習", "card", "顏色",
        "Meine Lieblingsfarbe", "我最愛的顏色",
        "Hallo!\nIch heiße Mina.\nMeine Lieblingsfarbe ist Blau.\nUnd deine?",
        "哈囉！\n我叫 Mina。\n我最愛的顏色是藍色。\n你的呢？",
        [n("heiße", "名叫", "heißen：名字是……"), n("Lieblingsfarbe", "最愛的顏色"), n("Blau", "藍色"), n("Und deine?", "你的呢？", "省略 Farbe。")],
        [p("Meine Lieblings… ist …", "說喜好", "Meine Lieblingsspeise ist Pizza."), p("Und deine?", "反問對方", "Und deins?")],
        ["把顏色換成 Rot、Grün 再說一次。", "練習：Lieblings- + 名詞。"],
        ["顏色", "喜好"],
    ),
    item(
        "uebung-52", "練習", "dialogue", "數字",
        "Wie alt bist du?", "你幾歲？",
        "Leo: Wie alt bist du?\nMia: Ich bin 19.\nLeo: Ich bin 21.\nMia: Cool!",
        "Leo：你幾歲？\nMia：我 19 歲。\nLeo：我 21 歲。\nMia：酷！",
        [n("Wie alt", "幾歲", "alt＝年齡老／歲。"), n("Ich bin + 數字", "我……歲"), n("Cool", "酷／真棒")],
        [p("Wie alt bist du?", "問年齡", "Wie alt ist er?"), p("Ich bin + Zahl", "回答年齡", "Ich bin zwanzig.")],
        ["數字 1–30 先練熟再談年齡。", "對正式場合用 Sie：Wie alt sind Sie?"],
        ["數字", "年齡"],
    ),
    item(
        "uebung-53", "練習", "sign", "開門時間",
        "Öffnungszeiten", "營業時間",
        "Bibliothek\nMo–Fr: 9–18 Uhr\nSa: 10–14 Uhr\nSo: geschlossen",
        "圖書館\n週一至五：9–18 點\n週六：10–14 點\n週日：休息",
        [n("Öffnungszeiten", "營業／開放時間"), n("Mo–Fr", "週一到週五"), n("geschlossen", "關閉／休息"), n("Bibliothek", "圖書館")],
        [p("Mo–Fr: … Uhr", "平日時間", "Di–Do: 8–16 Uhr"), p("…: geschlossen", "休息公告", "Heute geschlossen")],
        ["告示常縮寫星期：Mo Di Mi Do Fr Sa So。", "geschlossen＝不營業。"],
        ["告示", "時間"],
    ),
    item(
        "uebung-54", "練習", "message", "遲到",
        "Ich komme später", "我會晚點到",
        "Hi Tom,\nich komme 10 Minuten später.\nSorry!\nBis gleich\nNora",
        "嗨 Tom，\n我會晚 10 分鐘到。\n抱歉！\n待會見\nNora",
        [n("komme … später", "晚點到"), n("Minuten", "分鐘"), n("Sorry", "抱歉", "口語；正式用 Entschuldigung。"), n("Bis gleich", "待會見")],
        [p("Ich komme + 時間 + später", "說會晚到", "Ich komme eine Stunde später."), p("Bis gleich", "很快再見", "Bis später!")],
        ["簡訊：原因可短、先道歉。", "數字＋Minuten 很常用。"],
        ["時間", "道歉"],
    ),
    item(
        "uebung-55", "練習", "card", "寵物",
        "Mein Hund", "我的狗",
        "Das ist mein Hund.\nEr heißt Bruno.\nEr ist klein und braun.\nEr mag Bälle.",
        "這是我的狗。\n他叫 Bruno。\n他又小又棕色。\n他喜歡球。",
        [n("Hund", "狗"), n("Er heißt", "他叫"), n("klein und braun", "小而棕色"), n("mag", "喜歡", "mögen 現在時。")],
        [p("Das ist mein / meine + 名詞", "介紹所有物", "Das ist meine Katze."), p("Er mag + 複數／第四格", "說喜好", "Er mag Äpfel.")],
        ["動物用 er／sie，看名詞性別。", "換：Katze、Vogel。"],
        ["寵物", "形容詞"],
    ),
    item(
        "uebung-56", "練習", "dialogue", "飲料",
        "Was trinkst du?", "你喝什麼？",
        "A: Was trinkst du?\nB: Wasser, bitte.\nA: Mit Eis?\nB: Nein, danke.",
        "A：你喝什麼？\nB：水，麻煩。\nA：要加冰嗎？\nB：不用，謝謝。",
        [n("Was trinkst du?", "你喝什麼？"), n("Wasser", "水"), n("Mit Eis?", "加冰嗎？"), n("Nein, danke", "不用，謝謝")],
        [p("Was trinkst / möchten Sie?", "點飲料", "Ich trinke Tee."), p("Nein, danke.／Ja, bitte.", "禮貌回應", "Ja, bitte.")],
        ["點餐短句先背熟。", "bitte／danke 成對練。"],
        ["飲料", "點餐"],
    ),
    item(
        "uebung-57", "練習", "sign", "洗手間",
        "WC", "洗手間指示",
        "WC → links\nDamen / Herren\nBitte sauber halten!",
        "洗手間 → 左邊\n女廁／男廁\n請保持清潔！",
        [n("links", "左邊"), n("Damen", "女廁／女士"), n("Herren", "男廁／男士"), n("sauber halten", "保持清潔")],
        [p("→ links / rechts", "方向指示", "Ausgang → rechts"), p("Bitte + 動詞原形", "簡短要求", "Bitte warten!")],
        ["公共標誌多是短命令句。", "halten＝保持。"],
        ["方向", "標誌"],
    ),
    item(
        "uebung-58", "練習", "message", "祝福",
        "Alles Gute!", "祝一切順利",
        "Liebe Sara,\nalles Gute zur Prüfung!\nDu schaffst das.\nKüsse\nBen",
        "親愛的 Sara，\n考試一切順利！\n你做得到。\n親親\nBen",
        [n("Alles Gute", "一切順利／祝福"), n("zur Prüfung", "祝考試", "zu + 第三格場合。"), n("Du schaffst das", "你做得到"), n("Küsse", "親吻／親親")],
        [p("Alles Gute zu + 場合", "祝福", "Alles Gute zum Geburtstag!"), p("Du schaffst das.", "加油鼓勵", "Wir schaffen das.")],
        ["祝福短訊：場合＋鼓勵。", "正式可寫 Viel Erfolg!"],
        ["祝福", "考試"],
    ),
    item(
        "uebung-59", "練習", "card", "星期",
        "Mein Wochenplan", "我的一週計畫",
        "Montag: Sport\nDienstag: Deutsch\nFreitag: Kino\nSonntag: Pause",
        "星期一：運動\n星期二：德文\n星期五：看電影\n星期日：休息",
        [n("Montag", "星期一"), n("Sport", "運動"), n("Kino", "電影院／看電影"), n("Pause", "休息")],
        [p("星期: + 活動", "簡易行程", "Mittwoch: Arbeit"), p("…: Pause", "排休息", "Samstag: Pause")],
        ["先背七個星期名稱。", "可改成你的真實行程。"],
        ["星期", "行程"],
    ),
    item(
        "uebung-60", "練習", "dialogue", "名字拼寫",
        "Wie schreibt man das?", "怎麼拼？",
        "A: Wie heißt du?\nB: Yusuf.\nA: Wie schreibt man das?\nB: Y-U-S-U-F.",
        "A：你叫什麼名字？\nB：Yusuf。\nA：怎麼拼？\nB：Y-U-S-U-F。",
        [n("Wie heißt du?", "你叫什麼？"), n("Wie schreibt man das?", "怎麼拼寫？"), n("schreibt", "書寫／拼", "schreiben。")],
        [p("Wie schreibt man …?", "問拼法", "Wie schreibt man Ihren Namen?"), p("字母逐個念", "拼名字", "A-N-N-A")],
        ["德文字母表先練。", "電話裡常要拼名字。"],
        ["字母", "名字"],
    ),
    item(
        "uebung-61", "練習", "sign", "禁止吸菸",
        "Rauchen verboten", "禁止吸菸",
        "Rauchen verboten!\nAuch E-Zigaretten.\nVielen Dank.",
        "禁止吸菸！\n電子菸也不行。\n謝謝配合。",
        [n("Rauchen verboten", "禁止吸菸"), n("Auch", "也"), n("E-Zigaretten", "電子菸"), n("Vielen Dank", "非常感謝")],
        [p("… verboten", "禁止標誌", "Parken verboten"), p("Auch + 名詞", "範圍擴充", "Auch Hunde")],
        ["verboten＝禁止，很常見。", "標誌語氣短而硬。"],
        ["禁止", "標誌"],
    ),
    item(
        "uebung-62", "練習", "message", "到站",
        "Ich bin da", "我到了",
        "Hi!\nIch bin am Bahnhof.\nWo bist du?\nRuf mich an!",
        "嗨！\n我在火車站。\n你在哪？\n打電話給我！",
        [n("am Bahnhof", "在火車站", "an dem → am。"), n("Wo bist du?", "你在哪？"), n("Ruf mich an", "打電話給我", "anrufen 可分動詞。")],
        [p("Ich bin am / in + 地點", "報位置", "Ich bin im Café."), p("Ruf mich an!", "要求來電", "Schreib mir!")],
        ["會合簡訊：位置＋問對方。", "可分動詞：anrufen → Ruf … an。"],
        ["地點", "會合"],
    ),
    item(
        "uebung-63", "練習", "card", "職業",
        "Ich bin Koch", "我是廚師",
        "Ich bin Koch.\nIch arbeite in einem Restaurant.\nIch mag meinen Job.",
        "我是廚師。\n我在一家餐廳工作。\n我喜歡我的工作。",
        [n("Koch", "廚師", "陰性 Köchin。"), n("arbeite in", "在……工作"), n("Restaurant", "餐廳"), n("Job", "工作", "口語；正式 Beruf／Arbeit。")],
        [p("Ich bin + 職業", "說職業", "Ich bin Lehrerin."), p("Ich arbeite in + 第三格", "工作地點", "Ich arbeite in einer Firma.")],
        ["職業名詞注意陰陽。", "mag meinen Job：第四格。"],
        ["職業", "sein"],
    ),
    item(
        "uebung-64", "練習", "dialogue", "價錢",
        "Was kostet das?", "這個多少錢？",
        "Kundin: Was kostet das?\nVerkäufer: 4 Euro 50.\nKundin: Okay, ich nehme es.",
        "顧客：這個多少錢？\n店員：4 歐元 50。\n顧客：好，我買了。",
        [n("Was kostet das?", "多少錢？"), n("Euro", "歐元"), n("ich nehme es", "我買／要這個", "nehmen＝拿／選購。")],
        [p("Was kostet …?", "問價錢", "Was kostet die Fahrkarte?"), p("Ich nehme …", "決定購買", "Ich nehme das Brot.")],
        ["價錢：Zahl + Euro。", "購物三句就夠用。"],
        ["購物", "價錢"],
    ),
    item(
        "uebung-65", "練習", "message", "照片",
        "Schönes Foto!", "好美的照片！",
        "Wow, schönes Foto!\nWo war das?\nSieht toll aus.\n❤️ Lea",
        "哇，好美的照片！\n那是在哪裡？\n看起來很棒。\n❤️ Lea",
        [n("schönes Foto", "美麗的照片", "schön 中性：schönes。"), n("Wo war das?", "那是在哪？"), n("Sieht … aus", "看起來……", "aussehen。"), n("toll", "棒／了不起")],
        [p("schönes / tolles + 名詞", "稱讚", "Tolles Bild!"), p("Sieht … aus", "外觀評價", "Es sieht gut aus.")],
        ["社群短評：稱讚＋問地點。", "aussehen：看著像……。"],
        ["稱讚", "社群"],
    ),
    item(
        "uebung-66", "練習", "sign", "電梯",
        "Aufzug außer Betrieb", "電梯故障",
        "Aufzug außer Betrieb\nBitte Treppe benutzen.\nEntschuldigung!",
        "電梯暫停使用\n請走樓梯。\n抱歉！",
        [n("Aufzug", "電梯"), n("außer Betrieb", "停止運作／故障"), n("Treppe", "樓梯"), n("benutzen", "使用")],
        [p("… außer Betrieb", "故障告示", "Automat außer Betrieb"), p("Bitte + 名詞 + benutzen", "改用建議", "Bitte Ausgang B benutzen")],
        ["公共場所常見 außer Betrieb。", "Entschuldigung 緩和語氣。"],
        ["故障", "告示"],
    ),
    item(
        "uebung-67", "練習", "dialogue", "感覺",
        "Mir ist kalt", "我覺得冷",
        "A: Alles okay?\nB: Mir ist kalt.\nA: Hier, eine Jacke.\nB: Danke!",
        "A：還好嗎？\nB：我覺得冷。\nA：給，一件外套。\nB：謝謝！",
        [n("Alles okay?", "還好嗎？"), n("Mir ist kalt", "我覺得冷", "mir＝第三格。"), n("Jacke", "外套"), n("Hier", "給／這裡")],
        [p("Mir ist + 形容詞", "身體感覺", "Mir ist warm.／Mir ist schlecht."), p("Hier, + 名詞", "遞東西", "Hier, dein Tee.")],
        ["感覺常用第三格：mir／dir。", "不是 Ich bin kalt（那是「我這人冷漠」）。"],
        ["感覺", "第三格"],
    ),
    item(
        "uebung-68", "練習", "card", "國家語言",
        "Sprachen", "語言",
        "Ich komme aus Japan.\nIch spreche Japanisch.\nJetzt lerne ich Deutsch.",
        "我來自日本。\n我說日語。\n現在我在學德文。",
        [n("komme aus", "來自"), n("spreche", "說（語言）"), n("Japanisch", "日語"), n("Jetzt", "現在")],
        [p("Ich spreche + 語言", "語言能力", "Ich spreche Englisch."), p("Jetzt lerne ich …", "目前學習", "Jetzt lerne ich Kochen.")],
        ["國家／語言詞常相似但不同：Japan／Japanisch。", "換你的母語練習。"],
        ["語言", "出身"],
    ),
    item(
        "uebung-69", "練習", "message", "生日",
        "Herzlichen Glückwunsch", "生日快樂",
        "Lieber Omar,\nherzlichen Glückwunsch zum Geburtstag!\nFeier schön!\nDeine Lara",
        "親愛的 Omar，\n生日快樂！\n好好慶祝！\n你的 Lara",
        [n("herzlichen Glückwunsch", "誠摯祝賀"), n("zum Geburtstag", "生日"), n("Feier schön", "好好慶祝"), n("Deine", "你的（女性署名）")],
        [p("Herzlichen Glückwunsch zu …", "祝賀公式", "Herzlichen Glückwunsch zur Hochzeit!"), p("Feier schön!", "祝福玩得開心", "Genieß den Tag!")],
        ["生日訊息公式很固定。", "署名：Dein／Deine + 名字。"],
        ["生日", "祝賀"],
    ),
    item(
        "uebung-70", "練習", "dialogue", "再見",
        "Tschüss und bis morgen", "掰掰，明天見",
        "A: Ich muss gehen.\nB: Okay. Tschüss!\nA: Bis morgen!\nB: Bis dann!",
        "A：我得走了。\nB：好。掰掰！\nA：明天見！\nB：到時見！",
        [n("muss gehen", "必須離開", "müssen + 原形。"), n("Tschüss", "掰／再見", "口語。"), n("Bis morgen", "明天見"), n("Bis dann", "到時見")],
        [p("Ich muss + 原形", "說必須", "Ich muss arbeiten."), p("Bis + 時間", "約再見", "Bis Freitag!")],
        ["道別可疊：Tschüss + Bis …。", "正式用 Auf Wiedersehen。"],
        ["道別", "müssen"],
    ),
]


# ═══════════════════════════════════════════════════════════════════
# A1 51–70  (~150–250 chars)
# ═══════════════════════════════════════════════════════════════════
A1 = [
    item(
        "a1-51", "A1", "email", "鄰居",
        "Paket für Nachbarn", "幫鄰居收包裹",
        """Betreff: Paket

Hallo Frau Berg,

heute kam ein Paket für Sie.
Ich habe es angenommen.
Sie können es heute Abend bei mir abholen.

Viele Grüße
Kenji""",
        """主旨：包裹

Berg 女士您好，

今天有您的包裹送來。
我代收了。
您今晚可以來我家拿。

問候
Kenji""",
        [n("Paket", "包裹"), n("angenommen", "代收／收下", "annehmen。"), n("abholen", "來取"), n("heute Abend", "今晚"), n("bei mir", "在我家")],
        [p("Ich habe es angenommen.", "說明代收", "Können Sie das Paket annehmen?"), p("Sie können … abholen", "說明可取件", "Abholen ab 18 Uhr.")],
        ["鄰居郵件：事件＋行動＋取件時間。", "Viele Grüße 適合半正式。"],
        ["郵件", "鄰居"],
    ),
    item(
        "a1-52", "A1", "dialogue", "藥局",
        "In der Apotheke", "在藥局",
        """Apothekerin: Guten Tag. Was kann ich für Sie tun?
Kunde: Ich habe Kopfschmerzen. Haben Sie etwas dagegen?
Apothekerin: Ja, diese Tabletten. Dreimal täglich.
Kunde: Danke. Was kostet das?
Apothekerin: 6 Euro 90.""",
        """藥師：您好。有什麼可以幫您？
顧客：我頭痛。有什麼藥嗎？
藥師：有，這些錠劑。一天三次。
顧客：謝謝。多少錢？
藥師：6 歐元 90。""",
        [n("Apotheke", "藥局"), n("Kopfschmerzen", "頭痛", "複數。"), n("dagegen", "針對這個"), n("Tabletten", "錠劑"), n("Dreimal täglich", "一天三次")],
        [p("Haben Sie etwas gegen …?", "問有無對症藥", "Haben Sie etwas gegen Husten?"), p("…-mal täglich", "服藥頻率", "Zweimal täglich")],
        ["藥局對話：症狀→建議→劑量→價錢。", "täglich＝每天。"],
        ["健康", "購物"],
    ),
    item(
        "a1-53", "A1", "story", "週末計畫",
        "Am Wochenende", "這個週末",
        """Am Samstag gehe ich mit Freunden ins Museum.
Danach trinken wir Kaffee.
Am Sonntag bleibe ich zu Hause und lerne Deutsch.
Abends schaue ich einen Film.
Ich freue mich auf das Wochenende!""",
        """星期六我和朋友去博物館。
之後我們喝咖啡。
星期天我待在家學德文。
晚上我看電影。
我很期待這個週末！""",
        [n("Am Samstag", "在星期六", "am + 星期。"), n("ins Museum", "去博物館", "in das。"), n("Danach", "之後"), n("bleibe … zu Hause", "待在家"), n("Ich freue mich auf", "我期待……")],
        [p("Am + 星期 + gehe ich …", "週末行程", "Am Freitag gehe ich tanzen."), p("Ich freue mich auf + 第四格", "期待", "Ich freue mich auf die Reise.")],
        ["用 Am／Danach／Abends 串時間。", "freue mich auf＝期待尚未發生的事。"],
        ["時間", "計畫"],
    ),
    item(
        "a1-54", "A1", "notice", "健身房",
        "Aushang Fitnessstudio", "健身房公告",
        """Liebe Mitglieder,
ab Montag ist die Sauna wegen Reparatur geschlossen.
Das Fitnessstudio bleibt geöffnet.
Bitte Handtücher mitbringen.
Danke für Ihr Verständnis.
Die Leitung""",
        """親愛的會員們，
自星期一起，三溫暖因維修關閉。
健身房照常開放。
請自備毛巾。
感謝理解。
管理單位""",
        [n("Mitglieder", "會員"), n("wegen Reparatur", "因維修", "wegen + 第二格。"), n("bleibt geöffnet", "維持開放"), n("Handtücher", "毛巾"), n("Verständnis", "理解")],
        [p("wegen + 第二格", "說明原因", "wegen Bauarbeiten"), p("bleibt geöffnet / geschlossen", "狀態說明", "Die Bibliothek bleibt geöffnet.")],
        ["公告：關什麼／開什麼／請自備。", "Danke für Ihr Verständnis 很常用。"],
        ["公告", "設施"],
    ),
    item(
        "a1-55", "A1", "dialogue", "郵局",
        "Paket schicken", "寄包裹",
        """Mitarbeiter: Wohin soll das Paket?
Kundin: Nach Österreich.
Mitarbeiter: Luft oder Landweg?
Kundin: Landweg, bitte. Wie lange dauert das?
Mitarbeiter: Etwa vier Tage.
Kundin: Gut, dann so.""",
        """職員：包裹要寄去哪？
顧客：奧地利。
職員：空運還是陸運？
顧客：陸運。要多久？
職員：大約四天。
顧客：好，那就這樣。""",
        [n("Wohin", "去哪裡"), n("Nach Österreich", "寄到奧地利", "國家多用 nach。"), n("Landweg", "陸運"), n("Wie lange dauert", "要多久"), n("Etwa", "大約")],
        [p("Wohin soll …?", "問目的地", "Wohin soll die Karte?"), p("Wie lange dauert das?", "問耗時", "Es dauert zwei Stunden.")],
        ["郵局：目的地→方式→時間→決定。", "Luft＝空運。"],
        ["郵局", "旅行"],
    ),
    item(
        "a1-56", "A1", "email", "課程",
        "Frage zum Deutschkurs", "德文課詢問",
        """Betreff: Kurs am Abend

Guten Tag,

ich möchte einen Abendkurs besuchen.
Gibt es noch freie Plätze im A1-Kurs?
Wann beginnt der Kurs?

Mit freundlichen Grüßen
Yuna Park""",
        """主旨：晚間課程

您好，

我想上晚間課。
A1 班還有空位嗎？
課程何時開始？

此致問候
Yuna Park""",
        [n("Abendkurs", "晚間課程"), n("besuchen", "參加／上（課）"), n("freie Plätze", "空位"), n("Wann beginnt", "何時開始"), n("Mit freundlichen Grüßen", "正式結尾")],
        [p("Gibt es noch …?", "問是否還有", "Gibt es noch Tickets?"), p("Wann beginnt …?", "問開始時間", "Wann beginnt der Film?")],
        ["詢問郵件：意圖＋問題＋正式結尾。", "freie Plätze＝名額。"],
        ["學校", "郵件"],
    ),
    item(
        "a1-57", "A1", "story", "搬家日",
        "Umzug", "搬家",
        """Heute ziehe ich um.
Freunde helfen mir mit den Kartons.
Der Aufzug ist klein, deshalb tragen wir viel über die Treppe.
Am Abend sind wir müde, aber glücklich.
Die neue Wohnung ist hell und ruhig.""",
        """今天我搬家。
朋友幫我搬紙箱。
電梯很小，所以我們很多東西走樓梯搬。
晚上我們很累，但很開心。
新公寓明亮又安靜。""",
        [n("ziehe … um", "搬家", "umziehen。"), n("Kartons", "紙箱"), n("deshalb", "所以"), n("tragen", "搬／提"), n("hell und ruhig", "明亮又安靜")],
        [p("Deshalb + 句子", "說明結果", "Es regnet, deshalb bleibe ich zu Hause."), p("müde, aber glücklich", "對比形容", "teuer, aber gut")],
        ["umziehen：注意字首分離。", "用 deshalb 連接因果。"],
        ["搬家", "日常"],
    ),
    item(
        "a1-58", "A1", "notice", "洗衣機",
        "Waschküche", "洗衣房規則",
        """Waschküche – Regeln
1. Bitte Termin im Kalender eintragen.
2. Nach dem Waschen Maschine säubern.
3. Wäsche am gleichen Tag abholen.
4. Bei Problemen Hausmeister anrufen.""",
        """洗衣房－規則
1. 請在日曆登記時段。
2. 洗完請清理洗衣機。
3. 衣物須當日取走。
4. 有問題請打給管理員。""",
        [n("Waschküche", "洗衣房"), n("eintragen", "登記／填寫"), n("säubern", "清理"), n("am gleichen Tag", "同一天"), n("Hausmeister", "管理員")],
        [p("Bitte + 動詞原形", "規則語氣", "Bitte Tür schließen."), p("Nach dem + 名詞化", "之後", "Nach dem Kochen spülen.")],
        ["規則公告常編號。", "am gleichen Tag＝當天。"],
        ["住房", "規則"],
    ),
    item(
        "a1-59", "A1", "dialogue", "火車站",
        "Verspätung", "列車延誤",
        """Ansager: Der Zug nach Hamburg hat 20 Minuten Verspätung.
Fahrgast: Oh nein. Kommt er auf Gleis 3?
Ansager: Ja, Gleis 3.
Fahrgast: Danke für die Info.
Ansager: Bitte schön.""",
        """廣播：開往漢堡的列車延誤 20 分鐘。
旅客：喔不。還是 3 月台嗎？
廣播：是，3 月台。
旅客：謝謝告知。
廣播：不客氣。""",
        [n("Verspätung", "延誤"), n("Zug nach …", "開往……的列車"), n("Gleis", "月台／股道"), n("Info", "資訊", "口語＝Information。"), n("Bitte schön", "不客氣")],
        [p("hat … Verspätung", "說延誤", "Der Bus hat Verspätung."), p("auf Gleis + 數字", "月台", "Der Zug kommt auf Gleis 7.")],
        ["交通：目的地＋延誤＋月台。", "Verspätung 是名詞。"],
        ["交通", "旅行"],
    ),
    item(
        "a1-60", "A1", "email", "請假一天",
        "Einen Tag frei", "請一天假",
        """Betreff: Freier Tag am Donnerstag

Liebe Frau Klein,

kann ich am Donnerstag frei nehmen?
Ich muss zum Amt.
Am Freitag bin ich wieder da.

Liebe Grüße
Samir""",
        """主旨：星期四請假

Klein 女士您好，

星期四我可以請假嗎？
我得去辦事處。
星期五我會回來。

問候
Samir""",
        [n("frei nehmen", "請假"), n("zum Amt", "去辦事處", "Amt＝公家機關。"), n("wieder da", "又在（回來）"), n("Am Freitag", "星期五")],
        [p("Kann ich … frei nehmen?", "請求請假", "Darf ich morgen frei nehmen?"), p("Ich muss zu + 第三格", "必須去某處", "Ich muss zum Arzt.")],
        ["請假：日期＋原因＋何時回來。", "Liebe Grüße 比 Mit freundlichen Grüßen 稍軟。"],
        ["工作", "請假"],
    ),
    item(
        "a1-61", "A1", "story", "市場購物",
        "Auf dem Markt", "在市集",
        """Samstagmorgen gehe ich auf den Markt.
Ich kaufe Äpfel, Käse und Brot.
Die Verkäuferin ist freundlich und gibt mir ein Rezept.
Zu Hause koche ich eine Suppe.
Sie schmeckt sehr gut.""",
        """星期六早上我去市集。
我買蘋果、起司和麵包。
女店員很親切，還給我一份食譜。
回家後我煮湯。
湯很好喝。""",
        [n("auf den Markt", "去市集", "auf + 第四格＝方向。"), n("kaufe", "購買"), n("Rezept", "食譜／處方"), n("Zu Hause", "在家"), n("schmeckt", "味道……")],
        [p("Ich kaufe A, B und C.", "列購物清單", "Ich kaufe Milch und Eier."), p("Es schmeckt gut.", "評價味道", "Die Suppe schmeckt salzig.")],
        ["市集故事：去→買→做→評價。", "Rezept 也有「藥方」意思。"],
        ["購物", "食物"],
    ),
    item(
        "a1-62", "A1", "notice", "宿舍廚房",
        "Küchenplan Wohnheim", "宿舍廚房輪值",
        """Küchenplan – Woche 12
Mo/Di: Zimmer 3
Mi/Do: Zimmer 5
Fr/Sa: Zimmer 1
Bitte Spüle und Herd reinigen.
Müll am Sonntag rausbringen.""",
        """廚房輪值－第 12 週
一／二：3 號房
三／四：5 號房
五／六：1 號房
請清理水槽與爐具。
星期日請倒垃圾。""",
        [n("Küchenplan", "廚房輪值表"), n("Spüle", "水槽"), n("Herd", "爐具"), n("reinigen", "清潔"), n("Müll … rausbringen", "倒垃圾")],
        [p("Bitte … reinigen", "清潔要求", "Bitte Kühlschrank reinigen."), p("Müll rausbringen", "倒垃圾", "Bitte Glas und Papier trennen.")],
        ["輪值表：誰＋哪天＋清潔項目。", "rausbringen＝拿出去。"],
        ["宿舍", "家務"],
    ),
    item(
        "a1-63", "A1", "dialogue", "租腳踏車",
        "Fahrrad leihen", "租腳踏車",
        """Angestellte: Möchten Sie ein Rad für einen Tag?
Gast: Ja. Was kostet das?
Angestellte: 12 Euro, Helm inklusive.
Gast: Brauche ich einen Ausweis?
Angestellte: Ja, bitte. Hier ist der Schlüssel.""",
        """職員：您要租一天的車嗎？
客人：好。多少錢？
職員：12 歐元，含安全帽。
客人：需要證件嗎？
職員：要的。鑰匙在這裡。""",
        [n("Rad leihen", "租車", "leihen＝借入。"), n("für einen Tag", "租一天"), n("inklusive", "包含"), n("Ausweis", "證件"), n("Schlüssel", "鑰匙")],
        [p("für + 時間", "租用時長", "für zwei Stunden"), p("… inklusive", "費用含……", "Frühstück inklusive")],
        ["租借：時長→價錢→文件→取物。", "leihen／mieten 都可表租。"],
        ["交通", "服務"],
    ),
    item(
        "a1-64", "A1", "email", "活動報名",
        "Anmeldung Stadtführung", "報名城市導覽",
        """Betreff: Anmeldung Stadtführung

Hallo,

ich möchte mich für die Stadtführung am Sonntag anmelden.
Wir sind zwei Personen.
Treffpunkt ist am Rathaus, richtig?

Viele Grüße
Elena""",
        """主旨：城市導覽報名

您好，

我想報名星期天的城市導覽。
我們兩人。
集合點是市政廳，對嗎？

問候
Elena""",
        [n("mich … anmelden", "報名", "sich anmelden。"), n("Personen", "人數"), n("Treffpunkt", "集合點"), n("Rathaus", "市政廳"), n("richtig?", "對嗎？")],
        [p("Ich möchte mich für … anmelden.", "報名", "Ich melde mich für den Kurs an."), p("Treffpunkt ist …", "確認集合", "Treffpunkt vor dem Museum")],
        ["報名：活動＋人數＋確認地點。", "sich anmelden 要有反身代詞。"],
        ["活動", "城市"],
    ),
    item(
        "a1-65", "A1", "story", "第一次下雪",
        "Erster Schnee", "第一場雪",
        """Heute schneit es zum ersten Mal in diesem Winter.
Die Straßen sind weiß und ruhig.
Kinder bauen einen Schneemann.
Ich mache ein Foto und schicke es an meine Familie.
Es ist kalt, aber schön.""",
        """今天是這個冬天第一場雪。
街道又白又安靜。
孩子們堆雪人。
我拍照傳給家人。
很冷，但很美。""",
        [n("schneit", "下雪", "es schneit。"), n("zum ersten Mal", "第一次"), n("Schneemann", "雪人"), n("schicke … an", "傳給……"), n("kalt, aber schön", "冷但美")],
        [p("Es schneit / regnet.", "天氣無人稱", "Es ist windig."), p("zum ersten Mal", "第一次經驗", "Ich fahre zum ersten Mal Ski.")],
        ["天氣動詞常用 es。", "對比：kalt, aber schön。"],
        ["天氣", "季節"],
    ),
    item(
        "a1-66", "A1", "notice", "影印室",
        "Drucker außer Betrieb", "印表機故障",
        """Achtung!
Der Drucker im 2. Stock ist defekt.
Bitte nutzen Sie den Copyshop gegenüber.
Kopien für den Kurs bitte bis 16 Uhr fertig machen.
Technik-Team""",
        """注意！
二樓印表機故障。
請使用對面的影印店。
課程用影印請於 16 點前完成。
技術組""",
        [n("Achtung", "注意"), n("defekt", "故障的"), n("nutzen", "使用"), n("gegenüber", "對面"), n("fertig machen", "完成")],
        [p("Bitte nutzen Sie …", "改用建議", "Bitte nutzen Sie den Nebeneingang."), p("bis + 時間", "截止", "bis Freitag")],
        ["故障公告：問題＋替代＋期限。", "defekt ≈ außer Betrieb。"],
        ["學校", "公告"],
    ),
    item(
        "a1-67", "A1", "dialogue", "點甜點",
        "Zum Dessert", "點甜點",
        """Kellner: Möchten Sie noch ein Dessert?
Gast: Was empfehlen Sie?
Kellner: Den Apfelkuchen. Er ist frisch.
Gast: Dann nehme ich den, bitte.
Kellner: Mit Sahne?
Gast: Ja, gerne.""",
        """服務生：還要甜點嗎？
客人：您推薦什麼？
服務生：蘋果派。很新鮮。
客人：那就來這個。
服務生：要加鮮奶油嗎？
客人：好，麻煩。""",
        [n("Dessert", "甜點"), n("empfehlen", "推薦"), n("Apfelkuchen", "蘋果派"), n("frisch", "新鮮"), n("Sahne", "鮮奶油")],
        [p("Was empfehlen Sie?", "請人推薦", "Welche Suppe empfehlen Sie?"), p("Dann nehme ich …", "接受推薦", "Dann nehme ich die Tagessuppe.")],
        ["餐廳：問推薦→選→加料。", "gerne＝樂意。"],
        ["餐廳", "食物"],
    ),
    item(
        "a1-68", "A1", "email", "還書延期",
        "Frist verlängern", "延長借期",
        """Betreff: Buch verlängern

Guten Tag,

kann ich das Buch „Einfach Deutsch“ verlängern?
Die Frist endet morgen.
Eine Online-Verlängerung funktioniert leider nicht.

Vielen Dank
Omar""",
        """主旨：續借圖書

您好，

《Einfach Deutsch》這本書可以續借嗎？
期限明天截止。
線上續借無法使用。

謝謝
Omar""",
        [n("verlängern", "延長／續借"), n("Frist", "期限"), n("endet", "結束"), n("funktioniert … nicht", "無法運作"), n("leider", "可惜／遺憾")],
        [p("Kann ich … verlängern?", "請求延期", "Kann ich den Termin verlängern?"), p("Die Frist endet …", "說明期限", "Die Frist endet am Montag.")],
        ["圖書館郵件：書名＋期限＋問題。", "Frist＝截止日期。"],
        ["圖書館", "請求"],
    ),
    item(
        "a1-69", "A1", "story", "新同事",
        "Der erste Tag", "第一天上班",
        """Heute ist mein erster Tag in der Firma.
Meine Kollegin zeigt mir das Büro und die Kaffeemaschine.
Um 12 Uhr essen wir zusammen in der Kantine.
Alle sind nett zu mir.
Ich bin noch nervös, aber es geht gut.""",
        """今天是我在公司的第一天。
女同事帶我看辦公室和咖啡機。
12 點我們一起在員工餐廳吃飯。
大家對我都很好。
我還是緊張，但進行順利。""",
        [n("erster Tag", "第一天"), n("Kollegin", "女同事"), n("zeigt mir", "指給我看", "zeigen + 第三格。"), n("Kantine", "員工餐廳"), n("nervös", "緊張的")],
        [p("zeigt mir + 第四格", "帶人熟悉環境", "Sie zeigt mir den Weg."), p("nett zu mir", "對我友好", "freundlich zu den Gästen")],
        ["職場第一天：介紹→午餐→感受。", "es geht gut＝狀況不錯。"],
        ["工作", "日常"],
    ),
    item(
        "a1-70", "A1", "notice", "寵物日",
        "Hunde willkommen", "歡迎帶狗",
        """Info für Gäste
Kleine Hunde sind im Café willkommen.
Bitte an der Leine führen.
Nicht auf Stühle setzen.
Wasser für Hunde gibt es kostenlos an der Theke.
Wir freuen uns auf Ihren Besuch!""",
        """旅客須知
小型犬歡迎進入咖啡廳。
請繫繩牽好。
請勿放上椅子。
櫃台免費提供狗用水。
期待您的光臨！""",
        [n("willkommen", "受歡迎"), n("an der Leine", "用牽繩"), n("führen", "牽／帶領"), n("kostenlos", "免費"), n("Theke", "櫃台")],
        [p("… sind willkommen", "歡迎對象", "Kinder sind willkommen."), p("Bitte … führen / setzen", "行為規則", "Bitte draußen warten.")],
        ["場所規則：允許＋限制＋服務。", "an der Leine＝繫繩。"],
        ["服務", "規則"],
    ),
]


# ═══════════════════════════════════════════════════════════════════
# A2 51–70  (~280–420 chars)
# ═══════════════════════════════════════════════════════════════════
A2 = [
    item(
        "a2-51", "A2", "email", "保險理賠",
        "Schadensmeldung Fahrrad", "腳踏車理賠申請",
        """Betreff: Diebstahl meines Fahrrads

Sehr geehrte Damen und Herren,

am 3. März wurde mein Fahrrad vor dem Bahnhof gestohlen.
Ich habe am selben Tag Anzeige bei der Polizei erstattet.
Anbei sende ich die Anzeigenummer und Fotos des Schlosses.
Bitte teilen Sie mir mit, welche Unterlagen Sie noch benötigen.

Mit freundlichen Grüßen
Jonas Weber""",
        """主旨：腳踏車失竊

敬啟者：

3 月 3 日我的腳踏車在火車站前被偷。
當天我已向警方報案。
附件寄上報案編號與車鎖照片。
請告知還需要哪些資料。

此致問候
Jonas Weber""",
        [n("Diebstahl", "竊盜"), n("Anzeige … erstattet", "報案", "Anzeige erstatten。"), n("Anbei", "隨信附上"), n("Unterlagen", "文件資料"), n("benötigen", "需要")],
        [p("am selben Tag", "同一天", "Am selben Abend habe ich angerufen."), p("Bitte teilen Sie mir mit, …", "正式請求回覆", "Bitte teilen Sie uns die Frist mit."), p("Anbei sende ich …", "附件說明", "Anbei finden Sie die Rechnung.")],
        ["保險郵件：事件＋已採取步驟＋附件＋提問。", "Anzeige erstatten＝報案固定搭配。"],
        ["保險", "正式郵件"],
    ),
    item(
        "a2-52", "A2", "dialogue", "客服通話",
        "Falsche Lieferung", "送錯貨",
        """Kundin: Hallo, ich habe eine Bestellung erhalten, aber die Größe stimmt nicht.
Service: Wie lautet Ihre Bestellnummer?
Kundin: 88421. Ich möchte umtauschen.
Service: Kein Problem. Sie können das Paket kostenlos zurückschicken.
Kundin: Wie lange dauert der Umtausch?
Service: In der Regel fünf Werktage, sobald das Paket bei uns ist.""",
        """顧客：您好，我收到訂單，但尺寸不對。
客服：您的訂單編號是？
顧客：88421。我想換貨。
客服：沒問題。您可以免費退回包裹。
顧客：換貨要多久？
客服：包裹到我們這邊後，通常五個工作天。""",
        [n("Bestellung", "訂單"), n("stimmt nicht", "不對／不符"), n("umtauschen", "換貨"), n("zurückschicken", "寄回"), n("Werktage", "工作日")],
        [p("Die Größe stimmt nicht.", "說明瑕疵", "Die Farbe stimmt nicht."), p("sobald + 句子", "一……就……", "Sobald ich weiß, schreibe ich."), p("In der Regel …", "一般情況", "In der Regel antworten wir in 24 Stunden.")],
        ["客服：問題→編號→解決→時程。", "Werktage 不含假日。"],
        ["客服", "購物"],
    ),
    item(
        "a2-53", "A2", "story", "志工經驗",
        "Ehrenamt im Tierheim", "動物收容所志工",
        """Seit drei Monaten helfe ich samstags im Tierheim.
Ich füttere die Katzen und gehe mit den Hunden spazieren.
Am Anfang war ich unsicher, aber die Mitarbeiter erklären alles geduldig.
Durch die Arbeit lerne ich Verantwortung und werde ruhiger.
Nächsten Monat organisiere ich mit zwei Freunden eine Spendenaktion.""",
        """三個月來我每週六在動物收容所幫忙。
我餵貓、遛狗。
一開始沒把握，但員工會耐心說明。
透過這份工作我學會負責，也變得較沉穩。
下個月我和兩位朋友一起辦募款活動。""",
        [n("Ehrenamt", "志工／公益服務"), n("Tierheim", "動物收容所"), n("unsicher", "沒把握的"), n("geduldig", "耐心的"), n("Spendenaktion", "募款活動")],
        [p("Seit + 時間dauer", "從……以來", "Seit zwei Jahren wohne ich hier."), p("Am Anfang …, aber …", "前後對比", "Am Anfang war es schwer, aber jetzt geht es."), p("Durch + 第四格", "透過……", "Durch Sport werde ich fitter.")],
        ["經驗文：時間→任務→轉變→下一步。", "Ehrenamt 是名詞，做志工可說 ehrenamtlich helfen。"],
        ["社會", "經歷"],
    ),
    item(
        "a2-54", "A2", "notice", "大樓施工",
        "Baulärm im Hof", "庭院施工噪音",
        """Information der Hausverwaltung
Vom 12. bis 16. April finden im Innenhof Arbeiten statt.
Mit erhöhtem Lärm ist zwischen 8 und 16 Uhr zu rechnen.
Die Waschküche bleibt in dieser Zeit geschlossen.
Bei dringenden Fragen wenden Sie sich bitte an Frau Lange (Zi. 12).
Vielen Dank für Ihre Geduld.""",
        """管委會通知
4 月 12 至 16 日內院將進行施工。
8 至 16 點請預期噪音較大。
此期間洗衣房關閉。
緊急問題請洽 Lange 女士（12 室）。
感謝您的耐心。""",
        [n("Hausverwaltung", "管委會／物業管理"), n("finden … statt", "舉行／進行", "stattfinden。"), n("Mit … ist zu rechnen", "須預期……"), n("dringenden", "緊急的"), n("wenden Sie sich an", "請聯絡……")],
        [p("Vom … bis … finden … statt", "公告時段", "Vom Montag bis Mittwoch finden Prüfungen statt."), p("Mit … ist zu rechnen", "預期後果", "Mit Verzögerungen ist zu rechnen."), p("wenden Sie sich bitte an …", "正式聯絡指引", "Wenden Sie sich an den Support.")],
        ["施工公告：時段＋影響＋聯絡窗口。", "ist zu rechnen＝應預估到。"],
        ["住房", "公告"],
    ),
    item(
        "a2-55", "A2", "email", "大學宿舍",
        "Bewerbung Wohnheim", "申請宿舍",
        """Betreff: Bewerbung um einen Wohnheimplatz

Sehr geehrte Damen und Herren,

ich beginne im Oktober ein Studium an Ihrer Universität und bewerbe mich um ein Zimmer im Wohnheim.
Ich bin Nichtraucher und wünsche mir möglichst ein ruhiges Zimmer.
Anbei finden Sie Immatrikulationsbescheinigung und Einkommensnachweis.
Über eine positive Rückmeldung würde ich mich freuen.

Mit freundlichen Grüßen
Minh Tran""",
        """主旨：申請宿舍床位

敬啟者：

我將於十月於貴校開始就讀，特此申請宿舍房間。
我不抽菸，希望盡可能安靜的房間。
附件為註冊證明與收入證明。
若能獲正面回覆將不勝感激。

此致問候
Minh Tran""",
        [n("bewerbe mich um", "申請……", "sich bewerben um。"), n("Wohnheim", "宿舍"), n("Nichtraucher", "不抽菸者"), n("Immatrikulationsbescheinigung", "註冊證明"), n("Rückmeldung", "回覆")],
        [p("ich bewerbe mich um …", "正式申請", "Ich bewerbe mich um ein Praktikum."), p("möglichst + 形容詞", "盡可能……", "möglichst zentral"), p("Über … würde ich mich freuen", "客氣期待回覆", "Über eine Einladung würde ich mich freuen.")],
        ["申請信：目的＋偏好＋附件＋收尾。", "sich bewerben um + 第四格。"],
        ["大學", "住房"],
    ),
    item(
        "a2-56", "A2", "dialogue", "診所預約改期",
        "Termin verschieben", "改約診時間",
        """Patient: Guten Tag, ich habe morgen um 9 Uhr einen Termin. Kann ich ihn verschieben?
Empfang: Welchen Grund gibt es?
Patient: Ich muss unerwartet arbeiten.
Empfang: Wir hätten Freitag um 11 oder Montag um 15 Uhr.
Patient: Montag passt besser.
Empfang: Gut, ich trage das ein. Bitte kommen Sie zehn Minuten früher.""",
        """病人：您好，我明天 9 點有約診。可以改期嗎？
櫃台：什麼原因呢？
病人：我臨時必須加班。
櫃台：我們週五 11 點或週一 15 點有空。
病人：週一比較適合。
櫃台：好，我幫您登記。請提早十分鐘到。""",
        [n("verschieben", "改期／延後"), n("unerwartet", "出乎意料地"), n("Wir hätten …", "我們可以……", "虛擬式客氣提議。"), n("passt besser", "比較適合"), n("trage … ein", "登記", "eintragen。")],
        [p("Kann ich … verschieben?", "請求改期", "Kann ich den Flug verschieben?"), p("Wir hätten A oder B.", "提供選項", "Wir hätten noch zwei Plätze."), p("… passt besser", "選擇較佳方案", "Donnerstag passt besser.")],
        ["改約：原時間→原因→選項→確認。", "hätten 使提議較客氣。"],
        ["醫療", "預約"],
    ),
    item(
        "a2-57", "A2", "story", "語言交換",
        "Sprachpartner gesucht", "尋找語言交換夥伴",
        """Über eine App habe ich eine Sprachpartnerin gefunden.
Einmal pro Woche sprechen wir 30 Minuten Deutsch und 30 Minuten Koreanisch.
Manchmal korrigieren wir uns, manchmal erzählen wir einfach aus dem Alltag.
So vergesse ich Vokabeln weniger und habe weniger Angst vorm Sprechen.
Nächste Woche treffen wir uns zum ersten Mal persönlich in einem Café.""",
        """我透過 App 找到一位語言交換夥伴。
每週一次，我們各說 30 分鐘德文與韓文。
有時互相糾正，有時只聊日常。
這樣單字比較記得住，說話也比較不害怕。
下週我們第一次在咖啡廳見面。""",
        [n("Sprachpartnerin", "語言交換女夥伴"), n("Einmal pro Woche", "每週一次"), n("korrigieren", "糾正"), n("vorm Sprechen", "面對開口說話", "vor dem。"), n("persönlich", "親自／當面")],
        [p("Einmal pro Woche …", "頻率", "Zweimal pro Monat treffe ich sie."), p("Manchmal …, manchmal …", "並列情況", "Manchmal früh, manchmal spät."), p("Angst vor + 第三格", "害怕……", "Angst vor Prüfungen")],
        ["學習文：工具→節奏→好處→下一步。", "pro Woche＝每週。"],
        ["學習", "社交"],
    ),
    item(
        "a2-58", "A2", "notice", "圖書館閉館",
        "Umbau der Stadtbibliothek", "市立圖書館整修",
        """Wichtige Information
Die Stadtbibliothek bleibt vom 1. bis 20. Mai wegen Umbaus geschlossen.
Online-Verlängerungen sind weiterhin möglich.
Vorbestellte Medien können am Seiteneingang abgeholt werden (Mo–Fr 10–13 Uhr).
Fragen bitte an info@stadtbibliothek.example.
Wir bitten um Verständnis.""",
        """重要通知
市立圖書館因整修，5 月 1 至 20 日關閉。
線上續借仍可使用。
預約資料可於側門領取（週一至五 10–13 點）。
問題請寄 info@stadtbibliothek.example。
敬請見諒。""",
        [n("Umbau", "整修／改建"), n("weiterhin", "仍然"), n("Vorbestellte Medien", "預約的媒體資料"), n("Seiteneingang", "側門"), n("Wir bitten um Verständnis", "敬請見諒")],
        [p("bleibt … geschlossen", "關閉狀態", "Die Straße bleibt gesperrt."), p("sind weiterhin möglich", "服務仍可用", "Rückgaben sind weiterhin möglich."), p("Wir bitten um …", "正式請求體諒", "Wir bitten um Geduld.")],
        ["閉館公告：期間＋仍可服務＋替代取件。", "Medien＝書籍／影音等館藏。"],
        ["圖書館", "公告"],
    ),
    item(
        "a2-59", "A2", "email", "實習週報",
        "Kurzbericht Praktikum", "實習短報告",
        """Betreff: Wochenbericht KW 14

Liebe Frau Schneider,

diese Woche habe ich bei der Kundenaufnahme geholfen und zwei Präsentationen vorbereitet.
Besonders interessant war das Gespräch mit dem Marketingteam.
Nächste Woche werde ich bei der Messe am Stand mitarbeiten.
Bitte sagen Sie mir, ob der Bericht so ausführlich genug ist.

Viele Grüße
Leila""",
        """主旨：第 14 週週報

Schneider 女士您好，

本週我協助接待客戶，並準備兩份簡報。
與行銷團隊的談話特別有意思。
下週我將在展覽攤位協助。
請告訴我這份報告是否夠詳細。

問候
Leila""",
        [n("Wochenbericht", "週報"), n("Kundenaufnahme", "客戶接待"), n("Präsentationen", "簡報"), n("Messe", "展覽／商展"), n("ausführlich genug", "夠詳細")],
        [p("diese Woche habe ich …", "報告本週工作", "Diese Woche habe ich telefoniert."), p("Besonders interessant war …", "突出重點", "Besonders hilfreich war das Feedback."), p("ob … genug ist", "詢問是否足夠", "Ob der Text klar genug ist?")],
        ["實習報告：本週→亮點→下週→請回饋。", "KW＝Kalenderwoche 行事曆週次。"],
        ["職場", "實習"],
    ),
    item(
        "a2-60", "A2", "dialogue", "健身房入會",
        "Mitgliedschaft Fitness", "健身會員諮詢",
        """Berater: Suchen Sie eine Monats- oder Jahreskarte?
Kundin: Erstmal monatlich. Kann ich jederzeit kündigen?
Berater: Ja, mit einer Frist von 14 Tagen.
Kundin: Gibt es Kursangebote?
Berater: Ja, Yoga und Rückenfitness sind inklusive.
Kundin: Gut, dann schaue ich mir den Vertrag in Ruhe an.""",
        """顧問：您要月卡還是年卡？
顧客：先月繳。可以隨時解約嗎？
顧問：可以，需提前 14 天。
顧客：有團課嗎？
顧問：有，瑜伽與背部健身包含在內。
顧客：好，那我先慢慢看合約。""",
        [n("Mitgliedschaft", "會員資格"), n("kündigen", "解約"), n("Frist von … Tagen", "……天期限"), n("inklusive", "包含在內"), n("in Ruhe", "慢慢地／從容地")],
        [p("Kann ich jederzeit kündigen?", "問解約彈性", "Kann ich den Vertrag verlängern?"), p("mit einer Frist von …", "解約預告期", "mit einer Frist von einem Monat"), p("in Ruhe anschauen", "不急著決定", "Ich lese das in Ruhe.")],
        ["服務對話：方案→解約→內容→暫緩簽約。", "Frist＝預告期。"],
        ["消費", "合約"],
    ),
    item(
        "a2-61", "A2", "story", "共乘上班",
        "Mitfahrgelegenheit", "共乘上班",
        """Seit Januar fahre ich mit zwei Kollegen zur Arbeit.
Wir wechseln uns ab: jede Woche fährt jemand anderes.
So sparen wir Benzin und kommen trotzdem pünktlich an.
Manchmal gibt es Stau, aber dann hören wir Podcasts.
Nächsten Monat wollen wir noch eine Person aus der Nachbarabteilung mitnehmen.""",
        """從一月起我和兩位同事共乘上班。
我們輪流：每週換人開車。
這樣省油，卻仍能準時到。
有時塞車，但我們就聽 Podcast。
下個月還想再載鄰近部門的一個人。""",
        [n("Mitfahrgelegenheit", "共乘機會"), n("wechseln uns ab", "互相輪替", "sich abwechseln。"), n("Benzin", "汽油"), n("pünktlich", "準時"), n("Nachbarabteilung", "鄰近部門")],
        [p("Wir wechseln uns ab.", "輪流制度", "Wir wechseln uns mit dem Kochen ab."), p("trotzdem", "儘管如此仍……", "Es regnet, trotzdem gehe ich."), p("noch eine Person mitnehmen", "再載一人", "Können wir noch jemanden mitnehmen?")],
        ["共乘故事：制度→好處→小問題→擴充。", "sich abwechseln＝輪流。"],
        ["交通", "職場"],
    ),
    item(
        "a2-62", "A2", "notice", "社區菜園",
        "Gemeinschaftsgarten", "社區菜園報名",
        """Aushang: Gemeinschaftsgarten
Ab Mai können Bewohnerinnen und Bewohner Beete pachten.
Kosten: 20 Euro pro Saison inkl. Wasser und Werkzeug.
Einführungstermin: 28. April, 17 Uhr am Hinterhof.
Bitte bis 20. April per E-Mail an garten@haus.example melden.
Kinder sind willkommen, wenn eine Aufsichtsperson dabei ist.""",
        """公告：社區菜園
自五月起住戶可承租菜圃。
費用：每季 20 歐元，含水與工具。
說明會：4 月 28 日 17 點，後院。
請於 4 月 20 日前寄信至 garten@haus.example 報名。
歡迎兒童，但須有監護人陪同。""",
        [n("Gemeinschaftsgarten", "社區菜園"), n("Beete pachten", "承租菜圃"), n("inkl.", "包含", "inklusive。"), n("Einführungstermin", "說明會時段"), n("Aufsichtsperson", "監護人")],
        [p("Ab + 月份 können …", "自某時起可……", "Ab Juni können Sie buchen."), p("inkl. A und B", "費用含……", "inkl. Frühstück"), p("wenn eine … dabei ist", "條件附句", "wenn ein Erwachsener dabei ist")],
        ["社區活動：資格＋費用＋說明會＋條件。", "pachten＝承租（土地等）。"],
        ["社區", "活動"],
    ),
    item(
        "a2-63", "A2", "email", "旅行投訴",
        "Beschwerde Hotelzimmer", "飯店房間投訴",
        """Betreff: Beschwerde zu Zimmer 412

Sehr geehrte Damen und Herren,

leider war unser Zimmer bei der Ankunft nicht gereinigt und die Klimaanlage defekt.
Nach zwei Stunden bekamen wir ein anderes Zimmer, das in Ordnung war.
Dennoch erwarte ich eine teilweise Erstattung für den ersten Abend.
Anbei die Buchungsnummer und Fotos.

Mit freundlichen Grüßen
Carla Mendes""",
        """主旨：412 房投訴

敬啟者：

很遺憾，抵達時房間未清掃且空調故障。
兩小時後我們換到另一間狀況正常的房間。
儘管如此，我仍希望第一晚能獲部分退款。
附件為訂房編號與照片。

此致問候
Carla Mendes""",
        [n("leider", "遺憾地"), n("bei der Ankunft", "抵達時"), n("defekt", "故障的"), n("Dennoch", "儘管如此"), n("teilweise Erstattung", "部分退款")],
        [p("leider war … nicht …", "禮貌陳述問題", "Leider war das Essen kalt."), p("Dennoch erwarte ich …", "堅持請求", "Dennoch bitte ich um Klärung."), p("Anbei …", "附件", "Anbei die Rechnung.")],
        ["投訴：問題→已處理→仍要補償→附件。", "Dennoch 轉折後提出要求。"],
        ["旅行", "投訴"],
    ),
    item(
        "a2-64", "A2", "dialogue", "銀行辦卡",
        "Kreditkarte beantragen", "申請信用卡",
        """Beraterin: Möchten Sie eine Kreditkarte zu Ihrem Girokonto?
Kunde: Ja, aber mit niedrigem Limit, bitte.
Beraterin: Haben Sie eine feste Anstellung und eine Meldebescheinigung?
Kunde: Ja, beides. Wie hoch sind die Jahresgebühren?
Beraterin: Im ersten Jahr kostenlos, danach 30 Euro.
Kunde: Okay, ich nehme das Angebot.""",
        """行員：您要為往來帳戶加辦信用卡嗎？
顧客：要，但請給較低額度。
行員：您有正職與戶籍登記證明嗎？
顧客：都有。年費多少？
行員：第一年免費，之後 30 歐元。
顧客：好，我接受這個方案。""",
        [n("Kreditkarte", "信用卡"), n("niedrigem Limit", "較低額度"), n("feste Anstellung", "正職／穩定聘僱"), n("Jahresgebühren", "年費"), n("Im ersten Jahr", "第一年")],
        [p("mit niedrigem / hohem Limit", "額度偏好", "mit flexiblem Limit"), p("Im ersten Jahr …, danach …", "費用時程", "Im ersten Monat gratis, danach 10 Euro."), p("Ich nehme das Angebot.", "接受方案", "Ich nehme den Tarif Basic.")],
        ["銀行：產品→條件→費用→決定。", "Meldebescheinigung＝戶籍登記證明。"],
        ["銀行", "行政"],
    ),
    item(
        "a2-65", "A2", "story", "夜班體驗",
        "Eine Woche Nachtschicht", "一週夜班",
        """Letzte Woche habe ich zum ersten Mal Nachtschicht gearbeitet.
Tagsüber konnte ich kaum schlafen, weil es draußen hell und laut war.
Meine Kolleginnen haben mir Tipps gegeben: dunkle Vorhänge und feste Zeiten.
Ab dem dritten Tag ging es besser.
Trotzdem weiß ich jetzt, dass ich Dauer-Nachtarbeit nicht möchte.""",
        """上週我第一次上夜班。
白天幾乎睡不著，因為外面又亮又吵。
女同事給我建議：遮光窗簾與固定作息。
從第三天起好多了。
不過我現在知道自己不想長期做夜班。""",
        [n("Nachtschicht", "夜班"), n("Tagsüber", "白天"), n("kaum", "幾乎不"), n("feste Zeiten", "固定時段"), n("Dauer-Nachtarbeit", "長期夜班工作")],
        [p("zum ersten Mal …", "第一次經驗", "Zum ersten Mal bin ich allein gereist."), p("Ab dem … Tag", "從第……天起", "Ab dem zweiten Monat"), p("Trotzdem weiß ich jetzt, dass …", "經驗結論", "Trotzdem weiß ich, dass ich Hilfe brauche.")],
        ["經驗敘事：困難→建議→改善→結論。", "kaum＝幾乎不。"],
        ["職場", "健康"],
    ),
    item(
        "a2-66", "A2", "notice", "回收日變更",
        "Änderung der Müllabfuhr", "垃圾清運變更",
        """Bekanntmachung
Wegen eines Feiertags verschiebt sich die gelbe Tonne vom Mittwoch auf Donnerstag.
Die Biotonne bleibt am Dienstag.
Bitte stellen Sie die Tonnen erst ab 19 Uhr am Vorabend heraus.
Falsch befüllte Tonnen werden nicht geleert.
Fragen: 0800 123 456""",
        """公告
因國定假日，黃色資源回收桶由週三改為週四清運。
廚餘桶仍為週二。
請於前一晚 19 點後再推出去。
分類錯誤的桶將不予清空。
詢問：0800 123 456""",
        [n("Müllabfuhr", "垃圾清運"), n("verschiebt sich", "改期／挪動"), n("gelbe Tonne", "黃色資源桶"), n("Vorabend", "前一晚"), n("Falsch befüllte", "裝填錯誤的")],
        [p("Wegen … verschiebt sich …", "因故改期", "Wegen Streiks verschiebt sich der Zug."), p("bleibt am …", "維持原日", "Die Abholung bleibt am Freitag."), p("werden nicht …", "不予……", "werden nicht angenommen")],
        ["市政公告：哪種桶＋新日期＋放置規則。", "Tonne＝垃圾桶。"],
        ["市政", "公告"],
    ),
    item(
        "a2-67", "A2", "email", "課程請假",
        "Fehlzeiten Kurs", "課程缺席說明",
        """Betreff: Abwesenheit am 8. und 9. Mai

Liebe Kursleitung,

leider kann ich am 8. und 9. Mai nicht am Unterricht teilnehmen, weil ich eine Prüfung an der Universität habe.
Die Hausaufgabe schicke ich per E-Mail.
Könnten Sie mir bitte die Materialien der beiden Tage nachreichen?

Vielen Dank und freundliche Grüße
Sofia""",
        """主旨：5 月 8、9 日缺席

課程負責老師您好，

很遺憾 5 月 8、9 日無法上課，因為我有大學考試。
作業會用電子郵件交。
能否請您補寄這兩天的教材？

謝謝並致問候
Sofia""",
        [n("Abwesenheit", "缺席"), n("teilnehmen", "參加"), n("Hausaufgabe", "作業"), n("nachreichen", "事後補交／補寄"), n("Könnten Sie …", "能否請您……", "虛擬式客氣請求。")],
        [p("leider kann ich nicht …, weil …", "請假原因", "Leider kann ich nicht kommen, weil ich krank bin."), p("Könnten Sie mir bitte …?", "客氣請求", "Könnten Sie das wiederholen?"), p("per E-Mail", "以郵件方式", "per Post / per Telefon")],
        ["缺席信：日期＋原因＋已盡義務＋請求。", "nachreichen＝補上。"],
        ["學校", "郵件"],
    ),
    item(
        "a2-68", "A2", "dialogue", "租屋看房",
        "Wohnungsbesichtigung", "看房對話",
        """Vermieterin: Die Wohnung hat 48 Quadratmeter und einen Balkon.
Interessentin: Sind Nebenkosten in der Miete enthalten?
Vermieterin: Nein, zusätzlich etwa 120 Euro.
Interessentin: Darf man die Wände streichen?
Vermieterin: Ja, in hellen Farben. Vor dem Auszug bitte zurückstreichen.
Interessentin: Ich melde mich bis Freitag.""",
        """房東：公寓 48 平方公尺，有陽台。
看房者：租金含不含雜費？
房東：不含，大約另加 120 歐元。
看房者：可以粉刷牆壁嗎？
房東：可以，用淺色。退租前請漆回原色。
看房者：我週五前回覆。""",
        [n("Quadratmeter", "平方公尺"), n("Nebenkosten", "雜費"), n("enthalten", "包含在內"), n("streichen", "粉刷"), n("Auszug", "遷出")],
        [p("Sind … in der Miete enthalten?", "問是否含在租金", "Ist Internet enthalten?"), p("Darf man …?", "問是否允許", "Darf man Haustiere halten?"), p("Ich melde mich bis …", "承諾回覆期限", "Ich melde mich bis morgen.")],
        ["看房：面積→費用→規則→回覆期限。", "Nebenkosten 常含水電等。"],
        ["租屋", "住房"],
    ),
    item(
        "a2-69", "A2", "story", "數位斷食",
        "Ein Wochenende ohne Smartphone", "無手機的週末",
        """Am letzten Wochenende habe ich mein Smartphone ausgeschaltet.
Zuerst war es ungewohnt: Ich wollte ständig Nachrichten checken.
Später habe ich ein Buch gelesen und lange mit meiner Mitbewohnerin gesprochen.
Sonntagabend war ich überrascht, wie ruhig ich mich fühlte.
Vielleicht mache ich das einmal im Monat wieder.""",
        """上週末我把智慧型手機關掉。
一開始很不習慣：一直想查看訊息。
後來我讀了書，也和室友長談。
星期天晚上我很驚訝自己竟然這麼平靜。
也許我會每個月再做一次。""",
        [n("ausgeschaltet", "關掉", "ausschalten。"), n("ungewohnt", "不習慣的"), n("ständig", "不斷地"), n("Mitbewohnerin", "女室友"), n("überrascht", "驚訝的")],
        [p("Zuerst … Später …", "時間順序", "Zuerst war es schwer. Später wurde es leichter."), p("wie + 形容詞 + sich fühlen", "感受", "Wie müde ich mich fühlte!"), p("einmal im Monat", "每月一次", "zweimal im Jahr")],
        ["體驗文：決定→不適→替代活動→收穫。", "ständig＝一直。"],
        ["數位", "生活"],
    ),
    item(
        "a2-70", "A2", "notice", "公司防災演習",
        "Brandschutzübung", "消防演習",
        """Interne Mitteilung
Am Donnerstag, 10 Uhr, findet eine Brandschutzübung statt.
Bitte verlassen Sie bei Alarm ruhig das Gebäude über die Treppenhäuser.
Fahrstühle dürfen nicht benutzt werden.
Sammeln Sie sich auf dem Parkplatz Süd.
Die Übung dauert voraussichtlich 20 Minuten.""",
        """內部通知
週四 10 點將舉行消防演習。
警報響起時請經由樓梯間冷靜離開大樓。
禁止使用電梯。
請在南停車場集合。
演習預計約 20 分鐘。""",
        [n("Brandschutzübung", "消防演習"), n("bei Alarm", "警報響起時"), n("Treppenhäuser", "樓梯間"), n("dürfen nicht", "不得"), n("voraussichtlich", "預計／大概")],
        [p("findet … statt", "舉行", "Die Sitzung findet online statt."), p("dürfen nicht + Partizip II", "禁止被動", "dürfen nicht geöffnet werden"), p("voraussichtlich + 時間", "預估時長", "voraussichtlich eine Stunde")],
        ["演習公告：時間＋逃生＋禁止＋集合點。", "Treppenhaus＝樓梯間。"],
        ["職場", "安全"],
    ),
]

# ═══════════════════════════════════════════════════════════════════
# B1 51–70  (~380–550 chars)
# ═══════════════════════════════════════════════════════════════════
B1 = [
    item(
        "b1-51", "B1", "email", "工會／工時",
        "Anfrage zur Arbeitszeiterfassung", "工時紀錄詢問",
        """Betreff: Klärung der Zeiterfassung im Homeoffice

Sehr geehrte Frau Richter,

seit der Einführung der digitalen Stempeluhr entstehen Unklarheiten, wann Pausenzeiten zu buchen sind.
Mehrere Kolleginnen berichten, dass kurze Unterbrechungen automatisch als Pause gewertet werden.
Könnten Sie bitte erläutern, welche Regeln verbindlich gelten und wo Ausnahmen dokumentiert werden?
Eine kurze schriftliche Übersicht wäre für das Team sehr hilfreich.

Mit freundlichen Grüßen
Armin Keller
Personalrat""",
        """主旨：釐清在家宅辦的工時紀錄

Richter 女士您好，

自從導入數位打卡鐘後，何時應登記休息時間出現不清楚之處。
多位同事反映，短暫中斷會被自動算作休息。
能否請您說明哪些規則具拘束力、例外應如何記錄？
一份簡短書面整理對團隊會很有幫助。

此致問候
Armin Keller
員工代表會""",
        [n("Zeiterfassung", "工時紀錄"), n("Unklarheiten", "不清楚之處"), n("verbindlich gelten", "具拘束力地適用"), n("Ausnahmen dokumentiert", "例外被記錄"), n("Personalrat", "員工代表會"), n("wäre … hilfreich", "會很有幫助", "虛擬式客氣。")],
        [p("seit der Einführung …", "自實施以來", "Seit der Einführung der App …"), p("Könnten Sie bitte erläutern, …", "正式請求說明", "Könnten Sie bitte bestätigen, …"), p("Eine … Übersicht wäre hilfreich", "客氣建議", "Eine Checkliste wäre hilfreich.")],
        ["職場正式信：問題現象→影響→具體請求。", "verbindlich＝有拘束力。", "Personalrat＝員工代表組織。"],
        ["職場", "正式郵件", "工時"],
    ),
    item(
        "b1-52", "B1", "notice", "租戶大會",
        "Einladung zur Eigentümerversammlung", "區權人大會邀請",
        """Einladung
Zur ordentlichen Eigentümerversammlung am 18. Juni, 19 Uhr, im Gemeinschaftsraum.
Tagesordnung: 1) Jahresabrechnung 2) Dachsanierung 3) Hausordnung zu Fahrrädern.
Vollmachten sind schriftlich bis 16. Juni einzureichen.
Unterlagen liegen ab 1. Juni im Hausflur aus.
Eine Beschlussfähigkeit ist bei Anwesenheit von mindestens 50 Prozent der Anteile gegeben.""",
        """邀請
例行區權人大會：6 月 18 日 19 點，交誼廳。
議程：1) 年度結算 2) 屋頂整修 3) 腳踏車相關住戶公約。
委託書須於 6 月 16 日前書面提交。
資料自 6 月 1 日起置於門廳供閱。
出席份額至少達 50% 始具決議能力。""",
        [n("Eigentümerversammlung", "區權人大會"), n("Tagesordnung", "議程"), n("Vollmachten", "委託書／授權"), n("einzureichen", "須提交", "zu 不定式義務。"), n("Beschlussfähigkeit", "決議能力"), n("Anteile", "（所有權）份額")],
        [p("sind … einzureichen", "須提交", "sind schriftlich zu bestätigen"), p("liegen … aus", "陳列供閱", "Die Liste liegt im Büro aus."), p("bei Anwesenheit von …", "出席條件", "bei Anwesenheit der Hälfte")],
        ["住戶公告：時間地點→議程→文件→法定門檻。", "einzureichen＝有義務提交。"],
        ["住房", "法規", "公告"],
    ),
    item(
        "b1-53", "B1", "story", "遠距會議文化",
        "Kameras an oder aus?", "鏡頭開還是關？",
        """In vielen Teams ist unklar, ob man in Online-Meetings die Kamera einschalten sollte.
Manche argumentieren, sichtbare Gesichter fördern Aufmerksamkeit und Vertrauen.
Andere betonen, dass ständige Sichtbarkeit ermüdend wirkt und Privatsphäre verletzt.
Eine pragmatische Lösung könnte sein, Kameras bei Entscheidungsrunden ein-, bei reinen Info-Calls auszuschalten.
Entscheidend ist, dass die Regel gemeinsam vereinbart und nicht stillschweigend erwartet wird.""",
        """許多團隊不清楚線上會議是否該開鏡頭。
有人主張看得見臉有助專注與信任。
也有人強調持續被看見令人疲乏，也侵擾隱私。
務實做法或許是：決策會議開鏡頭，純資訊會議可關。
關鍵在於規則要共同約定，而非默默期待。""",
        [n("einschalten", "開啟"), n("fördern", "促進"), n("ermüdend wirkt", "產生令人疲乏的效果"), n("Privatsphäre", "隱私"), n("stillschweigend", "默默地／心照不宣地"), n("vereinbart", "約定")],
        [p("Manche … Andere …", "對立觀點", "Manche loben es. Andere kritisieren es."), p("Eine pragmatische Lösung könnte sein, …", "提出折衷", "Eine Lösung könnte sein, früher zu starten."), p("nicht stillschweigend erwartet wird", "反對默認期待", "sollte klar kommuniziert werden")],
        ["論述短文：正反→折衷→結論條件。", "stillschweigend＝未明說。"],
        ["職場", "數位", "論述"],
    ),
    item(
        "b1-54", "B1", "dialogue", "醫療第二意見",
        "Zweitmeinung einholen", "尋求第二意見",
        """Arzt: Die Operation wäre möglich, ist aber nicht dringend.
Patientin: Darf ich eine Zweitmeinung einholen, bevor ich entscheide?
Arzt: Selbstverständlich. Ich stelle Ihnen gerne die Befunde zusammen.
Patientin: Wird das von der Krankenkasse übernommen?
Arzt: In vielen Fällen ja; klären Sie das bitte vorab telefonisch.
Patientin: Gut. Ich melde mich in zehn Tagen mit meiner Entscheidung.""",
        """醫師：手術可行，但並不急迫。
病患：做決定前我可以尋求第二意見嗎？
醫師：當然。我很樂意幫您整理檢查結果。
病患：健保會給付嗎？
醫師：很多情況會；請事先電話確認。
病患：好。十天內回覆我的決定。""",
        [n("Zweitmeinung", "第二意見"), n("einholen", "取得／徵詢"), n("Befunde", "檢查結果／病歷發現"), n("übernommen", "被承擔／給付", "übernehmen。"), n("vorab", "事先"), n("Selbstverständlich", "當然")],
        [p("Darf ich …, bevor ich …?", "決策前請求", "Darf ich nachfragen, bevor ich unterschreibe?"), p("Wird das von … übernommen?", "問費用承擔", "Wird das von der Firma übernommen?"), p("vorab + 副詞／動詞", "事先", "vorab klären")],
        ["醫療對話：選項→權利→文件→費用→期限。", "Zweitmeinung 在德檢健康主題常見。"],
        ["醫療", "決策", "對話"],
    ),
    item(
        "b1-55", "B1", "email", "大學換課",
        "Antrag auf Modulwechsel", "申請更換模組課程",
        """Betreff: Antrag auf Wechsel des Wahlmoduls

Sehr geehrte Prüfungsausschussmitglieder,

hiermit beantrage ich den Wechsel vom Modul „Statistik I“ zum Modul „Qualitative Methoden“.
Grund ist eine Überschneidung mit meinem Pflichtpraktikum an zwei Wochentagen.
Beide Dozierenden haben dem Wechsel bereits per E-Mail zugestimmt; die Nachrichten sind angehängt.
Ich bitte um zeitnahe Entscheidung, da die Anmeldefrist in zehn Tagen endet.

Mit freundlichen Grüßen
Nadine Vogt
Matrikelnummer 308821""",
        """主旨：申請更換選修模組

考試委員會委員您好，

謹此申請由「統計 I」改修「質性方法」。
原因是與必修實習在兩個平日撞課。
兩位授課教師已透過郵件同意；信件附上。
因報名十天後截止，懇請儘速裁定。

此致問候
Nadine Vogt
學號 308821""",
        [n("hiermit beantrage ich", "謹此申請"), n("Wahlmodul", "選修模組"), n("Überschneidung", "時間衝突"), n("zugestimmt", "同意"), n("zeitnahe Entscheidung", "儘速決定"), n("Matrikelnummer", "學號")],
        [p("hiermit beantrage ich …", "正式申請開頭", "Hiermit beantrage ich Urlaub."), p("Grund ist …", "陳述理由", "Grund ist eine Erkrankung."), p("Ich bitte um zeitnahe …", "懇請盡快", "Ich bitte um zeitnahe Rückmeldung.")],
        ["大學申請：請求＋理由＋佐證＋時限。", "hiermit 是公文套語。"],
        ["大學", "行政", "正式郵件"],
    ),
    item(
        "b1-56", "B1", "notice", "資料保護更新",
        "Aktualisierte Datenschutzhinweise", "更新個資告知",
        """Hinweis zur Datenverarbeitung
Ab dem 1. Juli werden Bestelldaten länger gespeichert, um Garantieansprüche nachvollziehen zu können.
Eine Weitergabe an Partner erfolgt nur, soweit dies zur Vertragserfüllung erforderlich ist.
Sie können der Nutzung für Werbung jederzeit widersprechen, ohne dass die Bestellung davon betroffen ist.
Details und Kontaktdaten der Datenschutzbeauftragten finden Sie unter /datenschutz.
Diese Hinweise ersetzen die Fassung vom März.""",
        """資料處理提示
自 7 月 1 日起，訂單資料將保存更久，以便追蹤保固請求。
僅在履行契約所需範圍內才會提供給合作夥伴。
您可隨時拒絕用於行銷，且不影響訂單本身。
細節與個資保護負責人聯絡方式見 /datenschutz。
本提示取代三月版本。""",
        [n("Datenverarbeitung", "資料處理"), n("nachvollziehen", "追溯／理解過程"), n("soweit dies … erforderlich ist", "僅在必要範圍"), n("widersprechen", "提出異議／拒絕"), n("davon betroffen", "因此受影響"), n("ersetzen", "取代")],
        [p("werden … gespeichert, um … zu können", "目的說明", "werden archiviert, um Prüfungen zu ermöglichen"), p("soweit dies erforderlich ist", "必要性限制", "soweit gesetzlich vorgeschrieben"), p("ohne dass …", "不導致……", "ohne dass Mehrkosten entstehen")],
        ["個資公告：變更→限制→異議權→取代舊版。", "widersprechen＝行使拒絕權。"],
        ["法律", "個資", "公告"],
    ),
    item(
        "b1-57", "B1", "story", "共享經濟批判",
        "Teilen ist nicht immer günstig", "共享不一定比較便宜",
        """Carsharing und Roller gelten als flexibel und umweltfreundlich.
In der Praxis entstehen jedoch oft Zusatzkosten durch längere Buchungen oder beschädigte Fahrzeuge.
Wer selten fährt, spart möglicherweise; wer täglich pendelt, rechnet besser mit einem eigenen Rad oder Jobticket.
Zudem verlagert sich Verantwortung: Nutzerinnen müssen Schäden melden und Termine einhalten.
Nachhaltigkeit hängt daher weniger vom Label „Sharing“ ab als von Nutzungshäufigkeit und Alternativen vor Ort.""",
        """共乘汽車與滑板車被視為彈性又環保。
實務上卻常因較長租用或車輛損壞產生額外費用。
很少騎的人或可省錢；每天通勤者精算後可能自有單車或通勤票更划算。
此外責任轉移：使用者必須通報損壞並遵守時段。
永續因此較少取決於「共享」標籤，而取決於使用頻率與在地替代方案。""",
        [n("Carsharing", "共享汽車"), n("Zusatzkosten", "額外費用"), n("pendelt", "通勤"), n("verlagert sich", "轉移"), n("hängt … ab", "取決於", "abhängen von。"), n("Nutzungshäufigkeit", "使用頻率")],
        [p("gelten als …", "被視為……", "gelten als zuverlässig"), p("Wer A, …; wer B, …", "依對象分論", "Wer spät kommt, wartet; wer früh kommt, wählt."), p("hängt weniger von A ab als von B", "比較真正因素", "hängt weniger vom Preis ab als von der Qualität")],
        ["批判短論：流行說法→實務成本→責任→結論。", "abhängen von＝取決於。"],
        ["消費", "環境", "論述"],
    ),
    item(
        "b1-58", "B1", "dialogue", "職場回饋面談",
        "Feedbackgespräch", "回饋面談",
        """Führungskraft: Insgesamt arbeiten Sie zuverlässig. Ein Punkt betrifft die Dokumentation.
Mitarbeiter: Meinen Sie die Wochenberichte?
Führungskraft: Ja. Sie kommen oft erst nach Nachfrage. Das erschwert die Übergabe im Team.
Mitarbeiter: Verstehe. Ich kann sie künftig freitags bis 15 Uhr einstellen.
Führungskraft: Das wäre hilfreich. Dann prüfen wir den Punkt in vier Wochen erneut.
Mitarbeiter: Einverstanden. Danke für das klare Feedback.""",
        """主管：整體來說您工作可靠。有一點關於文件紀錄。
員工：您是指週報嗎？
主管：對。常要催才交。這讓團隊交接變困難。
員工：明白。我以後可以週五 15 點前上傳。
主管：那會很有幫助。四週後我們再檢視這點。
員工：同意。謝謝清楚的回饋。""",
        [n("zuverlässig", "可靠的"), n("betrifft", "涉及"), n("nach Nachfrage", "經催問之後"), n("erschwert", "使變困難"), n("einstellen", "上傳／設置", "此處＝放到系統。"), n("erneut", "再次")],
        [p("Ein Punkt betrifft …", "回饋聚焦", "Ein Punkt betrifft die Pünktlichkeit."), p("Das erschwert …", "說明影響", "Das erschwert die Planung."), p("Dann prüfen wir … erneut", "約定追蹤", "Dann sprechen wir in einem Monat erneut.")],
        ["回饋對話：肯定→問題→影響→具體承諾→追蹤。", "nach Nachfrage＝被催之後。"],
        ["職場", "溝通", "對話"],
    ),
    item(
        "b1-59", "B1", "email", "保險拒賠異議",
        "Widerspruch gegen Ablehnung", "對拒賠提出異議",
        """Betreff: Widerspruch zu Schadennummer 55219

Sehr geehrte Damen und Herren,

hiermit widerspreche ich der Ablehnung meines Antrags vom 2. April.
In Ihrem Schreiben fehlt die Begründung, warum der Wasserschaden als „grobe Fahrlässigkeit“ gewertet wird.
Laut Hausratversicherungspolice sind Leitungswasserschäden grundsätzlich versichert.
Ich bitte um erneute Prüfung und Übersendung der internen Bewertungsgrundlage.
Frist zur Stellungnahme: 14 Tage.

Mit freundlichen Grüßen
Helena Krüger""",
        """主旨：對理賠案 55219 提出異議

敬啟者：

謹此對貴公司 4 月 2 日拒賠提出異議。
來函未說明為何將水損評為「重大過失」。
依家庭財物保險條款，水管漏水損害原則上在保。
請重新審查並寄送內部評定依據。
請於 14 日內回覆。

此致問候
Helena Krüger""",
        [n("widerspreche", "提出異議", "widersprechen。"), n("Ablehnung", "拒絕／拒賠"), n("grobe Fahrlässigkeit", "重大過失"), n("grundsätzlich versichert", "原則上有承保"), n("erneute Prüfung", "重新審查"), n("Stellungnahme", "意見回覆")],
        [p("hiermit widerspreche ich …", "正式異議", "Hiermit widerspreche ich dem Bescheid."), p("In Ihrem Schreiben fehlt …", "指出缺漏", "In Ihrem Schreiben fehlt das Datum."), p("Ich bitte um erneute Prüfung", "請求重審", "Ich bitte um erneute Bearbeitung.")],
        ["異議信：案號→反駁理由→條款依據→期限。", "Fahrlässigkeit＝過失。"],
        ["保險", "法律", "異議"],
    ),
    item(
        "b1-60", "B1", "notice", "校園網路政策",
        "Nutzungsordnung WLAN", "校園無線網路使用規範",
        """Nutzungsordnung für das Hochschul-WLAN
Der Zugang ist ausschließlich Angehörigen der Hochschule gestattet.
Das Weitergeben von Zugangsdaten an Dritte ist untersagt und kann zur Sperrung führen.
Illegale Downloads sowie die Umgehung von Sicherheitssystemen sind verboten.
Bei Störungen melden Sie sich bitte beim IT-Helpdesk unter helpdesk@uni.example.
Mit der Anmeldung erkennen Sie diese Ordnung verbindlich an.""",
        """大學無線網路使用規範
僅校內成員可使用。
禁止將帳密轉給第三人，否則可能遭停權。
禁止非法下載及規避安全系統。
故障請向 IT 服務台 helpdesk@uni.example 回報。
登入即表示您具拘束力地接受本規範。""",
        [n("ausschließlich", "僅限"), n("Angehörigen", "所屬成員"), n("untersagt", "被禁止"), n("Umgehung", "規避"), n("Sperrung", "停權／封鎖"), n("verbindlich an", "具拘束力地接受", "anerkennen。")],
        [p("ist … gestattet / untersagt", "允許／禁止", "Rauchen ist untersagt."), p("kann zur … führen", "可能導致……", "kann zur Kündigung führen"), p("Mit der Anmeldung erkennen Sie … an", "默示同意條款", "Mit der Buchung erkennen Sie die AGB an.")],
        ["規範公告：資格→禁止→後果→聯絡→同意。", "untersagt＝正式「禁止」。"],
        ["大學", "數位", "規範"],
    ),
    item(
        "b1-61", "B1", "story", "城市交通收費",
        "City-Maut in der Diskussion", "討論市區通行費",
        """Mehrere Städte prüfen eine City-Maut, um Staus und Abgase zu reduzieren.
Befürworterinnen erwarten Einnahmen für den Ausbau von Bahnen und Radwegen.
Kritiker warnen vor sozialer Ungleichheit: Wer im Umland wohnt und aufs Auto angewiesen ist, zahlte stärker.
Ob die Maßnahme wirkt, hängt davon ab, ob gleichzeitig günstige Alternativen angeboten werden.
Ohne verlässlichen ÖPNV bleibt eine Maut vor allem ein Preissignal mit begrenzter Lenkungswirkung.""",
        """多個城市評估徵收市區通行費，以減少塞車與廢氣。
支持者期待收入用於擴建軌道與單車道。
批評者警告社會不均：住郊區又必須開車者負擔會更重。
措施能否奏效，取決於是否同時提供平價替代方案。
若沒有可靠大眾運輸，通行費多半只是價格訊號，導引效果有限。""",
        [n("City-Maut", "市區通行費"), n("Befürworterinnen", "女支持者們"), n("angewiesen ist", "依賴於……"), n("hängt davon ab, ob", "取決於是否"), n("ÖPNV", "大眾運輸", "öffentlicher Personennahverkehr。"), n("Lenkungswirkung", "導引效果")],
        [p("prüfen …, um … zu …", "評估目的", "prüfen Regeln, um Sicherheit zu erhöhen"), p("Wer …, zahlte / zahlt stärker", "負擔分配", "Wer später bucht, zahlt mehr."), p("hängt davon ab, ob …", "條件依賴", "hängt davon ab, ob Hilfe kommt")],
        ["政策短論：措施→正反→成功條件→限制。", "angewiesen auf＝依賴。"],
        ["交通", "社會", "論述"],
    ),
    item(
        "b1-62", "B1", "email", "志工排班衝突",
        "Absage Schicht Ehrenamt", "志工班次請假",
        """Betreff: Absage der Schicht am Samstag

Liebe Koordination,

leider muss ich meine Schicht am Samstag von 10–14 Uhr absagen, weil ein familiärer Notfall eingetreten ist.
Ich habe bereits zwei Teammitglieder gefragt; Frau Albers kann von 10–12 Uhr übernehmen.
Für 12–14 Uhr suche ich noch eine Vertretung und melde mich bis Donnerstagabend.
Bitte bestätigen Sie kurz den Eingang dieser Nachricht.

Herzliche Grüße
Timo Brandt""",
        """主旨：取消週六班次

協調組您好，

很遺憾必須取消週六 10–14 點班次，因家中突發狀況。
我已詢問兩位隊員；Albers 女士可接手 10–12 點。
12–14 點仍在找代理人，週四晚前回報。
請簡短確認已收到此訊息。

誠摯問候
Timo Brandt""",
        [n("Absage", "取消／婉拒"), n("Schicht", "班次"), n("eingetreten ist", "已發生", "eintreten。"), n("übernehmen", "接手"), n("Vertretung", "代理／代班"), n("Eingang", "收件／送達")],
        [p("leider muss ich … absagen, weil …", "取消並說明", "Leider muss ich absagen, weil ich krank bin."), p("kann … übernehmen", "找人接手", "Kannst du den Termin übernehmen?"), p("Bitte bestätigen Sie den Eingang", "請確認收悉", "Bitte bestätigen Sie den Erhalt.")],
        ["責任溝通：取消＋已做補救＋剩餘缺口＋確認。", "Notfall＝緊急狀況。"],
        ["志工", "組織", "郵件"],
    ),
    item(
        "b1-63", "B1", "notice", "噪音整治期",
        "Lärmsanierung Straßenbahn", "路面電車噪音整治",
        """Bekanntmachung des Verkehrsunternehmens
Vom 5. bis 25. September werden Gleise in der Nordstraße saniert.
Nachtarbeiten sind an Werktagen zwischen 22 und 5 Uhr möglich.
Anwohnerinnen erhalten bei Bedarf Gehörschutz über das Bürgerbüro.
Ersatzverkehr mit Bussen ist ausgeschildert; Fahrplanabweichungen sind unter /verkehr abrufbar.
Schadensersatzansprüche wegen Erschütterungen sind innerhalb von vier Wochen zu melden.""",
        """交通公司公告
9 月 5 至 25 日將整修北街軌道。
平日 22 至 5 點可能夜間施工。
住戶如有需要可向市民辦公室領取耳塞／護耳。
替代公車已設標示；班表異動見 /verkehr。
因震動提出之損害賠償須於四週內通報。""",
        [n("saniert", "整修", "sanieren。"), n("Nachtarbeiten", "夜間施工"), n("Anwohnerinnen", "女住戶們／住戶"), n("Ersatzverkehr", "替代交通"), n("ausgeschildert", "已設標示"), n("Schadensersatzansprüche", "損害賠償請求")],
        [p("sind … möglich", "可能發生", "Verzögerungen sind möglich."), p("ist … abrufbar", "可查閱", "Der Plan ist online abrufbar."), p("sind innerhalb von … zu melden", "期限義務", "sind innerhalb von 14 Tagen zu melden")],
        ["工程公告：時段→夜間→補助→替代→求償期限。", "sanieren＝整修更新。"],
        ["交通", "市政", "公告"],
    ),
    item(
        "b1-64", "B1", "dialogue", "租約終止諮詢",
        "Kündigung Mietvertrag", "租約終止諮詢",
        """Beraterin: Wann möchten Sie ausziehen?
Mieter: Zum 31. Oktober. Reicht die Kündigungsfrist von drei Monaten?
Beraterin: Ja, wenn Sie heute noch schriftlich kündigen und der Vermieter das Schreiben erhält.
Mieter: Muss ich Schönheitsreparaturen machen?
Beraterin: Das hängt vom Vertrag ab. Bringen Sie bitte die Klauseln mit.
Mieter: Gut. Ich schicke Ihnen morgen eine Kopie zur Prüfung.""",
        """顧問：您想何時遷出？
房客：10 月 31 日。三個月解約預告期夠嗎？
顧問：可以，若您今天仍書面解約且房東收到信件。
房客：我必須做修繕粉刷嗎？
顧問：取決於合約。請把相關條款帶來。
房客：好。我明天寄副本請您審閱。""",
        [n("ausziehen", "遷出"), n("Kündigungsfrist", "解約預告期"), n("schriftlich kündigen", "書面解約"), n("Schönheitsreparaturen", "修繕粉刷義務"), n("Klauseln", "條款"), n("zur Prüfung", "以供審閱")],
        [p("Reicht die Frist von …?", "確認期限是否足夠", "Reicht die Frist von zwei Wochen?"), p("Das hängt vom Vertrag ab.", "視合約而定", "Das hängt von der Regelung ab."), p("… zur Prüfung schicken", "送審", "Ich schicke die Unterlagen zur Prüfung.")],
        ["諮詢對話：目標日→期限→義務→下一步。", "Schönheitsreparaturen 是租屋常考詞。"],
        ["租屋", "法律", "對話"],
    ),
    item(
        "b1-65", "B1", "story", "演算法招聘",
        "Automatisierte Bewerbungsfilter", "自動化履歷篩選",
        """Viele Unternehmen filtern Bewerbungen zuerst per Software.
Das spart Zeit, kann aber auch passende Personen aussortieren, wenn Lebensläufe ungewöhnlich formuliert sind.
Transparenz wäre wichtig: Bewerberinnen sollten erfahren, welche Kriterien zählen und ob Menschen später nachprüfen.
Gewerkschaften fordern zudem, dass Diskriminierungsrisiken regelmäßig getestet werden.
Technik ersetzt keine Verantwortung; sie verschiebt nur, wann und von wem entschieden wird.""",
        """許多公司先用軟體篩履歷。
這能省時間，但若履歷寫法不尋常，也可能刷掉合適的人。
透明度很重要：應聘者應知道哪些標準算數、之後是否有人覆核。
工會亦要求定期檢測歧視風險。
技術不能取代責任；它只是改變決策的時機與決策者。""",
        [n("filtern", "篩選"), n("aussortieren", "刷掉／剔除"), n("ungewöhnlich formuliert", "表述不尋常"), n("nachprüfen", "覆核"), n("Diskriminierungsrisiken", "歧視風險"), n("verschiebt", "推移／轉移")],
        [p("kann … aussortieren, wenn …", "條件風險", "kann Fehler erzeugen, wenn Daten fehlen"), p("sollten erfahren, welche …", "資訊權", "sollten erfahren, warum …"), p("ersetzt keine …; sie verschiebt nur …", "技術／責任辯證", "ersetzt keine Kontrolle; sie verändert sie")],
        ["科技倫理：效率→誤殺風險→透明→責任歸屬。", "aussortieren＝篩除。"],
        ["科技", "職場", "倫理"],
    ),
    item(
        "b1-66", "B1", "email", "消費者保護",
        "Widerruf Onlinekauf", "線上購物撤回",
        """Betreff: Widerruf der Bestellung 907733

Sehr geehrte Damen und Herren,

hiermit widerrufe ich innerhalb der gesetzlichen Frist den Kauf des Kopfhörers vom 12. Mai.
Das ungeöffnete Paket sende ich morgen mit dem Retourenschein zurück.
Bitte erstatten Sie den Kaufpreis auf das Konto der ursprünglichen Zahlung.
Eine Bestätigung des Widerrufs erwarte ich per E-Mail.

Mit freundlichen Grüßen
Jonas Lehmann""",
        """主旨：撤銷訂單 907733

敬啟者：

謹此在法定期限內撤銷 5 月 12 日耳機購買。
未拆封包裹明日將以退貨單寄回。
請將款項退回原付款帳戶。
請以電子郵件確認已受理撤銷。

此致問候
Jonas Lehmann""",
        [n("widerrufe", "撤銷／撤回", "widerrufen。"), n("gesetzlichen Frist", "法定期限"), n("Retourenschein", "退貨單"), n("erstatten", "退款"), n("ursprünglichen Zahlung", "原付款"), n("Bestätigung", "確認")],
        [p("hiermit widerrufe ich …", "撤回聲明", "Hiermit widerrufe ich den Vertrag."), p("innerhalb der Frist", "在期限內", "innerhalb von 14 Tagen"), p("Bitte erstatten Sie …", "請求退款", "Bitte erstatten Sie den Betrag.")],
        ["消費者撤回：聲明＋退貨＋退款帳戶＋確認。", "Widerruf＝法定撤回權。"],
        ["消費", "法律", "郵件"],
    ),
    item(
        "b1-67", "B1", "notice", "疫苗接種門診",
        "Impfaktion im Stadtteil", "社區接種活動",
        """Öffentliche Impfaktion
Am Samstag, 9–15 Uhr, im Kulturzentrum Ost finden Impfungen ohne Termin statt.
Bitte Personalausweis und Impfpass mitbringen; wer keinen Pass hat, erhält eine Bescheinigung.
Für Menschen mit eingeschränkter Mobilität gibt es einen barrierefreien Eingang an der Südseite.
Kinder unter zwölf Jahren nur in Begleitung einer erwachsenen Bezugsperson.
Aktuelle Wartezeiten werden vor Ort und auf der Website angezeigt.""",
        """公共接種活動
週六 9–15 點於東區文化中心提供免預約接種。
請攜帶身分證與疫苗手冊；無手冊者可獲證明。
行動不便者可走南側無障礙入口。
未滿十二歲須由成年監護人陪同。
目前等候時間現場與網站會公布。""",
        [n("Impfaktion", "接種活動"), n("ohne Termin", "免預約"), n("Impfpass", "疫苗手冊"), n("eingeschränkter Mobilität", "行動受限"), n("barrierefreien", "無障礙的"), n("Bezugsperson", "監護／主要照顧者")],
        [p("finden … statt", "舉行", "finden Beratungen statt"), p("wer keinen … hat, erhält …", "條件補救", "Wer keine Karte hat, erhält ein Ersatzdokument."), p("nur in Begleitung …", "陪同條件", "nur in Begleitung eines Erwachsenen")],
        ["公衛公告：時地→文件→無障礙→年齡規則。", "Impfpass＝接種紀錄本。"],
        ["健康", "公共服務", "公告"],
    ),
    item(
        "b1-68", "B1", "dialogue", "跨部門專案",
        "Kick-off Projektmeeting", "專案啟動會議",
        """Projektleitung: Ziel ist, den Prototyp bis Ende August fertigzustellen.
Design: Dafür brauchen wir spätestens Mitte Juli finale Inhalte.
Technik: Wenn die Inhalte später kommen, verschiebt sich der Test.
Projektleitung: Dann setzen wir einen verbindlichen Liefertermin und eine Eskalationsstufe.
Finanzen: Bitte meldet Mehrbedarf an Budget vor dem 1. Juli.
Alle: Einverstanden. Protokoll kommt heute Nachmittag.""",
        """專案主管：目標是八月底完成原型。
設計：因此我們最晚七月中需要最終內容。
技術：若內容更晚到，測試就會延後。
專案主管：那我們訂具拘束力的交付日與升級處理層級。
財務：預算追加請於七月一日前提出。
全體：同意。會議紀錄今天下午發送。""",
        [n("fertigzustellen", "完成", "fertigstellen。"), n("spätestens", "最晚"), n("verschiebt sich", "延後"), n("verbindlichen Liefertermin", "具拘束力的交付期限"), n("Eskalationsstufe", "問題升級層級"), n("Mehrbedarf", "額外需求")],
        [p("Ziel ist, … zu + Infinitiv", "專案目標", "Ziel ist, Kosten zu senken."), p("Wenn …, verschiebt sich …", "依賴風險", "Wenn Teile fehlen, verschiebt sich die Montage."), p("setzen wir einen verbindlichen …", "訂定硬期限", "setzen wir eine Deadline")],
        ["會議對話：目標→依賴→風險→決策→紀錄。", "Eskalation＝向上呈報。"],
        ["職場", "專案", "對話"],
    ),
    item(
        "b1-69", "B1", "story", "夜班托育爭議",
        "Kita-Öffnungszeiten und Schichtarbeit", "托育時間與輪班",
        """Viele Eltern in Pflege und Logistik arbeiten zu Zeiten, in denen Kitas geschlossen sind.
Private Betreuung ist teuer und nicht überall verfügbar.
Betriebe fordern daher längere Kita-Öffnung, Kommunen verweisen auf fehlendes Personal.
Eine mögliche Zwischenlösung sind betriebliche Kinderzimmer mit klaren Qualitätsstandards.
Solange Versorgungslücken bleiben, betrifft die Debatte nicht nur Familien, sondern auch Fachkräftemangel.""",
        """許多護理與物流業父母的上班時間，托兒所已關閉。
私人托育昂貴且非處處有。
企業因此要求延長托育時間，地方政府則指人力不足。
可能的過渡方案是符合明確品質標準的企業托育室。
只要供給缺口仍在，這場辯論就不只關乎家庭，也關乎缺工。""",
        [n("Kitas", "托兒所", "Kindertagesstätte。"), n("verfügbar", "可取得的"), n("verweisen auf", "指向／歸因於"), n("Zwischenlösung", "過渡方案"), n("Versorgungslücken", "供給缺口"), n("Fachkräftemangel", "專業人力短缺")],
        [p("zu Zeiten, in denen …", "關係時間", "zu Zeiten, in denen wenig Busse fahren"), p("verweisen auf …", "把原因指向……", "verweisen auf fehlende Mittel"), p("Solange …, betrifft …", "持續條件", "Solange Unsicherheit bleibt, betrifft es alle.")],
        ["社會議題：問題→限制→各方立場→過渡→更大後果。", "Fachkräftemangel 是報紙高頻詞。"],
        ["社會", "家庭", "勞動"],
    ),
    item(
        "b1-70", "B1", "email", "媒體更正請求",
        "Gegendarstellung an Redaktion", "向編輯部請求更正說明",
        """Betreff: Gegendarstellung zum Artikel vom 4. Juni

Sehr geehrte Redaktion,

in Ihrem Artikel wird behauptet, unser Verein habe Fördermittel zweckwidrig verwendet.
Diese Darstellung ist unzutreffend; die Prüfung der Stadtverwaltung vom Mai hat keine Verstöße festgestellt.
Wir bitten um Veröffentlichung einer Gegendarstellung in vergleichbarer Länge und Platzierung.
Den Prüfbericht senden wir Ihnen vertraulich zu.
Für Rückfragen stehe ich telefonisch zur Verfügung.

Mit freundlichen Grüßen
Dr. Mira Soltani
Vorsitzende""",
        """主旨：針對 6 月 4 日報導之更正說明

編輯部您好，

貴文聲稱本協會不當使用補助款。
此說法不正確；市政府五月審查並未認定違規。
請以相當篇幅與版位刊登更正說明。
審查報告將保密寄上。
如有疑問，我可電話說明。

此致問候
Dr. Mira Soltani
理事長""",
        [n("Gegendarstellung", "更正／相對陳述"), n("zweckwidrig", "不符合用途地"), n("unzutreffend", "不正確的"), n("Verstöße", "違規"), n("vergleichbarer Länge", "相當篇幅"), n("vertraulich", "保密地")],
        [p("wird behauptet, …", "指出對方主張", "wird behauptet, wir seien informiert worden"), p("Wir bitten um Veröffentlichung …", "請求刊登", "Wir bitten um Berichtigung."), p("stehe … zur Verfügung", "可提供協助", "Ich stehe für ein Interview zur Verfügung.")],
        ["媒體交涉：指出錯誤→舉證→請求形式→附件。", "Gegendarstellung 是新聞法用語。"],
        ["媒體", "法律", "正式郵件"],
    ),
]



# ═══════════════════════════════════════════════════════════════════
# B2 51–70  (~1000–1400 chars)
# ═══════════════════════════════════════════════════════════════════
B2 = [
    item(
        'b2-51', "B2", 'story', '職場',
        'Grenzen im Homeoffice', '在宅辦公的界線',
        """Homeoffice wird oft als Gewinn an Freiheit dargestellt. Gleichzeitig berichten Beschäftigte von längeren Arbeitstagen, weil die Grenze zwischen Beruf und Privatleben verschwimmt. Wer morgens schon Mails liest und abends noch „kurz“ antwortet, verlängert die Anwesenheit, ohne dass dies in Verträgen sichtbar wird.

Unternehmen argumentieren mit Produktivität und gesparten Bürokosten. Betriebsräte hingegen fordern klare Erreichbarkeitsfenster und ein Recht auf Nicht-Erreichbarkeit. Ohne solche Regeln droht eine Kultur der ständigen Verfügbarkeit, die besonders Pflegeaufgaben zu Hause zusätzlich belastet.

Kritikerinnen wenden ein, starre Verbote passten nicht zu internationalen Teams. Dennoch lässt sich Mindestschutz formulieren: Kernarbeitszeiten, dokumentierte Mehrarbeit und freiwillige, aber echte Pausen. Technik allein löst das Problem nicht; nötig sind Vereinbarungen, die überprüft werden.

Insofern ist hybrides Arbeiten weder automatisch modern noch automatisch entlastend. Es bleibt abzuwarten, inwiefern gesetzliche Leitplanken und betriebliche Praxis tatsächlich Erholung sichern. Wer Flexibilität will, muss zugleich Schutzmechanismen mitdenken.""",
        """在宅辦公常被描繪成自由的收穫。同時員工反映工時變長，因為職業與私生活界線模糊。早上就讀郵件、晚上還「快速」回覆的人，延長了在場時間，卻未必寫進合約。

企業以生產力與節省辦公成本辯護。員工代表則要求明確可聯繫時段與「有權不被聯繫」。若無此類規則，恐形成持續待命文化，尤其加重居家照顧負擔。

批評者認為僵硬禁令不適合國際團隊。但仍可設定最低保護：核心工時、加班紀錄與真正自願的休息。單靠技術無法解決；需要可被檢查的約定。

因此混合辦公既不自動現代，也不自動減壓。法規護欄與企業實務能否真正保障恢復，仍有待觀察。想要彈性，就必須同時思考保護機制。""",
        [n('verschwimmt','變模糊'),n('Erreichbarkeitsfenster','可聯繫時段'),n('Nicht-Erreichbarkeit','不被聯繫／離線權'),n('wenden ein','提出反駁'),n('Leitplanken','護欄／基本框架'),n('Insofern','就這點而言'),n('inwiefern','在多大程度上')],
        [p('weder … noch …','雙重否定','weder modern noch entlastend'),p('Kritikerinnen wenden ein, …','引入反論','Kritiker wenden ein, die Kosten seien zu hoch.'),p('Es bleibt abzuwarten, inwiefern …','開放結論','Es bleibt abzuwarten, inwiefern die Reform wirkt.')],
        ['德檢論述：現象→勞資立場→讓步反論→開放結論。', '標出名詞化：Verfügbarkeit、Mehrarbeit、Leitplanken。', '圈出 dennoch／insofern／inwiefern。'],
        ['職場', '數位', '論述', '勞動'],
    ),
    item(
        'b2-52', "B2", 'email', '教育',
        'Beschwerde über Prüfungsorganisation', '對考試組織提出申訴',
        """Betreff: Formelle Beschwerde zur Klausurorganisation im Modul Schreiben

Sehr geehrte Mitglieder des Prüfungsausschusses,

hiermit erhebe ich Beschwerde gegen die Organisation der Klausur vom 14. Mai. Mehrere Prüflinge, einschließlich meiner Person, erhielten die Aufgabenblätter mit zehnminütiger Verspätung, während die Bearbeitungszeit nicht entsprechend verlängert wurde. Dadurch entstand ein messbarer Nachteil gegenüber dem veröffentlichten Zeitfenster.

Darüber hinaus fehlte eine barrierefreie Sitzplatzregelung für eine Kommilitonin mit attestierter Sehbehinderung, obwohl der Nachteilsausgleich rechtzeitig beantragt worden war. Die Aufsicht verwies lediglich auf „organisatorische Engpässe“, ohne Protokollierung.

Ich beantrage daher: (1) eine neutrale Untersuchung des Ablaufs, (2) die Option einer Nachklausur unter fairen Bedingungen bzw. eine anteilige Bewertungskorrektur sowie (3) eine schriftliche Stellungnahme binnen drei Wochen. Als Belege füge ich Zeitstempel der digitalen Einlassliste sowie zwei eidesstattliche Versicherungen von Mitprüflingen bei.

Mir ist bewusst, dass Fehler vorkommen können; gerade deshalb erwarte ich eine transparente Aufarbeitung statt informeller Zusagen. Für Rückfragen stehe ich gerne zur Verfügung.

Mit freundlichen Grüßen
Leonie Hartmann
Matrikelnummer 219004""",
        """主旨：對寫作模組考試組織提出正式申訴

考試委員會委員您好，

謹此對 5 月 14 日考試組織提出申訴。含本人在內多名考生晚十分鐘才拿到題本，但作答時間未相對延長，相對已公布時段形成可測量的不利益。

此外，一位具證明之視力障礙同學雖已及時申請補償措施，現場卻無無障礙座位安排。監考僅稱「組織瓶頸」，未做紀錄。

因此請求：(1) 中立調查流程，(2) 在公平條件下補考或按比例調整評分，(3) 三週內書面回覆。附件為數位入場時間戳與兩份同學切結書。

我理解疏失可能發生；正因如此更期待透明處理，而非口頭承諾。如有疑問，樂意說明。

此致問候
Leonie Hartmann
學號 219004""",
        [n('hiermit erhebe ich Beschwerde','謹此提出申訴'),n('messbarer Nachteil','可測量的不利益'),n('Nachteilsausgleich','考試補償措施'),n('eidesstattliche Versicherungen','切結書／宣誓證明'),n('Aufarbeitung','徹底釐清／檢討'),n('binnen drei Wochen','三週內'),n('anteiliger','按比例的')],
        [p('hiermit erhebe ich Beschwerde gegen …','正式申訴套語','hiermit erhebe ich Einspruch gegen …'),p('obwohl … worden war','過去完成被動讓步','obwohl der Antrag gestellt worden war'),p('Ich beantrage daher: (1) … (2) …','條列請求','Ich beantrage daher: Akteneinsicht und Fristverlängerung.')],
        ['正式申訴信：事實→程序瑕疵→具體請求→證據。', '注意副句：während／obwohl／ohne zu。', '德檢郵件：語氣堅定但保持禮貌公式。'],
        ['教育', '行政', '正式郵件', '申訴'],
    ),
    item(
        'b2-53', "B2", 'notice', '環境',
        'Konsultation zur Verkehrswende', '交通轉型公聽',
        """Öffentliche Konsultation – Entwurf „Mobilität 2030“
Die Stadtverwaltung legt hiermit den Entwurf zur Verkehrswende zur Stellungnahme vor. Vorgesehen sind eine Ausweitung der Busspuren, Tempo 30 in Wohngebieten sowie gestaffelte Parkgebühren nach Fahrzeuggröße. Ziel ist eine Reduktion der Stickoxidwerte und eine fairere Verteilung des öffentlichen Raums.

Einwände und Alternativvorschläge können bis zum 30. September schriftlich oder über das Portal /mobilitaet eingereicht werden. Anonymisierte Beiträge werden veröffentlicht; personenbezogene Daten nur verarbeitet, soweit für Rückfragen erforderlich. Eine Bürgerversammlung findet am 12. September, 18 Uhr, im Rathaussaal statt; Gebärdensprachdolmetschung ist angemeldet.

Die Verwaltung weist darauf hin, dass nicht alle Wünsche umsetzbar sind, sofern Haushaltsmittel oder rechtliche Vorgaben entgegenstehen. Dennoch soll transparent dargelegt werden, welche Argumente in die Beschlussvorlage einfließen. Nach Auswertung folgt eine Synopse der Stellungnahmen.

Weitere Unterlagen: Wirkungsabschätzung, Lärmkartierung und Sozialverträglichkeitsprüfung liegen in den Bürgerämtern aus. Bei Fragen wenden Sie sich an mobilitaet@stadt.example.""",
        """公開諮詢－《移動 2030》草案
市政府特此提出交通轉型草案徵求意見。計畫包括擴大公車專用道、住宅區時速 30，以及依車型分級停車費。目標是降低氮氧化物並更公平分配公共空間。

異議與替代方案可於 9 月 30 日前書面或透過 /mobilitaet 提交。匿名化意見將公開；個資僅在回覆所需範圍處理。公聽會訂於 9 月 12 日 18 點市政廳大禮堂，已安排手語翻譯。

市府提醒：若預算或法規限制，並非所有願望都能實現。但仍應透明說明哪些論點納入決議提案。彙整後將公布意見對照摘要。

其他文件：影響評估、噪音地圖與社會可接受性評估置於市民辦公室供閱。問題請洽 mobilitaet@stadt.example。""",
        [n('Konsultation','諮詢／公聽程序'),n('gestaffelte Parkgebühren','分級停車費'),n('Stickoxidwerte','氮氧化物數值'),n('sofern … entgegenstehen','若……相牴觸'),n('Beschlussvorlage','決議提案'),n('Synopse','對照摘要'),n('Sozialverträglichkeitsprüfung','社會可接受性評估')],
        [p('zur Stellungnahme vorlegen','提出以供表態','den Entwurf zur Stellungnahme vorlegen'),p('soweit für … erforderlich','必要性限制','soweit für die Bearbeitung erforderlich'),p('sofern … entgegenstehen','法律／預算限制句','sofern Mittel entgegenstehen')],
        ['市政公告：措施→參與管道→限制誠實說明→文件。', '找出條件句 sofern／soweit。', '注意行政名詞化堆疊。'],
        ['環境', '市政', '公告', '參與'],
    ),
    item(
        'b2-54', "B2", 'dialogue', '媒體',
        'Interview: Verantwortung von Plattformen', '訪談：平台責任',
        """Moderatorin: Frau Dr. Keller, sollen Plattformen stärker für Inhalte haften?
Keller: Haftung darf nicht bedeuten, dass jedes Risiko auf Nutzerinnen abgewälzt wird. Wer Geschäftsmodelle auf Reichweite aufbaut, muss Moderationspflichten ernst nehmen.
Moderatorin: Kritiker fürchten Zensur.
Keller: Es geht nicht um Meinungsverbote, sondern um Kennzeichnung, Transparenz und nachvollziehbare Verfahren. Wer gelöscht wird, braucht eine Begründung und eine Beschwerdemöglichkeit.
Moderatorin: Reicht Freiwilligkeit?
Keller: Freiwillige Kodizes helfen als Einstieg, ersetzen jedoch keine Mindeststandards. Zum einen entstehen sonst Wettbewerbsnachteile für seriöse Anbieter; zum anderen bleiben Grauzonen bestehen.
Moderatorin: Was wäre Ihr Sofortmaßnahme-Paket?
Keller: Unabhängige Audits, klarere Altersgrenzen und Forschungsschnittstellen für Wissenschaftlerinnen – ohne private Chatverläufe pauschal zu öffnen.
Moderatorin: Und die Nutzerseite?
Keller: Medienkompetenz bleibt unverzichtbar. Dennoch wäre es verkürzt, strukturelle Anreize allein durch Appelle an Individuen zu korrigieren.""",
        """主持人：Keller 博士，平台是否應為內容負更大責任？
Keller：責任不該意味把所有風險轉嫁使用者。誰靠觸及率建立商業模式，就必須認真看待審核義務。
主持人：批評者擔心審查。
Keller：重點不是禁止言論，而是標示、透明與可追溯程序。被刪文者需要理由與申訴管道。
主持人：自願夠嗎？
Keller：自願守則可作起點，但不能取代最低標準。一方面認真業者會吃虧；另一方面灰色地帶仍在。
主持人：您的立即措施清單？
Keller：獨立稽核、更清楚的年齡門檻，以及給研究者的介面——而非概括打開私人對話。
主持人：使用者端呢？
Keller：媒體素養仍不可或缺。但若只靠呼籲個人來修正結構誘因，就過於簡化。""",
        [n('haften','負責／承擔責任'),n('abgewälzt','被轉嫁'),n('nachvollziehbare Verfahren','可追溯的程序'),n('Kodizes','守則／行為準則'),n('Audits','稽核'),n('pauschal','概括地／一刀切地'),n('verkürzt','過於簡化的')],
        [p('Zum einen …; zum anderen …','雙面論證','Zum einen spart man Zeit; zum anderen steigt der Druck.'),p('Dennoch wäre es verkürzt, …','反駁簡化論','Dennoch wäre es verkürzt, nur Kosten zu sehen.'),p('Es geht nicht um A, sondern um B','澄清焦點','Es geht nicht um Strafe, sondern um Prävention.')],
        ['訪談體：問答中抓論點與轉折。', '標出讓步：Dennoch／reichen … nicht。', '區分『審查恐懼』與『程序透明』兩條線。'],
        ['媒體', '科技', '倫理', '訪談'],
    ),
    item(
        'b2-55', "B2", 'story', '住房',
        'Bezahlbarer Wohnraum jenseits von Appellen', '呼籲之外的可負擔住房',
        """In vielen Ballungsräumen übersteigen Mietsteigerungen die Einkommensentwicklung. Wer neu zuzieht, konkurriert mit kapitalstarken Investoren um knappen Wohnraum. Symbolische Mietendeckel ohne Neubau und ohne Schutz vor Umwandlung in Eigentum greifen oft zu kurz.

Zugleich ist nicht jeder Neubau automatisch sozial: Luxusprojekte können Bodenpreise weiter anheizen. Wirksamer wären Mischkalkulationen, bei denen ein verbindlicher Anteil dauerhaft gebunden bleibt, sowie die Aktivierung von Leerstand. Kommunen brauchen dafür Planungsrecht und Personal, nicht nur Pressemitteilungen.

Gegner warnen vor Eingriffen in Eigentumsrechte und vor ausbleibenden Investitionen. Dieses Argument ist ernst zu nehmen, darf jedoch nicht dazu führen, dass Wohnen ausschließlich als Renditeobjekt gedacht wird. Eine Stadt funktioniert nur, wenn Pflegekräfte, Lernende und Dienstleistungsbeschäftigte auch tatsächlich wohnen können.

Insofern verschiebt sich die Debatte von moralischen Appellen hin zu Steuerungsinstrumenten: Bodenpolitik, Genossenschaften und transparente Vergabe. Es bleibt abzuwarten, inwiefern neue Bündnisse zwischen Ländern und Kommunen messbare Entlastung bringen.""",
        """許多都會區租金漲幅超過收入成長。新移入者須與資本雄厚投資人爭奪稀缺住房。沒有新建與防止改為產權住宅配套的象徵性租金上限，往往力有未逮。

同時，新建案也不自動具社會性：豪宅可能繼續推高地價。較有效的是混合核算，讓一定比例長期受拘束，並活化空屋。地方政府需要規劃權與人力，而不只是新聞稿。

反對者警告干預所有權與投資卻步。這論點必須認真看待，但不能因此把居住只想成報酬標的。若護理人員、學生與服務業勞工實際上住不起，城市就無法運轉。

因此辯論從道德呼籲轉向政策工具：土地政策、合作社與透明分配。邦與市的新聯盟能否帶來可測量減壓，仍有待觀察。""",
        [n('Ballungsräumen','都會密集區'),n('Mietendeckel','租金上限'),n('greifen … zu kurz','力有未逮／不夠用'),n('anheizen','推高／煽動'),n('Leerstand','空屋／空置'),n('Renditeobjekt','報酬標的'),n('Steuerungsinstrumenten','調控工具')],
        [p('ohne A und ohne B greifen … zu kurz','指出配套不足','ohne Kontrolle greifen Appelle zu kurz'),p('Dieses Argument ist ernst zu nehmen, darf jedoch nicht …','承認後限制','Das Risiko ist ernst, darf jedoch nicht lähmen.'),p('verschiebt sich die Debatte von A hin zu B','論點轉向','verschiebt sich die Debatte von Schuld hin zu Struktur')],
        ['住房論述：數據現象→政策缺陷→反論→工具轉向。', '找出『承認對方論點』的句子。', '名詞化：Umwandlung、Vergabe、Entlastung。'],
        ['住房', '社會', '政策', '論述'],
    ),
    item(
        'b2-56', "B2", 'email', '職場',
        'Konfliktgespräch dokumentieren', '紀錄衝突面談',
        """Betreff: Dokumentation des Klärungsgesprächs vom 3. Juni

Sehr geehrte Frau Sandberg,

anbei übersende ich die vereinbarte Zusammenfassung unseres Gesprächs zu den wiederholten Fristüberschreitungen im Projekt „Nord“. Ziel ist eine gemeinsame Faktenbasis, keine einseitige Schuldzuweisung.

Festgehalten wurde: (1) Liefertermine wurden in drei Fällen ohne frühzeitige Eskalation überschritten; (2) Parallelaufgaben aus dem Tagesgeschäft waren unzureichend priorisiert; (3) eine wöchentliche Kurzabstimmung mittwochs 9 Uhr wird verbindlich eingeführt. Sie haben zugesagt, Engpässe spätestens 48 Stunden vorher zu melden; ich sichere zu, Prioritäten schriftlich zu bestätigen.

Sollten Sie Korrekturen am Protokoll haben, bitte ich um Rückmeldung bis Freitag 12 Uhr. Andernfalls gilt die Fassung als abgestimmt und wird der Personalakte des Projekts beigelegt. Eine erneute Auswertung erfolgt in vier Wochen.

Ich danke für die sachliche Gesprächsführung und gehe davon aus, dass wir die Zusammenarbeit damit stabilisieren.

Mit freundlichen Grüßen
Marc Eller
Projektleitung""",
        """主旨：6 月 3 日澄清面談紀錄

Sandberg 女士您好，

附上我們就「Nord」專案多次逾期之談話摘要。目的是建立共同事實基礎，而非單方歸咎。

紀錄要點：(1) 三次交付未及早升級呈報即逾期；(2) 日常並行任務優先順序不足；(3) 週三 9 點短會改為具拘束力。您承諾最晚提前 48 小時通報瓶頸；我承諾書面確認優先順序。

若對紀錄有修正，請於週五 12 點前回覆；否則視同定稿並歸入專案人事檔。四週後再評估。

感謝您務實的談話態度，並預期藉此穩定合作。

此致問候
Marc Eller
專案主管""",
        [n('Fristüberschreitungen','逾期'),n('Schuldzuweisung','歸咎'),n('Eskalation','問題升級呈報'),n('verbindlich eingeführt','具拘束力地導入'),n('beigelegt','附入／歸檔'),n('sachliche Gesprächsführung','務實／就事論事的談話'),n('abgestimmt','達成一致的')],
        [p('Ziel ist A, keine B','澄清目的','Ziel ist Klärung, keine Eskalation.'),p('Sollten Sie …, bitte ich um …','條件客氣請求','Sollten Sie Fragen haben, bitte ich um Nachricht.'),p('Andernfalls gilt … als …','預設後果','Andernfalls gilt der Antrag als zurückgezogen.')],
        ['職場正式信：摘要→約定→確認期限→追蹤。', '注意被動與名詞化：wurde festgehalten。', '區分『紀錄』與『指控』語氣。'],
        ['職場', '衝突', '正式郵件', '程序'],
    ),
    item(
        'b2-57', "B2", 'story', '健康',
        'Psychische Belastung am Arbeitsplatz', '職場心理負荷',
        """Psychische Erkrankungen gehören zu den häufigsten Gründen für längere Fehlzeiten. Dennoch wird Überlastung in manchen Branchen weiterhin als individuelles Versagen gedeutet. Wer früh Hilfe sucht, riskiert Stigmatisierung; wer schweigt, riskiert Chronifizierung.

Betriebliche Prävention müsste deshalb früher ansetzen: realistische Zielvereinbarungen, erholsame Pausenräume und Führungskräfte, die Überstunden nicht still belohnen. Externe Beratungsangebote helfen, ersetzen jedoch keine Organisationsentwicklung. Auch Beschäftigte mit hoher Motivation brauchen Schutz vor Dauererreichbarkeit.

Skeptiker argumentieren, Unternehmen seien keine Therapeuten. Das ist richtig – und gerade deshalb brauchen sie klare Schnittstellen zu professioneller Unterstützung sowie vertrauliche Verfahren. Prävention ist keine Softkompetenz-Dekoration, sondern Teil der Fürsorgepflicht.

Insofern verbindet sich Gesundheitsschutz mit Produktivität auf längere Sicht. Es bleibt abzuwarten, inwiefern gesetzliche Berichtspflichten und Tarifverträge psychische Belastungen ebenso ernst nehmen wie klassische Unfallrisiken. Wer nur Appelle veröffentlicht, verändert wenig.""",
        """心理疾患已是長期病假的常見原因之一。但在某些行業，過勞仍被解讀成個人失敗。早求助者冒著污名化風險；沉默者則冒著慢性化風險。

因此企業預防必須更早介入：務實目標約定、可恢復的休息空間，以及不暗中獎勵加班的主管。外部諮詢有幫助，但不能取代組織發展。高動機員工也需要免於持續待命的保護。

懷疑者說企業不是治療師。這話沒錯——正因如此更需要與專業支援的清晰介面與保密程序。預防不是軟實力裝飾，而是照顧義務的一環。

因此健康保護長期而言與生產力相連。法定報告義務與團體協約能否像看待傳統工安一樣認真看待心理負荷，仍有待觀察。只發呼籲，改變很少。""",
        [n('Fehlzeiten','缺勤／病假時數'),n('Stigmatisierung','污名化'),n('Chronifizierung','慢性化'),n('Zielvereinbarungen','目標約定'),n('Fürsorgepflicht','照顧義務'),n('Tarifverträge','團體協約'),n('Dauererreichbarkeit','持續可聯繫狀態')],
        [p('Wer A, riskiert X; wer B, riskiert Y','雙風險結構','Wer fragt, riskiert Kritik; wer schweigt, riskiert Fehler.'),p('Das ist richtig – und gerade deshalb …','承認後推進','Das ist teuer – und gerade deshalb müssen wir planen.'),p('Prävention ist keine A, sondern B','重新定義','Flexibilität ist keine Gabe, sondern Verhandlung.')],
        ['健康論述：數據→污名兩難→組織解方→義務框架。', '抓住『承認懷疑者』再推進的轉折。', '對照個人化 vs 結構性解釋。'],
        ['健康', '職場', '社會', '論述'],
    ),
    item(
        'b2-58', "B2", 'notice', '法律／規定',
        'Hinweis zu Hinweisgeberinnen', '吹哨者保護提示',
        """Interne Richtlinie – Schutz von Hinweisgeberinnen und Hinweisgebern
Personen, die im guten Glauben Verstöße gegen Recht oder interne Compliance melden, dürfen deswegen keine Benachteiligung erfahren. Meldungen können über das vertrauliche Portal /hinweis oder postalisch an die Ombudsstelle erfolgen. Anonyme Hinweise werden geprüft, sofern sie hinreichend konkret sind.

Die Bearbeitung erfolgt unabhängig von betroffenen Fachbereichen. Rückmeldungen zum Verfahrensstand erfolgen in der Regel innerhalb von drei Monaten, soweit keine gesetzlichen Geheimhaltungspflichten entgegenstehen. Mutwillige Falschmeldungen können arbeitsrechtliche Folgen haben; gutgläubige Irrtümer hingegen nicht.

Führungskräfte sind verpflichtet, Vergeltungsmaßnahmen zu unterbinden und Verdachtsfälle unverzüglich weiterzuleiten. Externe Meldestellen bleiben parallel nutzbar; interne Wege ersetzen keine gesetzlichen Rechte. Schulungen zur Richtlinie finden quartalsweise statt.

Fragen richten Sie bitte an compliance@firma.example. Diese Fassung ersetzt die Richtlinie vom Januar und tritt am 1. August in Kraft.""",
        """內部準則－吹哨者保護
善意舉報違法或內部法遵違規者，不得因此受不利益。可透過保密入口 /hinweis 或郵寄監察辦公室舉報。匿名檢舉若夠具體仍會審查。

處理獨立於涉案單位。除非有法定保密義務相牴觸，原則上三個月內回報進度。惡意不實檢舉可能有勞動法後果；善意誤解則否。

主管有義務遏止報復並立即上呈嫌疑案件。外部檢舉管道仍可並行；內部途徑不取代法定權利。準則培訓每季舉行。

問題請洽 compliance@firma.example。本版取代一月準則，8 月 1 日生效。""",
        [n('Hinweisgeberinnen','吹哨者（陰性複數）'),n('Benachteiligung','不利益／歧視待遇'),n('Ombudsstelle','監察／申訴辦公室'),n('hinreichend konkret','足夠具體'),n('Mutwillige Falschmeldungen','惡意不實檢舉'),n('Vergeltungsmaßnahmen','報復措施'),n('tritt … in Kraft','生效')],
        [p('dürfen deswegen keine … erfahren','保護條款','dürfen keine Nachteile erfahren'),p('sofern sie … sind','條件限定','sofern sie belegt sind'),p('soweit keine … entgegenstehen','法律保留','soweit keine Fristen entgegenstehen')],
        ['法遵公告：保護→管道→程序→例外→生效。', '區分 gutgläubig vs mutwillig。', '注意被動：werden geprüft／erfolgen。'],
        ['法律', '職場', '合規', '公告'],
    ),
    item(
        'b2-59', "B2", 'story', '文化',
        'Übersetzung als kulturelle Entscheidung', '翻譯作為文化決定',
        """Übersetzen gilt oberflächlich als technischer Transfer von Wörtern. Tatsächlich handelt es sich um fortlaufende Entscheidungen: Welche Anredeebene trifft den Ton? Welche Metapher bleibt verständlich, ohne den Ausgangstext zu verfälschen? Besonders bei Behördentexten und Literatur zeigt sich, dass scheinbar neutrale Formulierungen Werte transportieren.

Maschinelle Systeme beschleunigen Entwürfe, ersetzen jedoch kein Kontextwissen über Register, Irony oder rechtliche Bindungswirkung. Wer Warnhinweise falsch glättet, erzeugt Haftungsrisiken; wer literarische Mehrdeutigkeit tilgt, verliert Kunst. Deshalb fordern Berufsverbände sichtbare Verantwortung: Menschen prüfen kritische Passagen.

Gegner einer strengen Regulierung betonen Innovationsgeschwindigkeit. Geschwindigkeit ohne Qualitätsstandards verlagert Kosten jedoch auf Leserinnen, Patientinnen oder Antragstellende. Eine pragmatische Linie verbindet Automatisierung in Routinefällen mit verbindlicher Fachrevision bei Hochrisiko-Texten.

Insofern ist Sprachmittlung Infrastruktur, nicht bloß Dienstleistung. Es bleibt abzuwarten, inwiefern Ausbildung, Honorare und Transparenzregeln mit dem technischen Wandel Schritt halten.""",
        """翻譯表面像是詞語的技術轉移。實際上是一連串決定：哪個稱呼層級對味？哪種隱喻仍可懂又不扭曲原文？尤其在公文與文學中，看似中性的措辭也承載價值。

機器系統能加速草稿，卻取代不了語域、反諷或法律拘束力的語境知識。警告用語被錯誤「磨平」會產生責任風險；刪去文學歧義則失去藝術。因此專業協會要求可見的責任：關鍵段落由人審核。

反對嚴格管制者強調創新速度。但沒有品質標準的速度，會把成本轉嫁給讀者、病患或申請人。務實路線是：例行文本自動化，高風險文本強制專業覆核。

因此語言中介是基礎設施，而不只是服務。培養、稿費與透明規則能否跟上技術變遷，仍有待觀察。""",
        [n('handelt es sich um','這指的是……'),n('Register','語域／文體層級'),n('Bindungswirkung','拘束效力'),n('glättet','磨平／圓滑化'),n('tilgt','刪除／抹去'),n('Fachrevision','專業覆核'),n('Sprachmittlung','語言中介')],
        [p('handelt es sich um …','定義主題','Dabei handelt es sich um ein Missverständnis.'),p('Wer A, erzeugt B; wer C, verliert D','對照後果','Wer spart, riskiert Qualität.'),p('Eine pragmatische Linie verbindet A mit B','折衷方案','Eine Linie verbindet Tempo mit Kontrolle.')],
        ['文化／科技論述：表面定義→風險→反論→折衷。', '標出對偶句 Wer… / Wer…。', '注意名詞化：Bindungswirkung、Fachrevision。'],
        ['文化', '科技', '語言', '論述'],
    ),
    item(
        'b2-60', "B2", 'dialogue', '經濟',
        'Podium: Lieferketten und Verantwortung', '論壇：供應鏈與責任',
        """Moderator: Herr Okonjo, genügen freiwillige Lieferkettenstandards?
Okonjo: Freiwilligkeit reicht selten, wenn Preisdruck systematisch nach unten durchgereicht wird. Ohne sorgfältige Prüfung bleiben Risiken unsichtbar.
Unternehmerin Lang: Strenge Gesetze belasten vor allem kleinere Importeure.
Okonjo: Dann braucht es gestufte Pflichten und Unterstützung bei Audits, nicht ein Alles-oder-nichts. Zum einen schützen klare Regeln seriöse Firmen vor Dumping; zum anderen brauchen KMU praktikable Tools.
Lang: Und wenn Produzentinnen die Auflagen nicht erfüllen können?
Okonjo: Dann ist Ausstieg nicht die einzige Antwort. Man kann Übergangsfristen, Schulungen und gemeinsame Investitionen vereinbaren – allerdings mit messbaren Meilensteinen.
Moderator: Wer kontrolliert die Kontrolleure?
Okonjo: Unabhängigkeit, Rotationsregeln und öffentliche Summaries reduzieren Interessenkonflikte, ersetzen aber nicht zivilgesellschaftliche Beobachtung.
Lang: Das klingt teuer.
Okonjo: Teurer ist langfristig ein Reputationsschaden nach einem Skandal. Verantwortung ist Teil der Kalkulation, nicht ihr Gegenteil.""",
        """主持人：Okonjo 先生，自願供應鏈標準夠嗎？
Okonjo：若價格壓力被系統性往下轉嫁，自願往往不夠。沒有審慎檢查，風險就看不見。
企業家 Lang：嚴格法律尤其負擔較小進口商。
Okonjo：那需要分級義務與稽核支持，而非全有全無。一方面清楚規則保護認真公司免於傾銷式競爭；另一方面中小企業需要可用工具。
Lang：若生產者做不到規定呢？
Okonjo：退出不是唯一答案。可以談過渡期、培訓與共同投資——但要有可測量里程碑。
主持人：誰監督監督者？
Okonjo：獨立性、輪替與公開摘要可降低利益衝突，但仍不能取代公民社會觀察。
Lang：聽起來很貴。
Okonjo：醜聞後的商譽損害長期更貴。責任是成本計算的一部分，不是其對立面。""",
        [n('durchgereicht','被轉嫁下去'),n('gestufte Pflichten','分級義務'),n('KMU','中小企業'),n('Meilensteine','里程碑'),n('Interessenkonflikte','利益衝突'),n('Reputationsschaden','商譽損害'),n('Kalkulation','成本精算')],
        [p('Zum einen …; zum anderen …','雙面論證','Zum einen schützt es; zum anderen kostet es.'),p('nicht die einzige Antwort','拒絕單一解','Ausstieg ist nicht die einzige Antwort.'),p('A ist Teil von B, nicht ihr Gegenteil','重新框定','Sicherheit ist Teil der Qualität, nicht ihr Gegenteil.')],
        ['論壇對話：抓各方立場與折衷提案。', '注意條件句 Wenn… Dann…。', '德檢：辨識『成本』論與『風險』論。'],
        ['經濟', '倫理', '全球化', '對話'],
    ),
    item(
        'b2-61', "B2", 'story', '教育',
        'Noten und Motivation in der Diskussion', '討論中的分數與動機',
        """Noten strukturieren Lernwege, erzeugen aber auch Vergleichsdruck. Wer früh schlechte Rückmeldungen erhält, kann Kompetenzen unterschätzen, obwohl Entwicklung möglich wäre. Alternative Formate wie Portfolios und formative Rückmeldungen versprechen mehr Lernorientierung, verlangen jedoch Zeit und geschulte Lehrkräfte.

Eltern und Hochschulen fordern weiterhin vergleichbare Zertifikate. Ohne gemeinsame Standards droht Unübersichtlichkeit; mit starren Skalen droht Verengung auf Prüfbares. Eine differenzierte Praxis kombiniert verbindliche Kernkompetenzen mit narrativen Einschätzungen.

Kritikerinnen warnen, Soft-Assessment werde ungerecht, weil subjektiv. Subjektivität verschwindet jedoch nicht hinter Zahlen – sie wird nur unsichtbar. Transparente Rubriken und Zweitkorrekturen können Willkür begrenzen, ohne Komplexität zu leugnen.

Insofern ist die Frage weniger „Noten ja oder nein“ als „welche Informationen brauchen Lernende zum Weiterarbeiten“. Es bleibt abzuwarten, inwiefern Schulen Ressourcen erhalten, um Rückmeldung jenseits von Punktwerten professionell zu gestalten.""",
        """分數能結構化學習路徑，也製造比較壓力。很早收到負評者可能低估自己能力，儘管仍可發展。學習歷程檔與形成性回饋等替代形式承諾更以學習為導向，但需要時間與受過訓練的教師。

家長與大學仍要求可比較的證明。沒有共同標準會混亂；僵硬量表則把焦點窄化到可考之物。較細緻的做法是把具拘束力的核心能力與敘事評量結合。

批評者警告軟性評量因主觀而不公。但主觀性不會因數字而消失——只是被藏起來。透明量規與複評可限制恣意，同時不否認複雜性。

因此問題較少是「要不要分數」，而是「學習者繼續前進需要哪些資訊」。學校能否獲得資源，把回饋做到分數以外的專業水準，仍有待觀察。""",
        [n('Vergleichsdruck','比較壓力'),n('formative Rückmeldungen','形成性回饋'),n('Unübersichtlichkeit','混亂難辨'),n('Verengung','窄化'),n('Rubriken','評分量規'),n('Willkür','恣意'),n('Punktwerten','點數／分數值')],
        [p('obwohl … wäre','讓步虛擬','obwohl Hilfe möglich wäre'),p('Ohne A droht X; mit B droht Y','兩難結構','Ohne Regeln droht Chaos; mit Härte droht Angst.'),p('weniger A als B','重新提問','weniger Schuld als Struktur')],
        ['教育論述：功能→代價→替代→反論→重設問題。', '找出『數字並非中性』的論點。', '標出 Insofern／Es bleibt abzuwarten。'],
        ['教育', '評量', '論述', '社會'],
    ),
    item(
        'b2-62', "B2", 'email', '消費',
        'Aufforderung zur Nacherfüllung', '請求後履行（瑕疵補救）',
        """Betreff: Nacherfüllung zur Bestellung 441208 – defektes Gerät

Sehr geehrte Damen und Herren,

am 2. April erwarb ich bei Ihnen eine Waschmaschine (Modell AquaPro 8), die innerhalb der Gewährleistungsfrist einen irreparablen Pumpenschaden aufweist. Eine Reparatur vor Ort am 20. Mai blieb erfolglos; das Protokoll des Technikers sowie Fotos des Fehlercodes liegen bei. Bereits am 21. Mai habe ich Ihren Support telefonisch informiert und eine Ticketnummer erhalten, ohne dass seither ein verbindlicher Ersatztermin genannt wurde.

Hiermit fordere ich Sie zur Nacherfüllung auf, primär durch Lieferung einer mangelfreien Ersatzmaschine binnen 14 Tagen ab Zugang dieses Schreibens. Hilfsweise begehre ich Minderung bzw. Rücktritt vom Kaufvertrag einschließlich Erstattung der Anfahrtskosten der erfolglosen Reparatur. Eine weitere Verzögerung ist mir nicht zumutbar, da die Haushaltsführung erheblich beeinträchtigt ist und externe Wäschereikosten entstehen.

Bitte bestätigen Sie den Eingang und teilen Sie den Liefertermin verbindlich mit. Sollte keine fristgerechte Reaktion erfolgen, behalte ich mir weitere rechtliche Schritte vor, einschließlich der Einschaltung der Verbraucherzentrale und der Geltendmachung von Verzugsschäden.

Mit freundlichen Grüßen
Karim Haddad""",
        """主旨：訂單 441208 後履行請求－故障設備

敬啟者：

我於 4 月 2 日購買洗衣機（型號 AquaPro 8），在保固期內出現無法修復的水泵損壞。5 月 20 日到府維修未果；技師紀錄與錯誤代碼照片附上。5 月 21 日已電話告知客服並取得工單編號，其後仍未獲具拘束力的換機時程。

謹此請求後履行，原則上於本函送達後 14 日內交付無瑕疵替換機。退而求其次請求減價或解除買賣契約，並請退還無效維修的出勤費用。家務已明顯受影響且產生外部洗衣費用，再拖延對我而言不可期待。

請確認收悉並具拘束力地告知送達日期。若未如期回應，我保留進一步法律行動，包括向消費者中心求助及主張遲延損害。

此致問候
Karim Haddad""",
        [n('Nacherfüllung','後履行／瑕疵補救'),n('Gewährleistungsfrist','瑕疵擔保期間'),n('mangelfreien','無瑕疵的'),n('Hilfsweise','退而求其次／備位主張'),n('nicht zumutbar','不可期待／無法再忍受'),n('Minderung','減價'),n('Verbraucherzentrale','消費者中心')],
        [p('Hiermit fordere ich Sie zur … auf','正式催告','Hiermit fordere ich Sie zur Zahlung auf.'),p('Hilfsweise begehre ich …','備位請求','Hilfsweise begehre ich Schadensersatz.'),p('Sollte keine … erfolgen, behalte ich mir … vor','預告後果','Sollte keine Antwort erfolgen, behalte ich mir Klage vor.')],
        ['消費爭議信：事實→請求層級→期限→法律保留。', '分清 primär／hilfsweise。', '語氣強硬但公式完整。'],
        ['消費', '法律', '正式郵件', '契約'],
    ),
    item(
        'b2-63', "B2", 'notice', '交通',
        'Sperrung und Ersatzkonzept', '封閉與替代方案',
        """Verkehrsmeldung – Vollsperrung Konrad-Adenauer-Brücke
Wegen Brückenprüfung ist die Konrad-Adenauer-Brücke vom 8. bis 18. Oktober in beiden Richtungen gesperrt. Der motorisierte Individualverkehr wird über die Südumfahrung geleitet; mit erheblichen Reisezeitverlusten ist zu rechnen. Schwertransporte benötigen Sondergenehmigungen der Straßenverkehrsbehörde.

Für den ÖPNV gilt ein Schienenersatzverkehr zwischen Hauptbahnhof und Westkreuz. Taktverdichtung erfolgt in der Hauptverkehrszeit; Barrierefreiheit der Ersatzbusse ist weitgehend sichergestellt, vereinzelte Fahrten jedoch nur mit Voranmeldung. Radverkehr nutzt die ausgewiesene Behelfsfurt unterhalb der Brücke; Fußverkehr die Treppenanlage Ost mit Aufzugbetrieb 6–22 Uhr.

Anwohnerparken im Umleitungsbereich wird temporär ausgeweitet. Schadensersatz wegen Lieferverzögerungen ist beim Tiefbauamt innerhalb von sechs Wochen zu beantragen. Aktuelle Störungen erscheinen im Live-Ticker /verkehr. Wir bitten um Verständnis und frühzeitige Fahrtplanung.""",
        """交通訊息－Konrad-Adenauer 橋全面封閉
因橋樑檢測，該橋 10 月 8 至 18 日雙向封閉。汽機車改循南繞道；請預期明顯耗時增加。重車須向道路交通機關申請特別許可。

大眾運輸於中央車站與西十字站間實施軌道替代公車。尖峰加密班次；替代公車大致無障礙，少數班次需預約。單車行經橋下指定便道；行人走東側階梯，電梯 6–22 點運作。

改道區域臨停將臨時擴大。因延誤求償須於六週內向土木工程處提出。即時障礙見 /verkehr。請見諒並提早規劃行程。""",
        [n('Vollsperrung','全面封閉'),n('Individualverkehr','私人運具交通'),n('Reisezeitverlusten','旅途耗時損失'),n('Schienenersatzverkehr','軌道替代交通'),n('Taktverdichtung','班距加密'),n('Behelfsfurt','臨時便道'),n('Tiefbauamt','土木工程處')],
        [p('Mit … ist zu rechnen','預期後果','Mit Wartezeiten ist zu rechnen.'),p('gilt ein …','適用特別規定','gilt ein Ersatzfahrplan'),p('ist … zu beantragen','申請義務','ist schriftlich zu beantragen')],
        ['長公告：封閉→汽機車→大眾運→單車行人→求償。', '抓行政被動與 zu-不定式。', '對照『largely／vereinzelt』這類限定詞。'],
        ['交通', '市政', '公告', '基礎設施'],
    ),
    item(
        'b2-64', "B2", 'story', '科技',
        'Open Data und Machtasymmetrien', '開放資料與權力不對稱',
        """Open-Data-Initiativen versprechen Transparenz und Innovation. Behörden veröffentlichen Fahrpläne, Umweltwerte und Haushaltszahlen, damit Zivilgesellschaft und Start-ups darauf aufbauen können. Doch Rohdaten allein schaffen keine gleiche Augenhöhe: Wer über Analysekapazität, Rechtsberatung und Recheninfrastruktur verfügt, nutzt Freigaben oft wirksamer als ehrenamtliche Gruppen.

Zudem entscheiden Metadaten und Schnittstellen darüber, welche Fragen überhaupt stellbar sind. Unvollständige Dokumentation oder verzögerte Updates erzeugen Scheintransparenz. Deshalb fordern Fachleute verpflichtende Qualitätsstandards, nachhaltige Finanzierung und Schulungen für nutzende Organisationen.

Unternehmen argumentieren mit Geschäftsgeheimnissen, Verwaltungen mit Sicherheitsrisiken. Beides kann legitim sein, darf jedoch nicht pauschal als Ausrede dienen. Abwägungen sollten begründet und periodisch überprüft werden.

Insofern ist Open Data weniger ein Schalter als ein dauerhafter Institutionalisierungsprozess. Es bleibt abzuwarten, inwiefern gesetzliche Mindestkataloge tatsächlich Machtasymmetrien verringern – und nicht nur ohnehin privilegierte Akteure weiter stärken.""",
        """開放資料倡議承諾透明與創新。機關公開班表、環境數值與預算，讓公民社會與新創能據此開發。但光有原始資料並不造就對等：擁有分析能力、法律諮詢與運算基礎設施者，往往比志工團體更能有效利用開放。

此外，詮釋資料與介面決定了哪些問題根本問得出來。文件不全或更新延遲會製造假透明。因此專家要求強制品質標準、永續經費與對使用組織的培訓。

企業談營業秘密，行政談安全風險。兩者都可能正當，但不能一概作為藉口。權衡應說明理由並定期檢視。

因此開放資料比較不是一個開關，而是持續制度化過程。法定最低清單能否真正降低權力不對稱——而非只讓原本有優勢者更強——仍有待觀察。""",
        [n('Augenhöhe','對等／平視'),n('Metadaten','詮釋資料'),n('Scheintransparenz','假透明'),n('pauschal','一概地'),n('Abwägungen','權衡'),n('Institutionalisierungsprozess','制度化過程'),n('Machtasymmetrien','權力不對稱')],
        [p('weniger A als B','重新定義','weniger Produkt als Prozess'),p('darf jedoch nicht pauschal als … dienen','限制藉口','darf nicht pauschal als Sicherheitsargument dienen'),p('Es bleibt abzuwarten, inwiefern … – und nicht nur …','雙向開放結論','Es bleibt abzuwarten, inwiefern Hilfe trifft – und nicht nur Symbolik bleibt.')],
        ['科技治理文：承諾→不對稱→品質→權衡→制度。', '找出對『假透明』的批判。', '注意破折號延伸結論。'],
        ['科技', '治理', '透明', '論述'],
    ),
    item(
        'b2-65', "B2", 'dialogue', '移民／融合',
        'Gespräch in der Integrationsberatung', '融合諮詢對話',
        """Beraterin: Sie möchten die Anerkennung Ihrer Pflegeausbildung beschleunigen?
Klientin: Ja. Ich arbeite seit einem Jahr als Hilfskraft, obwohl ich im Herkunftsland examiniert bin.
Beraterin: Dafür brauchen wir beglaubigte Übersetzungen, den Lehrplanvergleich und ggf. eine Kenntnisprüfung. Die Wartezeiten sind derzeit lang.
Klientin: Kann ich parallel einen Sprachkurs B2 berufsbezogen belegen?
Beraterin: Das ist sinnvoll und wird teilweise gefördert. Allerdings müssen Kurszeiten mit Schichtplänen abgestimmt werden; wir können eine Bescheinigung für den Arbeitgeber formulieren.
Klientin: Und wenn die Anerkennung länger dauert als erwartet?
Beraterin: Dann prüfen wir Zwischenqualifikationen, damit Ihre Erfahrung nicht entwertet wird. Wichtig ist, Fristen im Blick zu behalten und Unterlagen vollständig einzureichen.
Klientin: Ich habe Angst vor bürokratischen Fehlern.
Beraterin: Deshalb machen wir eine Checkliste und einen Termin zur Zwischenkontrolle. Sie müssen das nicht allein navigieren.""",
        """顧問：您想加快護理學歷認證？
案主：對。我已當一年助理，但在原籍國已取得考試資格。
顧問：需要公證翻譯、課程對照，必要時還有專業知識考試。目前等候很久。
案主：我可以同時修職業導向 B2 語言課嗎？
顧問：合理，且部分有補助。但課程時間須與輪班協調；我們可幫開給雇主的證明。
案主：若認證比預期更久？
顧問：那就評估中間資格，避免您的經驗被貶值。重要的是盯緊期限並備齊文件。
案主：我怕行政出錯。
顧問：所以我們做清單與期中檢查。您不必一個人摸索。""",
        [n('Anerkennung','學歷／證照認證'),n('beglaubigte Übersetzungen','公證翻譯'),n('Kenntnisprüfung','專業知識考試'),n('berufsbezogen','職業導向的'),n('Zwischenqualifikationen','中間資格'),n('entwertet','被貶值'),n('navigieren','摸索前進／導航')],
        [p('obwohl ich … bin','讓步現實','obwohl ich qualifiziert bin'),p('Das ist sinnvoll und wird teilweise gefördert','肯定＋條件','Das ist möglich und wird teilweise erstattet.'),p('damit … nicht …','目的防杜','damit Erfahrung nicht verloren geht')],
        ['諮詢對話：目標→文件→並行策略→風險管理。', '注意行政程序詞：Anerkennung、Fristen。', '語氣支持但不給虛假保證。'],
        ['移民', '勞動', '行政', '對話'],
    ),
    item(
        'b2-66', "B2", 'story', '環境',
        'Recyclingquoten und echte Kreisläufe', '回收率與真正循環',
        """Hohe Recyclingquoten gelten als Beleg gelungener Umweltpolitik. Doch Quoten allein sagen wenig, wenn gesammelte Kunststoffe qualitativ minderwertig sind oder exportiert werden, ohne dass Weiterverarbeitung nachvollziehbar bleibt. Ein Kreislauf entsteht erst, wenn Produktdesign, Sammlung und Absatz von Rezyklaten zusammengeplant werden.

Hersteller verweisen auf Konsumentinnen, die falsch trennen; Kommunen auf fehlende Anlagen; Anlagenbetreiber auf schwankende Rohstoffpreise. Jede Teilwahrheit verschiebt Verantwortung. Verbindliche Rezyklatanteile, Ökodesign-Vorgaben und transparente Exportkontrollen wären kohärenter als Appelle zum „richtigen“ Mülltonnenverhalten.

Skeptiker fürchten Kostensteigerungen und Wettbewerbsnachteile. Ohne Internalisierung ökologischer Kosten bleiben jedoch Billigprodukte mit kurzer Lebensdauer systematisch im Vorteil. Politik muss daher Übergangsfristen und Förderungen so staffeln, dass Innovation möglich bleibt.

Insofern ist Kreislaufwirtschaft Industriepolitik plus Verbraucherinformation – nicht bloß Moral. Es bleibt abzuwarten, inwiefern neue EU-Vorgaben Messbarkeit verbessern, statt nur Berichtsaufwand zu erzeugen.""",
        """高回收率常被當作環境政策成功的證據。但若蒐集的塑膠品質差，或出口後再處理無法追溯，光看比率意義有限。唯有產品設計、回收與再生料銷路一起規劃，循環才成立。

製造商指向消費者分錯類；地方政府指向設備不足；處理業者指向原料價格波動。每個片面真相都在轉移責任。強制再生料比例、生態設計規範與透明出口管制，比呼籲「正確丟垃圾」更一致。

懷疑者擔心成本上升與競爭劣勢。但若不把生態成本內部化，短壽命廉價產品會系統性占優。因此政策須以過渡期與補助分級，使創新仍可能。

故循環經濟是產業政策加消費者資訊——不只是道德。新的歐盟規範能否改善可測量性，而非只增加報告負擔，仍有待觀察。""",
        [n('Recyclingquoten','回收率'),n('Rezyklaten','再生料'),n('Internalisierung','內部化（成本）'),n('Ökodesign','生態設計'),n('staffeln','分級／分期'),n('Kreislaufwirtschaft','循環經濟'),n('Berichtsaufwand','報告負擔')],
        [p(' Quoten allein sagen wenig, wenn …','質疑指標','Zahlen allein sagen wenig, wenn Kontext fehlt.'),p('Jede Teilwahrheit verschiebt Verantwortung','批判推責','Jede Ausrede verschiebt Kosten.'),p('A plus B – nicht bloß C','擴大定義','Bildung plus Praxis – nicht bloß Theorie.')],
        ['環境論述：指標迷思→責任推諉→工具→成本反論。', '注意『系統性占優』這類結構句。', '標出 Insofern 收束。'],
        ['環境', '政策', '經濟', '論述'],
    ),
    item(
        'b2-67', "B2", 'email', '學術',
        'Antrag auf Ethikvotum', '申請倫理審查意見',
        """Betreff: Antrag auf Ethikvotum – Studie „Alltag mit Langzeitpflege“

Sehr geehrte Mitglieder der Ethikkommission,

hiermit beantrage ich die Prüfung des beigefügten Studienprotokolls. Erhoben werden Leitfadeninterviews mit Angehörigen, die zu Hause pflegen. Die Teilnahme ist freiwillig; Einwilligungen werden schriftlich dokumentiert und können jederzeit widerrufen werden, ohne dass Nachteile für die Versorgung entstehen.

Besondere Sorgfalt gilt dem Schutz vulnerabler Personen sowie der Pseudonymisierung von Audioaufnahmen. Rohdaten lagern verschlüsselt auf Hochschulservern; Zugriff haben nur projektbeteiligte Personen mit dokumentierter Schulung. Eine Weitergabe an Dritte ist nicht vorgesehen. Transkripte werden nach Projektende gemäß Löschkonzept vernichtet bzw. archiviert.

Ich bitte um Hinweise, falls Einwilligungsformulare oder die Risikoabschätzung nachgeschärft werden müssen. Der geplante Erhebungsbeginn liegt acht Wochen nach positivem Votum; Zwischenberichte an die Kommission sind jährlich vorgesehen. Für Rückfragen stehe ich in der Sprechstunde dienstags 10–12 Uhr zur Verfügung.

Mit freundlichen Grüßen
Prof. Dr. Elena Vogt
Institut für Sozialwissenschaften""",
        """主旨：申請倫理審查－研究「長期照顧的日常」

倫理委員會委員您好，

謹此申請審查附件研究計畫書。將對居家照顧的家屬進行指引式訪談。參與自願；同意書書面紀錄且可隨時撤回，不影響其受照顧權益。

對脆弱群體保護與錄音假名化將特別審慎。原始資料加密存於大學伺服器；僅受過紀錄訓練的計畫參與者可存取。不預定提供給第三人。逐字稿於計畫結束後依刪除方案銷毀或歸檔。

若同意書或風險評估需再強化，請惠予指正。預定於獲同意見後八週開始蒐集資料；並將每年向委員會提交期中報告。每週二 10–12 點面談時段可答詢。

此致問候
Prof. Dr. Elena Vogt
社會科學研究所""",
        [n('Ethikvotum','倫理審查意見'),n('Leitfadeninterviews','指引式訪談'),n('widerrufen','撤回'),n('vulnerabler Personen','脆弱／易受傷害者'),n('Pseudonymisierung','假名化'),n('nachgeschärft','再加強／收緊'),n('Erhebungsbeginn','資料蒐集開始')],
        [p('hiermit beantrage ich die Prüfung …','研究倫理申請','hiermit beantrage ich die Genehmigung …'),p('können jederzeit widerrufen werden','撤回權','kann jederzeit beendet werden'),p('Ich bitte um Hinweise, falls …','預先開放修正','Ich bitte um Hinweise, falls Fristen eng sind.')],
        ['學術正式信：對象保護→資料安全→時程→可聯繫。', '抓住自願／撤回／假名化三關鍵。', '語氣謙遜但程序完整。'],
        ['學術', '倫理', '研究', '正式郵件'],
    ),
    item(
        'b2-68', "B2", 'story', '政治社會',
        'Bürgerbeteiligung ohne Alibiverfahren', '沒有走過場的公民參與',
        """Bürgerbeteiligung wird häufig angekündigt, wenn Konflikte bereits eskaliert sind. Dann wirken Workshops wie Beruhigungstherapie, während Entscheidungen faktisch feststehen. Seriöse Beteiligung beginnt früher: mit verständlichen Unterlagen, ausreichenden Fristen und einer klaren Angabe, welche Spielräume noch offen sind.

Digitale Portale erhöhen Reichweite, schließen jedoch Menschen ohne stabile Netzzugänge aus, sofern keine analogen Kanäle parallel laufen. Moderation muss zudem Machtasymmetrien aktiv bearbeiten, damit Lautstarke nicht automatisch obsiegen. Protokolle und Begründungen, warum Anregungen übernommen oder verworfen wurden, erzeugen Legitimität.

Kritiker sehen in Beteiligung Zeitverlust. Ohne sie drohen jedoch Klagewellen und Vertrauensverlust, die Projekte teurer machen. Beteiligung ist damit kein Gegenteil von Effizienz, sondern eine Investition in Robustheit.

Insofern braucht Demokratie nicht mehr Symbole, sondern verlässliche Verfahren. Es bleibt abzuwarten, inwiefern Kommunen Personal und Mandat erhalten, Beteiligung als Pflichtaufgabe statt als Imagepflege zu betreiben.""",
        """公民參與常在衝突已升溫才被宣布。此時工作坊像安撫治療，決策其實已定。認真的參與要更早開始：易懂文件、充足期限，並清楚說明還有哪些空間可討論。

數位入口擴大觸及，但若不並行實體管道，會排除網路不穩者。主持還必須主動處理權力不對稱，避免嗓門大的自動勝出。說明建議為何被採納或否決的紀錄與理由，才能產生正當性。

批評者視參與為費時。但沒有參與，可能迎來訴訟潮與信任流失，反而更貴。因此參與不是效率的對立面，而是對強健性的投資。

故民主需要的不是更多象徵，而是可靠程序。地方政府能否獲得人力與授權，把參與當法定任務而非形象工程，仍有待觀察。""",
        [n('eskaliert','升溫／升級'),n('Spielräume','可協商空間'),n('obsiegen','勝出'),n('Legitimität','正當性'),n('Klagewellen','訴訟潮'),n('Robustheit','強健性／抗壓性'),n('Imagepflege','形象經營')],
        [p('während … feststehen','對比表面／實際','während die Richtung feststeht'),p('damit A nicht automatisch B','目的防杜','damit Lautstärke nicht entscheidet'),p('A ist kein Gegenteil von B, sondern …','重新框定','Kontrolle ist kein Gegenteil von Vertrauen, sondern seine Basis.')],
        ['政治社會論述：假參與→條件→數位落差→效率反論。', '找出 Imagepflege 對比 Pflichtaufgabe。', '標出 Insofern 收束句。'],
        ['政治社會', '民主', '參與', '論述'],
    ),
    item(
        'b2-69', "B2", 'notice', '健康',
        'Krankenhaus: Besuchs- und Hygieneregeln', '醫院探病與衛生規定',
        """Information für Patientinnen, Patienten und Angehörige
Zum Schutz vulnerabler Personen gelten ab sofort angepasste Besuchszeiten: täglich 15–18 Uhr, maximal zwei Personen gleichzeitig am Bett. Bei Atemwegsinfekten bitten wir um Verschiebung des Besuchs; Mund-Nasen-Schutz ist auf allen Stationen mit Immunsuppression verpflichtend. Ausnahmen für Abschiedssituationen werden individuell mit der Stationsleitung abgestimmt.

Blumen mit stehendem Wasser sind auf Intensivstationen nicht gestattet. Lebensmittel bitte nur nach Absprache mit dem Pflegepersonal mitbringen. Die Weitergabe von Medikamenten durch Angehörige ist untersagt. Seelsorge und ethische Beratung können unabhängig von den Besuchszeiten angefordert werden; Dolmetschung ist über die Zentrale buchbar.

Beschwerden zum Ablauf richten Sie an die Patientenfürsprache (Zi. 1.12). Diese Regeln ersetzen den Aushang vom März und werden bei geänderter Infektionslage kurzfristig angepasst. Verstöße gegen Hygienevorgaben können zum Abbruch des Besuchs führen. Wir danken für Kooperation und Rücksichtnahme.

Notfallnummern und aktuelle Hinweise finden Sie am Informationsschalter sowie unter /klinik-besuch.""",
        """病患與家屬須知
為保護脆弱族群，即日起調整探病時間：每日 15–18 點，床邊同時最多兩人。有呼吸道感染症狀請改期；免疫抑制病房必須戴口罩。告別等特殊情況由病房主管個案協調例外。

加護病房禁止帶有積水的花。食物請先與護理人員商量。禁止家屬轉交藥品。牧靈與倫理諮詢可不受探病時段限制申請；口譯可向總機預約。

流程申訴請洽病患權益服務（1.12 室）。本規則取代三月公告，並隨感染情勢短期調整。違反衛生規定可能中止探視。感謝配合與體諒。

緊急電話與最新提示見服務台及 /klinik-besuch。""",
        [n('vulnerabler Personen','脆弱族群'),n('Immunsuppression','免疫抑制'),n('nicht gestattet','不允許'),n('untersagt','禁止'),n('Patientenfürsprache','病患權益／申訴窗口'),n('Infektionslage','感染情勢'),n('Rücksichtnahme','體諒／顧及他人')],
        [p('gelten ab sofort …','即時生效規則','gelten ab sofort neue Öffnungszeiten'),p('bitte nur nach Absprache …','需事先協商','bitte nur nach Absprache fotografieren'),p('werden bei … angepasst','動態調整','werden bei Bedarf angepasst')],
        ['醫院公告：保護理由→禁止清單→申訴→動態更新。', '抓住 verpflichtend／untersagt 強度詞。', '注意對弱勢的例外服務（Seelsorge）。'],
        ['健康', '機構', '公告', '規範'],
    ),
    item(
        'b2-70', "B2", 'story', '媒體',
        'Desinformation als Geschäftsmodell', '作為商業模式的假訊',
        """Desinformation wird manchmal als bloßes Missverständnis dargestellt. Tatsächlich existieren professionelle Produktionsketten, die Aufmerksamkeit als Ware behandeln: zugespitzte Behauptungen, emotionale Trigger, schnelle Verbreitung in geschlossenen Gruppen. Wer nur auf Absicht einzelner Täterinnen schaut, unterschätzt Anreizstrukturen.

Plattformen reagieren mit Kennzeichnungen und Löschungen, geraten jedoch in Zielkonflikte zwischen Reichweite und Verantwortung. Regulierung kann Transparenz erzwingen, ersetzt aber keine redaktionelle Einordnung und keine öffentliche Medienförderung. Gleichzeitig müssen Eingriffe richterlich überprüfbar bleiben, damit Macht nicht willkürlich wächst.

Nutzerinnen sind nicht hilflos, aber auch nicht allein verantwortlich. Medienkompetenz wirkt, sofern Schulen und Erwachsenenbildung dauerhaft ausgestattet werden. Appelle ohne Infrastruktur verpuffen.

Insofern ist der Kampf gegen Desinformation eine Aufgabe von Technik, Recht und Bildung zugleich. Es bleibt abzuwarten, inwiefern neue Kennzeichnungspflichten die Qualität öffentlicher Debatten messbar verbessern – oder lediglich Sichtbarkeit von Konflikten erhöhen.""",
        """假訊有時被說成只是誤解。實際上存在把注意力當商品的專業生產鏈：尖銳斷言、情緒觸發、在封閉群組快速擴散。若只看個別行為者意圖，會低估誘因結構。

平台以標示與刪除回應，卻陷入觸及率與責任的目標衝突。管制能強迫透明，但取代不了編輯定位與公共媒體資助。同時干預必須可受司法審查，以免權力恣意擴張。

使用者並非無助，但也非獨負全責。媒體素養要有效，學校與成人教育須長期獲得資源。沒有基礎設施的呼籲會落空。

因此對抗假訊是技術、法律與教育的共同任務。新的標示義務能否可測量地改善公共辯論品質——或只是提高衝突可見度——仍有待觀察。""",
        [n('Desinformation','假訊／虛假訊息'),n('zugespitzte Behauptungen','尖銳化的斷言'),n('Anreizstrukturen','誘因結構'),n('Zielkonflikte','目標衝突'),n('richterlich überprüfbar','可受司法審查'),n('verpuffen','落空／效果消散'),n('Kennzeichnungspflichten','標示義務')],
        [p('Wer nur auf A schaut, unterschätzt B','糾正焦點','Wer nur auf Kosten schaut, unterschätzt Risiken.'),p('wirkt, sofern …','條件有效','Hilfe wirkt, sofern sie früh kommt.'),p('eine Aufgabe von A, B und C zugleich','多重責任','eine Aufgabe von Staat, Firmen und Bürgern zugleich')],
        ['媒體論述：商業邏輯→平台兩難→管制界限→教育條件。', '找出『不只個人責任』的句子。', '結論保留兩種可能結果。'],
        ['媒體', '民主', '科技', '論述'],
    ),
]




# Natural expansions for items under length / notes targets.
ENRICH: dict[str, dict] = {
    "uebung-51": {
        "text": "Hallo!\nIch heiße Mina.\nMeine Lieblingsfarbe ist Blau.\nIch mag auch Grün.\nUnd deine Farbe?",
        "textZh": "哈囉！\n我叫 Mina。\n我最愛的顏色是藍色。\n我也喜歡綠色。\n你喜歡什麼顏色？",
        "notes": [n("heiße", "名叫", "heißen：名字是……"), n("Lieblingsfarbe", "最愛的顏色"), n("Blau", "藍色"), n("mag auch", "也喜歡"), n("Und deine", "你的呢？")],
    },
    "uebung-52": {
        "text": "Leo: Wie alt bist du?\nMia: Ich bin 19 Jahre alt.\nLeo: Ich bin 21.\nMia: Cool! Wir sind jung.",
        "textZh": "Leo：你幾歲？\nMia：我 19 歲。\nLeo：我 21 歲。\nMia：酷！我們還年輕。",
        "notes": [n("Wie alt", "幾歲", "alt＝年齡。"), n("Jahre alt", "……歲"), n("Ich bin + 數字", "回答年齡"), n("jung", "年輕的"), n("Cool", "酷")],
    },
    "uebung-53": {
        "text": "Bibliothek\nMo–Fr: 9–18 Uhr\nSa: 10–14 Uhr\nSo: geschlossen\nBitte leise sein!",
        "textZh": "圖書館\n週一至五：9–18 點\n週六：10–14 點\n週日：休息\n請保持安靜！",
        "notes": [n("Bibliothek", "圖書館"), n("Mo–Fr", "週一到週五"), n("geschlossen", "關閉"), n("Bitte leise sein", "請保持安靜"), n("Sa", "週六")],
    },
    "uebung-54": {
        "text": "Hi Tom,\nich komme 10 Minuten später.\nDer Bus hat Verspätung.\nSorry!\nBis gleich\nNora",
        "textZh": "嗨 Tom，\n我會晚 10 分鐘到。\n公車延誤了。\n抱歉！\n待會見\nNora",
        "notes": [n("komme … später", "晚點到"), n("Minuten", "分鐘"), n("Verspätung", "延誤"), n("Sorry", "抱歉"), n("Bis gleich", "待會見")],
    },
    "uebung-56": {
        "text": "A: Was trinkst du gerne?\nB: Wasser, bitte.\nA: Mit Eis oder ohne?\nB: Ohne Eis, danke.",
        "textZh": "A：你喜歡喝什麼？\nB：水，麻煩。\nA：加冰還是不加？\nB：不加冰，謝謝。",
        "notes": [n("Was trinkst du", "你喝什麼"), n("gerne", "喜歡／樂意"), n("Mit Eis", "加冰"), n("oder ohne", "還是不加"), n("danke", "謝謝")],
    },
    "uebung-57": {
        "text": "WC → links\nDamen / Herren\nBitte sauber halten!\nSeife und Papier sind da.",
        "textZh": "洗手間 → 左邊\n女廁／男廁\n請保持清潔！\n有肥皂與衛生紙。",
        "notes": [n("links", "左邊"), n("Damen", "女廁"), n("Herren", "男廁"), n("sauber halten", "保持清潔"), n("Seife", "肥皂")],
    },
    "uebung-58": {
        "text": "Liebe Sara,\nalles Gute zur Prüfung!\nDu schaffst das bestimmt.\nSchreib mir danach.\nKüsse\nBen",
        "textZh": "親愛的 Sara，\n考試一切順利！\n你一定做得到。\n考完寫信給我。\n親親\nBen",
        "notes": [n("Alles Gute", "一切順利"), n("zur Prüfung", "祝考試"), n("Du schaffst das", "你做得到"), n("bestimmt", "一定"), n("danach", "之後")],
    },
    "uebung-59": {
        "text": "Montag: Sport um 18 Uhr\nDienstag: Deutschkurs\nFreitag: Kino mit Freunden\nSonntag: Pause und Schlaf",
        "textZh": "星期一：18 點運動\n星期二：德文課\n星期五：和朋友看電影\n星期日：休息睡覺",
        "notes": [n("Montag", "星期一"), n("um 18 Uhr", "在 18 點"), n("Deutschkurs", "德文課"), n("mit Freunden", "和朋友"), n("Pause", "休息")],
    },
    "uebung-60": {
        "text": "A: Wie heißt du bitte?\nB: Yusuf.\nA: Wie schreibt man das?\nB: Y-U-S-U-F. Genau!",
        "textZh": "A：請問你叫什麼？\nB：Yusuf。\nA：怎麼拼？\nB：Y-U-S-U-F。沒錯！",
        "notes": [n("Wie heißt du", "你叫什麼"), n("bitte", "請／禮貌"), n("Wie schreibt man", "怎麼拼"), n("Genau", "沒錯／正確"), n("schreibt", "書寫")],
    },
    "uebung-61": {
        "text": "Rauchen verboten!\nAuch E-Zigaretten und Shisha.\nBußgeld möglich.\nVielen Dank.",
        "textZh": "禁止吸菸！\n電子菸與水菸也不行。\n可能開罰單。\n謝謝配合。",
        "notes": [n("Rauchen verboten", "禁止吸菸"), n("Auch", "也"), n("E-Zigaretten", "電子菸"), n("Bußgeld", "罰鍰"), n("Vielen Dank", "謝謝")],
    },
    "uebung-62": {
        "text": "Hi!\nIch bin am Bahnhof, Ausgang Ost.\nWo bist du gerade?\nRuf mich bitte an!",
        "textZh": "嗨！\n我在火車站東出口。\n你現在在哪？\n請打電話給我！",
        "notes": [n("am Bahnhof", "在火車站"), n("Ausgang Ost", "東出口"), n("Wo bist du", "你在哪"), n("gerade", "現在／此刻"), n("Ruf mich an", "打電話給我")],
    },
    "uebung-63": {
        "text": "Ich bin Koch.\nIch arbeite in einem Restaurant.\nHeute koche ich Pasta.\nIch mag meinen Job.",
        "textZh": "我是廚師。\n我在一家餐廳工作。\n今天我煮義大利麵。\n我喜歡我的工作。",
        "notes": [n("Koch", "廚師"), n("arbeite in", "在……工作"), n("Restaurant", "餐廳"), n("koche", "烹煮"), n("Job", "工作")],
    },
    "uebung-64": {
        "text": "Kundin: Was kostet das Brot?\nVerkäufer: 4 Euro 50.\nKundin: Okay, ich nehme zwei.",
        "textZh": "顧客：這個麵包多少錢？\n店員：4 歐元 50。\n顧客：好，我要兩個。",
        "notes": [n("Was kostet", "多少錢"), n("Brot", "麵包"), n("Euro", "歐元"), n("ich nehme", "我要／買"), n("zwei", "兩個")],
    },
    "uebung-65": {
        "text": "Wow, schönes Foto vom See!\nWo war das genau?\nSieht richtig toll aus.\n❤️ Lea",
        "textZh": "哇，湖邊的照片好美！\n那是在哪裡拍的？\n看起來真的很棒。\n❤️ Lea",
        "notes": [n("schönes Foto", "美麗的照片"), n("See", "湖"), n("Wo war das", "那是在哪"), n("genau", "確切地"), n("toll aus", "看起來很棒")],
    },
    "uebung-66": {
        "text": "Aufzug außer Betrieb\nBitte die Treppe benutzen.\nWartung bis Freitag.\nEntschuldigung!",
        "textZh": "電梯暫停使用\n請走樓梯。\n維修至星期五。\n抱歉！",
        "notes": [n("Aufzug", "電梯"), n("außer Betrieb", "停止運作"), n("Treppe benutzen", "使用樓梯"), n("Wartung", "維修"), n("Entschuldigung", "抱歉")],
    },
    "uebung-67": {
        "text": "A: Alles okay bei dir?\nB: Mir ist kalt heute.\nA: Hier, nimm meine Jacke.\nB: Danke schön!",
        "textZh": "A：你還好嗎？\nB：我今天覺得冷。\nA：給，穿我的外套。\nB：謝謝你！",
        "notes": [n("Alles okay", "還好嗎"), n("Mir ist kalt", "我覺得冷"), n("Nimm", "拿／穿", "nehmen 命令式。"), n("Jacke", "外套"), n("Danke schön", "謝謝")],
    },
    "uebung-68": {
        "text": "Ich komme aus Japan.\nIch spreche Japanisch und Englisch.\nJetzt lerne ich Deutsch in Berlin.",
        "textZh": "我來自日本。\n我說日語和英語。\n現在我在柏林學德文。",
        "notes": [n("komme aus", "來自"), n("spreche", "說"), n("Japanisch", "日語"), n("Englisch", "英語"), n("in Berlin", "在柏林")],
    },
    "uebung-70": {
        "text": "A: Ich muss jetzt gehen.\nB: Okay. Tschüss und bis morgen!\nA: Bis dann, gute Nacht!\nB: Bis dann!",
        "textZh": "A：我現在得走了。\nB：好。掰掰，明天見！\nA：到時見，晚安！\nB：到時見！",
        "notes": [n("muss … gehen", "必須離開"), n("jetzt", "現在"), n("Tschüss", "掰"), n("Bis morgen", "明天見"), n("gute Nacht", "晚安")],
    },
    "a1-51": {
        "text": "Betreff: Paket für Sie\n\nHallo Frau Berg,\n\nheute kam ein Paket für Sie.\nIch habe es angenommen und in meine Wohnung gelegt.\nSie können es heute Abend bei mir abholen, ab 18 Uhr.\n\nViele Grüße\nKenji",
        "textZh": "主旨：您的包裹\n\nBerg 女士您好，\n\n今天有您的包裹送來。\n我代收了，放在我家。\n您今晚 18 點後可以來拿。\n\n問候\nKenji",
    },
    "a1-62": {
        "text": "Küchenplan – Woche 12\nMo/Di: Zimmer 3\nMi/Do: Zimmer 5\nFr/Sa: Zimmer 1\nBitte Spüle und Herd nach dem Kochen reinigen.\nMüll am Sonntag rausbringen.\nDanke fürs Mitmachen!",
        "textZh": "廚房輪值－第 12 週\n一／二：3 號房\n三／四：5 號房\n五／六：1 號房\n煮完請清理水槽與爐具。\n星期日請倒垃圾。\n謝謝大家配合！",
    },
    "a2-66": {
        "text": "Bekanntmachung\nWegen eines Feiertags verschiebt sich die gelbe Tonne vom Mittwoch auf Donnerstag.\nDie Biotonne bleibt am Dienstag wie gewohnt.\nBitte stellen Sie die Tonnen erst ab 19 Uhr am Vorabend heraus.\nFalsch befüllte Tonnen werden nicht geleert.\nFragen bitte an 0800 123 456 (Mo–Fr 9–15 Uhr).",
        "textZh": "公告\n因國定假日，黃色資源回收桶由週三改為週四清運。\n廚餘桶仍依往常於週二清運。\n請於前一晚 19 點後再推出去。\n分類錯誤的桶將不予清空。\n詢問請打 0800 123 456（週一至五 9–15 點）。",
    },
    "a2-70": {
        "text": "Interne Mitteilung\nAm Donnerstag, 10 Uhr, findet eine Brandschutzübung statt.\nBitte verlassen Sie bei Alarm ruhig das Gebäude über die Treppenhäuser.\nFahrstühle dürfen nicht benutzt werden.\nSammeln Sie sich auf dem Parkplatz Süd und warten Sie auf die Freigabe.\nDie Übung dauert voraussichtlich 20 Minuten. Vielen Dank.",
        "textZh": "內部通知\n週四 10 點將舉行消防演習。\n警報響起時請經由樓梯間冷靜離開大樓。\n禁止使用電梯。\n請在南停車場集合並等候解除訊號。\n演習預計約 20 分鐘。謝謝配合。",
    },
    "b1-52": {
        "text": "Einladung\nZur ordentlichen Eigentümerversammlung am 18. Juni, 19 Uhr, im Gemeinschaftsraum.\nTagesordnung: 1) Jahresabrechnung 2) Dachsanierung 3) Hausordnung zu Fahrrädern.\nVollmachten sind schriftlich bis 16. Juni beim Verwalter einzureichen.\nUnterlagen liegen ab 1. Juni im Hausflur zur Einsicht aus.\nEine Beschlussfähigkeit ist bei Anwesenheit von mindestens 50 Prozent der Anteile gegeben.",
        "textZh": "邀請\n例行區權人大會：6 月 18 日 19 點，交誼廳。\n議程：1) 年度結算 2) 屋頂整修 3) 腳踏車相關住戶公約。\n委託書須於 6 月 16 日前書面提交物業管理人。\n資料自 6 月 1 日起置於門廳供閱。\n出席份額至少達 50% 始具決議能力。",
    },
}


def apply_enrichments(items: list[dict]) -> None:
    for it in items:
        patch = ENRICH.get(it["id"])
        if not patch:
            continue
        if "text" in patch:
            it["text"] = patch["text"].strip()
        if "textZh" in patch:
            it["textZh"] = patch["textZh"].strip()
        if "notes" in patch:
            it["notes"] = patch["notes"]


def main() -> None:
    data = json.loads(PATH.read_text(encoding="utf-8"))
    existing_ids = {it["id"] for it in data["items"]}
    new_items = UEBUNG + A1 + A2 + B1 + B2
    apply_enrichments(new_items)
    for it in new_items:
        assert it["id"] not in existing_ids, it["id"]
        assert 4 <= len(it["notes"]) <= 7, (it["id"], len(it["notes"]))
        assert 2 <= len(it["patterns"]) <= 4, (it["id"], len(it["patterns"]))
        assert 2 <= len(it["tips"]) <= 3, (it["id"], len(it["tips"]))
        bands = {"練習": (70, 130), "A1": (150, 250), "A2": (280, 420), "B1": (380, 550), "B2": (1000, 1400)}
        lo, hi = bands[it["level"]]
        assert lo <= len(it["text"]) <= hi, (it["id"], len(it["text"]), lo, hi)
    before = len(data["items"])
    data["items"].extend(new_items)
    data["levels"] = ["練習", "A1", "A2", "B1", "B2"]
    data["note"] = NOTE
    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    from collections import Counter, defaultdict
    by = Counter(it["level"] for it in data["items"])
    lens: dict[str, list[int]] = defaultdict(list)
    for it in data["items"]:
        lens[it["level"]].append(len(it["text"]))
    print(f"appended {len(new_items)} (was {before}, now {len(data['items'])})")
    assert len(data["items"]) == 350, len(data["items"])
    for lv in data["levels"]:
        assert by[lv] == 70, (lv, by[lv])
        avg = sum(lens[lv]) / len(lens[lv])
        print(f"  {lv}: n={by[lv]} avg_len={avg:.1f} min={min(lens[lv])} max={max(lens[lv])}")
    print("new items (51–70) avg lengths:")
    for lv in data["levels"]:
        new = [it for it in new_items if it["level"] == lv]
        avg = sum(len(it["text"]) for it in new) / len(new)
        print(f"  {lv}: avg={avg:.1f} min={min(len(it['text']) for it in new)} max={max(len(it['text']) for it in new)}")
    print("note:", data["note"])


if __name__ == "__main__":
    main()
