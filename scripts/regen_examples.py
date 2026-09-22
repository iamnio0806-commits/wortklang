#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regenerate unique, natural example sentences for every vocabulary entry."""
from __future__ import annotations

import json
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "src" / "data" / "vocabulary.json"


def hmix(s: str) -> int:
    n = 2166136261
    for ch in s:
        n ^= ord(ch)
        n = (n * 16777619) & 0xFFFFFFFF
    return n


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


def pick(pool: list, seed: int, salt: int = 0):
    return pool[(seed + salt) % len(pool)]


# (de_scene, zh_scene)
SCENES = {
    "日常": [
        ("heute Morgen", "今天早上"),
        ("am Nachmittag", "下午"),
        ("in der Stadt", "在城裡"),
        ("zu Hause", "在家"),
        ("am Wochenende", "週末"),
        ("nach der Arbeit", "下班後"),
    ],
    "飲食": [
        ("im Café", "在咖啡店"),
        ("beim Abendessen", "晚餐時"),
        ("auf dem Markt", "在市場"),
        ("in der Küche", "在廚房"),
        ("im Restaurant", "在餐廳"),
        ("zum Frühstück", "早餐時"),
    ],
    "旅行": [
        ("am Bahnhof", "在火車站"),
        ("im Hotel", "在旅館"),
        ("auf der Reise", "旅途中"),
        ("am Flughafen", "在機場"),
        ("in der Altstadt", "在老城區"),
        ("unterwegs", "在路上"),
    ],
    "家庭": [
        ("bei meinen Eltern", "在父母家"),
        ("mit der Familie", "和家人一起"),
        ("zu Hause", "在家"),
        ("am Sonntag", "星期天"),
        ("im Wohnzimmer", "在客廳"),
        ("nach der Schule", "放學後"),
    ],
    "自然": [
        ("im Park", "在公園"),
        ("am See", "在湖邊"),
        ("im Wald", "在森林裡"),
        ("bei gutem Wetter", "天氣好時"),
        ("auf dem Berg", "在山上"),
        ("am Strand", "在海邊"),
    ],
    "工作": [
        ("im Büro", "在辦公室"),
        ("in der Besprechung", "開會時"),
        ("bei der Arbeit", "工作時"),
        ("vor dem Termin", "約會前"),
        ("im Team", "在團隊裡"),
        ("diese Woche", "這週"),
    ],
    "時間": [
        ("jeden Tag", "每天"),
        ("nächste Woche", "下週"),
        ("seit gestern", "從昨天起"),
        ("um drei Uhr", "三點時"),
        ("im Sommer", "夏天"),
        ("bald", "很快"),
    ],
    "動詞": [
        ("jetzt", "現在"),
        ("gleich", "馬上"),
        ("morgen früh", "明天早上"),
        ("bitte", "拜託"),
        ("zusammen", "一起"),
        ("noch einmal", "再一次"),
    ],
    "形容詞": [
        ("heute", "今天"),
        ("diesmal", "這次"),
        ("wirklich", "真的"),
        ("ziemlich", "相當"),
        ("für mich", "對我來說"),
        ("leider", "可惜"),
    ],
    "數字": [
        ("genau", "正好"),
        ("ungefähr", "大約"),
        ("insgesamt", "總共"),
        ("pro Tag", "每天"),
        ("im Monat", "每個月"),
        ("dieses Jahr", "今年"),
    ],
}

NAMES = ["Anna", "Tom", "Lisa", "Paul", "Mia", "Jonas", "Sara", "Leo", "Nina", "Max"]


def scene_pair(cat: str, seed: int, salt: int = 0) -> tuple[str, str]:
    return pick(SCENES.get(cat, SCENES["日常"]), seed, salt)


def noun_example(w: dict, seed: int) -> tuple[str, str]:
    art = w["article"]
    word = w["word"]
    zh = w["translation"].split("／")[0].split("/")[0].strip()
    cat = w["category"]
    level = w["level"]
    de_sc, zh_sc = scene_pair(cat, seed, 1)
    name = pick(NAMES, seed, 2)
    a, d, Art = akk(art), dat(art), cap(art)

    if level == "A1":
        bank = [
            (f"Ich kenne {a} {word} schon.", f"我已經認識這個{zh}。"),
            (f"{name} erklärt mir {a} {word}.", f"{name}跟我解釋{zh}。"),
            (f"Was ist {art} {word}?", f"什麼是{zh}？"),
            (f"Wir sprechen über {a} {word}.", f"我們在談{zh}。"),
            (f"{Art} {word} interessiert mich.", f"我對{zh}有興趣。"),
            (f"Heute lerne ich {a} {word}.", f"今天我學「{zh}」這個詞。"),
            (f"Kennst du {a} {word}?", f"你知道{zh}嗎？"),
            (f"Ohne {a} {word} fehlt etwas.", f"少了{zh}就不完整。"),
            (f"{name} mag {a} {word}.", f"{name}喜歡{zh}。"),
            (f"Ich brauche {a} {word} {de_sc}.", f"我{zh_sc}需要{zh}。"),
            (f"Schau, {art} {word}!", f"看，那是{zh}！"),
            (f"Merk dir {a} {word} gut!", f"好好記住{zh}！"),
            (f"Haben wir {a} {word}?", f"我們有{zh}嗎？"),
            (f"{Art} {word} ist neu für mich.", f"「{zh}」對我來說是新的。"),
            (f"Erzähl mir von {d} {word}.", f"跟我說說{zh}吧。"),
        ]
    elif level == "A2":
        bank = [
            (f"Kannst du mir {a} {word} erklären?", f"你可以跟我解釋{zh}嗎？"),
            (f"Wir haben {de_sc} über {a} {word} gesprochen.", f"我們{zh_sc}談到了{zh}。"),
            (f"{name} sucht Informationen zu {d} {word}.", f"{name}在找關於{zh}的資料。"),
            (f"Mit {d} {word} wird alles klarer.", f"有了{zh}，一切比較清楚。"),
            (f"Warum ist {art} {word} so wichtig?", f"為什麼{zh}這麼重要？"),
            (f"Ich lese einen Text über {a} {word}.", f"我在讀關於{zh}的文章。"),
            (f"Vergiss {a} {word} morgen nicht!", f"明天別忘了{zh}！"),
            (f"{de_sc[:1].upper() + de_sc[1:]} geht es um {a} {word}.", f"{zh_sc}的主題是{zh}。"),
            (f"Ohne {a} {word} fehlt der Zusammenhang.", f"沒有{zh}就缺少脈絡。"),
            (f"{Art} {word} steht im Text.", f"課文裡有{zh}。"),
            (f"Sie fragt nach {d} {word}.", f"她問起{zh}。"),
            (f"Ich habe {a} {word} noch nicht verstanden.", f"我還沒理解{zh}。"),
            (f"{name} zeigt uns ein Beispiel zu {d} {word}.", f"{name}舉了一個關於{zh}的例子。"),
            (f"Bitte wiederhole {a} {word}!", f"請重複一次「{zh}」！"),
            (f"Zum Glück kennen wir {a} {word}.", f"幸好我們認識{zh}。"),
        ]
    elif level == "B1":
        bank = [
            (f"{Art} {word} spielt in diesem Thema eine große Rolle.", f"{zh}在這個主題裡很關鍵。"),
            (f"Ich habe {a} {word} erst gestern verstanden.", f"我昨天才理解「{zh}」。"),
            (f"{name} spricht oft über {a} {word}.", f"{name}常談到{zh}。"),
            (f"Könnten Sie mir {a} {word} kurz erklären?", f"可以請您簡短說明「{zh}」嗎？"),
            (f"Wegen {d} {word} haben wir den Plan geändert.", f"因為{zh}，我們改了計畫。"),
            (f"Der Bericht erwähnt {a} {word} mehrmals.", f"報告多次提到{zh}。"),
            (f"Wir diskutieren heute über {a} {word}.", f"我們今天討論{zh}。"),
            (f"{Art} {word} war diesmal entscheidend.", f"這次{zh}起了決定作用。"),
            (f"Ohne {a} {word} kommen wir nicht weiter.", f"沒有{zh}我們無法推進。"),
            (f"Je klarer {art} {word}, desto besser die Entscheidung.", f"{zh}越清楚，決定越好。"),
            (f"Man sollte {a} {word} nicht unterschätzen.", f"不應低估{zh}。"),
            (f"{name} notiert alles zu {d} {word}.", f"{name}把關於{zh}的重點都記下來。"),
            (f"Im Kurs behandeln wir {a} {word}.", f"課堂上我們會談到{zh}。"),
            (f"Ein Beispiel hilft, {a} {word} zu verstehen.", f"舉例有助於理解{zh}。"),
            (f"Die Frage nach {d} {word} bleibt offen.", f"關於{zh}的問題仍未解決。"),
        ]
    elif level == "B2":
        bank = [
            (f"Im Hinblick auf {a} {word} bleiben Fragen offen.", f"就「{zh}」而言，仍有問題未解。"),
            (f"{Art} {word} beeinflusst unsere Strategie.", f"{zh}影響我們的策略。"),
            (f"Fachleute bewerten {a} {word} unterschiedlich.", f"專家對「{zh}」評價不一。"),
            (f"Erst mit {d} {word} wird der Vorschlag tragfähig.", f"有了{zh}，提案才站得住。"),
            (f"{name} hat {a} {word} in einem Artikel analysiert.", f"{name}在文章裡分析了{zh}。"),
            (f"Die Debatte dreht sich um {a} {word}.", f"辯論圍繞「{zh}」展開。"),
            (f"Man unterschätzt leicht {a} {word}.", f"人們容易低估{zh}。"),
            (f"Wir müssen {a} {word} sorgfältiger prüfen.", f"我們必須更仔細檢視{zh}。"),
            (f"{Art} {word} steht im Zentrum der Kritik.", f"{zh}處於批評的中心。"),
            (f"Der Text verknüpft {a} {word} mit aktuellen Daten.", f"文本把{zh}與最新數據連結。"),
            (f"Ohne Bezug auf {a} {word} bleibt die These schwach.", f"若不涉及{zh}，論點偏弱。"),
            (f"Aktuell rückt {art} {word} wieder in den Fokus.", f"目前{zh}再次成為焦點。"),
            (f"Die Studie nimmt {a} {word} genauer unter die Lupe.", f"研究更仔細檢視了{zh}。"),
            (f"Zwischen den Positionen vermittelt {art} {word}.", f"{zh}在各立場之間居間協調。"),
            (f"Kritiker fordern Klarheit bei {d} {word}.", f"批評者要求在{zh}上說清楚。"),
        ]
    else:
        bank = [
            (f"In der Forschung gilt {art} {word} als zentraler Begriff.", f"在研究中，「{zh}」被視為核心概念。"),
            (f"Kritiker hinterfragen {a} {word} grundsätzlich.", f"批評者從根本上質疑「{zh}」。"),
            (f"{name} stellt {a} {word} in einen neuen Kontext.", f"{name}把「{zh}」放進新脈絡。"),
            (f"Der Text entfaltet {a} {word} mit großer Präzision.", f"文本極精確地展開「{zh}」。"),
            (f"Man sollte {a} {word} nicht isoliert interpretieren.", f"不應孤立地詮釋「{zh}」。"),
            (f"Zwischen Theorie und Praxis vermittelt {art} {word}.", f"「{zh}」在理論與實踐之間搭橋。"),
            (f"Die Relevanz von {d} {word} wird oft unterschätzt.", f"「{zh}」的重要性常被低估。"),
            (f"Eine differenzierte Sicht auf {a} {word} ist nötig.", f"必須對「{zh}」做細緻檢視。"),
            (f"Angesichts {d} {word} erscheint die These fragil.", f"鑑於「{zh}」，該論點顯得脆弱。"),
            (f"Nicht {art} {word} an sich, sondern die Wirkung zählt.", f"重要的不是「{zh}」本身，而是其效應。"),
            (f"Der Vortrag ordnet {a} {word} historisch ein.", f"演講把「{zh}」放入歷史脈絡。"),
            (f"In Fachkreisen wird {art} {word} neu verhandelt.", f"在專業圈裡，「{zh}」被重新討論。"),
            (f"Der Essay kontrastiert {a} {word} mit älteren Modellen.", f"這篇文章把「{zh}」與舊模型對照。"),
            (f"Eine vorschnelle Deutung von {d} {word} greift zu kurz.", f"對「{zh}」倉促詮釋會失之偏頗。"),
            (f"Hier erweist sich {art} {word} als Schlüsselkategorie.", f"在此「{zh}」成了關鍵範疇。"),
        ]
    return bank[seed % len(bank)]


def verb_example(w: dict, seed: int) -> tuple[str, str]:
    word = w["word"]
    zh = w["translation"].split("／")[0].split("/")[0].strip()
    level = w["level"]
    de_sc, zh_sc = scene_pair("動詞", seed, 1)
    name = pick(NAMES, seed, 2)
    adv_de, adv_zh = pick(
        [
            ("ruhig", "安靜地"),
            ("schnell", "快點"),
            ("gemeinsam", "一起"),
            ("sorgfältig", "仔細地"),
            ("bald", "盡快"),
            ("lieber", "最好"),
            ("kurz", "簡短地"),
            ("noch heute", "今天就"),
        ],
        seed,
        3,
    )

    if level in ("A1", "A2"):
        bank = [
            (f"Kannst du {de_sc} {word}?", f"你能{zh_sc}{zh}嗎？"),
            (f"Ich möchte {word}.", f"我想要{zh}。"),
            (f"Wir müssen {adv_de} {word}.", f"我們必須{adv_zh}{zh}。"),
            (f"{name} will nicht {word}.", f"{name}不想{zh}。"),
            (f"Darf ich hier {word}?", f"我可以在這裡{zh}嗎？"),
            (f"Lass uns {word}!", f"我們一起{zh}吧！"),
            (f"Warum soll ich {word}?", f"我為什麼該{zh}？"),
            (f"Er lernt, zu {word}.", f"他在學如何{zh}。"),
            (f"Könnten Sie bitte {word}?", f"可以請您{zh}嗎？"),
            (f"Ohne Hilfe kann ich nicht {word}.", f"沒有幫助我無法{zh}。"),
            (f"Wann können wir {word}?", f"我們什麼時候可以{zh}？"),
            (f"Ich versuche zu {word}.", f"我試著{zh}。"),
        ]
    elif level == "B1":
        bank = [
            (f"Es ist wichtig, rechtzeitig zu {word}.", f"及時{zh}很重要。"),
            (f"Er hat gestern versucht zu {word}.", f"他昨天試著{zh}。"),
            (f"Wir planen, nächste Woche zu {word}.", f"我們計畫下週{zh}。"),
            (f"Statt zu {word}, wartet sie ab.", f"她不立刻{zh}，而是先觀望。"),
            (f"Ich habe keine Lust mehr zu {word}.", f"我沒興致再{zh}了。"),
            (f"{name} schlägt vor, gemeinsam zu {word}.", f"{name}建議一起{zh}。"),
            (f"Bevor wir entscheiden, sollten wir {word}.", f"決定前我們應該先{zh}。"),
            (f"Das Ziel ist es, besser zu {word}.", f"目標是更好地{zh}。"),
            (f"Ohne Druck lässt sich leichter {word}.", f"沒有壓力時比較容易{zh}。"),
            (f"Man darf nicht vergessen zu {word}.", f"不該忘記要{zh}。"),
            (f"Sie hat aufgehört zu {word}.", f"她已停止{zh}。"),
            (f"Es fällt mir schwer zu {word}.", f"對我來說很難{zh}。"),
        ]
    else:
        bank = [
            (f"Es gilt, strategisch zu {word}.", f"關鍵在於有策略地{zh}。"),
            (f"Die Fähigkeit zu {word} unterscheidet die Kandidaten.", f"能否{zh}區分了候選人。"),
            (f"Kritiker fordern, transparenter zu {word}.", f"批評者要求更透明地{zh}。"),
            (f"Erst wer gelernt hat zu {word}, versteht den Prozess.", f"學會{zh}的人才懂這個過程。"),
            (f"Der Versuch zu {word} scheiterte zunächst.", f"試圖{zh}一開始失敗了。"),
            (f"Man sollte abwägen, ob man jetzt {word} sollte.", f"應衡量此刻是否該{zh}。"),
            (f"Anstatt impulsiv zu handeln, empfiehlt es sich zu {word}.", f"與其衝動行事，不如{zh}。"),
            (f"{name} weigert sich kategorisch zu {word}.", f"{name}斷然拒絕{zh}。"),
            (f"Ohne Vorbereitung zu {word} wäre riskant.", f"沒準備就{zh}會有風險。"),
            (f"Der Auftrag besteht darin zu {word}.", f"任務在於{zh}。"),
            (f"Sie zögert noch zu {word}.", f"她仍猶豫是否要{zh}。"),
            (f"Nur wer übt, kann souverän {word}.", f"唯有練習，才能自在地{zh}。"),
        ]
    return bank[seed % len(bank)]


def adj_example(w: dict, seed: int) -> tuple[str, str]:
    word = w["word"]
    zh = w["translation"].split("／")[0].split("/")[0].strip()
    level = w["level"]
    name = pick(NAMES, seed, 1)
    subj = pick(
        [
            ("Das Ergebnis", "結果"),
            ("Die Lösung", "解法"),
            ("Der Plan", "計畫"),
            ("Das Wetter", "天氣"),
            ("Die Situation", "情況"),
            ("Der Kurs", "課程"),
            ("Der Film", "電影"),
            ("Die Idee", "想法"),
        ],
        seed,
        2,
    )
    s_de, s_zh = subj

    if level in ("A1", "A2"):
        bank = [
            (f"{s_de} ist {word}.", f"{s_zh}很{zh}。"),
            (f"Heute fühle ich mich {word}.", f"今天我覺得{zh}。"),
            (f"Das klingt {word}.", f"這聽起來很{zh}。"),
            (f"{name} findet das {word}.", f"{name}覺得這很{zh}。"),
            (f"Warum ist das so {word}?", f"為什麼這這麼{zh}？"),
            (f"Bitte sei nicht zu {word}.", f"請不要太{zh}。"),
            (f"Das bleibt {word}.", f"這仍然很{zh}。"),
            (f"Für mich ist das {word} genug.", f"對我來說這已經夠{zh}。"),
            (f"Wirklich {word}!", f"真的很{zh}！"),
            (f"Ist der Tee noch {word}?", f"茶還{zh}嗎？"),
            (f"{name} wirkt heute {word}.", f"{name}今天看起來很{zh}。"),
            (f"Das Zimmer ist ziemlich {word}.", f"房間相當{zh}。"),
        ]
    elif level == "B1":
        bank = [
            (f"{s_de} wirkt überraschend {word}.", f"{s_zh}顯得意外地{zh}。"),
            (f"Man sollte ehrlich sagen, dass es {word} ist.", f"應誠實說這很{zh}。"),
            (f"{name} hält den Vorschlag für {word}.", f"{name}認為這提議很{zh}。"),
            (f"Trotz allem bleibt die Lage {word}.", f"儘管如此情勢仍{zh}。"),
            (f"Das Argument klingt wenig {word}.", f"這論點聽起來不太{zh}。"),
            (f"Ob das {word} genug ist, ist unklar.", f"這是否夠{zh}仍不清楚。"),
            (f"Verglichen mit gestern ist alles {word}er.", f"跟昨天比，一切更{zh}。"),
            (f"Wir brauchen eine Antwort, die {word} ist.", f"我們需要一個{zh}的答覆。"),
            (f"Der Ton war diesmal zu {word}.", f"這次語氣太{zh}了。"),
            (f"{s_de} bleibt erstaunlich {word}.", f"{s_zh}出奇地{zh}。"),
            (f"Nicht jeder findet das {word}.", f"不是每個人都覺得這{zh}。"),
            (f"Je {word}er, desto besser für uns.", f"越{zh}對我們越好。"),
        ]
    else:
        bank = [
            (f"Die Einschätzung bleibt bewusst {word}.", f"評估刻意保持{zh}。"),
            (f"Kritiker nennen den Ansatz zu {word}.", f"批評者認為這做法過於{zh}。"),
            (f"Die Rhetorik wirkt absichtlich {word}.", f"修辭顯得刻意{zh}。"),
            (f"{name} formuliert die These bewusst {word}.", f"{name}刻意把論點寫得{zh}。"),
            (f"Nicht alles, was {word} wirkt, ist es auch.", f"不是所有顯得{zh}的事物真是如此。"),
            (f"Der Ton der Debatte wurde zunehmend {word}.", f"辯論語氣越來越{zh}。"),
            (f"Das Urteil fällt erstaunlich {word} aus.", f"判斷出奇地{zh}。"),
            (f"Eine Lesart, die {word} bleibt, öffnet Perspektiven.", f"保持{zh}的讀法能開啟視角。"),
            (f"Zwischen den Polen erscheint nichts {word}.", f"兩極之間顯得毫不{zh}。"),
            (f"Der Befund ist methodisch {word}.", f"這發現在方法上相當{zh}。"),
            (f"Seine Kritik bleibt pointiert und {word}.", f"他的批評尖銳且{zh}。"),
            (f"Ob der Stil {word} wirkt, hängt vom Publikum ab.", f"風格是否顯得{zh}，取決於受眾。"),
        ]
    return bank[seed % len(bank)]


def other_example(w: dict, seed: int) -> tuple[str, str]:
    word = w["word"]
    zh = w["translation"].split("／")[0].split("/")[0].strip()
    name = pick(NAMES, seed, 1)
    bank = [
        (f"Was bedeutet „{word}“ genau?", f"「{word}」精確是什麼意思？（{zh}）"),
        (f"{name} benutzt oft das Wort „{word}“.", f"{name}常使用「{word}」（{zh}）這個詞。"),
        (f"Schreib bitte „{word}“ noch einmal.", f"請再寫一次「{word}」（{zh}）。"),
        (f"Ohne „{word}“ verstehe ich den Satz nicht.", f"沒有「{word}」（{zh}）我聽不懂這句。"),
        (f"Merke dir: {word} = {zh}.", f"記住：{word}＝{zh}。"),
        (f"Im Dialog fällt das Wort „{word}“.", f"對話裡出現了「{word}」（{zh}）。"),
        (f"Erklärt mir jemand „{word}“?", f"誰能解釋「{word}」（{zh}）？"),
        (f"„{word}“ hört man hier häufig.", f"這裡常聽到「{word}」（{zh}）。"),
        (f"Bitte übersetze „{word}“.", f"請翻譯「{word}」（{zh}）。"),
        (f"Ich notiere mir „{word}“.", f"我把「{word}」（{zh}）記下來。"),
    ]
    return bank[seed % len(bank)]


def make_example(w: dict, index: int = 0) -> tuple[str, str]:
    # Primary: rotate by list index so neighbors never share the same frame
    base = index * 3
    scramble = hmix(w["id"] + w["word"] + w["translation"] + w["level"])
    seed = (base + scramble) & 0xFFFFFFFF
    cat = w["category"]
    if w.get("article"):
        return noun_example(w, seed)
    if cat == "動詞":
        return verb_example(w, seed)
    if cat == "形容詞":
        return adj_example(w, seed)
    return other_example(w, seed)


def uniquify(entries: list[dict]) -> int:
    seen: dict[str, int] = {}
    fixed = 0
    for w in entries:
        de = w["example"]
        if de not in seen:
            seen[de] = 0
            continue
        seen[de] += 1
        n = seen[de]
        name = pick(NAMES, hmix(w["id"]), n)
        # appendix that keeps natural German
        if de.endswith((".", "!", "?")):
            de2 = f"{de[:-1]} — sagt {name}{de[-1]}"
        else:
            de2 = f"{de} — sagt {name}."
        # absolute fallback
        guard = 0
        while de2 in seen and guard < 20:
            guard += 1
            de2 = f"{de} ({w['id'][:12]}-{guard})"
        w["example"] = de2
        if "（補充）" not in w["exampleTranslation"]:
            w["exampleTranslation"] = w["exampleTranslation"] + f"（{name}這麼說）"
        seen[de2] = 0
        fixed += 1
    return fixed


def main() -> None:
    data = json.loads(PATH.read_text(encoding="utf-8"))
    for i, w in enumerate(data):
        de, zh = make_example(w, i)
        w["example"] = de
        w["exampleTranslation"] = zh

    fixed = uniquify(data)
    examples = [w["example"] for w in data]
    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    print(
        f"total={len(data)} unique={len(set(examples))} "
        f"collision_fixes={fixed} bytes={PATH.stat().st_size}"
    )
    # pattern diversity
    from collections import Counter
    starts = Counter(e.split()[0] for e in examples)
    print("top sentence starts:", starts.most_common(8))
    for lv in ["A1", "A2", "B1", "B2", "C1"]:
        print(f"\n== {lv}")
        for w in [x for x in data if x["level"] == lv][:4]:
            print(f"  {w.get('article') or '-'} {w['word']}")
            print(f"    DE: {w['example']}")
            print(f"    ZH: {w['exampleTranslation']}")


if __name__ == "__main__":
    main()
