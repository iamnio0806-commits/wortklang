#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Append 50 B2 reading items into reading.json."""
from __future__ import annotations

import json
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "src" / "data" / "reading.json"


def item(id, kind, topic, title, title_zh, text, text_zh, notes, patterns, tips, focus):
    return {
        "id": id,
        "level": "B2",
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


def pack(t):
    return item(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9], t[10])


B2 = []

RAW = [
(
"b2-01","story","社會","Die unsichtbare Arbeit zu Hause","家中看不見的勞動",
"""Viele Gespräche über Beruf und Erfolg blenden die Arbeit im Haushalt aus.
Dabei handelt es sich um Tätigkeiten, ohne die Berufstätigkeit kaum möglich wäre: Kochen, Putzen, Organisation von Terminen, emotionale Unterstützung.
Studien zeigen, dass diese Aufgaben nach wie vor ungleich verteilt sind, selbst wenn beide Partner erwerbstätig sind.
Wer das Thema anspricht, riskiert Konflikte; wer schweigt, zementiert bestehende Muster.
Sinnvoll wäre eine transparente Aufteilung, die regelmäßig überprüft wird.
Gerechtigkeit entsteht nicht von allein, sondern durch Vereinbarungen, die man auch einhält.""",
"""許多關於職業與成功的討論，忽略了家務勞動。
但其實若沒有這些工作，就業幾乎不可能：煮飯、打掃、安排行程、情感支持。
研究顯示即使雙方都就業，這些任務仍常分配不均。
誰提起這話題可能引發衝突；誰沉默則鞏固既有模式。
較合理的是透明分配，並定期檢視。
公平不會自動出現，而需要人們遵守的約定。""",
[n("blenden … aus","排除在外／忽略", "ausblenden。"),n("handelt es sich um","這指的是……"),n("nach wie vor","一如既往／仍然"),n("zementiert","鞏固／固化"),n("von allein","自行／自動地")],
[p("handelt es sich um + 第四格","定義主題","Dabei handelt es sich um ein Missverständnis."),p("Wer …, riskiert …; wer …, …","對照兩種行為","Wer fragt, lernt; wer schweigt, ratet."),p("entsteht nicht …, sondern durch …","否定自動論","Erfolg entsteht nicht von allein, sondern durch Übung.")],
["B2 論說文：定義→證據→兩難→建議。","標出所有名詞化（Tätigkeit、Aufteilung）。"],["論述","名詞化","社會"]),
(
"b2-02","email","職場","Stellungnahme zu einem Projektstopp","專案停擺聲明",
"""Sehr geehrte Damen und Herren,

hiermit nehme ich Stellung zu der Entscheidung, das Projekt „Nordlicht“ vorübergehend zu stoppen.
Zwar verstehe ich die budgetären Gründe; gleichwohl halte ich die Kommunikation für unzureichend.
Weder Team noch externe Partner wurden frühzeitig eingebunden, sodass Unsicherheit entstanden ist.
Ich schlage vor, innerhalb von zehn Tagen einen Alternativplan vorzulegen, der Meilensteine und Risiken klar benennt.
Nur so lässt sich Vertrauen wiederherstellen.

Mit freundlichen Grüßen
Dr. Elena Vogt
Projektleitung""",
"""敬啟者：

謹就「Nordlicht」專案暫時停擺之決定提出說明。
我雖理解預算理由，但仍認為溝通不足。
團隊與外部夥伴皆未及早參與，因而產生不安。
我建議於十日內提出替代計畫，清楚列出里程碑與風險。
唯有如此才能重新建立信任。

此致問候
Elena Vogt 博士
專案負責人""",
[n("nehme ich Stellung zu","就……表態／說明"),n("vorübergehend","暫時地"),n("gleichwohl","儘管如此／然而", "偏書面。"),n("unzureichend","不足的"),n("lässt sich … wiederherstellen","能夠被重建", "lassen sich + 不定式。")],
[p("hiermit nehme ich Stellung zu …","正式表態","Hiermit nehme ich Stellung zu Ihrem Schreiben."),p("Zwar …; gleichwohl …","讓步對立","Zwar teuer; gleichwohl sinnvoll."),p("Nur so lässt sich …","唯一途徑","Nur so lässt sich das Problem lösen.")],
["正式立場信：承認對方理由＋指出缺口＋具體提議。"],["正式郵件","論證","lassen sich"]),
(
"b2-03","notice","法律／規定","Hinweis zur Datenschutzgrundverordnung","個資規定提示",
"""Informationen zur Datenverarbeitung
Personenbezogene Daten werden ausschließlich zu dem Zweck verarbeitet, zu dem sie erhoben wurden.
Eine Weitergabe an Dritte erfolgt nur, sofern eine gesetzliche Pflicht besteht oder Sie eingewilligt haben.
Sie haben das Recht auf Auskunft, Berichtigung und Löschung.
Widerspruch gegen Werbung können Sie jederzeit formlos erklären.
Kontakt zur Datenschutzbeauftragten: datenschutz@beispiel.org""",
"""資料處理說明
個人資料僅就其蒐集之目的加以處理。
僅在有法律義務或您同意時，才會提供給第三方。
您有權查詢、更正與刪除。
您可隨時以非正式方式反對行銷用途。
個資保護負責人聯絡：datenschutz@beispiel.org""",
[n("Personenbezogene Daten","個人資料"),n("zu dem Zweck, zu dem …","以其被蒐集之目的", "關係子句。"),n("eingewilligt haben","已同意"),n("formlos erklären","以非正式方式聲明"),n("Datenschutzbeauftragten","個資保護負責人")],
[p("werden ausschließlich zu … verarbeitet","目的限制被動","werden nur intern genutzt"),p("erfolgt nur, sofern …","僅在……情況下發生","Die Zahlung erfolgt, sofern geliefert wurde."),p("Sie haben das Recht auf + 名詞","權利套語","Sie haben das Recht auf Widerspruch.")],
["法規公告語氣非人稱化，多被動。"],["被動","法律用語","關係句"]),
(
"b2-04","story","媒體批判","Filterblasen","同溫層",
"""Algorithmen zeigen uns vor allem Inhalte, die zu unserem bisherigen Verhalten passen.
Dadurch entsteht der Eindruck, die eigene Meinung sei gesellschaftlicher Konsens.
Wer widersprechende Perspektiven meidet, verliert die Fähigkeit, Argumente zu prüfen.
Das bedeutet nicht, dass man jeder Meinung zustimmen muss; es bedeutet, sie wenigstens zu verstehen.
Eine praktische Gegenmaßnahme ist, bewusst Quellen zu wechseln und Behauptungen zu verifizieren.
Medienkompetenz besteht weniger im Viel-Konsumieren als im gezielten Hinterfragen.""",
"""演算法主要推播符合我們既有行為的內容。
於是容易覺得自己的意見就是社會共識。
若回避相反觀點，就會失去檢視論證的能力。
這不是說必須同意每種意見；而是至少要理解。
實用對策是刻意更換來源並查證說法。
媒體素養較少在於「看很多」，而在於有意識地追問。""",
[n("bisherigen Verhalten","既有行為"),n("Konsens","共識"),n("widersprechende Perspektiven","相反觀點"),n("verifizieren","查證"),n("weniger … als …","比較不是……而是……")],
[p("Dadurch entsteht der Eindruck, … sei …","結果＋虛擬間接","Dadurch entsteht der Eindruck, alles sei klar."),p("Das bedeutet nicht, dass …; es bedeutet …","澄清誤解","Das heißt nicht, dass …; es heißt …"),p("weniger im A als im B","重點轉移","weniger im Reden als im Handeln")],
["先畫出『現象→後果→誤解澄清→對策』。"],["論述","媒體","比較結構"]),
(
"b2-05","dialogue","學術","Sprechstunde zur Hausarbeit","報告面談",
"""Professorin: Ihre Fragestellung ist interessant, wirkt aber noch zu breit.
Student: Soll ich mich auf einen Zeitraum beschränken?
Professorin: Ja. Außerdem fehlt bislang eine klare These, die Sie belegen oder widerlegen.
Student: Ich könnte argumentieren, dass die Maßnahme die Beteiligung erhöht hat.
Professorin: Gut. Dann brauchen Sie Vergleichsdaten und eine kritische Einordnung der Quellen.
Student: Ich schicke Ihnen bis Freitag eine überarbeitete Gliederung.""",
"""教授：你的問題意識有趣，但範圍仍太廣。
學生：我要限縮到某個時段嗎？
教授：對。而且目前缺少可證明或反駁的清楚命題。
學生：我可以主張該措施提高了參與度。
教授：很好。那你需要比較數據，並批判性定位來源。
學生：週五前我會寄修訂大綱。""",
[n("Fragestellung","問題意識／提問"),n("sich beschränken auf","限縮於"),n("These","論點／命題"),n("belegen oder widerlegen","證明或反駁"),n("kritische Einordnung","批判性定位")],
[p("wirkt noch zu + 形容詞","評價尚不足","wirkt noch zu vage"),p("Ich könnte argumentieren, dass …","提出可檢驗論點","Ich argumentiere, dass …"),p("bis Freitag eine überarbeitete …","交付修訂","bis Montag eine Skizze")],
["學術對話關鍵：範圍、命題、證據。"],["學術","論證","虛擬式"]),
(
"b2-06","story","經濟","Die Kosten der Bequemlichkeit","便利的代價",
"""Same-Day-Delivery wirkt wie ein Luxus, der kaum etwas kostet.
Tatsächlich werden die wahren Kosten oft ausgelagert: an Fahrerinnen und Fahrer, an Verpackungsmüll, an überlastete Innenstädte.
Konsumentinnen und Konsumenten entscheiden unter Zeitdruck und sehen selten die gesamte Kette.
Wenn Preise die gesellschaftlichen Folgekosten nicht abbilden, entsteht ein falscher Anreiz.
Mögliche Korrekturen wären höhere Transparenz und Alternativen, die etwas langsamer, aber nachhaltiger sind.
Bequemlichkeit ist nicht falsch; Blindheit gegenüber ihren Folgen schon.""",
"""當日達看起來像幾乎不花钱的奢侈。
實際上真正成本常被外部化：司機、包裝垃圾、超載的市中心。
消費者在時間壓力下做決定，很少看見整條鏈。
若價格無法反映社會後果，就會產生錯誤誘因。
可能的修正是提高透明，以及稍慢但更永續的選項。
便利本身沒錯；對後果視而不見才是問題。""",
[n("ausgelagert","外包／外部化"),n("gesamte Kette","整條鏈"),n("abbilden","反映／呈現"),n("Anreiz","誘因"),n("Blindheit gegenüber","對……視而不見")],
[p("wirken wie …, der/die …","看似……","wirkt wie ein Vorteil, der teuer ist"),p("Wenn … nicht …, entsteht …","條件後果","Wenn man nichts ändert, entsteht Chaos."),p("A ist nicht falsch; B schon","對比判斷","Fragen ist nicht falsch; Aufgeben schon.")],
["經濟議題文常用『表象 vs 隱藏成本』。"],["論述","經濟","關係句"]),
(
"b2-07","email","正式異議","Widerspruch gegen einen Bescheid","對行政處分提出異議",
"""Sehr geehrte Damen und Herren,

gegen den Bescheid vom 14. Mai lege ich fristgerecht Widerspruch ein.
Die darin angeführte Begründung berücksichtigt nicht die bereits eingereichten Nachweise.
Insbesondere wurde übersehen, dass meine Einkünfte vorübergehend gemindert waren.
Ich beantrage daher eine erneute Prüfung und die Aussetzung der Zahlung bis zur Entscheidung.
Anlagen: Kontoauszüge, ärztliche Bescheinigung, Kopie des Bescheids.

Mit freundlichen Grüßen
Mariam Haddad""",
"""敬啟者：

本人就 5 月 14 日之處分，於期限內提出異議。
其中理由未納入我已提交之證明。
尤其忽略我收入曾暫時減少之事實。
因此申請重新審查，並在決定前暫停繳款。
附件：帳戶明細、診斷證明、處分影本。

此致問候
Mariam Haddad""",
[n("lege ich … Widerspruch ein","提出異議", "Widerspruch einlegen。"),n("fristgerecht","符合期限地"),n("angeführte Begründung","所列理由"),n("gemindert","減少的"),n("Aussetzung der Zahlung","暫停付款")],
[p("gegen … lege ich Widerspruch ein","異議公式","Gegen den Bescheid lege ich Widerspruch ein."),p("Insbesondere wurde übersehen, dass …","強調疏漏","Insbesondere fehlt der Nachweis."),p("Ich beantrage daher …","因此申請","Ich beantrage Einsicht.")],
["行政救濟信：標的＋理由＋請求＋附件。"],["行政","法律用語","正式"]),
(
"b2-08","story","科技倫理","Automatisierte Entscheidungen","自動化決策",
"""Immer mehr Behörden und Unternehmen nutzen Systeme, die Anträge vorbewerten.
Befürworter betonen Effizienz; Kritiker warnen vor intransparenten Kriterien.
Ein zentrales Problem besteht darin, dass Fehler sich reproduzieren, wenn historische Daten verzerrt sind.
Betroffene müssen nachvollziehen können, warum eine Entscheidung gefallen ist.
Ohne Erklärbarkeit bleibt Widerspruch formal möglich, aber praktisch schwer.
Technik darf Prozesse beschleunigen, ersetzt jedoch keine Verantwortung.""",
"""愈來愈多機關與企業使用預先評估申請的系統。
支持者強調效率；批評者警告標準不透明。
核心問題是：若歷史資料有偏差，錯誤會被複製。
當事人必須能理解決定為何做成。
沒有可解釋性，異議形式上可行、實務上卻困難。
技術可以加速流程，但不能取代責任。""",
[n("vorbewerten","預先評估"),n("intransparenten Kriterien","不透明標準"),n("sich reproduzieren","自我複製"),n("verzerrt","有偏差的"),n("Erklärbarkeit","可解釋性")],
[p("Ein zentrales Problem besteht darin, dass …","點出核心","Das Problem besteht darin, dass …"),p("müssen nachvollziehen können, warum …","知情要求","müssen verstehen, warum …"),p("darf …, ersetzt jedoch keine …","允許與界線","darf helfen, ersetzt jedoch keine Kontrolle")],
["倫理論述：正反→機制→權利→結論。"],["科技","論述","抽象名詞"]),
(
"b2-09","dialogue","談判","Gehalt und Entwicklung","薪資與發展",
"""Mitarbeiterin: Angesichts meiner neuen Aufgaben möchte ich über eine Anpassung sprechen.
Führungskraft: Welche Vorstellung haben Sie?
Mitarbeiterin: Eine Erhöhung um acht Prozent sowie ein klarer Entwicklungsplan.
Führungskraft: Acht Prozent ist ambitioniert. Vier wären kurzfristig realistischer.
Mitarbeiterin: Dann schlage ich sechs vor, gekoppelt an messbare Ziele im nächsten Quartal.
Führungskraft: Das können wir prüfen. Schicken Sie mir bitte eine kurze Zusammenfassung.""",
"""員工：考量新職責，我想談調整。
主管：你有什麼想法？
員工：調薪百分之八，以及清楚發展計畫。
主管：八％偏積極。短期四％較實際。
員工：那我建議六％，並與下季可衡量目標連動。
主管：可以評估。請寄我簡短摘要。""",
[n("Angesichts + Genitiv","鑑於……"),n("ambitioniert","野心／積極的"),n("gekoppelt an","與……連結"),n("messbare Ziele","可衡量目標"),n("Quartal","季度")],
[p("Angesichts … möchte ich …","開場談判","Angesichts der Lage schlage ich vor …"),p("… Prozent, gekoppelt an …","條件式提案","eine Prämie, gekoppelt an Umsatz"),p("Das können wir prüfen","暫不拒絕","Das können wir besprechen.")],
["談判：開價→回價→折衷＋條件。"],["職場","談判","Genitiv"]),
(
"b2-10","notice","大學","Richtlinie zu KI-Tools","AI 工具使用準則",
"""Richtlinie zum Einsatz generativer KI in Prüfungsleistungen
Die Nutzung ist zulässig, sofern sie offengelegt und methodisch begründet wird.
Unzulässig ist die ungekennzeichnete Übernahme von Textpassagen.
Studierende bleiben für Richtigkeit und Eigenständigkeit verantwortlich.
Bei Verstößen drohen Maßnahmen nach der Prüfungsordnung.
Fragen richten Sie bitte an die Studiengangskoordination.""",
"""考試作業使用生成式 AI 準則
若有揭露並在方法上說明，原則允許使用。
未標示直接取用段落則不允許。
學生仍須對正確性與自主性負責。
違規可能依考試規則處置。
問題請洽系所協調窗口。""",
[n("sofern sie offengelegt … wird","只要有揭露……"),n("Unzulässig ist …","……不被允許", "主詞後置強調。"),n("ungekennzeichnete Übernahme","未標示取用"),n("Eigenständigkeit","自主性"),n("drohen Maßnahmen","可能面臨處置")],
[p("Die Nutzung ist zulässig, sofern …","附條件允許","ist erlaubt, sofern …"),p("Unzulässig ist + 名詞片語","強調禁止","Unzulässig ist das Abschreiben."),p("bleiben verantwortlich für …","責任歸屬","bleiben haftbar für …")],
["政策文本：允許條件、禁止、責任、後果。"],["學術","規定","被動"]),
]
B2.extend(pack(t) for t in RAW)

RAW2 = [
(
"b2-11","story","氣候","Anpassung statt nur Vermeidung","調適而不只減緩",
"""Klimapolitik wird oft auf Emissionsminderung verkürzt.
Ebenso notwendig ist Anpassung: Hitzepläne, grüne Innenhöfe, robuste Infrastruktur.
Wer ausschließlich auf Vermeidung setzt, unterschätzt Schäden, die bereits eintreten.
Gleichzeitig darf Anpassung nicht als Ausrede dienen, Ambitionen zu senken.
Beide Strategien greifen ineinander: Je erfolgreicher die Minderung, desto geringer der Anpassungsdruck.
Städte, die das ernst nehmen, investieren längst in beides.""",
"""氣候政策常被簡化成減碳。
同樣必要的是調適：高溫計畫、綠化中庭、韌性基礎建設。
只押寶減緩者，會低估已在發生的損害。
同時，調適也不能當降低志向的藉口。
兩者交織：減緩愈成功，調適壓力愈小。
認真的城市早已雙線投資。""",
[n("verkürzt auf","被簡化為"),n("setzt auf","押寶／依賴"),n("eintreten","發生"),n("als Ausrede dienen, zu …","作為……的藉口"),n("greifen ineinander","彼此交織")],
[p("wird oft auf … verkürzt","批評化約","wird auf Kosten verkürzt"),p("Ebenso notwendig ist …","平行主張","Ebenso wichtig ist Prävention."),p("Je … desto …","比例關係","Je klarer, desto besser")],
["政策論述抓『兩者／而非二選一』。"],["氣候","論述","比較"]),
(
"b2-12","email","跨部門","Bitte um Klärung der Zuständigkeit","請釐清權責",
"""Guten Tag Herr Lehmann, guten Tag Frau Ortiz,

bezüglich des Kundenfalls Nr. 4419 bitte ich um Klärung der Zuständigkeit.
Aus meiner Sicht betrifft der vertragliche Teil Ihren Bereich, während die technische Umsetzung bei IT liegt.
Derzeit erhält die Kundin widersprüchliche Aussagen, was den Eindruck von Unprofessionalität erzeugt.
Könnten wir morgen um 10 Uhr eine kurze Abstimmung machen und danach eine einheitliche Rückmeldung senden?

Beste Grüße
Kim Berger
Customer Success""",
"""Lehmann 先生、Ortiz 女士您好：

關於客戶案件 4419，請協助釐清權責。
就我所見，合約部分屬您們業務，技術執行則在 IT。
目前客戶收到互相矛盾的說法，造成不專業印象。
明天 10 點能否短會對齊，再給客戶一致回覆？

問候
Kim Berger
客戶成功""",
[n("bezüglich + Genitiv","關於……"),n("Zuständigkeit","權責歸屬"),n("während …","而……（對比）"),n("widersprüchliche Aussagen","互相矛盾的說法"),n("einheitliche Rückmeldung","一致回覆")],
[p("bezüglich … bitte ich um …","正式請求釐清","bezüglich des Termins bitte ich um Bestätigung"),p("Aus meiner Sicht …, während …","觀點＋對比","Aus meiner Sicht A, während B"),p("was den Eindruck von … erzeugt","後果關係句","was Unruhe erzeugt")],
["跨部門信：問題、切割、客戶影響、具體會議。"],["職場","正式郵件","關係句"]),
(
"b2-13","story","心理健康職場","Präsentismus","帶病硬撐上班",
"""Nicht nur Fehlzeiten belasten Organisationen, sondern auch Präsentismus: arbeiten trotz Krankheit.
Kurzfristig wirkt Anwesenheit produktiv; mittelfristig steigen Fehlerquote und Ansteckungsrisiko.
Ursachen liegen oft in einer Kultur, in der Ersetzbarkeit als Schwäche gilt.
Führungskräfte, die Erholung legitimieren, verändern Normen wirksamer als bloße Richtlinien.
Homeoffice kann helfen, ersetzt jedoch kein Vertrauen.
Gesundheit ist Voraussetzung für Leistung, nicht ihr Gegenteil.""",
"""傷害組織的不只是缺勤，還有帶病硬撐上班。
短期看起來人在就有效率；中期錯誤率與傳染風險上升。
原因常在於一種把「可被替代」視為弱點的文化。
讓休養合理化的主管，比光有規定更能改變規範。
在家上班有幫助，但不能取代信任。
健康是績效的前提，而非對立面。""",
[n("Fehlzeiten","缺勤"),n("Präsentismus","帶病出勤"),n("Fehlerquote","錯誤率"),n("Ersetzbarkeit","可替代性"),n("legitimieren","使合理化")],
[p("Nicht nur A, sondern auch B","雙焦點","Nicht nur Kosten, sondern auch Risiko"),p("Kurzfristig …; mittelfristig …","時間尺度","Kurzfristig günstig; langfristig teuer"),p("A ist Voraussetzung für B, nicht …","重定義關係","Pause ist Voraussetzung für Fokus")],
["抽象職場概念＋因果層次。"],["職場","論述","健康"]),
(
"b2-14","dialogue","醫療倫理","Aufklärungsgespräch","告知說明會談",
"""Ärztin: Bevor wir entscheiden, erkläre ich Nutzen und Risiken der Operation.
Patient: Wie hoch ist die Wahrscheinlichkeit von Komplikationen?
Ärztin: Bei Ihrem Profil etwa fünf Prozent; ohne Eingriff droht eine Verschlechterung.
Patient: Gibt es konservative Alternativen?
Ärztin: Ja, jedoch mit geringerer Erfolgschance. Die Entscheidung liegt bei Ihnen.
Patient: Ich möchte eine Nacht Bedenkzeit und dann Bescheid geben.""",
"""醫生：做決定前，我說明手術益處與風險。
病人：併發症機率多高？
醫生：以您的狀況約百分之五；不做可能惡化。
病人：有保守療法替代嗎？
醫生：有，但成功機會較低。決定在您。
病人：我想考慮一晚再回覆。""",
[n("Nutzen und Risiken","益處與風險"),n("Komplikationen","併發症"),n("konservative Alternativen","保守替代方案"),n("Erfolgschance","成功機會"),n("Bedenkzeit","考慮時間")],
[p("Bevor wir entscheiden, …","決策前程序","Bevor wir unterschreiben, prüfen wir."),p("Die Entscheidung liegt bei Ihnen","強調自主","Die Wahl liegt bei dir."),p("Ich möchte … Bedenkzeit","請求考慮","Ich brauche Bedenkzeit.")],
["知情同意對話：資訊→選擇→時間。"],["健康","倫理","對話"]),
(
"b2-15","notice","金融","Risikohinweis Anlageprodukt","投資商品風險提示",
"""Risikohinweis
Die Wertentwicklung der Vergangenheit ist kein verlässlicher Indikator für die Zukunft.
Kursverluste bis hin zum Totalverlust sind möglich.
Das Produkt eignet sich nur für Anlegerinnen und Anleger mit entsprechender Risikobereitschaft und Anlagehorizont.
Beratung ersetzt nicht Ihre eigenverantwortliche Prüfung der Unterlagen.
Bei Unklarheiten stellen Sie bitte Rückfragen vor der Zeichnung.""",
"""風險提示
過去績效並非未來可靠指標。
可能出現價格虧損乃至本金全損。
本商品僅適具備相應風險承受與投資期限者。
諮詢不能取代您自行檢視文件。
不清楚處請在認購前提問。""",
[n("Wertentwicklung","績效表現"),n("Indikator","指標"),n("Totalverlust","全部虧損"),n("Anlagehorizont","投資期限"),n("Zeichnung","認購")],
[p("ist kein verlässlicher Indikator für …","免責句型","ist keine Garantie für …"),p("eignet sich nur für …","適用對象","eignet sich für Fortgeschrittene"),p("ersetzt nicht …","界線","Beratung ersetzt nicht Ihre Entscheidung")],
["金融揭露文本：風險、對象、責任。"],["金融","正式","名詞化"]),
(
"b2-16","story","城市規劃","Wer besitzt den öffentlichen Raum?","誰擁有公共空間？",
"""Gehwege, Parks und Plätze gelten als öffentlich, werden aber unterschiedlich genutzt und kontrolliert.
Außengastronomie, Werbung und private Security verschieben Grenzen, oft schleichend.
Wer sich nicht konsumierend verhält, wird mancherorts früher angesprochen oder verdrängt.
Eine Stadt, die Vielfalt will, muss Nutzungsregeln transparent und verhandelbar halten.
Sonstanächst entsteht ein Raum, der nur noch für zahlungskräftige Gruppen komfortabel ist.
Öffentlichkeit bemisst sich nicht nur am Eigentum, sondern am Zugang.""",
"""人行道、公園與廣場被視為公共，但使用與管制方式不同。
戶外餐飲、廣告與私人保全常悄悄改寫界線。
在某些地方，不消費的人較早被盤問或排擠。
若城市要多元，使用規則必須透明且可協商。
否則空間會變成只對有消費力群體舒適。
公共性不只看所有權，更看近用權。""",
[n("schleichend","悄然地"),n("konsumierend","以消費方式"),n("verdrängt","被排擠"),n("verhandelbar","可協商的"),n("zahlungskräftige Gruppen","有消費力的群體")],
[p("gelten als …, werden aber …","名實落差","gelten als sicher, werden aber gemieden"),p("Wer sich nicht …, wird …","條件被動","Wer widerspricht, wird kritisiert"),p("bemisst sich nicht nur am …, sondern am …","衡量標準","bemisst sich am Zugang")],
["城市論述含權力與近用概念。"],["社會","論述","被動"]),
(
"b2-17","email","研究合作","Anfrage zur Datennutzung","資料使用詢問",
"""Sehr geehrte Frau Prof. Berg,

im Rahmen meiner Masterarbeit untersuche ich Sprachlernstrategien bei Erwachsenen.
Dazu würde ich gerne anonymisierte Umfragedaten Ihrer Arbeitsgruppe nachnutzen, sofern ethisch freigegeben.
Könnten Sie mir mitteilen, unter welchen Auflagen eine Nutzung denkbar wäre?
Selbstverständlich zitiere ich die Quelle und teile Ergebnisse vor der Veröffentlichung.

Mit freundlichen Grüßen
Jonas Pfeiffer""",
"""敬愛的 Berg 教授：

我的碩士論文研究成人語言學習策略。
若倫理上允許，希望能二次使用貴組匿名問卷資料。
可否告知在何種條件下可考慮提供？
我必將引用來源，並於發表前分享結果。

此致問候
Jonas Pfeiffer""",
[n("im Rahmen + Genitiv","在……架構下"),n("nachnutzen","二次使用"),n("sofern ethisch freigegeben","若已通過倫理開放"),n("Auflagen","附帶條件"),n("denkbar wäre","可以想像／或許可行")],
[p("im Rahmen meiner … untersuche ich …","研究開場","im Rahmen des Projekts …"),p("nachnutzen, sofern …","附條件請求","nutzen, sofern erlaubt"),p("unter welchen Auflagen …","詢問條件","unter welchen Voraussetzungen …")],
["學術請求：目的、條件、互惠。"],["學術","正式郵件"]),
(
"b2-18","dialogue","客服升級","Eskalation an die Fachabteilung","升級到專責單位",
"""Agent: Ich sehe, dass Ihr Fall bereits zweimal bearbeitet wurde, ohne Lösung.
Kundin: Genau deshalb bitte ich um Eskalation.
Agent: Ich leite ihn an die Fachabteilung weiter und setze eine Rückmeldung binnen 48 Stunden.
Kundin: Bitte bestätigen Sie mir das schriftlich.
Agent: Die Bestätigung erhalten Sie per Mail mit Ticketnummer.
Kundin: Danke. Ich erwarte eine inhaltliche Antwort, nicht nur eine Eingangsbestätigung.""",
"""客服：我看到您的案件已處理兩次仍無解。
顧客：所以才要求升級。
客服：我轉給專責單位，並設定 48 小時內回覆。
顧客：請書面確認。
客服：您會收到含工單號的郵件確認。
顧客：謝謝。我要的是實質回覆，不只收件確認。""",
[n("Eskalation","升級處理"),n("leite … weiter","轉送"),n("binnen 48 Stunden","48 小時內"),n("Eingangsbestätigung","收件確認"),n("inhaltliche Antwort","實質內容回覆")],
[p("Deshalb bitte ich um Eskalation","明確升級請求","Deshalb bitte ich um Prüfung."),p("binnen + 時間","時限","binnen einer Woche"),p("nicht nur A, sondern B","排除敷衍","nicht nur formal, sondern inhaltlich")],
["客服升級：過程摘要＋時限＋期待品質。"],["客服","談判口語"]),
(
"b2-19","story","語言政策","Mehrsprachigkeit als Ressource","多語作為資源",
"""In Debatten über Integration wird Mehrsprachigkeit manchmal als Defizit dargestellt.
Tatsächlich verfügen viele Lernende über Strategien, die monoliguale Peers so nicht kennen.
Wer zwischen Sprachen wechseln kann, trainiert Perspektivwechsel und metasprachliches Bewusstsein.
Schulen, die Herkunftssprachen wertschätzen, fördern Identität und Motivation.
Das schließt hohe Anforderungen an die Verkehrssprache nicht aus.
Ressource und Anspruch können parallel gedacht werden.""",
"""在融合辯論中，多語有時被描繪成缺陷。
事實上許多學習者具備單語同儕所無的策略。
能在語言間切換，可訓練視角轉換與後設語言意識。
重視傳承語的學校能促進認同與動機。
這並不排除對通用語的高要求。
資源與標準可以並行思考。""",
[n("Defizit","缺陷"),n("monolinguale Peers","單語同儕"),n("metasprachliches Bewusstsein","後設語言意識"),n("Herkunftssprachen","傳承語／家庭語言"),n("Verkehrssprache","通用語／公共交際語")],
[p("wird … als … dargestellt","被描繪成","wird als Chance dargestellt"),p("Das schließt … nicht aus","並不排除","Das schließt Kritik nicht aus."),p("können parallel gedacht werden","並行思考","müssen getrennt gedacht werden")],
["語言政策文：反刻板＋雙元主張。"],["社會","教育","論述"]),
(
"b2-20","notice","勞動","Hinweis zu Überstunden","加班提示",
"""Interne Regelung zu Überstunden
Überstunden sind grundsätzlich anzuordnen bzw. im Voraus zu vereinbaren.
Eigenmächtiges Mehrarbeiten begründet keinen automatischen Anspruch auf Freizeitausgleich.
Dokumentieren Sie Stunden tagesgenau im System.
Ausnahmen in Notfällen sind unverzüglich der Führungskraft zu melden.
Verstöße gegen Arbeitszeitgrenzen werden nicht geduldet.""",
"""加班內部規定
加班原則上須指派或事先約定。
自行加班不自動產生補休請求權。
請按日於系統確實記錄工時。
緊急例外須立即告知主管。
違反工時上限不予容忍。""",
[n("anzuordnen","被指派", "zu 不定式被動意味。"),n("Eigenmächtiges Mehrarbeiten","擅自加班"),n("Freizeitausgleich","補休"),n("tagesgenau","按日精確地"),n("werden nicht geduldet","不被容忍")],
[p("sind grundsätzlich zu + 不定式","原則義務","sind schriftlich zu bestätigen"),p("begründet keinen Anspruch auf …","不構成權利","schafft keinen Anspruch auf …"),p("werden nicht geduldet","零容忍","wird nicht akzeptiert")],
["勞動規範：程序、例外、紀錄、界線。"],["職場","規定","zu-不定式"]),
]
B2.extend(pack(t) for t in RAW2)

RAW3 = [
(
"b2-21","story","移民敘事","Ankommen in Etappen","分階段到達",
"""Ankommen ist selten ein einzelnes Datum.
Zuerst organisieren viele Menschen Unterkunft und Behördenwege, später Netzwerke und Routinen.
Emotionale Ankunft kann Jahre dauern, selbst wenn Papiere längst geregelt sind.
Wer das übersieht, unterschätzt Belastungen hinter scheinbarer Funktionalität.
Unterstützungsangebote sollten deshalb mehrphasig gedacht werden: praktisch, sozial, sprachlich.
Integration ist ein Prozess mit Rückschritten, nicht eine Prüfung, die man einmal besteht.""",
"""「到達」很少是單一日期。
許多人先處理住宿與行政，之後才建立網絡與作息。
即使證件早已辦妥，情感上的安頓仍可能花上數年。
忽略這點，就會低估表面功能正常背後的負荷。
因此支持措施應分階段構想：實務、社交、語言。
融合是含挫折的過程，不是一次考過就結束。""",
[n("Behördenwege","跑機關"),n("längst geregelt","早已辦妥"),n("scheinbarer Funktionalität","表面的正常運作"),n("mehrphasig","多階段的"),n("Rückschritten","倒退／挫折")],
[p("ist selten + 名詞","打破迷思","ist selten Zufall"),p("kann Jahre dauern, selbst wenn …","時間讓步","kann dauern, selbst wenn …"),p("sollten … gedacht werden","規範性建議被動","sollten neu bewertet werden")],
["複雜社會過程用『階段模型』理解。"],["社會","論述","移民"]),
(
"b2-22","email","合約","Nachverhandlung einer Klausel","條款再協商",
"""Sehr geehrte Frau Lang,

bezüglich Klausel 7 des Vertragsentwurfs sehe ich Anpassungsbedarf.
Die derzeitige Haftung erscheint unverhältnismäßig weit und kaum versicherbar.
Ich schlage vor, die Haftung auf Vorsatz und grobe Fahrlässigkeit zu begrenzen sowie eine Obergrenze festzusetzen.
Gerne erläutere ich die Gründe in einem kurzen Call.
Einen Formulierungsvorschlag füge ich bei.

Mit freundlichen Grüßen
Attorney Malik Reza""",
"""敬愛的 Lang 女士：

關於合約草案第 7 條，我認為需要調整。
目前責任範圍過寬，也幾乎無法投保。
建議將責任限於故意與重大過失，並設定上限。
我很樂意以短通話說明理由。
附件為條文建議稿。""",
[n("Anpassungsbedarf","需要調整"),n("unverhältnismäßig weit","不成比例地過寬"),n("Vorsatz","故意"),n("grobe Fahrlässigkeit","重大過失"),n("Obergrenze","上限")],
[p("sehe ich Anpassungsbedarf","點出修改必要","sehe ich Klärungsbedarf"),p("erscheint … und kaum …","雙重批評","erscheint riskant und teuer"),p("Ich schlage vor, … zu begrenzen sowie …","雙重提案","schlage vor, A zu tun sowie B")],
["合約郵件：問題定性＋具體修法＋下一步。"],["法律","正式郵件","商業"]),
(
"b2-23","dialogue","政治討論禮貌版","Unterschiedliche Positionen","不同立場",
"""A: Ich halte die Maßnahme für notwendig, weil sie Emissionen spürbar senkt.
B: Das Ziel teile ich; dennoch bezweifle ich die soziale Ausgewogenheit.
A: Welche Alternative schwebt Ihnen vor?
B: Eine gestaffelte Einführung mit Härtefallregeln.
A: Darüber können wir sprechen, sofern die Wirkung messbar bleibt.
B: Einverstanden. Lassen Sie uns Zahlen statt Zuschreibungen austauschen.""",
"""A：我認為這措施必要，因其明顯降排。
B：目標我認同；但仍懷疑社會公平性。
A：您傾向什麼替代方案？
B：分階段上路並設困境條款。
A：若效果仍可衡量，我們可以談。
B：同意。讓我們交換數據，而不是貼標籤。""",
[n("spürbar senkt","明顯降低"),n("Ausgewogenheit","均衡／公平性"),n("schwebt Ihnen vor","您心中構想是"),n("gestaffelte Einführung","分階段實施"),n("Zuschreibungen","貼標／歸咎")],
[p("Das Ziel teile ich; dennoch …","先共識後異議","Das Ziel teile ich; dennoch …"),p("Welche Alternative schwebt Ihnen vor?","詢問對案","Was schwebt dir vor?"),p("Zahlen statt Zuschreibungen","討論規範","Argumente statt Angriffe")],
["B2 辯論禮貌策略：共享目標→分歧→條件。"],["論辯","連接詞","禮貌"]),
(
"b2-24","story","藝術與市場","Wenn Kunst zur Marke wird","當藝術變成品牌",
"""Künstlerische Arbeit oszilliert zwischen Ausdruck und Vermarktung.
Plattformen belohnen Wiedererkennbarkeit, was Stil rasch zur Marke verdichten kann.
Einige nutzen das strategisch; andere empfinden es als Verengung.
Entscheidend ist, ob die ökonomische Logik noch Raum für Risiko lässt.
Ohne Experimente verarmt nicht nur die Kunst, sondern auch das Publikum.
Märkte setzen Anreize – sie ersetzen jedoch keine ästhetischen Kriterien.""",
"""藝術工作在表達與行銷之間擺盪。
平台獎勵辨識度，可能很快把風格壓縮成品牌。
有人策略性運用；有人覺得受到限縮。
關鍵在於經濟邏輯是否仍留給風險空間。
沒有實驗，貧瘠的不只藝術，還有觀眾。
市場提供誘因——但不能取代美學判準。""",
[n("oszilliert zwischen","在……之間擺盪"),n("Wiedererkennbarkeit","辨識度"),n("verdichten zu","濃縮成"),n("Verengung","窄化"),n("verarmt","變得貧瘠")],
[p("oszilliert zwischen A und B","雙重張力","schwankt zwischen A und B"),p("was … kann","關係句表後果","was zu Stress führen kann"),p("ob … noch Raum für … lässt","關鍵條件","ob Zeit für Fehler lässt")],
["文化評論句構較抽象，先抓張力對。"],["文化","論述","抽象"]),
(
"b2-25","email","危機溝通","Information nach einem Vorfall","事故後說明",
"""Liebe Kundinnen und Kunden,

gestern kam es in unserem Rechenzentrum zu einem zeitweisen Ausfall.
Ursache war ein defektes Netzteil; personenbezogene Daten waren nicht betroffen.
Der Dienst läuft wieder stabil. Zusätzlich prüfen wir redundante Systeme.
Für entstandene Unannehmlichkeiten bitten wir um Entschuldigung.
Fragen beantwortet unser Statusblog sowie der Support unter der bekannten Adresse.

Ihr Serviceteam""",
"""親愛的客戶：

昨日我們的資料中心發生短暫故障。
原因是電源模組故障；個人資料未受影響。
服務已恢復穩定。我們並加查備援系統。
造成不便，敬請見諒。
問題可參閱狀態部落格或既有客服地址。

服務團隊""",
[n("zeitweisen Ausfall","短暫中斷"),n("Netzteil","電源供應器"),n("nicht betroffen","未受影響"),n("redundante Systeme","備援系統"),n("Unannehmlichkeiten","不便")],
[p("kam es zu einem …","發生某事件","kam es zu Verzögerungen"),p("waren nicht betroffen","排除最糟情況","waren nicht gefährdet"),p("Für … bitten wir um Entschuldigung","公開致歉","Für die Wartezeit bitten wir um Entschuldigung")],
["危機溝通：事實、影響範圍、補救、致歉、管道。"],["公關","正式","科技"]),
(
"b2-26","story","教育不平等","Früh fördern, später weniger reparieren","早期支持、少事後補救",
"""Bildungschancen hängen stärker vom Elternhaus ab, als es Leistungsmythen nahelegen.
Frühe Sprachförderung und verlässliche Betreuung wirken präventiv.
Spätere Förderprogramme sind wichtig, aber teurer und oft weniger wirksam.
Das Argument knapper Kassen darf nicht dazu führen, Investitionen an der Wurzel zu kürzen.
Wer Chancengleichheit will, muss früher ansetzen und Ergebnisse ehrlich evaluieren.
Gerechtigkeit ist messbar – sofern man die richtigen Indikatoren wählt.""",
"""教育機會比功績迷思所暗示的，更依賴家庭背景。
早期語言支持與穩定托育具預防效果。
後期補救重要，但更貴且常較無效率。
預算短缺論不應導致砍掉源頭投資。
若要機會平等，必須更早介入並誠實評估成效。
公平可被測量——前提是選對指標。""",
[n("nahelegen","暗示／使人以為"),n("präventiv","預防性地"),n("knapper Kassen","拮据預算"),n("an der Wurzel","從根源"),n("evaluieren","評估")],
[p("hängen stärker von … ab, als …","比較依賴","hängt stärker von Übung ab, als …"),p("darf nicht dazu führen, zu …","警示因果","darf nicht dazu führen, aufzugeben"),p("sofern man … wählt","方法條件","sofern man ehrlich misst")],
["教育政策：預防優於補救的論證。"],["教育","論述","比較"]),
(
"b2-27","dialogue","科學傳播","Interview zum Forschungsergebnis","研究成果訪談",
"""Journalistin: Ihre Studie legt nahe, dass kurze Pausen die Fehlerquote senken.
Forscher: Korrekt, allerdings nur unter bestimmten Bedingungen der Aufgabenkomplexität.
Journalistin: Lässt sich das auf Schulen übertragen?
Forscher: Mit Vorsicht. Laborsettings unterscheiden sich von Klassenzimmern.
Journalistin: Was wäre Ihr vorsichtiger Rat an Lehrkräfte?
Forscher: Pausen bewusst planen und lokale Daten beobachten, statt Rezepte zu kopieren.""",
"""記者：您的研究暗示短暫休息可降低錯誤率。
研究者：正確，但僅在特定任務複雜度條件下。
記者：能套用到學校嗎？
研究者：要謹慎。實驗室情境不同於教室。
記者：您給教師的審慎建議是？
研究者：有意識安排休息並觀察在地數據，而非複製藥方。""",
[n("legt nahe, dass","暗示……"),n("allerdings nur unter …","但僅在……條件下"),n("Laborsettings","實驗室情境"),n("vorsichtiger Rat","審慎建議"),n("Rezepte zu kopieren","複製現成藥方")],
[p("legt nahe, dass …","研究結論語氣","Daten legen nahe, dass …"),p("Lässt sich … übertragen?","遷移性提問","Lässt sich das generalisieren?"),p("statt … zu kopieren","方法提醒","statt Lösungen zu kopieren")],
["科學傳播：限定條件、不可過度推廣。"],["學術","媒體","對話"]),
(
"b2-28","notice","建築","Brandschutzanweisung aktualisiert","消防指示更新",
"""Aktualisierte Brandschutzanweisung
Fluchtwege sind dauerhaft freizuhalten; Abstellen von Gegenständen ist untersagt.
Sammelpunkt ist der südliche Parkplatz; Aufzüge dürfen nicht benutzt werden.
Brandschutzhelferinnen und -helfer tragen orange Westen und weisen ein.
Nach dem Alarm ist das Gebäude erst nach Freigabe durch die Feuerwehr wieder zu betreten.
Übungen finden unangekündigt statt.""",
"""更新消防指示
逃生通道須持續暢通；禁止堆放物品。
集合點為南側停車場；不得使用電梯。
消防協助人員穿橘色背心並引導。
警報後須俟消防單位放行才可再進入。
演習不另行預告。""",
[n("freizuhalten","須保持暢通"),n("untersagt","被禁止"),n("weisen ein","引導進入／指示"),n("Freigabe","放行"),n("unangekündigt","未預告地")],
[p("sind dauerhaft zu + 不定式","持續義務","sind sauber zu halten"),p("erst nach … wieder zu …","條件恢復","erst nach Prüfung wieder zu öffnen"),p("finden unangekündigt statt","不預告舉行","finden jährlich statt")],
["安全指令祈使＋被動態勢濃。"],["安全","規定"]),
(
"b2-29","story","消費心理","Das Paradox der Wahl","選擇悖論",
"""Mehr Optionen gelten intuitiv als mehr Freiheit.
Empirisch führen Überangebote jedoch oft zu Aufschub oder Unzufriedenheit nach der Entscheidung.
Ursächlich sind Vergleichskosten und die Angst, etwas Besseres zu verpassen.
Händler nutzen das, indem sie Default-Optionen und künstliche Verknappung einsetzen.
Wer bewusst Filter setzt, reduziert Komplexität, ohne Wahlrecht aufzugeben.
Freiheit braucht mitunter Begrenzung, um handhabbar zu bleiben.""",
"""選項愈多，直覺上愈自由。
但實證上，過度供給常導致拖延或決定後不满意。
原因是比較成本，以及怕錯過更好的。
商家利用預設選項與人造稀缺。
刻意設定過濾條件，能降複雜度卻不放棄選擇權。
自由有時需要界線才好操作。""",
[n("Überangebote","過度供給"),n("Aufschub","拖延"),n("Vergleichskosten","比較成本"),n("Default-Optionen","預設選項"),n("künstliche Verknappung","人造稀缺"),n("handhabbar","可操作的")],
[p("gelten intuitiv als …","直覺成見","gelten als sicher"),p("indem sie … einsetzen","手段說明","indem sie Preise senken"),p("ohne … aufzugeben","保留底線","ohne Qualität aufzugeben")],
["心理／經濟概念文，注意因果鏈。"],["心理","論述","經濟"]),
(
"b2-30","email","董事會摘要","Kurzbericht für die Geschäftsleitung","給經營層的短報",
"""Sehr geehrte Geschäftsleitung,

anbei der Kurzbericht zum Quartal:
Umsatz +6 % gegenüber Vorjahr; Kundenbindung stabil; Lieferkettenrisiko weiterhin erhöht.
Wir empfehlen, das Dual-Sourcing auszubauen und Marketingbudget zugunsten von Retention umzuschichten.
Entscheidungstermin: 3. Juni. Details in der Anlage.

Mit freundlichen Grüßen
Controlling""",
"""敬愛的經營層：

附件為本季短報：
營收年增 6%；客戶黏著穩定；供應鏈風險仍偏高。
建議擴大雙來源採購，並將行銷預算轉向留存。
決策日：6 月 3 日。細節見附件。

此致問候
財務控制""",
[n("gegenüber Vorjahr","相對前年"),n("Kundenbindung","客戶留存／黏著"),n("Dual-Sourcing","雙來源採購"),n("zugunsten von","轉而惠及／偏向"),n("umzuschichten","重新配置")],
[p("anbei der Kurzbericht …","高階摘要開場","anbei die Übersicht"),p("Wir empfehlen, … auszubauen und … umzuschichten","雙建議","Wir empfehlen, A zu stärken und B zu kürzen"),p("Entscheidungstermin:","決策節點","Beschluss am …")],
["給高層：數據→建議→決策日，極短。"],["商業","正式郵件"]),
]
B2.extend(pack(t) for t in RAW3)

RAW4 = [
(
"b2-31","story","性別與語言","Sprache und Sichtbarkeit","語言與可見度",
"""Spracherformen wie gendergerechte Formen lösen heftige Debatten aus.
Manche sehen darin Symbolpolitik; andere ein Mittel gegen unsichtbare Normalität.
Unstrittig ist, dass Sprache Wahrnehmung beeinflussen kann, ohne Realität allein zu verändern.
Pragmatische Ansätze kombinieren Lesbarkeit mit inklusiven Formulierungen.
Dogmatismus auf beiden Seiten verengt den Raum für Experimente.
Sichtbarkeit entsteht durch Praxis, nicht durch Dauerempörung.""",
"""性別包容的語言形式引發激烈辯論。
有人視為象徵政治；有人視為對抗隱形常規的手段。
無可爭議的是：語言能影響認知，卻不能單憑自身改變現實。
務實做法會兼顧可讀性與包容表述。
雙方教條都會壓縮實驗空間。
可見度來自實踐，而非持續憤怒。""",
[n("heftige Debatten auslösen","引發激烈辯論"),n("Symbolpolitik","象徵政治"),n("Unstrittig ist, dass","無可爭議的是"),n("Dogmatismus","教條主義"),n("Dauerempörung","持續憤慨")],
[p("Manche sehen darin A; andere B","立場對照","Manche sehen Chance; andere Risiko"),p("Unstrittig ist, dass …","先立共識","Klar ist, dass …"),p("entsteht durch …, nicht durch …","因果對立","kommt durch Übung, nicht durch Zufall")],
["爭議題：先共識區，再談分歧。"],["社會","語言","論述"]),
(
"b2-32","dialogue","建築工地協調","Abstimmung mit Anwohnenden","與住戶協調",
"""Bauleitung: Ab Montag beginnen lärmintensive Arbeiten von 8 bis 16 Uhr.
Anwohnende: Können Sie die lautesten Phasen auf den Vormittag legen?
Bauleitung: Das prüfen wir; vollständig vermeiden lassen sie sich nicht.
Anwohnende: Dann erwarten wir zumindest eine Hotline bei Verstößen gegen die Ruhezeiten.
Bauleitung: Wird eingerichtet. Protokolle legen wir wöchentlich offen.
Anwohnende: Gut. Transparenz reduziert Widerstand.""",
"""工地主任：週一起喧鬧工程為 8–16 點。
住戶：能否把最吵時段排到上午？
工地：我們會評估；無法完全避免。
住戶：那至少要有違反安靜時段的申訴專線。
工地：會設置。紀錄每週公開。
住戶：好。透明能降低阻力。""",
[n("lärmintensive Arbeiten","高噪音工程"),n("vollständig vermeiden lassen sich nicht","無法被完全避免", "lassen sich。"),n("zumindest","至少"),n("legen wir … offen","公開"),n("reduziert Widerstand","降低阻力")],
[p("Können Sie … auf … legen?","請求時程調整","Können Sie das auf Montag legen?"),p("lassen sich nicht vollständig …","技術限制","lassen sich nicht vollständig planen"),p("Transparenz reduziert …","機制主張","Information reduziert Angst")],
["利益協調：限制坦白＋最小補償。"],["社區","談判","lassen sich"]),
(
"b2-33","story","數位勞動","Clickwork und Würde","點擊勞動與尊嚴",
"""Hinter scheinbar intelligenten Systemen steckt oft unsichtbare Clickarbeit:
Daten labeln, Inhalte prüfen, Grenzfälle entscheiden.
Die Entlohnung ist häufig prekär, die psychische Belastung hoch.
Öffentliche Debatten feiern Innovation, während die Infrastruktur menschlicher Arbeit verblasst.
Regulierung und Mitbestimmung könnten Mindeststandards setzen, ohne Forschung zu ersticken.
Intelligenz, die auf Ausbeutung beruht, verdient den Namen nur bedingt.""",
"""看似智能的系統背後，常是看不見的點擊勞動：
標註資料、審核內容、判斷邊界案例。
報酬常不穩定，心理負荷高。
公共討論歌頌創新，同時人的勞動基礎被淡化。
監管與共同決定可設最低標準，而不必窒息研究。
建立在剝削上的「智能」，只在有限意義上配得上這名字。""",
[n("labeln","標註"),n("prekär","不穩定／脆弱的"),n("verblasst","變淡／被淡忘"),n("Mitbestimmung","共同決定／勞資參與"),n("ersticken","窒息／扼殺"),n("nur bedingt","僅在有限程度上")],
[p("Hinter … steckt oft …","揭示背後","Hinter dem Erfolg steckt Glück."),p("während … verblasst","對比被忽略者","während Kosten steigen"),p("verdient den Namen nur bedingt","評價限定","gilt nur bedingt als …")],
["批判科技文：看見勞動鏈。"],["科技","勞動","論述"]),
(
"b2-34","email","學術審查","Gutachten – kurze Einschätzung","審查意見短評",
"""Liebe Kolleginnen und Kollegen,

anbei meine Einschätzung zum Manuskript.
Stärken: klare Fragestellung, saubere Methodik.
Schwächen: Diskussion zu knapp; Literatur nach 2022 kaum berücksichtigt.
Ich empfehle Überarbeitung mit Fokus auf Limitationen und Übertragbarkeit.
Details markiere ich in der Datei.

Beste Grüße
A. Richter""",
"""各位同仁：

附件是我對稿件的意見。
優點：問題清楚、方法扎實。
弱點：討論過短；2022 後文獻幾乎未納入。
建議修改，重點放在限制與可遷移性。
細節我在檔案中標出。

問候
A. Richter""",
[n("Manuskript","稿件"),n("Methodik","方法論"),n("zu knapp","過於簡短"),n("Limitationen","研究限制"),n("Übertragbarkeit","可遷移／可推廣性")],
[p("Stärken: … Schwächen: …","對照評價","Vorteile: … Nachteile: …"),p("Ich empfehle Überarbeitung mit Fokus auf …","修改建議","mit Fokus auf Klarheit"),p("Details markiere ich in …","指出位置","Kommentare stehen in …")],
["同儕審查短箋：優缺＋可執行修改。"],["學術","評價"]),
(
"b2-35","dialogue","心理諮商片段","Grenzen setzen","設定界線",
"""Therapeutin: Wann fällt es Ihnen besonders schwer, Nein zu sagen?
Klient: Wenn ich befürchte, andere zu enttäuschen.
Therapeutin: Welche Kosten entstehen Ihnen dadurch langfristig?
Klient: Erschöpfung und heimlicher Ärger.
Therapeutin: Formulieren wir einen Satz, der freundlich und klar ist.
Klient: „Heute kann ich nicht; lass uns nächste Woche schauen.“""",
"""諮商師：您何時特別難說不？
個案：當我怕讓別人失望時。
諮商師：長期這帶給您什麼代價？
個案：耗竭與暗自生氣。
諮商師：我們來組一句友善又清楚的話。
個案：「今天不行；我們下週再看。」""",
[n("Nein zu sagen","說不"),n("zu enttäuschen","讓人失望"),n("heimlicher Ärger","暗自的怒氣"),n("Formulieren wir","我們來表述"),n("freundlich und klar","友善且清楚")],
[p("Wann fällt es Ihnen schwer, zu …?","探索模式","Wann fällt es dir schwer, zu fragen?"),p("Welche Kosten entstehen …?","後果覺察","Welche Folgen entstehen?"),p("Formulieren wir einen Satz, der …","練習新行為","Üben wir einen Satz, der passt.")],
["對話示範界線語言的具體化。"],["心理","對話","不定式"]),
(
"b2-36","notice","環境政策","Pfand auf Einwegbecher","一次性杯子押金",
"""Ab September gilt ein Pfand von 0,50 € auf Einwegbecher im Stadtgebiet.
Ziel ist die Reduktion von Abfall in Parks und Bahnhöfen.
Rückgabe ist in teilnehmenden Cafés und Automaten möglich.
Ausgenommen sind medizinisch notwendige Becher.
Verstöße gegen die Kennzeichnungspflicht können mit Verwarnungsgeld geahndet werden.""",
"""自九月起市區一次性杯子收取 0.5 歐押金。
目標是減少公園與車站垃圾。
可於參與咖啡店與機器處退回。
醫療必要杯子除外。
違反標示義務可能處以警告罰鍰。""",
[n("Pfand","押金"),n("Einwegbecher","一次性杯子"),n("teilnehmenden","參與的"),n("Ausgenommen sind …","……除外"),n("Kennzeichnungspflicht","標示義務")],
[p("Ab … gilt ein Pfand von …","收費生效","Ab Januar gilt …"),p("Ausgenommen sind …","例外清單","Ausgenommen sind Kinder unter 6."),p("können mit … geahndet werden","處罰被動","kann mit Bußgeld geahndet werden")],
["政策公告含目標、退回點、例外、罰則。"],["環境","規定","被動"]),
(
"b2-37","story","記憶與敘事","Wie wir uns erinnern","我們如何記憶",
"""Erinnerungen sind keine Videoaufzeichnungen, sondern Rekonstruktionen.
Jedes Abrufen kann Details verschieben, besonders unter Emotionen.
Deshalb widersprechen sich Zeugenaussagen mitunter ehrlich und dennoch fehlerhaft.
Wer das weiß, wird demütiger im Umgang mit „sicheren“ Erinnerungen.
In der Therapie kann rekonstruktives Erinnern heilsam sein; vor Gericht braucht es Korrektive.
Narrationen stiften Identität – und verdienen Prüfung.""",
"""記憶不是錄像，而是重構。
每次提取都可能改動細節，尤其在情緒下。
因此證人陳述有時誠實卻仍出錯。
明白這點，會對「確定的記憶」更謙遜。
在治療中，重構式回憶可能療癒；在法庭則需要校正。
敘事形塑認同——也值得被檢視。""",
[n("Rekonstruktionen","重構"),n("Abrufen","提取（記憶）"),n("mitunter","有時"),n("demütiger","更謙遜"),n("Korrektive","校正機制"),n("stiften","促成／建立")],
[p("sind keine A, sondern B","重定義","sind keine Fakten, sondern Deutungen"),p("Deshalb … mitunter … und dennoch …","雙重修飾","Deshalb falsch und dennoch ehrlich"),p("kann … sein; … braucht …","語境分化","kann helfen; Wissenschaft braucht Belege")],
["認知主題：隱喻＋語用分化（治療／法庭）。"],["心理","論述","學術口吻"]),
(
"b2-38","email","供應商","Qualitätseinbruch und Maßnahmen","品質下滑與對策",
"""Sehr geehrte Frau Cho,

seit Charge 18 stellen wir erhöhte Ausschussraten fest.
Wir bitten um Ursachenanalyse binnen fünf Werktagen sowie um einen Maßnahmenplan.
Bis zur Klärung setzen wir weitere Abrufe aus.
Bitte bestätigen Sie den Eingang noch heute.

Mit freundlichen Grüßen
Einkauf – Mertens GmbH""",
"""敬愛的 Cho 女士：

自第 18 批次起，我們發現不良率升高。
請於五個工作天內提出原因分析與對策計畫。
釐清前我們暫停後續叫貨。
請於今日確認收悉。

此致問候
採購 – Mertens 有限公司""",
[n("Charge","批次"),n("Ausschussraten","不良率"),n("Ursachenanalyse","原因分析"),n("Abrufe","叫貨／提貨"),n("setzen … aus","暫停")],
[p("seit … stellen wir … fest","問題觀察","seit März stellen wir Verzögerungen fest"),p("bitten um A sowie um B","雙重要求","bitten um Angebot sowie Termin"),p("Bis zur Klärung setzen wir … aus","暫時措施","Bis zur Klärung pausieren wir")],
["供應商信：數據＋時限＋暫緩＋確認。"],["商業","正式郵件"]),
(
"b2-39","dialogue","法庭外和解","Vergleichsgespräch","和解會談",
"""Mediatorin: Beide Seiten haben Kostenrisiko und Zeitdruck.
Partei A: Wir könnten auf einen Teil der Forderung verzichten, wenn die Lieferung nachgebessert wird.
Partei B: Eine Nachbesserung ist machbar; die ursprüngliche Summe jedoch nicht.
Mediatorin: Ein Vergleich bei 60 Prozent plus Nachbesserung innerhalb eines Monats?
Partei A: Unter Vorbehalt der schriftlichen Fixierung ja.
Partei B: Einverstanden.""",
"""調解人：雙方都有成本風險與時間壓力。
甲方：若能補正交貨，我們可放棄部分請求。
乙方：補正可行；但原金額不行。
調解人：以六成金額加一個月內補正達成和解？
甲方：在書面確定前提下可以。
乙方：同意。""",
[n("Kostenrisiko","成本風險"),n("auf … verzichten","放棄……"),n("nachgebessert","補正／改善後交貨"),n("machbar","可行的"),n("Unter Vorbehalt","在保留條件下"),n("Fixierung","書面確定")],
[p("Wir könnten …, wenn …","條件讓步","Wir könnten warten, wenn …"),p("Ein Vergleich bei … plus …","和解結構","Ein Kompromiss bei X plus Y"),p("Unter Vorbehalt der …","法律保留","Unter Vorbehalt der Prüfung")],
["和解對話：讓步交換＋書面化。"],["法律","談判"]),
(
"b2-40","story","旅行批判","Overtourism lokal","在地過度觀光",
"""Tourismus bringt Einnahmen und Arbeitsplätze, erzeugt jedoch Druck auf Wohnraum und Infrastruktur.
Anwohnerinnen und Anwohner berichten von Lärm, Müll und dem Gefühl, Kulisse zu sein.
Steuern und Obergrenzen können steuern, sofern sie nicht nur symbolisch bleiben.
Zugleich braucht es Angebote, die Wertschöpfung lokal halten.
Ohne Beteiligung der Stadtgesellschaft drohen Protest und Polarisierung.
Nachhaltiger Tourismus misst Erfolg nicht allein an Übernachtungszahlen.""",
"""觀光帶來收入與就業，卻也對住房與基礎建設施壓。
居民反映噪音、垃圾，以及自己像佈景的感覺。
稅與上限可以調節——若不只是象徵。
同時需要把產值留在在地的方案。
若城市社會缺席，恐有抗議與對立。
永續觀光不以住宿數單論成功。""",
[n("Druck auf","對……的壓力"),n("Kulisse","佈景／背景板"),n("Obergrenzen","上限"),n("Wertschöpfung","價值創造／產值"),n("Polarisierung","對立／極化")],
[p("bringt A, erzeugt jedoch B","利弊並列","bringt Tempo, erzeugt jedoch Stress"),p("können steuern, sofern …","工具有效條件","können helfen, sofern …"),p("misst Erfolg nicht allein an …","成功指標重設","misst nicht allein an Profit")],
["在地視角的觀光批判結構完整。"],["社會","旅遊","論述"]),
]
B2.extend(pack(t) for t in RAW4)

RAW5 = [
(
"b2-41","email","內部調查","Vertrauliche Meldung","機密通報",
"""Vertraulich – nur für Compliance

hiermit melde ich mögliche Interessenkonflikte in der Vergabe vom März.
Mir liegen E-Mails vor, die eine bevorzugte Behandlung nahelegen.
Ich bitte um vertrauliche Prüfung und Schutz vor Repressalien.
Für Rückfragen stehe ich zur Verfügung, bevorzugt schriftlich.

Initialen: N. S.""",
"""機密 – 僅供法遵

謹通報三月採購可能存在利益衝突。
我持有暗示優惠待遇的郵件。
請機密查核並保護免遭報復。
若需詢問，我可配合，最好以書面。

縮寫：N. S.""",
[n("Interessenkonflikte","利益衝突"),n("Vergabe","採購／發包"),n("bevorzugte Behandlung","優惠待遇"),n("Repressalien","報復"),n("bevorzugt schriftlich","最好以書面")],
[p("hiermit melde ich mögliche …","吹哨開場","hiermit melde ich Unregelmäßigkeiten"),p("nahelegen","暗示證據力道","Die Daten legen Betrug nahe."),p("Schutz vor …","請求保護","bitte um Schutz vor Benachteiligung")],
["吹哨郵件：事實克制、請求保密與保護。"],["合規","正式","職場"]),
(
"b2-42","story","老化社會","Pflege neu denken","重新思考照護",
"""Eine alternde Gesellschaft braucht mehr als zusätzliche Pflegeplätze.
Prävention, barrierefreies Wohnen und entlastende Technik gehören dazu.
Zugleich bleibt menschliche Zuwendung unersetzlich.
Systeme, die Pflegekräfte ausbrennen, lösen den demografischen Druck nicht.
Bezahlung, Anerkennung und Einwanderung von Fachkräften müssen zusammengedacht werden.
Würde im Alter bemisst sich am Alltag, nicht an Sonntagsreden.""",
"""高齡社會需要的不只是更多床位。
預防、無障礙居住與減輕負荷的技術都在其中。
同時，人的關懷仍不可取代。
讓照護者燃盡的制度，解不了人口壓力。
薪資、尊重與專業人力移民必須一併思考。
老年尊嚴看日常，而非節日演說。""",
[n("barrierefreies Wohnen","無障礙居住"),n("entlastende Technik","減輕負荷的技術"),n("unersetzlich","不可取代"),n("ausbrennen","燃盡／過勞垮掉"),n("zusammengedacht werden","被一併思考"),n("Sonntagsreden","節日／空話演說")],
[p("braucht mehr als …","超越單一解","braucht mehr als Geld"),p("bleiben unersetzlich","不可取代主張","bleibt zentral"),p("müssen zusammengedacht werden","系統思維","müssen zusammengehören")],
["社會政策：多元支柱＋勞動條件。"],["社會","健康","論述"]),
(
"b2-43","dialogue","產品設計回饋","Usability-Test","可用性測試",
"""Moderatorin: An welcher Stelle sind Sie unsicher geworden?
Tester: Bei der Zahlung. Die Schaltfläche wirkt nicht klickbar.
Moderatorin: Was hätten Sie erwartet?
Tester: Eine klarere Beschriftung und eine Bestätigungsseite.
Entwickler: Das können wir in der nächsten Iteration priorisieren.
Moderatorin: Notiert – kritische Priorität.""",
"""主持人：您在哪一步開始不確定？
測試者：付款時。按鈕看起來不可點。
主持人：您原本期待什麼？
測試者：更清楚的標示與確認頁。
工程師：我們可以在下一輪迭代優先處理。
主持人：記下——關鍵優先級。""",
[n("Schaltfläche","按鈕"),n("Beschriftung","標示文字"),n("Bestätigungsseite","確認頁"),n("Iteration","迭代"),n("priorisieren","排優先次序")],
[p("An welcher Stelle …?","定位問題","An welcher Stelle stockt es?"),p("Was hätten Sie erwartet?","期望提問","Was hättest du erwartet?"),p("in der nächsten Iteration priorisieren","產品流程","im nächsten Sprint priorisieren")],
["設計回饋對話：觀察→期望→行動。"],["科技","產品","對話"]),
(
"b2-44","notice","交通基礎設施","Sperrung der Rheinbrücke","萊茵河橋封閉",
"""Vollsperrung der Rheinbrücke 9.–20. September wegen Sanierung
Umleitung über die Südbrücke; mit erheblichen Verzögerungen ist zu rechnen.
ÖPNV verdichtet Sonderfahrten zwischen 6 und 9 Uhr.
Fahrradverkehr wird über den parallel geführten Steg geleitet.
Aktuelle Lagebilder veröffentlicht die Stadt viertelstündlich online.""",
"""萊茵河橋 9/9–9/20 因整修全面封閉
改道南橋；請預期明顯延誤。
大眾運輸於 6–9 點加密加班車。
自行車改經平行便橋。
市府每十五分鐘於線上更新路況。""",
[n("Vollsperrung","全面封閉"),n("Sanierung","整修"),n("mit … ist zu rechnen","必須預期……"),n("verdichtet Sonderfahrten","加密加班車"),n("Steg","便橋／步道橋"),n("viertelstündlich","每十五分鐘")],
[p("wegen + Genitiv/名詞","原因","wegen Bauarbeiten"),p("mit … ist zu rechnen","預期公式","mit Wartezeit ist zu rechnen"),p("wird über … geleitet","改道被動","wird umgeleitet über …")],
["大型交通公告：替代、影響、資訊頻率。"],["交通","被動","公告"]),
(
"b2-45","story","幽默與界限","Ironie in der Zweitsprache","第二語言中的反諷",
"""Ironie setzt gemeinsames Wissen und feine Prosodie voraus.
In der Zweitsprache wird sie leicht als Unhöflichkeit missverstanden.
Deshalb empfehlen Lehrwerke anfangs Klarheit vor Wortspiel.
Fortgeschrittene können Ironie gezielt üben, indem sie Kontextmarker setzen.
Wer unsicher ist, fragt nach oder formuliert wörtlich.
Humor verbindet – missglückte Ironie trennt rascher als beabsichtigt.""",
"""反諷需要共享知識與細微韻律。
在第二語言裡很容易被誤認為不禮貌。
因此教材初期常建議先求清楚、再玩文字。
進階者可透過上下文標記刻意練習反諷。
不確定就詢問或改直說。
幽默能連結——失敗的反諷比預期更快造成隔閡。""",
[n("setzt … voraus","以……為前提"),n("Prosodie","韻律／聲調"),n("missverstanden","被誤解"),n("Kontextmarker","上下文標記"),n("missglückte Ironie","失敗的反諷")],
[p("setzt A und B voraus","前提","setzt Übung voraus"),p("wird leicht als … missverstanden","易被誤會","wird als Angriff missverstanden"),p("Klarheit vor …","優先次序","Sicherheit vor Tempo")],
["语用／語言學習後設主題。"],["語言","文化","論述"]),
(
"b2-46","email","贊助","Anfrage Sponsoring Bildung","教育贊助詢問",
"""Sehr geehrte Damen und Herren der Stiftung Horizonte,

wir bitten um Prüfung eines Sponsorings für unser Mentoring-Programm.
Zielgruppe sind Erststudierende aus nichtakademischen Haushalten.
Gegenleistung: Sichtbarkeit in Materialien, Einladung zum Abschlussevent, Wirkungsbericht.
Budgetrahmen und Konzept finden Sie in der Anlage.
Über ein Gespräch würden wir uns freuen.

Mit freundlichen Grüßen
Initiative Zugang Bildung""",
"""Horizonte 基金會鈞鑒：

懇請評估贊助我們的導師計畫。
對象為非學術家庭背景的大一學生。
回饋：文宣曝光、成果活動邀請、成效報告。
預算與構想見附件。
期待能進一步洽談。

此致問候
教育近用倡議""",
[n("Erststudierende","家族第一代大學生"),n("nichtakademischen Haushalten","非學術家庭"),n("Gegenleistung","對價／回饋"),n("Wirkungsbericht","成效報告"),n("Budgetrahmen","預算框架")],
[p("wir bitten um Prüfung eines …","贊助開場","wir bitten um Unterstützung"),p("Gegenleistung:","互惠清單","Im Gegenzug bieten wir …"),p("Über ein Gespräch würden wir uns freuen","客氣收尾","Über Feedback würden wir uns freuen")],
["贊助提案：對象、影響、回饋、附件。"],["非營利","正式郵件"]),
(
"b2-47","dialogue","危機室","Lagebesprechung","情勢簡報",
"""Leitung: Status der Systeme?
IT: Primärserver wieder online; Backup-Sync verzögert um 20 Minuten.
Kommunikation: Pressestatement ist freigegeben, Social-Kanal noch in Abstimmung.
Leitung: Kundensupport priorisiert Bestandskunden mit laufenden Verträgen.
Recht: Bitte keine Schuldzuweisungen nach außen.
Leitung: Nächstes Update in 30 Minuten.""",
"""主管：系統狀態？
IT：主伺服器已恢復；備援同步延遲 20 分鐘。
公關：新聞稿已放行，社群渠道尚在對齊。
主管：客服優先處理合約存續客戶。
法務：對外勿歸咎。
主管：30 分鐘後下一次更新。""",
[n("freigegeben","已放行／核准"),n("in Abstimmung","對齊／協調中"),n("Bestandskunden","既有客戶"),n("Schuldzuweisungen","歸咎"),n("nach außen","對外")],
[p("Status der …?","簡報提問","Status der Lieferung?"),p("priorisiert + 對象","資源排序","priorisiert Notfälle"),p("Bitte keine … nach außen","對外規範","Bitte keine Spekulation nach außen")],
["危機室對話：短句、責任清楚。"],["危機","職場","對話"]),
(
"b2-48","story","食物系統","Saisonale Küche als Politik","當季飲食即政治",
"""Saisonal kochen klingt nach Lifestyle, ist aber auch Ressourcenpolitik.
Kürzere Wege und angepasste Sorten senken Emissionen und stärken regionale Erzeuger.
Gleichzeitig darf Saisonalität nicht zur moralischen Keule gegen Wenigverdienende werden.
Zugang zu frischen Produkten hängt von Preis, Zeit und Infrastruktur ab.
Gute Politik verbindet Bildung, Subventionen und Stadtplanung.
Teller und System gehören zusammen.""",
"""當季料理聽起來像生活方式，其實也是資源政治。
較短運距與適地品種可降排並壯大在地生產者。
同時，當季不該變成打低收入者的道德棍棒。
新鮮食材近用取決於價格、時間與基礎建設。
好政策連結教育、補貼與都市計畫。
餐盤與系統本為一體。""",
[n("angepasste Sorten","適地品種"),n("Erzeuger","生產者"),n("moralischen Keule","道德大棒"),n("Wenigverdienende","低收入者"),n("Subventionen","補貼")],
[p("klingt nach …, ist aber auch …","表象與實質","klingt nach Zufall, ist aber Planung"),p("darf nicht zur … werden","規範底線","darf nicht zur Ausrede werden"),p("hängt von A, B und C ab","多重依賴","hängt von Zeit und Geld ab")],
["食物系統論述避免道德化約。"],["環境","社會","論述"]),
(
"b2-49","notice","文化機構","Leitlinien für Ausstellungen","展覽準則",
"""Leitlinien der städtischen Galerie
Ausstellungen sollen multiperspektivisch kuratiert und barrierearm vermittelt werden.
Leihgaben erfordern schriftliche Vereinbarungen zu Versicherung und Transport.
Kritische Provenienzprüfung ist vor Erwerb und Präsentation verpflichtend.
Bildungsangebote sind integraler Bestandteil, nicht optionales Beiwerk.
Beschwerden nimmt die Direktion entgegen und dokumentiert sie.""",
"""市立藝廊準則
展覽應多視角策展，並以便利近用方式傳達。
借展須有保險與運輸書面約定。
購藏與展出前必須進行出處檢視。
教育活動是整體一環，而非可有可無的附屬。
申訴由館長受理並記錄。""",
[n("multiperspektivisch","多視角地"),n("barrierearm","低障礙／較易近用"),n("Leihgaben","借展作品"),n("Provenienzprüfung","出處／源流檢視"),n("Beiwerk","附屬物")],
[p("sollen … und … werden","雙重規範被動","sollen geprüft und dokumentiert werden"),p("ist … verpflichtend","強制","ist schriftlich verpflichtend"),p("sind integraler Bestandteil, nicht …","定位","ist Kern, nicht Beiwerk")],
["文化機構治理語言：價值＋程序。"],["文化","規定","正式"]),
(
"b2-50","story","總複習","Was B2 von B1 unterscheidet","B2 與 B1 差在哪",
"""Auf B1 gelingt es oft, Alltag und Beruf funktional zu bewältigen.
B2 verlangt darüber hinaus, Positionen zu nuancieren, Gegenargumente einzubeziehen und Stilregister zu wechseln.
Man schreibt nicht nur, dass etwas problematisch ist, sondern warum, für wen und mit welchen Alternativen.
Mündlich bedeutet das: moderieren, nachfragen, zuspitzen, ohne die Beziehung zu gefährden.
Lesend trifft man auf längere Argumentationsketten und nominalen Stil.
Wer B2 anstrebt, übt deshalb bewusst das Verknüpfen von Standpunkt, Beleg und Einwand.""",
"""在 B1，人們多半能功能性處理日常與工作。
B2 進一步要求細緻表達立場、納入反論，並切換文體層級。
不只寫「有問題」，還要寫為何、對誰、有何替代。
口語上意味：主持、追問、尖銳化，卻不傷害關係。
閱讀上會遇到更長論證鏈與名詞化風格。
以 B2 為目標者，因此要刻意練習：立場—證據—反駁的連結。""",
[n("nuancieren","細緻區辨"),n("Stilregister","文體／語域層級"),n("zuspitzen","尖銳化／聚焦"),n("Argumentationsketten","論證鏈"),n("nominalen Stil","名詞化風格"),n("Einwand","異議／反駁")],
[p("darüber hinaus","除此之外／更進一步","darüber hinaus müssen wir …"),p("nicht nur, dass …, sondern warum …","深化論點","nicht nur dass, sondern wieso"),p("übt bewusst das Verknüpfen von A, B und C","後設學習","übt das Wechseln zwischen Registern")],
["把本篇當 B2 能力地圖，對照自己弱項。","與 B1 相比：更長、更多抽象名詞與反方觀點。"],
["複習","論述","語域","後設"]),
]
B2.extend(pack(t) for t in RAW5)

assert len(B2) == 50, len(B2)

# fix typo Sonstanächst if any
for it in B2:
    it["text"] = it["text"].replace("Sonstanächst", "Sonst")
    it["textZh"] = it["textZh"].replace("不花钱", "不花錢")

data = json.loads(PATH.read_text(encoding="utf-8"))
data["items"] = [i for i in data["items"] if i.get("level") != "B2"]
data["items"].extend(B2)
data["levels"] = ["A1", "A2", "B1", "B2"]
data["note"] = (
    "A1：短句／對話／告示；A2：段落／郵件／公告；"
    "B1：較長文章與正式情境；"
    "B2：論述、專業郵件與複雜文本，含反方觀點與抽象名詞。"
)
PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
lens = [len(i["text"]) for i in B2]
print(f"B2={len(B2)} avg={sum(lens)//len(lens)} min={min(lens)} max={max(lens)} total={len(data['items'])}")
