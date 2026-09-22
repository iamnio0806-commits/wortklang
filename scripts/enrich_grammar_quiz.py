#!/usr/bin/env python3
"""Enrich grammar.json with beginner tips + MCQ/fill exercises per topic."""
from __future__ import annotations

import json
import re
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "src" / "data" / "grammar.json"

BEGINNER_TIPS = {
    "發音與基礎": [
        "初學者：先跟著朗讀，不要急著一次記完所有規則。",
        "聽到不會的音就重播 2～3 次，嘴巴跟著動。",
    ],
    "冠詞與名詞": [
        "初學者鐵律：每個名詞都要連 der／die／das 一起背。",
        "先背高頻名詞的冠詞，再慢慢補例外。",
        "複數定冠詞一律是 die，可先記這個不變的點。",
    ],
    "代詞": [
        "把 ich/du/er 跟動詞變化綁在一起背，比較不容易忘。",
        "Sie（您）要大寫；跟 sie（她／他們）靠上下文分辨。",
    ],
    "動詞現在時": [
        "陳述句：變位動詞固定在第二位——先數位置再寫句子。",
        "先熟 ich／du／er 三種，再說 wir／ihr／sie。",
        "看到可分動詞（auf-/an-…），記得前綴常跑到句末。",
    ],
    "語序與句型": [
        "是非問句：動詞開頭；W 問句：疑問詞開頭、動詞第二。",
        "把短句唸順，比一次寫長句更有效。",
    ],
    "否定": [
        "kein 用來否定「一個／某個名詞」；nicht 否定動詞或形容詞。",
        "不要說 nicht ein Auto，要說 kein Auto。",
    ],
    "格變": [
        "先問：這個名詞是「誰做」（主格）還是「承受動作」（第四格）？",
        "陽性變化最明顯：der→den（第四格）、dem（第三格）。",
        "先練「我看到 den Mann」這種短句。",
    ],
    "情態動詞": [
        "情態動詞要變位，後面的主要動詞用原形放句末。",
        "Ich kann schwimmen（✓）不是 Ich kann schwimme。",
    ],
    "數字與時間": [
        "問時間：Wie spät ist es?；先會說 … Uhr 就夠用。",
        "星期用 am（am Montag），月份用 im（im Mai）。",
    ],
    "介詞": [
        "先背「介詞＋哪一格」的固定搭配，不要分開記。",
        "分清 wo（在哪裡）跟 wohin（去哪裡）。",
    ],
    "形容詞": [
        "放在 sein 後面當表語時，形容詞通常不加字尾。",
        "修飾名詞時才要加字尾，A1 可先少用長名詞片語。",
    ],
    "連接詞與從句": [
        "看到 weil／dass：從句的動詞要走到句末。",
        "先寫兩個短句，再練習用 weil 接起來。",
    ],
    "動詞時態": [
        "口語談過去多用 Perfekt：haben／sein + 過去分詞。",
        "分詞多半在句末；先找助動詞再找分詞。",
    ],
    "被動語態": [
        "被動看 werden／wurde + 過去分詞。",
        "先會讀「Das Fenster wird geöffnet」再學自己寫。",
    ],
    "虛擬式": [
        "禮貌請求常用 könnte／würde／hätte。",
        "點餐：Ich hätte gern… 非常實用。",
    ],
    "不定式與分詞": [
        "看到 zu + 動詞，想想前面是「想／試／重要…」這類結構。",
        "可分動詞：aufstehen → aufzustehen（zu 插在中間）。",
    ],
    "其他結構": [
        "先理解意思與語氣，再模仿例句改寫成自己的句子。",
        "正式書面用詞可先會認，口語不必一次全用上。",
    ],
}

GENERAL_A12 = [
    "看完重點後先做下面的選擇題，不會就點「提示」。",
    "填空題大小寫要正確；不確定時先看提示再作答。",
]


def merge_tips(topic: dict) -> list[str]:
    tips = list(topic.get("tips") or [])
    cat = topic["category"]
    level = topic["level"]
    extras = list(BEGINNER_TIPS.get(cat, []))
    if level in ("A1", "A2"):
        extras = extras + list(GENERAL_A12)
        if "第二位" in topic["summary"] or "動詞第二" in "".join(topic["points"]):
            extras.append("可用手指點句子位置：①第一位 ②動詞 ③其他。")
        if "冠詞" in topic["title"] or "Artikel" in topic["titleDe"]:
            extras.append("顏色記憶：der 藍、die 紅、das 綠。")
    for t in extras:
        if t not in tips:
            tips.append(t)
    seen: set[str] = set()
    out: list[str] = []
    for t in tips:
        if t not in seen:
            seen.add(t)
            out.append(t)
    if level in ("A1", "A2"):
        return out[:5] if out else list(GENERAL_A12)
    return out[:3] if out else ["先讀例句，再對照重點規則。", "做題時可隨時點提示。"]


def norm_answer(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip())


def mcq(eid: str, prompt: str, options: list[str], answer: str, hint: str) -> dict:
    opts = []
    for o in options:
        o = o.strip()
        if o and o not in opts and o not in ("—", "-"):
            opts.append(o)
    if answer not in opts:
        opts.insert(0, answer)
    # pad distractors
    for d in ["der", "die", "das", "den", "dem", "bin", "ist", "hat", "war", "nicht", "kein"]:
        if len(opts) >= 4:
            break
        if d not in opts:
            opts.append(d)
    opts = opts[:4]
    if answer not in opts:
        opts[-1] = answer
    return {
        "id": eid,
        "type": "mcq",
        "prompt": prompt,
        "options": opts,
        "answer": answer,
        "hint": hint,
    }


def fill(
    eid: str,
    prompt: str,
    answer: str,
    hint: str,
    accept: list[str] | None = None,
) -> dict:
    ans = norm_answer(answer)
    acc = [norm_answer(a) for a in (accept or [ans])]
    if ans not in acc:
        acc.insert(0, ans)
    return {
        "id": eid,
        "type": "fill",
        "prompt": prompt,
        "answer": ans,
        "accept": acc,
        "hint": hint,
    }


# Topic-specific high-quality quizzes
SPECIFIC: dict[str, list[dict]] = {}


def S(tid: str, items: list[dict]) -> None:
    SPECIFIC[tid] = items


S(
    "a1-articles-nom",
    [
        mcq("a1-art-1", "陽性「男士」的定冠詞是？", ["der", "die", "das", "den"], "der", "陽性主格定冠詞是 der（藍色）。"),
        mcq("a1-art-2", "陰性「女士」的定冠詞是？", ["die", "der", "das", "den"], "die", "陰性主格定冠詞是 die（紅色）。"),
        mcq("a1-art-3", "中性「孩子 Kind」的定冠詞是？", ["das", "der", "die", "dem"], "das", "das Kind：中性用 das（綠色）。"),
        fill("a1-art-4", "填空：___ Mann kommt.（那位男士來了）", "Der", "句首大寫；陽性主格 der。", ["Der", "der"]),
        fill("a1-art-5", "填空：不定冠詞陰性：___ Frau", "eine", "陰性不定冠詞是 eine。"),
    ],
)

S(
    "a1-sein-haben",
    [
        mcq("a1-sh-1", "ich + sein = ?", ["bin", "bist", "ist", "habe"], "bin", "ich bin。"),
        mcq("a1-sh-2", "er + haben = ?", ["hat", "habe", "hast", "ist"], "hat", "er/sie/es hat。"),
        mcq("a1-sh-3", "「我累了」怎麼說？", ["Ich bin müde.", "Ich habe müde.", "Ich ist müde.", "Ich bist müde."], "Ich bin müde.", "狀態用 sein。"),
        fill("a1-sh-4", "填空：Du ___ (sein) nett.", "bist", "du → bist。"),
        fill("a1-sh-5", "填空：Wir ___ (haben) Zeit.", "haben", "wir haben。"),
    ],
)

S(
    "a1-word-order",
    [
        mcq("a1-wo-1", "陳述句裡，變位動詞在第幾位？", ["第二位", "第一位", "最後一位", "第三位"], "第二位", "德文鐵律：動詞第二位。"),
        mcq("a1-wo-2", "哪句正確？", ["Heute gehe ich ins Kino.", "Heute ich gehe ins Kino.", "Gehe heute ich ins Kino.", "Ich heute gehe ins Kino."], "Heute gehe ich ins Kino.", "時間提前時，動詞仍第二，主語在後。"),
        mcq("a1-wo-3", "Ich ___ heute Deutsch.（lernen）", ["lerne", "lernen", "lernst", "lernt"], "lerne", "ich lerne；動詞在第二位。"),
        fill("a1-wo-4", "把動詞放對：Heute ___ ich Deutsch.（lernen 變位）", "lerne", "Heute(1) lerne(2) ich…"),
        fill("a1-wo-5", "填空：In Berlin ___ ich.（wohnen 變位，ich）", "wohne", "地點提前，動詞仍第二：wohne。"),
    ],
)

S(
    "a1-accusative",
    [
        mcq("a1-akk-1", "陽性定冠詞第四格是？", ["den", "der", "dem", "das"], "den", "der → den（第四格）。"),
        mcq("a1-akk-2", "Ich sehe ___ Mann.", ["den", "der", "dem", "des"], "den", "sehen 接第四格。"),
        mcq("a1-akk-3", "陰性第四格定冠詞？", ["die", "der", "den", "das"], "die", "陰性第四格仍是 die。"),
        fill("a1-akk-4", "填空：Hast du ___ Buch?（das 的第四格）", "das", "中性第四格仍是 das。"),
        fill("a1-akk-5", "填空：Wir brauchen ___ Tisch.（ein 陽性第四格）", "einen", "陽性不定冠詞第四格：einen。"),
    ],
)

S(
    "a1-negation",
    [
        mcq("a1-neg-1", "「我沒有車」正確說法？", ["Ich habe kein Auto.", "Ich habe nicht ein Auto.", "Ich habe nicht Auto.", "Ich habe keine Auto."], "Ich habe kein Auto.", "否定名詞用 kein，不是 nicht ein。"),
        mcq("a1-neg-2", "否定形容詞常用？", ["nicht", "kein", "ohne", "nie"], "nicht", "Das ist nicht teuer。"),
        mcq("a1-neg-3", "Ich trinke ___ Kaffee.（否定）", ["keinen", "nicht", "kein", "keine"], "keinen", "陽性第四格：keinen。"),
        fill("a1-neg-4", "填空：Er kommt heute ___.（他不來）", "nicht", "否定動詞／整句常用 nicht。"),
        fill("a1-neg-5", "填空：Wir haben ___ Zeit.", "keine", "Zeit 陰性 → keine。"),
    ],
)

S(
    "a1-questions",
    [
        mcq("a1-q-1", "是非問句通常怎麼開始？", ["動詞開頭", "主語開頭", "問號開頭", "nicht 開頭"], "動詞開頭", "Kommst du mit?"),
        mcq("a1-q-2", "問「在哪裡」用？", ["wo", "wohin", "woher", "wann"], "wo", "wo＝在哪；wohin＝去哪。"),
        mcq("a1-q-3", "問名字：___ heißt du?", ["Wie", "Was", "Wo", "Wer"], "Wie", "Wie heißt du?"),
        fill("a1-q-4", "填空：___ wohnst du?（在哪裡）", "Wo", "Wo＝位置。", ["Wo", "wo"]),
        fill("a1-q-5", "填空：___ gehst du?（去哪裡）", "Wohin", "Wohin＝方向。", ["Wohin", "wohin"]),
    ],
)

S(
    "a1-prasens-regular",
    [
        mcq("a1-pr-1", "du + lernen = ?", ["lernst", "lerne", "lernt", "lernen"], "lernst", "du 加 -st。"),
        mcq("a1-pr-2", "er + wohnen = ?", ["wohnt", "wohne", "wohnst", "wohnen"], "wohnt", "er/sie/es 加 -t。"),
        mcq("a1-pr-3", "wir + spielen = ?", ["spielen", "spielt", "spiele", "spielst"], "spielen", "wir 與不定式相同。"),
        fill("a1-pr-4", "填空：Ich ___ Deutsch.（lernen）", "lerne", "ich → -e。"),
        fill("a1-pr-5", "填空：Ihr ___ viel.（arbeiten）", "arbeitet", "字幹 -t 時加 e：arbeitet。", ["arbeitet"]),
    ],
)

S(
    "a1-modal-basic",
    [
        mcq("a1-mo-1", "情態動詞後面的主要動詞要用？", ["原形（不定式）放句末", "一樣變位", "過去分詞", "去掉字尾"], "原形（不定式）放句末", "Ich kann schwimmen。"),
        mcq("a1-mo-2", "ich + können = ?", ["kann", "können", "kannst", "könnt"], "kann", "情態單數常變母音。"),
        mcq("a1-mo-3", "禮貌「想要」常用？", ["möchten", "müssen", "dürfen", "sollen"], "möchten", "Ich möchte einen Kaffee。"),
        fill("a1-mo-4", "填空：Ich ___ Deutsch sprechen.（können）", "kann", "ich kann。"),
        fill("a1-mo-5", "填空：Wir müssen ___.（走：gehen）", "gehen", "主要動詞原形在句末。"),
    ],
)

S(
    "a2-dative",
    [
        mcq("a2-dat-1", "陽性定冠詞第三格是？", ["dem", "den", "der", "das"], "dem", "der → dem。"),
        mcq("a2-dat-2", "Ich helfe ___ Mann.", ["dem", "den", "der", "das"], "dem", "helfen 接第三格。"),
        mcq("a2-dat-3", "陰性第三格定冠詞？", ["der", "die", "dem", "den"], "der", "die → der（第三格）。"),
        fill("a2-dat-4", "填空：Das gehört ___ Frau.（定冠詞）", "der", "gehören + 第三格；陰性 der。"),
        fill("a2-dat-5", "填空：Das gefällt ___.（我：第三格代詞）", "mir", "mir = 我（第三格）。"),
    ],
)

S(
    "a2-perfekt",
    [
        mcq("a2-pf-1", "口語過去常用哪個時態？", ["Perfekt", "Futur", "只有 Präsens", "只有 Genitiv"], "Perfekt", "haben/sein + 過去分詞。"),
        mcq("a2-pf-2", "gehen 的完成時助動詞多用？", ["sein", "haben", "werden", "können"], "sein", "位移動詞常用 sein。"),
        mcq("a2-pf-3", "machen 的過去分詞？", ["gemacht", "gemachen", "macht", "gemachtet"], "gemacht", "ge- + 字幹 + -t。"),
        fill("a2-pf-4", "填空：Ich ___ gearbeitet.（助動詞）", "habe", "多數動詞用 haben。"),
        fill("a2-pf-5", "填空：Sie ist nach Hause ___.（gehen 分詞）", "gegangen", "強變化：gegangen。"),
    ],
)

S(
    "a2-weil-dass",
    [
        mcq("a2-wd-1", "weil 從句裡，變位動詞在哪？", ["句末", "第二位", "開頭", "可省略"], "句末", "從屬從句：動詞到句末。"),
        mcq("a2-wd-2", "哪句正確？", ["…, weil ich krank bin.", "…, weil ich bin krank.", "…, weil bin ich krank.", "…, weil krank ich bin."], "…, weil ich krank bin.", "weil 從句動詞在末。"),
        mcq("a2-wd-3", "引導「我相信…」常用？", ["dass", "weil", "aber", "oder"], "dass", "Ich glaube, dass…"),
        fill("a2-wd-4", "填空：Ich bleibe zu Hause, weil ich krank ___.（sein）", "bin", "從句動詞在末：bin。"),
        fill("a2-wd-5", "填空：Sie sagt, ___ sie keine Zeit hat.", "dass", "dass＝「那／說…」。"),
    ],
)

S(
    "a2-two-way-prep",
    [
        mcq("a2-tw-1", "問 wo（位置）時，兩用介詞接？", ["第三格", "第四格", "第二格", "不變"], "第三格", "位置→Dativ。"),
        mcq("a2-tw-2", "問 wohin（方向）時接？", ["第四格", "第三格", "主格", "第二格"], "第四格", "方向→Akkusativ。"),
        mcq("a2-tw-3", "Ich bin ___ Zimmer.（in + dem）", ["im", "ins", "am", "ans"], "im", "in dem → im。"),
        fill("a2-tw-4", "填空：Wir gehen ___ Kino.（in + das）", "ins", "in das → ins。"),
        fill("a2-tw-5", "填空：Das Buch liegt auf ___ Tisch.（dem/den？位置）", "dem", "位置用第三格 dem。"),
    ],
)

S(
    "b1-passive",
    [
        mcq("b1-pa-1", "過程被動的基本結構？", ["werden + Partizip II", "sein + zu", "haben + Infinitiv", "nur Partizip"], "werden + Partizip II", "Das Fenster wird geöffnet。"),
        mcq("b1-pa-2", "過去被動常用？", ["wurde gemacht", "wird gemacht", "ist machen", "war machen"], "wurde gemacht", "wurde + 分詞。"),
        mcq("b1-pa-3", "情態＋被動句末是？", ["werden", "worden", "geworden", "wird"], "werden", "muss gemacht werden。"),
        fill("b1-pa-4", "填空：Das Haus ___ gebaut.（現在被動助動詞）", "wird", "wird + 分詞。"),
        fill("b1-pa-5", "填空：Hier darf nicht geraucht ___.", "werden", "情態＋被動：… werden。"),
    ],
)

S(
    "b1-relative",
    [
        mcq("b1-re-1", "陽性主格關係代詞？", ["der", "den", "dem", "dessen"], "der", "與定冠詞同形。"),
        mcq("b1-re-2", "陽性第四格關係代詞？", ["den", "der", "dem", "die"], "den", "…, den ich sehe。"),
        mcq("b1-re-3", "關係從句動詞在？", ["句末", "第二位", "開頭", "可省略"], "句末", "關係從句也是從句。"),
        fill("b1-re-4", "填空：Das ist die Frau, ___ nebenan wohnt.", "die", "陰性主格 die。"),
        fill("b1-re-5", "填空：Der Mann, ___ ich gedankt habe, ist Lehrer.（第三格）", "dem", "danken + Dativ → dem。"),
    ],
)

S(
    "b1-konjunktiv2-basic",
    [
        mcq("b1-k2-1", "禮貌請求常用？", ["Könnten Sie…?", "Kannst du mussen?", "Du musst sofort!", "Ich will Sie!"], "Könnten Sie…?", "Konjunktiv II 表禮貌。"),
        mcq("b1-k2-2", "「我很想要咖啡」？", ["Ich hätte gern einen Kaffee.", "Ich habe gern gewesen Kaffee.", "Ich bin Kaffee.", "Ich muss Kaffee bin."], "Ich hätte gern einen Kaffee.", "hätte gern 點餐常用。"),
        mcq("b1-k2-3", "非真實條件常用？", ["würde + 不定式", "nur Perfekt", "nur Akkusativ", "nur Artikel"], "würde + 不定式", "würde kommen。"),
        fill("b1-k2-4", "填空：Ich ___ gern mitkommen.（würde）", "würde", "würde + 不定式。"),
        fill("b1-k2-5", "填空：Wenn ich Zeit ___, würde ich kommen.（haben K II）", "hätte", "hätte＝假如有。"),
    ],
)

S(
    "b2-konjunktiv1",
    [
        mcq("b2-k1-1", "Konjunktiv I 主要用於？", ["間接引語／轉述", "點餐", "問時間", "複數構成"], "間接引語／轉述", "新聞常用。"),
        mcq("b2-k1-2", "er + haben（K I）常見？", ["habe", "hat", "hätte", "hast"], "habe", "er habe…"),
        mcq("b2-k1-3", "與直陳式同形時改用？", ["Konjunktiv II", "只有被動", "刪除動詞", "改成英文"], "Konjunktiv II", "避免歧義。"),
        fill("b2-k1-4", "填空：Er sagt, er ___ keine Zeit.（haben K I）", "habe", "轉述：er habe。"),
        fill("b2-k1-5", "填空：Sie ___ zufrieden.（sein K I 複數）", "seien", "sie seien。"),
    ],
)

S(
    "c1-irony-particles",
    [
        mcq("c1-mp-1", "Modalpartikeln 主要改什麼？", ["語氣", "性別", "複數", "定冠詞顏色"], "語氣", "不改基本命題。"),
        mcq("c1-mp-2", "「你過來一下嘛」常用小品詞？", ["mal / doch", "der", "worden", "dessen"], "mal / doch", "Komm doch mal her!"),
        mcq("c1-mp-3", "halt／eben 常帶什麼語氣？", ["無奈接受", "命令被動", "第二格", "未來完成"], "無奈接受", "Dann ist es halt so。"),
        fill("c1-mp-4", "填空：Das ist ___ einfach!（顯而易見）", "ja", "Das ist ja einfach!"),
        fill("c1-mp-5", "填空：Das wird ___ gut gehen.（安撫）", "schon", "wird schon…"),
    ],
)


def from_forms(topic: dict, out: list[dict]) -> None:
    tid = topic["id"]
    for fi, form in enumerate(topic.get("forms") or []):
        headers = form.get("headers") or []
        rows = form.get("rows") or []
        if len(headers) < 2 or not rows:
            continue
        for row in rows:
            if len(row) < 2:
                continue
            label, ans = row[0].strip(), row[1].strip()
            if not ans or ans in ("—", "-"):
                continue
            col = headers[1]
            distractors = [
                r[1].strip()
                for r in rows
                if len(r) > 1 and r[1].strip() not in (ans, "—", "-", "")
            ]
            out.append(
                mcq(
                    f"{tid}-fm-{fi}",
                    f"【{form.get('label', '表格')}】{label} 的「{col}」是？",
                    [ans] + distractors,
                    ans,
                    f"看表格「{form.get('label', '')}」中 {label} 這一列。",
                )
            )
            out.append(
                fill(
                    f"{tid}-ff-{fi}",
                    f"填空：{label} → {col} = ____",
                    ans,
                    f"提示：表格「{form.get('label', '')}」。",
                )
            )
            return


def from_examples(topic: dict, out: list[dict]) -> None:
    tid = topic["id"]
    examples = topic.get("examples") or []
    if not examples:
        return
    # blank first content word after optional article
    for i, ex in enumerate(examples[:3]):
        de = ex["de"].rstrip(".")
        zh = ex["zh"]
        words = de.split()
        if len(words) < 2:
            continue
        # blank a middle word (verb-ish often index 1)
        idx = 1 if len(words) > 1 else 0
        answer = words[idx].strip(",.?!")
        if len(answer) < 2:
            continue
        blanked = words.copy()
        blanked[idx] = "____"
        prompt = f"填空（{zh}）：{' '.join(blanked)}"
        if not any(e.get("id") == f"{tid}-exf-{i}" for e in out):
            out.append(
                fill(
                    f"{tid}-exf-{i}",
                    prompt,
                    answer,
                    f"對照例句：{de}",
                    [answer, answer.lower(), answer.capitalize()],
                )
            )
        break

    # MCQ: which example matches meaning
    if len(examples) >= 2:
        correct = examples[0]
        opts = [e["de"] for e in examples[:4]]
        out.append(
            mcq(
                f"{tid}-exm-0",
                f"哪一句意思是「{correct['zh']}」？",
                opts,
                correct["de"],
                "先看中文再對德文關鍵詞。",
            )
        )


def from_points(topic: dict, out: list[dict]) -> None:
    tid = topic["id"]
    points = topic.get("points") or []
    title = topic["title"]
    if not points:
        return
    # True/false style as MCQ
    p0 = points[0]
    short = p0 if len(p0) < 60 else p0[:57] + "…"
    out.append(
        mcq(
            f"{tid}-pt-0",
            f"關於「{title}」，下列何者正確？",
            [short, "動詞永遠放在句首", "德文沒有冠詞", "名詞都不用記性別"],
            short,
            "對照本單元「重點」第一條。",
        )
    )
    if len(points) >= 2:
        p1 = points[1]
        short1 = p1 if len(p1) < 60 else p1[:57] + "…"
        out.append(
            mcq(
                f"{tid}-pt-1",
                f"「{title}」的另一個要點是？",
                [short1, "一律只用主格", "從句動詞一定在第二位", "kein 等於 und"],
                short1,
                "對照本單元「重點」第二條。",
            )
        )


def ensure_quiz(topic: dict) -> list[dict]:
    tid = topic["id"]
    if tid in SPECIFIC:
        return SPECIFIC[tid][:5]

    out: list[dict] = []
    from_forms(topic, out)
    from_examples(topic, out)
    from_points(topic, out)

    # generic fillers to guarantee 3 mcq + 2 fill
    level = topic["level"]
    title = topic["title"]
    cat = topic["category"]

    while sum(1 for e in out if e["type"] == "mcq") < 3:
        n = sum(1 for e in out if e["type"] == "mcq")
        out.append(
            mcq(
                f"{tid}-g-mcq-{n}",
                f"本單元「{title}」屬於哪個等級？",
                [level, "Z1", "X9", "D0"],
                level,
                f"標題旁的等級標籤是 {level}。",
            )
        )
        break
    while sum(1 for e in out if e["type"] == "mcq") < 3:
        n = sum(1 for e in out if e["type"] == "mcq")
        out.append(
            mcq(
                f"{tid}-g-mcq-{n}",
                f"「{title}」較接近哪個分類？",
                [cat, "數學公式", "化學元素", "地圖繪製"],
                cat,
                "看主題上方的分類標籤。",
            )
        )

    examples = topic.get("examples") or []
    while sum(1 for e in out if e["type"] == "fill") < 2:
        n = sum(1 for e in out if e["type"] == "fill")
        if examples:
            de = examples[min(n, len(examples) - 1)]["de"]
            # blank last word
            words = de.rstrip(".!?").split()
            if words:
                ans = words[-1].strip(",;")
                words[-1] = "____"
                out.append(
                    fill(
                        f"{tid}-g-fill-{n}",
                        f"填空：{' '.join(words)}",
                        ans,
                        f"完整例句：{de}",
                        [ans, ans.lower(), ans.capitalize()],
                    )
                )
                continue
        out.append(
            fill(
                f"{tid}-g-fill-{n}",
                f"填空：本單元德文標題是 ____",
                topic["titleDe"],
                "看主題德文標題。",
            )
        )

    # prefer 3 mcq + 2 fill order
    mcqs = [e for e in out if e["type"] == "mcq"][:3]
    fills = [e for e in out if e["type"] == "fill"][:2]
    # if still short mcq
    while len(mcqs) < 3:
        mcqs.append(
            mcq(
                f"{tid}-pad-mcq-{len(mcqs)}",
                f"學習「{title}」時，遇到不會的該怎做？",
                ["先看提示再作答", "略過永不複習", "刪除單字庫", "只用英文思考"],
                "先看提示再作答",
                "每個題目都有提示按鈕。",
            )
        )
    while len(fills) < 2:
        fills.append(
            fill(
                f"{tid}-pad-fill-{len(fills)}",
                f"填空：本單元中文標題是 ____",
                title,
                "看最上方標題。",
            )
        )
    return mcqs + fills


def main() -> None:
    topics = json.loads(PATH.read_text(encoding="utf-8"))
    for topic in topics:
        topic["tips"] = merge_tips(topic)
        topic["exercises"] = ensure_quiz(topic)

    PATH.write_text(json.dumps(topics, ensure_ascii=False, indent=2), encoding="utf-8")
    # stats
    tip_n = sum(len(t["tips"]) for t in topics) / len(topics)
    ex_n = sum(len(t["exercises"]) for t in topics) / len(topics)
    a12 = [t for t in topics if t["level"] in ("A1", "A2")]
    print(
        f"topics={len(topics)} avg_tips={tip_n:.1f} avg_ex={ex_n:.1f} "
        f"A12_min_tips={min(len(t['tips']) for t in a12)}"
    )


if __name__ == "__main__":
    main()
