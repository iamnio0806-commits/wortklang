#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate immersive graded story series for Wortklang."""
from __future__ import annotations

import json
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "src" / "data" / "stories.json"

NOTE = (
    "連貫分級故事：同一系列角色與情節會延續。A1 章節約 180–320 字元，"
    "A2 約 350–500。先聽／讀德文，再對照繁中與重點片語。"
)


def n(span: str, zh: str, tip: str = "") -> dict:
    d: dict = {"span": span, "zh": zh}
    if tip:
        d["tip"] = tip
    return d


def chapter(
    series_id: str,
    order: int,
    title: str,
    title_zh: str,
    text: str,
    text_zh: str,
    focus: list[str],
    notes: list[dict],
) -> dict:
    return {
        "id": f"{series_id}-{order:02d}",
        "order": order,
        "title": title,
        "titleZh": title_zh,
        "text": text.strip(),
        "textZh": text_zh.strip(),
        "focus": focus,
        "notes": notes,
    }


def series(
    sid: str,
    level: str,
    title: str,
    title_zh: str,
    blurb_zh: str,
    chapters: list[dict],
) -> dict:
    return {
        "id": sid,
        "level": level,
        "title": title,
        "titleZh": title_zh,
        "blurbZh": blurb_zh,
        "chapters": chapters,
    }


# ── A1-1: Anna in der Stadt ─────────────────────────────────────────
ANNA = "anna-stadt"
ANNA_CHS = [
    chapter(
        ANNA, 1, "Guten Morgen", "早安",
        """Anna wacht auf. Die Sonne scheint.
Sie sagt: „Guten Morgen!“
Anna steht auf und geht ins Bad.
Sie wäscht sich und putzt die Zähne.
Dann trinkt sie einen Kaffee.
Heute ist ein schöner Tag in der Stadt.""",
        """安娜醒來。太陽照耀著。
她說：「早安！」
安娜起床走進浴室。
她洗臉並刷牙。
然後她喝一杯咖啡。
今天在城市裡是美好的一天。""",
        ["sein", "Begrüßung", "Tagesablauf"],
        [
            n("Guten Morgen", "早安", "早上用；中午 Guten Tag。"),
            n("wacht auf", "醒來", "aufwachen：可分動詞。"),
            n("steht auf", "起床", "aufstehen。"),
            n("wäscht sich", "洗臉／洗澡", "sich waschen。"),
            n("putzt die Zähne", "刷牙"),
        ],
    ),
    chapter(
        ANNA, 2, "Frühstück", "早餐",
        """Anna macht Frühstück. Sie isst Brot mit Käse.
Dazu trinkt sie Orangensaft.
Ihr Handy klingelt. Es ist Lisa.
Lisa: „Hallo Anna! Hast du Zeit?“
Anna: „Ja! Was möchtest du machen?“
Lisa: „Kommst du mit in die Stadt?“
Anna: „Ja, gerne! Bis später!“""",
        """安娜做早餐。她吃起司麵包。
還喝柳橙汁。
她的手機響了。是 Lisa。
Lisa：「嗨安娜！你有空嗎？」
安娜：「有！你想做什麼？」
Lisa：「你要一起進城嗎？」
安娜：「好，很樂意！待會見！」""",
        ["Frühstück", "einladen", "Zeit"],
        [
            n("Hast du Zeit?", "你有空嗎？"),
            n("Kommst du mit…?", "你要一起……嗎？", "mitkommen。"),
            n("gerne", "很樂意／喜歡"),
            n("Bis später", "待會見"),
            n("Dazu", "此外／搭配"),
        ],
    ),
    chapter(
        ANNA, 3, "Mit dem Bus", "搭公車",
        """Anna nimmt den Bus. An der Haltestelle wartet Lisa.
Lisa: „Hallo! Wie geht's?“
Anna: „Gut, danke. Und dir?“
Lisa: „Auch gut!“
Der Bus kommt. Die beiden steigen ein.
Lisa: „Wir fahren zum Park.“
Anna schaut aus dem Fenster. Die Stadt ist groß.""",
        """安娜搭公車。Lisa 在公車站等著。
Lisa：「嗨！你好嗎？」
安娜：「很好，謝謝。你呢？」
Lisa：「也很好！」
公車來了。兩人上車。
Lisa：「我們去公園。」
安娜望向窗外。城市很大。""",
        ["Verkehr", "Wie geht's", "Richtung"],
        [
            n("nimmt den Bus", "搭公車", "nehmen + Verkehrsmittel。"),
            n("Haltestelle", "公車站"),
            n("steigen ein", "上車", "einsteigen。"),
            n("Wie geht's?", "你好嗎？", "口語＝Wie geht es dir?"),
            n("Und dir?", "你呢？"),
        ],
    ),
    chapter(
        ANNA, 4, "Im Park", "在公園",
        """Im Park ist es ruhig. Die Vögel singen.
Anna und Lisa gehen spazieren.
Lisa: „Schau! Ein Eiswagen!“
Anna: „Mmm, ich möchte ein Eis.“
Sie kaufen zwei Kugeln.
Anna: „Mein Eis ist Vanille. Und deins?“
Lisa: „Schokolade. Sehr lecker!“
Sie sitzen auf einer Bank und lachen.""",
        """公園裡很安靜。鳥在唱歌。
安娜和 Lisa 去散步。
Lisa：「看！冰淇淋車！」
安娜：「嗯，我想要一支冰淇淋。」
她們買了兩球。
安娜：「我的是香草。你的呢？」
Lisa：「巧克力。很好吃！」
她們坐在長椅上笑著。""",
        ["Freizeit", "möchten", "Essen"],
        [
            n("gehen spazieren", "去散步"),
            n("ich möchte", "我想要", "möchten＝客氣的「想要」。"),
            n("Kugel", "（冰淇淋）球"),
            n("lecker", "好吃"),
            n("Bank", "長椅", "也指銀行；此處是公園長椅。"),
        ],
    ),
    chapter(
        ANNA, 5, "Im Café", "在咖啡廳",
        """Später gehen sie in ein Café.
Der Kellner fragt: „Was möchten Sie?“
Anna: „Einen Tee, bitte.“
Lisa: „Einen Kaffee mit Milch.“
Kellner: „Sonst noch etwas?“
Anna: „Nein, danke.“
Das macht 6 Euro. Anna bezahlt.
Lisa: „Danke! Nächstes Mal zahle ich.“""",
        """之後她們走進一間咖啡廳。
服務生問：「您想要什麼？」
安娜：「一杯茶，麻煩。」
Lisa：「一杯加牛奶的咖啡。」
服務生：「還要別的嗎？」
安娜：「不用，謝謝。」
一共 6 歐元。安娜付錢。
Lisa：「謝謝！下次我請。」""",
        ["Café", "Sie", "bezahlen"],
        [
            n("Was möchten Sie?", "您想要什麼？", "對服務場合用 Sie。"),
            n("Einen Tee, bitte", "一杯茶，麻煩", "陽性第四格：ein→einen。"),
            n("Sonst noch etwas?", "還要別的嗎？"),
            n("Das macht … Euro", "一共……歐元"),
            n("Nächstes Mal", "下次"),
        ],
    ),
    chapter(
        ANNA, 6, "Einkaufen", "購物",
        """Nach dem Café gehen sie einkaufen.
Anna braucht eine neue Tasche.
Im Laden sagt die Verkäuferin: „Kann ich helfen?“
Anna: „Ja. Wie viel kostet die blaue Tasche?“
Verkäuferin: „Sie kostet 25 Euro.“
Anna: „Okay, ich nehme sie.“
Lisa: „Die Farbe steht dir gut!“""",
        """咖啡廳之後她們去購物。
安娜需要一個新包包。
店裡售貨員說：「需要幫忙嗎？」
安娜：「是的。藍色包包多少錢？」
售貨員：「25 歐元。」
安娜：「好，我要這個。」
Lisa：「這顏色很適合你！」""",
        ["Einkaufen", "Preise", "Farben"],
        [
            n("Wie viel kostet…?", "……多少錢？"),
            n("Ich nehme sie", "我要這個／買它", "nehmen＝選定購買。"),
            n("Kann ich helfen?", "需要幫忙嗎？"),
            n("steht dir gut", "很適合你", "顏色／衣服合身合色。"),
            n("braucht", "需要", "brauchen。"),
        ],
    ),
    chapter(
        ANNA, 7, "Der Regen", "下雨了",
        """Draußen regnet es plötzlich.
Anna: „Oh nein! Ich habe keinen Schirm.“
Lisa: „Ich habe einen. Komm unter meinen Schirm!“
Sie laufen schnell zur Bushaltestelle.
Anna: „Danke, du bist eine gute Freundin.“
Lisa: „Gern geschehen!“
Der Bus kommt gerade. Sie steigen nass und froh ein.""",
        """外面突然下雨了。
安娜：「喔不！我沒有傘。」
Lisa：「我有一把。到我傘下來！」
她們快步跑向公車站。
安娜：「謝謝，你真是好朋友。」
Lisa：「不客氣！」
公車剛好來了。她們溼著卻開心地上車。""",
        ["Wetter", "helfen", "Freundschaft"],
        [
            n("regnet es", "下雨", "es regnet。"),
            n("Schirm", "傘", "Regenschirm。"),
            n("Gern geschehen", "不客氣"),
            n("plötzlich", "突然"),
            n("gute Freundin", "好朋友（陰性）"),
        ],
    ),
    chapter(
        ANNA, 8, "Zu Hause", "回到家",
        """Zu Hause ist Anna müde, aber glücklich.
Sie schreibt Lisa eine Nachricht:
„Danke für den schönen Tag! Bis bald!“
Lisa antwortet: „Gern! Morgen im Park?“
Anna: „Ja! Um 10 Uhr.“
Anna lächelt. Die Stadt ist schön —
besonders mit einer Freundin.""",
        """回到家，安娜疲倦但快樂。
她傳訊息給 Lisa：
「謝謝美好的一天！明天見！」
Lisa 回覆：「不客氣！明天公園見？」
安娜：「好！十點。」
安娜微笑。城市很美——
尤其是有朋友一起。""",
        ["Nachricht", "planen", "Gefühle"],
        [
            n("Bis bald", "改天見／明天見"),
            n("müde", "疲倦"),
            n("glücklich", "快樂"),
            n("Nachricht", "訊息／消息"),
            n("besonders", "尤其／特別"),
            n("Um 10 Uhr", "在十點", "um + 時間。"),
        ],
    ),
]

# ── A1-2: Tom und der Umzug ─────────────────────────────────────────
TOM = "tom-umzug"
TOM_CHS = [
    chapter(
        TOM, 1, "Ein Brief", "一封信",
        """Tom wohnt in München. Heute kommt ein Brief.
Tom öffnet ihn und liest.
„Lieber Tom, wir haben eine Wohnung in Hamburg.
Kommst du uns helfen?“
Es ist von seinem Freund Paul.
Tom denkt: „Hamburg ist weit. Aber Paul ist mein Freund.“
Er ruft Paul an.""",
        """Tom 住在慕尼黑。今天來了一封信。
Tom 打開並閱讀。
「親愛的 Tom，我們在漢堡有一間公寓。
你能來幫我們嗎？」
信是他朋友 Paul 寄的。
Tom 想：「漢堡很遠。但 Paul 是我的朋友。」
他打電話給 Paul。""",
        ["wohnen", "Brief", "helfen"],
        [
            n("Brief", "信"),
            n("Kommst du uns helfen?", "你能來幫我們嗎？"),
            n("ruft … an", "打電話給……", "anrufen。"),
            n("weit", "遠"),
            n("Wohnung", "公寓／房子"),
        ],
    ),
    chapter(
        TOM, 2, "Am Telefon", "通電話",
        """Paul: „Hallo Tom! Danke für den Anruf.“
Tom: „Wann braucht ihr Hilfe?“
Paul: „Am Samstag. Um 9 Uhr.“
Tom: „Okay. Ich nehme den Zug.“
Paul: „Super! Bring bitte Handschuhe mit.“
Tom: „Kein Problem. Bis Samstag!“
Tom packt seine Tasche. Er ist bereit.""",
        """Paul：「嗨 Tom！謝謝來電。」
Tom：「你們什麼時候需要幫忙？」
Paul：「星期六。九點。」
Tom：「好。我搭火車。」
Paul：「太好了！請帶手套來。」
Tom：「沒問題。星期六見！」
Tom 打包行李。他準備好了。""",
        ["Telefon", "Zeit", "vorbereiten"],
        [
            n("Am Samstag", "在星期六", "am + 星期。"),
            n("Bring … mit", "帶……來", "mitbringen。"),
            n("Kein Problem", "沒問題"),
            n("packt", "打包", "packen。"),
            n("bereit", "準備好"),
        ],
    ),
    chapter(
        TOM, 3, "Im Zug", "在火車上",
        """Am Freitagabend sitzt Tom im Zug.
Neben ihm sitzt eine Frau.
Frau: „Fahren Sie nach Hamburg?“
Tom: „Ja. Ich helfe einem Freund.“
Frau: „Das ist nett!“
Tom liest ein Buch. Der Zug fährt schnell.
Um 22 Uhr ist er in Hamburg. Paul wartet am Bahnhof.""",
        """星期五晚上 Tom 坐在火車上。
旁邊坐著一位女士。
女士：「您去漢堡嗎？」
Tom：「是的。我去幫一個朋友。」
女士：「真好！」
Tom 讀一本書。火車開得很快。
二十二點他到漢堡。Paul 在車站等著。""",
        ["Reisen", "Sie", "Bahnhof"],
        [
            n("Fahren Sie nach…?", "您去……嗎？"),
            n("Das ist nett", "真好／真貼心"),
            n("Bahnhof", "火車站"),
            n("Neben ihm", "在他旁邊"),
            n("wartet", "等待", "warten。"),
        ],
    ),
    chapter(
        TOM, 4, "Die neue Wohnung", "新公寓",
        """Paul zeigt Tom die Wohnung.
Paul: „Hier ist das Wohnzimmer. Dort die Küche.“
Tom: „Sehr schön! Und das Schlafzimmer?“
Paul: „Links. Es ist noch leer.“
Mias Stimme kommt aus der Küche: „Hallo Tom!“
Mia ist Pauls Freundin. Sie kocht Tee.
Tom: „Danke. Morgen packen wir die Kisten.“""",
        """Paul 帶 Tom 看公寓。
Paul：「這裡是客廳。那裡是廚房。」
Tom：「很漂亮！臥室呢？」
Paul：「左邊。還是空的。」
Mia 的聲音從廚房傳來：「嗨 Tom！」
Mia 是 Paul 的女友。她泡茶。
Tom：「謝謝。明天我們就搬箱子。」""",
        ["Wohnung", "Räume", "Lokaladverbien"],
        [
            n("Wohnzimmer", "客廳"),
            n("links", "左邊"),
            n("noch leer", "還是空的"),
            n("Hier / Dort", "這裡／那裡"),
            n("Kisten", "箱子"),
        ],
    ),
    chapter(
        TOM, 5, "Schwere Kisten", "沉重的箱子",
        """Am Samstagmorgen beginnen sie.
Paul: „Diese Kiste ist schwer!“
Tom: „Vorsicht! Langsam.“
Sie tragen die Kisten die Treppe hoch.
Mia: „Passt auf! Die Tür ist eng.“
Nach zwei Stunden sind sie müde.
Tom: „Pause! Ich hole Wasser.“
Alle lachen und trinken.""",
        """星期六早上他們開始。
Paul：「這個箱子很重！」
Tom：「小心！慢慢來。」
他們把箱子抬上樓。
Mia：「小心！門很窄。」
兩小時後他們累了。
Tom：「休息！我去拿水。」
大家笑著喝水。""",
        ["helfen", "Adjektive", "Imperativ"],
        [
            n("schwer", "重", "也指「難」。"),
            n("Vorsicht", "小心"),
            n("Passt auf", "小心／注意", "aufpassen。"),
            n("Pause", "休息／暫停"),
            n("die Treppe hoch", "上樓"),
        ],
    ),
    chapter(
        TOM, 6, "Pizza bestellen", "訂披薩",
        """Abends sind alle hungrig.
Mia: „Sollen wir Pizza bestellen?“
Tom: „Ja! Eine mit Käse und eine mit Gemüse.“
Paul ruft an und bestellt.
Zwanzig Minuten später kommt der Bote.
Paul: „Das Essen ist da!“
Sie sitzen auf dem Boden und essen.
Tom: „Beste Pizza nach dem Umzug!“""",
        """晚上大家都餓了。
Mia：「我們要訂披薩嗎？」
Tom：「好！一份起司、一份蔬菜。」
Paul 打電話訂餐。
二十分鐘後外送員來了。
Paul：「食物到了！」
他們坐在地板上吃。
Tom：「搬家後最好吃的披薩！」""",
        ["Essen", "bestellen", "Sollen"],
        [
            n("Sollen wir…?", "我們要……嗎？", "提議句型。"),
            n("bestellen", "訂購"),
            n("hungrig", "肚子餓"),
            n("Das Essen ist da", "食物到了"),
            n("Bote", "外送員／信差"),
        ],
    ),
    chapter(
        TOM, 7, "Sonntagmorgen", "星期天早上",
        """Am Sonntag scheint die Sonne.
Tom, Paul und Mia putzen die Wohnung.
Mia: „Wohin kommt der Tisch?“
Tom: „Ans Fenster. Da ist mehr Licht.“
Paul hängt Bilder an die Wand.
Die Wohnung sieht jetzt gemütlich aus.
Tom: „Ihr habt ein schönes Zuhause.“""",
        """星期天太陽照耀。
Tom、Paul 和 Mia 打掃公寓。
Mia：「桌子放哪裡？」
Tom：「靠窗。那裡光線比較多。」
Paul 把畫掛上牆。
公寓現在看起來很溫馨。
Tom：「你們有一個漂亮的家。」""",
        ["putzen", "einrichten", "Lokal"],
        [
            n("Wohin kommt…?", "……要放哪裡？"),
            n("Ans Fenster", "靠窗", "an das → ans。"),
            n("gemütlich", "溫馨／舒適"),
            n("hängt … an", "掛上", "hängen an。"),
            n("Zuhause", "家"),
        ],
    ),
    chapter(
        TOM, 8, "Abschied", "告別",
        """Tom muss zurück nach München.
Am Bahnhof umarmen sie sich.
Paul: „Danke für alles, Tom!“
Mia: „Du bist immer willkommen.“
Tom: „Gern geschehen. Besucht mich bald!“
Der Zug fährt ein. Tom winkt.
Paul und Mia winken zurück.
Freunde helfen — und Freunde bleiben.""",
        """Tom 必須回慕尼黑。
在車站他們互相擁抱。
Paul：「謝謝一切，Tom！」
Mia：「隨時歡迎你來。」
Tom：「不客氣。很快來找我玩！」
火車進站。Tom 揮手。
Paul 和 Mia 也揮手。
朋友互相幫忙——朋友一直都在。""",
        ["Abschied", "danken", "Zukunft"],
        [
            n("Abschied", "告別"),
            n("Du bist willkommen", "歡迎你"),
            n("Besucht mich", "來找我／拜訪我", "besuchen。"),
            n("winkt", "揮手", "winken。"),
            n("muss zurück", "必須回去"),
        ],
    ),
]

# ── A1-3: Mia lernt kochen ──────────────────────────────────────────
MIA = "mia-kochen"
MIA_CHS = [
    chapter(
        MIA, 1, "Hunger!", "好餓！",
        """Mia kommt nach Hause. Sie hat Hunger.
Im Kühlschrank ist nicht viel:
etwas Milch, ein Ei und Brot.
Mia: „Oh nein. Was koche ich?“
Sie ruft ihre Oma an.
Oma: „Hallo, Liebling! Alles gut?“
Mia: „Oma, kannst du mir helfen? Ich will kochen lernen.“""",
        """Mia 回到家。她肚子餓。
冰箱裡東西不多：
一點牛奶、一顆蛋和麵包。
Mia：「喔不。我煮什麼？」
她打電話給奶奶。
奶奶：「嗨，寶貝！一切都好嗎？」
Mia：「奶奶，你能幫我嗎？我想學煮飯。」""",
        ["Hunger", "Kühlschrank", "lernen"],
        [
            n("Hunger haben", "肚子餓", "Ich habe Hunger。"),
            n("Kühlschrank", "冰箱"),
            n("etwas Milch", "一點牛奶", "不可數用 etwas。"),
            n("Liebling", "寶貝／親愛的"),
            n("kochen lernen", "學煮飯"),
        ],
    ),
    chapter(
        MIA, 2, "Omas Plan", "奶奶的計畫",
        """Oma: „Komm morgen zu mir. Wir kochen zusammen.“
Mia: „Was kochen wir?“
Oma: „Einfache Suppe und Nudeln. Sehr leicht!“
Mia: „Perfekt. Was soll ich mitbringen?“
Oma: „Tomaten und Zwiebeln, bitte.“
Mia: „Okay! Bis morgen, Oma.“
Mia ist froh. Morgen wird spannend.""",
        """奶奶：「明天來我家。我們一起煮。」
Mia：「我們煮什麼？」
奶奶：「簡單的湯和麵。很容易！」
Mia：「太好了。我要帶什麼來？」
奶奶：「番茄和洋蔥，麻煩。」
Mia：「好！明天見，奶奶。」
Mia 很開心。明天會很有趣。""",
        ["planen", "Lebensmittel", "mitbringen"],
        [
            n("Wir kochen zusammen", "我們一起煮"),
            n("leicht", "容易／輕"),
            n("Was soll ich…?", "我該……？"),
            n("mitbringen", "帶來"),
            n("spannend", "刺激／有趣"),
        ],
    ),
    chapter(
        MIA, 3, "Auf dem Markt", "在市場",
        """Am nächsten Tag geht Mia auf den Markt.
Verkäufer: „Frische Tomaten! Heute günstig!“
Mia: „Ein Kilo Tomaten, bitte. Und zwei Zwiebeln.“
Verkäufer: „Das macht 4 Euro.“
Mia bezahlt und sagt: „Danke, schönen Tag!“
Die Tüte ist schwer, aber Mia lächelt.
Sie geht zu Oma.""",
        """隔天 Mia 去市場。
攤販：「新鮮番茄！今天便宜！」
Mia：「一公斤番茄，麻煩。還有兩顆洋蔥。」
攤販：「一共 4 歐元。」
Mia 付錢並說：「謝謝，祝您有美好的一天！」
袋子很重，但 Mia 微笑著。
她走向奶奶家。""",
        ["Markt", "Mengen", "Höflichkeit"],
        [
            n("Ein Kilo", "一公斤"),
            n("günstig", "便宜／划算"),
            n("frische", "新鮮的"),
            n("schönen Tag", "祝美好的一天", "告別／祝福用語。"),
            n("Tüte", "袋子"),
        ],
    ),
    chapter(
        MIA, 4, "In Omas Küche", "在奶奶廚房",
        """Oma öffnet die Tür. „Willkommen, Mia!“
Die Küche riecht nach Kräutern.
Oma: „Wasch zuerst die Tomaten.“
Mia wäscht und schneidet.
Oma: „Sehr gut. Jetzt die Zwiebeln — aber vorsichtig!“
Mia: „Autsch! Die Zwiebeln beißen in die Augen.“
Oma lacht: „Das kennen alle Köche.“""",
        """奶奶開門。「歡迎，Mia！」
廚房有香草氣味。
奶奶：「先洗番茄。」
Mia 清洗並切好。
奶奶：「很好。現在洋蔥——但要小心！」
Mia：「哎喲！洋蔥刺眼睛。」
奶奶笑：「所有廚師都知道。」""",
        ["Küche", "Imperativ", "schneiden"],
        [
            n("Willkommen", "歡迎"),
            n("Wasch zuerst…", "先洗……", "祈使句。"),
            n("schneiden", "切"),
            n("vorsichtig", "小心的"),
            n("riecht nach", "聞起來像……"),
        ],
    ),
    chapter(
        MIA, 5, "Die Suppe kocht", "湯在煮",
        """Oma gibt Öl in die Pfanne.
Dann kommen Zwiebeln und Tomaten hinein.
Oma: „Jetzt Salz und Pfeffer.“
Mia rührt um. Die Suppe kocht.
Oma: „Zehn Minuten warten.“
Mia: „Es riecht fantastisch!“
Oma: „Warte ab. Gleich schmeckt es noch besser.“""",
        """奶奶把油倒進鍋裡。
接著洋蔥和番茄下鍋。
奶奶：「現在加鹽和胡椒。」
Mia 攪拌。湯在煮。
奶奶：「等十分鐘。」
Mia：「味道棒極了！」
奶奶：「等著看。馬上會更好吃。」""",
        ["kochen", "Gewürze", "warten"],
        [
            n("gibt … hinein", "放進去"),
            n("rührt um", "攪拌", "umrühren。"),
            n("Salz und Pfeffer", "鹽和胡椒"),
            n("kocht", "在煮／沸騰"),
            n("Warte ab", "等著看", "abwarten。"),
        ],
    ),
    chapter(
        MIA, 6, "Nudeln dazu", "再配麵",
        """Oma kocht auch Nudeln.
Mia: „Sind sie fertig?“
Oma: „Ja. Probier mal!“
Mia probiert die Suppe. „Mmm! Sehr lecker.“
Oma: „Du hast gut geholfen.“
Sie decken den Tisch.
Zwei Teller, zwei Löffel, Brot dazu.
Es ist ein kleines Fest.""",
        """奶奶也煮了麵。
Mia：「好了嗎？」
奶奶：「好了。嚐嚐看！」
Mia 嚐湯。「嗯！很好喝。」
奶奶：「你幫了很多忙。」
她們擺桌子。
兩個盤子、兩支湯匙，再配麵包。
這是一場小小的慶祝。""",
        ["probieren", "Tisch", "loben"],
        [
            n("fertig", "完成／好了"),
            n("Probier mal", "嚐嚐看", "probieren。"),
            n("decken den Tisch", "擺桌子"),
            n("dazu", "搭配／另加"),
            n("Fest", "慶典／宴會"),
        ],
    ),
    chapter(
        MIA, 7, "Rezept aufschreiben", "寫下食譜",
        """Nach dem Essen holt Oma Papier.
Oma: „Schreib das Rezept auf.“
Mia schreibt langsam:
Tomaten, Zwiebeln, Salz, Pfeffer, Öl, Nudeln.
Mia: „Und die Zeit?“
Oma: „Zehn Minuten für die Suppe. Acht für die Nudeln.“
Mia: „Danke, Oma. Jetzt kann ich allein kochen!“""",
        """飯後奶奶拿出紙。
奶奶：「把食譜寫下來。」
Mia 慢慢寫：
番茄、洋蔥、鹽、胡椒、油、麵。
Mia：「時間呢？」
奶奶：「湯十分鐘。麵八分鐘。」
Mia：「謝謝奶奶。現在我可以自己煮了！」""",
        ["Rezept", "schreiben", "allein"],
        [
            n("Rezept", "食譜／處方"),
            n("Schreib … auf", "寫下來", "aufschreiben。"),
            n("allein", "獨自"),
            n("holt", "拿來", "holen。"),
            n("langsam", "慢慢地"),
        ],
    ),
    chapter(
        MIA, 8, "Für Freunde", "為朋友煮",
        """Eine Woche später kommen Freunde zu Mia.
Anna und Lisa klingeln an der Tür.
Mia: „Willkommen! Heute koche ich.“
Im Topf kocht Omas Suppe.
Anna: „Wow, das riecht gut!“
Lisa: „Darf ich helfen?“
Mia: „Nein, setzt euch. Genießt!“
Sie essen und lachen. Mia ist stolz.""",
        """一週後朋友們來找 Mia。
Anna 和 Lisa 按門鈴。
Mia：「歡迎！今天我煮飯。」
鍋裡煮著奶奶的湯。
Anna：「哇，好香！」
Lisa：「我可以幫忙嗎？」
Mia：「不用，坐下。享用吧！」
她們邊吃邊笑。Mia 很驕傲。""",
        ["einladen", "stolz", "Gastgeber"],
        [
            n("klingeln", "按門鈴"),
            n("Darf ich…?", "我可以……嗎？"),
            n("setzt euch", "坐下（你們）", "sich setzen。"),
            n("Genießt", "享用吧", "genießen。"),
            n("stolz", "驕傲"),
        ],
    ),
]

# ── A2 (easy): Jonas am See ─────────────────────────────────────────
JONAS = "jonas-see"
JONAS_CHS = [
    chapter(
        JONAS, 1, "Die Einladung", "邀請",
        """Jonas bekommt eine Nachricht von seinem Cousin Felix.
„Hallo Jonas! Am Wochenende fahren wir an den See.
Möchtest du mitkommen? Wir schwimmen, grillen und zelten.“
Jonas arbeitet unter der Woche im Büro und ist oft müde.
Aber ein Wochenende am Wasser klingt perfekt.
Er antwortet schnell: „Ja! Wann und wo treffen wir uns?“
Felix schreibt: „Samstag um 8 Uhr am Bahnhof. Bring Schlafsack und Sonnencreme mit.“""",
        """Jonas 收到表哥 Felix 的訊息。
「嗨 Jonas！週末我們去湖邊。
你要一起來嗎？我們游泳、烤肉和露營。」
Jonas 平日在辦公室工作，常常很累。
但在水邊度過週末聽起來很完美。
他很快回覆：「好！我們何時何地碰面？」
Felix 寫：「星期六八點在車站。帶睡袋和防曬霜。」""",
        ["Einladung", "Wochenende", "mitkommen"],
        [
            n("Möchtest du mitkommen?", "你想一起來嗎？"),
            n("klingt perfekt", "聽起來很完美"),
            n("unter der Woche", "平日／週間"),
            n("Schlafsack", "睡袋"),
            n("treffen wir uns", "我們碰面", "sich treffen。"),
            n("Bring … mit", "把……帶來", "mitbringen。"),
        ],
    ),
    chapter(
        JONAS, 2, "Früh am Bahnhof", "清晨火車站",
        """Am Samstag steht Jonas früh auf. Der Himmel ist klar.
Am Bahnhof warten schon Felix und dessen Freundin Nora.
Nora: „Schön, dass du da bist! Kennst du den See?“
Jonas: „Nein, noch nicht. Ich freue mich darauf.“
Sie kaufen Tickets und steigen in den Regionalzug.
Im Zug erzählt Felix von dem Campingplatz: ruhig, nah am Wasser, mit einem kleinen Kiosk.
Jonas schaut aus dem Fenster. Felder und Wälder ziehen vorbei.""",
        """星期六 Jonas 早早起床。天空晴朗。
在車站，Felix 和他女友 Nora 已經在等。
Nora：「很高興你來了！你認識那個湖嗎？」
Jonas：「還沒。我很期待。」
他們買票上了區間車。
車上 Felix 描述露營區：安靜、靠近水邊，還有小賣店。
Jonas 望向窗外。田野和森林掠過。""",
        ["Reisen", "sich freuen", "Beschreiben"],
        [
            n("Schön, dass du da bist", "很高興你來了"),
            n("Ich freue mich darauf", "我很期待", "sich freuen auf。"),
            n("Regionalzug", "區間車／區域列車"),
            n("Campingplatz", "露營區"),
            n("ziehen vorbei", "掠過／經過"),
        ],
    ),
    chapter(
        JONAS, 3, "Ankunft am See", "抵達湖邊",
        """Nach zwei Stunden kommen sie an. Der See liegt ruhig und blau vor ihnen.
Felix: „Zuerst das Zelt aufbauen, dann schwimmen.“
Sie tragen Rucksäcke den Weg hinunter. Nora sucht einen flachen Platz.
Jonas hält die Stangen, Felix spannt die Plane. Nach einer Weile steht das Zelt.
Nora lacht: „Nicht schlecht für Anfänger!“
Jonas wischt sich den Schweiß ab und atmet die frische Luft ein.
Gleich nebenan glitzert das Wasser.""",
        """兩小時後他們抵達。平靜藍色的湖就在眼前。
Felix：「先搭帳篷，再游泳。」
他們背著背包走下小路。Nora 找一塊平坦的地方。
Jonas 扶著桿子，Felix 拉起篷布。過一會兒帳篷立好了。
Nora 笑：「對新手來說不錯！」
Jonas 擦掉汗水，吸入新鮮空氣。
緊鄰著，水面閃閃發光。""",
        ["Camping", "aufbauen", "Natur"],
        [
            n("Zelt aufbauen", "搭帳篷"),
            n("Nach einer Weile", "過一會兒"),
            n("Nicht schlecht", "不錯"),
            n("atmet … ein", "吸入", "einatmen。"),
            n("gleich nebenan", "就在旁邊"),
            n("glitzert", "閃閃發光"),
        ],
    ),
    chapter(
        JONAS, 4, "Das erste Bad", "第一次下水",
        """Die Sonne steht hoch. Nora springt zuerst ins Wasser.
„Kalt, aber herrlich!“ ruft sie.
Jonas geht langsam hinein. Das Wasser reicht ihm bis zur Brust.
Felix schwimmt ein paar Bahnen und kommt zurück.
Felix: „Kannst du gut schwimmen?“
Jonas: „Ein bisschen. In der Stadt gehe ich selten ins Bad.“
Sie treiben eine Weile auf dem Rücken und schauen in den Himmel.
Möwen kreisen über dem See.""",
        """太陽高掛。Nora 先跳進水裡。
她喊：「冷，但太棒了！」
Jonas 慢慢走進去。水到他胸口。
Felix 游了幾個來回再回來。
Felix：「你很會游泳嗎？」
Jonas：「一點點。在城裡我很少去泳池。」
他們仰躺漂浮一會兒，望著天空。
海鷗在湖上盤旋。""",
        ["schwimmen", "Körper", "Gegensatz"],
        [
            n("herrlich", "美妙／太棒了"),
            n("reicht … bis", "到……為止"),
            n("ein paar Bahnen", "幾個來回（泳道）"),
            n("Ein bisschen", "一點點"),
            n("selten", "很少"),
            n("treiben", "漂浮／漂流"),
        ],
    ),
    chapter(
        JONAS, 5, "Einkauf am Kiosk", "小賣店採買",
        """Am Nachmittag gehen sie zum Kiosk.
Verkäuferin: „Was darf's sein?“
Nora: „Drei Wasser, Brot, Käse und Äpfel, bitte.“
Felix: „Und Holzkohle für den Grill.“
Die Verkäuferin packt alles ein. „Das macht 18 Euro.“
Jonas bezahlt und sagt: „Darf ich die Tasche tragen?“
Zurück am Zelt schneiden sie das Brot und machen einfache Stulle.
Der Wind vom See ist leicht und angenehm.""",
        """下午他們去小賣店。
店員：「要什麼？」
Nora：「三瓶水、麵包、起司和蘋果，麻煩。」
Felix：「還有烤肉用的木炭。」
店員打包。「一共 18 歐元。」
Jonas 付錢並說：「袋子我來提好嗎？」
回到帳篷，他們切麵包做簡單三明治。
湖風輕柔舒適。""",
        ["einkaufen", "Grill", "Höflichkeit"],
        [
            n("Was darf's sein?", "要什麼？", "店員常用。"),
            n("Holzkohle", "木炭"),
            n("packt … ein", "打包", "einpacken。"),
            n("Stulle", "（北德）開放式三明治"),
            n("angenehm", "舒適／宜人"),
        ],
    ),
    chapter(
        JONAS, 6, "Abend am Grill", "傍晚烤肉",
        """Als die Sonne sinkt, zünden sie den Grill an.
Felix legt Würstchen auf den Rost. Nora schneidet Gurken.
Jonas erzählt von seiner Arbeit: Meetings, E-Mails, wenig Bewegung.
Nora: „Deshalb bist du hier. Pause vom Alltag.“
Sie essen, trinken Apfelschorle und hören leise Musik.
Am Nachbarzelt sitzt eine Familie und lacht.
Jonas denkt: Hier brauche ich kein Handy. Nur Freunde und den See.""",
        """太陽下沉時，他們點燃烤肉架。
Felix 把香腸放上烤網。Nora 切黃瓜。
Jonas 談起工作：會議、郵件、很少運動。
Nora：「所以你才來這裡。暫時離開日常。」
他們吃東西、喝蘋果氣泡汁，聽著輕柔音樂。
隔壁帳篷坐著一家人在笑。
Jonas 想：這裡我不需要手機。只要朋友和湖。""",
        ["Grill", "Alltag", "Gedanken"],
        [
            n("Als die Sonne sinkt", "當太陽下沉時", "als＝過去／一次性時間。"),
            n("zünden … an", "點燃", "anzünden。"),
            n("Pause vom Alltag", "暫時離開日常"),
            n("Apfelschorle", "蘋果氣泡汁"),
            n("Deshalb", "因此"),
        ],
    ),
    chapter(
        JONAS, 7, "Die Nacht", "夜晚",
        """Nachts wird es kühl. Sie sitzen noch eine Weile am Feuer.
Felix zeigt Jonas die Sterne: „Dort ist der Große Wagen.“
Jonas findet ihn nach ein paar Minuten. „Ah, jetzt sehe ich ihn!“
Später kriechen sie in die Schlafsäcke. Nora liest kurz mit der Taschenlampe.
Draußen ruft ein Vogel. Das Wasser plätschert leise.
Jonas schließt die Augen und schläft schneller ein als in der Stadt.""",
        """夜裡變涼。他們還在營火旁坐一會兒。
Felix 指給 Jonas 看星星：「那裡是北斗七星。」
Jonas 過幾分鐘才找到。「啊，現在看到了！」
之後他們鑽進睡袋。Nora 用手電筒短暫看書。
外頭有鳥叫。水聲輕輕拍打。
Jonas 閉上眼，比在城裡更快入睡。""",
        ["Nacht", "Natur", "Vergleich"],
        [
            n("Nachts", "在夜裡", "時間副詞。"),
            n("Große Wagen", "北斗七星"),
            n("kriechen", "爬／鑽進"),
            n("Taschenlampe", "手電筒"),
            n("schläft … ein", "入睡", "einschlafen。"),
            n("plätschert", "拍打作響（水聲）"),
        ],
    ),
    chapter(
        JONAS, 8, "Abschied vom See", "告別湖邊",
        """Am Sonntagmorgen packen sie zusammen. Das Zelt wird kleiner und kleiner.
Felix: „Nächstes Mal bleiben wir zwei Nächte.“
Jonas: „Gerne. Ich habe mich richtig erholt.“
Am Bahnhof umarmen sie sich. Der Zug nach Hause wartet schon.
Im Abteil schreibt Jonas eine kurze Notiz an sich selbst:
„Mehr Tage am Wasser. Weniger Bildschirm.“
Er lächelt und legt das Handy weg. Draußen beginnt die Stadt wieder — aber der See bleibt in seinem Kopf.""",
        """星期天早上他們一起打包。帳篷越收越小。
Felix：「下次我們待兩晚。」
Jonas：「好啊。我真的休息夠了。」
在車站他們互相擁抱。回家的火車已經在等。
車廂裡 Jonas 給自己寫了一則短記：
「多去水邊。少盯螢幕。」
他微笑並把手機放下。外頭城市又開始出現——但湖仍留在他腦中。""",
        ["Abschied", "Vorsätze", "erholen"],
        [
            n("packe zusammen", "一起打包／收拾", "zusammenpacken。"),
            n("Ich habe mich erholt", "我休息夠了／恢復了", "sich erholen。"),
            n("Nächstes Mal", "下次"),
            n("Notiz", "短記／便條"),
            n("legt … weg", "放下／收起", "weglegen。"),
            n("bleibt in seinem Kopf", "留在他腦中"),
        ],
    ),
]


def char_len(text: str) -> int:
    return len(text.strip())


def validate(data: dict) -> None:
    series_list = data["series"]
    assert len(series_list) >= 3, f"need ≥3 series, got {len(series_list)}"
    for s in series_list:
        chs = s["chapters"]
        assert len(chs) == 8, f"{s['id']}: need 8 chapters, got {len(chs)}"
        level = s["level"]
        lo, hi = (180, 320) if level == "A1" else (350, 500)
        for c in chs:
            L = char_len(c["text"])
            assert lo <= L <= hi, (
                f"{c['id']} ({level}): {L} chars, expected {lo}–{hi}"
            )
            assert 4 <= len(c["notes"]) <= 6, (
                f"{c['id']}: need 4–6 notes, got {len(c['notes'])}"
            )
            assert c["textZh"], f"{c['id']}: missing textZh"
            assert c["focus"], f"{c['id']}: missing focus"


def main() -> None:
    data = {
        "note": NOTE,
        "series": [
            series(
                ANNA,
                "A1",
                "Anna in der Stadt",
                "安娜在城市",
                "短短幾章的連貫故事：安娜與好友 Lisa 度過城市裡美好的一天——從早安到回家。",
                ANNA_CHS,
            ),
            series(
                TOM,
                "A1",
                "Tom und der Umzug",
                "Tom 與搬家",
                "Tom 搭火車去漢堡，幫朋友 Paul 和 Mia 搬家：從信件邀請到車站告別。",
                TOM_CHS,
            ),
            series(
                MIA,
                "A1",
                "Mia lernt kochen",
                "Mia 學煮飯",
                "Mia 肚子餓、冰箱空空，於是找奶奶學做簡單番茄湯——最後請朋友來嚐。",
                MIA_CHS,
            ),
            series(
                JONAS,
                "A2",
                "Jonas am See",
                "Jonas 在湖邊",
                "輕鬆 A2：Jonas 週末跟表哥去湖邊露營——搭帳篷、游泳、烤肉，帶回一點平靜。",
                JONAS_CHS,
            ),
        ],
    }
    validate(data)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Series: {len(data['series'])}")
    for s in data["series"]:
        lens = [char_len(c["text"]) for c in s["chapters"]]
        print(
            f"  [{s['level']}] {s['title']} / {s['titleZh']} "
            f"— {len(s['chapters'])} ch, chars {min(lens)}–{max(lens)}"
        )
        for c in s["chapters"]:
            print(f"    {c['order']}. {c['title']} ({char_len(c['text'])})")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print(f"VALIDATION FAILED: {e}", file=sys.stderr)
        sys.exit(1)
