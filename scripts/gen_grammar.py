#!/usr/bin/env python3
"""Generate CEFR-leveled German grammar curriculum for Wortklang."""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "src" / "data" / "grammar.json"

topics: list[dict] = []


def add(
    id: str,
    level: str,
    category: str,
    title: str,
    title_de: str,
    summary: str,
    points: list[str],
    examples: list[tuple[str, str]],
    *,
    forms: list[dict] | None = None,
    tips: list[str] | None = None,
    related: list[str] | None = None,
):
    topics.append(
        {
            "id": id,
            "level": level,
            "category": category,
            "title": title,
            "titleDe": title_de,
            "summary": summary,
            "points": points,
            "forms": forms or [],
            "examples": [{"de": de, "zh": zh} for de, zh in examples],
            "tips": tips or [],
            "related": related or [],
        }
    )


# ═══════════════════════════════════════════
# A1
# ═══════════════════════════════════════════

add(
    "a1-alphabet-pronunciation",
    "A1",
    "發音與基礎",
    "字母與發音要點",
    "Alphabet und Aussprache",
    "德文字母 26 個，外加 ä ö ü ß。掌握重音與常見字母組合，聽單字會比較準。",
    [
        "母音：a e i o u；變母音：ä ö ü；ß 讀如 ss。",
        "ch 在 i/e 後偏軟（ich），在 a/o/u 後偏喉（auch）。",
        "重音多在字首；不可分前綴通常重音在字根（verstehen）。",
        "z 讀如 ts；v 多讀 f（Vater）；w 讀如英文 v。",
    ],
    [
        ("Ich heiße Anna.", "我叫 Anna。"),
        ("Guten Tag!", "你好／午安！"),
        ("Wie bitte?", "請再說一次？"),
    ],
    tips=["先跟著朗讀短句，比單一背字母更有效。"],
)

add(
    "a1-articles-nom",
    "A1",
    "冠詞與名詞",
    "定冠詞與不定冠詞（主格）",
    "Bestimmte und unbestimmte Artikel (Nominativ)",
    "名詞一定有性別：陽性 der、陰性 die、中性 das。主格用來當主語。",
    [
        "定冠詞主格：der / die / das／複數 die。",
        "不定冠詞主格：ein / eine / ein；複數沒有不定冠詞（用 Ø 或 welche）。",
        "陰性與複數的 die 相同，靠名詞複數形與動詞判斷。",
        "學名詞一定要連冠詞一起記：der Tisch、die Lampe、das Buch。",
    ],
    [
        ("Der Mann kommt.", "那位男士來了。"),
        ("Eine Frau wartet.", "一位女士在等。"),
        ("Das Kind spielt.", "孩子在玩。"),
        ("Die Kinder spielen.", "孩子們在玩。"),
    ],
    forms=[
        {
            "label": "主格冠詞",
            "headers": ["", "陽性", "陰性", "中性", "複數"],
            "rows": [
                ["定冠詞", "der", "die", "das", "die"],
                ["不定冠詞", "ein", "eine", "ein", "—"],
            ],
        }
    ],
    tips=["不要只記中文意思，一定記 der/die/das。"],
    related=["a1-noun-plural", "a1-accusative"],
)

add(
    "a1-noun-plural",
    "A1",
    "冠詞與名詞",
    "名詞複數常見型",
    "Pluralformen der Nomen",
    "複數沒有單一規則，但有常見模式，可先記高頻詞的複數。",
    [
        "常見：-e（Tag→Tage）、-er（Kind→Kinder）、-n/-en（Frau→Frauen）。",
        "有些加母音變音：Buch→Bücher、Vater→Väter。",
        "外來詞常加 -s：Auto→Autos、Hotel→Hotels。",
        "複數定冠詞一律 die。",
    ],
    [
        ("die Tage", "日子們"),
        ("die Kinder", "孩子們"),
        ("die Frauen", "女人們"),
        ("die Autos", "汽車們"),
    ],
    tips=["單字卡上同時寫複數，例如 der Tag – die Tage。"],
    related=["a1-articles-nom"],
)

add(
    "a1-personal-pronouns",
    "A1",
    "代詞",
    "人稱代詞主格",
    "Personalpronomen (Nominativ)",
    "主格代詞當句子主語：ich, du, er/sie/es, wir, ihr, sie/Sie。",
    [
        "正式「您」寫 Sie（大寫），動詞用第三人稱複數形。",
        "er／sie／es 對應陽性／陰性／中性名詞。",
        "ihr = 你們（非正式複數）。",
    ],
    [
        ("Ich bin Student.", "我是學生。"),
        ("Du bist nett.", "你人很好。"),
        ("Sie sind Lehrer.", "您／他們是老師。"),
        ("Wir lernen Deutsch.", "我們學德文。"),
    ],
    forms=[
        {
            "label": "主格人稱代詞",
            "headers": ["單數", "複數"],
            "rows": [
                ["ich 我", "wir 我們"],
                ["du 你", "ihr 你們"],
                ["er/sie/es 他/她/它", "sie 他們"],
                ["Sie 您", "Sie 您們"],
            ],
        }
    ],
)

add(
    "a1-sein-haben",
    "A1",
    "動詞現在時",
    "sein 與 haben（現在時）",
    "sein und haben im Präsens",
    "最重要的兩個動詞：表「是／在」與「有」，也是完成時助動詞。",
    [
        "sein：bin, bist, ist, sind, seid, sind。",
        "haben：habe, hast, hat, haben, habt, haben。",
        "許多狀態、身份、年齡用 sein；擁有物用 haben。",
    ],
    [
        ("Ich bin müde.", "我累了。"),
        ("Er hat ein Auto.", "他有一輛車。"),
        ("Wir sind zu Hause.", "我們在家。"),
        ("Hast du Zeit?", "你有時間嗎？"),
    ],
    forms=[
        {
            "label": "sein / haben",
            "headers": ["人稱", "sein", "haben"],
            "rows": [
                ["ich", "bin", "habe"],
                ["du", "bist", "hast"],
                ["er/sie/es", "ist", "hat"],
                ["wir", "sind", "haben"],
                ["ihr", "seid", "habt"],
                ["sie/Sie", "sind", "haben"],
            ],
        }
    ],
    related=["a1-prasens-regular"],
)

add(
    "a1-prasens-regular",
    "A1",
    "動詞現在時",
    "規則動詞現在時",
    "Regelmäßige Verben im Präsens",
    "多數動詞現在時：去掉 -en，加 -e/-st/-t/-en/-t/-en。",
    [
        "字幹以 -t/-d/-n/-m 結尾時，du/er 常加 -e-：arbeiten → du arbeitest。",
        "字幹以 -s/-ß/-z/-x 結尾：du 只加 -t：heißen → du heißt。",
        "動詞通常在第二位（陳述句）。",
    ],
    [
        ("Ich lerne Deutsch.", "我學德文。"),
        ("Du wohnst in Berlin.", "你住在柏林。"),
        ("Er arbeitet viel.", "他工作很多。"),
        ("Wir spielen Fußball.", "我們踢足球。"),
    ],
    forms=[
        {
            "label": "lernen（學）",
            "headers": ["人稱", "形式"],
            "rows": [
                ["ich", "lerne"],
                ["du", "lernst"],
                ["er/sie/es", "lernt"],
                ["wir", "lernen"],
                ["ihr", "lernt"],
                ["sie/Sie", "lernen"],
            ],
        }
    ],
    related=["a1-word-order", "a1-sein-haben"],
)

add(
    "a1-prasens-irregular",
    "A1",
    "動詞現在時",
    "常見不規則現在時（母音變化）",
    "Unregelmäßige Präsensformen",
    "部分強變化動詞在 du／er 會改母音：e→i/ie，a→ä。",
    [
        "e→i：sprechen → du sprichst, er spricht。",
        "e→ie：lesen → du liest, er liest；sehen → du siehst。",
        "a→ä：fahren → du fährst；schlafen → du schläfst。",
        "wir／ihr／sie 通常與不定式相同（ihr 仍用 -t）。",
    ],
    [
        ("Was sprichst du?", "你說什麼語言？"),
        ("Er liest ein Buch.", "他在讀一本書。"),
        ("Wann fährst du?", "你什麼時候出發／開車？"),
        ("Sie schläft noch.", "她還在睡。"),
    ],
    forms=[
        {
            "label": "常見變化",
            "headers": ["不定式", "du", "er/sie/es"],
            "rows": [
                ["sprechen", "sprichst", "spricht"],
                ["lesen", "liest", "liest"],
                ["sehen", "siehst", "sieht"],
                ["fahren", "fährst", "fährt"],
                ["schlafen", "schläfst", "schläft"],
                ["geben", "gibst", "gibt"],
                ["nehmen", "nimmst", "nimmt"],
                ["essen", "isst", "isst"],
            ],
        }
    ],
)

add(
    "a1-word-order",
    "A1",
    "語序與句型",
    "陳述句語序：動詞第二位",
    "Satzstellung: Verbzweitstellung",
    "德文陳述句核心：變位動詞永遠在第二位。",
    [
        "主語可在第一位：Ich lerne Deutsch。",
        "也可把時間／地方提前，動詞仍第二：Heute lerne ich Deutsch。",
        "不要寫成 *Heute ich lerne…（錯）。",
    ],
    [
        ("Ich gehe heute ins Kino.", "我今天去電影院。"),
        ("Heute gehe ich ins Kino.", "今天我去電影院。"),
        ("In Berlin wohne ich.", "我住在柏林。"),
    ],
    tips=["把「動詞第二位」當成鐵律先練熟。"],
    related=["a1-questions"],
)

add(
    "a1-questions",
    "A1",
    "語序與句型",
    "是非問句與 W 問句",
    "Ja-/Nein-Fragen und W-Fragen",
    "是非問：動詞開頭；W 問：疑問詞開頭，動詞第二。",
    [
        "Kommst du mit? → Ja./Nein./Doch.",
        "W-詞：wer, was, wo, wohin, woher, wann, wie, warum, wie viel…",
        "Wo（在哪）≠ Wohin（去哪）≠ Woher（從哪來）。",
    ],
    [
        ("Wohnst du hier?", "你住這裡嗎？"),
        ("Wo wohnst du?", "你住哪裡？"),
        ("Wohin gehst du?", "你要去哪裡？"),
        ("Wie heißt du?", "你叫什麼名字？"),
    ],
    related=["a1-word-order"],
)

add(
    "a1-negation",
    "A1",
    "否定",
    "nicht 與 kein",
    "Negation mit nicht und kein",
    "kein 否定帶不定冠詞／無冠詞的名詞；nicht 否定動詞、形容詞、副詞或整句。",
    [
        "Ich habe kein Auto.（不是 *nicht ein Auto）",
        "nicht 常放在句末或被否定成分前：Ich komme nicht.／Das ist nicht gut.",
        "Kein 隨格與性別變化：kein, keine, keinen…",
    ],
    [
        ("Ich trinke keinen Kaffee.", "我不喝咖啡。"),
        ("Das ist nicht teuer.", "這不貴。"),
        ("Er kommt heute nicht.", "他今天不來。"),
        ("Wir haben keine Zeit.", "我們沒有時間。"),
    ],
    related=["a1-articles-nom", "a1-accusative"],
)

add(
    "a1-accusative",
    "A1",
    "格變",
    "第四格（Akkusativ）入門",
    "Akkusativ",
    "直接受詞用第四格。陽性定冠詞 der→den，ein→einen；其他性別形式多與主格相同。",
    [
        "問「誰／什麼被動詞直接作用」→ 第四格。",
        "定冠詞：den / die / das／複數 die。",
        "不定冠詞：einen / eine / ein。",
        "常見動詞：haben, sehen, kaufen, lesen, brauchen, treffen…",
    ],
    [
        ("Ich sehe den Mann.", "我看見那位男士。"),
        ("Sie kauft eine Tasche.", "她買一個袋子。"),
        ("Hast du das Buch?", "你有那本書嗎？"),
        ("Wir brauchen einen Tisch.", "我們需要一張桌子。"),
    ],
    forms=[
        {
            "label": "第四格冠詞",
            "headers": ["", "陽性", "陰性", "中性", "複數"],
            "rows": [
                ["定冠詞", "den", "die", "das", "die"],
                ["不定冠詞", "einen", "eine", "ein", "—"],
            ],
        }
    ],
    related=["a1-articles-nom", "a2-dative"],
)

add(
    "a1-possessive",
    "A1",
    "代詞",
    "所有格冠詞（主格／第四格）",
    "Possessivartikel",
    "mein, dein, sein, ihr, unser, euer, Ihr 像不定冠詞一樣變格。",
    [
        "主格：mein Vater, meine Mutter, mein Kind。",
        "第四格陽性：meinen Vater；陰性／中性：meine／mein。",
        "ihr = 她的／他們的；Ihr（大寫）= 您的。",
    ],
    [
        ("Das ist mein Bruder.", "這是我哥哥／弟弟。"),
        ("Ich rufe meinen Freund an.", "我打電話給我朋友。"),
        ("Ist das Ihre Tasche?", "這是您的袋子嗎？"),
    ],
    forms=[
        {
            "label": "mein（主格／第四格）",
            "headers": ["格", "陽性", "陰性", "中性", "複數"],
            "rows": [
                ["Nom.", "mein", "meine", "mein", "meine"],
                ["Akk.", "meinen", "meine", "mein", "meine"],
            ],
        }
    ],
)

add(
    "a1-modal-basic",
    "A1",
    "情態動詞",
    "情態動詞入門",
    "Modalverben (A1)",
    "können, müssen, wollen, dürfen, sollen, mögen：情態動詞變位，主要動詞用不定式放句末。",
    [
        "Ich kann schwimmen.（不是 *Ich kann schwimme）",
        "疑問：Kannst du mir helfen?",
        "möchten（想要，較禮貌）當情態用：Ich möchte einen Kaffee.",
    ],
    [
        ("Ich kann Deutsch sprechen.", "我會說德文。"),
        ("Wir müssen gehen.", "我們必須走了。"),
        ("Willst du mitkommen?", "你想一起去嗎？"),
        ("Ich möchte Wasser, bitte.", "我想要水，拜託。"),
    ],
    forms=[
        {
            "label": "können / müssen / wollen（單數）",
            "headers": ["", "können", "müssen", "wollen"],
            "rows": [
                ["ich", "kann", "muss", "will"],
                ["du", "kannst", "musst", "willst"],
                ["er/sie/es", "kann", "muss", "will"],
            ],
        }
    ],
    related=["a2-modal-full"],
)

add(
    "a1-separable",
    "A1",
    "動詞現在時",
    "可分動詞（現在時）",
    "Trennbare Verben",
    "aufstehen, anrufen, mitkommen…：前綴在陳述句中拆到句末。",
    [
        "Ich stehe um 7 Uhr auf.",
        "疑問：Stehst du früh auf?",
        "不定式／情態後：Ich will aufstehen.（前綴連在一起）",
    ],
    [
        ("Ich stehe früh auf.", "我早起。"),
        ("Rufst du mich an?", "你會打給我嗎？"),
        ("Kommst du mit?", "你一起來嗎？"),
        ("Wir gehen heute aus.", "我們今天外出。"),
    ],
    tips=["看到 auf-/an-/mit-/aus-/ein- 等，先想是不是可分。"],
)

add(
    "a1-imperative",
    "A1",
    "語序與句型",
    "命令式入門",
    "Imperativ",
    "對 du／ihr／Sie 下指令。du 常去掉 -st；Sie 用動詞原形＋Sie。",
    [
        "Komm!／Kommt!／Kommen Sie!",
        "sein：Sei still!／Seid ruhig!／Seien Sie bitte…",
        "禮貌請求常用 bitte，或用 Können Sie…?",
    ],
    [
        ("Komm her!", "過來！"),
        ("Macht die Tür zu!", "把門關上！（對你們）"),
        ("Kommen Sie bitte rein!", "請進來！"),
        ("Sei vorsichtig!", "小心點！"),
    ],
)

add(
    "a1-time-numbers",
    "A1",
    "數字與時間",
    "數字、時間與日期",
    "Zahlen, Uhrzeit und Datum",
    "點鐘用 Uhr；問時間 Wie spät ist es?；日期用 am + 星期／日期。",
    [
        "Es ist drei Uhr.／Es ist halb vier.（3:30）",
        "星期：am Montag；月份：im Juli。",
        "序數常加 -te／-ste：der erste, der zweite, der zwanzigste。",
    ],
    [
        ("Wie spät ist es?", "現在幾點？"),
        ("Es ist halb acht.", "七點半。"),
        ("Am Freitag habe ich Zeit.", "星期五我有空。"),
        ("Mein Geburtstag ist am 5. Mai.", "我生日是 5 月 5 日。"),
    ],
)

add(
    "a1-local-prep",
    "A1",
    "介詞",
    "地點介詞入門（in/an/auf/zu…）",
    "Lokale Präpositionen (A1)",
    "先分「在哪裡」（位置）與「去哪裡」（方向）。A1 先記固定搭配。",
    [
        "zu Hause（在家）／nach Hause（回家）。",
        "in die Schule（去學校，陰性第四格方向）。",
        "常用：in, an, auf, bei, zu, nach, aus, von。",
        "城市／國家多數用 nach（nach Berlin）；陰性國名／有冠詞的用 in die…",
    ],
    [
        ("Ich bin zu Hause.", "我在家。"),
        ("Ich gehe nach Hause.", "我回家。"),
        ("Wir fahren nach Deutschland.", "我們去德國。"),
        ("Sie ist in der Schule.", "她在學校。"),
    ],
    related=["a2-two-way-prep"],
)

add(
    "a1-adjectives-pred",
    "A1",
    "形容詞",
    "表語形容詞（不加字尾）",
    "Prädikative Adjektive",
    "形容詞在 sein／werden／bleiben 後當表語時，不加字尾。",
    [
        "Das Buch ist interessant.（不是 *interessantes）",
        "比較入門：größer, kleiner, besser, mehr…",
        "修飾名詞時才要加字尾（A2／B1 再系統學）。",
    ],
    [
        ("Das Wetter ist schön.", "天氣很好。"),
        ("Die Prüfung ist schwer.", "考試很難。"),
        ("Ich bin müde.", "我累了。"),
        ("Das ist besser.", "這樣比較好。"),
    ],
    related=["a2-adjective-endings"],
)

add(
    "a1-coord-conj",
    "A1",
    "連接詞與從句",
    "對等連接詞",
    "Nebenordnende Konjunktionen",
    "und, oder, aber, denn, sondern 連接兩個主句，語序不變（動詞仍第二）。",
    [
        "aber＝但是；sondern＝而是（接在否定後）。",
        "denn＝因為（主句語序，不同於 weil）。",
        "Ich bleibe hier, denn ich bin müde.",
    ],
    [
        ("Ich trinke Tee und er trinkt Kaffee.", "我喝茶，他喝咖啡。"),
        ("Kommst du mit oder bleibst du hier?", "你來還是留在這？"),
        ("Es ist teuer, aber gut.", "雖貴但好。"),
        ("Ich trinke nicht Bier, sondern Wein.", "我不喝啤酒，而是喝葡萄酒。"),
    ],
    related=["a2-weil-dass"],
)

# ═══════════════════════════════════════════
# A2
# ═══════════════════════════════════════════

add(
    "a2-dative",
    "A2",
    "格變",
    "第三格（Dativ）",
    "Dativ",
    "間接受詞、許多介詞與固定動詞用第三格。陽性／中性定冠詞變 dem，陰性 der，複數 den（＋名詞常加 -n）。",
    [
        "定冠詞：dem / der / dem / den。",
        "不定冠詞：einem / einer / einem。",
        "常見動詞：helfen, danken, gehören, gefallen, geben（給誰＝第三格）。",
        "Ich gebe dem Kind einen Ball.（誰→第三格，什麼→第四格）",
    ],
    [
        ("Ich helfe dem Mann.", "我幫助那位男士。"),
        ("Das Buch gehört der Frau.", "這本書屬於那位女士。"),
        ("Das gefällt mir.", "這個我喜歡。"),
        ("Wir danken Ihnen.", "我們感謝您。"),
    ],
    forms=[
        {
            "label": "第三格冠詞",
            "headers": ["", "陽性", "陰性", "中性", "複數"],
            "rows": [
                ["定冠詞", "dem", "der", "dem", "den"],
                ["不定冠詞", "einem", "einer", "einem", "—"],
            ],
        }
    ],
    related=["a1-accusative", "a2-akk-dat-verbs"],
)

add(
    "a2-akk-dat-verbs",
    "A2",
    "格變",
    "雙賓動詞：給誰＋什麼",
    "Verben mit Dativ und Akkusativ",
    "geben, zeigen, schenken, bringen, schicken…：人用第三格，物用第四格。",
    [
        "順序常是：主語 – 動詞 – 第三格 – 第四格。",
        "若第四格是代詞，代詞常靠前：Ich gebe es dir.",
        "Er zeigt mir das Foto.",
    ],
    [
        ("Ich gebe dir das Buch.", "我把書給你。"),
        ("Sie schickt ihm eine E-Mail.", "她寄一封信給他。"),
        ("Kannst du mir das Salz geben?", "你可以給我鹽嗎？"),
    ],
)

add(
    "a2-dative-prep",
    "A2",
    "介詞",
    "固定第三格介詞",
    "Präpositionen mit Dativ",
    "mit, nach, von, zu, aus, bei, seit, außer, gegenüber 後接第三格。",
    [
        "mit dem Bus, zur Arbeit（zu + der → zur）, zum Arzt。",
        "seit einem Jahr；bei meinen Eltern。",
        "aus Deutschland；von meinem Freund。",
    ],
    [
        ("Ich fahre mit dem Zug.", "我搭火車。"),
        ("Sie kommt aus Taiwan.", "她來自台灣。"),
        ("Ich wohne bei meiner Tante.", "我住在阿姨家。"),
        ("Wir gehen zum Bahnhof.", "我們去火車站。"),
    ],
    related=["a2-akk-prep", "a2-two-way-prep"],
)

add(
    "a2-akk-prep",
    "A2",
    "介詞",
    "固定第四格介詞",
    "Präpositionen mit Akkusativ",
    "durch, für, ohne, um, gegen, bis, entlang…後接第四格。",
    [
        "für dich, ohne mich, um 8 Uhr, durch den Park。",
        "gegen die Wand；bis nächsten Montag。",
    ],
    [
        ("Das Geschenk ist für dich.", "這禮物是給你的。"),
        ("Ohne dich gehe ich nicht.", "沒有你我不去。"),
        ("Wir gehen durch den Park.", "我們穿過公園。"),
        ("Der Kurs beginnt um 9 Uhr.", "課程九點開始。"),
    ],
)

add(
    "a2-two-way-prep",
    "A2",
    "介詞",
    "位置／方向兩用介詞（Wechselpräpositionen）",
    "Wechselpräpositionen",
    "in, an, auf, über, unter, vor, hinter, neben, zwischen：問 wo（位置）用第三格；問 wohin（方向）用第四格。",
    [
        "Ich bin in dem / im Zimmer.（位置→Dativ）",
        "Ich gehe in das / ins Zimmer.（方向→Akkusativ）",
        "縮寫：im, ins, am, ans, zum, zur…",
    ],
    [
        ("Das Buch liegt auf dem Tisch.", "書在桌上。"),
        ("Ich lege das Buch auf den Tisch.", "我把書放到桌上。"),
        ("Wir sind im Kino.", "我們在電影院。"),
        ("Wir gehen ins Kino.", "我們去電影院。"),
    ],
    tips=["liegen/stehen/sitzen＝位置；legen/stellen/setzen＝放置方向。"],
)

add(
    "a2-perfekt",
    "A2",
    "動詞時態",
    "現在完成時 Perfekt",
    "Perfekt",
    "口語談過去多用 Perfekt：haben/sein + 過去分詞（句末）。",
    [
        "多數動詞用 haben；位移／狀態變化常用 sein（gehen, fahren, kommen, aufstehen…）。",
        "規則分詞：ge- + 字幹 + -t（gemacht）。",
        "強變化：ge- + 字幹變化 + -en（gesprochen, gegangen）。",
        "可分動詞：前綴 + ge + 字幹（aufgestanden）。",
    ],
    [
        ("Ich habe gearbeitet.", "我工作過了。"),
        ("Sie ist nach Hause gegangen.", "她回家了。"),
        ("Hast du gut geschlafen?", "你睡得好嗎？"),
        ("Wir sind um 6 Uhr aufgestanden.", "我們六點起床。"),
    ],
    forms=[
        {
            "label": "助動詞選擇",
            "headers": ["類型", "例子"],
            "rows": [
                ["haben", "machen, kaufen, sehen, sprechen"],
                ["sein", "gehen, kommen, fahren, fliegen, aufstehen"],
            ],
        }
    ],
    related=["a2-participle", "b1-prateritum"],
)

add(
    "a2-participle",
    "A2",
    "動詞時態",
    "過去分詞構成",
    "Partizip II",
    "記住常見不規則三態，是 Perfekt 的關鍵。",
    [
        "弱變化：gemacht, gelernt, gekauft。",
        "強變化：geschrieben, gelesen, genommen, gegessen。",
        "不可分前綴（be-/ver-/er-/ent-…）不加 ge-：besucht, verkauft, erklärt。",
        "-ieren 動詞不加 ge-：studiert, telefoniert。",
    ],
    [
        ("Ich habe einen Brief geschrieben.", "我寫了一封信。"),
        ("Er hat das Fenster geöffnet.", "他開了窗。"),
        ("Wir haben das Museum besucht.", "我們參觀了博物館。"),
        ("Sie hat Medizin studiert.", "她念過醫學。"),
    ],
)

add(
    "a2-modal-full",
    "A2",
    "情態動詞",
    "情態動詞完整變化與用法",
    "Modalverben (A2)",
    "六個情態動詞表能力、義務、意願、許可、建議、喜好；過去常用简单過去（wollte, musste…）。",
    [
        "dürfen＝被允許；müssen＝必須；sollen＝應該（外在要求）。",
        "nicht dürfen＝禁止；nicht müssen＝不必。",
        "Perfekt 較少用情態完成時；口語常：Ich musste arbeiten.",
    ],
    [
        ("Hier darf man nicht rauchen.", "這裡不准吸菸。"),
        ("Du musst nicht kommen.", "你不必來。"),
        ("Was soll ich tun?", "我該怎麼辦？"),
        ("Ich wollte dich anrufen.", "我本來想打給你。"),
    ],
    forms=[
        {
            "label": "情態動詞現在時（ich/du/er）",
            "headers": ["動詞", "ich", "du", "er"],
            "rows": [
                ["können", "kann", "kannst", "kann"],
                ["müssen", "muss", "musst", "muss"],
                ["dürfen", "darf", "darfst", "darf"],
                ["sollen", "soll", "sollst", "soll"],
                ["wollen", "will", "willst", "will"],
                ["mögen", "mag", "magst", "mag"],
            ],
        }
    ],
)

add(
    "a2-weil-dass",
    "A2",
    "連接詞與從句",
    "weil / dass 從句：動詞到句末",
    "Nebensätze mit weil und dass",
    "從屬連接詞引出從句時，變位動詞移到句末。",
    [
        "Ich bleibe zu Hause, weil ich krank bin.",
        "Ich glaube, dass er recht hat.",
        "主句若在後：Weil ich krank bin, bleibe ich zu Hause.（從句後主句動詞仍第二）",
    ],
    [
        ("Ich lerne, weil ich die Prüfung bestehen will.", "我學習，因為想通過考試。"),
        ("Sie sagt, dass sie keine Zeit hat.", "她說她沒時間。"),
        ("Weil es regnet, nehmen wir ein Taxi.", "因為下雨，我們搭計程車。"),
    ],
    related=["a2-wenn-als", "b1-relative"],
)

add(
    "a2-wenn-als",
    "A2",
    "連接詞與從句",
    "wenn 與 als",
    "wenn und als",
    "als＝過去一次性；wenn＝現在／未來，或過去習慣性重複。",
    [
        "Als ich Kind war, …（從前那時候）",
        "Wenn ich Zeit habe, …（每當／如果）",
        "Falls 也表「如果」，較書面。",
    ],
    [
        ("Als ich nach Berlin kam, war alles neu.", "當我初到柏林時，一切都很新鮮。"),
        ("Wenn es kalt ist, trage ich einen Mantel.", "天氣冷時我穿大衣。"),
        ("Wenn du willst, können wir gehen.", "如果你願意，我們可以走。"),
    ],
)

add(
    "a2-reflexive",
    "A2",
    "動詞現在時",
    "反身動詞",
    "Reflexive Verben",
    "sich 對應主語：mich/dich/sich/uns/euch/sich。有些固定用反身。",
    [
        "Akkusativ 反身：Ich freue mich.／Setz dich!",
        "Dativ 反身：Ich wasche mir die Hände.（身體部位常用第三格反身）",
        "常見：sich freuen, sich interessieren für, sich ärgern, sich erinnern an。",
    ],
    [
        ("Ich freue mich auf das Wochenende.", "我期待週末。"),
        ("Interessierst du dich für Musik?", "你對音樂有興趣嗎？"),
        ("Er setzt sich auf den Stuhl.", "他坐到椅子上。"),
        ("Wir erinnern uns an dich.", "我們記得你。"),
    ],
)

add(
    "a2-adjective-endings",
    "A2",
    "形容詞",
    "形容詞字尾入門（定冠詞後）",
    "Adjektivdeklination nach dem bestimmten Artikel",
    "定冠詞後形容詞用「弱變化」：多為 -e／-en。",
    [
        "der gute Mann, die gute Frau, das gute Kind。",
        "第四格陽性：den guten Mann；複數：die guten Leute。",
        "先把「定冠詞 + 形容詞 + 名詞」練熟，再學不定冠詞後字尾。",
    ],
    [
        ("der alte Lehrer", "那位老老師"),
        ("eine kleine Wohnung", "一間小公寓"),
        ("mit dem neuen Auto", "用那輛新車"),
        ("Ich habe den teuren Mantel gekauft.", "我買了那件貴大衣。"),
    ],
    forms=[
        {
            "label": "定冠詞後（弱變化摘要）",
            "headers": ["格", "陽性", "陰性", "中性", "複數"],
            "rows": [
                ["Nom.", "-e", "-e", "-e", "-en"],
                ["Akk.", "-en", "-e", "-e", "-en"],
                ["Dat.", "-en", "-en", "-en", "-en"],
            ],
        }
    ],
    related=["b1-adjective-endings-full"],
)

add(
    "a2-comparative",
    "A2",
    "形容詞",
    "比較級與最高級",
    "Komparativ und Superlativ",
    "比較級多加 -er；最高級 am …-sten 或定冠詞 + …-ste。",
    [
        "groß → größer → am größten／der größte。",
        "常見不規則：gut-besser-am besten；viel-mehr-am meisten。",
        "比較用 als：größer als…；同等用 so … wie。",
    ],
    [
        ("Berlin ist größer als Bonn.", "柏林比波恩大。"),
        ("Heute ist es so kalt wie gestern.", "今天和昨天一樣冷。"),
        ("Das ist am besten.", "這樣最好。"),
        ("Er ist der älteste Student.", "他是最年長的學生。"),
    ],
)

add(
    "a2-pronouns-akk-dat",
    "A2",
    "代詞",
    "人稱代詞第三／四格",
    "Personalpronomen in Akkusativ und Dativ",
    "mich/dich/ihn/sie/es／mir/dir/ihm/ihr… 必須熟記。",
    [
        "Akk：mich, dich, ihn, sie, es, uns, euch, sie, Sie。",
        "Dat：mir, dir, ihm, ihr, ihm, uns, euch, ihnen, Ihnen。",
        "Sie（您）Akk＝Sie，Dat＝Ihnen。",
    ],
    [
        ("Ich sehe dich.", "我看見你。"),
        ("Kannst du mir helfen?", "你可以幫我嗎？"),
        ("Ich gebe es ihm.", "我把它給他。"),
        ("Wir besuchen Sie morgen.", "我們明天拜訪您。"),
    ],
    forms=[
        {
            "label": "代詞對照",
            "headers": ["Nom.", "Akk.", "Dat."],
            "rows": [
                ["ich", "mich", "mir"],
                ["du", "dich", "dir"],
                ["er", "ihn", "ihm"],
                ["sie", "sie", "ihr"],
                ["es", "es", "ihm"],
                ["wir", "uns", "uns"],
                ["ihr", "euch", "euch"],
                ["sie", "sie", "ihnen"],
                ["Sie", "Sie", "Ihnen"],
            ],
        }
    ],
)

add(
    "a2-indefinite",
    "A2",
    "代詞",
    "不定代詞 man / jemand / etwas",
    "Indefinitpronomen",
    "man＝人們／一般人（只作主語）；etwas／nichts；jemand／niemand。",
    [
        "Man spricht hier Deutsch.",
        "nichts／niemand 已是否定，不要再加 nicht。",
        "alles, viel, wenig 也可當代詞用。",
    ],
    [
        ("Man kann hier gut essen.", "這裡很好吃／人們在這吃得好。"),
        ("Ich habe nichts verstanden.", "我什麼都沒聽懂。"),
        ("Hat jemand angerufen?", "有人打電話來嗎？"),
        ("Das gefällt allen.", "大家都合口味。"),
    ],
)

add(
    "a2-future-werden",
    "A2",
    "動詞時態",
    "未來與 werden",
    "Futur mit werden / werden als Vollverb",
    "werden + 不定式可表未來；口語更常用現在時＋時間詞。werden 也可表「變成」。",
    [
        "Ich werde morgen anrufen.（未來）",
        "Morgen rufe ich an.（更自然的口語未來）",
        "Es wird kalt.（變冷）",
    ],
    [
        ("Ich werde nächstes Jahr nach Wien fahren.", "我明年要去維也納。"),
        ("Es wird spät.", "時候不早了。"),
        ("Was willst du werden?", "你將來想做什麼？"),
    ],
    related=["b1-passive"],
)

add(
    "a2-indirect-questions",
    "A2",
    "連接詞與從句",
    "間接問句",
    "Indirekte Fragesätze",
    "間接問句是從句：動詞在句末。用 ob（是否）或原疑問詞。",
    [
        "Ich weiß nicht, ob er kommt.",
        "Kannst du mir sagen, wo der Bahnhof ist?",
        "不要用是非問的動詞開頭語序。",
    ],
    [
        ("Weißt du, wann der Zug kommt?", "你知道火車何時到嗎？"),
        ("Ich frage mich, ob das stimmt.", "我在想這是否屬實。"),
        ("Sag mir bitte, wie du heißt.", "請告訴我你叫什麼。"),
    ],
)

add(
    "a2-connectors-time",
    "A2",
    "連接詞與從句",
    "時間從句：bevor, nachdem, während…",
    "Temporale Konjunktionen",
    "時間連接詞引導從句，動詞置末。注意時態搭配。",
    [
        "bevor＝在…之前；nachdem＝在…之後（常搭配完成時）。",
        "während＝當…時候／而；seit＝自從；bis＝直到。",
        "Nachdem ich gegessen hatte, ging ich spazieren.（B1 會再用過去完成）",
    ],
    [
        ("Bevor ich gehe, rufe ich dich an.", "我走之前會打給你。"),
        ("Während er kocht, höre ich Musik.", "他煮飯時我聽音樂。"),
        ("Wir warten, bis du kommst.", "我們等到你來。"),
    ],
)

# ═══════════════════════════════════════════
# B1
# ═══════════════════════════════════════════

add(
    "b1-genitive",
    "B1",
    "格變",
    "第二格（Genitiv）",
    "Genitiv",
    "表所屬：des / der / des / der。口語常被 von + Dativ 取代，但書面與固定介詞仍重要。",
    [
        "das Auto des Mannes；die Tasche der Frau。",
        "陽性／中性名詞常加 -s／-es：des Tages, des Kindes。",
        "介詞：während, wegen, trotz, statt／anstatt, aufgrund…（正式體）。",
        "口語：wegen dem Regen → 正式 wegen des Regens。",
    ],
    [
        ("Das ist das Fahrrad meines Bruders.", "這是我哥哥的腳踏車。"),
        ("Trotz des Regens gehen wir spazieren.", "儘管下雨我們仍去散步。"),
        ("Während der Pause trinke ich Kaffee.", "休息時間我喝咖啡。"),
        ("Das ist das Büro der Chefin.", "這是女上司的辦公室。"),
    ],
    forms=[
        {
            "label": "第二格冠詞",
            "headers": ["", "陽性", "陰性", "中性", "複數"],
            "rows": [
                ["定冠詞", "des", "der", "des", "der"],
                ["不定冠詞", "eines", "einer", "eines", "—"],
            ],
        }
    ],
)

add(
    "b1-n-declension",
    "B1",
    "格變",
    "陽性弱變化（N-Deklination）",
    "N-Deklination",
    "部分陽性名詞除主格單數外皆加 -n／-en：der Student – den Studenten – dem Studenten。",
    [
        "常見：Student, Herr, Nachbar, Name, Mensch, Kunde, Kollege, Experte…",
        "der Name → den Namen, dem Namen, des Namens（第二格多 -ens）。",
        "複數也常以 -n／-en 結尾。",
    ],
    [
        ("Ich kenne den Studenten.", "我認識那位大學生。"),
        ("Wir helfen dem Nachbarn.", "我們幫助鄰居。"),
        ("Der Name des Kunden steht hier.", "客戶的名字寫在這裡。"),
    ],
)

add(
    "b1-prateritum",
    "B1",
    "動詞時態",
    "简单過去 Präteritum",
    "Präteritum",
    "書面與敘事常用；sein/haben/情態動詞口語也常用简单過去。",
    [
        "弱變化：machte, lernte；強變化：ging, kam, sprach。",
        "war, hatte, konnte, musste… 很常見。",
        "口語日常多用 Perfekt；新聞／小說多用 Präteritum。",
    ],
    [
        ("Gestern war ich krank.", "昨天我生病了。"),
        ("Er hatte keine Zeit.", "他那時沒時間。"),
        ("Wir gingen nach Hause.", "我們回家了。"),
        ("Sie sagte nichts.", "她什麼也沒說。"),
    ],
    related=["a2-perfekt", "b1-plusquamperfekt"],
)

add(
    "b1-plusquamperfekt",
    "B1",
    "動詞時態",
    "過去完成時 Plusquamperfekt",
    "Plusquamperfekt",
    "表「過去的過去」：hatte/war + 過去分詞。常與 nachdem 連用。",
    [
        "Nachdem ich gegessen hatte, ging ich spazieren.",
        "助動詞用 hatte／war 的简单過去。",
    ],
    [
        ("Nachdem er angekommen war, rief er an.", "他到了之後就打電話。"),
        ("Ich hatte das Buch schon gelesen.", "我那時已經讀過那本書。"),
        ("Sie war vorher noch nie dort gewesen.", "她以前從未去過那裡。"),
    ],
)

add(
    "b1-passive",
    "B1",
    "被動語態",
    "過程被動：werden + Partizip II",
    "Vorgangspassiv",
    "強調動作過程：Das Fenster wird geöffnet. 施事用 von／durch。",
    [
        "現在：wird gemacht；過去：wurde gemacht；完成：ist … worden。",
        "情態＋被動：Das muss gemacht werden.",
        "主語是原主動句的受詞。",
    ],
    [
        ("Das Haus wird gebaut.", "房子正在被建造。"),
        ("Die E-Mail wurde gestern geschickt.", "那封郵件昨天寄出。"),
        ("Hier darf nicht geraucht werden.", "此處禁止吸菸。"),
        ("Der Termin ist abgesagt worden.", "約會已被取消。"),
    ],
    related=["b2-passive-state", "b1-passive-alternatives"],
)

add(
    "b1-passive-alternatives",
    "B1",
    "被動語態",
    "被動替代：man / sich lassen",
    "Passiversatz",
    "口語常用 man；也可用 sich lassen 表「可被…」。",
    [
        "Man öffnet die Tür um 9.（≈ Die Tür wird um 9 geöffnet.）",
        "Das lässt sich leicht erklären.（這很好解釋）",
        "sein + zu + Infinitiv：Die Aufgabe ist zu machen.（必須／可做）",
    ],
    [
        ("Man spricht hier Englisch.", "這裡有人說英語。"),
        ("Die Tür lässt sich nicht öffnen.", "這門打不開。"),
        ("Der Text ist noch zu korrigieren.", "這篇文章還需要修改。"),
    ],
)

add(
    "b1-relative",
    "B1",
    "連接詞與從句",
    "關係從句",
    "Relativsätze",
    "關係代詞與先行詞性／數一致，格由從句角色決定；動詞在從句末。",
    [
        "Nom：der/die/das／die；Akk：den/die/das／die；Dat：dem/der/dem／denen。",
        "Gen：dessen／deren。",
        "Das ist der Mann, der mir geholfen hat.",
        "介詞保留：…, mit dem ich arbeite.",
    ],
    [
        ("Das ist die Frau, die nebenan wohnt.", "那是住隔壁的那位女士。"),
        ("Ich habe ein Buch, das sehr spannend ist.", "我有一本很精彩的書。"),
        ("Der Mann, dem ich gedankt habe, ist Lehrer.", "我道謝的那位男士是老師。"),
        ("Die Stadt, in der ich wohne, ist klein.", "我住的城市很小。"),
    ],
    forms=[
        {
            "label": "關係代詞（定冠詞形）",
            "headers": ["格", "陽性", "陰性", "中性", "複數"],
            "rows": [
                ["Nom.", "der", "die", "das", "die"],
                ["Akk.", "den", "die", "das", "die"],
                ["Dat.", "dem", "der", "dem", "denen"],
                ["Gen.", "dessen", "deren", "dessen", "deren"],
            ],
        }
    ],
)

add(
    "b1-konjunktiv2-basic",
    "B1",
    "虛擬式",
    "第二虛擬式入門（禮貌／虛擬）",
    "Konjunktiv II (Grundlagen)",
    "表禮貌請求、願望、非真實條件。常用 würde + 不定式，或 wäre／hätte／würde／könnte…",
    [
        "Könnten Sie mir helfen?／Würden Sie bitte…?",
        "Wenn ich Zeit hätte, würde ich kommen.",
        "Ich hätte gern einen Kaffee.（點餐常用）",
        "高頻：wäre, hätte, würde, könnte, sollte, müsste。",
    ],
    [
        ("Ich würde gern mitkommen.", "我很想一起去。"),
        ("Hättest du morgen Zeit?", "你明天有空嗎？（較委婉）"),
        ("Wenn ich reich wäre, würde ich reisen.", "如果我有錢，我會去旅行。"),
        ("Könnten Sie das bitte wiederholen?", "可以請您再說一次嗎？"),
    ],
    related=["b2-konjunktiv2-advanced"],
)

add(
    "b1-infinitive-zu",
    "B1",
    "不定式與分詞",
    "zu 不定式與 um … zu",
    "Infinitiv mit zu",
    "許多表達後接 zu + 不定式；表目的用 um … zu。",
    [
        "Es ist wichtig, pünktlich zu sein.",
        "Ich plane, nächstes Jahr umzuziehen.（可分動詞：umzu-ziehen）",
        "Ich lerne Deutsch, um in Deutschland zu studieren.",
        "ohne … zu／statt … zu 也是常用結構。",
    ],
    [
        ("Ich versuche, früher aufzustehen.", "我試著早點起床。"),
        ("Es freut mich, dich zu sehen.", "很高興見到你。"),
        ("Er geht, ohne sich zu verabschieden.", "他沒打招呼就走了。"),
        ("Statt zu lernen, schaut er fern.", "他不學習，反而看電視。"),
    ],
)

add(
    "b1-verbs-prep",
    "B1",
    "介詞",
    "動詞＋固定介詞",
    "Verben mit Präpositionen",
    "許多動詞固定搭配介詞與格，必須整組背。",
    [
        "sich freuen auf + A（期待）；sich freuen über + A（為已發生的事高興）。",
        "warten auf + A；denken an + A；sprechen über + A／mit + D。",
        "teilnehmen an + D；sich erinnern an + A；Angst haben vor + D。",
        "問句用 wo(r)+介詞：Worauf wartest du?",
    ],
    [
        ("Ich freue mich auf die Ferien.", "我期待假期。"),
        ("Worüber sprecht ihr?", "你們在談論什麼？"),
        ("Sie nimmt an dem Kurs teil.", "她參加這門課。"),
        ("Er hat Angst vor Spinnen.", "他怕蜘蛛。"),
    ],
)

add(
    "b1-adjective-endings-full",
    "B1",
    "形容詞",
    "形容詞字尾三種變化",
    "Adjektivdeklination (Übersicht)",
    "依前面是否有定冠詞／不定冠詞／無冠詞，形容詞字尾不同。",
    [
        "定冠詞後：弱變化（多 -e／-en）。",
        "不定冠詞／所有格後：混合變化（主格陽性 -er、中性 -es 等）。",
        "無冠詞：強變化（字尾類似定冠詞：guter Wein, gute Milch）。",
        "複數無冠詞：gute Freunde；第三格複數常 -en：guten Freunden。",
    ],
    [
        ("der neue Wagen / ein neuer Wagen / neuer Wein", "新車／新車／新酒"),
        ("mit großem Interesse", "懷著很大興趣"),
        ("kalte Milch", "冷牛奶"),
        ("die Meinung netter Kollegen", "好心同事們的意見"),
    ],
    tips=["先練高頻短語，不要一次背完整張大表。"],
)

add(
    "b1-connectors-contrast",
    "B1",
    "連接詞與從句",
    "轉折與原因進階連接詞",
    "Konnektoren: obwohl, deshalb, trotzdem…",
    "分清「從句連接詞」與「副詞連接語」：後者放在主句，動詞仍第二。",
    [
        "obwohl＝雖然（從句，動詞在末）。",
        "deshalb／deswegen／darum＝因此（副詞，動詞第二）：Ich bin krank, deshalb bleibe ich zu Hause.",
        "trotzdem＝儘管如此（副詞）。",
        "da＝因為（較書面，從句）。",
    ],
    [
        ("Obwohl es regnet, gehen wir spazieren.", "雖然下雨，我們仍去散步。"),
        ("Es regnet, trotzdem gehen wir spazieren.", "在下雨，儘管如此我們仍去散步。"),
        ("Ich habe viel gearbeitet, deshalb bin ich müde.", "我做了很多，所以累了。"),
        ("Da das Wetter schlecht war, blieben wir zu Hause.", "由於天氣差，我們待在家。"),
    ],
)

add(
    "b1-word-order-advanced",
    "B1",
    "語序與句型",
    "語序進階：中域與時間－原因－方式－地點",
    "Satzbau: Mittelfeld",
    "多個副詞成分時，常見順序：時間 – 原因 – 方式 – 地點（TeKaMoLo）。",
    [
        "Ich fahre morgen wegen des Meetings mit dem Zug nach Berlin.",
        "代詞通常比名詞更靠前；第三人稱代詞受詞很靠前。",
        "nicht 位置影響否定焦點。",
    ],
    [
        ("Er hat gestern aus Nervosität sehr schnell gesprochen.", "他昨天因緊張說得很快。"),
        ("Ich gebe es dir morgen.", "我明天把它給你。"),
        ("Sie ist heute nicht zur Arbeit gekommen.", "她今天沒來上班。"),
    ],
)

add(
    "b1-local-directional",
    "B1",
    "介詞",
    "地方副詞：hin / her 與 wo-複合",
    "hin, her und wo-Komposita",
    "her＝朝向說話者；hin＝離開說話者。wofür, darauf, worüber 取代介詞＋代詞。",
    [
        "Komm her!／Geh hin!",
        "Ich freue mich darauf.（不是 *auf es）",
        "Worauf wartest du?／Darüber müssen wir sprechen.",
    ],
    [
        ("Bring das Buch bitte her.", "請把書帶過來。"),
        ("Ich bin dagegen.", "我反對。"),
        ("Worüber ärgerst du dich?", "你在氣什麼？"),
        ("Darauf kann ich nicht verzichten.", "那是我不能放棄的。"),
    ],
)

add(
    "b1-adjective-as-noun",
    "B1",
    "形容詞",
    "形容詞名詞化",
    "Substantivierte Adjektive",
    "der/die/das + 形容詞可指人／抽象概念，仍要變格。",
    [
        "der Alte, die Bekannte, etwas Neues, nichts Besonderes。",
        "大寫：Alles Gute!／im Allgemeinen。",
    ],
    [
        ("Hast du etwas Interessantes gehört?", "你有沒有聽到什麼有趣的？"),
        ("Die Angestellte ist freundlich.", "那位女職員很友善。"),
        ("Ich wünsche dir alles Gute.", "祝你一切順利。"),
    ],
)

add(
    "b1-reciprocal",
    "B1",
    "代詞",
    "互相代詞與相互結構",
    "Reziprokpronomen",
    "einander／uns／euch／sich 表互相。",
    [
        "Sie helfen einander.／Wir schreiben uns oft.",
        "miteinander, voneinander, miteinander sprechen。",
    ],
    [
        ("Die Nachbarn grüßen sich.", "鄰居們互相打招呼。"),
        ("Wir verstehen uns gut.", "我們彼此很合得來。"),
        ("Ihr solltet euch öfter sehen.", "你們應該多常見面。"),
    ],
)

# ═══════════════════════════════════════════
# B2
# ═══════════════════════════════════════════

add(
    "b2-konjunktiv1",
    "B2",
    "虛擬式",
    "第一虛擬式：間接引語",
    "Konjunktiv I (Indirekte Rede)",
    "新聞／書面轉述常用 Konjunktiv I；若與直陳式同形則改用 Konjunktiv II。",
    [
        "Er sagt, er habe keine Zeit.／Sie seien zufrieden.",
        "sein：ich sei, er sei, wir seien…",
        "與直陳式同形時（尤其 ich／wir）：改用 hätte／würde…",
        "口語轉述更常用 würde 或直陳式 + 據說。",
    ],
    [
        ("Die Ministerin sagte, sie prüfe den Vorschlag.", "部長表示她在審視該提案。"),
        ("Er behauptet, er sei unschuldig.", "他聲稱自己無辜。"),
        ("Sie meinten, sie hätten nichts gewusst.", "他們表示當時不知情。"),
    ],
    related=["b1-konjunktiv2-basic"],
)

add(
    "b2-konjunktiv2-advanced",
    "B2",
    "虛擬式",
    "第二虛擬式進階：非真實與禮貌",
    "Konjunktiv II (erweitert)",
    "非真實條件、遺憾、建議；完成體：hätte gemacht／wäre gegangen。",
    [
        "Wenn du gekommen wärst, hätten wir das gefeiert.",
        "An deiner Stelle würde ich …",
        "不规则：ginge, käme, wüsste, gäbe（書面較常見）。",
    ],
    [
        ("Wenn ich das gewusst hätte, wäre ich früher gekommen.", "我要是知道，就會早點來。"),
        ("Es wäre besser, wenn wir jetzt gingen.", "我們現在走比較好。"),
        ("Hätte ich nur mehr Zeit!", "我要是有更多時間就好了！"),
    ],
)

add(
    "b2-passive-state",
    "B2",
    "被動語態",
    "狀態被動：sein + Partizip II",
    "Zustandspassiv",
    "強調結果狀態，而非動作過程：Die Tür ist geöffnet.（門是開著的）",
    [
        "Vorgang：wird geöffnet（正在被開）；Zustand：ist geöffnet（開著）。",
        "常見：geschlossen, geöffnet, verletzt, geboren, geschrieben。",
        "不要與 Perfekt 混淆：Er ist gegangen＝他走了（主動完成，sein 動詞）。",
    ],
    [
        ("Das Fenster ist geöffnet.", "窗戶是開著的。"),
        ("Die Geschäfte sind sonntags geschlossen.", "商店週日不營業。"),
        ("Der Brief ist schon geschrieben.", "信已經寫好了。"),
    ],
)

add(
    "b2-nominalization",
    "B2",
    "其他結構",
    "名詞化（Nominalisierung）",
    "Nominalstil",
    "把動詞／形容詞變成名詞短語，常見於書面語與學術文。",
    [
        "prüfen → die Prüfung；entscheiden → die Entscheidung。",
        "nach dem Essen；bei der Ankunft；trotz wiederholter Warnungen。",
        "von + Dat／durch 常表施事；第二格表對象。",
    ],
    [
        ("Nach Abschluss des Projekts feiern wir.", "專案結束後我們慶祝。"),
        ("Die Einführung neuer Regeln führte zu Protesten.", "新規定的實施引發抗議。"),
        ("Bei starkem Regen bleibt die Schule geschlossen.", "大雨時學校關閉。"),
    ],
)

add(
    "b2-participle-clauses",
    "B2",
    "不定式與分詞",
    "分詞作形容詞與分詞短語",
    "Partizipialattribute",
    "現在分詞／過去分詞可放在名詞前當修飾語，使句子更緊湊。",
    [
        "die lachenden Kinder；ein geschriebenes Wort。",
        "die gestern angekommenen Gäste（分詞短語在名詞前）。",
        "可改寫成關係從句：die Gäste, die gestern angekommen sind。",
    ],
    [
        ("Die im Park spielenden Kinder sind laut.", "在公園玩的孩子們很吵。"),
        ("Das von ihm geschriebene Buch ist berühmt.", "他寫的那本書很有名。"),
        ("Aus Zeitgründen abgesagt, fand das Meeting nicht statt.", "因時間關係取消，會議沒舉行。"),
    ],
)

add(
    "b2-connectors-advanced",
    "B2",
    "連接詞與從句",
    "進階連接：indem, wodurch, sofern, zumal…",
    "Anspruchsvolle Konnektoren",
    "書面常見連接手段，用來表手段、後果、條件與補充原因。",
    [
        "indem＝藉由…（從句）；dadurch, dass…",
        "wodurch／weshalb 關係性連接。",
        "sofern／falls＝只要／如果；zumal＝尤其因為。",
        "je … desto／umso …＝越…越…。",
    ],
    [
        ("Man lernt, indem man übt.", "人藉由練習來學習。"),
        ("Je mehr man liest, desto besser wird man.", "讀得越多就讀得越好。"),
        ("Sofern es nicht regnet, findet das Fest statt.", "只要不下雨，活動就舉行。"),
        ("Er blieb zu Hause, zumal er krank war.", "他待在家，尤其因為他病了。"),
    ],
)

add(
    "b2-futur2",
    "B2",
    "動詞時態",
    "未來完成 Futur II 與推測",
    "Futur II und Vermutung",
    "werden + Partizip II + haben/sein 表未來完成，也常用來推測過去。",
    [
        "Bis morgen werde ich das gelesen haben.",
        "Er wird den Zug verpasst haben.（大概是誤點了）",
        "現在推測也常用 wird + Infinitiv：Sie wird im Büro sein.",
    ],
    [
        ("Bis Freitag werde ich die Arbeit beendet haben.", "到星期五我將已完成工作。"),
        ("Er wird schon angekommen sein.", "他大概已經到了。"),
        ("Das wird wohl stimmen.", "這大概是對的。"),
    ],
)

add(
    "b2-subjective-modal",
    "B2",
    "情態動詞",
    "情態動詞的主觀情態（推測／傳聞）",
    "Subjektive Modalität",
    "情態動詞可表說話者態度：推測、傳聞、竟然。",
    [
        "soll＝據說：Er soll reich sein.",
        "will＝自稱（常表懷疑）：Er will nichts gesehen haben.",
        "muss／dürfte／kann／mag 表不同把握程度的推測。",
    ],
    [
        ("Sie soll eine neue Stelle haben.", "聽說她有了新工作。"),
        ("Er will den Unfall nicht bemerkt haben.", "他自稱沒注意到事故。"),
        ("Das dürfte schwierig werden.", "這恐怕會變得困難。"),
        ("Er muss den Schlüssel verloren haben.", "他一定是把鑰匙弄丟了。"),
    ],
)

add(
    "b2-fixed-akk-dat",
    "B2",
    "格變",
    "固定片語中的格",
    "Feste Wendungen mit Kasus",
    "許多慣用表達鎖定某一格，需整組記憶。",
    [
        "es gibt + A；Spaß machen；Leid tun + D。",
        "jemandem auf die Nerven gehen；imstande sein。",
        "Schuld haben an + D；Wert legen auf + A。",
    ],
    [
        ("Es gibt viele Gründe.", "有很多理由。"),
        ("Das tut mir Leid.", "我對此感到抱歉。"),
        ("Das geht mir auf die Nerven.", "這讓我很煩。"),
        ("Sie legt Wert auf Pünktlichkeit.", "她很重視準時。"),
    ],
)

add(
    "b2-prepositional-adverbs",
    "B2",
    "介詞",
    "介詞副詞與 da(r)-／wo(r)-",
    "Präpositionaladverbien",
    "指事物時用 darauf／dafür…；問事物用 worauf／wofür…；指人仍用介詞＋代詞。",
    [
        "Ich warte auf den Bus. → Ich warte darauf.",
        "Ich warte auf dich.（人，不能 *darauf）",
        "darüber hinaus, dabei, dafür, dagegen… 也是篇章連接語。",
    ],
    [
        ("Ich bin dafür.", "我贊成。"),
        ("Darüber müssen wir noch sprechen.", "這件事我們還得談。"),
        ("Womit kann ich Ihnen helfen?", "我能用什麼幫您？"),
        ("Er hat sich darüber beschwert.", "他對此抱怨。"),
    ],
)

add(
    "b2-passive-modal",
    "B2",
    "被動語態",
    "情態動詞＋被動",
    "Modalverben im Passiv",
    "義務、許可與可能常與被動連用，書面極常見。",
    [
        "Das Formular muss ausgefüllt werden.",
        "過去：musste … werden；完成：hat … werden müssen（注意語序）。",
        "否定：braucht nicht … zu werden／muss nicht…",
    ],
    [
        ("Der Antrag soll bis Montag gestellt werden.", "申請應於星期一前提出。"),
        ("Das Problem konnte rasch gelöst werden.", "問題得以迅速解決。"),
        ("Hier darf nicht fotografiert werden.", "此處禁止拍照。"),
    ],
)

add(
    "b2-reported-questions",
    "B2",
    "連接詞與從句",
    "複雜轉述與嵌入從句",
    "Eingebettete Nebensätze",
    "多層從句嵌套時，每一層都把動詞推到該從句末。",
    [
        "Er sagte, dass er nicht wisse, ob sie komme.",
        "書面可混用 Konjunktiv I。",
        "注意標點與可讀性，過長嵌套宜拆句。",
    ],
    [
        ("Sie fragte, ob ich wüsste, wann der Zug abfahre.", "她問我是否知道火車何時開。"),
        ("Mir ist klar, dass das, was er sagt, wichtig ist.", "我明白他所說的很重要。"),
    ],
)

add(
    "b2-stylistic-inversion",
    "B2",
    "語序與句型",
    "強調與倒裝",
    "Hervorhebung und Inversion",
    "把焦點成分提前，動詞保持第二；也可用 es 作形式主語。",
    [
        "Besonders wichtig ist die Vorbereitung.",
        "Es ist wichtig, dass…／Es gibt…",
        "Nicht nur …, sondern auch …（注意動詞位置）。",
    ],
    [
        ("Schwer verständlich blieb seine Erklärung.", "他的解釋仍然難懂。"),
        ("Es freut mich, dass Sie gekommen sind.", "很高興您來了。"),
        ("Nicht nur er, sondern auch sie hat recht.", "不只是他，她也是對的。"),
    ],
)

# ═══════════════════════════════════════════
# C1
# ═══════════════════════════════════════════

add(
    "c1-register",
    "C1",
    "其他結構",
    "語域：口語、中性、書面",
    "Register und Stil",
    "同一語意在不同場合選不同結構：口語、標準、正式書面。",
    [
        "口語：Perfekt、短句、man、doch/mal/halt。",
        "書面：Präteritum、名詞化、被動、Konjunktiv I。",
        "正式信函：Seien Sie so freundlich…／Hiermit teilen wir mit…",
    ],
    [
        ("Hab ich gestern schon gemacht.（口語）", "我昨天就做了。"),
        ("Die Arbeiten wurden gestern abgeschlossen.（書面）", "工作於昨日完成。"),
        ("Hiermit bestätigen wir den Eingang Ihrer Nachricht.", "特此確認已收到您的訊息。"),
    ],
)

add(
    "c1-complex-connectors",
    "C1",
    "連接詞與從句",
    "學術／正式連接手段",
    "Wissenschaftliche Konnektoren",
    "論說文常用：insofern, infolgedessen, gleichwohl, nothingdestoweniger, zum einen … zum anderen。",
    [
        "insofern／insoweit＝在此範圍內。",
        "gleichwohl／dennoch＝儘管如此（書面）。",
        "einerseits … andererseits；zum einen … zum anderen。",
        " vorausgesetzt, dass…／angenommen, dass…",
    ],
    [
        ("Die These ist insofern problematisch, als sie…", "該論點之所以有問題，是因為…"),
        ("Gleichwohl bleibt die Frage offen.", "儘管如此，問題仍未解決。"),
        ("Zum einen spart man Zeit, zum anderen Geld.", "一方面省時，另一方面省錢。"),
    ],
)

add(
    "c1-konjunktiv-mix",
    "C1",
    "虛擬式",
    "虛擬式綜合運用",
    "Konjunktiv I und II im Gebrauch",
    "轉述、非真實、禮貌與評注性插入的綜合選擇。",
    [
        "新聞：Konjunktiv I；同形時改 II。",
        "評注：wie es heißt／angeblich／mutmaßlich 可輔助。",
        "條件句可省略 wenn 並倒裝：Hätte ich Zeit, würde ich…",
    ],
    [
        ("Hätte man früher reagiert, wäre der Schaden geringer gewesen.", "若早點反應，損失會較小。"),
        ("Der Sprecher betonte, man werde die Lage prüfen.", "發言人強調將審視情勢。"),
        ("Es sei darauf hingewiesen, dass…", "需要指出的是…"),
    ],
)

add(
    "c1-passive-advanced",
    "C1",
    "被動語態",
    "被動進階與無人稱被動",
    "Unpersönliches Passiv und Passivvarianten",
    "無賓語動詞也可被動：Es wird getanzt.／Hier wird gearbeitet.",
    [
        "及物與不及物都可形成被動（視語義）。",
        "bekommen／kriegen + Partizip（口語受惠被動）：Sie bekam das Paket zugeschickt.",
        "lassen + sich + Infinitiv 表可能性。",
    ],
    [
        ("Heute Abend wird gefeiert.", "今晚有派對／有人慶祝。"),
        ("Ihm wurde geholfen.", "有人幫助了他。"),
        ("Sie bekam die Unterlagen zugeschickt.", "文件寄給了她。"),
        ("Der Text lässt sich schwer übersetzen.", "這篇文章很難翻譯。"),
    ],
)

add(
    "c1-nominal-style",
    "C1",
    "其他結構",
    "名詞風格與動詞風格改寫",
    "Nominal- vs. Verbalstil",
    "能在兩種風格間改寫，是 C1 書面能力的核心。",
    [
        "Verbal：Nachdem das Gesetz beschlossen worden war, …",
        "Nominal：Nach der Beschlussfassung des Gesetzes …",
        "名詞風格更抽象緊湊，但過度使用會生硬。",
    ],
    [
        ("Die Erhöhung der Preise führte zu Protesten.", "漲價引發抗議。"),
        ("Dass die Preise erhöht wurden, führte zu Protesten.", "價格被提高，引發了抗議。"),
        ("Unter Berücksichtigung aller Faktoren…", "在考慮所有因素的情況下…"),
    ],
)

add(
    "c1-text-cohesion",
    "C1",
    "其他結構",
    "篇章銜接：指代與主題推進",
    "Textkohärenz",
    "用代詞、同義替換、框架語與連接副詞維持連貫。",
    [
        "dies／jenes／ersterer／letzterer（書面）。",
        "was 關係句指整句：Er kam zu spät, was alle ärgerte.",
        "dabei／dadurch／daraufhin 推進邏輯。",
    ],
    [
        ("Die Reform wurde beschlossen. Dadurch veränderten sich die Regeln.", "改革通過了。因此規則改變。"),
        ("Er vergaß den Termin, was unangenehm war.", "他忘了約會，這很尷尬。"),
        ("Zuerst … . Darüber hinaus … . Abschließend …", "首先…此外…最後…"),
    ],
)

add(
    "c1-verbs-fixed",
    "C1",
    "其他結構",
    "功能動詞結構（Funktionsverbgefüge）",
    "Funktionsverbgefüge",
    "名詞＋功能動詞取代簡單動詞，正式語體常見。",
    [
        "zur Entscheidung kommen ≈ entscheiden；in Frage stellen；unter Beweis stellen。",
        "eine Rolle spielen；Abschied nehmen；in Anspruch nehmen。",
        "注意介詞與冠詞：zur／zum／in＋Akk 等。",
    ],
    [
        ("Das stellt die Methode in Frage.", "這使該方法受到質疑。"),
        ("Wir nehmen Ihr Angebot gerne in Anspruch.", "我們很樂意接受您的提議。"),
        ("Die Ergebnisse kamen überraschend zum Vorschein.", "結果出人意料地顯現。"),
    ],
)

add(
    "c1-subjunctive-wishes",
    "C1",
    "虛擬式",
    "願望句、條件省略與固定套語",
    "Wunschsätze und formelhafte Konjunktive",
    "文學／正式套語仍保留虛擬式。",
    [
        "Käme er doch endlich!／Wenn er doch käme!",
        "Es lebe …／Gott sei Dank／dem sei, wie es wolle。",
        "sei es …, sei es …＝無論是…還是…",
    ],
    [
        ("Wäre ich doch zu Hause geblieben!", "我要是待在家就好了！"),
        ("Sei es Regen oder Schnee, wir fahren.", "無論下雨或下雪，我們都出發。"),
        ("Wie dem auch sei, wir müssen entscheiden.", "無論如何，我們必須做決定。"),
    ],
)

add(
    "c1-adjective-advanced",
    "C1",
    "形容詞",
    "分詞形容詞與複合修飾",
    "Erweiterte Attribute",
    "長修飾語放在名詞前是德文書面特色，閱讀時先找核心名詞。",
    [
        "讀法：從冠詞跳到名詞，再回頭看分詞短語。",
        "die von der Kommission gestern verabschiedete Richtlinie。",
        "也可改寫成關係從句以降低難度。",
    ],
    [
        ("die vom Ministerium vorgeschlagene Lösung", "部會提出的方案"),
        ("ein nicht zu unterschätzendes Risiko", "不可低估的風險"),
        ("die seit Jahren andauernde Diskussion", "持續多年的討論"),
    ],
)

add(
    "c1-prepositions-formal",
    "C1",
    "介詞",
    "正式介詞與介詞短語",
    "Formelle Präpositionen",
    "書面多用：bezüglich, hinsichtlich, infolge, anhand, mittels, zwecks…",
    [
        "多數接第二格：hinsichtlich des Problems。",
        "infolge＋Gen；aufgrund＋Gen；anhand＋Gen。",
        "口語對應：wegen、durch、mit Hilfe von…",
    ],
    [
        ("Hinsichtlich der Kosten bestehen Bedenken.", "關於成本存在疑慮。"),
        ("Anhand der Daten lässt sich das zeigen.", "藉由數據可以證明這點。"),
        ("Infolge des Sturms fiel der Strom aus.", "因暴風雨而停電。"),
    ],
)

add(
    "c1-speech-acts",
    "C1",
    "其他結構",
    "言語行為與緩和策略",
    "Sprechakte und Abschwächung",
    "異議、建議、批評常用緩和語：scheinen, tendenziell, eher, durchaus, nicht ganz…",
    [
        "Ich würde sagen…／Es scheint mir…／Man könnte einwenden…",
        "双重緩和：Es dürfte nicht ganz unproblematisch sein…",
        "直接命令在正式場合常改為被動或條件式。",
    ],
    [
        ("Das Argument scheint mir nicht ganz überzeugend.", "這論點我覺得不那麼有說服力。"),
        ("Es wäre zu überlegen, ob…", "或許可以考慮是否…"),
        ("Dagegen ließe sich einwenden, dass…", "對此可以反駁說…"),
    ],
)

add(
    "c1-tense-aspect-discourse",
    "C1",
    "動詞時態",
    "時態在篇章中的選擇",
    "Tempus im Text",
    "敘事、評論、背景與前瞻用不同時態組合。",
    [
        "背景：Plusquamperfekt／Präteritum；主線：Präteritum；評論：Präsens。",
        "學術摘要常用現在時表「通則」。",
        "歷史現在時可增加臨場感。",
    ],
    [
        ("Nachdem die Daten ausgewertet worden waren, zeigte sich…", "數據分析後顯示…"),
        ("Die Studie zeigt, dass…", "該研究顯示…"),
        ("Plötzlich öffnet sich die Tür…（歷史現在時）", "突然門開了…"),
    ],
)

add(
    "c1-relative-advanced",
    "C1",
    "連接詞與從句",
    "進階關係句：was, wer, wo, weswegen",
    "Erweiterte Relativsätze",
    "自由關係句與整句指代，使篇章更緊密。",
    [
        "wer …, (der) …；was …, (das) …",
        "wo／wohin 可關係地點；weshalb／weswegen 表原因。",
        "Präposition + was → wo(r)+präp：womit, worüber。",
    ],
    [
        ("Wer wagt, gewinnt.", "敢嘗試的人會贏。"),
        ("Alles, was er sagte, war falsch.", "他所說的一切都是錯的。"),
        ("Das ist der Punkt, weswegen wir streiten.", "這就是我們爭論的原因。"),
    ],
)

add(
    "c1-negation-advanced",
    "C1",
    "否定",
    "否定進階與多重否定語義",
    "Komplexe Negation",
    "kein…ohne, nicht…sondern, keineswegs, keinesfalls, alles andere als…",
    [
        "keineswegs／überhaupt nicht 加強否定。",
        "nicht einmal＝連…都不。",
        "雙重否定在德文通常仍是否定，不像部分語言變肯定。",
    ],
    [
        ("Das ist keineswegs klar.", "這絕不清楚。"),
        ("Er hat nicht einmal angerufen.", "他連電話都沒打。"),
        ("Die Lösung ist alles andere als einfach.", "這方案一點也不簡單。"),
        ("Ohne Fleiß kein Preis.", "沒有努力就沒有收穫。"),
    ],
)

# Extra coverage to make levels feel complete
add(
    "a1-greeting-intro",
    "A1",
    "語序與句型",
    "打招呼與自我介紹句型",
    "Begrüßung und Vorstellung",
    "固定開場句型，先求流利再求變化。",
    [
        "Guten Morgen／Tag／Abend；Hallo（非正式）。",
        "Ich heiße…／Mein Name ist…／Ich komme aus…",
        "Freut mich!／Angenehm!",
    ],
    [
        ("Guten Tag, ich heiße Lin.", "你好，我叫 Lin。"),
        ("Ich komme aus Taiwan und wohne in München.", "我來自台灣，住在慕尼黑。"),
        ("Freut mich, Sie kennenzulernen.", "很高興認識您。"),
    ],
)

add(
    "a2-lassen",
    "A2",
    "動詞現在時",
    "lassen 的基本用法",
    "lassen",
    "lassen 可表「讓／請人做／留下」。",
    [
        "Ich lasse das Auto reparieren.（請人修車）",
        "Lass uns gehen!（我們走吧）",
        "Kann ich meine Tasche hier lassen?",
    ],
    [
        ("Ich lasse mir die Haare schneiden.", "我去理髮（請人剪）。"),
        ("Lass uns morgen lernen.", "我們明天一起學習吧。"),
        ("Wo habe ich meinen Schlüssel gelassen?", "我把鑰匙放哪了？"),
    ],
)

add(
    "b1-als-wenn-ob",
    "B1",
    "虛擬式",
    "als ob / als wenn 虛擬比較",
    "als ob / als wenn",
    "表「彷彿」：從句常用 Konjunktiv II。",
    [
        "Er spricht, als ob er Experte wäre.",
        "也可：als wäre er Experte（省略 ob，動詞提前）。",
    ],
    [
        ("Sie tut so, als ob nichts wäre.", "她裝作若無其事。"),
        ("Es sieht aus, als hätte es geregnet.", "看起來好像下過雨。"),
    ],
)

add(
    "b2-double-infinitive",
    "B2",
    "情態動詞",
    "雙不定式與情態完成時",
    "Doppelter Infinitiv",
    "情態動詞的完成時：hat … gehen müssen（兩個不定式在句末）。",
    [
        "Ich habe gestern arbeiten müssen.",
        "從句：…, dass ich habe arbeiten müssen.（助動詞在兩個不定式前）",
        "感知動詞也類似：sehen/hören + Infinitiv。",
    ],
    [
        ("Sie hat lange warten müssen.", "她不得不等很久。"),
        ("Ich habe ihn kommen sehen.", "我看見他來了。"),
        ("Er sagt, dass er hat zu Hause bleiben müssen.", "他說他當時必須留在家。"),
    ],
)

add(
    "c1-irony-particles",
    "C1",
    "其他結構",
    "語氣小品詞（Modalpartikeln）",
    "Modalpartikeln",
    "doch, ja, halt, eben, wohl, mal, schon 不改命題，但改語氣——聽懂它們是接近母語的關鍵。",
    [
        "doch：反預期／提醒對方已知。",
        "ja：顯而易見；halt／eben：無奈接受。",
        "mal：緩和請求；schon：安撫或讓步。",
    ],
    [
        ("Das ist ja einfach!", "這明明很簡單嘛！"),
        ("Komm doch mal her!", "你過來一下嘛！"),
        ("Dann ist es halt so.", "那也就這樣吧。"),
        ("Das wird schon gut gehen.", "會沒事的。"),
    ],
)

# Validate unique ids
ids = [t["id"] for t in topics]
assert len(ids) == len(set(ids)), "duplicate ids"

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(topics, ensure_ascii=False, indent=2), encoding="utf-8")

from collections import Counter

c = Counter(t["level"] for t in topics)
print("levels", dict(c), "total", len(topics))
print("wrote", OUT, "bytes", OUT.stat().st_size)
