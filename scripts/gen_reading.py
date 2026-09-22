#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate A1/A2 reading items (~50 each) with notes, patterns, tips."""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "src" / "data" / "reading.json"


def item(
    id: str,
    level: str,
    kind: str,
    topic: str,
    title: str,
    title_zh: str,
    text: str,
    text_zh: str,
    notes: list[dict],
    patterns: list[dict],
    tips: list[str],
    focus: list[str],
) -> dict:
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


def n(span: str, zh: str, tip: str = "") -> dict:
    d = {"span": span, "zh": zh}
    if tip:
        d["tip"] = tip
    return d


def p(pattern: str, zh: str, example: str) -> dict:
    return {"pattern": pattern, "zh": zh, "example": example}


# ── A1: very short (dialogues, cards, signs, messages) ──────────────
A1: list[dict] = []

A1 += [
    item(
        "a1-01", "A1", "card", "自我介紹",
        "Hallo, ich bin Anna", "哈囉，我是 Anna",
        "Hallo!\nIch bin Anna.\nIch komme aus Taiwan.\nIch wohne in Berlin.\nIch lerne Deutsch.",
        "哈囉！\n我是 Anna。\n我來自台灣。\n我住在柏林。\n我在學德文。",
        [
            n("Hallo", "哈囉／你好", "很常用的打招呼。"),
            n("Ich bin", "我是", "自我介紹用 sein。"),
            n("komme aus", "來自", "kommen aus + 地方。"),
            n("wohne in", "住在", "wohnen in + 城市。"),
            n("lerne", "學習", "lernen + 科目。"),
        ],
        [
            p("Ich bin + 名字／職業", "自我介紹", "Ich bin Anna.／Ich bin Studentin."),
            p("Ich komme aus + 地方", "說明出身", "Ich komme aus Taiwan."),
            p("Ich wohne in + 城市", "說明住所", "Ich wohne in Berlin."),
        ],
        ["先大聲念五句，再遮住中文自己說。", "把名字換成你的名字練習。"],
        ["sein", "kommen aus", "wohnen"],
    ),
    item(
        "a1-02", "A1", "dialogue", "打招呼",
        "Guten Morgen", "早安對話",
        "Tom: Guten Morgen, Lisa!\nLisa: Guten Morgen, Tom!\nTom: Wie geht's?\nLisa: Gut, danke. Und dir?\nTom: Auch gut!",
        "Tom：早安，Lisa！\nLisa：早安，Tom！\nTom：你好嗎？\nLisa：很好，謝謝。你呢？\nTom：也很好！",
        [
            n("Guten Morgen", "早安", "早上用；中午 Guten Tag，晚上 Guten Abend。"),
            n("Wie geht's?", "你好嗎？", "口語＝Wie geht es dir?"),
            n("danke", "謝謝"),
            n("Und dir?", "你呢？", "對 du 用 dir。"),
            n("Auch gut", "也很好"),
        ],
        [
            p("Guten Morgen / Tag / Abend", "依時段打招呼", "Guten Tag, Frau Müller!"),
            p("Wie geht's? — Gut, danke.", "寒暄問答", "Gut, danke. Und dir?"),
        ],
        ["跟著角色分兩次念。", "記住：問完別人，記得問回來 Und dir?"],
        ["打招呼", "寒暄"],
    ),
    item(
        "a1-03", "A1", "dialogue", "咖啡廳",
        "Im Café", "在咖啡廳",
        "Kellner: Hallo! Was möchten Sie?\nAnna: Einen Kaffee, bitte.\nKellner: Mit Milch?\nAnna: Ja, bitte.\nKellner: Das macht 3 Euro.",
        "服務生：您好！您想要什麼？\nAnna：一杯咖啡，麻煩。\n服務生：要加牛奶嗎？\nAnna：好，麻煩。\n服務生：一共 3 歐元。",
        [
            n("Was möchten Sie?", "您想要什麼？", "對陌生人或服務場合用 Sie。"),
            n("Einen Kaffee", "一杯咖啡", "陽性第四格：ein→einen。"),
            n("bitte", "請／麻煩", "點餐、拜託都常用。"),
            n("Das macht … Euro", "一共……歐元", "結帳句型。"),
        ],
        [
            p("Einen / Eine / Ein + 名詞, bitte", "點東西", "Einen Tee, bitte."),
            p("Das macht + 價錢", "說金額", "Das macht 5 Euro."),
        ],
        ["注意 Einen（不是 Ein）Kaffee。", "練習把咖啡換成 Tee、Wasser。"],
        ["Akkusativ", "Sie", "點餐"],
    ),
    item(
        "a1-04", "A1", "message", "簡訊",
        "WhatsApp von Mia", "Mia 的訊息",
        "Hi Paul!\nBist du heute da?\nIch bin um 5 Uhr frei.\nBis später!\nMia",
        "嗨 Paul！\n你今天在嗎？\n我五點有空。\n待會見！\nMia",
        [
            n("Bist du …?", "你是……嗎？", "sein 的 du 變位。"),
            n("heute", "今天"),
            n("um 5 Uhr", "五點整", "鐘點：um + 數字 + Uhr。"),
            n("frei", "有空／自由的"),
            n("Bis später", "待會見", "口語道別。"),
        ],
        [
            p("Bist du + 形容詞／地方?", "問對方狀態", "Bist du müde?／Bist du zu Hause?"),
            p("Ich bin um … Uhr + 形容詞", "說時間狀態", "Ich bin um 8 Uhr fertig."),
            p("Bis später / Bis morgen", "道別", "Bis morgen!"),
        ],
        ["簡訊很短，適合先當朗讀練習。", "回覆可以寫：Ja, ich bin da!"],
        ["sein", "時間"],
    ),
    item(
        "a1-05", "A1", "sign", "告示",
        "Öffnungszeiten", "營業時間",
        "Bäckerei Sonne\nMo–Fr: 7–18 Uhr\nSa: 8–14 Uhr\nSo: geschlossen",
        "陽光麵包店\n週一至週五：7–18 點\n週六：8–14 點\n週日：公休",
        [
            n("Mo–Fr", "週一到週五", "Montag bis Freitag。"),
            n("Sa", "週六", "Samstag。"),
            n("So", "週日", "Sonntag。"),
            n("geschlossen", "關閉／公休", "反義：geöffnet＝營業中。"),
        ],
        [
            p("Mo–Fr: … Uhr", "平日時間", "Mo–Fr: 9–17 Uhr"),
            p("… : geschlossen", "公休／關閉", "Heute geschlossen."),
        ],
        ["看告示先找今天是星期幾。", "geschlossen 超常見，一定要認得。"],
        ["時間", "告示"],
    ),
]

# Generate more A1 systematically
A1_MORE = [
    ("a1-06", "dialogue", "購物", "Im Supermarkt", "在超市",
     "Verkäuferin: Kann ich Ihnen helfen?\nJonas: Ja. Wo ist die Milch?\nVerkäuferin: Dort links.\nJonas: Danke!\nVerkäuferin: Bitte!",
     "店員：需要幫忙嗎？\nJonas：好。牛奶在哪？\n店員：那邊左邊。\nJonas：謝謝！\n店員：不客氣！",
     [n("Kann ich Ihnen helfen?", "需要我幫您嗎？", "Ihnen＝對 Sie 的第三格。"),
      n("Wo ist …?", "……在哪？"), n("Dort links", "那邊左邊"), n("Bitte!", "不客氣／請")],
     [p("Wo ist + der/die/das + 名詞?", "問路／找東西", "Wo ist der Ausgang?"),
      p("Dort links / rechts / geradeaus", "指示方向", "Dort rechts.")],
     ["Bitte 可當「請」也可當「不客氣」。"], ["方向", "購物"]),
    ("a1-07", "card", "家庭", "Meine Familie", "我的家庭",
     "Das ist meine Familie.\nDas ist mein Vater.\nDas ist meine Mutter.\nDas sind meine Geschwister.\nWir wohnen zusammen.",
     "這是我的家庭。\n這是我爸爸。\n這是我媽媽。\n這些是我的兄弟姐妹。\n我們住在一起。",
     [n("meine / mein", "我的", "陰性 meine，陽性／中性 mein。"),
      n("Das ist", "這是（單數）"), n("Das sind", "這些是（複數）"),
      n("Geschwister", "兄弟姐妹", "只用複數。")],
     [p("Das ist mein / meine + 家人", "介紹家人", "Das ist meine Schwester."),
      p("Das sind + 複數", "介紹複數", "Das sind meine Freunde.")],
     ["先分清 Das ist／Das sind。"], ["所有格", "家庭"]),
    ("a1-08", "dialogue", "時間", "Wie spät ist es?", "現在幾點？",
     "Sara: Entschuldigung, wie spät ist es?\nLeo: Es ist zehn Uhr.\nSara: Danke schön!\nLeo: Kein Problem.",
     "Sara：不好意思，現在幾點？\nLeo：十點。\nSara：謝謝！\nLeo：沒問題。",
     [n("Entschuldigung", "不好意思／對不起"),
      n("wie spät ist es?", "現在幾點？"),
      n("Es ist … Uhr", "現在……點"),
      n("Kein Problem", "沒問題")],
     [p("Wie spät ist es?", "問時間", "Wie spät ist es?"),
      p("Es ist + 數字 + Uhr", "回答時間", "Es ist drei Uhr.")],
     ["問時間很實用，整句背起來。"], ["時間"]),
    ("a1-09", "message", "約會", "Treffen", "碰面",
     "Nina: Treffen wir uns um 6?\nMax: Ja, gerne.\nNina: Am Bahnhof?\nMax: Super. Bis dann!",
     "Nina：我們六點碰面嗎？\nMax：好，很樂意。\nNina：在火車站？\nMax：太好了。到時見！",
     [n("Treffen wir uns …?", "我們碰面嗎？", "sich treffen＝碰面。"),
      n("gerne", "樂意／喜歡"), n("Am Bahnhof", "在火車站", "an dem→am。"),
      n("Bis dann", "到時見")],
     [p("Treffen wir uns um …?", "約時間", "Treffen wir uns um 7?"),
      p("Am / Im / Bei + 地點", "約地點", "Im Café?")],
     ["uns 是「我們自己」，見面常用。"], ["sich treffen", "收縮介系詞"]),
    ("a1-10", "sign", "交通", "Haltestelle", "公車站牌",
     "Bus 12 → Zentrum\nab: 10:05, 10:25, 10:45\nBitte Einstieg nur vorne.",
     "12 路公車 → 市中心\n發車：10:05、10:25、10:45\n請只從前面上車。",
     [n("ab", "從……出發／起"), n("Zentrum", "市中心"),
      n("Einstieg", "上車處"), n("nur vorne", "只在前面")],
     [p("Bus / Bahn + 號碼 → 地方", "看路線", "Bus 5 → Flughafen"),
      p("ab: + 時間", "出發時刻", "ab: 9:30")],
     ["站牌先看箭頭方向與時間。"], ["交通"]),
    ("a1-11", "dialogue", "餐廳", "Im Restaurant", "在餐廳",
     "Kellner: Bitte sehr.\nPaul: Die Speisekarte, bitte.\nKellner: Hier.\nPaul: Ich hätte gerne die Suppe.\nKellner: Noch etwas?\nPaul: Nein, danke.",
     "服務生：請（這邊請）。\nPaul：菜單，麻煩。\n服務生：這裡。\nPaul：我想要湯。\n服務生：還要別的嗎？\nPaul：不用，謝謝。",
     [n("Speisekarte", "菜單"), n("Ich hätte gerne …", "我想要……", "禮貌點餐，比 Ich will 客氣。"),
      n("Noch etwas?", "還要別的嗎？"), n("Nein, danke", "不用，謝謝")],
     [p("Ich hätte gerne + 第四格", "禮貌點餐", "Ich hätte gerne einen Salat."),
      p("Noch etwas? — Nein, danke.", "結束點餐", "Noch etwas? — Ja, Wasser.")],
     ["Ich hätte gerne 是 A1 超實用客氣句。"], ["點餐", "客氣"]),
    ("a1-12", "card", "日常", "Mein Tag", "我的一天",
     "Ich stehe um 7 Uhr auf.\nIch frühstücke.\nIch gehe zur Arbeit.\nAm Abend lese ich.\nIch schlafe um 11 Uhr.",
     "我七點起床。\n我吃早餐。\n我去上班。\n晚上我看書。\n我十一點睡覺。",
     [n("stehe … auf", "起床", "aufstehen 可分動詞，字首到句尾。"),
      n("frühstücke", "吃早餐"), n("zur Arbeit", "去上班", "zu der→zur。"),
      n("Am Abend", "在晚上")],
     [p("Ich stehe um … Uhr auf", "說起床時間", "Ich stehe um 6 Uhr auf."),
      p("Am Morgen / Nachmittag / Abend", "時段", "Am Morgen trinke ich Kaffee.")],
     ["可分動詞：現在時字首飛到後面。"], ["可分動詞", "日常"]),
    ("a1-13", "dialogue", "天氣", "Das Wetter", "天氣",
     "Mia: Wie ist das Wetter heute?\nJonas: Es ist sonnig und warm.\nMia: Super! Gehen wir spazieren?\nJonas: Ja, gerne!",
     "Mia：今天天氣怎麼樣？\nJonas：晴朗又溫暖。\nMia：太好了！我們去散步嗎？\nJonas：好啊！",
     [n("Wie ist das Wetter?", "天氣怎麼樣？"),
      n("sonnig", "晴朗的"), n("warm", "溫暖的"),
      n("spazieren gehen", "去散步")],
     [p("Wie ist das Wetter heute?", "問天氣", "Wie ist das Wetter?"),
      p("Es ist + 形容詞", "描述天氣", "Es ist kalt.／Es ist windig.")],
     ["天氣形容詞：kalt、warm、regnerisch、sonnig。"], ["天氣"]),
    ("a1-14", "message", "請假", "Ich bin krank", "我生病了",
     "Hallo Frau Berger,\nich bin heute krank.\nIch komme nicht zur Arbeit.\nViele Grüße\nTom",
     "Berger 女士您好，\n我今天生病了。\n我今天不來上班。\n問候\nTom",
     [n("krank", "生病的"), n("komme nicht", "不來", "nicht 否定動詞。"),
      n("Viele Grüße", "多多問候", "郵件／訊息結尾常見。")],
     [p("Ich bin krank", "說生病", "Ich bin heute krank."),
      p("Ich komme nicht + 地方", "說明不去", "Ich komme nicht zur Schule.")],
     ["簡短請假訊息：原因＋結果即可。"], ["否定", "郵件"]),
    ("a1-15", "sign", "禁止", "Hinweis", "注意告示",
     "Bitte nicht rauchen!\nHandy aus!\nRuhe, bitte.",
     "請勿吸菸！\n手機關機！\n請安靜。",
     [n("Bitte nicht + 動詞", "請不要……", "告示常用不定式。"),
      n("Handy aus", "手機關機", "口語短句。"), n("Ruhe", "安靜")],
     [p("Bitte nicht + 不定式!", "禁止／請求", "Bitte nicht fotografieren!"),
      p("… aus!", "關掉", "Licht aus!")],
     ["告示常省略主語，只留動詞原形。"], ["告示", "否定"]),
    ("a1-16", "dialogue", "問路", "Der Weg", "問路",
     "Tourist: Entschuldigung, wo ist der Bahnhof?\nFrau: Geradeaus, dann links.\nTourist: Ist es weit?\nFrau: Nein, fünf Minuten.\nTourist: Vielen Dank!",
     "觀光客：不好意思，火車站在哪？\n女士：直走，然後左轉。\n觀光客：遠嗎？\n女士：不遠，五分鐘。\n觀光客：非常感謝！",
     [n("Geradeaus", "直走"), n("dann links", "然後左轉"),
      n("Ist es weit?", "遠嗎？"), n("fünf Minuten", "五分鐘"),
      n("Vielen Dank", "非常感謝")],
     [p("Wo ist + der/die/das …?", "問路", "Wo ist die Toilette?"),
      p("Geradeaus, dann links / rechts", "指路", "Geradeaus, dann rechts.")],
     ["問路三件套：Wo ist…?／遠嗎？／謝謝。"], ["方向"]),
    ("a1-17", "card", "喜好", "Was mag ich?", "我喜歡什麼？",
     "Ich mag Pizza.\nIch mag Fußball.\nIch mag meine Freunde.\nIch mag keinen Fisch.\nUnd du?",
     "我喜歡披薩。\n我喜歡足球。\n我喜歡我的朋友。\n我不喜歡魚。\n你呢？",
     [n("Ich mag", "我喜歡", "mögen 的 ich 變位。"),
      n("keinen Fisch", "不喜歡魚", "kein 否定名詞；陽性第四格 keinen。")],
     [p("Ich mag + 名詞", "說喜好", "Ich mag Schokolade."),
      p("Ich mag keinen / keine / kein …", "說不喜歡", "Ich mag keine Milch.")],
     ["喜歡用 mag，不喜歡用 kein，不要說 nicht ein。"], ["mögen", "kein"]),
    ("a1-18", "dialogue", "數字價錢", "Was kostet das?", "多少錢？",
     "Kunde: Was kostet das Brot?\nVerkäufer: Das kostet 2 Euro 50.\nKunde: Okay, ich nehme es.\nVerkäufer: Sonst noch etwas?\nKunde: Nein, das ist alles.",
     "顧客：這麵包多少錢？\n店員：2 歐 50。\n顧客：好，我要這個。\n店員：還要別的嗎？\n顧客：不用，就這些。",
     [n("Was kostet …?", "……多少錢？"), n("ich nehme es", "我要這個／我拿它"),
      n("Sonst noch etwas?", "還要別的嗎？"), n("das ist alles", "就這些")],
     [p("Was kostet + der/die/das …?", "問價錢", "Was kostet die Jacke?"),
      p("Ich nehme …", "決定買", "Ich nehme das hier.")],
     ["付錢場合把兩句問答背起來。"], ["購物", "數字"]),
    ("a1-19", "message", "邀請", "Party", "派對邀請",
     "Hey!\nAm Samstag habe ich eine Party.\nKommst du?\nAb 20 Uhr bei mir.\nBitte antworte bald!\n— Lisa",
     "嘿！\n星期六我有派對。\n你來嗎？\n從 20 點在我家。\n請快回覆！\n— Lisa",
     [n("Am Samstag", "在星期六", "星期用 am。"),
      n("Kommst du?", "你來嗎？"), n("Ab 20 Uhr", "從 20 點起"),
      n("bei mir", "在我家／我這邊"), n("antworte", "回覆（命令式）")],
     [p("Am + 星期", "說星期", "Am Freitag habe ich Zeit."),
      p("Kommst du?", "邀請", "Kommst du mit?")],
     ["回覆：Ja, gerne! 或 Leider nein."], ["時間介系詞", "邀請"]),
    ("a1-20", "card", "住處", "Meine Wohnung", "我的公寓",
     "Ich habe eine Wohnung.\nDie Wohnung ist klein, aber hell.\nEs gibt eine Küche und ein Bad.\nMein Zimmer ist ruhig.",
     "我有一間公寓。\n公寓小但明亮。\n有廚房和浴室。\n我的房間很安靜。",
     [n("Es gibt", "有……", "後面常用第四格。"),
      n("hell", "明亮的"), n("ruhig", "安靜的"),
      n("aber", "但是")],
     [p("Ich habe + 第四格", "說擁有", "Ich habe ein Auto."),
      p("Es gibt + 第四格", "描述存在", "Es gibt einen Balkon.")],
     ["Es gibt 後面：einen／eine／ein。"], ["haben", "Es gibt"]),
]

for t in A1_MORE:
    A1.append(item(t[0], "A1", t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9], t[10]))

A1_BATCH2 = [
    ("a1-21", "dialogue", "學習", "Im Kurs", "在課堂",
     "Lehrerin: Öffnet bitte die Bücher.\nSeite 12.\nStudent: Entschuldigung, was bedeutet „heute“?\nLehrerin: „Heute“ heißt: this day.\nStudent: Ah, danke!",
     "老師：請打開書。\n第 12 頁。\n學生：不好意思，「heute」是什麼意思？\n老師：「Heute」意思是今天。\n學生：啊，謝謝！",
     [n("Öffnet bitte", "請打開（你們）", "對你們用命令式 -t。"),
      n("was bedeutet …?", "……是什麼意思？"), n("heißt", "意思是／名叫")],
     [p("Was bedeutet „…“?", "問單字意思", "Was bedeutet „Arbeit“?"),
      p("… heißt …", "解釋意思", "„Danke“ heißt thank you.")],
     ["課堂救命句：Was bedeutet …?"], ["課堂"]),
    ("a1-22", "sign", "醫院", "Wartezimmer", "候診室",
     "Bitte warten.\nNummer 24 ist dran.\nKeine Handys.",
     "請等候。\n叫到 24 號。\n禁止使用手機。",
     [n("Bitte warten", "請等候"), n("ist dran", "輪到了"),
      n("Keine Handys", "禁止手機")],
     [p("Bitte + 不定式", "告示請求", "Bitte Platz nehmen."),
      p("Nummer … ist dran", "叫號", "Nummer 10 ist dran.")],
     ["公共場合短句，認字即可。"], ["告示"]),
    ("a1-23", "dialogue", "衣服", "Die Jacke", "外套",
     "Verkäuferin: Suchen Sie etwas?\nKunde: Ja, eine Jacke.\nVerkäuferin: Welche Größe?\nKunde: Größe M.\nVerkäuferin: Die ist blau und warm.",
     "店員：在找什麼嗎？\n顧客：對，一件外套。\n店員：什麼尺寸？\n顧客：M。\n店員：這件藍又暖。",
     [n("Suchen Sie etwas?", "您在找什麼嗎？"),
      n("Welche Größe?", "什麼尺寸？"), n("warm", "保暖的／溫暖的")],
     [p("Ich suche + 第四格", "說在找什麼", "Ich suche eine Hose."),
      p("Welche Größe?", "問尺寸", "Welche Größe haben Sie?")],
     ["購物兩句：Ich suche…／Welche Größe?"], ["購物"]),
    ("a1-24", "message", "延遲", "Ich komme später", "我晚點到",
     "Hi!\nDer Bus hat Verspätung.\nIch komme 10 Minuten später.\nSorry!\n— Anna",
     "嗨！\n公車誤點。\n我晚十分鐘到。\n抱歉！\n— Anna",
     [n("hat Verspätung", "誤點／延遲"), n("später", "較晚"),
      n("Minuten", "分鐘（複數）")],
     [p("Ich komme … später", "說遲到", "Ich komme etwas später."),
      p("Der Zug / Bus hat Verspätung", "說誤點", "Der Zug hat Verspätung.")],
     ["真實生活超常用，整段可背。"], ["交通", "道歉"]),
    ("a1-25", "card", "職業", "Beruf", "職業",
     "Ich bin Lehrer.\nMeine Frau ist Ärztin.\nMein Bruder ist Student.\nWir arbeiten viel.\nAber wir sind glücklich.",
     "我是老師。\n我太太是醫生。\n我弟弟是學生。\n我們工作很多。\n但我們很幸福。",
     [n("Lehrer / Ärztin / Student", "職業名詞", "女性常加 -in：Lehrerin。"),
      n("arbeiten", "工作"), n("glücklich", "幸福的")],
     [p("Ich bin + 職業", "說職業", "Ich bin Koch."),
      p("Wir sind + 形容詞", "說狀態", "Wir sind müde.")],
     ["職業不加冠詞：Ich bin Lehrer（不是 ein Lehrer，也可說）。A1 兩種都會聽到。"],
     ["sein", "職業"]),
    ("a1-26", "dialogue", "電話", "Am Telefon", "打電話",
     "A: Hallo, hier ist Mark.\nB: Hallo Mark! Ist Anna da?\nA: Moment, bitte.\nA: Anna, Telefon für dich!\nAnna: Ja, ich komme.",
     "A：哈囉，我是 Mark。\nB：哈囉 Mark！Anna 在嗎？\nA：請稍等。\nA：Anna，你的電話！\nAnna：好，我來了。",
     [n("hier ist …", "我是……（電話）"), n("Ist … da?", "……在嗎？"),
      n("Moment, bitte", "請稍等"), n("für dich", "給你的")],
     [p("Hallo, hier ist + 名字", "電話自我介紹", "Hier ist Lisa."),
      p("Ist + 名字 + da?", "找人", "Ist Herr Lang da?")],
     ["電話開場固定句，先背。"], ["電話"]),
    ("a1-27", "sign", "圖書館", "Bibliothek", "圖書館",
     "Öffnungszeiten: 9–20 Uhr\nBitte leise sprechen.\nEssen und Trinken: nein.",
     "開放時間：9–20 點\n請小聲說話。\n禁止飲食。",
     [n("leise sprechen", "小聲說話"), n("Essen und Trinken", "飲食"),
      n("nein", "不行／禁止（告示）")],
     [p("Bitte leise + 動詞", "請安靜做某事", "Bitte leise gehen."),
      p("…: nein / verboten", "禁止", "Fotografieren: nein.")],
     ["公共守則短句夠用。"], ["告示"]),
    ("a1-28", "card", "週末", "Am Wochenende", "週末",
     "Am Samstag kaufe ich ein.\nAm Sonntag besuche ich meine Eltern.\nWir essen zusammen.\nDas ist schön.",
     "星期六我去採買。\n星期天我探望父母。\n我們一起吃飯。\n這很好。",
     [n("kaufe … ein", "採買", "einkaufen 可分。"),
      n("besuche", "拜訪"), n("zusammen", "一起"), n("schön", "美好的")],
     [p("Am Samstag / Sonntag + 句子", "說週末計畫", "Am Samstag schlafe ich länger."),
      p("Das ist schön / toll / super", "評價", "Das ist toll!")],
     ["用兩個日子各寫一句你的週末。"], ["週末", "可分動詞"]),
    ("a1-29", "dialogue", "幫忙", "Hilfe", "幫忙",
     "Kind: Kannst du mir helfen?\nVater: Natürlich. Was ist los?\nKind: Ich finde meinen Stift nicht.\nVater: Hier, unter dem Buch.",
     "孩子：你可以幫我嗎？\n爸爸：當然。怎麼了？\n孩子：我找不到我的筆。\n爸爸：在這裡，在書下面。",
     [n("Kannst du mir helfen?", "你可以幫我嗎？", "helfen + 第三格。"),
      n("Was ist los?", "怎麼了？"), n("finde … nicht", "找不到"),
      n("unter dem Buch", "在書下面", "unter + 第三格（靜態）。")],
     [p("Kannst du mir helfen?", "求助", "Kannst du mir bitte helfen?"),
      n("Was ist los?", "怎麼了？") if False else p("Was ist los?", "詢問狀況", "Was ist los?")],
     ["helfen 要記：mir／dir／ihm。"], ["Dativ", "求助"]),
    ("a1-30", "message", "感謝", "Danke", "道謝",
     "Liebe Anna,\ndanke für deine Hilfe!\nDu bist sehr nett.\nBis bald\nPaul",
     "親愛的 Anna，\n謝謝你的幫忙！\n你人很好。\n待會見\nPaul",
     [n("danke für", "為……謝謝", "für + 第四格。"),
      n("nett", "好／親切的"), n("Bis bald", "待會見")],
     [p("Danke für + 第四格", "道謝", "Danke für den Kaffee."),
      p("Du bist sehr + 形容詞", "稱讚", "Du bist sehr freundlich.")],
     ["短訊息也能很有禮貌。"], ["道謝"]),
]

for t in A1_BATCH2:
    notes = t[7]
    patterns = t[8]
    # fix accidental bad pattern in a1-29 if any
    A1.append(item(t[0], "A1", t[1], t[2], t[3], t[4], t[5], t[6], notes, patterns, t[9], t[10]))

# Continue A1 to 50 with compact generator for remaining slots
A1_EXTRA = [
    ("a1-31", "dialogue", "顏色", "Welche Farbe?", "什麼顏色？",
     "A: Welche Farbe möchtest du?\nB: Rot, bitte.\nA: Hier ist ein roter Stift.\nB: Perfekt, danke!",
     "A：你想要什麼顏色？\nB：紅色，麻煩。\nA：這是一支紅色的筆。\nB：完美，謝謝！",
     [n("Welche Farbe?", "什麼顏色？"), n("roter Stift", "紅色的筆", "陽性主格形容詞 -er。")],
     [p("Welche Farbe möchtest du?", "問顏色喜好", "Welche Farbe magst du?"),
      p("Hier ist + 名詞", "遞東西", "Hier ist dein Buch.")],
     ["顏色：rot、blau、grün、gelb、schwarz、weiß。"], ["顏色"]),
    ("a1-32", "card", "食物", "Frühstück", "早餐",
     "Zum Frühstück esse ich Brot.\nIch trinke Kaffee.\nManchmal esse ich Obst.\nDas schmeckt gut.",
     "早餐我吃麵包。\n我喝咖啡。\n有時我吃水果。\n很好吃。",
     [n("Zum Frühstück", "作為早餐"), n("Manchmal", "有時候"), n("schmeckt gut", "好吃／味道好")],
     [p("Zum Frühstück / Mittagessen esse ich …", "說餐點", "Zum Abendessen esse ich Reis."),
      p("Das schmeckt gut", "說好吃", "Mmm, das schmeckt gut!")],
     ["essen／trinken 是飲食基本動詞。"], ["飲食"]),
    ("a1-33", "sign", "電梯", "Aufzug", "電梯",
     "Aufzug\nMax. 6 Personen\nBei Feuer: Treppe benutzen!",
     "電梯\n最多 6 人\n火災時：請走樓梯！",
     [n("Max.", "最多", "Maximum。"), n("Personen", "人（複數）"),
      n("Bei Feuer", "發生火災時"), n("Treppe benutzen", "使用樓梯")],
     [p("Bei + 情況: + 指令", "緊急指示", "Bei Gefahr: Ausgang!"),
      p("… benutzen", "使用", "Bitte den Eingang benutzen.")],
     ["公共標示常混德英縮寫。"], ["告示"]),
    ("a1-34", "dialogue", "名字", "Wie heißt du?", "你叫什麼？",
     "A: Hallo, wie heißt du?\nB: Ich heiße Sara. Und du?\nA: Ich heiße Ben.\nB: Freut mich!\nA: Mich auch!",
     "A：哈囉，你叫什麼名字？\nB：我叫 Sara。你呢？\nA：我叫 Ben。\nB：很高興認識你！\nA：我也是！",
     [n("Wie heißt du?", "你叫什麼？"), n("Ich heiße", "我叫"),
      n("Freut mich!", "很高興（認識你）")],
     [p("Wie heißt du? — Ich heiße …", "問名字", "Wie heißt er? — Er heißt Tom."),
      p("Freut mich!", "初次見面", "Freut mich, Sie kennenzulernen!")],
     ["A1 第一週就會用到。"], ["heißen"]),
    ("a1-35", "message", "確認", "Alles klar?", "清楚嗎？",
     "Paul: Treffpunkt ist um 4 am Tor.\nAlles klar?\nMia: Ja, alles klar.\nIch bin pünktlich.",
     "Paul：集合點是四點在大門。\n清楚嗎？\nMia：嗯，清楚。\n我會準時。",
     [n("Treffpunkt", "集合點"), n("Alles klar?", "清楚嗎／沒問題吧？"),
      n("pünktlich", "準時的")],
     [p("Alles klar?", "確認理解", "Alles klar so?"),
      p("Ich bin pünktlich", "保證準時", "Sei bitte pünktlich!")],
     ["口語確認：Alles klar?／Okay?"], ["約定"]),
    ("a1-36", "card", "國家語言", "Sprachen", "語言",
     "Ich spreche Chinesisch.\nIch spreche ein bisschen Englisch.\nIch lerne Deutsch.\nDeutsch ist interessant, aber schwer.",
     "我說中文。\n我說一點英文。\n我在學德文。\n德文有趣但難。",
     [n("spreche", "說（語言）"), n("ein bisschen", "一點點"),
      n("interessant", "有趣的"), n("schwer", "難的／重的")],
     [p("Ich spreche + 語言", "說會的語言", "Ich spreche Deutsch."),
      p("… ist interessant, aber schwer", "評價", "Mathe ist wichtig, aber schwer.")],
     ["語言名稱多半大寫：Deutsch、Englisch。"], ["語言"]),
    ("a1-37", "dialogue", "酒店", "Im Hotel", "在飯店",
     "Rezeption: Guten Tag! Haben Sie eine Reservierung?\nGast: Ja, auf den Namen Li.\nRezeption: Zimmer 12. Hier ist der Schlüssel.\nGast: Danke!",
     "櫃台：您好！您有預約嗎？\n客人：有，名字是 Li。\n櫃台：12 號房。這是鑰匙。\n客人：謝謝！",
     [n("Reservierung", "預約"), n("auf den Namen …", "以……的名字"),
      n("Schlüssel", "鑰匙（der）")],
     [p("Haben Sie eine Reservierung?", "問是否預約", "Ich habe eine Reservierung."),
      p("auf den Namen + 名字", "報名", "Auf den Namen Wang, bitte.")],
     ["旅行第一句很實用。"], ["旅行"]),
    ("a1-38", "sign", "廁所", "Toilette", "廁所標示",
     "Toilette\nDamen | Herren\nBitte sauber lassen!",
     "廁所\n女｜男\n請保持清潔！",
     [n("Damen", "女廁／女士"), n("Herren", "男廁／男士"),
      n("sauber lassen", "保持乾淨")],
     [p("Bitte … lassen", "請讓……保持", "Bitte die Tür zu lassen."),
      p("Damen / Herren", "性別標示", "Damen — rechts")],
     ["認得即可，出國超常用。"], ["告示"]),
    ("a1-39", "dialogue", "感覺", "Wie fühlst du dich?", "你感覺如何？",
     "A: Wie fühlst du dich?\nB: Ich bin müde.\nA: Warum?\nB: Ich habe schlecht geschlafen.\nA: Oh, dann ruh dich aus!",
     "A：你感覺如何？\nB：我好累。\nA：為什麼？\nB：我睡得不好。\nA：噢，那休息一下！",
     [n("müde", "累的"), n("Warum?", "為什麼？"),
      n("schlecht geschlafen", "睡得不好", "A1 可先當整塊記。"),
      n("ruh dich aus", "休息一下", "sich ausruhen 可分命令式。")],
     [p("Ich bin müde / hungrig / durstig", "說身體感覺", "Ich bin hungrig."),
      p("Warum? — Weil … / 簡單句", "問原因", "Warum? — Ich arbeite viel.")],
     ["感覺形容詞超實用。"], ["形容詞"]),
    ("a1-40", "card", "計劃", "Heute Nachmittag", "今天下午",
     "Heute Nachmittag habe ich Zeit.\nIch möchte Sport machen.\nDann koche ich.\nAm Abend sehe ich fern.",
     "今天下午我有空。\n我想運動。\n然後我煮飯。\n晚上我看電視。",
     [n("möchte", "想要", "möchten 客氣形式。"),
      n("Sport machen", "做運動"), n("sehe … fern", "看電視", "fernsehen 可分。")],
     [p("Ich möchte + 動詞原形", "說想做", "Ich möchte schlafen."),
      p("Dann … / Am Abend …", "排列活動", "Dann lerne ich.")],
     ["möchte 後面用原形：möchte gehen。"], ["情態", "計劃"]),
    ("a1-41", "message", "提醒", "Nicht vergessen", "別忘了",
     "Mama: Nicht vergessen!\nMilch und Brot kaufen.\nSchlüssel mitnehmen.\nIch liebe dich!",
     "媽媽：別忘了！\n買牛奶和麵包。\n帶鑰匙。\n我愛你！",
     [n("Nicht vergessen", "別忘記"), n("mitnehmen", "帶走", "可分。"),
      n("Ich liebe dich", "我愛你")],
     [p("Nicht vergessen: + 不定式", "提醒清單", "Nicht vergessen: anrufen!"),
      p("… mitnehmen / mitbringen", "帶去／帶來", "Bring bitte Kuchen mit!")],
     ["清單式訊息常用原形動詞。"], ["提醒"]),
    ("a1-42", "dialogue", "年齡", "Wie alt bist du?", "你幾歲？",
     "A: Wie alt bist du?\nB: Ich bin 20 Jahre alt.\nA: Wirklich? Du siehst jung aus!\nB: Danke!",
     "A：你幾歲？\nB：我 20 歲。\nA：真的嗎？你看起來好年輕！\nB：謝謝！",
     [n("Wie alt bist du?", "你幾歲？"), n("Jahre alt", "……歲"),
      n("siehst … aus", "看起來", "aussehen 可分。"), n("jung", "年輕的")],
     [p("Ich bin … Jahre alt", "說年齡", "Ich bin 18 Jahre alt."),
      p("Du siehst … aus", "評價外表", "Du siehst müde aus.")],
     ["年齡句型固定，整句背。"], ["數字", "aussehen"]),
    ("a1-43", "sign", "停車場", "Parkplatz", "停車場",
     "Parkplatz\nKosten: 2 € / Stunde\nNur für Kunden\nFrei: 3 Plätze",
     "停車場\n費用：每小時 2 歐\n僅供顧客\n空位：3 個",
     [n("Kosten", "費用"), n("Stunde", "小時"), n("Nur für Kunden", "僅供顧客"),
      n("Frei", "空的／有位子")],
     [p("… € / Stunde", "按小時計價", "1,50 € / Stunde"),
      p("Nur für + 複數／族群", "限制使用", "Nur für Personal")],
     ["看標示抓關鍵數字即可。"], ["告示"]),
    ("a1-44", "dialogue", "座位", "Ist hier frei?", "這裡有人嗎？",
     "A: Entschuldigung, ist hier frei?\nB: Ja, bitte!\nA: Danke. Ist das Ihr Platz?\nB: Nein, alles gut.",
     "A：不好意思，這裡有空嗎？\nB：有，請坐！\nA：謝謝。這是您的位子嗎？\nB：不是，沒關係。",
     [n("Ist hier frei?", "這裡空著嗎？"), n("Ihr Platz", "您的位子", "Ihr＝您的。"),
      n("alles gut", "沒問題／沒事")],
     [p("Ist hier frei?", "問座位", "Ist dieser Platz frei?"),
      p("Ist das Ihr / dein …?", "確認所屬", "Ist das Ihre Tasche?")],
     ["公共交通超常用。"], ["禮貌"]),
    ("a1-45", "card", "季節", "Die Jahreszeiten", "季節",
     "Im Frühling ist es warm.\nIm Sommer schwimme ich.\nIm Herbst fallen die Blätter.\nIm Winter schneit es oft.",
     "春天天氣暖。\n夏天我游泳。\n秋天葉子落下。\n冬天常常下雪。",
     [n("Im Frühling / Sommer / Herbst / Winter", "在……季", "in dem→im。"),
      n("fallen", "落下"), n("schneit", "下雪", "es schneit。")],
     [p("Im + 季節 + 句子", "談季節", "Im Sommer ist es heiß."),
      p("Es schneit / regnet", "天氣動詞", "Es regnet heute.")],
     ["四季介系詞幾乎都用 im。"], ["季節", "天氣"]),
    ("a1-46", "message", "分享照片", "Foto", "照片",
     "Schau!\nDas ist mein Hund.\nEr heißt Milo.\nEr ist klein und süß.\n❤️",
     "你看！\n這是我的狗。\n他叫 Milo。\n他又小又可愛。\n❤️",
     [n("Schau!", "你看！", "對 du 的命令式。"),
      n("Hund", "狗（der）"), n("süß", "可愛／甜的")],
     [p("Das ist mein / meine …", "分享照片", "Das ist meine Katze."),
      p("Er / Sie ist + 形容詞", "描述", "Sie ist groß und schnell.")],
     ["社群訊息風格，短句即可。"], ["所有格"]),
    ("a1-47", "dialogue", "重複", "Noch einmal", "再說一次",
     "Student: Wie bitte?\nLehrerin: Das Wort ist „Fenster“.\nStudent: Können Sie das bitte wiederholen?\nLehrerin: Fen-ster.\nStudent: Fenster. Okay!",
     "學生：請問您說什麼？\n老師：這個詞是「Fenster」。\n學生：可以請您再說一次嗎？\n老師：Fen-ster。\n學生：Fenster。好！",
     [n("Wie bitte?", "請問你說什麼？", "沒聽清時用。"),
      n("wiederholen", "重複"), n("Können Sie …?", "您可以……嗎？")],
     [p("Wie bitte?", "請對方再說", "Wie bitte? Ich verstehe nicht."),
      p("Können Sie das bitte wiederholen?", "請重複", "Bitte langsam wiederholen!")],
     ["聽不懂三寶：Wie bitte?／wiederholen／langsam。"], ["課堂", "禮貌"]),
    ("a1-48", "sign", "垃圾", "Müll", "垃圾分類",
     "Mülltrennung\nPapier → blau\nGlas → grün\nRestmüll → schwarz",
     "垃圾分類\n紙 → 藍\n玻璃 → 綠\n一般垃圾 → 黑",
     [n("Mülltrennung", "垃圾分類"), n("Papier", "紙"), n("Glas", "玻璃"),
      n("Restmüll", "一般／剩餘垃圾")],
     [p("… → 顏色／桶", "分類指示", "Bio → braun"),
      p("Bitte trennen!", "請分類", "Bitte Müll trennen!")],
     ["德國生活必看標示。"], ["生活"]),
    ("a1-49", "dialogue", "告別", "Tschüss", "再見",
     "A: Ich muss gehen.\nB: Schon?\nA: Ja, es ist spät.\nB: Okay. Tschüss!\nA: Tschüss, bis morgen!",
     "A：我得走了。\nB：這麼快？\nA：對，很晚了。\nB：好。掰！\nA：掰，明天見！",
     [n("Ich muss gehen", "我必須走了"), n("Schon?", "這麼快／已經？"),
      n("spät", "晚的"), n("Tschüss", "掰／再見（口語）")],
     [p("Ich muss gehen", "告辭", "Sorry, ich muss gehen."),
      p("Tschüss! / Bis morgen!", "道別", "Bis bald!")],
     ["正式場合多用 Auf Wiedersehen。"], ["道別"]),
    ("a1-50", "card", "複習短文", "Das bin ich", "這就是我",
     "Mein Name ist Alex.\nIch bin 22.\nIch komme aus München.\nIch studiere Medizin.\nIch mag Sport und Musik.\nFreut mich!",
     "我的名字是 Alex。\n我 22 歲。\n我來自慕尼黑。\n我唸醫學。\n我喜歡運動和音樂。\n很高興認識你！",
     [n("Mein Name ist", "我的名字是", "比 Ich heiße 稍正式。"),
      n("studiere", "就讀（大學）"), n("Medizin", "醫學")],
     [p("Mein Name ist …", "正式自介", "Mein Name ist Frau Koch."),
      p("Ich studiere + 科系", "說大學科系", "Ich studiere Informatik.")],
     ["把這六句改成你的版本，就是完整自介。"], ["自我介紹", "複習"]),
]

for t in A1_EXTRA:
    A1.append(item(t[0], "A1", t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9], t[10]))

assert len(A1) == 50, len(A1)

# ── A2: longer paragraphs, emails, notices ─────────────────────────
A2: list[dict] = []

A2_DATA = [
    ("a2-01", "email", "工作", "Krankmeldung", "請假信",
     """Betreff: Krankmeldung

Liebe Frau Schulz,

leider bin ich heute krank und kann nicht zur Arbeit kommen.
Ich habe Fieber und bleibe zu Hause.
Morgen gehe ich zum Arzt.

Viele Grüße
Markus Weber""",
     """主旨：病假通知

親愛的 Schulz 女士：

很抱歉，我今天生病了，無法來上班。
我發燒，留在家裡。
明天我會去看醫生。

問候
Markus Weber""",
     [n("Betreff", "主旨"), n("leider", "遺憾地／很抱歉"),
      n("kann nicht … kommen", "無法來", "情態動詞 + 原形。"),
      n("Fieber haben", "發燒"), n("zum Arzt", "去看醫生", "zu dem→zum。")],
     [p("leider + 句子", "委婉說明壞消息", "Leider habe ich keine Zeit."),
      p("Ich kann nicht + 原形", "說不能做", "Ich kann nicht kommen."),
      p("Viele Grüße / Mit freundlichen Grüßen", "信件結尾", "Viele Grüße")],
     ["A2 郵件：主旨＋稱呼＋原因＋計畫＋結尾。", "比 A1 多了完整段落與連貫。"],
     ["郵件", "情態動詞", " entlich"]),
    ("a2-02", "story", "日常", "Ein normaler Montag", "普通的星期一",
     """Am Montag stehe ich um halb sieben auf.
Nach dem Frühstück fahre ich mit dem Bus zur Schule.
Der Unterricht beginnt um acht.
Nach der Schule treffe ich meine Freundin im Café.
Wir trinken etwas und sprechen über die Hausaufgaben.
Abends bin ich müde, aber zufrieden.""",
     """星期一我六點半起床。
早餐後我搭公車去學校。
課程八點開始。
放學後我跟朋友在咖啡廳碰面。
我們喝點東西，討論作業。
晚上我很累，但很滿足。""",
     [n("um halb sieben", "六點半", "halb sieben＝6:30。"),
      n("Nach dem Frühstück", "早餐之後", "nach + 第三格。"),
      n("fahre … mit dem Bus", "搭公車"), n("beginnt", "開始"),
      n("sprechen über", "談論……", "über + 第四格。"),
      n("zufrieden", "滿足的")],
     [p("Nach + 第三格 …", "在……之後", "Nach dem Essen gehe ich spazieren."),
      p("mit dem Bus / der Bahn fahren", "搭交通工具", "Ich fahre mit der Bahn."),
      p("sprechen über + 第四格", "談論主題", "Wir sprechen über den Film.")],
     ["注意時間表達 halb。", "練習把學校改成 Arbeit。"],
     ["時間", "介系詞", "日常"]),
    ("a2-03", "notice", "公寓", "Wohnungsanzeige", "租屋廣告",
     """Helle 2-Zimmer-Wohnung in der Stadtmitte
65 m², Balkon, Einbauküche
Miete: 850 € + 150 € Nebenkosten
Frei ab 1. Mai
Nicht rauchen. Keine großen Haustiere.
Kontakt: wohnen@beispiel.de""",
     """市中心明亮兩房公寓
65 平方、陽台、系統廚具
租金：850 歐 + 150 歐雜費
5 月 1 日起可入住
禁菸。不可養大型寵物。
聯絡：wohnen@beispiel.de""",
     [n("2-Zimmer-Wohnung", "兩房公寓"), n("Stadtmitte", "市中心"),
      n("Miete", "租金"), n("Nebenkosten", "雜費（水電管理等）"),
      n("Frei ab", "從……起可入住"), n("Haustiere", "寵物")],
     [p("Frei ab + 日期", "可入住日期", "Frei ab sofort"),
      p("Miete: … € + … € Nebenkosten", "租金結構", "Kaltmiete / Warmmiete"),
      p("Keine + 複數", "禁止條款", "Keine Partys")],
     ["看房租要分清 Miete 與 Nebenkosten。"], ["生活", "廣告"]),
    ("a2-04", "dialogue", "旅行", "Fahrkarten", "買票",
     """Mitarbeiter: Wohin möchten Sie fahren?
Reisende: Nach Hamburg, bitte. Einmal hin und zurück.
Mitarbeiter: Wann fahren Sie?
Reisende: Heute Nachmittag, und am Sonntag zurück.
Mitarbeiter: Mit dem ICE kostet das 79 Euro.
Reisende: Gut, ich nehme das Ticket.""",
     """職員：您要去哪裡？
旅客：去漢堡，麻煩。來回票。
職員：您什麼時候走？
旅客：今天下午去，星期天回。
職員：搭 ICE 要 79 歐。
旅客：好，我買這張票。""",
     [n("Wohin …?", "去哪裡？", "問方向用 wohin。"),
      n("hin und zurück", "來回"), n("Wann?", "什麼時候？"),
      n("ICE", "德國高鐵車種"), n("Ticket", "票")],
     [p("Wohin möchten Sie fahren?", "問目的地", "Wohin gehst du?"),
      p("Einmal hin und zurück", "買來回票", "Nur hin, bitte."),
      p("Ich nehme das Ticket", "決定購買", "Ich nehme die Karte.")],
     ["Wo?＝在哪；Wohin?＝去哪。A2 要分清。"], ["旅行", "疑問副詞"]),
    ("a2-05", "email", "邀請", "Einladung zum Abendessen", "晚餐邀請",
     """Hallo Julia,

hast du am Freitag Abend Zeit?
Ich koche Pasta und salat.
Kommst du um 19 Uhr zu mir?
Bring gerne etwas zu trinken mit.

Liebe Grüße
Sam""",
     """嗨 Julia，

你星期五晚上有空嗎？
我煮義大利麵和沙拉。
你十九點來我家嗎？
可以的話帶點喝的。

問候
Sam""",
     [n("hast du … Zeit?", "你有空嗎？"), n("koche", "煮"),
      n("Bring … mit", "帶來", "mitbringen 命令式。"),
      n("etwas zu trinken", "一些喝的")],
     [p("Hast du am … Zeit?", "約時間", "Hast du am Wochenende Zeit?"),
      p("Kommst du … zu mir?", "邀來家裡", "Kommst du heute zu mir?"),
      p("Bring bitte … mit", "請帶來", "Bring einen Kuchen mit!")],
     ["邀請信比 A1 簡訊多了細節與請求。"], ["邀請", "可分動詞"]),
]

for t in A2_DATA:
    A2.append(item(t[0], "A2", t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9], t[10]))

# Generate remaining A2 to reach 50 with varied templates
A2_MORE = [
    ("a2-06", "story", "購物", "Im Einkaufszentrum", "在購物中心",
     """Gestern war ich im Einkaufszentrum.
Zuerst habe ich eine Jeans anprobiert.
Sie hat mir gut gepasst und war nicht teuer.
Danach habe ich noch ein T-Shirt gekauft.
Zum Schluss habe ich einen Kaffee getrunken.
Es war ein erfolgreicher Nachmittag.""",
     """昨天我去了購物中心。
先試穿了一條牛仔褲。
很合身而且不貴。
之後又買了一件 T 恤。
最後喝了杯咖啡。
那是個成功的下午。""",
     [n("Zuerst / Danach / Zum Schluss", "首先／然後／最後", "順序連接詞。"),
      n("anprobiert", "試穿（完成式）", "A2 開始常見完成式。"),
      n("gepasst", "合身"), n("erfolgreich", "成功的")],
     [p("Zuerst … Danach … Zum Schluss …", "敘述順序", "Zuerst lerne ich, danach spiele ich."),
      p("Perfekt: haben/sein + Partizip", "說過去經歷", "Ich habe gekauft.")],
     ["A2 短文常用完成式說『昨天做了什麼』。"], ["完成式", "順序"]),
    ("a2-07", "notice", "學校", "Aushang in der Schule", "學校公告",
     """Wichtige Information
Am Donnerstag entfällt der Sportunterricht.
Stattdessen gibt es eine Doppelstunde Mathe.
Bitte bringt eure Bücher mit.
Fragen an: herr.beck@schule.de""",
     """重要通知
星期四體育課停上。
改上兩堂數學。
請帶課本。
問題請寄：herr.lee@schule.de""",
     [n("entfällt", "取消／停課"), n("Stattdessen", "取而代之"),
      n("Doppelstunde", "連堂／兩堂"), n("bringt … mit", "帶來（你們）")],
     [p("… entfällt", "宣布取消", "Der Kurs entfällt heute."),
      p("Stattdessen + 句子", "改為……", "Stattdessen bleiben wir hier."),
      p("Bitte bringt … mit", "對群體的請求", "Bitte bringt Geld mit.")],
     ["公告語氣直接，動詞常命令式。"], ["學校", "公告"]),
    ("a2-08", "email", "客訴", "Problem mit der Bestellung", "訂單問題",
     """Guten Tag,

ich habe vor drei Tagen ein Buch bestellt.
Leider ist es noch nicht angekommen.
Können Sie bitte nachschauen?
Meine Bestellnummer ist 45821.

Mit freundlichen Grüßen
Lina Chen""",
     """您好，

我三天前訂了一本書。
遺憾的是還沒送到。
可以請您查一下嗎？
我的訂單編號是 45821。

此致問候
Lina Chen""",
     [n("bestellt", "訂購（完成式）"), n("angekommen", "抵達", "ankommen 完成式用 sein。"),
      n("nachschauen", "查看"), n("Bestellnummer", "訂單編號"),
      n("Mit freundlichen Grüßen", "正式信件結尾")],
     [p("Ich habe … bestellt", "說明已訂購", "Ich habe gestern bestellt."),
      p("Können Sie bitte …?", "禮貌請求", "Können Sie mir helfen?"),
      p("Mit freundlichen Grüßen", "正式結尾", "Mit freundlichen Grüßen")],
     ["正式信比 Viele Grüße 更客氣。"], ["郵件", "完成式"]),
    ("a2-09", "story", "天氣計劃", "Bei schlechtem Wetter", "壞天氣",
     """Heute regnet es den ganzen Tag.
Deshalb bleiben wir zu Hause.
Wir kochen zusammen und sehen einen Film.
Wenn es morgen besser wird, gehen wir spazieren.
Ich hoffe auf Sonne!""",
     """今天下了一整天的雨。
所以我們留在家。
我們一起煮飯、看電影。
如果明天好轉，我們就去散步。
我希望出太陽！""",
     [n("den ganzen Tag", "一整天"), n("Deshalb", "所以"),
      n("Wenn …, …", "如果……，就……", "A2 條件句入門。"),
      n("hoffe auf", "期待／希望有……")],
     [p("Deshalb + 句子", "說明結果", "Ich bin müde. Deshalb gehe ich früh schlafen."),
      p("Wenn + 現在式, + 現在式", "簡單條件", "Wenn es regnet, bleibe ich hier.")],
     ["Wenn 子句動詞在句尾（更完整規則後面再細學）。此處先看懂意思。"],
     ["連接詞", "條件"]),
    ("a2-10", "dialogue", "醫生", "Beim Arzt", "看醫生",
     """Arzt: Was fehlt Ihnen?
Patientin: Ich habe Halsschmerzen und Husten.
Arzt: Seit wann?
Patientin: Seit zwei Tagen.
Arzt: Dann verschreibe ich Ihnen etwas.
Bitte trinken Sie viel Tee und ruhen Sie sich aus.""",
     """醫生：您哪裡不舒服？
病人：我喉嚨痛而且咳嗽。
醫生：從什麼時候開始？
病人：兩天了。
醫生：那我幫您開一點藥。
請多喝茶，並好好休息。""",
     [n("Was fehlt Ihnen?", "您哪裡不適？", "fehlen + 第三格。"),
      n("Halsschmerzen", "喉嚨痛"), n("Seit wann?", "從何時起？"),
      n("verschreibe", "開處方"), n("ruhen Sie sich aus", "請休息")],
     [p("Was fehlt Ihnen? / Was tut weh?", "問症狀", "Mir ist schlecht."),
      p("Seit + 時間", "持續多久", "Seit gestern."),
      p("Ruhen Sie sich aus", "醫囑休息", "Bleiben Sie im Bett.")],
     ["看診對話：症狀＋時間＋醫囑。"], ["健康", "Dativ"]),
]

for t in A2_MORE:
    A2.append(item(t[0], "A2", t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9], t[10]))

# Programmatically expand A2 to 50 with structured variants
A2_TEMPLATES = [
    ("a2-11", "story", "朋友", "Ein Besuch", "探訪朋友",
     """Am Samstag habe ich meinen Freund Tim besucht.
Er wohnt nicht weit von mir.
Wir haben Karten gespielt und Pizza bestellt.
Später sind wir noch kurz spazieren gegangen.
Es war entspannt und lustig.
Nächstes Wochenende kommt er zu mir.""",
     """星期六我去探望朋友 Tim。
他住得離我不遠。
我們玩牌，還點了披薩。
之後又出去稍微走走。
很輕鬆很好玩。
下週末他來我家。""",
     [n("besucht", "探望"), n("nicht weit von", "離……不遠"),
      n("bestellt", "點餐／訂購"), n("entspannt", "輕鬆的"),
      n("Nächstes Wochenende", "下週末")],
     [p("Ich habe + 人 + besucht", "說探訪", "Ich habe meine Oma besucht."),
      p("Nächstes Wochenende / Nächste Woche", "未來計劃", "Nächste Woche lerne ich mehr.")],
     ["完成式敘事＋一句未來計劃。"], ["社交", "完成式"]),
    ("a2-12", "email", "學校", "Frage zur Hausaufgabe", "作業相關詢問",
     """Hallo Herr Braun,

ich war gestern krank und habe die Hausaufgabe nicht verstanden.
Könnten Sie mir bitte kurz erklären, was wir machen sollen?
Ich schicke die Arbeit dann bis Montag.

Danke und viele Grüße
Sofia""",
     """Braun 老師您好，

我昨天生病了，作業沒看懂。
可以請您簡短說明我們該做什麼嗎？
我會在星期一前交。

謝謝，問候
Sofia""",
     [n("Könnten Sie …?", "您可不可以……？", "比 Können Sie 更客氣。"),
      n("erklären", "解釋"), n("schicke", "寄送"), n("bis Montag", "在星期一前")],
     [p("Könnten Sie bitte …?", "超客氣請求", "Könnten Sie mir helfen?"),
      p("bis + 時間", "截止", "bis Freitag")],
     ["寫給老師：客氣＋說明原因＋你的計畫。"], ["郵件", "客氣"]),
    ("a2-13", "notice", "活動", "Flohmarkt", "跳蚤市場",
     """Flohmarkt im Stadtpark
Sonntag, 10–16 Uhr
Verkauf von Kleidung, Büchern und Spielsachen
Tische: 10 € pro Tag
Bei Regen findet der Markt trotzdem statt.
Alle sind willkommen!""",
     """市政公園跳蚤市場
星期天 10–16 點
販售衣物、書籍與玩具
攤位桌：每天 10 歐
下雨照常舉行。
歡迎大家！""",
     [n("Flohmarkt", "跳蚤市場"), n("pro Tag", "每天"),
      n("findet … statt", "舉行", "stattfinden 可分。"),
      n("trotzdem", "儘管如此"), n("willkommen", "受歡迎的")],
     [p("findet … statt", "活動舉行", "Das Konzert findet um 8 Uhr statt."),
      p("Bei Regen / Schnee …", "天氣條件", "Bei Regen bleiben wir innen."),
      p("Alle sind willkommen", "歡迎參加", "Jeder ist willkommen.")],
     ["看活動海報抓：時間、地點、費用、雨天是否取消。"], ["活動"]),
    ("a2-14", "story", "交通", "Verspätung", "誤點",
     """Heute Morgen hatte mein Zug zehn Minuten Verspätung.
Deshalb bin ich zu spät zum Meeting gekommen.
Ich habe dem Chef eine kurze Nachricht geschrieben.
Glücklicherweise hat er verstanden.
Nächstes Mal fahre ich früher los.""",
     """今天早上我的火車誤點十分鐘。
所以我開會遲到了。
我傳了簡訊給主管。
幸好他表示理解。
下次我會早點出發。""",
     [n("zu spät kommen", "遲到"), n("Glücklicherweise", "幸好"),
      n("verstanden", "理解（完成式）"), n("früher losfahren", "早點出發")],
     [p("Deshalb bin ich zu spät gekommen", "說明遲到", "Deshalb konnte ich nicht kommen."),
      p("Nächstes Mal + 句子", "下次改進", "Nächstes Mal bin ich pünktlich.")],
     ["問題→原因→處理→改進，是 A2 敘事好架構。"], ["交通", "連接詞"]),
    ("a2-15", "dialogue", "住房", "Nebenkosten", "雜費說明",
     """Vermieter: Die Miete beträgt 700 Euro.
Mieterin: Sind die Nebenkosten inklusive?
Vermieter: Nein, sie sind extra: etwa 120 Euro.
Mieterin: Und die Kaution?
Vermieter: Drei Monatsmieten.
Mieterin: Okay, ich überlege es mir bis morgen.""",
     """房東：租金是 700 歐。
房客：雜費含在內嗎？
房東：不含，另外大約 120 歐。
房客：那押金呢？
房東：三個月租金。
房客：好，我考慮到明天。""",
     [n("beträgt", "為……（金額）"), n("inklusive", "包含在內"),
      n("extra", "另外"), n("Kaution", "押金"),
      n("überlege es mir", "考慮一下", "sich überlegen。")],
     [p("Sind … inklusive?", "問是否含在內", "Ist Frühstück inklusive?"),
      p("Ich überlege es mir bis …", "暫緩決定", "Ich überlege es mir.")],
     ["租屋關鍵詞：Miete、Nebenkosten、Kaution。"], ["住房"]),
]

for t in A2_MORE if False else A2_TEMPLATES:
    A2.append(item(*([t[0], "A2"] + list(t[1:]))))

# More A2 items 16-50
A2_REST = [
("a2-16","story","運動","Fit bleiben","保持健康",
"""Dreimal pro Woche gehe ich joggen.
Manchmal gehe ich auch ins Fitnessstudio.
Danach dusche ich und trinke Wasser.
Sport hilft mir gegen Stress.
Wenn ich keine Zeit habe, mache ich Übungen zu Hause.""",
"""我一週跑步三次。
有時也去健身房。
之後洗澡喝水。
運動幫我對抗壓力。
沒時間時就在家做操。""",
[n("Dreimal pro Woche","一週三次"),n("Fitnessstudio","健身房"),n("gegen Stress","對抗壓力"),n("Übungen","練習／運動動作")],
[p("…-mal pro Woche","每週頻率","Zweimal pro Woche lerne ich Deutsch."),p("helfen gegen","有助於對抗","Tee hilft gegen Husten.")],
["把頻率詞換成你的運動習慣。"],["健康"]),
("a2-17","email","租屋","Besichtigung","看房預約",
"""Guten Tag Frau Keller,

ich interessiere mich für Ihre Wohnung.
Könnte ich sie am Samstag um 11 Uhr besichtigen?
Ich arbeite in der Nähe und suche etwas Ruhiges.

Mit freundlichen Grüßen
David Huang""",
"""Keller 女士您好，

我對您的公寓有興趣。
可以星期六 11 點去看房嗎？
我在附近工作，想找安靜一點的。

此致問候
David Huang""",
[n("interessiere mich für","對……有興趣"),n("besichtigen","參觀／看房"),n("in der Nähe","在附近"),n("etwas Ruhiges","安靜一點的東西")],
[p("Ich interessiere mich für + 第四格","表達興趣","Ich interessiere mich für den Kurs."),p("Könnte ich …?","客氣請求許可","Könnte ich morgen kommen?")],
["看房信：興趣＋提議時間＋簡短自我背景。"],["住房","郵件"]),
("a2-18","notice","工作","Praktikum","實習公告",
"""Praktikum im Büro (3 Monate)
Aufgaben: E-Mails schreiben, Termine planen, Telefon annehmen
Voraussetzungen: gute Deutschkenntnisse, Teamfähigkeit
Beginn: 1. September
Bitte Lebenslauf senden an jobs@firma.de""",
"""辦公室實習（3 個月）
工作：寫郵件、安排行程、接電話
條件：德語良好、具備團隊能力
開始：9 月 1 日
請寄履歷至 jobs@firma.de""",
[n("Praktikum","實習"),n("Aufgaben","工作內容"),n("Voraussetzungen","條件／前提"),n("Lebenslauf","履歷")],
[p("Aufgaben: + 不定式列表","列工作","Aufräumen, Kochen, Einkaufen"),p("Bitte … senden an","投遞指示","Bitte Foto senden an …")],
["讀職缺先抓：時間、任務、條件、聯絡。"],["工作"]),
("a2-19","story","節日","Geburtstag","生日",
"""Letzte Woche hatte meine Schwester Geburtstag.
Wir haben einen Kuchen gebacken und Gäste eingeladen.
Am Abend haben wir gesungen und Fotos gemacht.
Sie hat sich sehr gefreut.
Ich schenke ihr nächstes Jahr etwas Besonderes.""",
"""上週我妹妹過生日。
我們烤了蛋糕並邀請客人。
晚上我們唱歌拍照。
她非常開心。
明年我會送她特別一點的禮物。""",
[n("hatte … Geburtstag","過生日"),n("eingebacken/gebacken","烤"),n("eingeladen","邀請"),n("hat sich gefreut","感到高興"),n("etwas Besonderes","特別的東西")],
[p("Jemanden einladen","邀請某人","Wir haben Freunde eingeladen."),p("sich freuen","感到高興","Ich freue mich auf morgen.")],
["完成式描述活動很常見。"],["慶祝","完成式"]),
("a2-20","dialogue","銀行","Konto","開戶對話",
"""Berater: Möchten Sie ein Girokonto eröffnen?
Kundin: Ja, bitte. Welche Unterlagen brauche ich?
Berater: Personalausweis und eine Meldebescheinigung.
Kundin: Okay, die habe ich dabei.
Berater: Dann können wir gleich starten.""",
"""行員：您想開立往來帳戶嗎？
顧客：好的。我需要哪些文件？
行員：身分證與戶籍登記證明。
顧客：好，我帶了。
行員：那我們可以馬上開始。""",
[n("Girokonto","往來帳戶"),n("eröffnen","開立"),n("Unterlagen","文件資料"),n("Personalausweis","身分證"),n("dabei haben","隨身帶著")],
[p("Welche … brauche ich?","問需要什麼","Welche Dokumente brauche ich?"),p("Ich habe … dabei","說有帶","Ich habe Geld dabei.")],
["行政對話：需求＋文件＋下一步。"],["行政"]),
]
for t in A2_REST:
    A2.append(item(t[0],"A2",t[1],t[2],t[3],t[4],t[5],t[6],t[7],t[8],t[9],t[10]))

# Fill a2-21 .. a2-50 with compact but real content
FILL = [
("a2-21","story","媒體","Nachrichten","看新聞",
"""Jeden Abend schaue ich kurz Nachrichten.
Ich verstehe noch nicht alles, aber ich lerne Wörter.
Manchmal lese ich auch einfache Texte online.
So bleibe ich über das Wetter und den Verkehr informiert.
Deutsch lernen geht auch mit Medien.""",
"""每天晚上我看一下新聞。
我還不能全懂，但能學單字。
有時也在網路上讀簡單文章。
這樣我能知道天氣與交通資訊。
用媒體也能學德文。""",
[n("Nachrichten","新聞"),n("noch nicht alles","還不能全部"),n("informiert bleiben","保持知情"),n("Verkehr","交通")],
[p("Ich verstehe noch nicht alles, aber …","程度說明","Ich spreche noch nicht perfekt, aber ich übe."),p("über … informiert","知情於……","über die Schule informiert")],
["真實學習策略短文。"],["媒體","學習"]),
("a2-22","email","抱怨","Zu laute Nachbarn","太吵的鄰居",
"""Guten Tag,

seit einer Woche ist es abends sehr laut bei meinen Nachbarn.
Ich muss früh aufstehen und kann nicht gut schlafen.
Könnten Sie bitte mit ihnen sprechen?

Vielen Dank
Herr Braun (Wohnung 4)""",
"""您好，

一週以來鄰居晚上都很吵。
我必須早起，睡不好。
可以請您跟他們談談嗎？

謝謝
Braun 先生（4 號房）""",
[n("seit einer Woche","一週以來"),n("laut","大聲的"),n("aufstehen","起床")],
[p("seit + 時間","從……以來","seit zwei Tagen"),p("Könnten Sie bitte …?","客氣請求","Könnten Sie das prüfen?")],
["投訴信保持禮貌與事實。"],["郵件","生活"]),
("a2-23","notice","安全","Feuerübung","消防演習",
"""Achtung: Feuerübung morgen um 10 Uhr
Bitte verlassen Sie das Gebäude ruhig über die Treppen.
Nicht den Aufzug benutzen!
Treffpunkt: Parkplatz vor dem Haus.""",
"""注意：明天 10 點消防演習
請冷靜走樓梯離開大樓。
不要使用電梯！
集合點：屋前停車場。""",
[n("Achtung","注意"),n("verlassen","離開"),n("Treppen","樓梯（複數）"),n("Treffpunkt","集合點")],
[p("Bitte verlassen Sie …","正式指示","Bitte warten Sie hier."),p("Nicht + 名詞 + benutzen","禁止使用","Nicht das Handy benutzen!")],
["安全指示：動詞命令＋集合點。"],["安全"]),
("a2-24","story","食物","Neues Rezept","新食譜",
"""Gestern habe ich zum ersten Mal Lasagne gemacht.
Zuerst habe ich die Zutaten gekauft.
Dann habe ich alles Schritt für Schritt zubereitet.
Es hat länger gedauert als gedacht.
Aber meine Freunde fanden es lecker.""",
"""昨天我第一次做千層麵。
先買了材料。
再一步步料理。
花的時間比想的久。
但朋友們覺得很好吃。""",
[n("zum ersten Mal","第一次"),n("Zutaten","材料"),n("Schritt für Schritt","一步步"),n("zubereiten","料理準備"),n("länger als gedacht","比想的更久")],
[p("zum ersten Mal + 完成式","第一次做某事","Zum ersten Mal bin ich geflogen."),p("länger / teurer als gedacht","超出預期","Es war teurer als gedacht.")],
["敘事含比較：als gedacht。"],["飲食","比較"]),
("a2-25","dialogue","數位","WLAN-Passwort","Wi‑Fi 密碼",
"""Gast: Haben Sie WLAN?
Host: Ja, klar. Das Passwort steht auf der Karte.
Gast: Ich finde die Karte nicht.
Host: Moment, ich schreibe es Ihnen auf.
Gast: Super, jetzt bin ich online.""",
"""客人：有 Wi‑Fi 嗎？
主人：有啊。密碼寫在卡片上。
客人：我找不到卡片。
主人：稍等，我寫給您。
客人：太好了，我現在上網了。""",
[n("Passwort","密碼"),n("steht auf","寫在……上面"),n("schreibe … auf","寫下來"),n("online","在線上")],
[p("Haben Sie WLAN?","問網路","Gibt es WLAN?"),p("auf die Karte schreiben","寫在卡片","Ich schreibe es auf.")],
["旅行住宿超常見對話。"],["旅行","數位"]),
("a2-26","story","環境","Müll trennen","垃圾分類",
"""In Deutschland trennt man den Müll.
Papier kommt in die blaue Tonne.
Glas bringt man zum Container.
Bioabfall hat eine eigene Tonne.
Am Anfang ist das kompliziert, aber man gewöhnt sich daran.""",
"""在德國要分垃圾。
紙類進藍色桶。
玻璃拿到回收桶。
廚餘有專用桶。
一開始很複雜，但會習慣。""",
[n("trennt","分類"),n("Tonne","垃圾桶"),n("Bioabfall","廚餘"),n("gewöhnt sich daran","習慣這件事")],
[p("man + 動詞","一般人／人們","Man spricht hier Deutsch."),p("sich an etwas gewöhnen","習慣某事","Ich gewöhne mich an den Lärm.")],
["文化短文：說明規則＋個人感受。"],["文化","生活"]),
("a2-27","email","課程","Anmeldung zum Kurs","報名課程",
"""Hallo,

ich möchte mich für den A2-Kurs am Abend anmelden.
Ist noch ein Platz frei?
Ich kann dienstags und donnerstags.

Freundliche Grüße
Nora""",
"""您好，

我想報名晚上的 A2 課程。
還有位子嗎？
我星期二、四可以。

問候
Nora""",
[n("mich … anmelden","報名", "sich anmelden für。"),n("Platz frei","有空位"),n("dienstags","每逢週二")],
[p("Ich möchte mich für … anmelden","報名","Ich melde mich für den Kurs an."),p("dienstags / mittwochs","每週固定日","Ich arbeite montags.")],
["報名信短而清楚：想要什麼＋時間條件。"],["學習","郵件"]),
("a2-28","notice","交通","Baustelle","施工",
"""Baustelle: 12.–20. März
Die Hauptstraße ist teilweise gesperrt.
Bitte benutzen Sie die Umleitung über die Parkstraße.
Mit dem Bus rechnen Sie mit 10 Minuten mehr.""",
"""施工：3 月 12–20 日
主街部分封閉。
請改走經 Parkstraße 的改道。
搭公車請預多 10 分鐘。""",
[n("Baustelle","工地"),n("gesperrt","封閉的"),n("Umleitung","改道"),n("rechnen mit","預計會有……")],
[p("ist gesperrt","宣布封閉","Die Brücke ist gesperrt."),p("rechnen mit + 第三格","預估","Rechnen Sie mit Regen.")],
["交通公告抓：日期、改道、多花時間。"],["交通"]),
("a2-29","story","感情","Streit und Entschuldigung","吵架與道歉",
"""Gestern hatte ich Streit mit meinem Mitbewohner.
Wir haben beide laut gesprochen.
Später habe ich mich entschuldigt.
Er auch.
Jetzt ist wieder alles okay.
Gutes Reden hilft.""",
"""昨天我和室友吵架了。
我們都大聲說話。
後來我道歉了。
他也是。
現在又沒事了。
好好說話有幫助。""",
[n("Streit haben","吵架"),n("Mitbewohner","室友"),n("mich entschuldigt","道歉", "sich entschuldigen。"),n("wieder alles okay","又沒事了")],
[p("sich entschuldigen","道歉","Ich entschuldige mich."),p("Jetzt ist wieder alles okay","和好","Alles wieder gut.")],
["A2 可談簡單人際衝突與和解。"],["社交"]),
("a2-30","dialogue","郵局","Paket","寄包裹",
"""Mitarbeiterin: Möchten Sie das Paket ins Inland oder ins Ausland schicken?
Kunde: Ins Inland, bitte.
Mitarbeiterin: Mit Tracking kostet das 5,99 Euro.
Kunde: Gut. Wann kommt es an?
Mitarbeiterin: In der Regel in zwei Tagen.""",
"""職員：您要寄國內還是國外？
顧客：國內，麻煩。
職員：含追蹤是 5.99 歐。
顧客：好。什麼時候到？
職員：通常兩天內。""",
[n("ins Inland / Ausland","國內／國外"),n("Tracking","追蹤"),n("Wann kommt es an?","什麼時候到？"),n("In der Regel","通常")],
[p("ins Inland / Ausland schicken","寄送範圍","Nach Österreich schicken"),p("In der Regel + 時間","一般情況","In der Regel um 9 Uhr")],
["服務場合問清楚費用與時間。"],["服務"]),
]
for t in FILL:
    A2.append(item(t[0],"A2",t[1],t[2],t[3],t[4],t[5],t[6],t[7],t[8],t[9],t[10]))

A2_FINAL = [
("a2-31","story","科技","Zu viel Handy","太多手機",
"""Viele Leute schauen zu oft aufs Handy.
Auch ich mache das manchmal.
Deshalb lege ich abends das Handy in ein anderes Zimmer.
So schlafe ich besser.
Kleine Regeln helfen im Alltag.""",
"""很多人太常看手機。
我也有時這樣。
所以晚上我把手機放到另一間房。
這樣我睡得比較好。
小規則有助於日常生活。""",
[n("aufs Handy","看著手機", "auf das。"),n("lege","放置"),n("So + 句子","這樣一來"),n("im Alltag","在日常生活中")],
[p("Deshalb + 改變習慣","因果","Deshalb stehe ich früher auf."),p("So + 結果","因而","So spare ich Zeit.")],
["議題短文：問題→作法→效果。"],["生活","論點"]),
("a2-32","email","感謝","Danke für die Hilfe","感謝信",
"""Liebe Frau Nguyen,

vielen Dank für Ihre Hilfe gestern.
Ohne Sie hätte ich den Formular-Fehler nicht gefunden.
Ich habe alles korrigiert und abgeschickt.

Herzliche Grüße
Omar""",
"""親愛的 Nguyen 女士，

非常感謝您昨天的幫忙。
沒有您我找不到表格錯誤。
我已全部改正並寄出。

誠摯問候
Omar""",
[n("Ohne Sie","沒有您"),n("Formular","表格"),n("korrigiert","改正"),n("abgeschickt","寄出")],
[p("Vielen Dank für + 第四格","感謝","Vielen Dank für Ihre Zeit."),p("Ich habe … korrigiert","說明已處理","Ich habe die E-Mail geschickt.")],
["感謝信：謝什麼＋結果。"],["郵件"]),
("a2-33","notice","健身","Studio-Regeln","健身房規定",
"""Studio-Regeln
1. Handtuch benutzen
2. Geräte nach dem Training reinigen
3. Keine laute Musik ohne Kopfhörer
Bei Fragen: Rezeption""",
"""健身房規定
1. 使用毛巾
2. 訓練後清潔器材
3. 無耳機勿放大聲音樂
問題請洽櫃台""",
[n("Handtuch","毛巾"),n("Geräte","器材"),n("reinigen","清潔"),n("Rezeption","櫃台")],
[p("Nummerierte Regeln","條列規定","1. … 2. …"),p("Bei Fragen: + 單位","洽詢","Bei Fragen: Info-Punkt")],
["條列閱讀是 A2 必備能力。"],["規定"]),
("a2-34","story","假期","Kurzer Trip","短旅行",
"""Am langen Wochenende war ich in Leipzig.
Ich habe Museen besucht und viel zu Fuß entdeckt.
Das Hostel war günstig und sauber.
Nur das Wetter war schlecht.
Trotzdem war die Reise toll.""",
"""連假我去了萊比錫。
我參觀博物館，步行探索很多。
旅舍便宜又乾淨。
只是天氣不好。
儘管如此旅行很棒。""",
[n("langes Wochenende","連假"),n("zu Fuß","步行"),n("entdeckt","探索發現"),n("Trotzdem","儘管如此")],
[p("Nur …","唯一缺點","Nur der Preis war hoch."),p("Trotzdem + 正面評價","轉折","Trotzdem bleibe ich.")],
["短評結構：整體＋細節＋轉折。"],["旅行"]),
("a2-35","dialogue","保險","Versicherung", "保險諮詢",
"""Beraterin: Haben Sie schon eine Haftpflichtversicherung?
Kunde: Nein, noch nicht. Brauche ich die?
Beraterin: Ja, sie ist in Deutschland sehr wichtig.
Kunde: Was kostet sie ungefähr?
Beraterin: Oft zwischen 50 und 70 Euro im Jahr.""",
"""顧問：您有責任險了嗎？
顧客：還沒。我需要嗎？
顧問：需要，在德國很重要。
顧客：大概多少錢？
顧問：常常一年 50 到 70 歐。""",
[n("Haftpflichtversicherung","責任險"),n("ungefähr","大約"),n("im Jahr","每年")],
[p("Brauche ich …?","問是否需要","Brauche ich einen Termin?"),p("zwischen … und …","範圍","zwischen 10 und 20")],
["行政／保險詞彙 A2 開始出現。"],["行政"]),
("a2-36","story","學習策略","Besser lernen","更好學習",
"""Ich lerne jeden Tag 20 Minuten Deutsch.
Ich schreibe neue Wörter in ein Heft.
Dann mache ich zwei Beispielsätze.
Einmal pro Woche wiederhole ich alles.
So vergesse ich weniger.""",
"""我每天學 20 分鐘德文。
我把新單字寫進筆記本。
再造兩個例句。
每週複習一次全部。
這樣忘得比較少。""",
[n("Heft","筆記本"),n("Beispielsätze","例句"),n("wiederhole","複習"),n("weniger","比較少")],
[p("jeden Tag + 時間量","習慣","Jeden Tag lese ich 10 Minuten."),p("So + 比較級結果","方法成效","So lerne ich schneller.")],
["學習方法短文，可直接套用。"],["學習"]),
("a2-37","email","改期","Termin verschieben","改期",
"""Hallo Herr Vogt,

leider kann ich den Termin am Mittwoch nicht einhalten.
Könnten wir auf Donnerstag 15 Uhr verschieben?
Bitte sagen Sie mir kurz Bescheid.

Viele Grüße
Elena""",
"""Vogt 先生您好，

很抱歉我無法趕上星期三的預約。
可以改到星期四 15 點嗎？
請簡短回覆我。

問候
Elena""",
[n("einhalten","遵守／趕上（約定）"),n("verschieben","延期／改期"),n("Bescheid sagen","告知結果")],
[p("leider kann ich … nicht","委婉拒絕／改期","Leider kann ich nicht kommen."),p("auf + 時間 + verschieben","改到……","auf Montag verschieben"),p("Bescheid sagen","請回覆","Sagen Sie bitte Bescheid.")],
["改期信三句就夠。"],["郵件","約定"]),
("a2-38","notice","宿舍","Waschküche","洗衣房",
"""Waschküche
Öffnung: 7–22 Uhr
Waschmaschine: 2 €
Bitte Wäsche danach sofort abholen.
Name auf Waschmittel schreiben.""",
"""洗衣房
開放：7–22 點
洗衣機：2 歐
洗完請立即取走衣物。
清潔劑上請寫名字。""",
[n("Waschküche","洗衣房"),n("Wäsche","待洗衣物"),n("abholen","取走"),n("Waschmittel","洗衣精／粉")],
[p("bitte … danach …","先後順序規則","Bitte danach aufräumen."),p("Name auf … schreiben","標名","Namen auf die Box schreiben")],
["宿舍生活實用閱讀。"],["生活"]),
("a2-39","dialogue","餐廳抱怨","Das Essen ist kalt","餐點是冷的",
"""Gast: Entschuldigung, das Essen ist kalt.
Kellner: Oh, das tut mir leid. Ich bringe Ihnen sofort ein neues.
Gast: Danke, und bitte ohne Zwiebeln.
Kellner: Natürlich. Einen Moment.""",
"""客人：不好意思，餐點是冷的。
服務生：噢，抱歉。我立刻幫您換一份。
客人：謝謝，另外請不要洋蔥。
服務生：當然。請稍候。""",
[n("das tut mir leid","我很抱歉"),n("sofort","立刻"),n("ohne + 名詞","不要……"),n("Einen Moment","請稍候")],
[p("Das Essen ist kalt / falsch","禮貌投訴","Die Suppe ist zu salzig."),p("bitte ohne …","排除配料","bitte ohne Milch")],
["投訴＋解決＋額外需求。"],["餐廳","禮貌"]),
("a2-40","story","搬家","Umzug","搬家",
"""Am Samstag bin ich umgezogen.
Freunde haben mir geholfen, die Kartons zu tragen.
Die neue Wohnung ist kleiner, aber näher an der Uni.
Am Abend waren wir alle erschöpft.
Trotzdem haben wir Pizza gefeiert.""",
"""星期六我搬家了。
朋友幫我搬紙箱。
新公寓比較小，但離大學更近。
晚上大家都累壞了。
儘管如此我們還是用披薩慶祝。""",
[n("umgezogen","搬家（完成式）"),n("Kartons","紙箱"),n("näher an","更靠近"),n("erschöpft","筋疲力盡")],
[p("jemandem helfen, zu + 不定式","幫忙做","Sie hilft mir zu lernen."),p("kleiner, aber näher","比較級對照","teurer, aber besser")],
["搬家故事含比較級。"],["生活","比較級"]),
]
for t in A2_FINAL:
    A2.append(item(t[0],"A2",t[1],t[2],t[3],t[4],t[5],t[6],t[7],t[8],t[9],t[10]))

A2_LAST = [
("a2-41","email","推薦","Restauranttipp","餐廳推薦",
"""Hi Lea,

falls du ein gutes Restaurant suchst: Probier „Olive“!
Es ist nicht teuer und die Pasta ist fantastisch.
Am besten reservierst du am Wochenende.

Bis bald
Chris""",
"""嗨 Lea，

如果你在找好餐廳：試試「Olive」！
不貴，義大利麵超棒。
週末最好先訂位。

待會見
Chris""",
[n("falls","如果／倘若"),n("Probier","試試（命令式）"),n("Am besten","最好"),n("reservierst","預約")],
[p("falls du … suchst","條件推薦","Falls du Zeit hast, komm vorbei."),p("Am besten + 句子","給建議","Am besten gehst du früh.")],
["口語郵件可用 falls／Am besten。"],["推薦"]),
("a2-42","story","志願","Ehrenamt","志工",
"""Einmal im Monat helfe ich in einer Bibliothek.
Ich sortiere Bücher und erkläre Besuchern das System.
Manchmal lese ich auch Kindern vor.
Es macht mir Spaß und ich treffe neue Leute.
Ehrenamt bringt Erfahrung.""",
"""我每個月在圖書館幫忙一次。
我整理書籍並向訪客說明系統。
有時也朗讀給孩子聽。
我覺得很有趣，也能認識新朋友。
做志工能累積經驗。""",
[n("Einmal im Monat","每月一次"),n("sortiere","分類整理"),n("vorlesen","朗讀"),n("Ehrenamt","志工／榮譽職"),n("Erfahrung","經驗")],
[p("Einmal im Monat / in der Woche","頻率","Zweimal im Jahr"),p("Es macht mir Spaß","覺得有趣","Deutsch macht mir Spaß.")],
["談興趣與社會參與。"],["社交","學習"]),
("a2-43","notice","大學","Sprechstunde","老師面談時間",
"""Sprechstunde Prof. Adler
Dienstag 13–14 Uhr, Raum 2.17
Bitte per E-Mail anmelden.
Themen: Hausarbeit, Prüfung, Praktikum
Ohne Anmeldung nur kurze Fragen.""",
"""Adler 教授面談時間
週二 13–14 點，2.17 室
請先用電子郵件預約。
主題：作業、考試、實習
未預約僅接受簡短問題。""",
[n("Sprechstunde","辦公室面談時間"),n("anmelden","登記預約"),n("Hausarbeit","書面作業"),n("Ohne Anmeldung","未預約")],
[p("Bitte per E-Mail anmelden","預約方式","Bitte telefonisch anmelden."),p("Ohne … nur …","限制條件","Ohne Ticket nur Stehplätze")],
["大學生活必讀告示。"],["學校"]),
("a2-44","dialogue","天氣計劃改變","Picknick verschieben","野餐改期",
"""A: Sollen wir das Picknick auf Sonntag verschieben?
B: Warum?
A: Der Wetterbericht sagt Regen für Samstag.
B: Gut Idee. Sonntag passt bei mir.
A: Super, ich schreibe es in die Gruppe.""",
"""A：我們要把野餐改到星期天嗎？
B：為什麼？
A：氣象報告說星期六會下雨。
B：好主意。星期天我可以。
A：太好了，我寫到群組裡。""",
[n("Sollen wir …?","我們要不要……？"),n("Wetterbericht","氣象報告"),n("passt bei mir","我方便／合適"),n("Gruppe","群組")],
[p("Sollen wir …?","提議","Sollen wir später treffen?"),p("passt bei mir / mir","時間合適","Donnerstag passt mir.")],
["計劃變更的自然對話。"],["計劃","天氣"]),
("a2-45","story","消費","Zu impulsiv","太衝動",
"""Online sehe ich oft Rabatte.
Letzte Woche habe ich zu schnell etwas gekauft.
Das T-Shirt gefällt mir gar nicht.
Jetzt schreibe ich eine Liste, bevor ich bestelle.
So spare ich Geld.""",
"""我常在網上看見折扣。
上週我太快下單。
那件 T 恤我一點都不喜歡。
現在我會先列清單再下單。
這樣能省錢。""",
[n("Rabatte","折扣"),n("gefällt mir gar nicht","一點都不喜歡"),n("bevor","在……之前"),n("spare","節省")],
[p("bevor + 句子","在……之前","Bevor ich kaufe, vergleiche ich Preise."),p("So spare ich …","因此節省","So spare ich Zeit.")],
["反思消費，A2 議題短文。"],["生活","連接詞"]),
("a2-46","email","詢問","Öffnungszeiten fragen","詢問營業時間",
"""Guten Tag,

haben Sie auch sonntags geöffnet?
Ich möchte am Sonntag Vormittag vorbeikommen.
Bitte um kurze Rückmeldung.

Mit freundlichen Grüßen
Tanja Meister""",
"""您好，

您們星期天也有營業嗎？
我想星期天早上去一趟。
請簡短回覆。

此致問候
Tanja Meister""",
[n("sonntags","每逢周日"),n("geöffnet","營業中"),n("vorbeikommen","過來一趟"),n("Rückmeldung","回覆")],
[p("Haben Sie … geöffnet?","問是否營業","Haben Sie heute geöffnet?"),p("Bitte um kurze Rückmeldung","請回覆","Ich bitte um Rückmeldung.")],
["服務業詢問信範本。"],["郵件","服務"]),
("a2-47","notice","健康","Impfaktion","接種活動",
"""Impfaktion im Gesundheitsamt
Freitag 9–15 Uhr
Bitte Versichertenkarte mitbringen.
Wartezeit möglich.
Kinder nur mit Eltern.""",
"""衛生局接種活動
星期五 9–15 點
請攜帶保險卡。
可能需要等候。
兒童須由家長陪同。""",
[n("Impfaktion","接種活動"),n("Gesundheitsamt","衛生局"),n("Versichertenkarte","保險卡"),n("Wartezeit","等候時間")],
[p("Bitte … mitbringen","請攜帶","Bitte Ausweis mitbringen."),p("… nur mit …","附帶條件","Eintritt nur mit Ticket")],
["公共服務告示閱讀。"],["健康","行政"]),
("a2-48","story","文化","Erstes Konzert","第一場演唱會",
"""Am Freitag war ich zum ersten Mal in einem Konzert.
Es gab viele Leute und laute Musik.
Am Anfang war ich nervös, dann habe ich mitgesungen.
Nach dem Konzert habe ich ein Poster gekauft.
Ein schöner Abend!""",
"""星期五我第一次去演唱會。
人很多，音樂很吵。
一開始我很緊張，後來跟著唱。
演唱會後我買了海報。
美好的夜晚！""",
[n("Es gab","有"),n("nervös","緊張的"),n("mitgesungen","跟著唱"),n("Poster","海報")],
[p("Am Anfang …, dann …","過程轉折","Am Anfang war es schwer, dann besser."),p("Ein schöner Abend!","短評收尾","Ein toller Tag!")],
["文化體驗短敘事。"],["文化"]),
("a2-49","dialogue","共用廚房","Küchenplan","廚房值日",
"""A: Wer putzt diese Woche die Küche?
B: Ich bin dran, oder?
A: Ja. Und ich kaufe Spülmittel.
B: Super. Wann machst du es?
A: Morgen Abend nach der Arbeit.""",
"""A：這週誰清廚房？
B：輪到我了吧？
A：對。我去買洗碗精。
B：太好了。你什麼時候做？
A：明天晚上下班後。""",
[n("Wer …?","誰？"),n("Ich bin dran","輪到我"),n("Spülmittel","洗碗精"),n("nach der Arbeit","下班後")],
[p("Wer ist dran?","問輪值","Du bist dran."),p("nach der Arbeit / dem Unterricht","在……之後","nach dem Sport")],
["室友生活對話。"],["生活","社交"]),
("a2-50","story","複習長文","Mein Alltag in Deutschland","我在德國的日常",
"""Ich wohne seit einem Jahr in Deutschland.
Morgens fahre ich mit dem Rad zur Uni.
Nachmittags lerne ich in der Bibliothek oder treffe Freunde.
Deutsch ist manchmal schwer, besonders die Artikel.
Aber ich werde besser.
Am Wochenende entdecke ich die Stadt.
Ich bin froh, dass ich hier bin.""",
"""我在德國住一年了。
早上騎腳踏車去大學。
下午在圖書館學習或見朋友。
德文有時很難，尤其是冠詞。
但我愈來愈好。
週末探索城市。
我很高興自己在這裡。""",
[n("seit einem Jahr","一年以來"),n("mit dem Rad","騎腳踏車"),n("besonders","尤其"),n("werde besser","變得更好"),n("froh, dass","高興……")],
[p("seit + 時間量","持續到現在","seit drei Monaten"),p("besonders + 名詞","強調難點","besonders die Grammatik"),p("Ich bin froh, dass …","情感＋dass","Ich bin froh, dass du kommst.")],
["A2 總複習：日常＋學習感受＋dass 入門。","長度比 A1 明顯更長，註解也更多。"],
["複習","生活","dass"]),
]
for t in A2_LAST:
    A2.append(item(t[0],"A2",t[1],t[2],t[3],t[4],t[5],t[6],t[7],t[8],t[9],t[10]))

assert len(A2) == 50, len(A2)

# Fix a1-01 tip typo if any and a2-01 focus typo
for it in A2:
    it["focus"] = [f for f in it["focus"] if f.strip() and "entlich" not in f]
    if not it["focus"]:
        it["focus"] = ["閱讀"]

data = {
    "levels": ["A1", "A2"],
    "note": "A1：短句／對話／告示；A2：段落／郵件／公告。先完成前面等級。",
    "items": A1 + A2,
}

OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"wrote {OUT} a1={len(A1)} a2={len(A2)} total={len(data['items'])}")
