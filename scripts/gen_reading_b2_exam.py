#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Append 50 exam-length B2 reading items into reading.json (Goethe/ÖSD-style)."""
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
'b2-01','story','社會','Die unsichtbare Arbeit zu Hause','家中看不見的勞動',
"""Viele Gespräche über Beruf und Erfolg blenden die Arbeit im Haushalt aus. Dabei handelt es sich um Tätigkeiten, ohne die Berufstätigkeit kaum möglich wäre: Kochen, Putzen, Organisation von Terminen und emotionale Unterstützung. Studien zeigen, dass diese Aufgaben nach wie vor ungleich verteilt sind, selbst wenn beide Partner erwerbstätig sind.

Wer das Thema anspricht, riskiert Konflikte; wer schweigt, zementiert bestehende Muster. Sinnvoll wäre eine transparente Aufteilung, die regelmäßig überprüft wird. Gerechtigkeit entsteht nicht von allein, sondern durch Vereinbarungen, die man auch einhält.

Dennoch bleibt festzuhalten, dass gesellschaftliche Normen und betriebliche Erwartungen die private Aufteilung stark beeinflussen. Insofern ist die Frage nicht allein privat, sondern auch politisch: Welche Rahmenbedingungen erleichtern eine gerechtere Verteilung? Zum einen fordern Gewerkschaften mehr Flexibilität bei Arbeitszeiten; zum anderen fehlt es vielerorts noch an bezahlbarer Betreuung.

Es bleibt abzuwarten, inwiefern gesetzliche Regelungen und kulturelle Veränderungen tatsächlich zu messbaren Verschiebungen führen. Wer die unsichtbare Arbeit sichtbar macht, leistet bereits einen ersten Schritt, der weitergedacht werden muss.""",
"""許多關於職業與成功的討論，忽略了家務勞動。這指的是若沒有就幾乎無法就業的工作：煮飯、打掃、安排行程與情感支持。研究顯示，即使雙方都就業，這些任務仍常分配不均。

誰提起這話題可能引發衝突；誰沉默則鞏固既有模式。較合理的是透明分配，並定期檢視。公平不會自動出現，而需要人們遵守的約定。

儘管如此，仍須指出：社會規範與職場期待強烈影響私人分工。就這點而言，問題不只是私領域，也是政治問題：哪些制度條件能促進更公平的分配？一方面工會要求工時更有彈性；另一方面許多地方仍缺乏負擔得起的托育。

法規與文化變遷究竟能帶來多少可測量的改變，仍有待觀察。讓看不見的勞動被看見，已是必須繼續延伸的第一步。""",
[n('blenden … aus','排除在外／忽略','ausblenden。'),n('handelt es sich um','這指的是……'),n('nach wie vor','一如既往／仍然'),n('zementiert','鞏固／固化'),n('Insofern','就這點而言／因此'),n('Es bleibt abzuwarten','仍有待觀察'),n('inwiefern','在多大程度上／如何')],
[p('handelt es sich um + 第四格','定義主題','Dabei handelt es sich um ein Missverständnis.'),p('Zum einen …; zum anderen …','雙面論證','Zum einen spart man Zeit; zum anderen steigt der Druck.'),p('Es bleibt abzuwarten, inwiefern …','開放結果','Es bleibt abzuwarten, inwiefern die Reform wirkt.')],
['德檢論說文：現象→兩難→制度層次→開放結論。','標出名詞化：Tätigkeit、Aufteilung、Rahmenbedingungen。','圈出連接詞 dennoch／insofern／zum einen…zum anderen。'],['論述','名詞化','社會','連接詞']),
(
'b2-02','story','媒體','Filterblasen und öffentliche Debatte','同溫層與公共辯論',
"""Algorithmen zeigen uns vor allem Inhalte, die zu unserem bisherigen Verhalten passen. Dadurch entsteht der Eindruck, die eigene Meinung sei gesellschaftlicher Konsens. Wer widersprechende Perspektiven meidet, verliert allmählich die Fähigkeit, Argumente nüchtern zu prüfen.

Das bedeutet nicht, dass man jeder Meinung zustimmen muss; es bedeutet, sie wenigstens zu verstehen. Eine praktische Gegenmaßnahme ist, bewusst Quellen zu wechseln und Behauptungen zu verifizieren. Medienkompetenz besteht weniger im Viel-Konsumieren als im gezielten Hinterfragen.

Kritikerinnen und Kritiker wenden ein, individuelle Vorsätze reichten nicht aus, solange Plattformen Aufmerksamkeit als Ware behandeln. In der Tat werden kontroverse oder vereinfachte Beiträge oft stärker belohnt als differenzierte Einordnungen. Dennoch wäre es verkürzt, Nutzerinnen und Nutzer als reine Opfer darzustellen; Verantwortung verteilt sich auf Technik, Wirtschaft und Öffentlichkeit.

Insofern stellt sich die Frage, welche Regulierungen Transparenz schaffen, ohne legitime Meinungsfreiheit einzuschränken. Es bleibt abzuwarten, inwiefern Kennzeichnungspflichten und Medienbildung tatsächlich die Qualität öffentlicher Debatten verbessern. Bis dahin gilt: Wer informiert mitreden will, muss die Architektur der Filterblase mitdenken.""",
"""演算法主要推播符合我們既有行為的內容。於是容易覺得自己的意見就是社會共識。若回避相反觀點，會逐漸失去冷靜檢視論證的能力。

這不是說必須同意每種意見；而是至少要理解。實用對策是刻意更換來源並查證說法。媒體素養較少在於「看很多」，而在於有意識地追問。

批評者認為，只要平台把注意力當商品，個人立志並不夠。確實，爭議或簡化貼文常比細緻定位更受獎勵。但若把使用者描繪成純粹受害者，也過於簡化；責任分散在技術、經濟與公共領域。

因此要問：哪些規範能提高透明度，又不侵害正當言論自由？標示義務與媒體教育究竟能改善公共辯論品質到什麼程度，仍有待觀察。在此之前：想知情發言，就必須一併思考同溫層的結構。""",
[n('bisherigen Verhalten','既有行為'),n('Konsens','共識'),n('verifizieren','查證'),n('wenden ein','提出異議'),n('dennoch','儘管如此'),n('Insofern','就這點而言'),n('Kennzeichnungspflichten','標示義務')],
[p('Dadurch entsteht der Eindruck, … sei …','結果＋虛擬間接','Dadurch entsteht der Eindruck, alles sei klar.'),p('weniger im A als im B','重點轉移','weniger im Reden als im Handeln'),p('Es bleibt abzuwarten, inwiefern …','開放評價','Es bleibt abzuwarten, inwiefern die Regel hilft.')],
['先畫『現象→個人對策→制度反論→開放結語』。','注意虛擬式 sei：間接呈現印象。','德檢常考：作者立場是否完全否定個人責任？'],['媒體','論述','虛擬式','反論']),
(
'b2-03','story','環境','Die Kosten der Bequemlichkeit','便利的代價',
"""Same-Day-Delivery wirkt wie ein Luxus, der kaum etwas kostet. Tatsächlich werden die wahren Kosten oft ausgelagert: an Fahrerinnen und Fahrer, an Verpackungsmüll, an überlastete Innenstädte. Konsumentinnen und Konsumenten entscheiden unter Zeitdruck und sehen selten die gesamte Lieferkette.

Wenn Preise die gesellschaftlichen Folgekosten nicht abbilden, entsteht ein falscher Anreiz. Mögliche Korrekturen wären höhere Transparenz und Alternativen, die etwas langsamer, aber nachhaltiger sind. Bequemlichkeit ist nicht falsch; Blindheit gegenüber ihren Folgen schon.

Unternehmen entgegnen, Kundschaft verlange Geschwindigkeit und werde sonst zur Konkurrenz abwandern. Zum einen ist dieser Druck real; zum anderen gestaltet die Branche selbst Erwartungen mit, indem sie Extremgeschwindigkeit als Normalfall vermarktet. Während einzelne Städte Zufahrtsregeln verschärfen, bleibt die nationale Koordination lückenhaft.

Es stellt sich daher die Frage, inwiefern politische Rahmenbedingungen den Wettbewerb fairer machen können, ohne Versorgungssicherheit zu gefährden. Solange externe Kosten unsichtbar bleiben, wird Bequemlichkeit weiterhin zu billig erscheinen. Eine informierte Öffentlichkeit könnte wenigstens verlangen, dass Lieferversprechen ehrlich über Umwelt- und Sozialfolgen Auskunft geben.""",
"""當日達看起來像幾乎不花錢的奢侈。實際上，真實成本常被轉嫁：給司機、給包裝垃圾、給超負荷的市區。消費者在時間壓力下決策，很少看見整條供應鏈。

若價格未反映社會後果成本，就會產生錯誤誘因。可能的修正包括提高透明度，以及稍慢但更永續的替代方案。便利本身沒錯；對其後果視而不見才有問題。

企業反駁：顧客要速度，否則會流向競爭對手。一方面壓力確實存在；另一方面產業也透過把極速當成常態來行銷，自己形塑了期待。在部分城市加嚴進出規則之際，全國協調仍殘缺。

因此要問：政治框架能在多大程度上讓競爭更公平，又不危及供應安全？只要外部成本看不見，便利就會繼續顯得太便宜。至少，知情的公眾可以要求：配送承諾必須誠實說明環境與社會後果。""",
[n('ausgelagert','外包／轉嫁'),n('Folgekosten','後果成本'),n('Anreiz','誘因'),n('entgegnen','反駁'),n('Während','正當……之際／而'),n('inwiefern','在多大程度上'),n('Versorgungssicherheit','供應安全')],
[p('Wenn …, entsteht …','條件→後果','Wenn Preise lügen, entsteht Fehlsteuerung.'),p('Zum einen …; zum anderen …','雙面','Zum einen real; zum anderen selbstgemacht.'),p('Es stellt sich die Frage, inwiefern …','提問套語','Es stellt sich die Frage, inwiefern das hilft.')],
['對照『個人消費』與『產業／政策』兩層論證。','標出被動與名詞化：werden ausgelagert、Folgekosten。','德檢：誰被呈現為責任主體？'],['環境','消費','反論','名詞化']),
(
'b2-04','story','健康','Prävention jenseits von Appellen','呼籲之外的預防',
"""Öffentliche Kampagnen fordern regelmäßig mehr Bewegung, weniger Zucker und ausreichend Schlaf. Solche Appelle sind nicht falsch, treffen jedoch Menschen unter sehr unterschiedlichen Bedingungen. Wer Schicht arbeitet, lange Pendelwege hat oder in beengten Wohnungen lebt, kann Ratschläge nur begrenzt umsetzen.

Deshalb verschiebt sich die Debatte zunehmend von individueller Disziplin hin zu struktureller Prävention: Stadtplanung, Arbeitszeiten, Schulverpflegung und Zugänglichkeit von Sportangeboten. Während Appelle moralisieren, verändern Strukturen den Handlungsspielraum. Dennoch bleibt persönliche Verantwortung relevant; sie sollte nur nicht als alleinige Erklärung für Gesundheitsunterschiede dienen.

Zum einen belegen Studien den Nutzen früher Interventionen; zum anderen zeigt die Praxis, dass Angebote oft diejenigen erreichen, die ohnehin schon sensibilisiert sind. Insofern müssen Präventionsprogramme aktiv Ungleichheit mitdenken, statt neutrale Tipps zu verbreiten.

Es bleibt abzuwarten, inwiefern Kommunen und Betriebe Prävention als Investition begreifen und nicht nur als Imagepflege. Solange Gesundheitspolitik vor allem Symptome behandelt, bleibt Vorbeugung rhetorisch stark und praktisch schwach.""",
"""公共宣導經常呼籲多運動、少糖、充足睡眠。這些呼籲本身沒錯，卻落在條件差異很大的人身上。輪班、長通勤或住得擁擠者，只能有限落實建議。

因此辯論逐漸從個人紀律轉向結構性預防：都市計畫、工時、學校伙食與運動設施近用。呼籲容易道德化，結構則改變行動空間。儘管如此，個人責任仍重要；只是不該被當成健康差距的唯一解釋。

一方面研究證實早期介入有效；另一方面實務顯示，方案常先觸及本來就已有意識的人。因此預防計畫必須主動納入不平等，而非只發「中立」小撇步。

縣市與企業是否把預防當投資而非形象工程，仍有待觀察。只要健康政策主要處理症狀，預防就會停留在口號強、實作弱。""",
[n('Appelle','呼籲／勸誡'),n('beengten Wohnungen','擁擠的住所'),n('Handlungsspielraum','行動空間'),n('moralisieren','道德化批評'),n('Insofern','因此／就這點'),n('Imagepflege','形象維護'),n('Vorbeugung','預防')],
[p('Während A …, verändern B …','對照','Während Appelle mahnen, schaffen Regeln Raum.'),p('Zum einen …; zum anderen …','雙面證據','Zum einen wirkt es; zum anderen erreicht es Wenige.'),p('Es bleibt abzuwarten, inwiefern …','開放','Es bleibt abzuwarten, inwiefern Betriebe investieren.')],
['區分『個人呼籲』與『結構措施』兩條論線。','注意作者並未完全否定個人責任。','德檢：找出讓步句（Dennoch…）。'],['健康','社會','論述','結構']),
(
'b2-05','story','教育','Noten, Leistung und Motivation','分數、表現與動機',
"""Noten sollen Leistung vergleichbar machen und Orientierung geben. Zugleich erzeugen sie Druck, der Lernen auf Strategie reduziert: Was wird geprüft, was kann ich weglassen? Viele Lernende berichten, dass Neugier schwindet, sobald Bewertung im Vordergrund steht.

Befürworterinnen und Befürworter entgegnen, ohne Noten fehle Transparenz für Bewerbungen und Übergänge. Das Argument wiegt schwer, insofern Bildungssysteme weiterhin selektieren. Dennoch stellt sich die Frage, ob Alternativen – Portfolios, formative Rückmeldungen, kompetenzorientierte Berichte – Selektion gerechter gestalten könnten.

Während manche Schulen experimentieren, bleiben bundesweite Standards zögerlich. Zum einen fürchten Eltern Nachteile im Wettbewerb; zum anderen fehlen Ressourcen für intensive individuelle Begleitung. Nominalstil und Passiv in Reformpapieren verdecken oft, wer Verantwortung trägt: „Es wird empfohlen, Feedbackkulturen zu stärken.“

Es bleibt abzuwarten, inwiefern digitale Tools echte Rückmeldung ersetzen oder nur beschleunigen. Wer Motivation erhalten will, muss Bewertung so gestalten, dass Fehler als Information gelten – nicht als endgültiges Urteil über Fähigkeiten.""",
"""分數本應讓表現可比較並提供方向。同時也造成壓力，使學習淪為策略：考什麼、可省略什麼？許多學習者表示，一旦評量成焦點，好奇心就消退。

支持者反駁：沒有分數，申請與升學就缺乏透明度。這點有分量，因為教育體系仍在篩選。但仍要問：作品集、形成性回饋、能力導向報告等替代方案，能否讓篩選更公平？

部分學校在實驗，全國標準卻仍躊躇。一方面家長擔心競爭吃虧；另一方面密集個別輔導資源不足。改革文件的名詞化與被動常掩蓋誰負責：「建議強化回饋文化。」

數位工具究竟是取代真實回饋，還是只加速流程，仍有待觀察。若想保住動機，評量必須讓錯誤成為資訊——而非對能力的最終判決。""",
[n('vergleichbar','可比較的'),n('formative Rückmeldungen','形成性回饋'),n('zögerlich','躊躇／遲疑'),n('Nominalstil','名詞化文體'),n('Feedbackkulturen','回饋文化'),n('endgültiges Urteil','最終判決'),n('entgegnen','反駁')],
[p('Das Argument wiegt schwer, insofern …','承認論點','Das Argument wiegt schwer, insofern Stellen knapp sind.'),p('Während …, bleiben …','對照進度','Während Schulen testen, bleiben Gesetze starr.'),p('Es wird empfohlen, … zu …','被動建議','Es wird empfohlen, früh zu informieren.')],
['找出作者對『分數不可或缺』的部分承認。','圈出改革文件裡的被動與名詞化。','德檢常問：替代方案的阻礙是什麼？'],['教育','評量','被動','反論']),
(
'b2-06','story','科技','Homeoffice und die neue Normalität','居家辦公與新常態',
"""Was während der Pandemie als Notlösung galt, ist für viele Branchen zur Option geworden. Homeoffice spart Wege, erleichtert die Vereinbarkeit und kann Konzentration fördern. Zugleich berichten Teams von Entgrenzung: Arbeit dringt in den Abend, Meetings multiplizieren sich, informeller Austausch schwindet.

Führungskräfte stehen vor der Aufgabe, Leistung zu bewerten, ohne Präsenz mit Engagement zu verwechseln. Wer nur misst, wer online ist, verfehlt den Kern. Dennoch darf Autonomie nicht bedeuten, dass Überlastung privatisiert wird. Klare Kernzeiten, erreichbare Ansprechpersonen und respektierte Offline-Phasen wären Mindeststandards.

Zum einen verlangen Beschäftigte Flexibilität; zum anderen brauchen Organisationen Verlässlichkeit für Kundschaft und Kolleginnen. Während hybride Modelle Kompromisse suchen, bleiben Fragen der Fairness offen: Wer hat zu Hause einen ruhigen Arbeitsplatz, wer nicht?

Insofern ist Digitalisierung kein reiner Gewinn. Es bleibt abzuwarten, inwiefern Tarifverträge und Betriebsvereinbarungen die neue Normalität sozial absichern. Technik ermöglicht Distanz; Kultur entscheidet, ob Distanz Isolierung oder Entlastung bedeutet.""",
"""疫情期間被視為應急方案的做法，如今在許多產業成了選項。居家辦公省通勤、利於兼顧生活，也可能提升專注。同時團隊回報界線模糊：工作侵入夜晚、會議倍增、非正式交流減少。

主管的任務是評量績效，卻不能把「在場」誤當「投入」。只盯誰在線，就偏離核心。但自主也不該意味過勞被私有化。明確核心時段、可聯繫窗口與受尊重的離線時段，應是最低標準。

一方面員工要彈性；另一方面組織要對顧客與同事保持可靠。混合模式尋求折衷時，公平問題仍在：誰家有安靜工作空間，誰沒有？

因此數位化並非純收益。勞資協議與企業協議能否為新常態提供社會保障，仍有待觀察。技術讓距離成為可能；文化則決定距離是孤立還是減壓。""",
[n('Vereinbarkeit','兼顧（工作與生活）'),n('Entgrenzung','界線消失'),n('verwechseln','混淆'),n('privatisiert','被私有化'),n('Betriebsvereinbarungen','企業協議'),n('sozial absichern','提供社會保障'),n('hybride Modelle','混合模式')],
[p('Was … galt, ist … geworden','昔今對照','Was Notlösung galt, ist Option geworden.'),p('darf nicht bedeuten, dass …','劃界','Autonomie darf nicht bedeuten, dass Hilfe fehlt.'),p('Technik ermöglicht X; Kultur entscheidet …','雙層結論','Technik erlaubt Tempo; Kultur setzt Grenzen.')],
['對照『彈性好處』與『過勞／公平』。','注意 Mindeststandards 清單。','德檢：作者對完全遠距持何保留？'],['職場','數位化','公平','論述']),
(
'b2-07','story','消費','Nachhaltiger Konsum zwischen Anspruch und Alltag','永續消費：理想與日常',
"""Viele Menschen möchten nachhaltiger konsumieren, stoßen im Alltag jedoch auf Widersprüche. Bio-Produkte sind teurer, Reparaturdienste rar, und Werbung verspricht ständig Neues. Wer unter Zeitdruck einkauft, greift zu dem, was verfügbar und bezahlbar ist.

Unternehmen reagieren mit Siegeln und Nachhaltigkeitsberichten. Manche Kennzeichnungen helfen; andere verwirren eher. Kritiker sprechen von Greenwashing, wenn Imagepflege die Geschäftsmodell-Logik unangetastet lässt. Dennoch wäre es unfair, jede Verbesserung als Täuschung abzutun: schrittweise Veränderungen können real sein, auch wenn sie unzureichend bleiben.

Während Politik Mindeststandards setzen kann, bleibt Kaufverhalten relevant. Zum einen erzeugen Nachfrageverschiebungen Marktdruck; zum anderen entlastet ein reiner Appell an Konsumenten die Produzenten. Insofern braucht es beides: informierte Nachfrage und verbindliche Regeln.

Es bleibt abzuwarten, inwiefern Recht auf Reparatur und längere Gewährleistung den Wegwerfzyklus verlangsamen. Nachhaltiger Konsum beginnt nicht mit Perfektion, sondern mit der Bereitschaft, Bequemlichkeit und Kosten ehrlich gegeneinander abzuwägen.""",
"""許多人想更永續地消費，日常卻撞上矛盾。有機較貴、維修服務稀少，廣告又不斷承諾「新的」。時間緊時，人們會拿得到且付得起的。

企業以標章與永續報告回應。有些標示有幫助；有些反而令人困惑。當形象工程未碰觸商業模式邏輯時，批評者稱為漂綠。但把每項改善都打成欺騙也不公平：逐步改變可以是真的，即使仍不足。

政策可設最低標準，購買行為仍重要。一方面需求轉移形成市場壓力；另一方面只呼籲消費者會讓生產者卸責。因此需要兩者：知情需求與具約束力的規則。

修復權與更長保固能否減緩用完即棄循環，仍有待觀察。永續消費不從完美開始，而從願意誠實權衡便利與成本開始。""",
[n('stoßen auf','撞上／遇到'),n('Greenwashing','漂綠'),n('unangetastet','未受觸動'),n('abzutun','輕率否定'),n('verbindliche Regeln','具約束力的規則'),n('Wegwerfzyklus','用完即棄循環'),n('abzuwägen','權衡')],
[p('Manche …; andere …','區分','Manche helfen; andere verwirren.'),p('Dennoch wäre es unfair, …','讓步公正','Dennoch wäre es unfair, alles abzulehnen.'),p('braucht es beides: A und B','雙重要求','braucht es Transparenz und Kontrolle.')],
['標出作者對 Greenwashing 的『承認＋修正』。','Recht auf Reparatur 常成考點詞。','德檢：結論是只要個人改變就夠嗎？'],['消費','環境','反論','政策']),
(
'b2-08','story','政治社會','Bürgerbeteiligung jenseits der Wahl','選舉之外的公民參與',
"""Demokratie beschränkt sich nicht auf den Wahlakt. Bürgerinnen und Bürger können sich in Beiräten, Petitionen, Bürgerhaushalten und lokalen Initiativen einbringen. Dennoch bleibt Beteiligung oft ungleich: Wer Zeit, Bildung und Netzwerke besitzt, wird eher gehört.

Verfahren, die Beteiligung ermöglichen sollen, können paradoxerweise ausschließen, wenn sie kompliziert formuliert oder schlecht beworben sind. Während Online-Formate Reichweite versprechen, fehlen manchen Gruppen Zugang oder Vertrauen. Zum einen erhöhen digitale Tools die Geschwindigkeit; zum anderen vertiefen sie digitale Spaltungen, sofern keine Begleitung stattfindet.

Insofern muss gute Beteiligung barrierearm, frühzeitig und ergebnisoffen gestaltet werden. Scheinpartizipation – also Anhören ohne echte Einflussnahme – untergräbt Legitimität nachhaltiger als gar keine Beteiligung. Es bleibt abzuwarten, inwiefern Kommunen Lernprozesse aus gelungenen Formaten systematisch übernehmen.

Wer Mitgestaltung ernst nimmt, akzeptiert auch, dass Entscheidungen länger dauern und Kompromisse sichtbar werden. Das ist unbequem, aber demokratisch produktiver als schnelle Beschlüsse hinter verschlossenen Türen.""",
"""民主不只限於投票。公民可透過諮詢會、請願、參與式預算與地方倡議投入。但參與常不均等：有時間、教育與網絡者較容易被聽見。

本應促進參與的程序，若措辭複雜或宣傳不足，反而可能排除人。線上形式承諾觸及面，但部分群體缺乏近用或信任。一方面數位工具加快速度；另一方面若無陪同，也加深數位落差。

因此良好參與必須低障礙、及早、結果開放。假參與——只聽不真實影響——對正當性的傷害，可能比完全不參與更持久。縣市能否系統吸收成功格式的經驗，仍有待觀察。

認真看待共同形塑，就得接受決策較慢、妥協被看見。這很麻煩，但比關起門來快速拍板更有助民主。""",
[n('Wahlakt','投票行為'),n('Bürgerhaushalten','參與式預算'),n('paradoxerweise','弔詭地'),n('barrierearm','低障礙'),n('Scheinpartizipation','假參與'),n('untergräbt','侵蝕／削弱'),n('ergebnisoffen','結果開放的')],
[p('können paradoxerweise …','弔詭效果','Regeln können paradoxerweise ausschließen.'),p('sofern keine … stattfindet','條件','sofern keine Begleitung stattfindet'),p('Das ist unbequem, aber …','評價權衡','Das ist teuer, aber nachhaltiger.')],
['區分『有程序』與『真能影響』。','注意不平等參與的社會條件。','德檢：作者對線上參與的保留為何？'],['政治社會','參與','公平','論述']),
(
'b2-09','story','文化','Kulturelle Teilhabe und Ticketpreise','文化近用與票價',
"""Theater, Museen und Konzerthäuser gelten als Orte öffentlicher Bildung und Begegnung. Gleichzeitig schrecken hohe Ticketpreise und ungeschriebene Verhaltensregeln viele potenzielle Besuchende ab. Kulturelle Teilhabe bleibt damit teilweise ein Privileg, auch wenn Häuser formal allen offenstehen.

Subventionen sollen Zugänge sichern; dennoch reichen Ermäßigungen nicht aus, wenn Informationskanäle und Programmgestaltung bestimmte Gruppen kaum ansprechen. Während „Lange Nächte“ und Gratisstunden Reichweite erhöhen, bleibt die Frage, ob einmalige Events nachhaltige Bindung schaffen.

Zum einen argumentieren Institutionen mit gestiegenen Produktionskosten; zum anderen droht ein Image als elitäre Veranstaltung, wenn Preise und Kommunikation exclusiv wirken. Insofern braucht Kulturpolitik beides: solide Finanzierung und aktive Öffnung.

Es bleibt abzuwarten, inwiefern digitale Formate echte Teilhabe erweitern oder nur ein Ersatzpublikum im Netz erzeugen. Wer Kultur als öffentliche Aufgabe versteht, muss messen, wer kommt – und wer systematisch fehlt.

Kritikerinnen entgegnen, Kostendruck sei real und Subventionen begrenzt. Dennoch bleibt kulturelle Teilhabe ein öffentliches Gut, das nicht allein dem Markt überlassen werden sollte. Wer nur zahlungskräftiges Publikum bedient, verengt den gesellschaftlichen Dialog.""",
"""劇場、博物館與音樂廳被視為公共教育與相遇之所。同時高票價與不成文規矩也嚇退許多潛在觀眾。即使場館形式上對所有人開放，文化近用仍部分是特權。

補助本應保障近用；但若資訊渠道與節目設計幾乎碰不到某些群體，優惠仍不夠。雖然「長夜」活動與免費時段擴大觸及，仍要問：一次性活動能否形成持久連結？

一方面機構以製作成本上升論證；另一方面若價格與溝通顯得排外，就有菁英活動之形象風險。因此文化政策需要兩者：穩固經費與主動開放。

數位形式是擴張真實近用，還是只在網路上製造替代觀眾，仍有待觀察。若把文化當公共任務，就必須測量誰來了——以及誰系統性地缺席。

批評者反駁：成本壓力真實，補助有限。但文化近用仍是公共財，不應只交給市場。若只服務付得起的觀眾，社會對話就會變窄。""",
[n('schrecken … ab','嚇退'),n('ungeschriebene Verhaltensregeln','不成文規矩'),n('Subventionen','補助'),n('Ermäßigungen','優惠／減免'),n('elitäre','菁英式的'),n('exclusiv','排外／專屬'),n('systematisch fehlt','系統性缺席')],
[p('gelten als …','被視為','gelten als Orte der Bildung'),p('reichen … nicht aus, wenn …','不足條件','reichen Tipps nicht aus, wenn Zeit fehlt'),p('braucht … beides: A und B','雙軌','braucht Geld und Öffnung')],
['對照『形式開放』與『實質近用』。','注意作者要求『測量誰缺席』。','德檢：補助被認為足夠嗎？'],['文化','近用','政策','論述']),
(
'b2-10','story','交通','Mobilität zwischen Autofreundlichkeit und Klimazielen','交通：汽車友善與氣候目標之間',
"""Städtische Mobilität steht unter doppeltem Druck: Klimaziele verlangen weniger Emissionen, während viele Haushalte auf das Auto angewiesen bleiben. ÖPNV-Ausbau, Radwege und Tempo-30-Zonen werden diskutiert, stoßen aber auf Widerstand, sobald Parkplätze oder Fahrzeiten betroffen sind.

Befürworter dichterer Netze verweisen auf Gesundheits- und Aufenthaltsqualität; Gegnerinnen und Gegner warnen vor Belastung von Pendlerinnen und Lieferverkehr. Beide Perspektiven enthalten berechtigte Punkte. Dennoch führt eine reine Polarisierung selten zu tragfähigen Kompromissen.

Während einzelne Städte experimentieren, fehlen oft regionale Tarife und verlässliche Taktungen über Gemeindegrenzen hinweg. Zum einen investieren Kommunen in Infrastruktur; zum anderen entscheidet der Alltag über Annahme: Unpünktlichkeit und Überfüllung untergraben Vertrauen schnell.

Insofern ist Verkehrswende nicht nur Technikfrage, sondern Verteilungsfrage: Wer trägt Kosten und Unannehmlichkeiten der Umstellung? Es bleibt abzuwarten, inwiefern bundeseinheitliche Standards lokale Konflikte entschärfen. Ohne spürbare Alternativen bleibt das Auto für viele die rationale Wahl – auch wenn sie klimapolitisch problematisch ist.""",
"""都市交通承受雙重壓力：氣候目標要求減排，同時許多家庭仍仰賴汽車。大眾運輸擴建、自行車道與時速30區被討論，但一旦影響停車位或車程就遭抗拒。

支持更密集路網者以健康與停留品質為據；反對者警告通勤者與貨運負擔。雙方都有合理之處。但純對立少能產生可支撐的妥協。

部分城市在實驗，跨行政區的區域票價與可靠班距卻常不足。一方面縣市投資基礎建設；另一方面日常決定是否被接受：誤點與擁擠很快侵蝕信任。

因此交通轉型不只是技術問題，也是分配問題：誰承擔轉換的成本與不便？全國一致標準能否緩和地方衝突，仍有待觀察。若無明顯替代，汽車對許多人仍是理性選擇——即使就氣候政策而言有問題。""",
[n('angewiesen bleiben','仍仰賴'),n('ÖPNV','大眾運輸'),n('tragfähigen Kompromissen','可支撐的妥協'),n('Taktungen','班距／發車頻率'),n('untergraben','侵蝕'),n('Verkehrswende','交通轉型'),n('entschärfen','緩和')],
[p('steht unter doppeltem Druck','雙重壓力','steht unter Zeit- und Kostendruck'),p('Beide Perspektiven enthalten …','平衡承認','Beide Seiten haben Punkte.'),p('Ohne … bleibt … die rationale Wahl','條件結論','Ohne Alternative bleibt das Auto Wahl.')],
['找出『氣候 vs. 日常依賴』張力。','注意分配問題：誰負擔轉換成本。','德檢：作者是否主張立即禁車？'],['交通','環境','妥協','政策']),
(
'b2-11','story','職場','Fachkräftemangel und Arbeitsbedingungen','缺工與勞動條件',
"""In vielen Branchen wird über Fachkräftemangel gesprochen. Gemeint sind fehlende qualifizierte Beschäftigte, die offene Stellen besetzen könnten. Gleichzeitig berichten Bewerberinnen und Bewerber von befristeten Verträgen, hoher Belastung und begrenzten Aufstiegschancen. Die Diagnose „Mangel“ erklärt daher nur einen Teil der Lage.

Unternehmen werben mit Homeoffice und Benefits, während grundlegende Fragen der Bezahlung und Planbarkeit oft ungelöst bleiben. Wer langfristig binden will, muss Verlässlichkeit bieten. Dennoch allein höhere Löhne zu fordern, greift zu kurz, sofern Schichtsysteme und Anerkennungskulturen unattraktiv bleiben.

Zum einen investieren Betriebe in Weiterbildung; zum anderen fehlt es an Zeit, Erlerntes tatsächlich anzuwenden. Während die Politik Zuwanderung erleichtert, bleibt die Anerkennung ausländischer Abschlüsse bürokratisch. Insofern ist Fachkräftesicherung eine organisatorische und gesellschaftliche Aufgabe zugleich.

Es bleibt abzuwarten, inwiefern Tarifbindung und bessere Ausbildungskapazitäten den Druck mindern. Solange „Mangel“ vor allem als Imageproblem behandelt wird, ändern sich Arbeitsbedingungen nur langsam.""",
"""許多產業談論缺工，意指缺少能填補職缺的合格人力。同時求職者回報定期契約、高負荷與有限升遷。因此「短缺」診斷只解釋部分現況。

企業以居家與福利招募，基本薪資與可預期性問題卻常未解。若要長期留才，必須提供可靠。但若輪班與承認文化仍無吸引力，只喊加薪也太短視。

一方面企業投資進修；另一方面缺少把所學真正用上的時間。政策放寬移入之際，外國學歷承認仍官僚。因此人力確保同時是組織與社會任務。

團體協約覆蓋與更好的培訓能量能否減輕壓力，仍有待觀察。只要「短缺」主要被當形象問題處理，勞動條件就只會緩慢改變。""",
[n('Fachkräftemangel','專業人力短缺'),n('befristeten Verträgen','定期契約'),n('Planbarkeit','可預期性'),n('greift zu kurz','過於短視／不足'),n('Anerkennungskulturen','承認／肯定文化'),n('Tarifbindung','團體協約適用'),n('Ausbildungskapazitäten','培訓能量')],
[p('Gemeint sind …','澄清所指','Gemeint sind fehlende Fachkräfte.'),p('greift zu kurz, sofern …','批評不足','Die Forderung greift zu kurz, sofern …'),p('ist … Aufgabe zugleich','雙重定位','ist technische und soziale Aufgabe zugleich')],
['對照『缺人敘事』與『條件問題』。','注意承認外國學歷的官僚點。','德檢：作者認為只加薪夠嗎？'],['職場','勞動','政策','論述']),
(
'b2-12','story','數位化','Künstliche Intelligenz im Büroalltag','辦公室日常中的人工智慧',
"""Textgeneratoren und Analysewerkzeuge halten Einzug in den Büroalltag. Sie beschleunigen Entwürfe, sortieren Informationen und übernehmen Routineaufgaben. Gleichzeitig entstehen Unsicherheiten: Welche Daten dürfen verarbeitet werden, wer haftet für Fehler, und wie bleibt Expertise erhalten, wenn Maschinen Formulierungen liefern?

Optimistische Stimmen betonen Produktivitätsgewinne; skeptische mahnen vor Entwertung von Tätigkeiten und vor blinder Vertrauensseligkeit. Beide Seiten haben Anhaltspunkte. Dennoch hilft weder Technikfeindlichkeit noch unkritischer Enthusiasmus weiter.

Während Leitlinien entstehen, hinkt die Schulungspraxis hinterher. Zum einen brauchen Teams klare Regeln für vertrauliche Inhalte; zum anderen müssen Prüfkompetenzen gestärkt werden, damit Ergebnisse nicht ungeprüft übernommen werden. Insofern verändert KI weniger den Beruf als solchen, sondern die Anforderungen an Urteilskraft.

Es bleibt abzuwarten, inwiefern Betriebsvereinbarungen Transparenz über eingesetzte Systeme schaffen. Wer KI sinnvoll nutzen will, behandelt sie als Werkzeug mit Grenzen – nicht als Ersatz für Verantwortung.""",
"""文本生成與分析工具進入辦公室日常。它們加速草稿、整理資訊並承接例行工作。同時產生不安：哪些資料可處理、錯誤誰負責、機器提供措辭時專業如何保存？

樂觀者強調生產力；懷疑者警告工作被貶值與盲目信任。雙方都有依據。但仇視技術或無批判熱情都無濟於事。

準則出現之際，培訓實務卻落後。一方面團隊需要機密內容的清楚規則；另一方面必須強化檢核能力，以免結果未經查證就被採用。因此 AI 改變的比較不是職業本身，而是對判斷力的要求。

企業協議能否讓所用系統透明，仍有待觀察。想善用 AI，就把它當有界限的工具——而非責任的替代。""",
[n('halten Einzug','進入／登場'),n('haftet für','對……負責'),n('Vertrauensseligkeit','輕信'),n('Anhaltspunkte','依據／線索'),n('hinkt … hinterher','落後於'),n('Prüfkompetenzen','檢核能力'),n('Urteilskraft','判斷力')],
[p('halten Einzug in …','進入某領域','halten Einzug in den Unterricht'),p('mahnen vor …','警告提防','mahnen vor blinder Nutzung'),p('behandelt sie als … – nicht als …','定位','behandelt KI als Werkzeug – nicht als Chef')],
['標出資料保護與責任問題。','注意『判斷力』結論。','德檢：作者支持全面自動化嗎？'],['科技','職場','責任','論述']),
(
'b2-13','story','住房','Wohnraum, Miete und soziale Mischung','住房、租金與社會混居',
"""In wachsenden Städten wird bezahlbarer Wohnraum zur zentralen sozialen Frage. Steigende Mieten verdrängen Haushalte mit mittlerem und niedrigem Einkommen an den Rand oder aus der Stadt. Gleichzeitig entstehen luxussanierte Viertel, in denen langfristig gewachsene Nachbarschaften verschwinden.

Politik reagiert mit Mietpreisbremsen, sozialem Wohnungsbau und Genossenschaftsmodellen. Die Wirkung bleibt umstritten: Manche Instrumente dämpfen, andere erzeugen Ausweichreaktionen. Dennoch ohne Eingriffe den Markt allein regieren zu lassen, verschärft Ungleichheit sichtbar.

Während Neubau Flächen und Ressourcen braucht, steht Leerstand an anderer Stelle ungenutzt. Zum einen fordern Investoren Planbarkeit; zum anderen brauchen Mieterinnen Schutz vor abrupten Erhöhungen. Insofern ist Wohnungspolitik immer Abwägung zwischen Eigentumsrechten und Teilhabe am städtischen Leben.

Es bleibt abzuwarten, inwiefern bundeseinheitliche Standards lokale Engpässe lindern. Soziale Mischung entsteht nicht von allein; sie erfordert aktive Steuerung, die Verdrängung ernst nimmt, ohne Mobilität zu verteufeln.

Mieterinitiativen fordern verbindliche Quoten für geförderten Wohnraum in Neubauprojekten. Investoren warnen vor Investitionszurückhaltung. Eine nüchterne Politik muss beide Risiken benennen und Prioritäten transparent setzen.""",
"""在成長中的城市，負擔得起的住房成了核心社會問題。房租上漲把中低收入戶推到邊緣或趕出城市。同時出現豪宅化街區，長期形成的鄰里消逝。

政策以租金管制、社會住宅與合作社模式回應。效果有爭議：有些工具能抑制，有些引發規避。但不干預、放任市場，會明顯加劇不平等。

新建需要土地與資源之際，他處空屋卻閒置。一方面投資者要可預期；另一方面房客需要免於驟漲的保護。因此住房政策總是在財產權與城市生活近用之間權衡。

全國標準能否緩解地方瓶頸，仍有待觀察。社會混居不會自動出現；它需要認真對待迫遷、又不妖魔化流動性的積極治理。

房客倡議要求新建案強制納入補貼住宅比例。投資者警告投資卻步。務實政策必須點名雙方風險並透明排優先。""",
[n('verdrängen','排擠／迫遷'),n('luxussanierte','豪宅整修的'),n('Mietpreisbremsen','租金管制'),n('Ausweichreaktionen','規避反應'),n('Leerstand','空屋／空置'),n('Abwägung','權衡'),n('verteufeln','妖魔化')],
[p('wird … zur zentralen Frage','成為核心問題','wird Bildung zur zentralen Frage'),p('Dennoch ohne … zu lassen','反事實批評','Dennoch den Markt allein regieren zu lassen …'),p('entsteht nicht von allein','非自動','Gerechtigkeit entsteht nicht von allein')],
['對照管制工具與市場邏輯。','注意『混居需積極治理』。','德檢：作者是否主張完全自由市場？'],['住房','社會','政策','權衡']),
(
'b2-14','story','移民／融合','Sprache, Arbeit und Ankommen','語言、工作與安頓',
"""Ankommen in einer neuen Gesellschaft bedeutet mehr als einen Aufenthaltsstatus. Sprache, Anerkennung von Qualifikationen und soziale Kontakte entscheiden mit darüber, ob Teilhabe gelingt. Viele Zugewanderte bringen Kompetenzen mit, stoßen jedoch auf Wartezeiten, bürokratische Hürden und unsichere Beschäftigungsverhältnisse.

Integrationskurse und Beratungsangebote sind wichtige Bausteine; sie ersetzen jedoch keine fairen Zugänge zum Arbeitsmarkt. Während einzelne Betriebe aktiv ausbilden und begleiten, bleiben Vorbehalte an anderer Stelle spürbar. Zum einen braucht gelingende Integration klare Regeln; zum anderen gelingt sie besser, wo Willkommen nicht nur rhetorisch bleibt.

Dennoch wäre es verkürzt, Herausforderungen allein den Neuankömmlingen zuzuschreiben. Aufnahmegesellschaften verändern sich ebenfalls und müssen Ressourcen sowie Konfliktkultur ernst nehmen. Insofern ist Integration ein beiderseitiger Prozess mit Rechten und Pflichten.

Es bleibt abzuwarten, inwiefern beschleunigte Anerkennungsverfahren und sprachsensible Ausbildungsgänge Teilhabe messbar verbessern. Eine nüchterne Debatte vermeidet sowohl Illusionen als auch pauschale Abwertung.""",
"""在新社會安頓，不只是居留身分。語言、資格承認與社會聯繫，共同決定近用能否成功。許多移入者帶來能力，卻碰上等待、官僚關卡與不穩定就業。

融合課程與諮詢是重要組成，但不能取代公平的勞動市場近用。部分企業積極培訓陪同之際，他處偏見仍可感。一方面成功融合需要清楚規則；另一方面在「歡迎」不只停於修辭之處，效果更好。

但若把挑戰全歸因於新來者，也過於簡化。接收社會同樣在變，必須認真看待資源與衝突文化。因此融合是雙方過程，含權利與義務。

加速承認程序與對語言敏感的培訓路徑能否可測量地改善近用，仍有待觀察。冷靜辯論既避幻想，也避一概貶低。""",
[n('Aufenthaltsstatus','居留身分'),n('Zugewanderte','移入者'),n('bürokratische Hürden','官僚關卡'),n('Bausteine','組成要件'),n('Vorbehalte','保留／偏見'),n('beiderseitiger Prozess','雙向過程'),n('pauschale Abwertung','一概貶低')],
[p('bedeutet mehr als …','不只是','bedeutet mehr als Formalität'),p('Während …, bleiben …','對照','Während Betriebe helfen, bleiben Vorbehalte'),p('vermeidet sowohl A als auch B','雙避','vermeidet Panik und Verharmlosung')],
['注意中立表述：雙方過程、權利義務。','標出勞動市場近用關鍵。','德檢：作者把責任只放在移入者嗎？'],['融合','社會','勞動','中立']),
(
'b2-15','story','媒體','Meinungsvielfalt in lokalen Medien','地方媒體的意見多元',
"""Lokale Zeitungen und Sender gelten als Seismografen des Alltags: sie berichten über Gemeinderäte, Vereine und Konflikte vor Ort. Durch Einsparungen schrumpfen Redaktionen, und Nachrichtenagenturen füllen Lücken. Dadurch droht eine Vereinheitlichung, die regionale Besonderheiten unsichtbar macht.

Plattformen bieten zwar Reichweite, ersetzen jedoch investigative Recherche selten. Während Bürgerjournalismus Impulse liefert, fehlen oft Standards der Prüfung. Zum einen retten Kooperationen zwischen Häusern Stellen; zum anderen steigt die Abhängigkeit von wenigen Portalen.

Dennoch bleibt lokale Berichterstattung demokratisch relevant, weil sie Kontrolle und Zugehörigkeit ermöglicht. Insofern ist Medienvielfalt keine Luxusdebatte, sondern Infrastrukturfrage. Es bleibt abzuwarten, inwiefern öffentliche Förderungen Unabhängigkeit stärken oder neue Abhängigkeiten erzeugen.

Wer informierte Mitbestimmung will, braucht verlässliche Quellen in der Nähe – nicht nur nationale Schlagzeilen. Qualität kostet; ihr Fehlen kostet langfristig Vertrauen.

Ohne lokale Medien schrumpft die Fähigkeit der Öffentlichkeit, Verwaltungshandeln zu kontrollieren. Spendenmodelle und Genossenschaften experimentieren; ihre Reichweite bleibt jedoch ungleich. Qualität braucht nachhaltige Finanzierung jenseits kurzfristiger Klicks.""",
"""地方報紙與電台被視為日常的測震儀：報導市議會、社團與地方衝突。因節省，編輯部縮小，通訊社填補空缺。於是出現齊一化風險，使地區特色看不見。

平台雖有觸及面，卻很少取代調查報導。公民新聞帶來刺激之際，查證標準常不足。一方面館際合作保住職缺；另一方面對少數入口網站依賴上升。

但地方報導對民主仍重要，因它促成監督與歸屬。因此媒體多元不是奢侈辯論，而是基礎建設問題。公共補助是強化獨立，還是製造新依賴，仍有待觀察。

想要知情共治，需要附近可靠來源——而不只是全國頭條。品質有成本；其缺席長期侵蝕信任。

沒有地方媒體，公眾監督行政的能力會萎縮。捐款模式與合作社在實驗，觸及面仍不均。品質需要超越短期點擊的永續經費。""",
[n('Seismografen','測震儀／敏銳指標'),n('investigative Recherche','調查採訪'),n('Bürgerjournalismus','公民新聞'),n('Vereinheitlichung','齊一化'),n('Mitbestimmung','共治／共同決定'),n('Förderungen','補助'),n('Abhängigkeiten','依賴')],
[p('gelten als …','被視為','gelten als Seismografen'),p('ersetzen jedoch … selten','否定替代','ersetzen Recherche selten'),p('Qualität kostet; ihr Fehlen kostet …','對句','Zeit kostet; Hektik kostet Fehler')],
['對照『覆蓋面』與『調查深度』。','注意補助的雙面風險。','德檢：地方媒體為何與民主有關？'],['媒體','地方','民主','論述']),
(
'b2-16','story','教育','Digitale Schule zwischen Chance und Überforderung','數位學校：機會與過載之間',
"""Tablets, Lernplattformen und Videokonferenzen haben den Unterricht verändert. Sie ermöglichen individualisiertes Tempo und Zugang zu Materialien außerhalb der Schule. Gleichzeitig berichten Lehrkräfte von Technikproblemen, Datenschutzfragen und einer zusätzlichen Vorbereitungslast.

Eltern erwarten moderne Ausstattung, während Ausstattung allein noch keinen didaktischen Gewinn garantiert. Wer Tools ohne Konzept einsetzt, multipliziert Ablenkung. Dennoch auf analoge Formate zu beharren, ignoriert Kompetenzen, die Absolventinnen später brauchen.

Zum einen fehlen flächendeckende Fortbildungen; zum anderen unterscheiden sich Schulen stark nach Ressourcen. Insofern verstärkt Digitalisierung bestehende Ungleichheiten, sofern Finanzierung und Begleitung ungleich bleiben. Es bleibt abzuwarten, inwiefern landesweite Standards Mindestqualität sichern.

Sinnvolle digitale Bildung misst Erfolg nicht an Gerätezahl, sondern daran, ob Lernen verständlicher, gerechter und nachhaltiger wird. Technik ist Mittel – nicht Selbstzweck.

Eltern und Lehrkräfte brauchen klare Ansprechstrukturen, wenn Technik ausfällt oder Datenschutzfragen entstehen. Fortbildung muss verpflichtend und praxisnah sein, sonst bleibt Digitalisierung Stückwerk. Evaluation sollte didaktischen Nutzen messen, nicht nur Gerätezahlen.""",
"""平板、學習平台與視訊會議改變了教學。它們使個別節奏與校外教材近用成為可能。同時教師回報技術故障、個資問題與額外備課負擔。

家長期待現代設備，但設備本身不保證教學收益。沒有概念就用工具，只會讓分心加倍。但死守類比形式，也忽略畢業生日後需要的能力。

一方面缺乏全面進修；另一方面學校資源差異大。若經費與陪同不均，數位化會加剧既有不平等。全國標準能否守住最低品質，仍有待觀察。

有意義的數位教育不以設備數量衡量成功，而看學習是否更易懂、更公平、更持久。技術是手段——不是目的本身。

技術故障或個資疑問出現時，家長與教師需要清楚窗口。進修必須義務且貼近實務，否則數位化只是零碎工程。評估應測教學效益，而非只數設備。""",
[n('individualisiertes Tempo','個別化節奏'),n('Vorbereitungslast','備課負擔'),n('didaktischen Gewinn','教學收益'),n('flächendeckende Fortbildungen','全面進修'),n('Mindestqualität','最低品質'),n('Selbstzweck','自我目的'),n('beharren auf','堅持')],
[p('ermöglichen … Gleichzeitig berichten …','利弊並列','ermöglichen Tempo. Gleichzeitig berichten …'),p('Dennoch auf … zu beharren, ignoriert …','批評固執','Dennoch auf Papier zu beharren, ignoriert …'),p('misst Erfolg nicht an A, sondern daran, ob …','改寫指標','misst nicht an Klicks, sondern daran, ob …')],
['區分『有設備』與『有教學概念』。','注意不平等被強化的條件句。','德檢：作者把技術當目的嗎？'],['教育','數位化','公平','論述']),
(
'b2-17','story','健康','Psychische Belastung am Arbeitsplatz','職場心理負荷',
"""Burn-out und Erschöpfung sind aus dem öffentlichen Gespräch nicht mehr wegzudenken. Dennoch werden psychische Belastungen in vielen Betrieben erst thematisiert, wenn Ausfälle bereits sichtbar sind. Prävention bleibt nachgeordnet, obwohl frühe Signale – Reizbarkeit, Schlafprobleme, Rückzug – erkennbar wären.

Führungskräfte stehen unter eigenem Druck und fehlen manchmal an Gesprächskompetenz. Schulungen helfen, ersetzen jedoch keine realistische Personalplanung. Während Gesundheitsangebote wie Yoga-Kurse symbolisch wirken, bleiben Überstundenkulturen unangetastet.

Zum einen schützen Betriebsärztinnen Vertraulichkeit; zum anderen scheuen Beschäftigte Offenheit aus Angst vor Nachteilen. Insofern braucht psychische Gesundheit strukturelle Entlastung und eine Kultur, in der Grenzen respektiert werden.

Es bleibt abzuwarten, inwiefern gesetzliche Gefährdungsbeurteilungen ernsthaft umgesetzt werden. Wer nur individuelle Resilienz trainiert, individualisiert ein organisatorisches Problem.

Kollegiale Unterstützung und transparente Arbeitsplanung sind wirksamer als Appelle zur Self-Care allein. Betriebsräte können Gefährdungsbeurteilungen einfordern und Maßnahmen nachhalten. Gesundheitsschutz endet nicht beim Sportangebot in der Mittagspause.""",
"""過勞與耗竭已無法從公共討論中抹去。但許多企業要到缺勤已可見才談心理負荷。預防仍居次，儘管易怒、睡眠問題、退縮等早期訊號本可辨識。

主管自身也有壓力，有時缺乏對談能力。培訓有助益，卻不能取代務實的人力規劃。健康方案如瑜伽課看似象徵，加班文化卻未觸動。

一方面企業醫師保護機密；另一方面員工因怕吃虧而不敢坦誠。因此心理健康需要結構性減壓，以及尊重界線的文化。

法定危害評估是否被認真執行，仍有待觀察。若只訓練個人韌性，就把組織問題個人化了。

同儕支持與透明工作規畫，比單靠自我照顧呼籲更有效。企業委員會可要求危害評估並追蹤措施。健康保護不止於午休運動課。""",
[n('wegzudenken','想像沒有','nicht wegzudenken＝不可或缺'),n('nachgeordnet','居次的'),n('Reizbarkeit','易怒'),n('Überstundenkulturen','加班文化'),n('Gefährdungsbeurteilungen','危害評估'),n('Resilienz','韌性'),n('individualisiert','個人化（歸責）')],
[p('sind … nicht mehr wegzudenken','已不可或缺','sind aus dem Alltag nicht wegzudenken'),p('ersetzen jedoch keine …','有限效用','Schulungen ersetzen keine Planung'),p('individualisiert ein … Problem','歸責轉移','individualisiert ein Systemproblem')],
['對照象徵性方案與結構原因。','注意『個人化組織問題』批評。','德檢：作者認為瑜伽課夠嗎？'],['健康','職場','預防','結構']),
(
'b2-18','story','環境','Hitze in der Stadt','城市裡的熱',
"""Hitzewellen treffen Städte besonders hart. Versiegelte Flächen speichern Wärme, Grün fehlt, und nächtliche Abkühlung bleibt aus. Ältere Menschen, chronisch Kranke und Outdoor-Beschäftigte sind überproportional gefährdet. Was früher als seltene Ausnahme galt, wird zur wiederkehrenden Belastung.

Kommunen pflanzen Bäume, öffnen Kühlräume und passen Bauleitplanung an. Dennoch reichen Einzelmaßnahmen nicht, wenn Neubauten weiterhin maximale Versiegelung priorisieren. Während Klimaanlagen kurzfristig entlasten, erhöhen sie Energieverbrauch und verlagern Wärme nach draußen.

Zum einen braucht es verbindliche Grünflächenquoten; zum anderen müssen Warnsysteme verständlich und mehrsprachig sein. Insofern ist Hitzeanpassung soziale Infrastruktur. Es bleibt abzuwarten, inwiefern Förderprogramme auch benachteiligte Viertel erreichen.

Wer nur auf Technik setzt, übersieht, dass Schatten, Wasser und Nachbarschaftshilfe oft wirksamer und gerechter sind. Stadtklima ist Gestaltungssache – nicht Schicksal.

Bauordnungen können Hellhörigkeit und Verschattung verbindlich regeln, wenn politischer Wille vorhanden ist. Bürgerinitiativen dokumentieren Hitzeinseln und fordern prioritäre Investitionen in belastete Viertel. Anpassung ist verteilt gerecht zu gestalten.""",
"""熱浪對城市特別嚴酷。硬化地表蓄熱、綠地不足、夜間降溫缺席。長者、慢性病患與戶外工作者承受不成比例風險。昔日罕見例外，正變成反覆負荷。

縣市種樹、開設降溫空間並調整都市計畫。但若新建仍優先最大硬化，單點措施不夠。空調短期減壓之際，也提高能耗並把熱排到室外。

一方面需要具約束力的綠覆率；另一方面預警系統必須好懂且多語。因此熱適應是社會基礎建設。補助方案能否也到達弱勢街區，仍有待觀察。

只押寶技術，會忽略陰影、水源與鄰居互助往往更有效也更公平。城市氣候是可設計的——不是命運。

若有政治意志，建築規範可強制透風與遮蔭。公民團體記錄熱島並要求優先投資受影響街區。調適應以分配正義方式設計。""",
[n('Versiegelte Flächen','硬化地表'),n('überproportional','不成比例地'),n('Bauleitplanung','都市計畫'),n('verlagern','轉移'),n('Grünflächenquoten','綠覆率／綠地配額'),n('benachteiligte Viertel','弱勢街區'),n('Gestaltungssache','可設計之事')],
[p('Was … galt, wird zur …','昔今','Was Ausnahme galt, wird zur Regel'),p('reichen … nicht, wenn …','不足','reichen Apps nicht, wenn Schatten fehlt'),p('ist … – nicht …','重新定義','ist Gestaltung – nicht Schicksal')],
['連結氣候與社會不平等。','對照空調短期／長期效應。','德檢：誰被點名為高風險群體？'],['環境','城市','公平','適應']),
(
'b2-19','story','文化','Sprache im Wandel','變動中的語言',
"""Sprachen verändern sich ständig: neue Wörter entstehen, Bedeutungen verschieben sich, Register mischen sich. Manche Beobachterinnen sehen darin Verfall; andere erkennen lebendige Anpassung. Historisch betrachtet ist Wandel der Normalfall, nicht die Ausnahme.

Öffentliche Debatten entzünden sich oft an Anredeformen, Anglizismen oder gendergerechter Sprache. Während die einen Verständlichkeit und Tradition betonen, verweisen die anderen auf Sichtbarkeit und Respekt. Beide Anliegen sind nachvollziehbar. Dennoch führt moralische Eskalation selten zu sprachlicher Klarheit.

Zum einen brauchen Institutionen Leitfäden; zum anderen bleibt Alltagssprache vielfältig und situativ. Insofern ist Sprachpolitik immer Abwägung zwischen Inklusion und Lesbarkeit. Es bleibt abzuwarten, inwiefern empirische Studien tatsächliche Verständnishürden belegen.

Wer Sprache pflegen will, sollte Neugier vor Empörung setzen. Präzision entsteht durch Übung und Kontextbewusstsein – nicht durch pauschale Verbote.

Schulen und Redaktionen können Sprachwandel erklären, statt nur zu skandalisieren. Wer Begriffe ablehnt, sollte Alternativen und Gründe nennen. So entsteht Debatte statt Lagerbildung, und Präzision bleibt ein gemeinsames Ziel.""",
"""語言不斷改變：新詞出現、意義挪移、語域混雜。有人視為衰退；有人看作活生生的適應。從歷史看，變動才是常態，不是例外。

公共辯論常引爆於稱呼、英語借詞或性別包容用語。一方強調可懂與傳統，另一方指向可見與尊重。兩者都可理解。但道德升級很少帶來語言清晰。

一方面機構需要指引；另一方面日常語言仍多元且依情境。因此語言政策總在包容與可讀之間權衡。實證研究能否證明真實理解障礙，仍有待觀察。

想呵護語言，應把好奇放在憤怒之前。精確來自練習與語境意識——而非一概禁止。

學校與編輯部可以解釋語言變化，而非只炒作。拒絕某詞者應提出替代與理由。如此產生辯論而非陣營，精確仍是共同目標。""",
[n('Register','語域／文體層級'),n('Verfall','衰退'),n('entzünden sich an','因……引爆'),n('gendergerechter Sprache','性別包容用語'),n('nachvollziehbar','可理解的'),n('Inklusion','包容'),n('pauschale Verbote','一概禁止')],
[p('Historisch betrachtet ist …','歷史視角','Historisch betrachtet ist Wandel normal'),p('Während die einen …, verweisen die anderen …','雙方','Während A warnt, verweist B auf …'),p('sollte Neugier vor Empörung setzen','優先序','sollte Fragen vor Urteilen setzen')],
['作者對『變動＝衰退』持何態度？','標出包容／可讀權衡。','德檢：結論強調好奇而非禁令。'],['文化','語言','辯論','權衡']),
(
'b2-20','story','科技','Überwachung im öffentlichen Raum','公共空間的監控',
"""Kameras und automatische Auswertungssysteme werden mit Sicherheitsargumenten begründet. Sie sollen Straftaten abschrecken und Aufklärung erleichtern. Gleichzeitig wächst die Sorge, dass permanente Beobachtung Verhaltensspielräume einengt und Unschuldige unter Generalverdacht stellt.

Befürworter verweisen auf Erfolge bei der Aufklärung; Kritikerinnen fragen nach Fehlalarmraten, Diskriminierung und Speicherfristen. Während Technik präziser wird, bleibt rechtliche Kontrolle entscheidend. Dennoch Transparenz allein genügt nicht, wenn Betroffene kaum Widerspruchsmöglichkeiten haben.

Zum einen können gezielte Einsätze sinnvoll sein; zum anderen droht schleichende Ausweitung ohne öffentliche Debatte. Insofern muss jede Ausweitung begründungspflichtig und befristet sein. Es bleibt abzuwarten, inwiefern unabhängige Aufsichtsstellen Wirksamkeit und Nebenfolgen prüfen.

Sicherheit und Freiheit stehen nicht in einfachem Nullsummenspiel, aber Abwägungen müssen sichtbar bleiben. Wer Schutz will, sollte auch Schutz der Grundrechte meinen.

Gerichte und Datenschutzbehörden setzen zunehmend Grenzen für biometrische Auswertung. Transparente Löschfristen und Auskunftsrechte sind Mindestbedingungen. Ohne sie droht Gewöhnung an Kontrolle, die später schwer rückgängig zu machen ist.""",
"""鏡頭與自動分析系統常以安全論證合理化。它們應嚇阻犯罪並利於破案。同時憂慮上升：持續監視壓縮行為空間，並使無辜者處於全面嫌疑。

支持者指向破案成效；批評者追問誤報率、歧視與保存期限。技術更精準之際，法律控管仍關鍵。但若當事人幾乎無法異議，僅有透明也不夠。

一方面針對性部署可能合理；另一方面恐在缺乏公共辯論下悄然擴大。因此每次擴大必須可說理且有期限。獨立監督機構能否檢視成效與副作用，仍有待觀察。

安全與自由並非簡單零和，但權衡必須可見。要保護，也應意味保護基本權利。

法院與個資機關日益為生物辨識分析設限。透明刪除期限與查詢權是最低條件。若無，恐習慣於監控，日後難逆轉。""",
[n('abschrecken','嚇阻'),n('Verhaltensspielräume','行為空間'),n('Generalverdacht','全面嫌疑'),n('Fehlalarmraten','誤報率'),n('schleichende Ausweitung','悄然擴大'),n('begründungspflichtig','必須說明理由'),n('Nullsummenspiel','零和遊戲')],
[p('werden mit … begründet','以……合理化','werden mit Sicherheit begründet'),p('genügt nicht, wenn …','不足條件','Transparenz genügt nicht, wenn …'),p('muss … begründungspflichtig und befristet sein','雙重要求','muss prüfbar und befristet sein')],
['對照安全成效與權利風險。','注意『悄然擴大』論點。','德檢：作者要求什麼程序條件？'],['科技','權利','安全','權衡']),
(
'b2-21','email','職場','Stellungnahme zu einem Projektstopp','專案停擺聲明',
"""Sehr geehrte Damen und Herren,

hiermit nehme ich Stellung zu der Entscheidung, das Projekt „Nordlicht“ vorübergehend zu stoppen. Zwar verstehe ich die budgetären Gründe; gleichwohl halte ich die Kommunikation für unzureichend. Weder Team noch externe Partner wurden frühzeitig eingebunden, sodass Unsicherheit und Gerüchte entstanden sind.

Aus fachlicher Sicht wäre es möglich gewesen, einen abgespeckten Zwischenstand zu sichern, statt sämtliche Arbeiten abzubrechen. Die bislang erzielten Ergebnisse drohen an Wert zu verlieren, sofern keine dokumentierte Übergabe erfolgt. Zum einen stehen vertragliche Fristen mit dem Auftraggeber; zum anderen ist die Motivation der Mitarbeitenden spürbar gesunken.

Ich schlage daher vor, innerhalb von zehn Tagen einen Alternativplan vorzulegen, der Meilensteine, Risiken und benötigte Mindestressourcen klar benennt. Nur so lässt sich Vertrauen wiederherstellen und ein geordneter Neustart vorbereiten. Es bleibt abzuwarten, inwiefern die Geschäftsleitung diese Empfehlung aufgreift; ich bitte jedenfalls um eine schriftliche Rückmeldung bis Freitag.

Mit freundlichen Grüßen
Dr. Elena Vogt
Projektleitung""",
"""敬啟者：

謹就「Nordlicht」專案暫時停擺之決定提出說明。我雖理解預算理由，但仍認為溝通不足。團隊與外部夥伴皆未及早參與，因而產生不安與謠傳。

就專業而言，本可保住精簡的中期成果，而非中斷全部工作。若不做書面交接，既有成果價值恐流失。一方面與委託方有契約期限；另一方面同仁動機明顯下滑。

因此建議十日內提出替代計畫，清楚列出里程碑、風險與最低所需資源。唯有如此才能重建信任並準備有序重啟。經營層是否採納此建議仍有待觀察；無論如何請於週五前書面回覆。

此致問候
Elena Vogt 博士
專案負責人""",
[n('nehme ich Stellung zu','就……表態'),n('vorübergehend','暫時地'),n('gleichwohl','儘管如此'),n('abgespeckten','精簡的'),n('lässt sich … wiederherstellen','能夠被重建'),n('Mindestressourcen','最低資源'),n('schriftliche Rückmeldung','書面回覆')],
[p('hiermit nehme ich Stellung zu …','正式表態','Hiermit nehme ich Stellung zu Ihrem Schreiben.'),p('Zwar …; gleichwohl …','讓步對立','Zwar teuer; gleichwohl sinnvoll.'),p('Nur so lässt sich …','唯一途徑','Nur so lässt sich das Problem lösen.')],
['正式立場信：承認理由＋指出缺口＋具體期限。','標出 gleichwohl／sofern 等書面連接。','德檢：找出具體提議與期限。'],['正式郵件','論證','職場']),
(
'b2-22','email','教育','Antrag auf Verlängerung der Abgabefrist','申請延長繳交期限',
"""Sehr geehrte Frau Professorin Keller,

hiermit beantrage ich eine Verlängerung der Abgabefrist für meine Hausarbeit um zwei Wochen. Aufgrund einer unvorhergesehenen familiären Belastung sowie verzögerter Bibliothekszugänge konnte ich die Quellenarbeit nicht im geplanten Umfang abschließen. Die Themenstellung bleibt unverändert; lediglich der Zeitplan muss angepasst werden.

Ich habe bereits einen Gliederungsentwurf und die Hälfte der Literaturrecherche fertiggestellt. Eine Verlängerung würde mir ermöglichen, Argumentation und Gegenpositionen sorgfältiger auszuarbeiten, statt unter Zeitdruck zu vereinfachen. Zum einen möchte ich wissenschaftliche Sorgfalt wahren; zum anderen respektiere ich die organisatorischen Zwänge Ihres Lehrstuhls.

Sollten Sie dem Antrag zustimmen, reiche ich die Arbeit verbindlich bis zum 28. des Monats ein und stehe für Rückfragen in der Sprechstunde zur Verfügung. Es wäre hilfreich, wenn Sie mir kurz schriftlich bestätigen könnten, ob die Verlängerung gewährt wird. Für Ihr Verständnis danke ich im Voraus.

Mit freundlichen Grüßen
Jonas Hartmann

Sollten zusätzliche Nachweise erforderlich sein, reiche ich diese umgehend nach. Ich versichere, dass die Verlängerung ausschließlich der Qualität der Arbeit dient und nicht der Themenänderung.""",
"""敬愛的 Keller 教授：

謹申請將報告繳交期限延長兩週。因突發家庭負擔與圖書館近用延誤，資料工作未能如期完成。題目不變，僅需調整時程。

大綱草稿與半數文獻檢索已完成。延期將使我能更仔細處理論證與反論，而非在時間壓力下簡化。一方面想維持學術嚴謹；另一方面也尊重貴研究室的行政限制。

若蒙同意，我保證於本月28日前繳交，並可於面談時間接受詢問。若能短暫書面確認是否核准延期，將有幫助。先行感謝您的體諒。

此致問候
Jonas Hartmann

若需額外證明，我會立即補交。我保證延期只為報告品質，而非更改題目。""",
[n('beantrage','申請'),n('unvorhergesehenen','未預見的'),n('Quellenarbeit','資料／文獻工作'),n('Gegenpositionen','反論立場'),n('verbindlich','保證／有約束力地'),n('gewährt wird','被核准'),n('im Voraus','先行／預先')],
[p('hiermit beantrage ich …','正式申請','Hiermit beantrage ich Urlaub.'),p('würde mir ermöglichen, … statt …','條件利益','würde ermöglichen zu prüfen statt zu raten'),p('Sollten Sie …, reiche ich …','禮貌條件','Sollten Sie zustimmen, liefere ich …')],
['申請信：理由具體＋已完成進度＋明確新期限。','注意虛擬 würde ermöglichen。','德檢：作者是否改變題目？'],['郵件','學術','請求']),
(
'b2-23','email','消費','Beschwerde über mangelhafte Lieferung','瑕疵配送申訴',
"""Sehr geehrte Damen und Herren,

am 12. dieses Monats erhielt ich die Bestellung Nr. 45821. Leider entsprach die Lieferung weder der Beschreibung noch dem vereinbarten Liefertermin. Zwei Artikel wiesen Beschädigungen auf, ein dritter fehlte vollständig. Die Verpackung war unzureichend gepolstert, sodass ein Transportschaden nahelegt.

Ich habe den Schaden fotografisch dokumentiert und füge die Bilder sowie den Lieferschein bei. Gemäß Ihren Allgemeinen Geschäftsbedingungen erwarte ich innerhalb von sieben Tagen Ersatzlieferung oder vollständige Erstattung. Eine Gutschrift allein für die beschädigten Teile wäre unzureichend, da der fehlende Artikel den Gebrauch der übrigen unmöglich macht.

Sollte keine zeitnahe Lösung erfolgen, behalte ich mir vor, die Verbraucherzentrale einzuschalten und den Vorgang zu widerrufen. Zum einen wünsche ich eine unkomplizierte Klärung; zum anderen muss Verlässlichkeit für Kundinnen und Kunden gewährleistet bleiben. Bitte bestätigen Sie den Eingang dieser Nachricht schriftlich.

Mit freundlichen Grüßen
Mara Stein

Für Rückfragen bin ich werktags telefonisch und per E-Mail erreichbar. Ich gehe von einer kundenorientierten Lösung aus und dokumentiere den weiteren Schriftverkehr.""",
"""敬啟者：

本月12日我收到訂單45821。遺憾配送既不符說明，也未守約定交期。兩件有損，第三件完全缺失。包裝緩衝不足，顯示可能為運輸損害。

我已拍照存證，並附上圖片與送貨單。依貴公司條款，我期待七日內換貨或全額退款。僅就受損件開立折讓並不足夠，因為缺件使其餘無法使用。

若未能及時解決，我保留向消費者中心求助並撤銷交易之權利。一方面希望無事化解決；另一方面必須維持對顧客的可靠。請書面確認收悉本信。

此致問候
Mara Stein

平日可電話或電郵聯繫。我期待以顧客為導向的解決，並會記錄後續往來。""",
[n('entsprach weder … noch …','既不符……也不……'),n('gepolstert','有緩衝包裝'),n('nahelegt','顯示／暗示'),n('Erstattung','退款'),n('behalte ich mir vor','我保留……權利'),n('widerrufen','撤銷'),n('gewährleistet','獲保障')],
[p('entsprach weder A noch B','雙否定符合','entsprach weder Preis noch Qualität'),p('Gemäß … erwarte ich …','依規要求','Gemäß Vertrag erwarte ich Nachbesserung'),p('behalte ich mir vor, …','保留權利','behalte mir vor, zu klagen')],
['申訴信：事實→證據→法律／條款依據→後續步驟。','圈出 Frist（七日）。','德檢：為何僅部分折讓不夠？'],['郵件','消費','申訴']),
(
'b2-24','email','職場','Rückmeldung zum Praktikumszeugnis','對實習證明的回饋',
"""Sehr geehrte Frau Lehmann,

vielen Dank für das übersandte Praktikumszeugnis. Ich schätze die ausführliche Darstellung meiner Aufgaben. Gleichwohl bitte ich um eine Korrektur in zwei Punkten, die für spätere Bewerbungen wesentlich sind.

Erstens entspricht die Datumsangabe des Praktikumsendes nicht dem tatsächlich letzten Arbeitstag; korrekt ist der 31. März. Zweitens fehlt der Hinweis auf die eigenständige Betreuung der Kundenumfrage, die ich geplant, ausgewertet und präsentiert habe. Diese Leistung wurde intern positiv bewertet und sollte im Zeugnis sichtbar sein.

Ich verstehe, dass Zeugnisse knappe Formulierungen verlangen. Dennoch wäre eine präzise Ergänzung im Interesse beider Seiten, da sie die tatsächliche Verantwortung widerspiegelt. Anbei sende ich einen Formulierungsvorschlag, den Sie selbstverständlich anpassen können. Für eine kurze Rückmeldung bis Ende der Woche wäre ich dankbar.

Mit freundlichen Grüßen
Luis Berger

Mir ist bewusst, dass Zeugnisformulierungen knappen Konventionen folgen. Gerade deshalb bitte ich um präzise, belastbare Formulierungen statt allgemeiner Floskeln. Für Rückfragen stehe ich kurzfristig zur Verfügung und danke erneut für die Betreuung während des Praktikums.""",
"""敬愛的 Lehmann 女士：

感謝寄來的實習證明。我重視對任務的詳盡描述。但仍請就兩點對日後求職至關重要的內容更正。

第一，實習結束日期與實際最後工作日不符；正確為3月31日。第二，缺少我獨立負責顧客問卷——含規劃、分析與報告——的說明。此表現內部評價正面，應在證明中可見。

我理解證明需精簡措辭。但精確補充符合雙方利益，因其反映真實職責。附件為措辭建議，您當然可調整。若能在本週末前短暫回覆，感激不盡。

此致問候
Luis Berger

我理解證明措辭遵循精簡慣例。正因如此，請用精確可檢驗的表述，而非空泛套語。如有疑問我可盡快說明，並再次感謝實習期間的指導。""",
[n('übersandte','寄來的'),n('Gleichwohl','儘管如此'),n('entspricht … nicht','不符'),n('eigenständige Betreuung','獨立負責'),n('widerspiegelt','反映'),n('Formulierungsvorschlag','措辭建議'),n('Anbei','附件隨信')],
[p('Gleichwohl bitte ich um …','禮貌堅持','Gleichwohl bitte ich um Korrektur.'),p('Erstens … Zweitens …','條列','Erstens Daten, zweitens Aufgaben'),p('wäre … im Interesse beider Seiten','雙贏論證','wäre eine Klärung im Interesse beider')],
['更正信：感謝＋具體兩點＋合作語氣。','注意 Zeugnis 對求職的重要性。','德檢：作者要求什麼補充？'],['郵件','職場','證明']),
(
'b2-25','email','環境','Vorschlag zur betrieblichen Mobilität','企業交通改善建議',
"""Sehr geehrte Mitglieder der Geschäftsleitung,

im Anschluss an die letzte Betriebsversammlung möchte ich einen Vorschlag zur betrieblichen Mobilität unterbreiten. Derzeit dominiert das Auto den Arbeitsweg, obwohl die Anbindung an den öffentlichen Verkehr in den letzten Jahren verbessert wurde. Gleichzeitig steigen Parkdruck und Emissionen rund um das Gelände.

Ich schlage ein gestaffeltes Modell vor: Jobticket-Zuschuss, sichere Fahrradstellplätze sowie zwei Homeoffice-Tage für geeignete Tätigkeiten. Zum einen würden Beschäftigte entlastet; zum anderen ließe sich das Nachhaltigkeitsziel der Firma konkretisieren. Eine dreimonatige Pilotphase mit Evaluation könnte Risiken begrenzen.

Kritische Stimmen werden einwenden, Kundentermine erforderten Flexibilität. Dem ist zuzustimmen; gleichwohl betrifft das nicht alle Abteilungen gleichermaßen. Insofern sollte das Modell freiwillig und abteilungsbezogen starten. Ich bitte um einen Termin, um Zahlen und Kostenabschätzungen vorzulegen.

Mit freundlichen Grüßen
Aylin Demir
Betriebsrat

Gerne liefere ich Vergleichszahlen aus ähnlichen Betrieben und eine grobe CO₂-Schätzung für Pendelwege. Eine kurze Rückmeldung, ob Interesse an einem Pilot besteht, würde uns bei der Planung helfen.""",
"""敬愛的經營層成員：

延續上次企業大會，謹提出企業交通建議。目前通勤仍以汽車為主，儘管大眾運輸接駁近年已改善。同時園區周邊停車壓力與排放上升。

我建議分級模式：通勤票補助、安全自行車位，以及適合職務的兩日居家辦公。一方面減輕員工負擔；另一方面可具體化公司永續目標。三個月試辦並評估可限制風險。

批評者會說客戶行程需要彈性。這點可同意；但並非所有部門同樣適用。因此模式應自願並依部門啟動。請安排時間，以便呈報數據與成本估算。

此致問候
Aylin Demir
企業委員會

我樂意提供類似企業比較數據與通勤碳排粗估。若能短暫回覆是否有意試辦，將有助規畫。""",
[n('unterbreiten','提出（建議）'),n('gestaffeltes Modell','分級模式'),n('Jobticket','通勤票'),n('einwenden','提出異議'),n('Dem ist zuzustimmen','這一點可同意'),n('abteilungsbezogen','依部門'),n('Kostenabschätzungen','成本估算')],
[p('möchte ich einen Vorschlag … unterbreiten','正式提案','möchte ich einen Vorschlag unterbreiten'),p('Dem ist zuzustimmen; gleichwohl …','承認＋轉折','Dem ist zuzustimmen; gleichwohl gilt …'),p('sollte … freiwillig und … starten','審慎起步','sollte klein und freiwillig starten')],
['內部提案：現況→措施→反論預答→下一步。','注意 Pilotphase。','德檢：模式是否強制？'],['郵件','環境','職場']),
(
'b2-26','email','健康','Einladung zur Gefährdungsbeurteilung','危害評估邀請',
"""Liebe Kolleginnen und Kollegen,

die jährliche psychische Gefährdungsbeurteilung steht an. Ziel ist es, Belastungsfaktoren frühzeitig zu erkennen und Maßnahmen abzuleiten – nicht, einzelne Personen zu bewerten. Die Teilnahme ist freiwillig, aber wichtig, damit Ergebnisse belastbar sind.

In der Woche vom 5. finden kurze Online-Fragebögen sowie zwei Präsenzworkshops statt. Alle Angaben werden anonymisiert ausgewertet; personenbezogene Rückschlüsse sind nicht vorgesehen. Zum einen hilft Ihre Einschätzung dem Arbeitsschutz; zum anderen fließen Ergebnisse in die Planung von Arbeitszeiten und Pausenräumen ein.

Sollten Sie Bedenken haben, wenden Sie sich vertraulich an den Betriebsarzt oder die Schwerbehindertenvertretung. Es bleibt abzuwarten, welche Schwerpunkte die Auswertung zeigt; bereits jetzt danke ich für Ihre Mitwirkung. Bitte reservieren Sie sich 20 Minuten in Ihrem Kalender.

Freundliche Grüße
Team Arbeitsschutz

Bitte beachten Sie, dass die Auswertung nur auf Gruppenebene berichtet wird. Einzelne Abteilungen erhalten Hinweise, sofern Fallzahlen eine Aussage zulassen, ohne Personen identifizierbar zu machen. Ihre Ehrlichkeit verbessert die Qualität der Maßnahmenplanung erheblich.""",
"""各位同事：

年度心理危害評估即將進行。目標是及早辨識負荷因素並導出措施——而非評價個人。參與自願，但很重要，如此結果才站得住。

5日當週將有短線上問卷與兩場實體工作坊。資料匿名分析；不打算做個人回溯。一方面您的評估有助勞動保護；另一方面結果會納入工時與休息空間規劃。

若有疑慮，可機密聯繫企業醫師或重度身心障礙代表。分析會呈現哪些重點仍有待觀察；先行感謝參與。請在行事曆預留20分鐘。

此致問候
勞動保護小組

請注意分析只在群體層級報告。個別部門僅在樣本足以說明且無法識別個人時獲得提示。您的誠實會大幅提高措施規畫品質。""",
[n('Gefährdungsbeurteilung','危害評估'),n('Belastungsfaktoren','負荷因素'),n('belastbar','站得住／可靠'),n('anonymisiert','匿名化'),n('Schwerbehindertenvertretung','重度身心障礙代表'),n('Mitwirkung','參與／協力'),n('reservieren','預留')],
[p('Ziel ist es, … – nicht …','目的澄清','Ziel ist helfen – nicht bewerten'),p('Zum einen hilft …; zum anderen fließen …','雙益','Zum einen hilft es; zum anderen spart es'),p('Sollten Sie Bedenken haben, …','預答疑慮','Sollten Sie Fragen haben, melden Sie sich')],
['內部通知：目的、匿名、自願、管道。','區分『評估工作』與『評價個人』。','德檢：資料如何處理？'],['郵件','健康','職場']),
(
'b2-27','email','科技','Stellungnahme zur Einführung eines KI-Tools','對導入 AI 工具的聲明',
"""Sehr geehrte IT-Leitung, sehr geehrte Personalabteilung,

im Namen mehrerer Fachbereiche nehme ich Stellung zur geplanten Einführung des Textgenerators „NovaWrite“. Die angekündigte Produktivitätssteigerung ist nachvollziehbar; gleichwohl fehlen bislang verbindliche Regeln zum Umgang mit vertraulichen Kundendaten. Ohne klare Leitlinien drohen Datenschutzverstöße und Qualitätsverluste.

Wir schlagen vor, vor dem Roll-out eine Pilotgruppe von zwölf Personen zu bilden, die drei Wochen lang typische Vorgänge testet und dokumentiert. Dabei sollen Fehlerraten, Zeitersparnis und notwendige Nachbearbeitung gemessen werden. Zum einen ermöglicht dies eine evidenzbasierte Entscheidung; zum anderen können Schulungsbedarfe früh erkannt werden.

Kritisch sehen wir die Idee, KI-Ergebnisse ungeprüft an Kundschaft zu senden. Insofern muss eine Vier-Augen-Prüfung für sensible Schreiben verpflichtend bleiben. Es bleibt abzuwarten, inwiefern Lizenzkosten den Nutzen übersteigen; bitte legen Sie bis zum 15. eine Kosten-Nutzen-Skizze und einen Datenschutzfolgeabschätzungsentwurf vor.

Mit freundlichen Grüßen
Nora Falk
Fachbereich Kommunikation""",
"""敬愛的 IT 主管、人事部門：

我代表多個專責單位，就計畫導入文本生成器「NovaWrite」表態。所稱生產力提升可以理解；但迄今缺少處理機密客戶資料的約束規則。若無清楚準則，恐有個資違規與品質損失。

我們建議上線前組成十二人試用組，以三週測試並記錄典型流程，測量錯誤率、省時與必要後修。一方面利於實證決策；另一方面可及早看出訓練需求。

我們對「AI 結果未經查證就寄給客戶」持批判。因此敏感信件必須維持四人原則檢核。授權費用是否超過效益仍有待觀察；請於15日前提出成本效益草圖與個資影響評估草案。

此致問候
Nora Falk
傳播專責""",
[n('nachvollziehbar','可以理解'),n('verbindliche Regeln','具約束力的規則'),n('Roll-out','全面上線'),n('evidenzbasierte','實證基礎的'),n('Vier-Augen-Prüfung','雙人／四人檢核'),n('Datenschutzfolgeabschätzung','個資影響評估'),n('ungeprüft','未經查證')],
[p('im Namen … nehme ich Stellung','代表表態','Im Namen des Teams nehme ich Stellung'),p('Ohne … drohen …','風險條件','Ohne Regeln drohen Verstöße'),p('muss … verpflichtend bleiben','堅守底線','muss Prüfung verpflichtend bleiben')],
['內部風險信：承認效益＋點出缺口＋試辦設計。','注意 Datenschutzfolgeabschätzung。','德檢：作者要求全面立刻導入嗎？'],['郵件','科技','個資']),
(
'b2-28','email','住房','Schreiben an die Hausverwaltung','致物業管理函',
"""Sehr geehrte Damen und Herren,

seit sechs Wochen ist die Heizung in Wohnung 12 nur eingeschränkt funktionsfähig. Trotz zwei gemeldeter Störungen wurde bislang lediglich ein Provisorium eingerichtet, das die Temperatur in den Abendstunden unter 18 Grad sinken lässt. Die Situation ist insbesondere für die im Haushalt lebende ältere Person unzumutbar.

Gemäß Mietvertrag und ortsüblichen Standards erwarte ich unverzüglich eine fachgerechte Reparatur sowie eine anteilige Mietminderung für den Zeitraum der Beeinträchtigung. Anbei finden Sie die bisherigen Störungsmeldungen mit Daten und Uhrzeiten. Zum einen bitte ich um einen verbindlichen Termin binnen fünf Werktagen; zum anderen um schriftliche Bestätigung der Minderungsquote.

Sollte keine zeitnahe Abhilfe erfolgen, werde ich den Mieterschutzverein einschalten und die weiteren Schritte prüfen lassen. Ich wünsche eine einvernehmliche Lösung und stehe telefonisch unter der bekannten Nummer zur Verfügung. Bitte bestätigen Sie den Eingang dieses Schreibens.

Mit freundlichen Grüßen
Helena Krug

Ich bitte um Verständnis für die Dringlichkeit und um eine verbindliche Auskunft zum Reparaturtermin. Eine weitere Verzögerung ohne Kommunikation ist für uns nicht akzeptabel.""",
"""敬啟者：

十二號房暖氣六週來僅能有限運作。儘管兩次報修，迄今只做臨時處置，晚間溫度降至18度以下。對家中長者而言，此情況難以忍受。

依租約與當地慣常標準，我要求立即專業維修，並就影響期間按比例減租。附件為既有報修紀錄含日期時間。一方面請於五個工作日內給確定時程；另一方面請書面確認減租比例。

若未能及時改善，我將聯繫租屋者保護協會並研擬後續。我希望和解解決，並可透過已知電話聯繫。請確認收悉本函。

此致問候
Helena Krug

請體諒急迫性，並給予維修時程的確定答覆。再無溝通地拖延，我們無法接受。""",
[n('eingeschränkt funktionsfähig','僅能有限運作'),n('Provisorium','臨時處置'),n('unzumutbar','難以忍受／不可期待'),n('Mietminderung','減租'),n('ortsüblichen Standards','當地慣常標準'),n('Abhilfe','改善／救濟'),n('einvernehmliche Lösung','和解方案')],
[p('Trotz … wurde bislang lediglich …','抱怨進展','Trotz Meldung wurde lediglich …'),p('erwarte ich unverzüglich … sowie …','雙重要求','erwarte Reparatur sowie Minderung'),p('Sollte keine …, werde ich …','條件升級','Sollte keine Antwort kommen, werde ich …')],
['租屋申訴：時程、標準、減租、下一步。','標出 unzumutbar 評價詞。','德檢：作者要什麼兩項回覆？'],['郵件','住房','權利']),
(
'b2-29','email','教育','Kooperationsanfrage an eine Hochschule','致大學的合作詢問',
"""Sehr geehrte Frau Dr. Sommer,

unsere Stiftung plant ein Praxisprojekt zu digitaler Teilhabe älterer Menschen und sucht eine wissenschaftliche Partnerin. Ihr Institut hat in den letzten Jahren einschlägige Studien veröffentlicht, deren Methodik uns besonders überzeugt hat. Wir möchten prüfen, inwiefern eine Kooperation für beide Seiten sinnvoll wäre.

Konkret denken wir an eine zwölfmonatige Begleitforschung mit Studierendenbeteiligung sowie gemeinsamen Fachveranstaltungen. Zum einen könnten empirische Daten erhoben werden; zum anderen erhielten Studierende Einblicke in die Projektpraxis. Eine Finanzierungsskizze liegt vor und kann vertraulich zugesandt werden.

Gleichwohl möchten wir keine vorschnellen Erwartungen wecken: Entscheidend ist, ob Kapazitäten und ethische Standards zusammenpassen. Es bleibt abzuwarten, welche Work-Packages realistisch sind. Ich schlage ein dreißigminütiges Online-Gespräch in den nächsten zwei Wochen vor und sende gerne eine Agenda vorab.

Mit freundlichen Grüßen
Omar Belhaj
Projektkoordination

Bei Interesse sende ich vorab ein zweiseitiges Exposé mit Zeitplan und ethischen Leitplanken. Wir freuen uns auf den Austausch und eine mögliche langfristige Zusammenarbeit.""",
"""敬愛的 Sommer 博士：

本基金會規畫高齡數位近用實務專案，尋求學術夥伴。貴所近年發表相關研究，其方法特別令我們信服。想了解合作對雙方是否有意義。

具體構想為十二個月伴隨研究，含學生參與與共同專業活動。一方面可蒐集實證資料；另一方面學生能接觸專案實務。經費草圖已備，可機密寄送。

但仍不想過早拉高期待：關鍵在能量與倫理標準是否契合。哪些工作包務實可行，仍有待觀察。建議兩週內進行三十分鐘線上會談，並可預先寄議程。

此致問候
Omar Belhaj
專案協調

若有興趣，我可先寄兩頁企劃含時程與倫理界線。期待交流與可能的長期合作。""",
[n('einschlägige Studien','相關研究'),n('Begleitforschung','伴隨研究'),n('Finanzierungsskizze','經費草圖'),n('vorschnellen Erwartungen','過早期待'),n('Work-Packages','工作包'),n('Agenda','議程'),n('vertraulich','機密地')],
[p('suchen eine … Partnerin','尋求夥伴','suchen eine wissenschaftliche Partnerin'),p('möchten prüfen, inwiefern …','審慎探詢','möchten prüfen, inwiefern Kooperation lohnt'),p('Gleichwohl möchten wir keine …','降溫期待','Gleichwohl keine falschen Hoffnungen')],
['合作邀約：具體構想＋審慎語氣＋下一步。','注意倫理與能量條件。','德檢：專案主題是什麼？'],['郵件','教育','合作']),
(
'b2-30','email','媒體','Gegendarstellung an eine Redaktion','致編輯部的更正聲明',
"""Sehr geehrte Redaktion,

in Ihrem Online-Beitrag vom 3. März wird behauptet, unser Verein habe Fördermittel zweckwidrig verwendet. Diese Darstellung ist unzutreffend und stützt sich auf eine verkürzte Darstellung interner Umbuchungen, die prüfbar dokumentiert sind. Wir fordern eine zeitnahe Gegendarstellung sowie eine Korrektur der irreführenden Überschrift.

Die angesprochenen Mittel wurden innerhalb des genehmigten Zwecks umgeschichtet, nachdem ein Teilprojekt pandemiebedingt entfiel. Der Vorgang wurde der Bewilligungsbehörde gemeldet; eine Rückforderung liegt nicht vor. Zum einen schädigt die Berichterstattung unseren Ruf; zum anderen erschwert sie die Arbeit mit Partnerorganisationen.

Wir stehen für ein Interview zur Verfügung und übersenden auf Wunsch die relevanten Schreiben. Sollte keine Korrektur erfolgen, behalten wir uns rechtliche Schritte vor, ohne die journalistische Arbeit grundsätzlich infrage zu stellen. Bitte bestätigen Sie den Eingang und nennen Sie eine Ansprechperson.

Mit freundlichen Grüßen
Vorstand „Kulturbrücke e. V.“

Wir bitten ausdrücklich darum, Leserkommentare mit nachweislich falschen Behauptungen zu moderieren, sofern sie unter dem Beitrag fortbestehen. Eine sachliche Berichterstattung liegt im Interesse der Öffentlichkeit.""",
"""敬愛的編輯部：

貴刊3月3日網路報導稱本協會不當使用補助。此說法不實，並基於對內部轉帳的簡化描述；相關文件可查核。我們要求及時刊登更正聲明，並修正誤導標題。

所述款項是在核可用途內重分配，因部分子計畫受疫情影響取消。過程已通報核准機關；並無追回。一方面報導損害聲譽；另一方面妨礙與夥伴機構合作。

我們願接受專訪，並可應要求寄送相關函件。若未更正，我們保留法律途徑，但並非原則否定新聞工作。請確認收悉並告知窗口。

此致問候
「文化橋」協會理事會

若留言區仍有可證偽說法，請予以管理。務實報導符合公共利益。""",
[n('zweckwidrig','不當用途／違目的'),n('unzutreffend','不實的'),n('Gegendarstellung','更正／對等報導'),n('umgeschichtet','重分配'),n('Bewilligungsbehörde','核准機關'),n('Rückforderung','追回／求償'),n('infrage zu stellen','質疑')],
[p('wird behauptet, … habe …','轉述斷言','wird behauptet, X habe …'),p('stützt sich auf …','依據','stützt sich auf Gerüchte'),p('ohne … grundsätzlich infrage zu stellen','限定批評','ohne die Presse infrage zu stellen')],
['更正函：指出錯誤＋反證＋要求＋保留權利。','語氣堅定但不人身攻擊。','德檢：協會要求哪兩件事？'],['郵件','媒體','聲明']),
(
'b2-31','email','交通','Einwand gegen eine Baustellenführung','對工地動線的異議',
"""Sehr geehrte Verkehrsbehörde,

gegen die geplante Umleitung der Buslinie 42 während der Bauarbeiten erhebe ich Einwand. Die vorgesehene Streckenführung verlängert den Arbeitsweg vieler Pendlerinnen um mehr als zwanzig Minuten und umgeht barrierefreie Haltestellen. Insbesondere ältere Fahrgäste sowie Personen mit Kinderwagen sind davon betroffen.

Zwar erkenne ich die Notwendigkeit der Sanierung an; gleichwohl fehlt eine frühzeitige Bürgerinformation und eine Prüfung alternativer Takte. Zum einen könnte ein Shuttle zwischen den betroffenen Haltestellen Abhilfe schaffen; zum anderen wäre eine temporäre Tarifvergünstigung ein Signal der Fairness. Die derzeitige Planung wirkt einseitig auf den Autoverkehr ausgerichtet.

Ich bitte um schriftliche Begründung, inwiefern barrierefreie Alternativen geprüft wurden, und um einen Erörterungstermin vor Baubeginn. Es bleibt abzuwarten, ob Anpassungen möglich sind; ohne sie droht die Akzeptanz der Maßnahme zu sinken. Anbei eine Unterschriftensammlung aus der Nachbarschaft.

Mit freundlichen Grüßen
Ralf Nguyen

Anbei finden Sie Fotos der betroffenen Haltestellen sowie eine grobe Darstellung der Mehrwege. Ich stehe für eine Ortsbegehung zur Verfügung und bitte um Aufnahme in den Verteiler für Bauupdates.""",
"""敬愛的交通主管機關：

就建案期間42路公車改道計畫，我提出異議。預定路線使許多通勤者多花逾二十分鐘，並繞過無障礙站點。長者與推嬰兒車者尤其受影響。

我雖承認整修必要；但仍缺及早的公民資訊與替代班距評估。一方面可用接駁車連接受影響站點；另一方面臨時票價優惠可示公平。目前規畫顯得偏汽車導向。

請書面說明無障礙替代方案檢討到何程度，並在開工前安排說明會。能否調整仍有待觀察；否則措施接受度恐下降。附件為鄰里連署。

此致問候
Ralf Nguyen

附件為受影響站點照片與繞道路徑示意。我可陪同現地會勘，並請加入工程更新通訊名單。""",
[n('erhebe ich Einwand','提出異議'),n('barrierefreie','無障礙的'),n('Takte','班距'),n('Abhilfe schaffen','提供改善'),n('Tarifvergünstigung','票價優惠'),n('Erörterungstermin','說明／討論會'),n('Unterschriftensammlung','連署')],
[p('gegen … erhebe ich Einwand','正式異議','gegen den Plan erhebe ich Einwand'),p('Zwar …; gleichwohl fehlt …','承認＋缺口','Zwar nötig; gleichwohl fehlt Info'),p('wirkt … ausgerichtet','評價導向','wirkt einseitig ausgerichtet')],
['公民異議：受影響群體＋替代建議＋程序要求。','注意 barrierefrei。','德檢：作者完全否定整修嗎？'],['郵件','交通','公民']),
(
'b2-32','email','職場','Absage eines Angebots mit Begründung','附理由的報價婉拒',
"""Sehr geehrte Frau Conti,

vielen Dank für Ihr ausführliches Angebot zur Schulungsreihe „Führen auf Distanz“. Inhalt und Referentinnenprofil überzeugen grundsätzlich. Nach interner Abwägung müssen wir das Angebot dennoch für dieses Quartal absagen.

Ausschlaggebend sind zum einen die Gesamtkosten, die unser Weiterbildungsbudget überschreiten, zum anderen der Terminrahmen, der mit bereits verbindlichen Projektschlussphasen kollidiert. Wir haben geprüft, ob eine verkürzte Variante möglich wäre; die von Ihnen genannte Mindestteilnehmerzahl lässt sich derzeit jedoch nicht erreichen.

Sollten Sie im kommenden Halbjahr Kapazitäten haben, bitten wir um ein angepasstes Konzept für maximal zwei Tage und zwölf Teilnehmende. Es bleibt abzuwarten, inwiefern Budgetumschichtungen Spielraum schaffen. Bis dahin danken wir für die investierte Zeit und die transparente Kalkulation.

Mit freundlichen Grüßen
Kai Okonkwo
Personalentwicklung

Sollten sich unsere Prioritäten verschieben, kommen wir gerne auf Sie zurück. Bis dahin wünschen wir Ihnen weiterhin erfolgreiche Programme und danken für die professionelle und freundliche Kommunikation während der Angebotsphase.""",
"""敬愛的 Conti 女士：

感謝您就「遠距領導」培訓系列提出詳盡報價。內容與講師履歷原則上具說服力。經內部權衡，本季仍須婉拒。

關鍵一方面是總費用超出進修預算，另一方面時程與既定專案收尾衝突。我們評估過縮短版本；但您所提最低人數目前無法達成。

若下半年仍有能量，請提供最多兩天、十二人的調整方案。預算重分配能否創造空間，仍有待觀察。在此感謝投入的時間與透明估價。

此致問候
Kai Okonkwo
人才發展

若優先順序改變，我們樂於再聯繫。在此祝貴單位課程持續成功，並感謝報價階段專業友善的溝通。""",
[n('Absage','婉拒'),n('Ausschlaggebend','具決定性的'),n('kollidiert','衝突'),n('Mindestteilnehmerzahl','最低人數'),n('Budgetumschichtungen','預算重分配'),n('Kalkulation','估價／核算'),n('grundsätzlich','原則上')],
[p('müssen wir … dennoch … absagen','禮貌拒絕','müssen wir dennoch absagen'),p('Ausschlaggebend sind zum einen … zum anderen …','雙因','Ausschlaggebend sind Zeit und Kosten'),p('Sollten Sie …, bitten wir um …','保留未來','Sollten Sie Kapazität haben, bitten wir …')],
['婉拒信：肯定＋具體理由＋未來開口。','避免模糊『不適合』。','德檢：兩項決定性理由？'],['郵件','職場','協商']),
(
'b2-33','notice','法律／規定','Hinweis zur Datenverarbeitung im Betrieb','企業資料處理說明',
"""Informationen zur Datenverarbeitung im Beschäftigtenverhältnis

Personenbezogene Daten der Mitarbeitenden werden ausschließlich zu Zwecken verarbeitet, die für Begründung, Durchführung und Beendigung des Arbeitsverhältnisses erforderlich sind. Dazu zählen unter anderem Kontaktdaten, Arbeitszeiten, Gehaltsabrechnungen sowie dokumentierte Qualifikationen. Eine Weitergabe an Dritte erfolgt nur, sofern eine gesetzliche Pflicht besteht, ein Auftragsverarbeitungsvertrag vorliegt oder eine ausdrückliche Einwilligung erteilt wurde.

Sie haben das Recht auf Auskunft, Berichtigung, Einschränkung der Verarbeitung und – soweit gesetzlich vorgesehen – Löschung. Widerspruch gegen nicht erforderliche Verarbeitungen können Sie formlos an die Datenschutzbeauftragte richten. Zum einen dient die Dokumentation dem Arbeitsschutz und der Entgeltabrechnung; zum anderen sollen Überwachungsgefühle vermieden werden, weshalb Zugriffe protokolliert und begrenzt sind.

Während Videoüberwachung nur in ausgewiesenen Bereichen stattfindet, bleibt die private Nutzung dienstlicher Geräte eingeschränkt erlaubt, sofern Betriebsvereinbarungen eingehalten werden. Es bleibt abzuwarten, inwiefern neue Analysewerkzeuge zusätzliche Folgeabschätzungen erfordern. Bis dahin gilt: Ohne Rechtsgrundlage keine Verarbeitung.

Kontakt: datenschutz@beispiel-firma.de | Betriebsrat: betriebsrat@beispiel-firma.de""",
"""僱傭關係中的資料處理說明

員工個人資料僅就建立、履行與結束勞動關係所必要之目的處理。包括聯絡資料、工時、薪資結算與已記錄之資格等。僅在有法律義務、有委託處理契約或經明示同意時，才提供給第三方。

您有查詢、更正、限制處理以及——在法律規定範圍內——刪除之權利。對非必要處理之異議，可以非正式方式向個資保護負責人提出。一方面文件有助勞動保護與薪資結算；另一方面為避免監控感，存取會被記錄並受限。

監視錄影僅在標示區域進行；公務設備之私人使用在遵守企業協議前提下仍有限允許。新分析工具是否需要額外影響評估，仍有待觀察。在此之前：無法律依據即不處理。

聯絡：datenschutz@beispiel-firma.de｜企業委員會：betriebsrat@beispiel-firma.de""",
[n('Personenbezogene Daten','個人資料'),n('Auftragsverarbeitungsvertrag','委託處理契約'),n('ausdrückliche Einwilligung','明示同意'),n('formlos','非正式方式'),n('Folgeabschätzungen','影響評估'),n('Rechtsgrundlage','法律依據'),n('ausgewiesenen Bereichen','標示區域')],
[p('werden ausschließlich zu Zwecken verarbeitet, die …','目的限制','werden nur zu erforderlichen Zwecken verarbeitet'),p('erfolgt nur, sofern …','條件發生','erfolgt nur, sofern Pflicht besteht'),p('Ohne … keine …','禁令套語','Ohne Rechtsgrundlage keine Verarbeitung')],
['法規公告：目的、權利、例外、聯絡。','標出被動與 Nominalstil。','德檢：私人使用設備是否完全禁止？'],['被動','法律','職場']),
(
'b2-34','notice','教育','Richtlinie für Prüfungsrücktritte','退考準則',
"""Richtlinie der Fakultät zum Rücktritt von Prüfungen

Ein Rücktritt ist bis spätestens sieben Tage vor dem Prüfungstermin ohne Angabe von Gründen schriftlich möglich. Danach ist ein Rücktritt nur bei nachgewiesenem triftigem Grund zulässig, insbesondere bei Krankheit, nachgewiesen durch ärztliches Attest, oder bei unabwendbaren familiären Ereignissen. Verspätete Einreichungen ohne Beleg führen zur Bewertung mit „nicht bestanden“, sofern keine Härtefallregelung greift.

Studierende reichen den Antrag über das Campusportal ein und fügen erforderliche Nachweise als PDF bei. Die Prüfungsausschussvorsitzende entscheidet innerhalb von zehn Werktagen. Zum einen soll Planungssicherheit für Prüfende gewahrt bleiben; zum anderen dürfen nachweisbare Notlagen nicht benachteiligen. Widerspruch gegen ablehnende Bescheide ist binnen eines Monats möglich.

Während Online-Atteste akzeptiert werden, behält sich die Fakultät stichprobenartige Nachfragen vor. Es bleibt abzuwarten, inwiefern landesweite Vorgaben die Fristen vereinheitlichen. Bis dahin gilt diese Richtlinie verbindlich für alle Bachelor- und Masterstudiengänge der Fakultät.

Fragen: pruefungsamt@uni-beispiel.de""",
"""學院退考準則

最遲於考前七日可不附理由書面退考。其後僅在可證明之正當理由下允許，尤其是疾病（須醫師證明）或不可避免之家庭事件。無證明之遲交將評為不及格，除非適用困境條款。

學生經校園入口提交申請，並以 PDF 附上必要證明。考試委員會主席於十個工作日內決定。一方面保障命題者規畫可預期；另一方面不應使可證明困境者吃虧。對駁回決定可於一個月內異議。

接受線上證明之際，學院保留抽查詢問權。全國規定能否統一期限，仍有待觀察。在此之前本準則對學院所有學士與碩士學程具約束力。

詢問：pruefungsamt@uni-beispiel.de""",
[n('triftigem Grund','正當理由'),n('ärztliches Attest','醫師證明'),n('Härtefallregelung','困境條款'),n('Planungssicherheit','規畫可預期性'),n('ablehnende Bescheide','駁回決定'),n('stichprobenartige','抽樣式的'),n('verbindlich','具約束力')],
[p('ist … nur bei … zulässig','限制允許','ist nur bei Attest zulässig'),p('führen zur Bewertung mit …, sofern …','後果條件','führen zu Nichtbestehen, sofern …'),p('behält sich … vor','保留權利','behält sich Nachfragen vor')],
['規定文：期限層級＋例外＋程序。','注意 Härtefall。','德檢：七日後還能無理由退考嗎？'],['規定','教育','程序']),
(
'b2-35','notice','環境','Mitteilung zur kommunalen Hitzehilfe','縣市熱傷害協助公告',
"""Mitteilung der Stadtverwaltung: Hitzehilfe in den Sommermonaten

Angesichts wiederkehrender Hitzewellen öffnet die Stadt vom 1. Juni bis 15. September klimatisierte Ruheräume in drei Bürgerzentren. Die Nutzung ist kostenfrei; eine Anmeldung ist nicht erforderlich. Trinkwasserstellen werden zusätzlich in Parks und an stark frequentierten Plätzen eingerichtet. Besonders angesprochen sind ältere Menschen, chronisch Kranke und Personen ohne kühle Wohnräume.

Einsatzkräfte der Feuerwehr und des Roten Kreuzes verstärken bei Warnstufe Orange die aufsuchende Hilfe in bekannten Risikohaushalten. Zum einen sollen Notfälle verhindert werden; zum anderen wird Nachbarschaftshilfe ausdrücklich ermutigt. Während Baustellen in der Innenstadt angepasste Pausenzeiten erhalten, bleibt die Verantwortung von Arbeitgeberinnen und Arbeitgebern für Outdoor-Beschäftigte unberührt.

Es wird empfohlen, körperliche Anstrengungen in die Morgen- und Abendstunden zu verlegen und Medikamente kühl zu lagern. Es bleibt abzuwarten, inwiefern mobile Kühlstellen in Außenbezirken ergänzt werden können. Aktuelle Warnungen finden Sie unter hitze.stadt-beispiel.de sowie in der städtischen App.

Notruf: 112 | Bürgertelefon: 115""",
"""市政公所公告：夏季熱傷害協助

鑑於反覆熱浪，市府於6月1日至9月15日在三處市民中心開放空調休息室。免費使用，無需預約。公園與人潮密集廣場另設飲水點。特別呼籲長者、慢性病患與住所不涼爽者。

橙色警戒時，消防與紅十字會加強對已知風險住戶的外展協助。一方面預防急症；另一方面明確鼓勵鄰居互助。市中心工地調整休息時間；戶外工作者之雇主責任不受影響。

建議將費力活動移至早晚，藥物置於陰涼處。外圍行政區能否增設移動降溫點，仍有待觀察。最新警戒見 hitze.stadt-beispiel.de 與市政 App。

急救：112｜市民電話：115""",
[n('Angesichts','鑑於'),n('klimatisierte Ruheräume','空調休息室'),n('frequentierten','人潮密集的'),n('aufsuchende Hilfe','外展／到宅協助'),n('unberührt','不受影響'),n('verlegen','改期／移至'),n('Warnstufe','警戒等級')],
[p('Angesichts … öffnet …','原因措施','Angesichts der Lage öffnet die Stadt …'),p('Es wird empfohlen, … zu …','被動建議','Es wird empfohlen, früh zu handeln'),p('bleibt … unberührt','保留不變','bleibt die Pflicht unberührt')],
['公告：對象、時間、措施、責任界線。','注意雇主責任『unberührt』。','德檢：休息室要預約嗎？'],['公告','環境','健康']),
(
'b2-36','notice','文化','Leitlinien für städtische Ausstellungen','市立展覽準則',
"""Leitlinien der städtischen Galerie für Ausstellungen und Vermittlung

Ausstellungen sollen multiperspektivisch kuratiert und barrierearm vermittelt werden. Texte in leichter Sprache sowie Audioformate sind für wechselnde Sonderausstellungen verpflichtend vorzusehen. Leihgaben erfordern schriftliche Vereinbarungen zu Versicherung, Transport und Klimabedingungen. Kritische Provenienzprüfung ist vor Erwerb und Präsentation durchzuführen; ungeklärte Herkunft ist im Raum kenntlich zu machen.

Bildungsangebote gelten als integraler Bestandteil, nicht als optionales Beiwerk. Kooperationen mit Schulen und Nachbarschaftszentren sind jährlich zu dokumentieren. Zum einen sichert dies öffentliche Legitimität; zum anderen erweitert es das Publikum über das Stammklientel hinaus. Beschwerden nimmt die Direktion entgegen, dokumentiert sie und antwortet innerhalb von vier Wochen.

Während Sponsoring transparent ausgewiesen werden muss, bleiben kuratorische Entscheidungen unabhängig. Es bleibt abzuwarten, inwiefern digitale Sammlungszugänge die physische Teilhabe ergänzen. Die Leitlinien treten zum 1. Januar in Kraft und werden nach zwei Jahren evaluiert.

Kontakt: direktion@galerie-beispiel.de""",
"""市立藝廊展覽與教育準則

展覽應多視角策展，並以便利近用方式傳達。輪替特展必須提供易讀文本與音訊格式。借展須有保險、運輸與氣候條件之書面約定。購藏與展出前須進行出處檢視；來源未明者應於展場標示。

教育活動屬整體一環，而非可有可無附屬。與學校、鄰里中心之合作須逐年記錄。一方面確保公共正當性；另一方面把觀眾擴到固定客群之外。申訴由館長受理、記錄，並於四週內回覆。

贊助必須透明標示；策展決定保持獨立。數位典藏近用能否補充實體參與，仍有待觀察。本準則自1月1日生效，兩年後評估。

聯絡：direktion@galerie-beispiel.de""",
[n('multiperspektivisch','多視角地'),n('barrierearm','低障礙'),n('Leihgaben','借展作品'),n('Provenienzprüfung','出處檢視'),n('Beiwerk','附屬物'),n('Stammklientel','固定客群'),n('kuratorische','策展的')],
[p('sollen … und … werden','雙重規範被動','sollen geprüft und dokumentiert werden'),p('gelten als …, nicht als …','定位','gelten als Kern, nicht als Beiwerk'),p('treten … in Kraft','生效','treten zum 1. Januar in Kraft')],
['文化機構治理：價值＋程序＋獨立性。','注意 Provenienz。','德檢：贊助能否影響策展？'],['文化','規定','正式']),
(
'b2-37','notice','職場','Betriebsvereinbarung Homeoffice (Auszug)','居家辦公企業協議（節錄）',
"""Betriebsvereinbarung zur mobilen Arbeit – Auszug für alle Beschäftigten

Mobile Arbeit ist nach Zustimmung der Führungskraft für geeignete Tätigkeiten möglich, sofern betriebliche Abläufe und Kundenservice gewährleistet bleiben. Grundsätzlich können bis zu zwei Tage pro Woche außerhalb der Betriebsstätte gearbeitet werden; Abweichungen bedürfen einer schriftlichen Regelung. Erreichbarkeit wird in Kernzeiten von 10 bis 15 Uhr erwartet, außerhalb gelten die allgemeinen Arbeitszeitregeln.

Arbeitsmittel stellt der Arbeitgeber bedarfsbezogen bereit. Kosten für privaten Strom und Internet werden pauschal erstattet, soweit keine abweichende Regelung besteht. Zum einen soll Flexibilität gefördert werden; zum anderen dürfen Überstunden nicht unsichtbar werden – Zeiterfassung bleibt verpflichtend. Vertrauliche Daten dürfen nur über freigegebene Systeme verarbeitet werden.

Während Präsenztermine Vorrang haben können, ist eine Diskriminierung wegen fehlender häuslicher Arbeitsplätze unzulässig. Es bleibt abzuwarten, inwiefern die Evaluation nach zwölf Monaten Anpassungen nahelegt. Fragen richtet bitte an Personal und Betriebsrat.

Gültig ab: 1. April | Version 2.1""",
"""行動辦公企業協議——全體員工節錄

適合之職務經主管同意可行動辦公，前提是營運流程與客戶服務仍獲保障。原則上每週最多兩天可在非營業場所工作；例外須書面約定。核心時段10至15點須可聯繫，其餘適用一般工時規定。

工作設備由雇主依需求提供。私人電費與網路在無其他約定時以定額補助。一方面促進彈性；另一方面加班不得隱形——工時記錄仍義務。機密資料僅能透過核准系統處理。

實體會議可優先；但不得因家中無工作空間而歧視。十二個月後評估是否顯示需調整，仍有待觀察。問題請洽人事與企業委員會。

生效：4月1日｜版本2.1""",
[n('mobile Arbeit','行動／遠距辦公'),n('bedürfen','需要'),n('Kernzeiten','核心時段'),n('pauschal erstattet','定額補助'),n('Zeiterfassung','工時記錄'),n('freigegebene Systeme','核准系統'),n('unzulässig','不被允許')],
[p('ist … möglich, sofern …','條件允許','ist möglich, sofern Service bleibt'),p('Dürfen … nur über …','限制','dürfen nur über VPN laufen'),p('ist … unzulässig','禁止','ist Diskriminierung unzulässig')],
['企業協議語氣：條件、上限、權利。','標出 Kernzeiten／Zeiterfassung。','德檢：每週遠距有上限嗎？'],['規定','職場','數位化']),
(
'b2-38','notice','消費','Widerrufsbelehrung (Musterauszug)','撤回權告知（範例節錄）',
"""Widerrufsbelehrung für Fernabsatzverträge – Musterauszug

Verbraucherinnen und Verbraucher haben das Recht, binnen vierzehn Tagen ohne Angabe von Gründen diesen Vertrag zu widerrufen. Die Widerrufsfrist beginnt mit dem Tag, an dem Sie oder ein von Ihnen benannter Dritter die Waren in Besitz genommen haben. Um Ihr Widerrufsrecht auszuüben, müssen Sie uns mittels einer eindeutigen Erklärung informieren.

Zur Fristwahrung genügt die rechtzeitige Absendung vor Fristablauf. Im Falle eines wirksamen Widerrufs erstatten wir alle Zahlungen unverzüglich, spätestens binnen vierzehn Tagen ab Zugang der Erklärung. Zum einen können wir die Rückzahlung verweigern, bis die Waren zurückerhalten wurden; zum anderen tragen Sie die unmittelbaren Kosten der Rücksendung, sofern im Angebot nichts anderes bestimmt ist.

Während Waren, die aus Hygienegründen nicht zur Rückgabe geeignet sind und deren Siegel entfernt wurde, vom Widerruf ausgeschlossen sein können, bleibt das Gewährleistungsrecht unberührt. Es bleibt abzuwarten, inwiefern gesetzliche Änderungen die Fristen anpassen. Das Muster ersetzt keine Rechtsberatung im Einzelfall.

Kontakt Widerruf: widerruf@shop-beispiel.de""",
"""遠距契約撤回權告知——範例節錄

消費者有權於十四日內不附理由撤回契約。期限自您或您指定之第三人取得商品之日起算。行使撤回權時，須以明確聲明通知我們。

為遵守期限，於屆滿前及時寄出即可。有效撤回時，我們至遲於收到聲明後十四日內退還所有款項。一方面我們可待收回商品後再退款；另一方面若要約未另定，退貨直接費用由您負擔。

基於衛生不宜退貨且封條已拆之商品可能排除撤回；瑕疵擔保權利不受影響。法律是否調整期限，仍有待觀察。本範例不取代個案法律諮詢。

撤回聯絡：widerruf@shop-beispiel.de""",
[n('Fernabsatzverträge','遠距契約'),n('widerrufen','撤回'),n('Fristwahrung','遵守期限'),n('unverzüglich','立即／不遲延'),n('Gewährleistungsrecht','瑕疵擔保權'),n('Siegel','封條'),n('unberührt','不受影響')],
[p('haben das Recht, … zu widerrufen','權利套語','haben das Recht zu widersprechen'),p('Zur Fristwahrung genügt …','期限技巧','Zur Fristwahrung genügt die Absendung'),p('bleibt … unberührt','保留其他權利','bleibt Gewährleistung unberührt')],
['消費法規：起算、行使、退款、例外。','注意十四日期限。','德檢：退貨費用誰付？'],['規定','消費','法律']),
(
'b2-39','notice','交通','Bekanntmachung Fahrplanwechsel','時刻表變更公告',
"""Bekanntmachung des Verkehrsverbunds: Fahrplanwechsel ab 10. Dezember

Zum Fahrplanwechsel werden auf mehreren Stadt- und Regionallinien Taktungen verdichtet, während einzelne Schwachlastfahrten entfallen. Die Linie R3 verkehrt werktags künftig im 15-Minuten-Takt bis 20 Uhr; nach 20 Uhr gilt ein 30-Minuten-Takt. Parallel dazu werden barrierefreie Haltestellen an drei Standorten fertiggestellt und in den Liniennetzplänen ausgewiesen.

Zum einen sollen Berufspendlerinnen zuverlässigere Anschlüsse erhalten; zum anderen reagieren wir auf Rückmeldungen aus Bürgerdialogen. Dennoch kann es in den ersten zwei Wochen zu Verspätungen kommen, weil Baustellen im Südabschnitt noch nicht abgeschlossen sind. Fahrgäste werden gebeten, digitale Abfahrtsmonitore und die Verbund-App zu nutzen.

Es bleibt abzuwarten, inwiefern Nachtverkehre an Wochenenden ausgeweitet werden können. Monatskarten behalten ihre Gültigkeit; Umstellungstarife sind nicht erforderlich. Beschwerden und Anregungen nimmt das Kundencenter entgegen.

Hotline: 0800 123 456 | App: VerbundMobil

Baustellenbedingte Abweichungen werden tagesaktuell in der App gekennzeichnet. Fahrgäste mit Mobilitätseinschränkungen finden unter barrierefrei.verbund-beispiel.de Ersatzhaltestellen und Assistenzkontakte. Wir bitten um Geduld in der Umstellungsphase und um Hinweise bei fehlenden Anschlüssen.""",
"""交通聯盟公告：12月10日起時刻表變更

時刻表變更後，多條市區與區域路線加密班距，同時取消部分離峰班次。R3線平日20點前改為15分一班；20點後為30分一班。同時三處無障礙站點完工，並標示於路線圖。

一方面讓通勤者銜接更可靠；另一方面回應公民對話回饋。但南段工地未完工，前兩週仍可能誤點。請旅客使用電子發車螢幕與聯盟 App。

週末夜间班次能否擴充，仍有待觀察。月票繼續有效；無需換票。申訴與建議由客服中心受理。

專線：0800 123 456｜App：VerbundMobil

工地造成的臨時改道將於 App 即時標示。行動不便旅客可至 barrierefrei.verbund-beispiel.de 查替代站點與協助窗口。轉換期請包涵，若缺銜接請回報。""",
[n('Fahrplanwechsel','時刻表變更'),n('Taktungen verdichtet','加密班距'),n('Schwachlastfahrten','離峰班次'),n('Anschlüsse','銜接'),n('Verspätungen','誤點'),n('Umstellungstarife','換票／改票價'),n('Nachtverkehre','夜間班次')],
[p('Zum Fahrplanwechsel werden …','生效套語','Zum Fahrplanwechsel werden Linien angepasst'),p('Während …, werden …','同時對照','Während Takte steigen, entfallen Fahrten'),p('Fahrgäste werden gebeten, …','公告請求','Fahrgäste werden gebeten, umzusteigen')],
['交通公告：變更內容＋暫時風險＋票證。','注意班距數字。','德檢：月票要重買嗎？'],['公告','交通','程序']),
(
'b2-40','notice','健康','Aushang Impfaktion Betrieb','企業疫苗活動公告',
"""Aushang: Betriebliche Impfaktion gegen Influenza

Am 8. und 9. Oktober findet in der Kantine eine freiwillige Impfaktion statt. Die Kosten übernimmt der Arbeitgeber; eine Terminbuchung über das Intranet ist erforderlich, um Wartezeiten zu begrenzen. Bitte bringen Sie den Impfausweis sowie Angaben zu bekannten Allergien mit. Personen mit akuten Infekten werden gebeten, den Termin zu verschieben.

Die Teilnahme ist freiwillig und hat keine Auswirkungen auf die dienstliche Beurteilung. Zum einen soll der Gesundheitsschutz gestärkt werden; zum anderen bleiben betriebsärztliche Sprechstunden für individuelle Beratung geöffnet. Während der Impfung gilt Maskenpflicht im Wartebereich, sofern die Gesundheitsbehörde dies empfiehlt.

Es bleibt abzuwarten, inwiefern eine zweite Aktion im Januar angeboten wird. Datenschutz: Impfstatus wird nicht an Führungskräfte übermittelt. Fragen beantwortet der Betriebsarzt unter betriebsarzt@firma-beispiel.de.

Öffnungszeiten: 9–16 Uhr | Barrierefreier Zugang über Eingang B

Schwangere und Personen mit besonderen Risiken erhalten bevorzugt frühe Termine. Eine Zweitimpfung ist im Rahmen dieser Aktion nicht vorgesehen; Beratung dazu erfolgt über den Betriebsarzt. Bitte erscheinen Sie fünf Minuten vor dem gebuchten Slot.""",
"""公告：企業流感疫苗活動

10月8、9日於餐廳舉辦自願接種。費用由雇主負擔；須經內網預約以縮短等候。請攜帶接種手冊及已知過敏資料。急性感染者請改期。

參與自願，不影響考績。一方面強化健康保護；另一方面企業醫師門診仍提供個別諮詢。等候區在衛生機關建議時須戴口罩。

一月是否二度舉辦，仍有待觀察。個資：接種狀態不轉交主管。問題洽企業醫師 betriebsarzt@firma-beispiel.de。

時間：9–16點｜無障礙入口為 B 門

孕婦與高風險者優先早時段。本次活動不含追加劑；相關諮詢由企業醫師處理。請於預約時段前五分鐘到場。""",
[n('Impfaktion','疫苗活動'),n('Impfausweis','接種手冊'),n('akuten Infekten','急性感染'),n('dienstliche Beurteilung','考績／勤務評價'),n('betriebsärztliche','企業醫師的'),n('übermittelt','轉交／傳送'),n('Barrierefreier Zugang','無障礙入口')],
[p('findet … statt','舉辦','findet in der Kantine statt'),p('hat keine Auswirkungen auf …','無影響','hat keine Auswirkungen auf die Note'),p('wird nicht an … übermittelt','資料隔離','wird nicht an Vorgesetzte übermittelt')],
['健康公告：自願、費用、個資界線。','注意不影響考績。','德檢：要預約嗎？'],['公告','健康','職場']),
(
'b2-41','notice','政治社會','Bekanntmachung Bürgerdialog','公民對話公告',
"""Bekanntmachung: Bürgerdialog zur Neugestaltung des Bahnhofsumfelds

Die Stadtverwaltung lädt am 18. Mai von 17 bis 20 Uhr zu einem öffentlichen Bürgerdialog in die Stadthalle ein. Gegenstand ist die Neugestaltung des Bahnhofsvorplatzes einschließlich Radverkehr, Barrierefreiheit und Aufenthaltsqualität. Eine Anmeldung ist nicht erforderlich; aufgrund begrenzter Plätze wird um rechtzeitiges Erscheinen gebeten. Unterlagen liegen ab sofort im Rathaus und online unter stadt-beispiel.de/bahnhof aus.

Zum einen sollen Anwohnerinnen und Pendler ihre Perspektiven einbringen; zum anderen werden Fachplanungen vorgestellt und kommentierbar gemacht. Schriftliche Stellungnahmen können bis 1. Juni eingereicht werden. Während der Veranstaltung ist Gebärdensprachdolmetschung vorgesehen; leichte Sprache wird für die Kerninhalte angeboten.

Es bleibt abzuwarten, inwiefern die Ergebnisse in den Bebauungsplanentwurf übernommen werden. Eine Zusammenfassung wird binnen drei Wochen veröffentlicht. Kritik an früheren Verfahren nehmen wir ernst und dokumentieren offene Fragen sichtbar.

Kontakt: beteiligung@stadt-beispiel.de | Tel. 0123 456-0""",
"""公告：車站周邊再造公民對話

市府邀請於5月18日17至20點至市民禮堂參加公開公民對話。主題為車站前廣場再造，含自行車交通、無障礙與停留品質。無需報名；座位有限請提早到場。資料即日起於市政廳及 stadt-beispiel.de/bahnhof 公開。

一方面讓居民與通勤者提出觀點；另一方面展示專業規畫並供評論。書面意見可至6月1日提交。活動提供手語翻譯；核心內容提供易讀版。

結果納入都市計畫草案到何程度，仍有待觀察。摘要三週內公布。我們認真看待對過往程序的批評，並公開記錄未決問題。

聯絡：beteiligung@stadt-beispiel.de｜電話 0123 456-0""",
[n('Gegenstand','主題／標的'),n('Aufenthaltsqualität','停留品質'),n('Stellungnahmen','意見書'),n('Gebärdensprachdolmetschung','手語翻譯'),n('Bebauungsplanentwurf','都市計畫草案'),n('dokumentieren','記錄'),n('Anwohnerinnen','居民（女性含括）')],
[p('lädt … zu … ein','邀請','lädt zu einem Dialog ein'),p('Gegenstand ist …','主題定位','Gegenstand ist die Umgestaltung'),p('Während … ist … vorgesehen','活動安排','Während der Sitzung ist Dolmetschung vorgesehen')],
['公民參與公告：時間、主題、管道、無障礙。','注意書面期限。','德檢：一定要報名嗎？'],['公告','參與','城市']),
(
'b2-42','notice','教育','Ausschreibung Stipendienprogramm','獎學金計畫公告',
"""Ausschreibung: Stipendienprogramm „Studium mit Verantwortung“

Die Stiftung vergibt für das kommende Studienjahr zwanzig Stipendien an Studierende, die akademische Leistung mit gesellschaftlichem Engagement verbinden. Gefördert werden Lebenshaltungskosten sowie gezielte Weiterbildungen. Bewerbungsfrist ist der 15. Februar; vollständige Unterlagen umfassen Motivationsschreiben, Leistungsübersicht, Nachweis des Engagements und zwei Referenzen.

Auswahlkriterien sind fachliche Eignung, Nachhaltigkeit des Engagements und die Plausibilität des Studienplans. Zum einen sollen Erstakademikerinnen besonders ermutigt werden; zum anderen bleibt das Verfahren diskriminierungsfrei und transparent. Interviews finden im März statt; Zu- und Absagen ergehen schriftlich.

Während Doppelförderungen grundsätzlich anzeigepflichtig sind, führt nicht jede Kombination zum Ausschluss. Es bleibt abzuwarten, inwiefern digitale Bewerbungsworkshops die Chancengleichheit erhöhen. Unvollständige Bewerbungen werden nicht nachbearbeitet.

Infoveranstaltung: 20. Januar, 18 Uhr, online | bewerbung@stiftung-beispiel.org""",
"""公告：「責任求學」獎學金計畫

基金會於下學年提供二十個名額，頒給結合學術表現與社會參與的學生。補助生活費與特定進修。截止2月15日；完整文件含動機信、成績、參與證明與兩封推薦。

遴選標準為專業適性、參與永續性與學習計畫可信度。一方面特別鼓勵家庭第一代大學生；另一方面程序保持無歧視且透明。面談於三月；錄取與婉拒皆書面通知。

重複補助原則上須申報，但並非每種組合都排除。數位申請工作坊能否提高機會平等，仍有待觀察。不完整申請不予補正。

說明會：1月20日18點線上｜bewerbung@stiftung-beispiel.org""",
[n('vergibt','頒發'),n('Lebenshaltungskosten','生活費'),n('Leistungsübersicht','成績單／表現一覽'),n('Plausibilität','可信度／合理性'),n('Erstakademikerinnen','家庭第一代大學生'),n('anzeigepflichtig','有申報義務'),n('Nachbearbeitet','事後補正')],
[p('vergibt … an …, die …','對象限定','vergibt Stipendien an Studierende, die …'),p('Auswahlkriterien sind …','標準列舉','Auswahlkriterien sind Leistung und Engagement'),p('Unvollständige … werden nicht …','嚴格程序','Unvollständige Anträge werden nicht geprüft')],
['獎助公告：條件、文件、程序語氣。','注意 Erstakademikerinnen。','德檢：申請不完整會怎樣？'],['公告','教育','程序']),
(
'b2-43','dialogue','學術','Sprechstunde zur Hausarbeit','報告面談',
"""Professorin: Ihre Fragestellung ist interessant, wirkt aber noch zu breit. Wenn Sie das gesamte Jahrzehnt abdecken, droht die Argumentation an der Oberfläche zu bleiben.
Student: Soll ich mich auf einen Zeitraum von drei Jahren beschränken?
Professorin: Ja. Außerdem fehlt bislang eine klare These, die Sie belegen oder widerlegen. Ohne These bleibt die Arbeit eine Aneinanderreihung von Befunden.
Student: Ich könnte argumentieren, dass die Maßnahme die Beteiligung erhöht hat, jedoch vor allem bei bereits engagierten Gruppen.
Professorin: Gut, das wäre bereits nuancierter. Dann brauchen Sie Vergleichsdaten und eine kritische Einordnung der Quellen. Achten Sie darauf, Gegenargumente nicht nur zu erwähnen, sondern zu gewichten.
Student: Soll ich Interviews ergänzen oder reichen die vorhandenen Statistiken?
Professorin: Quantitativ sind die Zahlen brauchbar; qualitativ fehlte bislang die Stimme der Betroffenen. Zwei bis drei Interviews würden die These stützen, sofern die Auswahl transparent begründet wird.
Student: Ich schicke Ihnen bis Freitag eine überarbeitete Gliederung und eine kurze Methodenskizze.
Professorin: Einverstanden. Und formulieren Sie die Forschungsfrage so, dass sie mit Ihren Daten tatsächlich beantwortbar ist.""",
"""教授：你的問題意識有趣，但範圍仍太廣。若涵蓋整十年，論證容易流於表面。
學生：我要限縮到三年嗎？
教授：對。而且目前缺少可證明或反駁的清楚命題。沒有命題，報告會變成發現的堆砌。
學生：我可以主張該措施提高了參與，但主要發生在本來就投入的群體。
教授：很好，這樣已較細緻。那你需要比較數據，並批判性定位來源。注意反論不要只「提到」，還要權重。
學生：要補訪談，還是現有統計就夠？
教授：量化數字可用；質化上還缺當事人聲音。兩到三則訪談能支撐命題，前提是抽樣說明透明。
學生：週五前我會寄修訂大綱與簡短方法草圖。
教授：可以。並把研究問題寫成你的資料真正回答得了的形式。""",
[n('Fragestellung','問題意識'),n('Aneinanderreihung','堆砌／並列'),n('nuancierter','更細緻'),n('Einordnung','定位'),n('gewichten','權重／衡量'),n('Methodenskizze','方法草圖'),n('beantwortbar','可回答的')],
[p('wirkt noch zu + Adj.','評價不足','wirkt noch zu vage'),p('Ich könnte argumentieren, dass …','可檢驗論點','Ich könnte argumentieren, dass …'),p('sofern die Auswahl … wird','條件','sofern die Auswahl begründet wird')],
['學術對話：範圍、命題、方法、期限。','注意『权重反論』要求。','德檢：教授對訪談的條件？'],['學術','對話','論證']),
(
'b2-44','dialogue','職場','Jahresgespräch über Entwicklung','年度發展面談',
"""Führungskraft: Lassen Sie uns zuerst bilanzieren, was im letzten Jahr gelungen ist. Die Projektübergabe an das Partnerteam lief aus meiner Sicht strukturiert.
Mitarbeiterin: Danke. Gleichzeitig hatte ich den Eindruck, dass Abstimmungsschleifen zu lange dauerten, weil Entscheidungsträger oft erst spät eingebunden wurden.
Führungskraft: Das ist ein wichtiger Punkt. Insofern sollten wir künftig Meilensteine mit klaren Eskalationspfaden versehen. Wie schätzen Sie Ihre Belastung ein?
Mitarbeiterin: Zum einen motiviert mich die inhaltliche Arbeit; zum anderen sind die Überstunden in der Schlussphase nicht nachhaltig. Ohne zusätzliche Kapazität droht Qualitätsverlust.
Führungskraft: Verstehe. Wir können eine halbe Stelle befristet aufstocken und Prioritäten schärfen. Welche Kompetenz möchten Sie als Nächstes ausbauen?
Mitarbeiterin: Moderations- und Verhandlungstechniken, idealerweise mit externer Schulung. Außerdem würde ich gerne ein kleines Budget für Fachliteratur erhalten.
Führungskraft: Beides ist vertretbar. Ich halte fest: Kapazitätsanpassung, Schulung im zweiten Quartal, Literaturpauschale. Bitte senden Sie mir bis Montag Ihre Zielskizze.
Mitarbeiterin: Mache ich. Und ich bitte darum, die Offline-Zeiten im Team verbindlicher zu kommunizieren.""",
"""主管：我們先盤點去年成果。對我而言，專案移交夥伴團隊很有結構。
員工：謝謝。同時我覺得對齊循環太長，因為決策者常很晚才被拉進來。
主管：這點很重要。因此我們往後應為里程碑設清楚升級路徑。你如何評估自己的負荷？
員工：一方面內容工作激勵我；另一方面收尾加班不可持續。沒有額外能量，品質恐下滑。
主管：理解。我們可定期約聘增加半職並釐清優先序。接下來想強化哪項能力？
員工：主持與談判技巧，最好有外部訓練。另外希望有一小筆專業書預算。
主管：兩者都說得通。我記下：能量調整、第二季訓練、圖書定額。請週一前寄目標草圖。
員工：我會。也請在團隊更有約束力地溝通離線時段。""",
[n('bilanzieren','盤點／結算'),n('Abstimmungsschleifen','對齊／協調循環'),n('Eskalationspfaden','升級路徑'),n('aufstocken','增加人力／額度'),n('vertretbar','說得通／可辯護'),n('Literaturpauschale','圖書定額'),n('verbindlicher','更有約束力地')],
[p('Lassen Sie uns zuerst …','主持開場','Lassen Sie uns zuerst Ziele klären'),p('Zum einen …; zum anderen …','雙面負荷','Zum einen motivierend; zum anderen belastend'),p('Ich halte fest: …','會議結論','Ich halte fest: Termin und Budget')],
['發展面談：成果→問題→資源→目標。','注意員工提出 Offline-Zeiten。','德檢：約定了哪些具體措施？'],['對話','職場','談判']),
(
'b2-45','dialogue','媒體','Interview zu Lokaljournalismus','地方新聞訪談',
"""Moderatorin: Sie leiten eine Lokalredaktion mit deutlich weniger Stellen als vor zehn Jahren. Wie verändert das die Berichterstattung?
Redakteur: Wir müssen stärker priorisieren. Gemeinderäte und Untersuchungsrecherchen bleiben zentral, während Veranstaltungskalender teils automatisiert werden. Dennoch verlieren wir Tiefe, wenn niemand mehr Zeit für längere Recherchen hat.
Moderatorin: Viele Menschen informieren sich über soziale Netzwerke. Sehen Sie darin Konkurrenz oder Ergänzung?
Redakteur: Beides. Reichweite entsteht dort; Glaubwürdigkeit entsteht durch Prüfung. Zum einen nutzen wir Plattformen zur Verbreitung; zum anderen erklären wir transparent, wie wir Quellen prüfen.
Moderatorin: Was erwarten Sie von der Politik?
Redakteur: Verlässliche Auskunftspflichten und Medienförderung, die Unabhängigkeit nicht untergräbt. Es bleibt abzuwarten, inwiefern neue Modelle Redaktionen in der Fläche sichern.
Moderatorin: Und an das Publikum?
Redakteur: Bereitschaft, für Qualität zu zahlen und Fehlerkorrekturen als Stärke zu lesen – nicht als Schwäche. Journalismus ist Infrastruktur, keine Selbstverständlichkeit.""",
"""主持人：您主持的地方編輯部人力比十年前少很多。這如何改變報導？
編輯：我們必須更用力排優先。市議會與調查報導仍是核心，活動行程部分自動化。但若無人再有時間做長調查，深度就會流失。
主持人：許多人靠社群獲知。您視為競爭還是補充？
編輯：兩者都是。觸及在那裡產生；可信靠查證。一方面用平台傳播；另一方面透明說明如何查核來源。
主持人：對政治有何期待？
編輯：可靠的資訊公開義務，以及不侵蝕獨立性的媒體補助。新模式能否保住地方編輯部，仍有待觀察。
主持人：對讀者呢？
編輯：願意為品質付費，並把更正當成優勢而非弱點。新聞是基礎建設，不是理所當然。""",
[n('priorisieren','排優先'),n('Untersuchungsrecherchen','調查採訪'),n('Glaubwürdigkeit','可信度'),n('Auskunftspflichten','資訊公開義務'),n('untergräbt','侵蝕'),n('Fehlerkorrekturen','錯誤更正'),n('Selbstverständlichkeit','理所當然之事')],
[p('Während …, …','對照取捨','Während A bleibt, wird B automatisiert'),p('Sehen Sie darin A oder B?','訪談選擇題','Sehen Sie darin Chance oder Risiko?'),p('Bereitschaft, … zu …','對聽眾要求','Bereitschaft, genau zu lesen')],
['訪談結構：現況→平台→政策→讀者。','注意『新聞＝基礎建設』。','德檢：編輯如何看社群平台？'],['對話','媒體','地方']),
(
'b2-46','dialogue','環境','Podium zur Verkehrswende','交通轉型座談',
"""Moderator: Willkommen zum Podium. Frau Berger, Sie vertreten den ADFC. Warum reicht technischer Fortschritt allein nicht?
Berger: Weil Verteilungsfragen ungelöst bleiben. Wer sichere Radwege erhält und wer Umwege fährt, ist politisch. Technik ohne Priorisierung reproduziert alte Muster.
Moderator: Herr Klein vom Handelsverband, Sie warnen vor Lieferengpässen.
Klein: Ja. Zum einen brauchen Geschäfte verlässliche Anlieferzeiten; zum anderen akzeptieren wir, dass Zufahrtsregeln notwendig sein können. Dennoch müssen Ausnahmen klar und unbürokratisch sein.
Berger: Einverstanden mit Klarheit. Aber „unbürokratisch“ darf nicht bedeuten, dass Klima- und Sicherheitsziele regelmäßig ausgehebelt werden.
Moderator: Wo sehen Sie kurzfristig Kompromisse?
Klein: Lieferfenster am frühen Morgen und Sammeldepot am Stadtrand.
Berger: Plus Tempo 30 und getrennte Radspuren. Es bleibt abzuwarten, inwiefern Pilotprojekte messbar Unfälle senken.
Moderator: Danke. Die Dokumentation geht online; schriftliche Nachfragen sind bis Freitag möglich.

Aus dem Publikum wird nach Kosten und Zeitplan gefragt. Klein nennt eine Evaluation nach sechs Monaten; Berger fordert unabhängige Unfall- und Luftmessungen. Der Moderator schließt mit dem Hinweis, dass politische Beschlüsse erst nach der Anhörungsfrist fallen.""",
"""主持人：歡迎座談。Berger 女士代表自行車俱樂部。為何僅有技術進步不夠？
Berger：因為分配問題未解。誰得到安全車道、誰繞路，是政治問題。沒有優先序的技術會複製舊模式。
主持人：商會的 Klein 先生警告配送瓶頸。
Klein：對。一方面店家要可靠送貨時段；另一方面我們接受進出規則可能必要。但仍須例外清楚且不官僚。
Berger：同意要清楚。但「不官僚」不該意味氣候與安全目標經常被掏空。
主持人：短期妥協在哪？
Klein：清晨配送窗與城郊集貨站。
Berger：外加速度30與分隔自行車道。試辦能否可測量降低事故，仍有待觀察。
主持人：謝謝。紀錄將上網；書面追問至週五。

現場詢問成本與時程。Klein 提出半年後評估；Berger 要求獨立的事故與空氣測量。主持人結語：政治決議須待陳述期限結束後才下。""",
[n('ADFC','德國自行車俱樂部'),n('reproduziert','複製'),n('Lieferengpässe','配送瓶頸'),n('Anlieferzeiten','送貨時段'),n('ausgehebelt','被掏空／架空'),n('Sammeldepot','集貨站'),n('Pilotprojekte','試辦專案')],
[p('Warum reicht … allein nicht?','追問不足','Warum reicht Technik allein nicht?'),p('darf nicht bedeuten, dass …','劃界','darf nicht bedeuten, dass Regeln fallen'),p('Plus …','追加要求','Plus Tempo 30 und Radspuren')],
['座談：標出雙方主張與重疊區。','注意『分配問題』。','德檢：短期妥協提了哪些？'],['對話','交通','環境']),
(
'b2-47','dialogue','健康','Gespräch in der Hausarztpraxis','家庭醫師診所對談',
"""Ärztin: Die Blutwerte zeigen erhöhte Entzündungswerte, aber noch keinen akuten Notfall. Dennoch sollten wir die Beschwerden ernst nehmen und die Ursachen eingrenzen.
Patient: Ich dachte, es sei nur Stress. Die Schmerzen kommen vor allem abends, wenn ich mich endlich hinsetze.
Ärztin: Das passt zu einer Überlastung, schließt andere Ursachen jedoch nicht aus. Zum einen empfehle ich für zwei Wochen eine belastungsärmere Routine; zum anderen brauchen wir ein EKG und gegebenenfalls eine Überweisung.
Patient: Habe ich etwas falsch gemacht?
Ärztin: Es geht nicht um Schuld. Körperliche Signale sind Informationen. Insofern wäre es kontraproduktiv, die Warnungen zu ignorieren, nur weil der Kalender voll ist.
Patient: Und Medikamente?
Ärztin: Schmerzmittel können kurzfristig helfen, ersetzen aber keine Anpassung der Belastung. Es bleibt abzuwarten, inwiefern Physiotherapie zusätzlich sinnvoll ist. Kommen Sie bitte in zehn Tagen mit den Befunden wieder.
Patient: Gut. Ich schreibe mir die Fragen vorher auf, damit ich nichts vergesse.
Ärztin: Sehr sinnvoll. Und notieren Sie, wann die Beschwerden auftreten – das erleichtert die Einordnung.""",
"""醫師：血液顯示發炎指數偏高，但尚非急性急症。我們仍應認真看待不適並縮小原因範圍。
病人：我以為只是壓力。疼痛多在晚上終於坐下時出現。
醫師：這符合過度負荷，但不排除其他原因。一方面建議兩週較低負荷作息；另一方面需要心電圖，必要時轉診。
病人：是我做錯什麼嗎？
醫師：重點不是責備。身體訊號是資訊。因此若因行程滿就忽略警示，會適得其反。
病人：那藥物呢？
醫師：止痛可短期幫忙，但不能取代調整負荷。物理治療是否額外有益，仍有待觀察。請十天後帶檢查結果再來。
病人：好。我會先寫下問題以免忘記。
醫師：很合理。並記下不適何時出現——有助定位。""",
[n('Entzündungswerte','發炎指數'),n('eingrenzen','縮小範圍'),n('belastungsärmere','較低負荷的'),n('kontraproduktiv','適得其反'),n('Befunden','檢查結果'),n('Einordnung','定位'),n('gegebenenfalls','必要時')],
[p('schließt … jedoch nicht aus','不完全排除','schließt andere Ursachen nicht aus'),p('Es geht nicht um Schuld','去責備','Es geht nicht um Schuld, sondern um …'),p('ersetzen aber keine …','有限效用','Tabletten ersetzen keine Pause')],
['醫病對話：症狀→檢查→界線（藥≠根治）。','注意『訊號＝資訊』。','德檢：十天後要帶什麼？'],['對話','健康','溝通']),
(
'b2-48','dialogue','住房','Beratung in der Mietervereinigung','租屋協會諮詢',
"""Beraterin: Lassen Sie uns die Schreiben der Hausverwaltung der Reihe nach prüfen. Zuerst die Betriebskostenabrechnung, danach die angekündigte Modernisierung.
Mieter: Die Nachzahlung wirkt hoch, und ich verstehe einzelne Posten nicht. Außerdem soll die Miete nach dem Badumbau steigen.
Beraterin: Bei Betriebskosten gilt: Nur umlagefähige Kosten dürfen berechnet werden, und die Abrechnung muss nachvollziehbar sein. Zum einen fordern wir Belegeinsicht; zum anderen prüfen wir Fristen.
Mieter: Darf ich die Modernisierung ablehnen?
Beraterin: Nicht pauschal. Duldungspflichten bestehen, dennoch müssen Ankündigung und Mieterhöhung formell korrekt sein. Unzumutbare Härte kann geltend gemacht werden, sofern Sie sie belegen.
Mieter: Und wenn die Heizung weiter ausfällt?
Beraterin: Dann dokumentieren Sie jeden Ausfall und setzen eine Frist zur Abhilfe. Mietminderung kommt infrage, sollte aber juristisch abgesichert formuliert werden.
Mieter: Ich schicke Ihnen heute Abend die Unterlagen digital.
Beraterin: Gut. Es bleibt abzuwarten, inwiefern eine einvernehmliche Lösung möglich ist; wir bereiten dennoch die nächsten Schritte vor.""",
"""顧問：我們依序檢視物業來信。先看管理費結算，再看預告的現代化工程。
房客：補繳金額偏高，有些項目看不懂。浴室整修後房租還要漲。
顧問：管理費原則：只有可分攤費用能計入，且結算須可理解。一方面我們要求閱覽憑證；另一方面檢查期限。
房客：我能拒絕現代化嗎？
顧問：不能一概拒絕。有容忍義務，但預告與漲租必須形式上正確。若可證明難以承受之困境，可主張。
房客：若暖氣繼續故障呢？
顧問：那就記錄每次故障並設改善期限。減租可能適用，但措辭最好有法律把關。
房客：今晚把文件數位寄給您。
顧問：好。能否和解仍有待觀察；我們仍會準備下一步。""",
[n('Betriebskostenabrechnung','管理費／營業費用結算'),n('umlagefähige Kosten','可分攤費用'),n('Belegeinsicht','閱覽憑證'),n('Duldungspflichten','容忍義務'),n('geltend gemacht','主張（權利）'),n('Mietminderung','減租'),n('einvernehmliche','和解的')],
[p('Lassen Sie uns … der Reihe nach …','結構化諮詢','Lassen Sie uns die Punkte der Reihe nach klären'),p('Nicht pauschal','避免一概','Nicht pauschal – es kommt darauf an'),p('kommt infrage, sollte aber …','審慎選項','kommt infrage, sollte aber geprüft werden')],
['租屋諮詢：文件→權利→程序下一步。','注意 Duldung vs. Härte。','德檢：管理費爭議先做哪兩步？'],['對話','住房','權利']),
(
'b2-49','dialogue','教育','Elternabend zur digitalen Schule','數位學校家長會',
"""Schulleiterin: Willkommen. Ziel des Abends ist es, Chancen und Risiken digitaler Tools transparent zu machen – nicht, Entscheidungen bereits als fertig zu präsentieren.
Elternteil A: Wir begrüßen Tablets, sorgen uns jedoch um Ablenkung und Datenschutz. Wer hat Zugriff auf welche Lernstände?
Schulleiterin: Zugriff ist rollenbasiert; externe Anbieter wurden vertraglich geprüft. Dennoch bleiben Fragen, die wir gemeinsam mit dem Schulträger klären.
Elternteil B: Zum anderen fehlt manchen Familien zuverlässiges WLAN. Digitalisierung darf nicht neue Ungleichheit zementieren.
Lehrkraft: Deshalb bieten wir Geräteausleihe und analoge Alternativen für ausgewählte Aufgaben. Während Übungsphasen digital laufen, bleiben Prüfungen vorerst papierbasiert.
Elternteil A: Wie werden Lehrkräfte fortgebildet?
Schulleiterin: Verpflichtende Module im ersten Halbjahr, danach kollegiale Hospitationen. Es bleibt abzuwarten, inwiefern die Evaluation im Sommer Anpassungen nahelegt.
Elternteil B: Bitte veröffentlichen Sie eine kurze Zusammenfassung der offenen Punkte.
Schulleiterin: Das machen wir binnen einer Woche auf der Schulhomepage.""",
"""校長：歡迎。今晚目標是透明說明數位工具的機會與風險——而非把決策當已完成來展示。
家長A：我們歡迎平板，但擔心分心與個資。誰能看到哪些學習狀態？
校長：存取依角色；外部供應商已契約檢視。但仍有問題須與主辦機關共同釐清。
家長B：另一方面，有些家庭缺少穩定網路。數位化不該鞏固新的不平等。
教師：因此我們提供設備出借，並對部分作業保留類比替代。練習階段可數位，考試暫仍紙本。
家長A：教師如何進修？
校長：上半年義務模組，其後同儕觀課。夏季評估是否顯示需調整，仍有待觀察。
家長B：請公布未決問題摘要。
校長：一週內放上學校網頁。""",
[n('rollenbasierter Zugriff','依角色存取'),n('Schulträger','學校主辦／主管機關'),n('zementieren','鞏固'),n('Geräteausleihe','設備出借'),n('papierbasiert','紙本的'),n('Hospitationen','觀課'),n('nahelegt','顯示／暗示')],
[p('Ziel … ist es, … – nicht …','目的澄清','Ziel ist Transparenz – nicht Druck'),p('Digitalisierung darf nicht …','規範底線','darf nicht Ungleichheit zementieren'),p('Bitte veröffentlichen Sie …','公民要求','Bitte veröffentlichen Sie das Protokoll')],
['家長會：利益相關者多方發言。','對照機會／不平等。','德檢：考試目前數位嗎？'],['對話','教育','數位化']),
(
'b2-50','dialogue','文化','Interview mit einer Kuratorin','策展人訪談',
"""Journalist: Ihre Ausstellung thematisiert Migration und Stadtgeschichte. Wie vermeiden Sie Vereinfachungen?
Kuratorin: Indem wir multiperspektivisch arbeiten und Widersprüche sichtbar lassen. Objekte erzählen selten eine einzige Wahrheit; deshalb kommentieren wir Lücken in der Überlieferung offen.
Journalist: Manche Stimmen fordern mehr Leichtigkeit, weniger Problematisierung.
Kuratorin: Leichtigkeit und Ernst schließen sich nicht aus. Zum einen brauchen wir zugängliche Vermittlung; zum anderen wäre es unverantwortlich, Konflikte wegzuretuschieren.
Journalist: Wie gehen Sie mit Sponsoren um, die inhaltlich Einfluss nehmen wollen?
Kuratorin: Sponsoring muss transparent sein, kuratorische Entscheidungen bleiben unabhängig. Sollte Druck entstehen, verzichten wir lieber auf Mittel, als Glaubwürdigkeit zu riskieren.
Journalist: Was soll das Publikum mitnehmen?
Kuratorin: Die Einsicht, dass Teilhabe an Geschichte verhandelbar ist – und dass Museen Orte der Debatte sind, nicht nur der Bewahrung. Es bleibt abzuwarten, inwiefern Schulprogramme diese Debatte in den Alltag tragen.
Journalist: Danke für das Gespräch.
Kuratorin: Gerne. Der Katalog enthält vertiefende Essays und Quellenangaben.""",
"""記者：您的展覽主題是遷移與城市史。如何避免簡化？
策展人：靠多視角工作，並讓矛盾可見。物件很少只說單一真理；因此我們公開註記史料缺口。
記者：有些聲音要求更輕鬆、少問題化。
策展人：輕鬆與嚴肅並不互斥。一方面需要好懂的傳達；另一方面把衝突修掉不負責任。
記者：若贊助想干預內容怎麼辦？
策展人：贊助必須透明，策展決定保持獨立。若出現壓力，寧可放棄經費，也不賭上可信度。
記者：希望觀眾帶走什麼？
策展人：體認歷史近用是可協商的——博物館是辯論之所，而不只是保存之所。學校方案能否把辯論帶入日常，仍有待觀察。
記者：謝謝訪談。
策展人：不客氣。圖錄有深入文章與出處。""",
[n('multiperspektivisch','多視角地'),n('Überlieferung','史料傳承'),n('wegzuretuschieren','修掉／粉飾'),n('kuratorische','策展的'),n('verhandelbar','可協商的'),n('Bewahrung','保存'),n('Quellenangaben','出處／來源註記')],
[p('Indem wir …','手段說明','Indem wir Lücken zeigen'),p('schließen sich nicht aus','並非互斥','schließen sich nicht aus'),p('verzichten wir lieber auf A, als B zu …','優先序','verzichten lieber auf Geld, als …')],
['文化訪談：方法、反論、倫理底線。','注意贊助與獨立性。','德檢：策展人如何看待『輕鬆』要求？'],['對話','文化','倫理']),

]
B2.extend(pack(t) for t in RAW)

assert len(B2) == 50, len(B2)
ids = [i["id"] for i in B2]
assert len(set(ids)) == 50, "duplicate ids"
assert ids == [f"b2-{n:02d}" for n in range(1, 51)]

lens = [len(i["text"]) for i in B2]
avg = sum(lens) / len(lens)
assert min(lens) >= 900, (min(lens), [i["id"] for i, L in zip(B2, lens) if L == min(lens)])
assert max(lens) <= 2200, max(lens)
assert avg >= 1100, avg

for it in B2:
    assert 5 <= len(it["notes"]) <= 8, (it["id"], len(it["notes"]))
    assert 3 <= len(it["patterns"]) <= 4, (it["id"], len(it["patterns"]))
    assert 2 <= len(it["tips"]) <= 3, (it["id"], len(it["tips"]))
    assert 2 <= len(it["focus"]) <= 4, (it["id"], len(it["focus"]))

data = json.loads(PATH.read_text(encoding="utf-8"))
data["items"] = [i for i in data["items"] if i.get("level") != "B2"]
data["items"].extend(B2)
data["levels"] = ["練習", "A1", "A2", "B1", "B2"]
data["note"] = (
    "對齊德檢（Goethe／ÖSD）閱讀難度：練習＝熱身短文；A1／A2／B1 循序銜接；"
    "B2＝考場長度論述／正式郵件／公告與訪談，含反論、名詞化與複合句。"
)
PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(
    f"B2={len(B2)} avg={sum(lens)//len(lens)} min={min(lens)} max={max(lens)} "
    f"total={len(data['items'])} levels={data['levels']}"
)
