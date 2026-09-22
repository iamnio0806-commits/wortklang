#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Append 15 NEW reading items per level (練習/A1/A2/B1/B2) → 75 total.

Does NOT remove or rewrite existing items. IDs continue from 71–85 per level.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "src" / "data" / "reading.json"

NOTE = (
    "對齊德檢（Goethe／ÖSD）閱讀難度：練習＝熱身短文；A1／A2／B1 循序銜接；"
    "B2＝考場長度論述／正式郵件／公告與訪談，含反論、名詞化與複合句。"
    "各級各 85 篇（練習＋A1–B2），共 425 篇分級閱讀。"
)

BANDS = {
    "練習": (70, 130),
    "A1": (150, 250),
    "A2": (280, 420),
    "B1": (380, 550),
    "B2": (1000, 1400),
}


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
# 練習 71–85  (~70–130 chars)
# ═══════════════════════════════════════════════════════════════════
UEBUNG = [
    item(
        "uebung-71", "練習", "card", "天氣",
        "Heute ist es sonnig", "今天很晴朗",
        "Heute ist es sonnig und warm.\nIch gehe in den Park.\nIch nehme Sonnenbrille mit.",
        "今天晴朗又溫暖。\n我去公園。\n我帶太陽眼鏡。",
        [n("sonnig", "晴朗的"), n("warm", "溫暖的"), n("Park", "公園"), n("Sonnenbrille", "太陽眼鏡"), n("nehme … mit", "帶去", "mitnehmen 可分動詞。")],
        [p("Heute ist es + 形容詞", "說天氣", "Heute ist es windig."), p("Ich nehme … mit", "帶東西出門", "Ich nehme einen Schirm mit.")],
        ["天氣＋計畫兩句就夠用。", "mitnehmen：把東西帶著走。"],
        ["天氣", "出門"],
    ),
    item(
        "uebung-72", "練習", "dialogue", "問路",
        "Wo ist die Bank?", "銀行在哪？",
        "A: Entschuldigung, wo ist die Bank?\nB: Geradeaus, dann links.\nA: Danke schön!\nB: Bitte!",
        "A：不好意思，銀行在哪？\nB：直走，然後左轉。\nA：謝謝！\nB：不客氣！",
        [n("Entschuldigung", "不好意思／抱歉"), n("wo ist", "在哪裡"), n("Geradeaus", "直走"), n("dann links", "然後左轉")],
        [p("Entschuldigung, wo ist …?", "問路開頭", "Entschuldigung, wo ist der Bahnhof?"), p("Geradeaus, dann links / rechts", "簡單指路", "Geradeaus, dann rechts.")],
        ["問路先說 Entschuldigung。", "Danke／Bitte 成對練。"],
        ["方向", "禮貌"],
    ),
    item(
        "uebung-73", "練習", "sign", "停車",
        "Parken nur mit Ticket", "停車需票證",
        "Parken nur mit Ticket\nMo–Sa 8–20 Uhr\nOhne Ticket: 40 Euro",
        "停車需購票\n週一至六 8–20 點\n無票：40 歐元",
        [n("Parken", "停車"), n("nur mit Ticket", "僅限持票"), n("Ohne Ticket", "無票"), n("Euro", "歐元")],
        [p("… nur mit + 名詞", "限制條件", "Eintritt nur mit Ausweis"), p("Ohne …: + 罰款", "罰則告示", "Ohne Maske: kein Eintritt")],
        ["停車告示：時間＋罰則。", "nur mit＝必須具備。"],
        ["告示", "規則"],
    ),
    item(
        "uebung-74", "練習", "message", "約咖啡",
        "Kaffee um 16 Uhr?", "下午四點喝咖啡？",
        "Hi Lea,\nHast du Zeit um 16 Uhr?\nKaffee im Café Sonne?\nLG Tim",
        "嗨 Lea，\n你下午四點有空嗎？\n在 Sonne 咖啡館喝咖啡？\n問候 Tim",
        [n("Hast du Zeit", "你有空嗎"), n("um 16 Uhr", "在 16 點"), n("Café", "咖啡館"), n("LG", "親切問候", "Liebe Grüße 縮寫。")],
        [p("Hast du Zeit um …?", "約時間", "Hast du Zeit am Freitag?"), p("… im Café …?", "提議地點", "Tee im Park?")],
        ["簡訊：時間＋地點＋署名。", "LG 很口語。"],
        ["約會", "簡訊"],
    ),
    item(
        "uebung-75", "練習", "card", "家庭",
        "Meine Familie", "我的家庭",
        "Ich habe eine Schwester.\nSie heißt Nina.\nSie ist Lehrerin.\nWir wohnen zusammen.",
        "我有一個姐姐／妹妹。\n她叫 Nina。\n她是老師。\n我們住在一起。",
        [n("Schwester", "姐／妹"), n("Sie heißt", "她叫"), n("Lehrerin", "女老師"), n("zusammen", "一起")],
        [p("Ich habe einen / eine + 家人", "介紹家人", "Ich habe einen Bruder."), p("Wir wohnen zusammen.", "同住", "Wir lernen zusammen.")],
        ["家人：陽性 Bruder／陰性 Schwester。", "職業陰陽：Lehrer／Lehrerin。"],
        ["家庭", "sein"],
    ),
    item(
        "uebung-76", "練習", "dialogue", "時間",
        "Wie spät ist es?", "現在幾點？",
        "A: Wie spät ist es?\nB: Es ist halb drei.\nA: Schon? Danke!\nB: Kein Problem.",
        "A：現在幾點？\nB：兩點半。\nA：已經？謝謝！\nB：沒問題。",
        [n("Wie spät ist es?", "幾點了？"), n("halb drei", "兩點半", "halb + 下一整點。"), n("Schon?", "已經？"), n("Kein Problem", "沒問題")],
        [p("Wie spät ist es?", "問時間", "Wie spät hast du?"), p("Es ist halb + 整點", "半點說法", "Es ist halb acht.")],
        ["德文 halb drei＝2:30。", "先練整點再練半點。"],
        ["時間", "日常"],
    ),
    item(
        "uebung-77", "練習", "sign", "請排隊",
        "Bitte anstellen", "請排隊",
        "Bitte hier anstellen!\nEin Kunde nach dem anderen.\nDanke für Ihre Geduld.",
        "請在此排隊！\n一位一位來。\n感謝您的耐心。",
        [n("anstellen", "排隊"), n("Ein … nach dem anderen", "一個接著一個"), n("Geduld", "耐心"), n("Ihre", "您的")],
        [p("Bitte hier + 動詞!", "現場指示", "Bitte hier warten!"), p("Danke für Ihre + 名詞", "禮貌致謝", "Danke für Ihre Hilfe.")],
        ["公共場合常用 Sie／Ihre。", "anstellen＝排隊。"],
        ["隊列", "禮貌"],
    ),
    item(
        "uebung-78", "練習", "message", "謝謝幫忙",
        "Danke für deine Hilfe", "謝謝你的幫忙",
        "Liebe Maya,\nvielen Dank für deine Hilfe gestern!\nDu bist super.\nDein Jonas",
        "親愛的 Maya，\n謝謝你昨天的幫忙！\n你超棒。\n你的 Jonas",
        [n("vielen Dank", "非常感謝"), n("für deine Hilfe", "為你的幫忙"), n("gestern", "昨天"), n("super", "超棒")],
        [p("Vielen Dank für …", "感謝公式", "Vielen Dank für die Einladung."), p("Du bist super.", "稱讚對方", "Du bist toll.")],
        ["感謝簡訊：事由＋稱讚。", "Dein／Deine 看署名者性別。"],
        ["感謝", "友誼"],
    ),
    item(
        "uebung-79", "練習", "card", "早餐",
        "Mein Frühstück", "我的早餐",
        "Zum Frühstück esse ich Brot mit Käse.\nIch trinke Tee.\nManchmal esse ich Obst.",
        "早餐我吃起司麵包。\n我喝茶。\n有時我吃水果。",
        [n("Zum Frühstück", "作為早餐"), n("Brot mit Käse", "起司麵包"), n("Manchmal", "有時候"), n("Obst", "水果", "集合名詞，常不加冠詞。")],
        [p("Zum Frühstück esse ich …", "說早餐", "Zum Abendessen esse ich Reis."), p("Manchmal + 動詞", "說頻率", "Manchmal laufe ich.")],
        ["essen／trinken 分開練。", "mit + 食物很常用。"],
        ["飲食", "日常"],
    ),
    item(
        "uebung-80", "練習", "dialogue", "座位",
        "Ist der Platz frei?", "這個位子空嗎？",
        "A: Entschuldigung, ist der Platz frei?\nB: Ja, bitte!\nA: Danke.\nB: Gern.",
        "A：不好意思，這個位子空嗎？\nB：是的，請坐！\nA：謝謝。\nB：不客氣。",
        [n("Platz", "位子／座位"), n("frei", "空的／有空"), n("bitte", "請（坐）"), n("Gern", "樂意／不客氣", "口語回覆。")],
        [p("Ist der / die / das … frei?", "問是否空", "Ist der Tisch frei?"), p("Ja, bitte!", "允許／邀請", "Nein, leider nicht.")],
        ["搭車／餐廳常問 Platz frei。", "Gern＝不客氣的口語版。"],
        ["座位", "公共場所"],
    ),
    item(
        "uebung-81", "練習", "sign", "保持安靜",
        "Bitte Ruhe", "請保持安靜",
        "Bitte Ruhe!\nPrüfung von 9–12 Uhr\nHandy bitte lautlos.",
        "請保持安靜！\n考試 9–12 點\n手機請靜音。",
        [n("Ruhe", "安靜"), n("Prüfung", "考試"), n("Handy", "手機"), n("lautlos", "靜音的")],
        [p("Bitte Ruhe!", "安靜要求", "Bitte leise sein!"), p("Handy bitte lautlos.", "手機規則", "Bitte Flugmodus.")],
        ["考試／圖書館常見標誌。", "lautlos＝無聲。"],
        ["考試", "告示"],
    ),
    item(
        "uebung-82", "練習", "message", "忘記東西",
        "Ich habe meinen Schirm vergessen", "我忘了雨傘",
        "Hi Sara,\nich habe meinen Schirm bei dir vergessen.\nKann ich ihn morgen holen?\nDanke!\nPaul",
        "嗨 Sara，\n我把雨傘忘在你家了。\n明天可以去拿嗎？\n謝謝！\nPaul",
        [n("vergessen", "忘記"), n("bei dir", "在你家／你那兒"), n("holen", "去取"), n("ihn", "它／他", "陽性 Schirm → ihn。")],
        [p("Ich habe … vergessen", "說忘了東西", "Ich habe meine Schlüssel vergessen."), p("Kann ich … holen?", "請求取回", "Kann ich es heute holen?")],
        ["vergessen 常用完成式。", "代詞看名詞性別。"],
        ["遺忘", "請求"],
    ),
    item(
        "uebung-83", "練習", "card", "交通工具",
        "Mit dem Bus", "搭公車",
        "Ich fahre mit dem Bus zur Arbeit.\nDie Fahrt dauert 20 Minuten.\nManchmal nehme ich das Rad.",
        "我搭公車上班。\n車程 20 分鐘。\n有時我騎腳踏車。",
        [n("mit dem Bus", "搭公車", "mit + 第三格。"), n("zur Arbeit", "去上班", "zu der。"), n("dauert", "持續／花費時間"), n("Rad", "腳踏車", "Fahrrad 簡稱。")],
        [p("Ich fahre mit dem / der …", "說交通方式", "Ich fahre mit der Bahn."), p("Die Fahrt dauert …", "說車程", "Die Fahrt dauert eine Stunde.")],
        ["mit dem／mit der 看交通工具性別。", "Rad＝腳踏車口語。"],
        ["交通", "上班"],
    ),
    item(
        "uebung-84", "練習", "dialogue", "點餐",
        "Zum Mitnehmen", "外帶",
        "Kellner: Zum Hieressen oder zum Mitnehmen?\nGast: Zum Mitnehmen, bitte.\nKellner: Eine Minute.\nGast: Super, danke!",
        "服務生：內用還是外帶？\n客人：外帶，麻煩。\n服務生：一分鐘。\n客人：太好了，謝謝！",
        [n("Zum Hieressen", "內用"), n("zum Mitnehmen", "外帶"), n("Eine Minute", "一分鐘／稍等"), n("Gast", "客人")],
        [p("Zum Hieressen oder zum Mitnehmen?", "內用／外帶", "Nur zum Mitnehmen."), p("…, bitte.", "禮貌點餐", "Einen Kaffee, bitte.")],
        ["咖啡店兩句超實用。", "zum + 名詞化動詞。"],
        ["點餐", "外帶"],
    ),
    item(
        "uebung-85", "練習", "message", "週末見",
        "Bis am Wochenende", "週末見",
        "Hi Nora,\nbis am Wochenende!\nSchreib mir den Treffpunkt.\nCiao\nSam",
        "嗨 Nora，\n週末見！\n跟我說碰面地點。\n掰\nSam",
        [n("bis am Wochenende", "週末見"), n("Schreib mir", "寫給我", "schreiben + 第三格。"), n("Treffpunkt", "碰面地點"), n("Ciao", "掰", "口語道別。")],
        [p("Bis am / am + 時間!", "約再見", "Bis am Freitag!"), p("Schreib mir + 資訊", "請對方告知", "Schreib mir die Adresse.")],
        ["約見簡訊：再見＋請補資訊。", "mir＝第三格『給我』。"],
        ["約會", "道別"],
    ),
]


# ═══════════════════════════════════════════════════════════════════
# A1 71–85  (~150–250 chars)
# ═══════════════════════════════════════════════════════════════════
A1 = [
    item(
        "a1-71", "A1", "email", "室友",
        "Einkaufsliste für WG", "室友購物清單",
        """Betreff: Einkaufen heute

Hallo zusammen,

ich gehe heute Nachmittag einkaufen.
Brauchen wir Milch, Eier und Spülmittel?
Schreibt mir bitte bis 15 Uhr.

Liebe Grüße
Yuna""",
        """主旨：今天採買

大家好，

我今天下午去採買。
我們需要牛奶、蛋和洗碗精嗎？
請在 15 點前跟我說。

問候
Yuna""",
        [n("zusammen", "大家／一起"), n("einkaufen", "採買"), n("Spülmittel", "洗碗精"), n("Schreibt mir", "寫給我", "複數命令式。"), n("bis 15 Uhr", "到 15 點為止")],
        [p("Brauchen wir …?", "確認需求", "Brauchen wir Brot?"), p("Schreibt mir bitte bis …", "設回覆期限", "Schreibt mir bis morgen.")],
        ["室友信：計畫＋問需求＋期限。", "命令式複數：schreibt。"],
        ["郵件", "同居"],
    ),
    item(
        "a1-72", "A1", "dialogue", "服飾店",
        "Eine andere Größe", "換尺寸",
        """Verkäuferin: Kann ich Ihnen helfen?
Kundin: Ja, diese Hose in Größe 38, bitte.
Verkäuferin: Hier, bitte. Die Kabine ist links.
Kundin: Danke. Haben Sie die auch in Blau?
Verkäuferin: Moment, ich schaue nach.""",
        """店員：需要幫忙嗎？
顧客：是的，這件褲子要 38 號。
店員：請。試衣間在左邊。
顧客：謝謝。藍色也有嗎？
店員：稍等，我去看一下。""",
        [n("Größe", "尺寸"), n("Hose", "褲子"), n("Kabine", "試衣間"), n("in Blau", "藍色款"), n("schaue nach", "去查看", "nachschauen。")],
        [p("… in Größe …, bitte", "指定尺寸", "Das Shirt in Größe M, bitte."), p("Haben Sie … auch in …?", "問其他顏色／款", "Haben Sie das auch in Rot?")],
        ["購物：尺寸→試穿→顏色。", "Ihnen＝第三格『您』。"],
        ["購物", "服裝"],
    ),
    item(
        "a1-73", "A1", "story", "圖書館借書",
        "Mein erster Bibliotheksausweis", "我的第一張借書證",
        """Heute hole ich meinen Bibliotheksausweis ab.
Ich brauche einen Ausweis und eine Meldebescheinigung.
Dann darf ich drei Wochen lang Bücher ausleihen.
Online verlängern ist auch möglich.
Ich freue mich auf viele Krimis!""",
        """今天我去領借書證。
我需要身分證件和戶籍證明。
然後我可以借書三週。
也可以線上續借。
我很期待很多推理小說！""",
        [n("Bibliotheksausweis", "借書證"), n("Meldebescheinigung", "戶籍登記證明"), n("ausleihen", "借出"), n("verlängern", "延長／續借"), n("Krimis", "推理小說")],
        [p("Ich hole … ab", "去領取", "Ich hole mein Paket ab."), p("… Wochen lang", "持續幾週", "zwei Wochen lang")],
        ["辦證常要身分＋住址證明。", "ausleihen／verlängern 成對記。"],
        ["圖書館", "行政"],
    ),
    item(
        "a1-74", "A1", "notice", "游泳池",
        "Hinweis Schwimmbad", "游泳池公告",
        """Liebe Badegäste,
die Rutsche ist heute wegen Wartung geschlossen.
Das Schwimmbecken bleibt geöffnet.
Bitte Badeschuhe tragen.
Schließfächer kosten 1 Euro.
Viel Spaß!
Die Badleitung""",
        """親愛的泳客們，
溜滑梯今天因維護關閉。
泳池照常開放。
請穿泳鞋。
置物櫃 1 歐元。
玩得開心！
泳池管理""",
        [n("Badegäste", "泳客"), n("Rutsche", "溜滑梯"), n("Wartung", "維護"), n("Badeschuhe", "泳鞋"), n("Schließfächer", "置物櫃")],
        [p("wegen + 名詞", "關閉原因", "wegen Reinigung"), p("bleibt geöffnet", "維持開放", "Die Sauna bleibt geöffnet.")],
        ["公告：關／開＋規則＋費用。", "Viel Spaß 收尾友善。"],
        ["公告", "休閒"],
    ),
    item(
        "a1-75", "A1", "dialogue", "計程車",
        "Zum Hauptbahnhof", "去中央車站",
        """Fahrer: Wohin darf ich Sie fahren?
Fahrgast: Zum Hauptbahnhof, bitte. Ich habe es eilig.
Fahrer: In Ordnung. Mit Gepäck?
Fahrgast: Ja, einen Koffer.
Fahrer: Gut, ich helfe Ihnen.""",
        """司機：要載您去哪？
乘客：中央車站，麻煩。我趕時間。
司機：好的。有行李嗎？
乘客：有，一個行李箱。
司機：好，我幫您。""",
        [n("Wohin", "去哪裡"), n("Hauptbahnhof", "中央車站"), n("eilig", "趕時間", "Ich habe es eilig。"), n("Gepäck", "行李"), n("Koffer", "行李箱")],
        [p("Zum / Zur + 地點, bitte", "報目的地", "Zur Klinik, bitte."), p("Ich habe es eilig.", "說趕時間", "Können Sie etwas schneller fahren?")],
        ["計程車：目的地＋行李＋趕時間。", "helfen + 第三格：Ihnen。"],
        ["交通", "旅行"],
    ),
    item(
        "a1-76", "A1", "email", "語言班",
        "Fehlende Hausaufgaben", "缺交作業",
        """Betreff: Hausaufgaben von Montag

Liebe Frau Keller,

leider konnte ich die Hausaufgaben nicht abgeben.
Ich war krank.
Darf ich sie am Mittwoch nachreichen?

Viele Grüße
Omar""",
        """主旨：星期一作業

Keller 女士您好，

很抱歉我無法交作業。
我生病了。
星期三可以補交嗎？

問候
Omar""",
        [n("leider", "很遺憾／可惜"), n("abgeben", "繳交"), n("krank", "生病"), n("nachreichen", "補交"), n("Darf ich", "我可以嗎")],
        [p("leider konnte ich … nicht …", "道歉＋原因", "Leider konnte ich nicht kommen."), p("Darf ich … nachreichen?", "請求補交", "Darf ich die Arbeit später abgeben?")],
        ["請假／補交：抱歉＋原因＋請求。", "nachreichen＝晚點補上。"],
        ["課程", "郵件"],
    ),
    item(
        "a1-77", "A1", "story", "超市打工",
        "Mein erster Job im Supermarkt", "超市第一份工",
        """Seit zwei Wochen arbeite ich im Supermarkt.
Ich räume Regale ein und helfe an der Kasse.
Die Kolleginnen sind freundlich.
Am Abend bin ich oft müde, aber zufrieden.
Das Geld spare ich für eine Reise.""",
        """我在超市工作兩週了。
我補貨，也在收銀台幫忙。
同事們很友善。
晚上我常很累，但滿足。
錢我存起來準備旅行。""",
        [n("räume … ein", "上架／補貨", "einräumen。"), n("Kasse", "收銀台"), n("müde", "疲倦"), n("zufrieden", "滿意"), n("spare", "存錢", "sparen。")],
        [p("Seit + 時間 + arbeite ich …", "說工作多久", "Seit einem Monat lerne ich Deutsch."), p("Das Geld spare ich für …", "存錢目的", "Ich spare für ein Fahrrad.")],
        ["seit + 時間＝從那時到現在。", "aber 連接兩個形容詞。"],
        ["工作", "日常生活"],
    ),
    item(
        "a1-78", "A1", "notice", "停車場",
        "Parkhaus geschlossen", "停車場關閉",
        """Achtung!
Das Parkhaus ist von Freitag 22 Uhr bis Sonntag 6 Uhr wegen Reinigung geschlossen.
Bitte nutzen Sie den Parkplatz an der Oststraße.
Fahrzeuge müssen bis 21:30 Uhr entfernt werden.
Vielen Dank.
Stadtwerke""",
        """注意！
停車場因清潔，週五 22 點至週日 6 點關閉。
請改用東街停車場。
車輛須於 21:30 前移出。
謝謝。
市政事業""",
        [n("Parkhaus", "立體停車場"), n("wegen Reinigung", "因清潔"), n("nutzen", "使用"), n("entfernt werden", "被移出", "被動。"), n("Stadtwerke", "市政公用事業")],
        [p("von … bis … wegen …", "時段＋原因", "von 8 bis 12 wegen Umbau"), p("müssen … werden", "強制被動", "müssen rechtzeitig entfernt werden")],
        ["關閉公告：時段＋替代＋期限。", "注意被動 entfernt werden。"],
        ["公告", "交通"],
    ),
    item(
        "a1-79", "A1", "dialogue", "美髮",
        "Beim Friseur", "在美髮店",
        """Friseurin: Wie soll ich schneiden?
Kundin: Nicht zu kurz, bitte. Und etwas Stufen.
Friseurin: Waschen auch?
Kundin: Ja, und föhnen.
Friseurin: Gut. Das dauert etwa 40 Minuten.""",
        """髮型師：要怎麼剪？
顧客：別太短。再修一點層次。
髮型師：也洗頭嗎？
顧客：要，還要吹整。
髮型師：好。大約 40 分鐘。""",
        [n("schneiden", "剪"), n("Nicht zu kurz", "別太短"), n("Stufen", "層次"), n("Waschen", "洗頭"), n("föhnen", "吹整")],
        [p("Nicht zu + 形容詞, bitte", "限制程度", "Nicht zu lang, bitte."), p("Das dauert etwa …", "預估時間", "Das dauert etwa eine Stunde.")],
        ["美髮：長度＋服務＋時間。", "etwas＝一點點。"],
        ["服務", "外貌"],
    ),
    item(
        "a1-80", "A1", "email", "活動取消",
        "Treffen fällt aus", "聚會取消",
        """Betreff: Treffen am Donnerstag

Hallo Team,

unser Treffen am Donnerstag fällt leider aus.
Ich bin auf Dienstreise.
Neuen Termin schlage ich nächste Woche vor.

Beste Grüße
Lina""",
        """主旨：週四聚會

團隊大家好，

週四聚會很抱歉取消。
我出差。
下週我會提議新時間。

此致問候
Lina""",
        [n("fällt … aus", "取消／告吹", "ausfallen。"), n("Dienstreise", "出差"), n("Neuen Termin", "新時段"), n("schlage … vor", "提議", "vorschlagen。"), n("Beste Grüße", "此致問候")],
        [p("… fällt aus", "活動取消", "Der Kurs fällt aus."), p("Ich schlage … vor", "提議替代", "Ich schlage Freitag vor.")],
        ["取消信：什麼取消＋原因＋下一步。", "vorschlagen 可分動詞。"],
        ["工作", "行程"],
    ),
    item(
        "a1-81", "A1", "story", "腳踏車爆胎",
        "Platter Reifen", "爆胎",
        """Heute Morgen hatte mein Fahrrad einen platten Reifen.
Ich bin zur Arbeit gelaufen und kam zehn Minuten zu spät.
Am Nachmittag repariere ich den Reifen in der Werkstatt.
Nächstes Mal nehme ich eine Luftpumpe mit.
So lernt man!""",
        """今天早上我的腳踏車爆胎了。
我走路上班，晚了十分鐘。
下午我去修車行修輪胎。
下次我會帶打氣筒。
這就是學習！""",
        [n("platten Reifen", "爆胎／沒氣的輪胎"), n("gelaufen", "走路去了", "laufen 完成式。"), n("zu spät", "太晚"), n("repariere", "修理"), n("Luftpumpe", "打氣筒")],
        [p("hatte einen platten Reifen", "說爆胎", "Mein Auto hatte eine Panne."), p("kam … zu spät", "遲到", "Ich kam fünf Minuten zu spät.")],
        ["問題→後果→解決→預防。", "完成式：bin … gelaufen。"],
        ["交通", "問題處理"],
    ),
    item(
        "a1-82", "A1", "notice", "影印費",
        "Preise Kopierer", "影印價格",
        """Kopieren – Preise
A4 schwarz-weiß: 0,05 Euro
A4 Farbe: 0,20 Euro
A3 schwarz-weiß: 0,10 Euro
Bitte mit Campus-Karte bezahlen.
Störung? Tel. 2221
IT-Service""",
        """影印－價格
A4 黑白：0.05 歐元
A4 彩色：0.20 歐元
A3 黑白：0.10 歐元
請用校園卡付款。
故障？電話 2221
IT 服務""",
        [n("Kopieren", "影印"), n("schwarz-weiß", "黑白"), n("Farbe", "彩色"), n("Campus-Karte", "校園卡"), n("Störung", "故障")],
        [p("…: + 價格", "價目表", "Scan: 0,10 Euro"), p("Bitte mit … bezahlen", "付款方式", "Bitte bar bezahlen")],
        ["價目表閱讀：規格＋單價。", "逗號是德文小數點。"],
        ["校園", "費用"],
    ),
    item(
        "a1-83", "A1", "dialogue", "旅館入住",
        "Check-in im Hotel", "旅館辦理入住",
        """Rezeption: Guten Abend. Auf welchen Namen?
Gast: Müller, Anna. Ich habe reserviert.
Rezeption: Ja, Zimmer 214. Frühstück von 7 bis 10.
Gast: Wann ist Check-out?
Rezeption: Bis 11 Uhr. Hier ist Ihre Schlüsselkarte.""",
        """櫃檯：晚安。請問姓名？
客人：Müller, Anna。我有預約。
櫃檯：是，214 房。早餐 7 到 10 點。
客人：退房幾點？
櫃檯：11 點前。這是您的房卡。""",
        [n("Auf welchen Namen?", "登記在誰名下？"), n("reserviert", "已預約"), n("Check-out", "退房"), n("Schlüsselkarte", "房卡"), n("Bis 11 Uhr", "到 11 點為止")],
        [p("Ich habe reserviert.", "說明有預約", "Ich habe ein Zimmer reserviert."), p("Wann ist Check-out?", "問退房時間", "Wann ist das Frühstück?")],
        ["入住：姓名→房號→餐→退房。", "Auf welchen Namen 很固定。"],
        ["旅行", "旅館"],
    ),
    item(
        "a1-84", "A1", "email", "借用會議室",
        "Raum 3A reservieren", "預約 3A 會議室",
        """Betreff: Raum 3A am Freitag

Hallo Herr Vogt,

dürfen wir Raum 3A am Freitag von 14–16 Uhr nutzen?
Wir haben ein Teammeeting.
Beamer brauchen wir auch.

Danke und Grüße
Sofia""",
        """主旨：週五 3A 會議室

Vogt 先生您好，

我們週五 14–16 點可以用 3A 室嗎？
我們有團隊會議。
也需要投影機。

謝謝與問候
Sofia""",
        [n("dürfen wir", "我們可以嗎"), n("nutzen", "使用"), n("Teammeeting", "團隊會議"), n("Beamer", "投影機"), n("brauchen", "需要")],
        [p("Dürfen wir … nutzen?", "請求使用空間", "Dürfen wir die Küche nutzen?"), p("… brauchen wir auch.", "追加需求", "Stühle brauchen wir auch.")],
        ["借用信：時間＋用途＋設備。", "dürfen＝被允許。"],
        ["工作", "預約"],
    ),
    item(
        "a1-85", "A1", "story", "夜市初體驗",
        "Auf dem Nachtmarkt", "在夜市",
        """Am Samstagabend gehe ich mit Freunden auf den Nachtmarkt.
Es riecht nach Essen und ist laut und bunt.
Ich kaufe Bubble Tea und gebratenen Mais.
Wir machen viele Fotos.
Danach fahren wir mit der U-Bahn nach Hause.""",
        """星期六晚上我和朋友去夜市。
到處是食物香味，又吵又繽紛。
我買珍奶和烤玉米。
我們拍很多照片。
之後搭地鐵回家。""",
        [n("Nachtmarkt", "夜市"), n("Es riecht nach", "聞起來像……"), n("laut und bunt", "吵雜又色彩豐富"), n("gebratenen Mais", "烤玉米"), n("U-Bahn", "地鐵")],
        [p("Es riecht nach …", "描述氣味", "Es riecht nach Kaffee."), p("Danach fahren wir …", "接下行程", "Danach gehen wir schlafen.")],
        ["感官詞：riecht／laut／bunt。", "Danach 串故事。"],
        ["休閒", "食物"],
    ),
]


# ═══════════════════════════════════════════════════════════════════
# A2 71–85  (~280–420 chars)
# ═══════════════════════════════════════════════════════════════════
A2 = [
    item(
        "a2-71", "A2", "email", "宿舍維修",
        "Heizung funktioniert nicht", "暖氣故障",
        """Betreff: Defekte Heizung in Zimmer 12

Sehr geehrte Hausverwaltung,

seit Dienstag wird mein Zimmer nicht mehr warm.
Die Heizung macht Geräusche, aber die Luft bleibt kalt.
Die Außentemperatur liegt unter fünf Grad, deshalb ist das dringend.

Könnten Sie bitte heute oder morgen einen Techniker schicken?
Ich bin ab 17 Uhr zu Hause und unter 0176 555 221 erreichbar.

Mit freundlichen Grüßen
Jin Park""",
        """主旨：12 號房暖氣故障

物業管理處鈞鑒，

自星期二起房間不再暖和。
暖氣有聲音，但空氣仍冷。
室外低於五度，因此很緊急。

能否今天或明天派技術人員？
我 17 點後在家，電話 0176 555 221。

此致問候
Jin Park""",
        [n("defekte Heizung", "故障的暖氣"), n("Geräusche", "聲音／雜音"), n("Außentemperatur", "室外溫度"), n("dringend", "緊急"), n("Techniker", "技術人員"), n("erreichbar", "可聯繫到")],
        [p("seit + 時間 + wird … nicht mehr …", "說明故障起點", "Seit Montag geht das WLAN nicht."), p("Könnten Sie bitte … schicken?", "客氣請求派人", "Könnten Sie jemanden vorbeischicken?")],
        ["維修信：症狀＋急迫＋可聯繫時段。", "Könnten Sie 比 Können Sie 更客氣。"],
        ["住房", "維修"],
    ),
    item(
        "a2-72", "A2", "dialogue", "手機門市",
        "Handydisplay tauschen", "更換手機螢幕",
        """Mitarbeiter: Was ist passiert?
Kundin: Das Display ist gesprungen. Geht noch, aber die Ecken sind tot.
Mitarbeiter: Wir können es in zwei Stunden tauschen. Kostet 129 Euro plus Display.
Kundin: Haben Sie ein Ersatzgerät für die Wartezeit?
Mitarbeiter: Leider nein. Sie können aber hier sitzen und WLAN nutzen.
Kundin: Okay. Bitte machen Sie einen Kostenvoranschlag schriftlich.
Mitarbeiter: Klar, ich drucke ihn aus.""",
        """店員：發生什麼事？
顧客：螢幕裂了。還能用，但邊角沒反應。
店員：兩小時可換。129 歐元外加面板。
顧客：等候期間有備用機嗎？
店員：沒有。但您可以坐這裡用 Wi‑Fi。
顧客：好。請給我書面估價。
店員：沒問題，我列印。""",
        [n("Display", "螢幕"), n("gesprungen", "裂開"), n("tauschen", "更換"), n("Ersatzgerät", "備用機"), n("Kostenvoranschlag", "估價單"), n("schriftlich", "書面")],
        [p("Wir können es in … tauschen", "說明維修時程", "Wir können es heute noch reparieren."), p("Bitte … schriftlich", "要求書面", "Bitte bestätigen Sie das schriftlich.")],
        ["維修對話：故障→費用→替代→書面確認。", "plus＝外加。"],
        ["消費", "維修"],
    ),
    item(
        "a2-73", "A2", "story", "社區清潔日",
        "Frühjahrsputz im Viertel", "社區春季清掃",
        """Letzten Samstag gab es in unserem Viertel einen Frühjahrsputz.
Nachbarinnen und Nachbarn haben Müll an der Böschung gesammelt und Beete neu bepflanzt.
Die Stadt hat Handschuhe, Säcke und heißen Tee gestellt.
Ich habe vor allem Plastik und Zigarettenstummel gefunden.
Am Ende gab es Kuchen im Gemeindehaus.
Es war anstrengend, aber das Ufer sieht jetzt wirklich besser aus.
Nächstes Jahr mache ich wieder mit.""",
        """上週六我們社區辦春季清掃。
鄰居們在邊坡撿垃圾、重種花圃。
市府提供手套、袋子和熱茶。
我主要撿到塑膠和菸蒂。
最後在社區中心有蛋糕。
很累，但河岸看起來好多了。
明年我還會參加。""",
        [n("Frühjahrsputz", "春季大掃除"), n("Viertel", "街區／社區"), n("Böschung", "邊坡"), n("bepflanzt", "栽種"), n("Zigarettenstummel", "菸蒂"), n("Gemeindehaus", "社區活動中心")],
        [p("Es gab …", "有舉辦／有提供", "Es gab Tee und Kuchen."), p("Nächstes Jahr mache ich wieder mit.", "說會再參加", "Nächstes Mal helfe ich wieder.")],
        ["活動敘事：誰做什麼→支援→結果→未來。", "mitmachen＝參加。"],
        ["社區", "志工"],
    ),
    item(
        "a2-74", "A2", "notice", "電梯維修",
        "Aufzug außer Betrieb – Hinweis", "電梯停用公告",
        """Wichtige Information an alle Bewohnerinnen und Bewohner
Der Aufzug ist von Montag, 7 Uhr, bis voraussichtlich Mittwoch, 18 Uhr, wegen Wartung außer Betrieb.
Bitte planen Sie mehr Zeit ein und nutzen Sie das Treppenhaus.
Für Personen mit eingeschränkter Mobilität steht ein Begleitservice zur Verfügung: bitte bis Sonntag 12 Uhr unter 030 111 222 anmelden.
Lieferungen bitte im Hof abstellen und uns informieren.
Vielen Dank für Ihr Verständnis.
Hausverwaltung Nord""",
        """給全體住戶的重要通知
電梯因維護，自週一 7 點起至預計週三 18 點停用。
請預留更多時間並走樓梯。
行動不便者可申請陪同服務：請於週日 12 點前撥打 030 111 222 登記。
送貨請放中庭並通知我們。
感謝理解。
北區物業""",
        [n("voraussichtlich", "預計"), n("Wartung", "維護"), n("planen … ein", "預留／排入", "einplanen。"), n("eingeschränkter Mobilität", "行動受限"), n("Begleitservice", "陪同服務"), n("abstellen", "放置")],
        [p("von … bis voraussichtlich …", "預估時段", "von 9 bis voraussichtlich 15 Uhr"), p("steht … zur Verfügung", "可使用", "Ein Taxi steht zur Verfügung.")],
        ["長公告：時段＋替代＋弱勢協助＋物流。", "außer Betrieb 很關鍵。"],
        ["住房", "無障礙"],
    ),
    item(
        "a2-75", "A2", "email", "實習申請回覆",
        "Rückfrage zum Praktikum", "實習相關追問",
        """Betreff: Praktikum Marketing – kurze Rückfrage

Sehr geehrte Frau Albrecht,

vielen Dank für die Einladung zum Gespräch am 12. Mai.
Ich hätte noch zwei Fragen: Ist das Praktikum vergütet, und kann ich an zwei Tagen im Homeoffice arbeiten?

Außerdem möchte ich wissen, ob ein Fahrradstellplatz vorhanden ist.
Über eine kurze Rückmeldung würde ich mich freuen.

Mit freundlichen Grüßen
Elena Kovacs""",
        """主旨：行銷實習－簡短追問

Albrecht 女士您好，

感謝邀請我 5 月 12 日面談。
我還有兩個問題：實習是否有津貼？以及是否可兩天在家遠距？

另外想確認是否有腳踏車停車位。
若能短覆，感激不盡。

此致問候
Elena Kovacs""",
        [n("Rückfrage", "追問／回詢"), n("vergütet", "有給付／有薪"), n("Homeoffice", "在家上班"), n("Fahrradstellplatz", "腳踏車停車位"), n("Rückmeldung", "回覆"), n("vorhanden", "有／存在")],
        [p("Ich hätte noch … Fragen", "客氣追加問題", "Ich hätte noch eine Frage."), p("Über … würde ich mich freuen", "禮貌期待回覆", "Über eine Antwort würde ich mich freuen.")],
        ["申請後追問：感謝＋具體問題＋結語。", "Konjunktiv II：hätte／würde 更客氣。"],
        ["實習", "求職"],
    ),
    item(
        "a2-76", "A2", "dialogue", "牙科預約",
        "Termin in der Zahnarztpraxis", "牙科診所預約",
        """Assistentin: Zahnarztpraxis Berger, guten Tag.
Patient: Hallo, ich brauche einen Termin wegen Zahnschmerzen.
Assistentin: Geht es um eine akute Sache? Dann hätten wir heute 17:40.
Patient: Ja, bitte. Muss ich etwas mitbringen?
Assistentin: Versichertenkarte und eine Liste Ihrer Medikamente, falls Sie welche nehmen.
Patient: Gut. Bin ich als Notfall oder normal eingetragen?
Assistentin: Als dringender Termin. Bitte 10 Minuten früher kommen.""",
        """助理：Berger 牙科診所，您好。
病人：您好，我牙痛想預約。
助理：是急性嗎？那我們今天 17:40 有位。
病人：好，麻煩。需要帶什麼？
助理：健保卡，若有服藥請帶藥單。
病人：好。我是掛急診還是一般？
助理：緊急時段。請早 10 分鐘到。""",
        [n("Zahnschmerzen", "牙痛"), n("akut", "急性的"), n("Versichertenkarte", "健保卡"), n("Medikamente", "藥物"), n("Notfall", "急診／緊急情況"), n("dringender Termin", "緊急時段")],
        [p("Ich brauche einen Termin wegen …", "預約原因", "Ich brauche einen Termin wegen Husten."), p("Dann hätten wir …", "提供時段", "Dann hätten wir morgen früh einen Platz.")],
        ["電話預約：症狀→時段→攜帶物→抵達。", "hätten wir＝客氣提供。"],
        ["健康", "預約"],
    ),
    item(
        "a2-77", "A2", "story", "失物招領",
        "Mein Schal im Bus", "公車裡的圍巾",
        """Gestern habe ich im Bus meinen Schal vergessen.
Als ich es merkte, war ich schon zwei Stationen weiter.
Ich bin zurückgefahren und habe den Fahrer gefragt.
Er schickte mich zum Fundbüro am Endbahnhof.
Tatsächlich lag der Schal dort in einer Kiste mit Handschuhen und Regenschirmen.
Ich musste meinen Ausweis zeigen und eine kurze Liste unterschreiben.
Nächstes Mal hänge ich den Schal fester an die Tasche.""",
        """昨天我把圍巾忘在公車上。
發現時已過了兩站。
我折返問司機。
他叫我去終點站的失物招領處。
圍巾果然在箱子裡，和手套、雨傘在一起。
我得出示證件並簽一份短單。
下次我會把圍巾綁緊在袋子上。""",
        [n("merkte", "察覺", "merken。"), n("Stationen", "站"), n("Fundbüro", "失物招領處"), n("tatsächlich", "果然／確實"), n("unterschreiben", "簽名"), n("fester", "更緊")],
        [p("Als ich …, war ich schon …", "發現太晚", "Als ich ankam, war der Zug schon weg."), p("Ich musste … und …", "必要步驟", "Ich musste warten und Formulare ausfüllen.")],
        ["故事線：遺失→尋找→找回→教訓。", "Fundbüro 實用詞。"],
        ["交通", "遺失"],
    ),
    item(
        "a2-78", "A2", "notice", "社團招新",
        "Mitglieder gesucht – Fotoclub", "攝影社招員",
        """Fotoclub Campus sucht neue Mitglieder!
Wir treffen uns jeden zweiten Donnerstag um 18:30 im Medienraum B2.
Themen: Porträt, Streetfotografie und Bildbearbeitung.
Ausleihen von Kameras ist für Mitglieder kostenlos, nach kurzer Einführung.
Anmeldung per Mail an foto@campus.example bis 30. September.
Bitte schreibt kurz, welches Equipment ihr schon habt.
Anfängerinnen und Anfänger sind ausdrücklich willkommen.
Der erste Abend ist unverbindlich zum Kennenlernen.""",
        """校園攝影社徵求新社員！
每兩週週四 18:30 在媒體教室 B2 聚會。
主題：人像、街拍與後製。
社員可在短訓後免費借用相機。
請於 9 月 30 日前寄信至 foto@campus.example 報名。
請簡短說明已有器材。
初學者特別歡迎。
第一次聚會不強制入社，僅認識。""",
        [n("jeden zweiten Donnerstag", "每隔一個週四"), n("Bildbearbeitung", "影像後製"), n("Ausleihen", "借用"), n("ausdrücklich", "明確地"), n("unverbindlich", "無約束／不強制"), n("Kennenlernen", "認識／熟識")],
        [p("… sucht neue Mitglieder", "招募", "Der Chor sucht neue Mitglieder."), p("Der erste … ist unverbindlich", "降低門檻", "Das Probetraining ist unverbindlich.")],
        ["招新公告：時間＋主題＋福利＋報名。", "ausdrücklich willkommen＝特別歡迎。"],
        ["校園", "社團"],
    ),
    item(
        "a2-79", "A2", "email", "保險詢問",
        "Frage zur Reiseversicherung", "旅行保險詢問",
        """Betreff: Deckung bei Reiseabsage

Sehr geehrte Damen und Herren,

ich habe bei Ihnen eine Reiseversicherung abgeschlossen.
Meine Frage: Bin ich versichert, wenn ich wegen einer plötzlichen Erkrankung der Mutter die Reise absagen muss?

Die Reise soll am 3. Oktober beginnen.
Anbei sende ich die Buchungsbestätigung.
Bitte teilen Sie mir mit, welche Atteste nötig sind.

Mit freundlichen Grüßen
Marco Silva""",
        """主旨：取消行程的承保範圍

諸位鈞鑒，

我向貴公司投保旅行保險。
請問：若因母親突發疾病取消行程，是否在保範圍？

行程預計 10 月 3 日開始。
附上訂位確認。
請告知需要哪些診斷證明。

此致問候
Marco Silva""",
        [n("Deckung", "承保範圍"), n("Reiseabsage", "取消旅行"), n("abgeschlossen", "已投保／簽訂"), n("plötzlichen Erkrankung", "突發疾病"), n("Atteste", "診斷證明"), n("Anbei", "附件隨信")],
        [p("Bin ich versichert, wenn …?", "確認承保條件", "Bin ich versichert, wenn der Flug ausfällt?"), p("Bitte teilen Sie mir mit, welche …", "請告知細節", "Bitte teilen Sie mir mit, welche Fristen gelten.")],
        ["保險信：保單→情境→附件→所需文件。", "Anbei＝附件在此。"],
        ["保險", "旅行"],
    ),
    item(
        "a2-80", "A2", "dialogue", "腳踏車店",
        "Fahrrad Bremsen prüfen", "檢查煞車",
        """Mechaniker: Was kann ich für Sie tun?
Kundin: Die Bremsen quietschen und greifen schlecht.
Mechaniker: Ich schaue mir die Beläge und die Kabel an. Dauert etwa 30 Minuten.
Kundin: Können Sie gleich die Beleuchtung prüfen? Gestern war das Rücklicht schwach.
Mechaniker: Mache ich. Soll ich einen Kostenvoranschlag machen, bevor ich etwas wechsle?
Kundin: Ja, bitte. Über 60 Euro möchte ich erst angerufen werden.
Mechaniker: Notiert.""",
        """技師：有什麼能幫您？
顧客：煞車有尖叫聲，而且不太靈。
技師：我看來令片和鋼索，大約 30 分鐘。
顧客：能順便檢查燈光嗎？昨天尾燈偏弱。
技師：好。更換前要先估價嗎？
顧客：要。超過 60 歐元請先打電話給我。
技師：記下了。""",
        [n("quietschen", "尖叫／刺耳聲"), n("greifen", "咬住／發揮作用"), n("Beläge", "來令片"), n("Beleuchtung", "燈光"), n("Rücklicht", "尾燈"), n("Notiert", "記下了")],
        [p("Können Sie gleich … prüfen?", "順便請求", "Können Sie gleich den Reifendruck prüfen?"), p("Über … möchte ich erst … werden", "設定費用上限", "Über 100 Euro möchte ich erst gefragt werden.")],
        ["維修店：症狀→檢查→追加→費用門檻。", "gleich＝順便／馬上。"],
        ["交通", "維修"],
    ),
    item(
        "a2-81", "A2", "story", "義工導覽",
        "Als Museumsführerin auf Probe", "試當博物館導覽",
        """Am Sonntag habe ich zum ersten Mal eine Kurzführung im Stadtmuseum gemacht.
Vorher habe ich den Text zwei Stunden wiederholt und Karten mit Daten gelernt.
Die Gruppe war klein: sechs Erwachsene und zwei Kinder.
Am Anfang war ich nervös und habe zu schnell gesprochen.
Eine Besucherin hat freundlich gebeten, etwas langsamer zu sein.
Danach wurde es besser, und am Ende gab es sogar Applaus.
Die Leitung hat mir ein Feedback-Gespräch für nächste Woche angeboten.""",
        """星期天我第一次在市立博物館做短導覽。
事前我複習文本兩小時，並背資料卡。
團體不大：六位成人與兩個孩子。
一開始我很緊張，講太快。
一位訪客客氣請我慢一點。
之後好多了，最後甚至有掌聲。
主管下週要约我做回饋面談。""",
        [n("Kurzführung", "短導覽"), n("wiederholt", "複習"), n("nervös", "緊張"), n("gebeten", "請求", "bitten 完成式。"), n("Applaus", "掌聲"), n("Feedback-Gespräch", "回饋面談")],
        [p("zum ersten Mal … gemacht", "第一次經驗", "Zum ersten Mal habe ich allein unterrichtet."), p("Danach wurde es besser", "情況改善", "Danach wurde die Lage ruhiger.")],
        ["學習曲線：準備→緊張→調整→回饋。", "gebeten＝被請求。"],
        ["志工", "表達"],
    ),
    item(
        "a2-82", "A2", "notice", "垃圾分類提醒",
        "Falsche Befüllung der Tonnen", "垃圾桶錯誤投放",
        """Hinweis der Abfallwirtschaft
In den letzten Wochen wurden mehrere gelbe Tonnen nicht geleert, weil Restmüll oder Glas darin lag.
Bitte beachten Sie: Verpackungen gehören in die gelbe Tonne, Glas zum Container, Biomüll in die braune Tonne.
Falsch befüllte Tonnen bleiben stehen; eine Nachleerung kostet extra.
Einen kurzen Leitfaden finden Sie im Hausflur und unter abfall.example/stadt.
Fragen: Mo–Fr 9–15 Uhr, 0800 987 654.
Vielen Dank für Ihre Mithilfe.""",
        """廢棄物處理單位提醒
近幾週多個黃色資源桶因混入一般垃圾或玻璃而未清運。
請注意：包裝進黃桶，玻璃進回收桶，廚餘進棕桶。
錯誤投放的桶會留置；加清需額外付費。
簡短指南在門廳及 abfall.example/stadt。
詢問：週一至五 9–15 點，0800 987 654。
感謝配合。""",
        [n("Befüllung", "填裝／投放"), n("geleert", "被清空"), n("Restmüll", "一般垃圾"), n("Nachleerung", "加開清運"), n("Leitfaden", "指南"), n("Mithilfe", "協助／配合")],
        [p("wurden … nicht geleert, weil …", "說明未清運原因", "wurde nicht abgeholt, weil …"), p("Falsch … bleiben stehen", "後果說明", "Falsch geparkte Autos werden abgeschleppt.")],
        ["分類公告：錯誤→規則→後果→聯絡。", "gehören in／zum 表示歸屬。"],
        ["環保", "住家"],
    ),
    item(
        "a2-83", "A2", "email", "課程轉班",
        "Wechsel in den Abendkurs", "轉到晚班課程",
        """Betreff: Bitte um Kurswechsel A2

Liebe Frau Neumann,

ich besuche derzeit den Vormittagskurs A2.
Ab Oktober beginne ich eine Teilzeitstelle und kann vormittags nicht mehr kommen.
Gibt es noch Plätze im Abendkurs dienstags und donnerstags?

Mein Kenntnisstand entspricht dem aktuellen Kapitel.
Über eine positive Rückmeldung würde ich mich freuen.

Herzliche Grüße
Deniz Yilmaz""",
        """主旨：請求轉 A2 課程

Neumann 女士您好，

我目前上 A2 上午班。
十月起開始兼職，上午無法再來。
週二、四晚班還有名額嗎？

我的程度與目前單元相符。
若能獲准，十分感謝。

親切問候
Deniz Yilmaz""",
        [n("Kurswechsel", "轉班／轉課"), n("derzeit", "目前"), n("Teilzeitstelle", "兼職工作"), n("Kenntnisstand", "程度／知識水準"), n("entspricht", "符合"), n("positive Rückmeldung", "正面回覆")],
        [p("Ab + 時間 + beginne ich …", "說明新時程", "Ab Mai arbeite ich in Hamburg."), p("Gibt es noch Plätze im …?", "問名額", "Gibt es noch Plätze im Wochenendkurs?")],
        ["轉班信：現況→原因→目標班→程度說明。", "entspricht＝相當於／符合。"],
        ["課程", "工作"],
    ),
    item(
        "a2-84", "A2", "dialogue", "租屋仲介",
        "Besichtigung einer Wohnung", "看房",
        """Maklerin: Die Wohnung ist 48 Quadratmeter, Baujahr 1998, renoviert 2022.
Interessent: Sind die Nebenkosten in den 780 Euro enthalten?
Maklerin: Nein, plus etwa 180 Euro. Kaution sind drei Kaltmieten.
Interessent: Darf man die Wände streichen?
Maklerin: In hellen Farben ja, nach Absprache. Haustiere nur nach Zustimmung der Eigentümerin.
Interessent: Wann wäre der früheste Einzug?
Maklerin: Zum 1. November, wenn die Unterlagen passen.""",
        """仲介：房子 48 平方公尺，1998 年建、2022 整修。
看房者：780 歐元含不含水電雜費？
仲介：不含，大約再加 180。押金三個月淨租金。
看房者：可以粉刷牆壁嗎？
仲介：淺色可以，需事先商量。寵物須房東同意。
看房者：最早何時可入住？
仲介：文件齊備則 11 月 1 日。""",
        [n("Nebenkosten", "雜費（水電等）"), n("enthalten", "包含在內"), n("Kaution", "押金"), n("Kaltmieten", "淨租金（不含雜費）"), n("nach Absprache", "經商量後"), n("Einzug", "入住")],
        [p("Sind … in … enthalten?", "問是否含在價格內", "Sind Getränke im Preis enthalten?"), p("Zum 1. + Monat", "起租日", "Zum 1. März")],
        ["看房：面積→費用→規定→入住日。", "plus＝外加。"],
        ["住房", "租屋"],
    ),
    item(
        "a2-85", "A2", "story", "數位掛號",
        "Online einen Amtstermin buchen", "線上預約機關時段",
        """Ich brauchte einen Termin beim Bürgeramt und habe ihn online gebucht.
Zuerst musste ich ein Konto anlegen und einen Code per SMS bestätigen.
Freie Termine gab es erst in drei Wochen, außer für Notfälle.
Ich habe mir eine Erinnerung in den Kalender gesetzt und alle Dokumente vorher sortiert.
Am Tag selbst war die Warteschlange trotzdem lang, aber digital angemeldete Personen wurden getrennt aufgerufen.
Ohne Online-Buchung hätte ich wahrscheinlich noch länger gewartet.""",
        """我需要市民局時段，於是線上預約。
先要開帳號並用簡訊驗證碼確認。
除非急件，否則要等三週才有空缺。
我在日曆設提醒，並事先整理文件。
當天隊伍仍長，但線上掛號者分開叫號。
若沒線上預約，大概要等更久。""",
        [n("Bürgeramt", "市民事務所"), n("Konto anlegen", "建立帳號"), n("Erinnerung", "提醒"), n("Warteschlange", "等候隊伍"), n("aufgerufen", "被叫號"), n("Ohne … hätte ich …", "虛擬式：若沒有……")],
        [p("Ich habe ihn online gebucht", "線上預約", "Ich habe den Tisch online reserviert."), p("Ohne A hätte ich B", "對比假設", "Ohne App hätte ich den Bus verpasst.")],
        ["行政故事：預約→等待→當日流程→反思。", "注意 Konjunktiv II：hätte … gewartet。"],
        ["行政", "數位化"],
    ),
]


# ═══════════════════════════════════════════════════════════════════
# B1 71–85  (~380–550 chars)
# ═══════════════════════════════════════════════════════════════════
B1 = [
    item(
        "b1-71", "B1", "email", "彈性工時申請",
        "Antrag auf Gleitzeit", "申請彈性工時",
        """Betreff: Antrag auf Gleitzeit ab September

Sehr geehrte Frau Hartmann,

hiermit beantrage ich Gleitzeit von 7:30–16:00 Uhr (Kernzeit 9–15) ab dem 1. September.
Grund ist die Betreuung meiner Tochter nach dem Kita-Wechsel; die neue Einrichtung schließt früher.

Meine Aufgaben im Projekt „Atlas“ kann ich weiterhin in voller Höhe erfüllen.
Absprachen mit dem Team sind bereits vorbesprochen; Vertretungen in der Kernzeit sichere ich zu.

Über eine schriftliche Zustimmung bis 20. August würde ich mich freuen.
Gerne erläutere ich Details in einem kurzen Gespräch.

Mit freundlichen Grüßen
Jonas Weber""",
        """主旨：申請自九月起彈性工時

Hartmann 女士您好，

謹此申請自 9 月 1 日起彈性工時 7:30–16:00（核心工時 9–15）。
原因是女兒托育機構轉換後接送；新機構較早關門。

「Atlas」專案任務我仍可全額完成。
已與團隊預先溝通；核心時段代理我保證到位。

若能於 8 月 20 日前書面同意，感激不盡。
也樂意短談細節。

此致問候
Jonas Weber""",
        [n("hiermit beantrage ich", "謹此申請"), n("Gleitzeit", "彈性工時"), n("Kernzeit", "核心工時"), n("Kita-Wechsel", "托兒所轉換"), n("in voller Höhe", "全額／完整程度"), n("Vertretungen", "代理"), n("sichere ich zu", "我保證")],
        [p("hiermit beantrage ich … ab …", "正式申請", "Hiermit beantrage ich Homeoffice ab Mai."), p("Über … würde ich mich freuen", "禮貌期待", "Über eine Rückmeldung würde ich mich freuen.")],
        ["申請信：措施＋原因＋工作保障＋期限。", "hiermit 提升正式度。"],
        ["職場", "家庭", "申請"],
    ),
    item(
        "b1-72", "B1", "notice", "宿舍網路升級",
        "Wartungsfenster WLAN-Upgrade", "無線網升級維護窗",
        """Mitteilung der IT-Wohnheimverwaltung
Am Samstag, 14. Oktober, 6–10 Uhr, wird das WLAN-Netzwerk auf neuen Standard umgestellt.
In diesem Zeitraum ist mit Unterbrechungen und zeitweise fehlendem Internetzugang zu rechnen.
Bitte speichern Sie offene Arbeiten vorher lokal und beenden Sie große Uploads rechtzeitig.
VPN-Zugänge zur Hochschule bleiben nach der Umstellung bestehen; ggf. ist einmaliges Neuverbinden nötig.
Bei Problemen nach 10 Uhr melden Sie sich über das Ticketportal /it-heim mit Raumnummer.
Notdienst nur bei totalem Netzausfall: 0170 444 889 (kurzfristig besetzt).
Vielen Dank für Ihre Geduld.""",
        """宿舍 IT 管理通知
10 月 14 日週六 6–10 點，無線網將升級至新標準。
此時段可能中斷，並暫時無法上網。
請事先將未存檔工作存到本機，並及早結束大型上傳。
升級後校內 VPN 仍可用；必要時重新連線一次。
10 點後若有問題，請至 /it-heim 開票並註明房號。
僅全面斷網時打緊急電話 0170 444 889（短時值班）。
感謝耐心。""",
        [n("umgestellt", "轉換／改設定"), n("mit … zu rechnen", "預計會有……"), n("zeitweise", "暫時／間歇"), n("ggf.", "必要時", "gegebenenfalls。"), n("Neuverbinden", "重新連線"), n("Ticketportal", "工單入口"), n("Notdienst", "緊急值班")],
        [p("ist mit … zu rechnen", "預期後果", "Mit Verzögerungen ist zu rechnen."), p("ggf. ist … nötig", "可能額外步驟", "Ggf. ist ein Neustart nötig.")],
        ["維護公告：時段→影響→自助步驟→回報管道。", "mit … zu rechnen 很正式。"],
        ["校園", "IT", "公告"],
    ),
    item(
        "b1-73", "B1", "story", "共享廚房衝突",
        "Streit um die WG-Küche", "室友廚房爭執",
        """In unserer WG eskalierte der Streit um die Küche, nachdem zweimal Geschirr über Nacht stehen blieb.
Statt Vorwürfe per Chat zu schicken, haben wir eine halbe Stunde am Tisch gesprochen.
Jeder nannte ein konkretes Ärgernis und einen Vorschlag: Spüldienstplan, 20-Minuten-Regel und ein gemeinsamer Vorratsbereich.
Interessant war, dass niemand „Absicht“ unterstellte – eher Überarbeitung und unterschiedliche Standards.
Wir schrieben die Regeln auf und hängten sie innen an die Schranktür.
Nach zwei Wochen stockte der Plan einmal, aber eine kurze Erinnerung reichte.
Die Atmosphäre ist nicht perfekt, aber spürbar entspannter.""",
        """我們宿舍在碗盤兩次過夜沒洗後，廚房爭執升高。
我們沒在聊天軟體互責，而是坐下來談半小時。
每人說一個具體困擾與一個建議：洗碗輪值、20 分鐘規則、共用儲物區。
有趣的是沒人指控「故意」——比較像過勞與標準不同。
我們把規則寫下貼在櫃門內側。
兩週後計畫中斷一次，但短提醒就夠。
氣氛不算完美，但明顯輕鬆多了。""",
        [n("eskalierte", "升高／失控升級"), n("Vorwürfe", "指責"), n("Ärgernis", "令人惱火之事"), n("unterstellte", "暗指／栽贓"), n("Überarbeitung", "過勞"), n("stockte", "停滯"), n("spürbar", "明顯可感覺到")],
        [p("Statt A zu tun, haben wir B", "替代做法", "Statt zu schimpfen, haben wir geredet."), p("nicht perfekt, aber …", "務實收尾", "nicht ideal, aber tragfähig")],
        ["衝突敘事：引爆→對話→規則→追蹤。", "注意名詞化：Überarbeitung。"],
        ["同居", "溝通", "日常"],
    ),
    item(
        "b1-74", "B1", "dialogue", "職涯諮詢",
        "Gespräch in der Studienberatung", "學習諮詢對話",
        """Beraterin: Sie schwanken zwischen einem Master und dem direkten Berufseinstieg?
Student: Ja. Finanziell wäre Arbeit attraktiver, aber ich fürchte Wissenslücken.
Beraterin: Welche Lücken genau – methodisch oder fachlich?
Student: Vor allem Statistik und Projektmanagement.
Beraterin: Dann wären gezielte Zertifikatskurse plus Werkstudentenstelle eine Option, ohne gleich zwei Jahre Master.
Student: Und wenn ich den Master später nachhole?
Beraterin: Viele Programme akzeptieren Berufserfahrung. Wichtig ist, dass Sie Ihre Motive schriftlich sortieren.
Student: Ich erstelle eine Vor- und Nachteilliste und komme in zwei Wochen wieder.""",
        """諮詢師：您在碩士與直接就業之間猶豫？
學生：對。經濟上工作較吸引，但我怕知識缺口。
諮詢師：什麼缺口——方法還是專業內容？
學生：主要是統計與專案管理。
諮詢師：那可考慮針對性證照課加上工讀，不必立刻讀兩年碩士。
學生：若之後再補碩士呢？
諮詢師：許多學程認可工作經驗。重要的是把動機寫清楚。
學生：我做優缺列表，兩週後再來。""",
        [n("schwanken zwischen", "在……之間搖擺"), n("Berufseinstieg", "進入職場"), n("Wissenslücken", "知識缺口"), n("gezielte", "針對性的"), n("Werkstudentenstelle", "在學工讀職"), n("nachhole", "補修／後補"), n("Motive", "動機")],
        [p("schwanken zwischen A und B", "猶豫兩選項", "Ich schwanke zwischen Umzug und Bleiben."), p("Dann wären … eine Option", "提出選項", "Dann wäre Teilzeit eine Option.")],
        ["諮詢對話：釐清缺口→替代路徑→下次行動。", "wären＝客氣虛擬。"],
        ["教育", "職涯", "決策"],
    ),
    item(
        "b1-75", "B1", "email", "房東修繕追蹤",
        "Erinnerung an Schimmelbekämpfung", "黴菌處理提醒",
        """Betreff: Zweite Erinnerung – Schimmel im Bad

Sehr geehrter Herr Lange,

am 2. März habe ich Schimmel im Bad gemeldet; am 10. März wurde ein Termin angekündigt, der ausfiel.
Bisher fand keine fachgerechte Sanierung statt. Die Stelle wird größer und verursacht Hustenreiz.

Ich bitte Sie, bis 5. April ein Fachunternehmen zu beauftragen und mir den Termin schriftlich zu nennen.
Andernfalls behalte ich mir vor, die Mietminderung zu prüfen und die zuständige Behörde zu informieren.

Für eine konstruktive Lösung bleibe ich ansprechbar.

Mit freundlichen Grüßen
Amira Haddad""",
        """主旨：第二次提醒－浴室黴菌

Lange 先生您好，

我於 3 月 2 日通報浴室發霉；3 月 10 日原訂時段取消。
至今未進行專業修繕。範圍擴大並引起咳嗽刺激。

請您於 4 月 5 日前委託專業公司，並書面告知時程。
否則我保留檢討減租並通知主管機關的權利。

我仍願以建設性方式解決。

此致問候
Amira Haddad""",
        [n("fachgerechte Sanierung", "符合專業的修繕"), n("Hustenreiz", "咳嗽刺激"), n("beauftragen", "委託"), n("behalte ich mir vor", "我保留……權利"), n("Mietminderung", "減租"), n("ansprechbar", "可聯繫／願溝通"), n("konstruktive Lösung", "建設性解決")],
        [p("Ich bitte Sie, bis … zu …", "設期限請求", "Ich bitte Sie, bis Freitag zu antworten."), p("Andernfalls behalte ich mir vor, …", "預告後續手段", "Andernfalls behalte ich mir rechtliche Schritte vor.")],
        ["追蹤信：時間線→現況→期限→保留權利→仍願協商。", "behalte mir vor 屬正式措辭。"],
        ["租屋", "法律", "健康"],
    ),
    item(
        "b1-76", "B1", "notice", "辦公室熱適應",
        "Maßnahmen bei Hitze im Büro", "辦公室高溫措施",
        """Interne Mitteilung – Hitzeschutz
Bei Außentemperaturen über 30 °C gelten folgende Regelungen:
1) Homeoffice ist nach Absprache mit der Führungskraft möglich, sofern die Tätigkeit es erlaubt.
2) Zwischen 12 und 15 Uhr werden Präsenzmeetings auf 30 Minuten begrenzt.
3) Ventilatoren und Wasser stehen in der Teeküche bereit; Fenster bitte nur in den Morgenstunden öffnen.
Wer gesundheitliche Beschwerden hat, meldet sich frühzeitig beim Betriebsarzt.
Diese Regelung gilt bis einschließlich 31. August und kann bei anhaltender Hitze verlängert werden.
Fragen an personal@firma.example.""",
        """內部通知－防暑
室外超過 30°C 時適用以下規定：
1) 經主管同意可居家辦公，前提是工作性質允許。
2) 12–15 點現場會議以 30 分鐘為限。
3) 茶水間提供風扇與飲水；窗戶請僅於早晨開啟。
有健康不適者請及早向廠醫回報。
本規定適用至 8 月 31 日（含），若持續高溫可延長。
問題洽 personal@firma.example。""",
        [n("Hitzeschutz", "防暑／熱危害防護"), n("nach Absprache", "經商量"), n("sofern", "只要／倘若"), n("Präsenzmeetings", "實體會議"), n("Betriebsarzt", "廠醫／企業醫師"), n("bis einschließlich", "至……為止（含當日）"), n("anhaltender Hitze", "持續高溫")],
        [p("Bei … gelten folgende Regelungen", "條件觸發規定", "Bei Alarm gelten folgende Regeln."), p("sofern die Tätigkeit es erlaubt", "前提條件", "sofern Kapazität vorhanden ist")],
        ["內部規定：觸發條件→條列→健康→效期。", "sofern 引導條件。"],
        ["職場", "健康", "公告"],
    ),
    item(
        "b1-77", "B1", "story", "二手修復經濟",
        "Reparieren statt Wegwerfen", "修理代替丟棄",
        """Als mein Toaster den Geist aufgab, wollte ich zuerst ein Neugerät bestellen.
Stattdessen brachte ich ihn in ein Repair-Café. Eine Freiwillige öffnete das Gehäuse, reinigte Kontakte und erklärte mir den Fehler in zehn Minuten.
Das Gerät läuft wieder; ich habe fünf Euro Spende gegeben und zwei Stunden Wartezeit investiert.
Dabei wurde mir klar, wie sehr Wegwerfgewohnheiten mit fehlendem Wissen zusammenhängen.
Nicht jede Reparatur lohnt sich finanziell – bei billiger Elektronik oft nicht.
Aber bei robusten Geräten spart man Ressourcen und lernt handwerkliche Souveränität.
Ich habe mir inzwischen ein kleines Werkzeugset zugelegt.""",
        """烤麵包機壞掉時，我原本想直接訂新的。
後來拿到 Repair-Café。一位志工打開機殼、清理接點，十分鐘說明故障。
機器又能用了；我捐五歐元，也投入兩小時等候。
這讓我明白，丟棄習慣與缺乏知識關係很大。
不是每種維修都划算——廉價電子產品常常不划算。
但對耐用設備可省資源，也學到動手自主。
我後來買了一套小工具。""",
        [n("den Geist aufgab", "壞掉／報銷", "口語。"), n("Repair-Café", "維修咖啡／義修空間"), n("Spende", "捐款"), n("Wegwerfgewohnheiten", "用完即丟習慣"), n("lohnt sich", "划得來"), n("Souveränität", "自主／主權感"), n("zugelegt", "添購")],
        [p("Statt A wollte ich B; stattdessen …", "計畫改變", "Statt zu kaufen, reparierte ich."), p("Nicht jede … lohnt sich", "有保留的主張", "Nicht jede Reise lohnt sich.")],
        ["敘事＋反思：個人經驗→結構原因→界限→行動。", "lohnt sich＝值得。"],
        ["消費", "永續", "技能"],
    ),
    item(
        "b1-78", "B1", "dialogue", "客服申訴升級",
        "Beschwerde beim Kundenservice", "客服投訴",
        """Agentin: Kundenservice ElektroPlus, mein Name ist Sara. Wie kann ich helfen?
Kunde: Mein Kühlschrank ist nach der Reparatur erneut ausgefallen. Ich möchte eine Eskalation.
Agentin: Ich verstehe. Haben Sie die Auftragsnummer?
Kunde: Ja, A-44921. Außerdem habe ich Fotos vom Fehlercode.
Agentin: Ich leite den Fall an die regionale Technikleitung weiter. Sie erhalten innerhalb von 48 Stunden einen Rückruf.
Kunde: Und falls niemand anruft?
Agentin: Dann schreiben Sie an eskalation@elektroplus.example und nennen die Ticket-ID, die ich Ihnen jetzt nenne: T-88314.
Kunde: Gut. Bitte notieren Sie auch, dass Lebensmittel verdorben sind.""",
        """客服：ElektroPlus 客服，我是 Sara。有何可幫忙？
顧客：冰箱維修後又故障。我要升級處理。
客服：了解。有工單號碼嗎？
顧客：有，A-44921。我也有錯誤碼照片。
客服：我會轉給區域技術主管。48 小時內會回电。
顧客：若沒人打呢？
客服：請寫信至 eskalation@elektroplus.example，並提及我現在給您的工單 T-88314。
顧客：好。也請註記有食品損壞。""",
        [n("erneut ausgefallen", "再次故障"), n("Eskalation", "升級處理"), n("Auftragsnummer", "工單／委託編號"), n("leite … weiter", "轉交", "weiterleiten。"), n("Rückruf", "回电"), n("verdorben", "變質／損壞"), n("Ticket-ID", "工單代碼")],
        [p("Ich möchte eine Eskalation", "要求升級", "Ich möchte mit einer Leitung sprechen."), p("Falls niemand …, dann …", "備案", "Falls niemand antwortet, schreibe ich erneut.")],
        ["申訴對話：問題→編號→時限→備案→損害。", "weiterleiten 可分動詞。"],
        ["消費", "客服", "權益"],
    ),
    item(
        "b1-79", "B1", "email", "社團經費報銷",
        "Abrechnung Vereinsausflug", "社團出遊報銷",
        """Betreff: Abrechnung Tagesausflug 22. Juni

Liebe Kassiererin Lea,

anbei die Abrechnung unseres Ausflugs: Bahn 186 €, Museumseintritt 120 €, Picknick 64 € – Summe 370 €.
Einnahmen aus Teilnehmerbeiträgen: 15 × 20 € = 300 €.
Differenz 70 € bitte aus der Projektkasse erstatten; Belege sind gescannt angehängt.

Zwei Personen sind krankheitsbedingt ausgefallen; ihre Beiträge habe ich zurücküberwiesen.
Falls die Kasse die Differenz erst im nächsten Monat verbuchen kann, gib mir kurz Bescheid.

Danke und sportliche Grüße
Milan""",
        """主旨：6 月 22 日出遊結算

出納 Lea 你好，

附上出遊結算：火車 186€、博物館 120€、野餐 64€——合計 370€。
學員繳費收入：15×20€＝300€。
差額 70€ 請從專案帳戶報支；收據已掃描附上。

兩人因病缺席；我已退還其費用。
若帳戶要到下月才能入帳，請短訊告知。

謝謝，運動社團問候
Milan""",
        [n("Abrechnung", "結算"), n("anbei", "附件隨信"), n("Teilnehmerbeiträge", "參加費"), n("Differenz", "差額"), n("erstatten", "報銷／退還"), n("krankheitbedingt", "因病"), n("verbuchen", "入帳")],
        [p("anbei die Abrechnung …", "附上結算", "Anbei die Quittungen."), p("Falls …, gib mir kurz Bescheid", "條件＋通知", "Falls es hakt, gib mir Bescheid.")],
        ["報銷信：支出→收入→差額→例外→彈性。", "anbei 很常用於附件。"],
        ["社團", "財務", "行政"],
    ),
    item(
        "b1-80", "B1", "notice", "腳踏車棚改建",
        "Umbau der Fahrradgarage", "車棚改建",
        """An alle Mieterinnen und Mieter
Ab 5. Mai wird die Fahrradgarage umgebaut. Bis 20. Mai stehen nur 20 Ersatzbügel im Innenhof zur Verfügung.
Bitte kennzeichnen Sie Ihr Rad mit Name und Wohnung und schließen Sie es tagsüber nicht dauerhaft an Treppengeländer.
Lastenräder und Anhänger melden Sie bitte bis 2. Mai per Mail an hof@haus.example, damit wir Sonderflächen zuweisen.
In der Bauphase kann es zu Lärm zwischen 8 und 17 Uhr kommen.
Nach Abschluss erhalten alle eine neue Stellplatznummer.
Wir danken für Kooperation und kurze Wege bei Rückfragen an die Hausverwaltung.""",
        """給全體房客
自 5 月 5 日起改建腳踏車棚。至 5 月 20 日僅中庭 20 個臨時車架可用。
請在車上標示姓名與房號，白天勿長時間鎖在樓梯扶手。
大型載貨車與拖車請於 5 月 2 日前寄信 hof@haus.example，以便分配特別空間。
施工期間 8–17 點可能有噪音。
完工後每人會取得新車位編號。
感謝配合；問題請短洽物業。""",
        [n("Ersatzbügel", "臨時車架"), n("kennzeichnen", "標示"), n("Lastenräder", "載貨腳踏車"), n("zuweisen", "指派／分配"), n("Bauphase", "施工階段"), n("Stellplatznummer", "車位編號"), n("Kooperation", "合作／配合")],
        [p("Ab … wird … umgebaut", "工程起點", "Ab Montag wird die Straße saniert."), p("damit wir …", "目的從句", "damit wir planen können")],
        ["住戶公告：工期→替代→例外車種→噪音→收尾。", "damit 表目的。"],
        ["住房", "交通", "公告"],
    ),
    item(
        "b1-81", "B1", "story", "遠距面試文化",
        "Vorstellungsgespräch online", "線上面試",
        """Mein erstes Online-Vorstellungsgespräch fühlte sich an wie eine Mischung aus Prüfung und Techniktest.
Ich prüfte Kamera, Licht und Headset eine Stunde vorher und legte Notizen außerhalb des Bildes bereit.
Trotzdem hakte der Ton einmal; ich sagte ruhig Bescheid und wechselte aufs Handy-Hotspot.
Die Kommission stellte verhaltensorientierte Fragen zu Konflikten im Team.
Ich antwortete mit Situation–Handlung–Ergebnis und fragte am Ende nach Einarbeitungszeit und Weiterbildungsbudget.
Später merkte ich, dass Blickkontakt in die Linse wichtiger war als auf die eigenen Kacheln zu starren.
Ob ich die Stelle bekomme, weiß ich noch nicht – aber die Vorbereitung war trotzdem wertvoll.""",
        """我的第一次線上面試像考試與技術測試的混合。
我提前一小時檢查鏡頭、光線與耳機，並把筆記放在畫面外。
音訊仍卡過一次；我平靜說明並改用手機熱點。
委員會問團隊衝突等行為事例題。
我用情境–行動–結果回答，最後詢問到職輔導與進修預算。
後來發現看鏡頭比盯著自己的小視窗更重要。
是否錄取尚不知——但準備本身仍有價值。""",
        [n("fühlte sich an wie", "感覺像……"), n("hakte", "卡住／不順"), n("Hotspot", "熱點分享"), n("verhaltensorientierte Fragen", "行為事例題"), n("Einarbeitungszeit", "到職適應期"), n("Kacheln", "視訊小窗格"), n("Linse", "鏡頭")],
        [p("fühlte sich an wie …", "主觀感受", "Es fühlte sich an wie Chaos."), p("Ob …, weiß ich noch nicht – aber …", "開放結局", "Ob es klappt, weiß ich nicht – aber ich lernte viel.")],
        ["面試敘事：準備→突發→回答結構→反思。", "Situation–Handlung–Ergebnis 可遷移。"],
        ["求職", "科技", "溝通"],
    ),
    item(
        "b1-82", "B1", "email", "社團場地租借",
        "Raumanfrage für Lesung", "朗讀會場地租借",
        """Betreff: Anfrage Gemeinschaftsraum 19. November

Sehr geehrte Damen und Herren,

der Literaturkreis „Seitenwind“ möchte am 19. November, 19–21:30 Uhr, den Gemeinschaftsraum für eine öffentliche Lesung nutzen.
Erwartet werden etwa 40 Gäste; wir bringen eigene Technik mit und verpflichten uns zur Reinigung.

Benötigt werden Stuhlreihen, zwei Mikrofone und Zugang zur Küche für Wasser.
Eintritt ist frei; Spenden kommen einem Alphabetisierungsprojekt zugute.

Bitte teilen Sie uns Verfügbarkeit, Nutzungsgebühr und Schlüsselübergabe mit.
Für Rückfragen bin ich unter 0151 222 778 erreichbar.

Mit freundlichen Grüßen
Paula Kranz
Organisation Seitenwind""",
        """主旨：11 月 19 日交誼廳詢問

諸位鈞鑒，

文學圈「Seitenwind」希望於 11 月 19 日 19–21:30 借用交誼廳舉辦公開朗讀。
預計約 40 位來賓；我們自備器材並承諾清理。

需要椅列、兩支麥克風及廚房用水。
免費入場；捐款將捐給識字計畫。

請告知空檔、使用費與鑰匙交接。
聯絡電話 0151 222 778。

此致問候
Paula Kranz
Seitenwind 籌備""",
        [n("Anfrage", "詢問／洽詢"), n("verpflichten uns", "我們承諾"), n("Stuhlreihen", "成排座椅"), n("zugute kommen", "惠及／用於"), n("Alphabetisierungsprojekt", "識字計畫"), n("Nutzungsgebühr", "使用費"), n("Schlüsselübergabe", "鑰匙交接")],
        [p("möchte … nutzen", "提出借用", "Wir möchten die Halle nutzen."), p("Bitte teilen Sie uns A, B und C mit", "一次索取多項資訊", "Bitte teilen Sie uns Termin und Kosten mit.")],
        ["租借信：活動簡介→需求→公益→請對方回覆項目。", "zugute kommen＝使受益。"],
        ["文化", "行政", "社團"],
    ),
    item(
        "b1-83", "B1", "notice", "資料保存期限",
        "Aufbewahrung von Bewerbungsunterlagen", "求職資料保存",
        """Hinweis Datenschutz / Personal
Unaufgefordert eingesandte Bewerbungsunterlagen werden maximal sechs Monate gespeichert, sofern kein Einstellungsverfahren eröffnet wird.
Nach Ablauf werden Dateien gelöscht und Papierunterlagen datenschutzgerecht vernichtet.
Bewerberinnen und Bewerber können früher Löschung verlangen; schreiben Sie an datenschutz@org.example.
Im laufenden Verfahren gelten längere Fristen gemäß berechtigtem Interesse und gesetzlichen Nachweispflichten.
Bitte verzichten Sie auf die Zusendung besonders sensibler Gesundheitsdaten, sofern nicht ausdrücklich gefordert.
Diese Information ersetzt die Fassung vom März.""",
        """資料保護／人事提醒
未經請求寄來的履歷資料最多保存六個月，除非已開啟錄用程序。
期滿後檔案刪除，紙本依個資規範銷毀。
應徵者可要求提早刪除：請寫信 datenschutz@org.example。
程序進行中依正當利益與法定舉證義務適用較長保存期。
除非明確要求，請勿寄送特別敏感的健康資料。
本資訊取代三月版本。""",
        [n("Unaufgefordert", "未經請求地"), n("sofern kein …", "除非沒有……"), n("datenschutzgerecht", "符合個資規範地"), n("vernichtet", "銷毀"), n("berechtigtem Interesse", "正當利益"), n("Nachweispflichten", "舉證／證明義務"), n("verzichten auf", "放棄／不要做")],
        [p("werden maximal … gespeichert, sofern …", "保存規則", "werden 30 Tage gespeichert, sofern …"), p("Bitte verzichten Sie auf …", "禁止／勸阻", "Bitte verzichten Sie auf Anhänge über 10 MB.")],
        ["個資公告：保存→刪除→權利→例外→敏感資料。", "sofern 表條件。"],
        ["法律", "求職", "個資"],
    ),
    item(
        "b1-84", "B1", "dialogue", "醫院出院說明",
        "Entlassgespräch", "出院說明",
        """Ärztin: Sie können morgen entlassen werden, wenn die Blutwerte stabil bleiben.
Patient: Darf ich wieder Sport machen?
Ärztin: Leichte Spaziergänge ja; Training erst nach der Kontrolle in zehn Tagen.
Patient: Welche Medikamente sind neu?
Ärztin: Ein Blutverdünner morgens, und bei Schmerzen das bekannte Mittel – nicht zusammen mit Alkohol.
Patient: Und falls die Schwellung zurückkommt?
Ärztin: Dann kommen Sie sofort in die Notaufnahme und bringen den Arztbrief mit.
Patient: Verstanden. Bekomme ich eine AU-Bescheinigung für die Arbeit?
Ärztin: Ja, für sieben Tage; Verlängerung über Ihre Hausärztin.""",
        """醫師：若血值穩定，明天可出院。
病人：可以恢復運動嗎？
醫師：慢走可以；正式訓練等十天後回診。
病人：哪些藥是新的？
醫師：早上一種抗凝血藥；疼痛用原本的藥——不可與酒同用。
病人：若腫脹復發呢？
醫師：立刻去急診並帶醫師摘要。
病人：明白。能開工作病假單嗎？
醫師：可以，七天；延期請找家庭醫師。""",
        [n("entlassen werden", "出院"), n("Blutwerte", "血液數值"), n("Blutverdünner", "抗凝血藥"), n("Schwellung", "腫脹"), n("Notaufnahme", "急診"), n("Arztbrief", "醫師摘要／出院病摘"), n("AU-Bescheinigung", "失能／病假證明")],
        [p("Sie können …, wenn …", "出院條件", "Sie können gehen, wenn die Werte passen."), p("Falls …, dann kommen Sie sofort …", "警示路徑", "Falls Fieber kommt, rufen Sie an.")],
        ["醫療對話：條件→限制→藥物→緊急→公文。", "AU＝Arbeitsunfähigkeit。"],
        ["健康", "醫療", "溝通"],
    ),
    item(
        "b1-85", "B1", "story", "城市農園等待名單",
        "Warteliste für den Gemeinschaftsgarten", "社區農園候補",
        """Als ich mich für den Gemeinschaftsgarten anmeldete, landete ich auf Platz 47 der Warteliste.
Statt zu warten, half ich bei Arbeitseinsätzen: Beete vorbereiten, Kompost wenden, Schuppen streichen.
Dadurch lernte ich Regeln, Werkzeuge und – wichtiger – Leute kennen.
Nach einem Jahr rückte ich auf; eine Parzelle wurde frei, weil jemand umzog.
Heute ziehe ich Tomaten und Kräuter und gebe Überschüsse an die Nachbarschaftstafel.
Die Wartezeit fühlte sich nicht mehr sinnlos an, weil ich schon Teil der Praxis war.
Manchmal ist der Umweg die eigentliche Mitgliedschaft.""",
        """我報名社區農園時，候補排到第 47。
我沒乾等，而是參加勞動日：整畦、翻堆肥、油漆小棚。
因此學會規則、工具——更重要的是認識人。
一年後往前排；有人搬家空出一小區。
如今我種番茄與香草，多餘的放到鄰里食物架。
等待不再顯得無意義，因為我已參與實作。
有時繞路才是真正的入會。""",
        [n("landete ich auf", "落到（某個名次）"), n("Arbeitseinsätzen", "勞動／志工出勤"), n("Kompost wenden", "翻堆肥"), n("rückte ich auf", "往前遞補"), n("Parzelle", "小塊園區"), n("Überschüsse", "多餘收成"), n("Nachbarschaftstafel", "鄰里食物分享架")],
        [p("Statt zu warten, half ich …", "主動替代", "Statt zu klagen, handelte ich."), p("Manchmal ist der Umweg …", "反思金句", "Manchmal ist der Umweg die Lösung.")],
        ["敘事弧：候補→參與→遞補→意義重構。", "aufrücken＝往前遞補。"],
        ["社區", "永續", "等待"],
    ),
]


# ═══════════════════════════════════════════════════════════════════
# B2 71–85  (~1000–1400 chars)
# ═══════════════════════════════════════════════════════════════════
B2 = [
    item(
        "b2-71", "B2", "story", "住房政策",
        "Belegungsbindungen und soziale Mischung", "配住義務與社會混合",
        """Belegungsbindungen gelten als Instrument, um in angespannten Wohnungsmärkten Einkommensschwächere zu schützen. Gleichzeitig wird kontrovers diskutiert, ob feste Quoten soziale Mischung erzeugen oder vielmehr Stigmatisierung einzelner Adressen verstärken. Empirisch zeigt sich: Bindungen wirken nur, wenn Neubau und Bestandsmodernisierung parallel laufen und Kontrollen nicht rein symbolisch bleiben.

Kritikerinnen monieren Bürokratiekosten und Ausweichreaktionen von Eigentümern, die Wohnungen dem Markt entziehen oder befristete Verträge bevorzugen. Befürworter entgegnen, ohne bindende Regeln verschiebe sich die Last vollständig auf Transferleistungen und lange Pendelwege. Eine differenzierte Steuerung verknüpft daher Bindungsdauer mit Förderhöhe und prüft regelmäßig, ob Zielgruppen tatsächlich erreicht werden.

Hinzu kommt die Frage der Nachbarschaftsqualität: Soziale Mischung entsteht nicht allein durch Belegungsschlüssel, sondern durch Schulen, ÖPNV und Treffpunkte. Wer nur Kontingente festschreibt, ohne Infrastruktur mitzudenken, riskiert parallele Lebenswelten hinter derselben Hausnummer. Insofern ist Wohnungspolitik Stadtpolitik.

Ob digitale Wartelisten Transparenz erhöhen oder neue Zugangshürden schaffen, hängt von Beratung und Sprachmittlung ab. Es bleibt abzuwarten, inwiefern Kommunen Evaluationen öffentlich machen und Fehlsteuerungen korrigieren, bevor Bindungen rein administrativ weiterlaufen.""",
        """配住義務被視為在緊繃房市中保護收入較弱者的工具。同時也有爭議：固定配額究竟促成社會混合，還是強化特定地址的污名。經驗顯示：唯有新建與存量更新並行、且監管不只是象徵，義務才真正有效。

批評者指摘行政成本與房東規避——把房子撤出市場或偏好定期契約。支持者反駁：沒有拘束規則，負擔會完全轉到津貼與長距離通勤。細緻治理因此把義務年限與補助金額連結，並定期檢查是否真的觸及目標族群。

還有鄰里品質問題：社會混合不只靠配住公式，也靠學校、大眾運輸與聚會點。只寫名額、不思基礎設施，可能讓同一門牌後出現平行生活世界。因此住房政策即城市政策。

數位候補名單是提高透明還是製造新門檻，取決於諮詢與語言中介。各市是否公開評估並在義務空轉前修正偏差，仍有待觀察。""",
        [n("Belegungsbindungen", "配住／入住資格拘束"), n("Einkommensschwächere", "收入較弱者"), n("Stigmatisierung", "污名化"), n("Ausweichreaktionen", "規避反應"), n("Transferleistungen", "移轉支付／津貼"), n("Belegungsschlüssel", "配住公式"), n("Zugangshürden", "進入門檻")],
        [p("gelten als …; gleichzeitig wird kontrovers diskutiert", "定義＋爭議", "gelten als Lösung; gleichzeitig bleibt Skepsis."), p("Wer nur A, ohne B, riskiert C", "條件風險", "Wer nur spart, ohne zu investieren, riskiert Qualität."), p("Es bleibt abzuwarten, inwiefern …", "開放展望", "Es bleibt abzuwarten, inwiefern Reformen greifen.")],
        ["住房論述：工具→反論→基礎設施→數位治理。", "抓住『混合≠公式』的轉折。", "注意名詞化：Belegungsbindung、Förderhöhe。"],
        ["住房", "政策", "社會", "論述"],
    ),
    item(
        "b2-72", "B2", "email", "學術倫理",
        "Stellungnahme zu Plagiatsvorwurf", "針對抄襲指控之說明",
        """Betreff: Stellungnahme zur Prüfung meiner Masterarbeit

Sehr geehrte Mitglieder der Prüfungskommission,

hiermit nehme ich zu dem Vorwurf unzureichender Kennzeichnung Stellung. Ich bedauere, dass drei Absätze in Kapitel 4 die Herkunft paraphrasierter Passagen nicht klar genug ausweisen. Eine Absicht der Täuschung lag nicht vor; gleichwohl trage ich die Verantwortung für die Endfassung.

Ich bitte darum, eine überarbeitete Version mit vollständiger Quellenangabe und einer dokumentierten Änderungsliste einreichen zu dürfen. Zusätzlich schlage ich ein Gespräch mit der Ombudsstelle für gute wissenschaftliche Praxis vor, um Méthodik und Zitierstandards zu klären.

Die Rohdaten und Zwischenstände meiner Literaturverwaltung stelle ich auf Anfrage zur Verfügung. Sollte die Kommission eine mündliche Erörterung für erforderlich halten, stehe ich innerhalb von zehn Werktagen zur Verfügung.

Mir ist bewusst, dass wissenschaftliche Integrität Vertrauensgut ist. Ich bitte um eine faire, dokumentierte Prüfung und um Mitteilung des weiteren Verfahrenswegs.

Mit freundlichen Grüßen
Dr. cand. Hana Voigt""",
        """主旨：針對碩士論文審查之說明

考試委員會諸位委員鈞鑒，

謹此就「標註不足」之指控提出說明。我遺憾第 4 章有三段改寫段落的出處標示不夠清楚。並無欺騙意圖；但我仍對定稿負責。

懇請允許提交附完整出處與變更清單的修訂版。另建議與學術誠信監察辦公室面談，釐清方法與引用標準。

文獻管理之原始資料與中間版本可應要求提供。若委員會認為需要口頭說明，我可於十個工作日內出席。

我明白學術誠信是信任資產。懇請公平、可追溯之審查，並告知後續程序。

此致問候
博士候選人 Hana Voigt""",
        [n("Stellungnahme", "立場說明／書面回應"), n("unzureichender Kennzeichnung", "標註不足"), n("paraphrasierter Passagen", "改寫段落"), n("Täuschung", "欺瞞"), n("Ombudsstelle", "監察／誠信辦公室"), n("Änderungsliste", "變更清單"), n("Vertrauensgut", "信任資產／信任財")],
        [p("hiermit nehme ich zu … Stellung", "正式回應指控", "Hiermit nehme ich zu den Vorwürfen Stellung."), p("Ich bitte darum, … zu dürfen", "請求許可", "Ich bitte darum, nachzureichen."), p("Sollte …, stehe ich … zur Verfügung", "條件配合", "Sollte ein Gespräch nötig sein, stehe ich bereit.")],
        ["學術正式信：承認範圍→無意圖但負責→補救→配合調查。", "區分 paraphrasieren 與 kopieren。", "Vertrauensgut 屬高階措辭。"],
        ["學術", "倫理", "正式郵件", "程序"],
    ),
    item(
        "b2-73", "B2", "notice", "氣候",
        "Kommunale Hitzeaktionsplan – Stufe Orange", "市政防暑行動計畫－橘色等級",
        """Öffentliche Bekanntmachung – Hitzeaktionsplan Stufe Orange
Ab sofort bis auf Widerruf gilt Stufe Orange. Die Gesundheitsverwaltung empfiehlt: schwere körperliche Arbeit im Freien auf Morgen- und Abendstunden verlagern, regelmäßig trinken, direkte Sonne meiden. Kühlräume in Bibliotheken und Bürgerämtern sind verlängert geöffnet (Liste unter stadt.example/hitze).

Pflegeeinrichtungen und Schulen aktivieren ihre internen Protokolle; Angehörige werden gebeten, alleinlebende ältere Personen telefonisch zu erreichen. Veranstaltungen mit mehr als 500 Personen im Außenbereich bedürfen einer Kurzprüfung durch Ordnungsamt und Sanitätsdienst.

Arbeitgeberinnen und Arbeitgeber sind angehalten, Pausenregelungen anzupassen und besonders schutzbedürftige Beschäftigte nicht in der Mittagshitze einzusetzen. Verstöße gegen arbeitsschutzrechtliche Vorgaben können geprüft werden.

Bitte beachten Sie, dass Notrufnummern nur für akute Notfälle zu nutzen sind; allgemeine Beratung unter 115. Diese Mitteilung ersetzt keine individuellen ärztlichen Empfehlungen und wird bei Entspannung der Wetterlage zurückgestuft.""",
        """公開公告－防暑行動計畫橘色等級
即日起至另行通知適用橘色等級。衛生單位建議：戶外重體力改到早晚、定時喝水、避免直射陽光。圖書館與市民局之涼空間延長開放（清單見 stadt.example/hitze）。

長照與學校啟動內部程序；請親屬電話聯繫獨居長者。室外超過 500 人活動須經秩序機關與急救單位簡核。

雇主應調整休息規定，避免在正午高溫指派特別需保護的員工。違反職業安全規定者可受檢查。

請注意緊急電話僅供急性危難；一般諮詢打 115。本公告不取代個人醫囑，天氣緩和後將降級。""",
        [n("bis auf Widerruf", "直至另行撤回／通知"), n("verlagern", "轉移"), n("Kühlräume", "降溫／避暑空間"), n("schutzbedürftige Beschäftigte", "特別需保護的受僱者"), n("angehalten", "被要求／被敦促"), n("arbeitsschutzrechtliche Vorgaben", "職業安全法規要求"), n("zurückgestuft", "降級")],
        [p("Ab sofort bis auf Widerruf gilt …", "即時生效條款", "Ab sofort gilt die Regelung."), p("sind angehalten, …", "官方敦促", "sind angehalten, Pausen zu verlängern"), p("bedürfen einer …", "需要許可／審查", "bedürfen einer Genehmigung")],
        ["市政公告：等級→建議→機構→雇主→熱線。", "bis auf Widerruf 常見於緊急措施。", "被動與官方語氣：sind angehalten。"],
        ["氣候", "公共衛生", "行政", "公告"],
    ),
    item(
        "b2-74", "B2", "dialogue", "媒體素養",
        "Podium: Deepfakes und Verantwortung", "論壇：深偽與責任",
        """Moderatorin: Frau Liao, reichen Plattform-Kennzeichnungen gegen Deepfakes?
Liao: Kennzeichnungen helfen, greifen aber zu spät, wenn Inhalte bereits viral sind. Wir brauchen vorgeschaltete Risikoanalysen bei reichweitenstarken Konten und klare Fristen für Entfernung nachweislich manipulierter Wahlwerbung.
Journalist Berg: Löschungen können jedoch journalistische Dokumentation erschweren.
Liao: Deshalb unterscheiden wir zwischen Kontextualisierung und Löschung. Zum einen bleiben Archive mit Warnhinweis zugänglich; zum anderen entfällt die algorithmische Empfehlung.
Berg: Wer definiert „nachweislich“?
Liao: Unabhängige Fachstellen plus Widerspruchsverfahren. Reine Unternehmensentscheidungen ohne Revision erzeugen Misstrauen – und Misstrauen ist selbst ein Demokratierisiko.
Moderatorin: Was ist mit satirischen Formen?
Liao: Satire bleibt geschützt, sofern sie als solche erkennbar ist oder bei Nachfrage kennzeichnet. Unkenntlichkeit ist kein Freibrief.
Berg: Klingt nach hohem Aufwand.
Liao: Der Aufwand entsteht ohnehin – entweder als Prävention oder als gesellschaftliche Reparatur nach Skandalen.""",
        """主持人：Liao 女士，平台標示足以對抗深偽嗎？
Liao：標示有幫助，但內容已病毒傳播時往往太晚。需要對高流量帳號前置風險分析，並對可證明遭竄改的競選廣告設明確下架期限。
記者 Berg：但刪除可能妨礙新聞存證。
Liao：因此我們區分「加脈絡」與「刪除」。一方面檔案可帶警告保留；另一方面取消演算法推薦。
Berg：誰定義「可證明」？
Liao：獨立專業單位加上異議程序。沒有覆核的純企業決定會製造不信任——而不信任本身就是民主風險。
主持人：諷刺形式呢？
Liao：諷刺受保障，前提是可辨識或經詢問後標示。難以辨識不是尚方寶劍。
Berg：聽起來成本很高。
Liao：成本本來就會發生——要麼在預防，要麼在醜聞後的社會修復。""",
        [n("vorgeschaltete Risikoanalysen", "前置風險分析"), n("reichweitenstarken", "高觸及／高流量的"), n("Kontextualisierung", "脈絡化說明"), n("Widerspruchsverfahren", "異議／申訴程序"), n("Freibrief", "尚方寶劍／空白授權"), n("Prävention", "預防"), n("gesellschaftliche Reparatur", "社會修復")],
        [p("helfen, greifen aber zu spät, wenn …", "效果有限", "helfen, greifen aber zu kurz"), p("Zum einen …; zum anderen …", "雙軌方案", "Zum einen Archiv; zum anderen keine Empfehlung."), p("entweder als A oder als B", "成本轉移論", "entweder als Prävention oder als Reparatur")],
        ["媒體論壇：標示限制→存證兩難→認定機構→諷刺例外。", "抓住『不信任本身是風險』。", "nachweislich／erkennbarkeit 是關鍵詞。"],
        ["媒體", "民主", "科技", "對話"],
    ),
    item(
        "b2-75", "B2", "story", "勞動",
        "Tarifbindung und der Druck der Außenseiterkonkurrenz", "團體協約拘束與外部競爭壓力",
        """Tarifverträge stabilisieren Löhne und Planbarkeit, verlieren jedoch an Reichweite, wenn immer mehr Betriebe außerhalb der Bindung agieren. In Branchen mit hoher Fluktuation und Werkverträgen entsteht ein Unterbietungswettbewerb, der tarifgebundene Unternehmen strukturell benachteiligt. Beschäftigte spüren das als stagnierende Reallöhne trotz formaler Mindeststandards.

Gegner verpflichtender Tarifbindung warnen vor Flexibilitätsverlust und Standortflucht. Das Argument verdient Ernsthaftigkeit: starre Regelungen ohne Öffnungsklauseln können Anpassungen in Krisen erschweren. Dennoch ersetzt Freiwilligkeit allein selten kollektive Verhandlungsmacht, besonders wo Personalvertretungen schwach sind. Eine kluge Ordnungspolitik kombiniert Anreize zur Mitgliedschaft mit Transparenzpflichten bei öffentlicher Auftragsvergabe.

Auch Qualifizierung gehört in dieses Bild. Wo Tarife nur Preise setzen, aber Weiterbildung fehlt, wandert Wertschöpfung ab. Betriebsräte und Kammern können Lernzeitkonten und branchenweite Umschulungen verankern. Internationaler Preisdruck verschwindet dadurch nicht, wird aber gestaltbarer.

Insofern ist die Debatte weniger „Markt gegen Staat“ als Frage institutioneller Lernfähigkeit. Ob Gesetzgeber Mindestabdeckungsquoten einführen oder eher vergaberechtliche Hebel nutzen, wird die Verteilung von Risiken zwischen Stammbelegschaften und Randbeschäftigten spürbar verschieben.""",
        """團體協約能穩定薪資與可預期性，但若愈來愈多企業游離於拘束之外，其覆蓋就萎縮。在高流動與承攬契約盛行的產業，會出現削價競爭，使受協約拘束的企業結構性吃虧。勞工感受到的是：即使有形式最低標準，實質薪資仍停滯。

反對強制性協約拘束者警告失去彈性與產業外移。這論點值得認真：沒有開放條款的僵硬規定，會讓危機調適變難。但僅靠自願很少能取代集體談判力，尤其在員工代表薄弱之處。精明的秩序政策會把入會誘因與政府採購透明度義務結合。

培訓也屬同一圖像。若協約只訂價格、沒有進修，價值創造會流失。企業委員會與公會可把學習時數帳戶與全產業轉業訓練寫進制度。國際價格壓力不會消失，但變得較可塑造。

因此辯論比較不像「市場對國家」，而是制度學習能力問題。立法者要採最低覆蓋率還是採購法槓桿，將明顯改寫核心員工與邊緣就業之間的風險分配。""",
        [n("Tarifbindung", "團體協約拘束"), n("Unterbietungswettbewerb", "削價競爭"), n("Reallöhne", "實質薪資"), n("Öffnungsklauseln", "開放／例外條款"), n("Auftragsvergabe", "公共採購／發包"), n("Lernzeitkonten", "學習時數帳戶"), n("Stammbelegschaften", "核心／正職員工")],
        [p("stabilisieren A, verlieren jedoch an B, wenn …", "功能＋條件失效", "stärken Sicherheit, verlieren an Reichweite, wenn …"), p("Das Argument verdient Ernsthaftigkeit: … Dennoch …", "承認後推進", "Das Argument zählt: … Dennoch bleibt …"), p("weniger A als B", "重新框定辯論", "weniger Ideologie als Handwerk")],
        ["勞動論述：覆蓋萎縮→反論彈性→培訓→制度學習。", "注意複合名詞：Unterbietungswettbewerb。", "對照 Stamm vs Randbeschäftigte。"],
        ["勞動", "經濟", "政策", "論述"],
    ),
    item(
        "b2-76", "B2", "email", "消費爭議",
        "Fristsetzung vor Widerruf eines Vertrags", "撤回契約前之期限設定",
        """Betreff: Letzte Frist zur Nachbesserung – Vorgang K-77201

Sehr geehrte Damen und Herren,

trotz zweier Reparaturversuche vom 3. und 21. Februar weist das gelieferte E-Bike weiterhin den beschriebenen Bremsdefekt auf. Eine weitere Nutzung ist aus Sicherheitsgründen nicht zumutbar.

Ich setze Ihnen hiermit eine letzte Frist bis 18. April, den Mangel fachgerecht zu beheben oder gleichwertigen Ersatz zu liefern. Sollte bis dahin keine nachweisbare Abhilfe erfolgen, werde ich vom Kaufvertrag zurücktreten und die Rückabwicklung sowie Ersatz etwaiger Gutachterkosten verlangen.

Bitte bestätigen Sie den Eingang dieses Schreibens und nennen Sie mir eine Ansprechperson mit Durchwahl. Korrespondenz bevorzugt schriftlich an die unten genannte Adresse; telefonische Zusagen ohne Aktenzeichen erkenne ich nicht als verbindlich an.

Mit freundlichen Grüßen
Lars Meinhardt
Vorgang: K-77201 / Kauf vom 12. Januar""",
        """主旨：最後補正期限－案號 K-77201

諸位鈞鑒，

儘管 2 月 3 日與 21 日兩次維修，所交付之電動自行車仍有所述煞車缺陷。基於安全，無法再合理期待繼續使用。

謹此設定最後期限至 4 月 18 日：請專業排除瑕疵或交付同等替代。若屆時無可行救濟，我將解除買賣契約，要求回復原狀並請求可能鑑定費用之賠償。

請確認收悉本函，並告知分機聯絡人。通訊請以書面寄至下方地址；無案號之電話承諾，我不視為有拘束力。

此致問候
Lars Meinhardt
案號：K-77201／購買日 1 月 12 日""",
        [n("Nachbesserung", "補正／修理改善"), n("nicht zumutbar", "無法合理期待／不可苛求"), n("setze … eine letzte Frist", "設定最後期限"), n("Abhilfe", "救濟／改善措施"), n("zurücktreten", "解除／退出契約"), n("Rückabwicklung", "回復原狀／相互返還"), n("Aktenzeichen", "案號")],
        [p("Ich setze Ihnen hiermit eine letzte Frist bis …", "消費者期限函", "Ich setze eine Frist bis Freitag."), p("Sollte bis dahin keine …, werde ich …", "預告法律效果", "Sollte keine Zahlung erfolgen, werde ich mahnen."), p("erkenne ich nicht als verbindlich an", "拒絕口頭拘束", "erkenne ich nicht als Zusage an")],
        ["消費正式信：事實→最後期限→解除預告→通訊規則。", "zumutbar／Fristsetzung 是關鍵。", "書面優於電話：程序意識。"],
        ["消費", "法律", "正式郵件", "權益"],
    ),
    item(
        "b2-77", "B2", "story", "教育公平",
        "Digitale Endgeräte und die versteckte Hausaufgabe", "數位裝置與隱形作業",
        """Die Ausgabe von Tablets an Schulen gilt als Fortschritt. Doch ohne verlässliches Netz, ruhigen Arbeitsplatz und Unterstützung durch Erwachsene wird aus der digitalen Hausaufgabe eine soziale Auswahlprüfung. Kinder in beengten Wohnungen teilen sich Geräte; andere klicken sich durch Tutorials, während Eltern Schichtarbeit leisten und nicht helfen können.

Technische Ausstattung ohne didaktische Weiterbildung der Lehrkräfte multipliziert Zufall statt Qualität. Manche Schulen nutzen Plattformen kohärent, andere stapeln Apps ohne gemeinsame Regeln zu Datenschutz und Abgabefristen. Die Folge sind ungleich verteilte Feedbackschleifen: Wer früh stockt, bleibt unsichtbar, wenn Betreuungskapazität fehlt.

Skeptiker fordern weniger Bildschirmzeit. Das trifft ein reales Entwicklungsrisiko, ersetzt jedoch keine Antwort auf die Frage, wie grundlegende Kulturtechniken unter digitalen Bedingungen gerecht vermittelt werden. Eine seriöse Strategie kombiniert Geräte, Lernbegleitung und analoge Alternativen für Prüfungssituationen.

Schließlich braucht es Evaluation jenseits von Gerätezahlen: Lernzuwachs, Belastung und Beteiligung von Eltern mit geringer Digitalkompetenz. Andernfalls bleibt Digitalisierung eine sichtbare Investition mit unsichtbarer Selektion.""",
        """學校發放平板被視為進步。但若沒有穩定網絡、安靜工作空間與成人支持，數位作業會變成社會篩選考。擁擠住房的孩子共用裝置；另一些人能順暢跟著教學影片，而輪班父母無法協助。

只有設備、沒有教師教學進修，是把偶然加倍而非提升品質。有的學校一貫使用平台，有的堆疊 App 卻缺乏個資與繳交期限的共同規則。結果是回饋迴路分配不均：早卡住的人，在輔導能量不足時就隱形。

懷疑者要求減少螢幕時間。這點中真實發展風險，但仍未回答：在數位條件下如何公平傳授基本文化技能。嚴謹策略應結合裝置、學習陪伴，以及考試情境的類比替代。

最後需要超越「發放數量」的評估：學習增益、負荷，以及數位能力較弱家長的參與。否則數位化只是看得見的投資，看不見的篩選。""",
        [n("verlässliches Netz", "穩定網絡"), n("beengten Wohnungen", "擁擠住宅"), n("didaktische Weiterbildung", "教學法進修"), n("Feedbackschleifen", "回饋迴路"), n("Kulturtechniken", "基本文化技能（讀寫算等）"), n("analoge Alternativen", "非數位替代方案"), n("Selektion", "篩選")],
        [p("gilt als A. Doch ohne B wird C", "表面進步＋條件翻轉", "gilt als Hilfe. Doch ohne Beratung wird es Ausschluss."), p("multipliziert A statt B", "效果批判", "multipliziert Zufall statt Qualität"), p("Andernfalls bleibt A eine B mit C", "警告收尾", "Andernfalls bleibt Reform Symbolpolitik")],
        ["教育公平：裝置≠機會→教學能力→螢幕懷疑→評估指標。", "抓住『隱形作業／隱形篩選』。", "名詞化：Digitalkompetenz、Betreuungskapazität。"],
        ["教育", "數位化", "公平", "論述"],
    ),
    item(
        "b2-78", "B2", "notice", "交通",
        "Temporäre Fußgängerzone – Verkehrsversuch", "臨時行人區－交通試驗",
        """Bekanntmachung Ordnungsamt
Vom 1. Juni bis 30. September wird die Mittelstraße zwischen Kirchplatz und Bahnhofstraße als Fußgängerzone im Verkehrsversuch geführt. Ziel ist die Prüfung von Aufenthaltsqualität, Einzelhandelsfrequenzen und Rettungswegen.

Lieferverkehr ist täglich 6–11 Uhr freigegeben; außerhalb dieses Fensters nur mit Sondergenehmigung. Anliegern bleibt die Zufahrt zu Tiefgaragen über die Parallelstraße erhalten. Der ÖPNV nutzt eine umgeleitete Linie; Fahrpläne liegen in den Stationen und unter stadt.example/versuch.

Einwendungen und Beobachtungen können bis 15. Oktober über das Online-Formular eingereicht werden. Die Auswertung erfolgt unabhängig und wird öffentlich vorgestellt, bevor über eine Verstetigung entschieden wird. Ordnungswidrigkeiten – insbesondere unzulässiges Befahren – werden konsequent geahndet.

Diese Anordnung tritt am 1. Juni in Kraft und ersetzt die vorläufige Sperrung vom Mai. Bei Großveranstaltungen bleiben gesonderte Hinweise vorbehalten.""",
        """秩序機關公告
6 月 1 日至 9 月 30 日，Mittelstraße 於教堂廣場與車站街之間進行行人區交通試驗。目標是檢視停留品質、零售人流與救援動線。

送貨每日 6–11 點開放；時段外僅限特別許可。住戶進出地下車庫改由平行街。大眾運輸改線；時刻表見站點與 stadt.example/versuch。

異議與觀察可於 10 月 15 日前經線上表單提交。評估獨立進行並公開說明後，才決定是否常態化。違規行駛等秩序案件將一貫裁罰。

本命令 6 月 1 日生效，取代五月臨時封閉。大型活動另有通知。""",
        [n("Verkehrsversuch", "交通試驗"), n("Aufenthaltsqualität", "停留／休憩品質"), n("freigegeben", "開放通行"), n("Sondergenehmigung", "特別許可"), n("Anliegern", "沿街住戶／鄰地使用人"), n("Verstetigung", "常態化／永久化"), n("geahndet", "被裁罰")],
        [p("wird … als … geführt", "試驗定性", "wird als Pilotprojekt geführt"), p("Einwendungen … können … eingereicht werden", "公民參與", "Stellungnahmen können eingereicht werden"), p("tritt … in Kraft und ersetzt …", "生效與取代", "tritt am 1. Mai in Kraft")],
        ["交通公告：試驗目的→通行例外→參與→裁罰→生效。", "Verstetigung＝是否永久。", "被動語態密度高，適合考場。"],
        ["交通", "城市", "行政", "公告"],
    ),
    item(
        "b2-79", "B2", "story", "健康資料",
        "Wearables, Einwilligung und asymmetrische Transparenz", "穿戴裝置、同意與不對稱透明",
        """Fitnessarmbänder versprechen Selbstermächtigung durch Daten. Gleichzeitig wandern Messwerte in Ökosysteme, deren Nutzungsbedingungen selten im Alltag gelesen werden. Die Einwilligung ist formal vorhanden, materiell jedoch oft asymmetrisch: Nutzerinnen sehen Schritte und Puls, Anbieter sehen Muster über Populationen und Zeit.

Für Versicherungen und Arbeitgeberinnen sind Aggregatdaten reizvoll, weil sie Risiken kalkulierbarer machen. Genau dort entsteht Druck zu „freiwilliger“ Freigabe, die sozial kaum frei bleibt, wenn Prämien oder Aufstiegschancen implizit daran hängen. Datenschutzrecht setzt Grenzen, ersetzt aber keine öffentliche Debatte über zumutbare Transparenz.

Technisch ließen sich Daten minimieren, anonymisieren und lokal verarbeiten. Ökonomisch siegt jedoch häufig das Modell, Rohdaten zu speichern „für spätere Features“. Diese Zukunftsoption ist aus Sicht der Produktentwicklung rational – aus Sicht informationaler Selbstbestimmung riskant.

Eine reife Praxis würde Widerruf so einfach machen wie die Erstanmeldung und unabhängige Audits sichtbar belohnen. Andernfalls bleibt Gesundheitstracking eine Geschichte von Kontrolle, die als Wellness erzählt wird.""",
        """健身手環以資料許諾自我賦權。同時，測量值流入日常很少被讀完的使用條款生態系。形式上有同意，實質卻常不對稱：使用者看到步數與心跳，業者看到跨族群與時間的模式。

對保險與雇主而言，彙總資料很有吸引力，因風險更可精算。正是在此出現「自願」授權壓力；當保費或升遷隱含與之掛鉤時，社會上幾乎不再自由。個資法設下界限，但取代不了對「可合理期待之透明」的公共辯論。

技術上可最小化、匿名化並在本機處理。經濟上卻常勝出「先存原始資料以備後續功能」的模型。對產品開發這是理性的未來選項——對資訊自主卻是風險。

成熟做法應讓撤回與初次註冊一樣簡單，並讓獨立稽核被看見且被獎勵。否則健康追蹤只是用 Wellness 敘事包裝的控制。""",
        [n("Selbstermächtigung", "自我賦權"), n("materiell jedoch oft asymmetrisch", "實質上卻常不對稱"), n("Aggregatdaten", "彙總資料"), n("implizit daran hängen", "隱含地掛鉤"), n("informationaler Selbstbestimmung", "資訊自主決定"), n("Widerruf", "撤回同意"), n("Audits", "稽核")],
        [p("formal …, materiell jedoch …", "形式／實質對照", "formal frei, materiell gebunden"), p("Genau dort entsteht Druck zu …", "指出結構壓力", "Genau dort entsteht Anreiz zu …"), p("Andernfalls bleibt A eine Geschichte von B, die als C erzählt wird", "批判收尾", "Andernfalls bleibt Flexibilität eine Geschichte von Risiko")],
        ["健康／科技論述：賦權承諾→不對稱→制度壓力→設計倫理。", "抓住 formal vs materiell。", "Wellness vs Kontrolle 的重新命名。"],
        ["健康", "科技", "個資", "論述"],
    ),
    item(
        "b2-80", "B2", "email", "職場歧視",
        "Beschwerde wegen benachteiligender Schichtpraxis", "針對不利輪班實務之申訴",
        """Betreff: Formelle Beschwerde – Benachteiligung bei Schichtvergabe

Sehr geehrte Mitglieder der Beschwerdestelle,

hiermit erhebe ich Beschwerde gegen die seit März praktizierte Schichtvergabe in Team Süd. Trotz gleicher Qualifikation erhalte ich überdurchschnittlich viele Spät- und Wochenenddienste, während Kolleginnen mit vergleichbarer Seniorität bevorzugt Frühschichten erhalten.

Ich habe die Ungleichverteilung am 12. und 28. April intern angesprochen; eine nachvollziehbare Kriterienliste wurde nicht vorgelegt. Die Praxis beeinträchtigt meine Weiterbildung abends und erzeugt den Eindruck mittelbarer Benachteiligung.

Ich beantrage: (1) Offenlegung der Vergabekriterien der letzten sechs Monate, (2) Neutralisierung der Dienste für die kommenden acht Wochen, (3) ein moderiertes Gespräch mit Führungskraft und Personalvertretung.

Unterlagen und Dienstpläne füge ich bei. Ich bitte um Eingangsbestätigung und um Mitteilung der Verfahrensschritte innerhalb von zwei Wochen.

Mit freundlichen Grüßen
Samira El-Sayed
Personalnummer 10422""",
        """主旨：正式申訴－輪班分配不利益

申訴單位諸位鈞鑒，

謹就南組自三月起之輪班分配提出申訴。在資格相同情況下，我被分配到高於平均的晚班與週末班，而資歷相當的同事較常取得早班。

我曾於 4 月 12、28 日內部提出；未獲可核對之標準清單。此做法影響我晚間進修，並造成間接不利益之印象。

我請求：(1) 公開近六個月分配標準，(2) 未來八週班表中立化重整，(3) 由主管與員工代表主持之調解談話。

值班表等資料附上。請確認收悉，並於兩週內告知程序步驟。

此致問候
Samira El-Sayed
員工編號 10422""",
        [n("hiermit erhebe ich Beschwerde", "謹此提出申訴"), n("überdurchschnittlich", "高於平均"), n("nachvollziehbare Kriterienliste", "可核對的標準清單"), n("mittelbarer Benachteiligung", "間接不利益／間接歧視"), n("Neutralisierung", "中立化重整"), n("moderiertes Gespräch", "有主持／調解的談話"), n("Eingangsbestätigung", "收件確認")],
        [p("hiermit erhebe ich Beschwerde gegen …", "正式申訴開場", "hiermit erhebe ich Einspruch gegen …"), p("Ich beantrage: (1) … (2) … (3) …", "條列請求", "Ich beantrage Akteneinsicht und Fristverlängerung."), p("erzeugt den Eindruck …", "審慎表述歧視印象", "erzeugt den Eindruck ungleicher Behandlung")],
        ["職場申訴：事實模式→已內部反映→具體請求→期限。", "mittelbar vs unmittelbar 歧視概念。", "語氣堅定但不謾罵。"],
        ["職場", "平等", "正式郵件", "程序"],
    ),
    item(
        "b2-81", "B2", "dialogue", "能源轉型",
        "Gespräch: Netzausbau und lokale Akzeptanz", "對話：電網擴建與在地接受度",
        """Moderator: Warum scheitern Trassen so oft an Protesten, Frau Okoro?
Okoro: Nicht am Klima­ziel, sondern an Verfahren, die Betroffene spät einbeziehen und Unsicherheit über Entschädigung lassen.
Bürgermeister Hein: Wir wollen Erneuerbare, aber keine Dauerbaustelle ohne greifbaren Nutzen vor Ort.
Okoro: Dann müssen Netzbetreiber lokale Wertschöpfung sichtbarer machen: Schulungen, Gewerbesteuer, unterirdische Abschnitte wo geologisch sinnvoll.
Hein: Und wenn der Zeitdruck der Energiewende kurze Fristen erzwingt?
Okoro: Tempo ohne Vertrauen erzeugt Blockaden. Parallelisierung von Planung und Dialog ist teurer am Anfang und billiger am Ende.
Moderator: Reichen Bürgerdialoge oder braucht es Vetorechte?
Okoro: Vetorechte einzelner können Gemeinwohl lähmen; verpflichtende Anhörungen mit dokumentierter Abwägung sind der mittlere Weg.
Hein: Wir brauchen außerdem ehrliche Karten zu Lärm und Landschaftsbild – nicht nur Werbebroschüren.
Okoro: Transparenz ist Infrastruktur. Wer sie spart, zahlt später mit Jahren Verzögerung.""",
        """主持人：Okoro 女士，為何線路常因抗議失敗？
Okoro：不是敗在氣候目標，而是程序太晚納入受影響者，且補償不確定。
市長 Hein：我們要再生能源，但不要沒有在地可見利益的長期工地。
Okoro：那電網業者必須讓在地價值更可見：培訓、營業稅、在地質可行處改地下段。
Hein：若能源轉型的時間壓力迫使縮短期限呢？
Okoro：沒有信任的速度會製造封鎖。規劃與對話平行，起初較貴、最後較便宜。
主持人：公民對話夠嗎，還是要否決權？
Okoro：個人否決可能癱瘓公益；具義務性、且可追溯權衡的聽證是中道。
Hein：還需要關於噪音與景觀的老實地圖——不要只有文宣。
Okoro：透明本身就是基礎設施。誰省它，後來用數年延誤償還。""",
        [n("Trassen", "線路廊道"), n("Entschädigung", "補償"), n("Wertschöpfung", "價值創造"), n("Parallelisierung", "平行化／同步推進"), n("Vetorechte", "否決權"), n("dokumentierter Abwägung", "可追溯的利益權衡"), n("Landschaftsbild", "地景樣貌")],
        [p("Nicht am A, sondern an B", "重新定位原因", "Nicht am Ziel, sondern am Verfahren"), p("Tempo ohne Vertrauen erzeugt …", "因果警句", "Sparen ohne Plan erzeugt Kosten"), p("A ist Infrastruktur", "重新定義", "Beratung ist Infrastruktur")],
        ["能源對話：接受度≠反綠→在地利益→程序中道。", "注意『透明是基礎設施』金句。", "Abwägung 是行政關鍵詞。"],
        ["能源", "民主", "城市", "對話"],
    ),
    item(
        "b2-82", "B2", "story", "移民勞動",
        "Anerkennung ausländischer Abschlüsse als Flaschenhals", "外國學歷認證作為瓶頸",
        """Fachkräftemangel und lange Anerkennungsverfahren stehen in einem widersprüchlichen Verhältnis. Während Betriebe Stellen nicht besetzen, warten qualifizierte Zugewanderte Monate auf Bescheide, Ausgleichsmaßnahmen oder Prüfungstermine. Die Wartezeit entwertet Humankapital: Sprachkurse enden, Praktika verfallen, Motivation erodiert.

Behörden argumentieren mit Qualitäts- und Patientenschutz – berechtigt in reglementierten Berufen. Dennoch lassen sich Doppelprüfungen reduzieren, wenn Curricula digital vergleichbar und Teilqualifikationen anrechenbar sind. Mentoring durch Berufskammern verkürzt Unsicherheit stärker als allgemeine Informationsportale allein.

Kritisch bleibt die Finanzierung von Anpassungsqualifizierungen. Wer parallel jobben muss, scheitert häufiger an Abendkursen. Stipendien und bezahlte Praxisphasen sind daher keine Wohltat, sondern Arbeitsmarktpolitik. Auch Arbeitgeberinnen können Praktika mit klarer Übernahmeperspektive anbieten, statt nur Engpässe zu beklagen.

Insofern ist Anerkennung Infrastruktur der Integration. Es bleibt abzuwarten, inwiefern bundeseinheitliche Fristen und digitale Aktenlaufwerke Wartezeiten messbar senken – oder ob Reformrhetorik die Flaschenhälse lediglich neu beschriftet.""",
        """缺工與冗長認證程序處於矛盾關係。企業找不到人時，合格移民卻為處分、補修或考試時段等待數月。等待折損人力資本：語言班結束、實習過期、動機流失。

機關以品質與病人安全辯護——在受管制職業有其正當性。但若課程可數位比對、部分資格可折抵，仍可減少重複考試。職業公會導師制比單靠一般資訊入口更能縮短不確定。

補修培訓的金流仍是關鍵。必須同時打工者更常在夜間課程失敗。獎學金與支薪實務階段因此不是慈善，而是勞動市場政策。雇主也可提供具明確留用前景的實習，而非只抱怨缺工。

因此認證是融合的基礎設施。聯邦統一期限與數位案卷能否顯著縮短等待——或改革修辭只是替瓶頸換標籤，仍有待觀察。""",
        [n("Anerkennungsverfahren", "認證程序"), n("Zugewanderte", "移入者"), n("entwertet Humankapital", "使人力資本貶值"), n("reglementierten Berufen", "受管制職業"), n("anrechenbar", "可折抵／可採計"), n("Anpassungsqualifizierungen", "銜接／補修培訓"), n("Reformrhetorik", "改革修辭")],
        [p("stehen in einem widersprüchlichen Verhältnis", "指出結構矛盾", "stehen in Spannung zueinander"), p("sind daher keine A, sondern B", "重新定性", "sind keine Wohltat, sondern Politik"), p("lediglich neu beschriftet", "批判空轉改革", "lediglich umbenannt")],
        ["移民／勞動：缺工矛盾→品質辯護→金流→基礎設施比喻。", "Flaschenhals＝瓶頸。", "注意複數被動與名詞化密集。"],
        ["移民", "勞動", "行政", "論述"],
    ),
    item(
        "b2-83", "B2", "notice", "學術行政",
        "Richtlinie zu KI-gestütztem Schreiben in Prüfungen", "考試中 AI 輔助寫作準則",
        """Prüfungsrichtlinie – Umgang mit generativer KI
Ab dem Wintersemester gilt: Der Einsatz generativer KI zur Texterstellung ist in benoteten Prüfungen nur zulässig, wenn die Aufgabenstellung dies ausdrücklich erlaubt und die verwendeten Systeme sowie Prompts in einem Anhang dokumentiert werden. Undeklarierte Übernahme gilt als Täuschungsversuch.

Erlaubt bleibt der Einsatz für Ideenfindung und Sprachkorrektur in Hausarbeiten, sofern die inhaltliche Argumentation eigenständig ist und Quellen kritisch geprüft wurden. Die Letztverantwortung für Richtigkeit und Urheberrecht liegt bei den Studierenden.

Lehrende sind gehalten, Aufgaben so zu gestalten, dass reine Generierung erkennbar unzureichend ist – etwa durch lokale Falldaten, mündliche Verteidigung oder Prozessdokumentation. Verdachtsfälle werden nach den bestehenden Ordnungen geprüft; technische Detektoren sind Hilfsmittel, nicht alleiniger Beweis.

Fragen zur Auslegung richtet die Fakultät an eine zentrale Kommission. Diese Richtlinie wird nach einem Jahr evaluiert. Sie tritt am 1. Oktober in Kraft und ersetzt den Übergangsvermerk vom April.""",
        """考試準則－生成式 AI 之使用
自冬季學期起：在計分考試中，僅當試題明確允許、並在附件記錄所用系統與提示詞時，才可用生成式 AI 產製文本。未申報之搬用視同作弊意圖。

報告中用於發想與語言潤飾仍可，前提是論證自主且來源經批判檢視。正確性與著作權之最終責任在學生。

教師應設計使「純生成」明顯不足的任務——例如在地個案、口頭答辯或過程文件。嫌疑依既有規章審查；偵測工具是輔助，非唯一證據。

解釋問題由學院提交中央委員會。本準則一年後評估。10 月 1 日生效，取代四月過渡說明。""",
        [n("generativer KI", "生成式 AI"), n("ausdrücklich erlaubt", "明確允許"), n("Undeklarierte Übernahme", "未申報之搬用"), n("Täuschungsversuch", "作弊意圖"), n("Letztverantwortung", "最終責任"), n("mündliche Verteidigung", "口頭答辯"), n("Detektoren", "偵測工具")],
        [p("ist nur zulässig, wenn …", "許可條件", "ist nur zulässig, wenn dokumentiert"), p("gelten als …", "定性違規", "gilt als Täuschung"), p("sind gehalten, …", "對教師之義務語氣", "sind gehalten, Kriterien offenzulegen")],
        ["學術準則：允許範圍→責任→教學設計→證據門檻→生效。", "undeclared vs erlaubt 對照清楚。", "Detektor≠唯一證據。"],
        ["學術", "科技", "考試", "公告"],
    ),
    item(
        "b2-84", "B2", "story", "文化機構",
        "Museumsschließungen und die Ökonomie der Aufmerksamkeit", "博物館關閉與注意力經濟",
        """Wenn Kommunen Museen verkürzen oder schließen, wird sparsamkeitspolitisch argumentiert. Unterbelichtet bleibt, dass kulturelle Infrastruktur Aufmerksamkeit, Tourismus und informelles Lernen bindet, deren Nutzen sich erst über Jahre in Bildungs- und Standortstatistiken zeigt. Kurzfristige Haushaltsschnitte erzeugen langfristige Leerstellen im kollektiven Gedächtnis.

Gegner großzügiger Kulturförderung verlangen messbare Besucherzahlen. Zahlen sind notwendig, aber unvollständig: Wer misst die Qualität von Schulprogrammen oder die Wirkung auf Sprachförderung Geflüchteter? Eine nur an Tickets orientierte Logik begünstigt Blockbuster und vernachlässigt Archive, die weniger spektakulär, jedoch grundlegend sind.

Digitale Zugänge können Reichweite erhöhen, ersetzen jedoch keine physischen Begegnungsräume. Hybride Modelle brauchen Personal für Kuratierung und Vermittlung – Technologie ohne Fachkräfte ist eine leere Plattform. Sponsoring kann Lücken füllen, darf öffentliche Verantwortung nicht privat diluieren.

Insofern ist die Debatte eine über Zeitlichkeit von Politik: Legislaturperioden denken in Jahren, Bildungswirkungen in Jahrzehnten. Wer Museen nur als Kostenstelle führt, führt Buch über das Falsche.""",
        """當城市縮短開放或關閉博物館，論述常訴諸節約。被低估的是：文化基礎設施能黏住注意力、觀光與非正式學習，其效益往往數年後才出現在教育與地方統計。短期預算刪減會在集體記憶留下長期空缺。

反對慷慨文化補助者要求可測量訪客數。數字必要但不完整：誰衡量學校方案品質或對難民語言支持的影響？只看票券的邏輯偏愛大展，忽略較不炫目但基礎的典藏。

數位入口可擴大觸及，卻取代不了實體相遇空間。混合模式需要策展與教育人員——沒有專業人力的科技是空平台。贊助可補缺口，不該把公共責任稀釋成私領域。

因此這是關於政治時間性的辯論：任期以年計，教育效應以十年計。若只把博物館當成本中心，就是記錯帳。""",
        [n("sparsamkeitspolitisch", "以節約政策為由地"), n("Unterbelichtet bleibt", "仍被低估／光照不足"), n("kollektiven Gedächtnis", "集體記憶"), n("begünstigt Blockbuster", "偏愛大牌／爆款展覽"), n("Kuratierung", "策展"), n("diluieren", "稀釋"), n("Kostenstelle", "成本中心")],
        [p("wird A argumentiert. Unterbelichtet bleibt B", "主流論述＋盲點", "wird mit Kosten argumentiert. Unterbelichtet bleibt Nutzen."), p("Zahlen sind notwendig, aber unvollständig", "承認指標限度", "Daten sind nötig, aber nicht hinreichend."), p("führt Buch über das Falsche", "隱喻收尾", "misst das Falsche")],
        ["文化政策：節約論→指標不全→數位≠空間→政治時間性。", "注意『記錯帳』隱喻。", "ハイブリッド／hybrid 模式的條件。"],
        ["文化", "公共財政", "教育", "論述"],
    ),
    item(
        "b2-85", "B2", "email", "公共參與",
        "Stellungnahme zum Bebauungsplanentwurf", "對都市計畫草案之意見書",
        """Betreff: Stellungnahme Bebauungsplan 14/Nord – Beteiligung der Öffentlichkeit

Sehr geehrte Damen und Herren,

als Anwohnerin der Nordstraße nehme ich zum Entwurf des Bebauungsplans 14/Nord Stellung. Die geplante Nachverdichtung ist grundsätzlich nachvollziehbar; kritisch sehe ich jedoch die unzureichende Ausweisung von Spiel- und Grünflächen sowie die Unterschätzung des Verkehrsaufkommens in der engen Zufahrt.

Ich beantrage eine Überarbeitung mit folgenden Punkten: verbindlicher Erhalt der Baumreihe, eine zusätzliche Fuß- und Radquerung an der Schule sowie ein schalltechnisches Gutachten für die östliche Blockkante. Ohne diese Maßnahmen drohen Nutzungskonflikte zwischen Wohnen, Lieferverkehr und Schulwegsicherheit.

Die bisherige Bürgerwerkstatt war konstruktiv, blieb jedoch ohne dokumentierte Abwägung einzelner Einwände. Ich bitte um Veröffentlichung der Abwägungstabelle vor dem Satzungsbeschluss und um eine Ortstermin-Einladung für die betroffenen Haushalte.

Mit freundlichen Grüßen
Mireille Fontaine
Nordstraße 18""",
        """主旨：對 14/Nord 都市計畫草案之意見－公眾參與

諸位鈞鑒，

作為北街居民，謹對 14/Nord 草案提出意見。計畫中的加密開發原則上可理解；但我認為遊戲與綠地標示不足，且對狹窄進出口之交通量估計偏低。

我請求依下列重點修訂：具拘束力地保留行道樹列、學校旁增設行人與自行車穿越，以及東側街區之噪音技術鑑定。若無這些措施，居住、送貨與通學安全恐生衝突。

既有公民工作坊具建設性，但個別異議未見可追溯權衡。請於議會通過前公布權衡表，並邀請受影響住戶會勘。

此致問候
Mireille Fontaine
北街 18 號""",
        [n("Nachverdichtung", "都市加密／增建"), n("Ausweisung", "劃設／標示"), n("Unterschätzung", "低估"), n("schalltechnisches Gutachten", "噪音技術鑑定"), n("Nutzungskonflikte", "使用衝突"), n("Abwägungstabelle", "權衡對照表"), n("Satzungsbeschluss", "自治條例／計畫通過決議")],
        [p("nehme ich zum Entwurf … Stellung", "公眾參與開場", "nehme ich zur Planung Stellung"), p("ist grundsätzlich nachvollziehbar; kritisch sehe ich jedoch …", "先承認後批評", "ist sinnvoll; kritisch sehe ich die Kosten"), p("Ohne diese Maßnahmen drohen …", "後果預告", "Ohne Nachbesserung drohen Verzögerungen")],
        ["都市參與信：原則同意→具體缺口→條列請求→程序透明。", "Abwägung 是德文規劃法核心。", "語氣公民但不情緒化。"],
        ["城市", "參與", "環境", "正式郵件"],
    ),
]


# Length-band patches (exam-aligned remaps); applied before asserts.
ENRICH = {
    "uebung-73": {
        "text": "Parken nur mit Ticket\nMo–Sa 8–20 Uhr\nOhne Ticket: 40 Euro\nTicket am Automaten.",
        "textZh": "停車需購票\n週一至六 8–20 點\n無票：40 歐元\n請至自動販賣機購票。",
    },
    "uebung-74": {
        "text": "Hi Lea,\nHast du Zeit um 16 Uhr?\nKaffee im Café Sonne?\nSchreib kurz zurück!\nLG Tim",
        "textZh": "嗨 Lea，\n你下午四點有空嗎？\n在 Sonne 咖啡館喝咖啡？\n回我一下！\n問候 Tim",
    },
    "uebung-81": {
        "text": "Bitte Ruhe!\nPrüfung von 9–12 Uhr\nHandy bitte lautlos.\nDanke fürs Mitmachen.",
        "textZh": "請保持安靜！\n考試 9–12 點\n手機請靜音。\n感謝配合。",
    },
    "uebung-85": {
        "text": "Hi Nora,\nbis am Wochenende!\nSchreib mir den Treffpunkt.\nIch freue mich.\nCiao\nSam",
        "textZh": "嗨 Nora，\n週末見！\n跟我說碰面地點。\n我很期待。\n掰\nSam",
    },
    "a2-73": {
        "textZh": "上週六我們社區辦春季清掃。\n鄰居們在邊坡撿垃圾、重種花圃。\n市府提供手套、袋子和熱茶。\n我主要撿到塑膠和菸蒂。\n最後在社區中心有蛋糕。\n很累，但河岸看起來好多了。\n明年我還會參加。",
    },
    "a2-74": {
        "text": """Wichtige Information an alle Bewohnerinnen und Bewohner
Der Aufzug ist von Montag 7 Uhr bis voraussichtlich Mittwoch 18 Uhr wegen Wartung außer Betrieb.
Bitte nutzen Sie das Treppenhaus und planen Sie mehr Zeit ein.
Für Personen mit eingeschränkter Mobilität: Begleitservice unter 030 111 222, Anmeldung bis Sonntag 12 Uhr.
Lieferungen bitte im Hof abstellen und uns informieren.
Vielen Dank.
Hausverwaltung Nord""",
        "textZh": """給全體住戶的重要通知
電梯因維護，自週一 7 點起至預計週三 18 點停用。
請走樓梯並預留更多時間。
行動不便者：陪同服務電話 030 111 222，週日 12 點前登記。
送貨請放中庭並通知我們。
謝謝。
北區物業""",
    },
    "a2-76": {
        "text": """Assistentin: Zahnarztpraxis Berger, guten Tag.
Patient: Hallo, ich brauche einen Termin wegen Zahnschmerzen.
Assistentin: Akut? Dann hätten wir heute 17:40.
Patient: Ja, bitte. Muss ich etwas mitbringen?
Assistentin: Versichertenkarte und Medikamentenliste, falls nötig.
Patient: Bin ich als Notfall eingetragen?
Assistentin: Als dringender Termin. Bitte 10 Minuten früher kommen.""",
        "textZh": """助理：Berger 牙科診所，您好。
病人：您好，我牙痛想預約。
助理：急性嗎？那今天 17:40 有位。
病人：好，麻煩。需要帶什麼？
助理：健保卡，必要時帶藥單。
病人：我是掛急診嗎？
助理：緊急時段。請早 10 分鐘到。""",
    },
    "a2-78": {
        "text": """Fotoclub Campus sucht neue Mitglieder!
Wir treffen uns jeden zweiten Donnerstag um 18:30 im Medienraum B2.
Themen: Porträt, Streetfotografie und Bildbearbeitung.
Kameras ausleihen ist für Mitglieder nach kurzer Einführung kostenlos.
Anmeldung an foto@campus.example bis 30. September; schreibt kurz euer Equipment.
Anfängerinnen und Anfänger sind willkommen. Der erste Abend ist unverbindlich.""",
        "textZh": """校園攝影社徵求新社員！
每兩週週四 18:30 在媒體教室 B2 聚會。
主題：人像、街拍與後製。
社員短訓後可免費借相機。
9 月 30 日前報名 foto@campus.example；請簡述器材。
歡迎初學者。第一次聚會不強制。""",
    },
    "a2-80": {
        "text": """Mechaniker: Was kann ich für Sie tun?
Kundin: Die Bremsen quietschen und greifen schlecht.
Mechaniker: Ich prüfe Beläge und Kabel – etwa 30 Minuten.
Kundin: Können Sie gleich die Beleuchtung prüfen? Das Rücklicht war schwach.
Mechaniker: Mache ich. Soll ich vor dem Wechseln einen Kostenvoranschlag machen?
Kundin: Ja. Über 60 Euro bitte erst anrufen.
Mechaniker: Notiert.""",
        "textZh": """技師：有什麼能幫您？
顧客：煞車有尖叫聲，而且不太靈。
技師：我看來令片和鋼索——約 30 分鐘。
顧客：能順便檢查燈光嗎？尾燈偏弱。
技師：好。更換前要估價嗎？
顧客：要。超過 60 歐元請先來電。
技師：記下了。""",
    },
    "a2-81": {
        "text": """Am Sonntag habe ich zum ersten Mal eine Kurzführung im Stadtmuseum gemacht.
Vorher habe ich den Text wiederholt und Datenkarten gelernt.
Die Gruppe war klein: sechs Erwachsene und zwei Kinder.
Am Anfang sprach ich zu schnell; eine Besucherin bat freundlich um langsameres Tempo.
Danach wurde es besser, und am Ende gab es Applaus.
Die Leitung bot mir ein Feedback-Gespräch für nächste Woche an.""",
        "textZh": """星期天我第一次在市立博物館做短導覽。
事前我複習文本並背資料卡。
團體不大：六位成人與兩個孩子。
一開始講太快；一位訪客客氣請我慢一點。
之後好多了，最後有掌聲。
主管下週要约我做回饋面談。""",
    },
    "a2-82": {
        "text": """Hinweis der Abfallwirtschaft
Mehrere gelbe Tonnen wurden nicht geleert, weil Restmüll oder Glas darin lag.
Verpackungen gehören in die gelbe Tonne, Glas zum Container, Biomüll in die braune Tonne.
Falsch befüllte Tonnen bleiben stehen; eine Nachleerung kostet extra.
Leitfaden im Hausflur und unter abfall.example/stadt.
Fragen: Mo–Fr 9–15 Uhr, 0800 987 654. Danke für Ihre Mithilfe.""",
        "textZh": """廢棄物處理單位提醒
多個黃色資源桶因混入一般垃圾或玻璃而未清運。
包裝進黃桶，玻璃進回收桶，廚餘進棕桶。
錯誤投放的桶會留置；加清需額外付費。
指南在門廳及 abfall.example/stadt。
詢問：週一至五 9–15 點，0800 987 654。感謝配合。""",
    },
    "a2-84": {
        "text": """Maklerin: Die Wohnung hat 48 Quadratmeter, Baujahr 1998, renoviert 2022.
Interessent: Sind die Nebenkosten in den 780 Euro enthalten?
Maklerin: Nein, plus etwa 180 Euro. Kaution: drei Kaltmieten.
Interessent: Darf man die Wände streichen?
Maklerin: Helle Farben ja, nach Absprache. Haustiere nur mit Zustimmung.
Interessent: Frühester Einzug?
Maklerin: Zum 1. November, wenn die Unterlagen passen.""",
        "textZh": """仲介：房子 48 平方公尺，1998 年建、2022 整修。
看房者：780 歐元含不含水電雜費？
仲介：不含，大約再加 180。押金三個月淨租金。
看房者：可以粉刷牆壁嗎？
仲介：淺色可以，需商量。寵物須同意。
看房者：最早入住？
仲介：文件齊備則 11 月 1 日。""",
    },
    "a2-85": {
        "text": """Ich brauchte einen Termin beim Bürgeramt und habe ihn online gebucht.
Zuerst musste ich ein Konto anlegen und einen SMS-Code bestätigen.
Freie Termine gab es erst in drei Wochen, außer für Notfälle.
Ich setzte eine Kalendererinnerung und sortierte die Dokumente vorher.
Am Tag war die Schlange lang, aber digital Angemeldete wurden getrennt aufgerufen.
Ohne Online-Buchung hätte ich noch länger gewartet.""",
        "textZh": """我需要市民局時段，於是線上預約。
先要開帳號並用簡訊碼確認。
除非急件，否則要等三週才有空缺。
我設日曆提醒，並事先整理文件。
當天隊伍仍長，但線上掛號者分開叫號。
若沒線上預約，大概要等更久。""",
    },
    "b1-71": {
        "text": """Betreff: Antrag auf Gleitzeit ab September

Sehr geehrte Frau Hartmann,

hiermit beantrage ich Gleitzeit von 7:30–16:00 Uhr (Kernzeit 9–15) ab dem 1. September.
Grund ist die Betreuung meiner Tochter nach dem Kita-Wechsel; die neue Einrichtung schließt früher.

Meine Aufgaben im Projekt „Atlas“ erfülle ich weiterhin vollständig.
Absprachen mit dem Team sind vorbesprochen; Vertretungen in der Kernzeit sichere ich zu.

Über eine schriftliche Zustimmung bis 20. August würde ich mich freuen.

Mit freundlichen Grüßen
Jonas Weber""",
        "textZh": """主旨：申請自九月起彈性工時

Hartmann 女士您好，

謹此申請自 9 月 1 日起彈性工時 7:30–16:00（核心工時 9–15）。
原因是女兒托育機構轉換後接送；新機構較早關門。

「Atlas」專案任務我仍完整完成。
已與團隊預先溝通；核心時段代理我保證到位。

若能於 8 月 20 日前書面同意，感激不盡。

此致問候
Jonas Weber""",
    },
    "b1-72": {
        "text": """Mitteilung der IT-Wohnheimverwaltung
Am Samstag, 14. Oktober, 6–10 Uhr, wird das WLAN auf neuen Standard umgestellt.
In diesem Zeitraum ist mit Unterbrechungen und fehlendem Internetzugang zu rechnen.
Bitte speichern Sie Arbeiten lokal und beenden Sie große Uploads rechtzeitig.
VPN bleibt bestehen; ggf. einmal neu verbinden.
Probleme nach 10 Uhr: Ticketportal /it-heim mit Raumnummer.
Notdienst nur bei totalem Ausfall: 0170 444 889.
Vielen Dank für Ihre Geduld.""",
        "textZh": """宿舍 IT 管理通知
10 月 14 日週六 6–10 點，無線網升級至新標準。
此時段可能中斷且暫時無法上網。
請將工作存到本機，並及早結束大型上傳。
VPN 仍可用；必要時重新連線一次。
10 點後問題：/it-heim 開票並註明房號。
僅全面斷網時打 0170 444 889。
感謝耐心。""",
    },
    "b1-73": {
        "text": """In unserer WG eskalierte der Küchenstreit, nachdem zweimal Geschirr über Nacht stehen blieb.
Statt Vorwürfe per Chat zu schicken, haben wir kurz gesprochen.
Jeder nannte ein Ärgernis und einen Vorschlag: Spüldienstplan, 20-Minuten-Regel, gemeinsamer Vorrat.
Niemand unterstellte Absicht – eher Überarbeitung und unterschiedliche Standards.
Wir schrieben die Regeln auf und hängten sie an die Schranktür.
Nach zwei Wochen stockte der Plan einmal, doch eine Erinnerung reichte.
Die Atmosphäre ist nicht perfekt, aber spürbar entspannter.""",
        "textZh": """我們宿舍在碗盤兩次過夜沒洗後，廚房爭執升高。
我們沒在聊天軟體互責，而是談了半小時。
每人說一個困擾與建議：洗碗輪值、20 分鐘規則、共用儲物。
沒人指控故意——比較像過勞與標準不同。
我們把規則寫下貼在櫃門。
兩週後計畫中斷一次，但提醒就夠。
氣氛不算完美，但明顯輕鬆多了。""",
    },
    "b1-74": {
        "text": """Beraterin: Sie schwanken zwischen Master und direktem Berufseinstieg?
Student: Ja. Arbeit wäre finanziell attraktiver, aber ich fürchte Wissenslücken.
Beraterin: Methodisch oder fachlich?
Student: Vor allem Statistik und Projektmanagement.
Beraterin: Zertifikatskurse plus Werkstudentenstelle wären eine Option ohne zwei Jahre Master.
Student: Und wenn ich den Master später nachhole?
Beraterin: Viele Programme akzeptieren Berufserfahrung. Sortieren Sie Motive schriftlich.
Student: Ich mache eine Vor-/Nachteilliste und komme in zwei Wochen wieder.""",
        "textZh": """諮詢師：您在碩士與直接就業之間猶豫？
學生：對。工作經濟上較吸引，但我怕知識缺口。
諮詢師：方法還是專業內容？
學生：主要是統計與專案管理。
諮詢師：證照課加工讀可不立刻讀兩年碩士。
學生：若之後再補碩士呢？
諮詢師：許多學程認可工作經驗。請把動機寫清楚。
學生：我做優缺列表，兩週後再來。""",
    },
    "b1-75": {
        "text": """Betreff: Zweite Erinnerung – Schimmel im Bad

Sehr geehrter Herr Lange,

am 2. März habe ich Schimmel im Bad gemeldet; der Termin am 10. März fiel aus.
Bisher fand keine fachgerechte Sanierung statt. Die Stelle wird größer und verursacht Hustenreiz.

Ich bitte Sie, bis 5. April ein Fachunternehmen zu beauftragen und mir den Termin schriftlich zu nennen.
Andernfalls behalte ich mir vor, Mietminderung zu prüfen und die Behörde zu informieren.

Für eine konstruktive Lösung bleibe ich ansprechbar.

Mit freundlichen Grüßen
Amira Haddad""",
        "textZh": """主旨：第二次提醒－浴室黴菌

Lange 先生您好，

我於 3 月 2 日通報浴室發霉；3 月 10 日時段取消。
至今未專業修繕。範圍擴大並引起咳嗽刺激。

請於 4 月 5 日前委託專業公司，並書面告知時程。
否則我保留檢討減租並通知機關的權利。

我仍願建設性解決。

此致問候
Amira Haddad""",
    },
    "b1-76": {
        "text": """Interne Mitteilung – Hitzeschutz
Bei Außentemperaturen über 30 °C gelten folgende Regelungen:
1) Homeoffice nach Absprache möglich, sofern die Tätigkeit es erlaubt.
2) Zwischen 12 und 15 Uhr werden Präsenzmeetings auf 30 Minuten begrenzt.
3) Ventilatoren und Wasser stehen in der Teeküche bereit; Fenster nur morgens öffnen.
Bei Beschwerden frühzeitig den Betriebsarzt melden.
Die Regelung gilt bis einschließlich 31. August und kann verlängert werden.
Fragen: personal@firma.example.""",
        "textZh": """內部通知－防暑
室外超過 30°C 時適用：
1) 經商量可居家辦公，前提工作允許。
2) 12–15 點現場會議以 30 分鐘為限。
3) 茶水間有風扇與水；窗戶僅早晨開。
不適請及早向廠醫回報。
規定至 8 月 31 日（含），可延長。
問題：personal@firma.example。""",
    },
    "b1-77": {
        "text": """Als mein Toaster den Geist aufgab, wollte ich zuerst ein Neugerät bestellen.
Stattdessen brachte ich ihn ins Repair-Café. Eine Freiwillige öffnete das Gehäuse, reinigte Kontakte und erklärte den Fehler.
Das Gerät läuft wieder; ich spendete fünf Euro und investierte Wartezeit.
Mir wurde klar, wie stark Wegwerfgewohnheiten mit fehlendem Wissen zusammenhängen.
Nicht jede Reparatur lohnt sich – bei billiger Elektronik oft nicht.
Bei robusten Geräten spart man Ressourcen und lernt Souveränität.
Inzwischen habe ich ein kleines Werkzeugset zugelegt.""",
        "textZh": """烤麵包機壞掉時，我原本想直接訂新的。
後來拿到 Repair-Café。志工打開機殼、清理接點並說明故障。
機器又能用；我捐五歐元並投入等候時間。
我明白丟棄習慣與缺乏知識關係很大。
不是每種維修都划算——廉價電子產品常常不划算。
耐用設備可省資源並學到自主。
我後來買了一套小工具。""",
    },
    "b1-78": {
        "text": """Agentin: Kundenservice ElektroPlus, Sara. Wie kann ich helfen?
Kunde: Mein Kühlschrank ist nach der Reparatur erneut ausgefallen. Ich möchte eine Eskalation.
Agentin: Haben Sie die Auftragsnummer?
Kunde: Ja, A-44921. Außerdem Fotos vom Fehlercode.
Agentin: Ich leite den Fall an die Technikleitung weiter. Rückruf innerhalb von 48 Stunden.
Kunde: Und falls niemand anruft?
Agentin: Dann mailen Sie an eskalation@elektroplus.example mit Ticket-ID T-88314.
Kunde: Gut. Bitte notieren Sie auch verdorbene Lebensmittel.""",
        "textZh": """客服：ElektroPlus，Sara。有何可幫忙？
顧客：冰箱維修後又故障。我要升級處理。
客服：有工單號碼嗎？
顧客：有，A-44921。也有錯誤碼照片。
客服：我轉給技術主管。48 小時內回电。
顧客：若沒人打呢？
客服：請寫信 eskalation@elektroplus.example，工單 T-88314。
顧客：好。也請註記食品損壞。""",
    },
    "b1-80": {
        "text": """An alle Mieterinnen und Mieter
Ab 5. Mai wird die Fahrradgarage umgebaut. Bis 20. Mai stehen 20 Ersatzbügel im Innenhof zur Verfügung.
Bitte kennzeichnen Sie Ihr Rad mit Name und Wohnung; tagsüber nicht dauerhaft an Treppengeländer schließen.
Lastenräder und Anhänger bis 2. Mai an hof@haus.example melden, damit wir Sonderflächen zuweisen.
In der Bauphase kann es 8–17 Uhr zu Lärm kommen.
Nach Abschluss erhalten alle eine neue Stellplatznummer.
Rückfragen an die Hausverwaltung. Danke für Kooperation.""",
        "textZh": """給全體房客
自 5 月 5 日起改建腳踏車棚。至 5 月 20 日中庭有 20 個臨時車架。
請標示姓名與房號；白天勿長鎖樓梯扶手。
載貨車與拖車請於 5 月 2 日前寄 hof@haus.example。
施工期間 8–17 點可能有噪音。
完工後發給新車位編號。
問題洽物業。感謝配合。""",
    },
    "b1-81": {
        "text": """Mein erstes Online-Vorstellungsgespräch fühlte sich an wie Prüfung plus Techniktest.
Ich prüfte Kamera, Licht und Headset und legte Notizen außerhalb des Bildes bereit.
Trotzdem hakte der Ton; ich sagte Bescheid und wechselte aufs Handy-Hotspot.
Die Kommission stellte Fragen zu Teamkonflikten.
Ich antwortete mit Situation–Handlung–Ergebnis und fragte nach Einarbeitung.
Später merkte ich: Blick in die Linse zählt mehr als auf die eigenen Kacheln.
Ob ich die Stelle bekomme, weiß ich nicht – die Vorbereitung war trotzdem wertvoll.""",
        "textZh": """我的第一次線上面試像考試加技術測試。
我事先檢查鏡頭、光線與耳機，筆記放在畫面外。
音訊仍卡住；我說明並改用手機熱點。
委員會問團隊衝突。
我用情境–行動–結果回答，並詢問到職輔導。
後來發現看鏡頭比盯自己小窗更重要。
是否錄取尚不知——但準備仍有價值。""",
    },
    "b1-82": {
        "text": """Betreff: Anfrage Gemeinschaftsraum 19. November

Sehr geehrte Damen und Herren,

der Literaturkreis „Seitenwind“ möchte am 19. November, 19–21:30 Uhr, den Gemeinschaftsraum für eine Lesung nutzen.
Erwartet werden etwa 40 Gäste; wir bringen Technik mit und verpflichten uns zur Reinigung.

Benötigt: Stuhlreihen, zwei Mikrofone und Küchenzugang für Wasser.
Eintritt frei; Spenden kommen einem Alphabetisierungsprojekt zugute.

Bitte teilen Sie Verfügbarkeit, Gebühr und Schlüsselübergabe mit.
Rückfragen: 0151 222 778.

Freundliche Grüße
Paula Kranz""",
        "textZh": """主旨：11 月 19 日交誼廳詢問

諸位鈞鑒，

文學圈「Seitenwind」希望 11 月 19 日 19–21:30 借用交誼廳朗讀。
預計約 40 位來賓；自備器材並承諾清理。

需要椅列、兩支麥克風及廚房用水。
免費入場；捐款捐給識字計畫。

請告知空檔、費用與鑰匙交接。
電話 0151 222 778。

問候
Paula Kranz""",
    },
    "b1-83": {
        "text": """Hinweis Datenschutz / Personal
Unaufgefordert eingesandte Bewerbungen werden maximal sechs Monate gespeichert, sofern kein Verfahren eröffnet wird.
Danach werden Dateien gelöscht und Papier datenschutzgerecht vernichtet.
Frühere Löschung: datenschutz@org.example.
Im laufenden Verfahren gelten längere Fristen gemäß berechtigtem Interesse und Nachweispflichten.
Bitte keine sensiblen Gesundheitsdaten senden, sofern nicht ausdrücklich gefordert.
Diese Information ersetzt die Fassung vom März.""",
        "textZh": """資料保護／人事提醒
未經請求寄來的履歷最多保存六個月，除非已開啟程序。
期滿後檔案刪除，紙本依個資規範銷毀。
提早刪除：datenschutz@org.example。
程序進行中依正當利益與舉證義務適用較長保存期。
除非明確要求，請勿寄送敏感健康資料。
本資訊取代三月版本。""",
    },
    "b1-84": {
        "text": """Ärztin: Sie können morgen entlassen werden, wenn die Blutwerte stabil bleiben.
Patient: Darf ich wieder Sport machen?
Ärztin: Spaziergänge ja; Training erst nach der Kontrolle in zehn Tagen.
Patient: Welche Medikamente sind neu?
Ärztin: Morgens ein Blutverdünner; Schmerzmittel nicht mit Alkohol.
Patient: Falls die Schwellung zurückkommt?
Ärztin: Sofort in die Notaufnahme und Arztbrief mitbringen.
Patient: Bekomme ich eine AU für die Arbeit?
Ärztin: Ja, sieben Tage; Verlängerung über die Hausärztin.""",
        "textZh": """醫師：若血值穩定，明天可出院。
病人：可以恢復運動嗎？
醫師：散步可以；訓練等十天後回診。
病人：哪些藥是新的？
醫師：早上一種抗凝血藥；止痛藥不可與酒同用。
病人：若腫脹復發？
醫師：立刻去急診並帶醫師摘要。
病人：能開工作病假單嗎？
醫師：可以，七天；延期找家庭醫師。""",
    },
    "b1-85": {
        "text": """Als ich mich für den Gemeinschaftsgarten anmeldete, landete ich auf Platz 47.
Statt zu warten, half ich bei Arbeitseinsätzen: Beete, Kompost, Schuppen streichen.
Dadurch lernte ich Regeln, Werkzeuge und Leute kennen.
Nach einem Jahr rückte ich auf; eine Parzelle wurde frei.
Heute ziehe ich Tomaten und Kräuter und gebe Überschüsse an die Nachbarschaftstafel.
Die Wartezeit fühlte sich nicht mehr sinnlos an, weil ich schon Teil der Praxis war.
Manchmal ist der Umweg die eigentliche Mitgliedschaft.""",
        "textZh": """我報名社區農園時，候補排到第 47。
我沒乾等，而是參加勞動：整畦、堆肥、油漆小棚。
因此學會規則、工具與人際。
一年後往前排；有人空出一小區。
如今我種番茄與香草，多餘放到鄰里食物架。
等待不再無意義，因為我已參與實作。
有時繞路才是真正的入會。""",
    },
    "b2-71": {
        "text": """Belegungsbindungen gelten als Instrument, um in angespannten Wohnungsmärkten Einkommensschwächere zu schützen. Gleichzeitig wird kontrovers diskutiert, ob feste Quoten soziale Mischung erzeugen oder vielmehr Stigmatisierung einzelner Adressen verstärken. Empirisch zeigt sich: Bindungen wirken nur, wenn Neubau und Bestandsmodernisierung parallel laufen und Kontrollen nicht rein symbolisch bleiben.

Kritikerinnen monieren Bürokratiekosten und Ausweichreaktionen von Eigentümern, die Wohnungen dem Markt entziehen oder befristete Verträge bevorzugen. Befürworter entgegnen, ohne bindende Regeln verschiebe sich die Last vollständig auf Transferleistungen und lange Pendelwege. Eine differenzierte Steuerung verknüpft daher Bindungsdauer mit Förderhöhe und prüft regelmäßig, ob Zielgruppen erreicht werden.

Hinzu kommt die Nachbarschaftsqualität: Soziale Mischung entsteht nicht allein durch Belegungsschlüssel, sondern durch Schulen, ÖPNV und Treffpunkte. Wer nur Kontingente festschreibt, ohne Infrastruktur mitzudenken, riskiert parallele Lebenswelten hinter derselben Hausnummer. Insofern ist Wohnungspolitik Stadtpolitik.

Ob digitale Wartelisten Transparenz erhöhen oder neue Hürden schaffen, hängt von Beratung und Sprachmittlung ab. Es bleibt abzuwarten, inwiefern Kommunen Evaluationen öffentlich machen und Fehlsteuerungen korrigieren, bevor Bindungen rein administrativ weiterlaufen.""",
        "textZh": """配住義務被視為在緊繃房市中保護收入較弱者的工具。同時也有爭議：固定配額究竟促成社會混合，還是強化特定地址的污名。經驗顯示：唯有新建與存量更新並行、且監管不只是象徵，義務才真正有效。

批評者指摘行政成本與房東規避——把房子撤出市場或偏好定期契約。支持者反駁：沒有拘束規則，負擔會完全轉到津貼與長距離通勤。細緻治理因此把義務年限與補助金額連結，並定期檢查是否觸及目標族群。

還有鄰里品質：社會混合不只靠配住公式，也靠學校、大眾運輸與聚會點。只寫名額、不思基礎設施，可能讓同一門牌後出現平行生活世界。因此住房政策即城市政策。

數位候補名單是提高透明還是製造新門檻，取決於諮詢與語言中介。各市是否公開評估並在義務空轉前修正偏差，仍有待觀察。""",
    },
    "b2-75": {
        "text": """Tarifverträge stabilisieren Löhne und Planbarkeit, verlieren jedoch an Reichweite, wenn immer mehr Betriebe außerhalb der Bindung agieren. In Branchen mit hoher Fluktuation und Werkverträgen entsteht ein Unterbietungswettbewerb, der tarifgebundene Unternehmen strukturell benachteiligt. Beschäftigte spüren das als stagnierende Reallöhne trotz formaler Mindeststandards.

Gegner verpflichtender Tarifbindung warnen vor Flexibilitätsverlust und Standortflucht. Das Argument verdient Ernsthaftigkeit: starre Regelungen ohne Öffnungsklauseln können Anpassungen in Krisen erschweren. Dennoch ersetzt Freiwilligkeit allein selten kollektive Verhandlungsmacht, besonders wo Personalvertretungen schwach sind. Eine kluge Ordnungspolitik kombiniert Anreize zur Mitgliedschaft mit Transparenzpflichten bei öffentlicher Auftragsvergabe.

Auch Qualifizierung gehört in dieses Bild. Wo Tarife nur Preise setzen, aber Weiterbildung fehlt, wandert Wertschöpfung ab. Betriebsräte und Kammern können Lernzeitkonten und branchenweite Umschulungen verankern. Internationaler Preisdruck verschwindet dadurch nicht, wird aber gestaltbarer.

Insofern ist die Debatte weniger „Markt gegen Staat“ als Frage institutioneller Lernfähigkeit. Ob Gesetzgeber Mindestabdeckungsquoten einführen oder vergaberechtliche Hebel nutzen, verschiebt Risiken zwischen Stammbelegschaften und Randbeschäftigten spürbar.""",
        "textZh": """團體協約能穩定薪資與可預期性，但若愈來愈多企業游離於拘束之外，其覆蓋就萎縮。在高流動與承攬契約盛行的產業，會出現削價競爭，使受協約拘束的企業結構性吃虧。勞工感受到的是：即使有形式最低標準，實質薪資仍停滯。

反對強制性協約拘束者警告失去彈性與產業外移。這論點值得認真：沒有開放條款的僵硬規定，會讓危機調適變難。但僅靠自願很少能取代集體談判力，尤其在員工代表薄弱之處。精明的秩序政策會把入會誘因與政府採購透明度義務結合。

培訓也屬同一圖像。若協約只訂價格、沒有進修，價值創造會流失。企業委員會與公會可把學習時數帳戶與全產業轉業訓練寫進制度。國際價格壓力不會消失，但變得較可塑造。

因此辯論比較不像「市場對國家」，而是制度學習能力問題。立法者要採最低覆蓋率還是採購法槓桿，將明顯改寫核心員工與邊緣就業之間的風險分配。""",
    },
    "b2-76": {
        "text": """Betreff: Letzte Frist zur Nachbesserung – Vorgang K-77201

Sehr geehrte Damen und Herren,

trotz zweier Reparaturversuche vom 3. und 21. Februar weist das gelieferte E-Bike weiterhin den beschriebenen Bremsdefekt auf. Eine weitere Nutzung ist aus Sicherheitsgründen nicht zumutbar. Bereits am 28. Februar habe ich den Mangel schriftlich gerügt und um unverzügliche Abhilfe gebeten.

Ich setze Ihnen hiermit eine letzte Frist bis 18. April, den Mangel fachgerecht zu beheben oder gleichwertigen Ersatz zu liefern. Sollte bis dahin keine nachweisbare Abhilfe erfolgen, werde ich vom Kaufvertrag zurücktreten und die Rückabwicklung sowie Ersatz etwaiger Gutachterkosten verlangen. Eine weitere Teilreparatur ohne Funktionsnachweis lehne ich ab.

Bitte bestätigen Sie den Eingang dieses Schreibens und nennen Sie mir eine Ansprechperson mit Durchwahl. Korrespondenz bevorzugt schriftlich an die unten genannte Adresse; telefonische Zusagen ohne Aktenzeichen erkenne ich nicht als verbindlich an. Für eine zeitnahe, dokumentierte Lösung bleibe ich erreichbar.

Mit freundlichen Grüßen
Lars Meinhardt
Vorgang: K-77201 / Kauf vom 12. Januar""",
        "textZh": """主旨：最後補正期限－案號 K-77201

諸位鈞鑒，

儘管 2 月 3 日與 21 日兩次維修，所交付之電動自行車仍有所述煞車缺陷。基於安全，無法再合理期待繼續使用。我已於 2 月 28 日書面催告並請求立即救濟。

謹此設定最後期限至 4 月 18 日：請專業排除瑕疵或交付同等替代。若屆時無可行救濟，我將解除買賣契約，要求回復原狀並請求可能鑑定費用之賠償。無功能驗證之再次局部維修，我拒絕接受。

請確認收悉本函，並告知分機聯絡人。通訊請以書面寄至下方地址；無案號之電話承諾，我不視為有拘束力。我仍願及時、可追蹤地解決。

此致問候
Lars Meinhardt
案號：K-77201／購買日 1 月 12 日""",
    },
    "b2-78": {
        "text": """Bekanntmachung Ordnungsamt
Vom 1. Juni bis 30. September wird die Mittelstraße zwischen Kirchplatz und Bahnhofstraße als Fußgängerzone im Verkehrsversuch geführt. Ziel ist die Prüfung von Aufenthaltsqualität, Einzelhandelsfrequenzen und Rettungswegen unter Alltagsbedingungen.

Lieferverkehr ist täglich 6–11 Uhr freigegeben; außerhalb dieses Fensters nur mit Sondergenehmigung. Anliegern bleibt die Zufahrt zu Tiefgaragen über die Parallelstraße erhalten. Der ÖPNV nutzt eine umgeleitete Linie; aktuelle Fahrpläne liegen in den Stationen und unter stadt.example/versuch aus.

Einwendungen und Beobachtungen können bis 15. Oktober über das Online-Formular eingereicht werden. Die Auswertung erfolgt unabhängig und wird öffentlich vorgestellt, bevor über eine Verstetigung entschieden wird. Ordnungswidrigkeiten – insbesondere unzulässiges Befahren – werden konsequent geahndet. Hinweise zu Barrierefreiheit finden Sie in derselben Bekanntmachung online.

Diese Anordnung tritt am 1. Juni in Kraft und ersetzt die vorläufige Sperrung vom Mai. Bei Großveranstaltungen bleiben gesonderte Hinweise vorbehalten.""",
        "textZh": """秩序機關公告
6 月 1 日至 9 月 30 日，Mittelstraße 於教堂廣場與車站街之間進行行人區交通試驗。目標是在日常條件下檢視停留品質、零售人流與救援動線。

送貨每日 6–11 點開放；時段外僅限特別許可。住戶進出地下車庫改由平行街。大眾運輸改線；最新時刻表見站點與 stadt.example/versuch。

異議與觀察可於 10 月 15 日前經線上表單提交。評估獨立進行並公開說明後，才決定是否常態化。違規行駛等秩序案件將一貫裁罰。無障礙相關說明見同一公告網頁。

本命令 6 月 1 日生效，取代五月臨時封閉。大型活動另有通知。""",
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


def main() -> None:
    data = json.loads(PATH.read_text(encoding="utf-8"))
    existing_ids = {it["id"] for it in data["items"]}
    new_items = UEBUNG + A1 + A2 + B1 + B2
    apply_enrichments(new_items)

    assert len(UEBUNG) == 15 and len(A1) == 15 and len(A2) == 15 and len(B1) == 15 and len(B2) == 15

    for it in new_items:
        assert it["id"] not in existing_ids, it["id"]
        assert 4 <= len(it["notes"]) <= 7, (it["id"], len(it["notes"]))
        assert 2 <= len(it["patterns"]) <= 4, (it["id"], len(it["patterns"]))
        assert 2 <= len(it["tips"]) <= 3, (it["id"], len(it["tips"]))
        lo, hi = BANDS[it["level"]]
        L = len(it["text"])
        assert lo <= L <= hi, (it["id"], L, lo, hi)

    before = len(data["items"])
    data["items"].extend(new_items)
    data["levels"] = ["練習", "A1", "A2", "B1", "B2"]
    data["note"] = NOTE
    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    by = Counter(it["level"] for it in data["items"])
    lens: dict[str, list[int]] = defaultdict(list)
    for it in data["items"]:
        lens[it["level"]].append(len(it["text"]))

    print(f"appended {len(new_items)} (was {before}, now {len(data['items'])})")
    assert len(data["items"]) == 425, len(data["items"])
    for lv in data["levels"]:
        assert by[lv] == 85, (lv, by[lv])
        avg = sum(lens[lv]) / len(lens[lv])
        print(f"  {lv}: n={by[lv]} avg_len={avg:.1f} min={min(lens[lv])} max={max(lens[lv])}")

    print("new items (71–85) avg lengths:")
    for lv in data["levels"]:
        new = [it for it in new_items if it["level"] == lv]
        avg = sum(len(it["text"]) for it in new) / len(new)
        print(
            f"  {lv}: avg={avg:.1f} "
            f"min={min(len(it['text']) for it in new)} "
            f"max={max(len(it['text']) for it in new)}"
        )
    print("note:", data["note"])


if __name__ == "__main__":
    main()
