#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Append 50 B1 reading items into reading.json (longer texts, richer scaffolding)."""
from __future__ import annotations

import json
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "src" / "data" / "reading.json"


def item(
    id: str,
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
        "level": "B1",
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
    d: dict = {"span": span, "zh": zh}
    if tip:
        d["tip"] = tip
    return d


def p(pattern: str, zh: str, example: str) -> dict:
    return {"pattern": pattern, "zh": zh, "example": example}


B1: list[dict] = []

B1.append(
    item(
        "b1-01",
        "story",
        "工作",
        "Mein erster Job in Deutschland",
        "我在德國的第一份工作",
        """Als ich nach Deutschland kam, suchte ich zuerst einen Nebenjob.
Nach drei Wochen habe ich in einem Café angefangen.
Am Anfang war alles neu: die Bestellungen, die Kunden und das Tempo.
Weil ich noch unsicher war, habe ich oft nachgefragt.
Meine Kolleginnen waren geduldig und haben mir viel erklärt.
Heute fühle ich mich sicherer, obwohl ich noch Fehler mache.
Der Job hilft mir nicht nur finanziell, sondern auch beim Deutschlernen.""",
        """我剛到德國時，先找打工。
三週後我在一間咖啡廳開始上班。
一開始一切都陌生：點餐、客人，還有節奏。
因為我還不確定，所以常常再確認。
同事們很有耐心，跟我解釋很多。
現在我比較有把握了，雖然還是會犯錯。
這份工作不只在經濟上幫我，也幫我學德文。""",
        [
            n("Als ich … kam", "當我……來時", "過去時間子句，動詞在句尾。"),
            n("Nebenjob", "打工／兼職"),
            n("Weil ich noch unsicher war", "因為我還不確定", "weil 子句動詞在句尾。"),
            n("obwohl ich noch Fehler mache", "雖然我還會犯錯", "obwohl＝儘管。"),
            n("nicht nur …, sondern auch …", "不僅……而且……"),
        ],
        [
            p("Als + 過去式, + 主句", "敘述過去時間點", "Als ich ankam, war ich nervös."),
            p("Weil + 子句, + 主句", "說明原因", "Weil es regnete, blieben wir zu Hause."),
            p("obwohl + 子句", "讓步", "Obwohl ich müde bin, lerne ich weiter."),
            p("nicht nur A, sondern auch B", "遞進", "Nicht nur billig, sondern auch gut."),
        ],
        [
            "B1 短文常見：Als／Weil／obwohl 串故事。",
            "先標出所有子句動詞位置，再整段朗讀。",
        ],
        ["從句", "過去敘事", "連接詞"],
    )
)

B1.append(
    item(
        "b1-02",
        "email",
        "正式郵件",
        "Bewerbung um ein Praktikum",
        "實習申請信",
        """Betreff: Bewerbung um ein Praktikum im Marketing

Sehr geehrte Frau Braun,

hiermit bewerbe ich mich um ein dreimonatiges Praktikum in Ihrer Abteilung.
Ich studiere Betriebswirtschaft und interessiere mich besonders für digitale Kampagnen.
Während meines Studiums habe ich bereits an einem Hochschulprojekt mitgearbeitet, bei dem wir Social-Media-Inhalte geplant haben.
Ich arbeite zuverlässig, lerne schnell und kann gut im Team arbeiten.
Über eine Einladung zum Gespräch würde ich mich sehr freuen.

Mit freundlichen Grüßen
Lara Hoffmann""",
        """主旨：申請行銷部門實習

敬愛的 Braun 女士：

謹此申請貴部門為期三個月的實習。
我主修企管，特別對數位活動有興趣。
在學期間我已參與過一個大學專案，我們規劃社群內容。
我做事可靠、學習快，也能良好團隊合作。
若能獲邀面談，將不勝感激。

此致問候
Lara Hoffmann""",
        [
            n("hiermit bewerbe ich mich um", "謹此申請……"),
            n("Während meines Studiums", "在學期間", "während + 第二格。"),
            n("bei dem wir … geplant haben", "在其中我們……", "關係子句。"),
            n("Über … würde ich mich freuen", "若……我會很高興", "客氣虛擬式。"),
            n("Sehr geehrte … / Mit freundlichen Grüßen", "正式書信開頭結尾"),
        ],
        [
            p("Hiermit bewerbe ich mich um + 第四格", "正式申請", "Hiermit bewerbe ich mich um die Stelle."),
            p("Während + Genitiv …", "在……期間", "Während der Woche arbeite ich."),
            p("bei dem / der / dem + 關係子句", "補充說明名詞", "das Projekt, bei dem ich half"),
            p("Über … würde ich mich freuen", "客氣期待", "Über eine Antwort würde ich mich freuen."),
        ],
        [
            "正式信：稱呼正確、動機清楚、結尾客氣。",
            "把行銷換成你的科系／部門再寫一版。",
        ],
        ["正式郵件", "關係子句", "虛擬式客氣"],
    )
)

# Bulk B1 content
MORE = [
(
"b1-03","story","居住","Nachbarn und Rücksicht","鄰居與體諒",
"""In meinem Haus wohnen Menschen aus vielen Ländern.
Meistens ist es ruhig, aber am Wochenende wird manchmal laut gefeiert.
Deshalb haben wir uns auf eine Hausregel geeinigt: nach 22 Uhr keine laute Musik.
Wer Gäste einlädt, informiert die Nachbarn vorher kurz.
Seitdem gibt es deutlich weniger Konflikte.
Ich finde das fair, weil jeder Erholung braucht.""",
"""我這棟樓住著許多不同國家的人。
大多時候很安靜，但週末有時會吵鬧慶祝。
因此我們約好一條規矩：22 點後不大聲放音樂。
誰請客，就先簡短告知鄰居。
從那以後衝突明顯變少。
我覺得公平，因為每個人都需要休息。""",
[n("sich einigen auf","就……達成共識"),n("Hausregel","大樓規定"),n("Wer …, …","誰……，就……", "無先行詞的關係句。"),n("Seitdem","從那時起"),n("deutlich weniger","明顯比較少")],
[p("sich auf etwas einigen","達成共識","Wir haben uns auf einen Termin geeinigt."),p("Wer + 動詞, + 主句","泛指『任何人』","Wer kommt, bringt Kuchen mit."),p("Seitdem + 句子","從那時起","Seitdem schlafe ich besser.")],
["B1 談社區規則：原因＋解決＋結果。"],["被動語氣入門","關係句","社會"]),
(
"b1-04","notice","行政","Anmeldung beim Bürgeramt","市民局登記公告",
"""Hinweis zur Anmeldung
Neuzugezogene müssen sich innerhalb von zwei Wochen anmelden.
Bitte bringen Sie Pass, Mietvertrag und eine Wohnungsgeberbestätigung mit.
Ohne Termin ist die Wartezeit oft länger als eine Stunde.
Termine können online gebucht werden.
Bei fehlenden Unterlagen kann der Antrag nicht bearbeitet werden.""",
"""戶籍登記提示
新遷入者須於兩週內辦理登記。
請攜帶護照、租約與房東住宿證明。
若無預約，等候常超過一小時。
可線上預約。
缺件時申請無法受理。""",
[n("Neuzugezogene","新遷入者"),n("innerhalb von zwei Wochen","兩週內"),n("Wohnungsgeberbestätigung","房東住宿證明"),n("ohne Termin","未預約"),n("kann … nicht bearbeitet werden","無法被處理", "被動。")],
[p("innerhalb von + 時間","時限內","innerhalb von drei Tagen"),p("kann … werden","可能性／被動","kann nicht geändert werden"),p("Bitte bringen Sie … mit","正式攜帶清單","Bitte Ausweis mitbringen")],
["行政公告：義務、文件、後果要抓到。"],["行政","被動","正式用語"]),
(
"b1-05","dialogue","職場","Feedback im Team","團隊回饋",
"""Chefin: Wie läuft die neue Aufgabe für dich?
Mitarbeiter: Insgesamt gut, aber die Deadline war eng.
Chefin: Was hätte dir geholfen?
Mitarbeiter: Wenn ich früher die Dateien bekommen hätte, wäre ich fertiger geworden.
Chefin: Verstehe. Ab jetzt schicken wir die Unterlagen zwei Tage früher.
Mitarbeiter: Das wäre eine große Hilfe, danke.""",
"""主管：新任務對你來說怎麼樣？
員工：整體不錯，但截止很緊。
主管：什麼會對你有幫助？
員工：如果我更早拿到檔案，就會完成得更完整。
主管：了解。從現在起我們提早兩天寄資料。
員工：那會是很大幫助，謝謝。""",
[n("Insgesamt","整體而言"),n("Deadline","截止日期"),n("Was hätte dir geholfen?","什麼本來會幫到你？", "虛擬式。"),n("Wenn ich … bekommen hätte, wäre ich …","與過去事實相反的條件"),n("Ab jetzt","從現在起")],
[p("Was hätte dir geholfen?","回饋提問","Was hättest du gebraucht?"),p("Wenn ich … hätte, wäre / hätte ich …","虛擬條件","Wenn ich Zeit hätte, käme ich."),p("Ab jetzt + 改變","宣布新規則","Ab jetzt starten wir früher.")],
["B1 職場對話會出現客氣虛擬式。","把重點放在『問題→假設→改善』。"],["虛擬式","職場","條件句"]),
(
"b1-06","story","健康","Nach dem Sportarzt","看完運動醫生之後",
"""Seit meinem Sturz beim Joggen habe ich Knieschmerzen.
Der Arzt hat gesagt, dass ich zwei Wochen pausieren soll.
Außerdem soll ich regelmäßig Dehnübungen machen.
Obwohl ich ungern auf Sport verzichte, folge ich dem Rat.
Langfristig ist das vernünftiger, als weiterzulaufen und alles zu verschlimmern.
Nächste Woche habe ich einen Kontrolltermin.""",
"""自從跑步跌倒後我膝蓋痛。
醫生說我應該休息兩週。
此外要定期做伸展。
雖然我不想放棄運動，但我聽從建議。
長期來看，這比繼續跑、把狀況弄糟更合理。
下週我有回診。""",
[n("Seit meinem Sturz","自從我跌倒後"),n("dass ich … soll","說我應該……", "dass 子句。"),n("auf etwas verzichten","放棄某事"),n("Langfristig","長期來看"),n("als weiterzulaufen","比起繼續跑", "比較＋zu 不定式。")],
[p("Der Arzt hat gesagt, dass …","轉述醫囑","Sie sagt, dass ich warten soll."),p("auf etwas verzichten","放棄","Ich verzichte auf Zucker."),p("vernünftiger, als zu + 不定式","比較合理","Besser, als nichts zu tun.")],
["健康主題常有建議與讓步。"],["dass","比較","健康"]),
(
"b1-07","email","投訴升級","Beschwerde über eine Lieferung","物流投訴信",
"""Sehr geehrte Damen und Herren,

am 3. März habe ich die Bestellung Nr. 88214 aufgegeben.
Laut Sendungsverfolgung sollte das Paket schon am Freitag ankommen.
Leider ist es bis heute nicht da, obwohl der Status „zugestellt“ zeigt.
Ich bitte Sie, den Fall zu prüfen und mir bis Ende der Woche eine Lösung anzubieten.
Andernfalls werde ich die Zahlung zurückfordern.

Mit freundlichen Grüßen
Jonas Berg""",
"""敬啟者：

我於 3 月 3 日下了訂單 88214。
依物流追蹤，包裹應於週五送達。
遺憾的是至今未到，儘管狀態顯示「已送達」。
請貴公司查核此案，並於本週末前提供解決方案。
否則我將要求退款。

此致問候
Jonas Berg""",
[n("Laut + 名詞","根據……"),n("obwohl der Status … zeigt","儘管狀態顯示……"),n("Ich bitte Sie, zu + 不定式","懇請您……"),n("Andernfalls","否則"),n("zurückfordern","要求退回")],
[p("Laut + 名詞 / Angaben","引據","Laut Wetterbericht regnet es."),p("Ich bitte Sie, … zu prüfen","正式請求","Ich bitte Sie, mir zu schreiben."),p("Andernfalls + Futur/werden","否則後果","Andernfalls werde ich stornieren.")],
["投訴信語氣堅定但保持禮貌。"],["正式郵件","讓步","請求"]),
(
"b1-08","story","學習","Prüfungsvorbereitung","考試準備",
"""In zwei Wochen schreibe ich die B1-Prüfung.
Deshalb habe ich einen Lernplan gemacht.
Morgens wiederhole ich Grammatik, nachmittags lese ich kurze Artikel.
Was mir noch schwerfällt, sind die Hörtexte mit Dialekt.
Deshalb übe ich mit Podcasts, die langsam und klar gesprochen sind.
Wenn ich den Plan einhalte, fühle ich mich am Prüfungstag sicherer.""",
"""兩週後我要考 B1。
因此我做了學習計畫。
早上複習文法，下午讀短文。
我仍覺得難的是帶口音的聽力。
所以我用說得慢又清楚的 Podcast 練習。
若我遵守計畫，考試當天會更有把握。""",
[n("schreibe … die Prüfung","參加筆試／考試", "Prüfung schreiben。"),n("Was mir noch schwerfällt","我仍覺得難的是……", "free relative。"),n("Hörtexte","聽力文本"),n("den Plan einhalten","遵守計畫")],
[p("Was mir schwerfällt, ist …","說明難點","Was mir hilft, ist Wiederholung."),p("Deshalb übe ich mit …, die …","因果＋關係子句","Ich lese Bücher, die kurz sind."),p("Wenn ich … einhalte, …","條件與規律","Wenn ich übe, werde ich besser.")],
["把你的弱項寫成『Was mir schwerfällt…』一句。"],["學習","關係句","計畫"]),
(
"b1-09","notice","租屋","Hausordnung Auszug","住戶公約摘錄",
"""Auszug aus der Hausordnung
1. Die Ruhezeiten gelten von 22 bis 6 Uhr sowie sonntags ganztägig.
2. Fahrräder gehören in den Keller, nicht in den Flur.
3. Der Hausflur muss freigehalten werden (Fluchtweg).
4. Müll ist getrennt und nur zu den Abfuhrzeiten rauszustellen.
Verstöße können zu einer Abmahnung führen.""",
"""住戶公約摘錄
1. 安靜時段為 22–6 點以及週日全天。
2. 腳踏車放地下室，不放走廊。
3. 走廊須保持暢通（逃生通道）。
4. 垃圾須分類，且僅在清運時段拿出。
違規可能導致警告。""",
[n("Ruhezeiten","安靜時段"),n("freigehalten werden","被保持暢通", "被動。"),n("Fluchtweg","逃生通道"),n("rauszustellen","拿到外面", "zu 不定式拼寫。"),n("Abmahnung","警告函")],
[p("gelten von … bis …","規定時段","Die Regel gilt für alle."),p("muss … werden","義務被動","muss getrennt werden"),p("können zu … führen","可能導致","kann zu Problemen führen")],
["公約閱讀抓：禁止、義務、後果。"],["被動","規定","住房"]),
(
"b1-10","dialogue","服務","Reklamation im Laden","店內申訴",
"""Kundin: Guten Tag, ich habe diese Jeans vor einer Woche gekauft.
Leider ist der Reißverschluss kaputt.
Verkäufer: Haben Sie den Kassenbon?
Kundin: Ja, hier. Könnte ich umtauschen oder das Geld zurückbekommen?
Verkäufer: Umtausch ist möglich. Möchten Sie eine andere Größe?
Kundin: Ja, bitte eine Nummer größer.""",
"""顧客：您好，我一週前買了這條牛仔褲。
遺憾拉鍊壞了。
店員：您有收據嗎？
顧客：有，在這。我可以換貨或退款嗎？
店員：可以換貨。要換別的尺寸嗎？
顧客：好，請大一號。""",
[n("Reißverschluss","拉鍊"),n("Kassenbon","收據"),n("umtauschen","換貨"),n("zurückbekommen","拿回（錢）"),n("eine Nummer größer","大一號")],
[p("Könnte ich …?","客氣請求許可","Könnte ich umtauschen?"),p("Umtausch ist möglich","說明政策","Rückgabe ist möglich innerhalb 14 Tagen."),p("eine Nummer größer / kleiner","尺寸調整","Bitte eine Nummer kleiner.")],
["消費維權對話：問題＋證明＋請求選項。"],["購物","客氣虛擬式"]),
]

for t in MORE:
    B1.append(item(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9], t[10]))

BATCH2 = [
(
"b1-11","story","交通","Ohne Auto in der Stadt","在城市不開車",
"""Seit ich in die Stadt gezogen bin, nutze ich selten das Auto.
Meistens fahre ich mit dem Rad oder der Straßenbahn.
Das spart Geld und ist oft schneller in der Rushhour.
Allerdings wird es problematisch, wenn ich schwere Einkäufe habe.
Dann leihe ich mir ein Lastenrad oder bestelle online.
Insgesamt bin ich mit dieser Lösung zufrieden, weil sie flexibel ist.""",
"""自從搬到城市後，我很少開車。
多半騎車或搭路面電車。
這樣省錢，尖峰時段也常比較快。
不過買重東西時就麻煩了。
那時我會借貨運自行車或改網購。
整體我滿意這做法，因為彈性高。""",
[n("Seit ich … gezogen bin","自從我搬家後"),n("Rushhour","尖峰時刻"),n("Allerdings","不過"),n("Lastenrad","貨運自行車"),n("Insgesamt","整體而言")],
[p("Seit ich …, …","自從……之後","Seit ich hier wohne, lerne ich Deutsch."),p("Allerdings + 對比","轉折","Allerdings ist es teurer."),p("Insgesamt + 評價","總結","Insgesamt war es gut.")],
["論點短文：優點→限制→折衷→總結。"],["論述","交通","連接詞"]),
(
"b1-12","email","大學","Verlängerung der Abgabefrist","延期繳交申請",
"""Sehr geehrter Herr Prof. Keller,

leider kann ich die Hausarbeit nicht bis Freitag abgeben.
Aufgrund einer Erkrankung in der Familie brauche ich mehr Zeit.
Könnten Sie die Frist bitte bis zum 20. des Monats verlängern?
Ich habe bereits einen großen Teil fertig und würde die Arbeit dann vollständig einreichen.

Mit freundlichen Grüßen
Mira Soltani""",
"""敬愛的 Keller 教授：

遺憾我無法在週五前繳交報告。
因家中有人生病，我需要更多時間。
可否請您將期限延至本月 20 日？
我已完成大部分，屆時會完整繳交。

此致問候
Mira Soltani""",
[n("Aufgrund + Genitiv","由於……"),n("Frist verlängern","延長期限"),n("einen großen Teil","一大部分"),n("einreichen","繳交／提交")],
[p("Aufgrund + Genitiv / von …","原因","Aufgrund des Wetters …"),p("Könnten Sie … verlängern?","請求延期","Könnten Sie den Termin verschieben?"),p("Ich würde … einreichen","客氣未來計畫","Ich würde dann kommen.")],
["學術郵件：原因具體、提出新日期、說明進度。"],["正式郵件","大學","Genitiv"]),
(
"b1-13","story","數位","Digitale Pause","數位休息",
"""Früher habe ich abends stundenlang Serien geschaut.
Danach konnte ich schlecht einschlafen.
Deshalb habe ich mir eine digitale Pause von 21 Uhr an vorgenommen.
Stattdessen lese ich oder gehe kurz spazieren.
Am Anfang war das ungewohnt, aber nach zwei Wochen fühlte ich mich erholter.
Manchmal breche ich die Regel, doch ich starte am nächsten Tag neu.""",
"""以前我晚上會長時間追劇。
之後很難入睡。
因此我決定從 21 點起數位休息。
改為閱讀或短暫散步。
一開始不習慣，但兩週後覺得更有恢復感。
有時會破功，但我隔天重新開始。""",
[n("stundenlang","連續數小時"),n("einschlafen","入睡"),n("sich etwas vornehmen","下決心做某事"),n("von 21 Uhr an","從 21 點起"),n("ungewohnt","不習慣的")],
[p("sich vornehmen, zu + 不定式／名詞","立志","Ich nehme mir vor, früher zu schlafen."),p("Am Anfang …, aber nach …","過程變化","Am Anfang schwer, aber dann leichter."),p("doch + 轉折","口語轉折","Ich will, doch ich kann nicht.")],
["習慣改變敘事很適合 B1。"],["生活","連接詞"]),
(
"b1-14","notice","工作","Homeoffice-Regelung","在家上班規定",
"""Interne Regelung: Homeoffice
Mitarbeitende dürfen bis zu zwei Tage pro Woche von zu Hause arbeiten.
Voraussetzung ist, dass die Aufgaben das zulassen und die Erreichbarkeit gesichert ist.
Termine mit Kundinnen und Kunden finden weiter vor Ort statt, sofern nichts anderes vereinbart wurde.
Technikprobleme sind umgehend der IT zu melden.""",
"""內部規定：在家上班
員工每週最多可在家兩天。
前提是任務允許，且可保持聯繫。
與客戶的會面原則上仍在現場，除非另有約定。
技術問題須立即向 IT 回報。""",
[n("dürfen bis zu …","最多可……"),n("Voraussetzung ist, dass …","前提是……"),n("Erreichbarkeit","可聯繫性"),n("sofern","只要／除非另有……", "偏正式。"),n("umgehend","立即")],
[p("Voraussetzung ist, dass …","訂定前提","Bedingung ist, dass …"),p("sofern nichts anderes …","除外條件","sofern nicht anders vereinbart"),p("ist … zu melden","必須回報（正式）","ist zu beachten")],
["職場公告語氣客觀、條件清楚。"],["職場","dass","正式"]),
(
"b1-15","dialogue","旅行投訴","Verspäteter Flug","班機延誤",
"""Passagier: Entschuldigung, mein Flug hat drei Stunden Verspätung.
Gibt es Verpflegung oder eine Entschädigung?
Mitarbeiterin: Bei dieser Verspätung haben Sie Anspruch auf Snacks und Getränke.
Passagier: Und wenn ich den Anschlussflug verpasse?
Mitarbeiterin: Dann buchen wir Sie auf die nächste Verbindung um.
Passagier: Alles klar, danke für die Information.""",
"""乘客：不好意思，我的班機延誤三小時。
有餐食或補償嗎？
職員：依此延誤，您有權獲得點心與飲料。
乘客：若我錯過轉機呢？
職員：那我們會幫您改訂下一班。
乘客：好的，謝謝說明。""",
[n("Anspruch auf","有權獲得……"),n("Verpflegung","餐食供應"),n("Entschädigung","補償"),n("Anschlussflug","轉機航班"),n("umbuchen auf","改訂到……")],
[p("Anspruch auf + 第四格 haben","主張權利","Ich habe Anspruch auf Hilfe."),p("Wenn ich … verpasse, dann …","假設後果","Wenn ich den Bus verpasse, nehme ich ein Taxi."),p("umbuchen auf + 第四格","改訂","auf einen späteren Zug umbuchen")],
["旅行突發：問權利＋問備案。"],["旅行","條件","權利用語"]),
(
"b1-16","story","社會","Ehrenamt im Tierheim","動物收容所志工",
"""Einmal wöchentlich helfe ich in einem Tierheim.
Dort gehe ich mit den Hunden spazieren und reinige Gehege.
Manche Tiere sind schüchtern, weil sie schlechte Erfahrungen gemacht haben.
Man muss geduldig sein und klare Routinen einhalten.
Was mich motiviert, ist das Gefühl, etwas Nützliches beizutragen.
Außerdem verbessere ich mein Deutsch im Gespräch mit den anderen Helfenden.""",
"""我每週一次在動物收容所幫忙。
在那裡帶狗散步、清理圍欄。
有些動物很怕生，因為有過不好經驗。
必須有耐心並遵守清楚作息。
激勵我的是感到自己有貢獻。
此外跟其他志工交談也讓我德文進步。""",
[n("Gehege","圍欄／獸欄"),n("schüchtern","怕生／害羞"),n("Routinen einhalten","遵守例行"),n("etwas Nützliches beitragen","做出有用貢獻"),n("Helfenden","協助者們", "分詞當名詞。")],
[p("Was mich motiviert, ist …","說明動機","Was mich stört, ist der Lärm."),p("Man muss … und …","一般義務","Man muss warten und zuhören."),p("weil sie … gemacht haben","完成式原因","weil er gelernt hat")],
["志工主題可練習『動機＋規則＋收穫』。"],["社會","關係句","完成式"]),
(
"b1-17","email","房東","Feuchtigkeit in der Wohnung","公寓潮濕問題",
"""Sehr geehrte Frau Lorenz,

seit zwei Wochen bemerke ich Feuchtigkeit an der Schlafzimmerwand.
Es riecht muffig und die Farbe blättert ab.
Ich habe bereits gelüftet und die Heizung angepasst, aber das Problem bleibt.
Könnten Sie bitte eine Fachfirma schicken oder einen Termin zur Besichtigung vorschlagen?
Fotos habe ich angehängt.

Mit freundlichen Grüßen
Keno Ali""",
"""敬愛的 Lorenz 女士：

兩週來我發現臥室牆面潮濕。
有霉味，油漆也在剝落。
我已通風並調整暖氣，但問題仍在。
可否請您派專業廠商，或提出看屋時間？
照片已附上。

此致問候
Keno Ali""",
[n("bemerke","察覺"),n("muffig","霉味的"),n("blättert ab","剝落", "abblättern。"),n("Fachfirma","專業公司"),n("angehängt","已附件")],
[p("seit + 時間 + Präsens","持續到現在","Seit einer Woche habe ich Husten."),p("Ich habe bereits …, aber …","已嘗試卻無效","Ich habe angerufen, aber niemand ging ran."),p("Fotos habe ich angehängt","附件說明","Die Datei habe ich angehängt.")],
["問題描述要具體：時間、現象、已做措施、請求。"],["住房","正式郵件"]),
(
"b1-18","story","媒體","Falschnachrichten erkennen","辨識假訊息",
"""Im Internet verbreiten sich Nachrichten sehr schnell.
Nicht jede Meldung ist überprüft.
Bevor ich etwas teile, schaue ich, wer die Quelle ist und ob andere Medien dasselbe berichten.
Wenn Behauptungen extrem klingen, werde ich besonders vorsichtig.
Es kostet ein paar Minuten, spart aber Peinlichkeit.
Kritisches Lesen gehört heute zur Alltagsfähigkeit.""",
"""網路上消息傳得很快。
不是每則都經過查證。
分享前我會看來源是誰、其他媒體是否也這樣報導。
若說法很極端，我會特別小心。
只花幾分鐘，卻能少出糗。
批判性閱讀已是日常能力。""",
[n("verbreiten sich","傳播"),n("überprüft","查證過的"),n("Quelle","來源"),n("Behauptungen","說法／主張"),n("Peinlichkeit","尷尬")],
[p("Bevor ich …, …","在……之前","Bevor ich antworte, denke ich nach."),p("Wenn … extrem klingen, …","條件警戒","Wenn es unrealistisch klingt, prüfe ich."),p("Es kostet …, spart aber …","代價與好處","Es kostet Zeit, spart aber Geld.")],
["議論文短版：現象→方法→結論。"],["媒體","論述"]),
(
"b1-19","dialogue","銀行進階","Dispokredit","透支額度",
"""Berater: Möchten Sie einen Dispokredit einrichten?
Kundin: Was genau bedeutet das?
Berater: Damit können Sie Ihr Konto kurzzeitig überziehen, gegen Zinsen.
Kundin: Und wenn ich das nicht brauche?
Berater: Dann bleibt er ungenutzt. Sie können ihn auch wieder abschalten.
Kundin: Gut, dann richte ich ihn mit einem niedrigen Limit ein.""",
"""行員：您要設定透支額度嗎？
顧客：那到底是什麼意思？
行員：您可短暫讓帳戶透支，但需付利息。
顧客：若我不需要呢？
行員：那就不會動用。也可以再關閉。
顧客：好，那我設一個較低上限。""",
[n("Dispokredit","透支信用"),n("überziehen","透支"),n("gegen Zinsen","需付利息"),n("ungenutzt","未使用的"),n("Limit","上限")],
[p("Was genau bedeutet das?","要求清楚解釋","Was heißt das genau?"),p("Dann bleibt …","說明後果／狀態","Dann bleibt alles wie bisher."),p("mit einem niedrigen Limit","附加條件","mit kurzer Laufzeit")],
["金融對話：先問定義再決定。"],["行政","金融"]),
(
"b1-20","notice","活動","Nachbarschaftsfest","鄰里節",
"""Nachbarschaftsfest am 12. Juni, 15–20 Uhr, Innenhof
Bring mit: Salat, Kuchen oder Getränke (nach Möglichkeit).
Für Kinder gibt es Spiele; bitte Aufsichtspersonen mitbringen.
Musik bis 19 Uhr, danach Gespräche in Zimmerlautstärke.
Bei starkem Regen treffen wir uns im Gemeinschaftsraum.
Anmeldung bis 5. Juni per Aushang oder E-Mail.""",
"""鄰里節：6 月 12 日 15–20 點，內院
請盡量帶沙拉、蛋糕或飲料。
兒童有遊戲；請家長陪同。
音樂至 19 點，之後請保持室內音量交談。
若下大雨改至交誼廳。
請於 6 月 5 日前以公告欄或郵件報名。""",
[n("nach Möglichkeit","盡可能"),n("Aufsichtspersonen","監護／陪同成人"),n("Zimmerlautstärke","室內音量"),n("Gemeinschaftsraum","交誼廳"),n("Aushang","公告欄")],
[p("Bring mit: + 清單","自備物","Bring mit: Teller und Becher."),p("Bei starkem Regen …","天氣備案","Bei Hitze gibt es Schattenplätze."),p("Anmeldung bis + 日期","報名截止","Anmeldung bis Montag")],
["活動公告包含備案與截止日。"],["社區","公告"]),
]
for t in BATCH2:
    B1.append(item(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9], t[10]))

BATCH3 = [
(
"b1-21","story","環境","Weniger Plastik","減少塑膠",
"""Ich versuche, weniger Plastik zu benutzen.
Deshalb kaufe ich öfter unverpacktes Obst und nehme Stoffbeutel mit.
Unterwegs habe ich eine Flasche dabei, die ich wiederauffülle.
Natürlich ist das nicht immer möglich, besonders unter Zeitdruck.
Trotzdem merke ich, dass mein Müll sichtbar weniger wird.
Kleine Schritte sind besser als gar keine.""",
"""我試著少用塑膠。
所以更常買散裝水果並帶布袋。
出門會帶可回充水瓶。
當然不是每次都行，尤其趕時間時。
儘管如此我發現垃圾明顯變少。
小步驟勝過完全不做。""",
[n("unverpackt","未包裝的"),n("Stoffbeutel","布袋"),n("wiederauffülle","回充"),n("unter Zeitdruck","在時間壓力下"),n("sichtbar weniger","明顯變少")],
[p("Ich versuche, zu + 不定式","嘗試","Ich versuche, früher zu kommen."),p("besonders unter …","尤其在……情況下","besonders unter Stress"),p("besser als gar keine","比較級論點","Besser spät als nie.")],
["環保主題常用『嘗試→例外→仍有效果』。"],["環境","不定式"]),
(
"b1-22","email","客服跟催","Zweite Nachfrage","二次催問",
"""Guten Tag,

am 10. April habe ich bereits wegen meiner Bestellung geschrieben.
Leider habe ich noch keine Antwort erhalten.
Könnten Sie mir bitte den aktuellen Status mitteilen?
Falls das Paket verloren gegangen ist, möchte ich eine Neulieferung oder Erstattung.

Freundliche Grüße
Svenja Orth""",
"""您好，

我已於 4 月 10 日就訂單寫過信。
遺憾尚未收到回覆。
可否請告知目前狀態？
若包裹遺失，我希望補寄或退款。

問候
Svenja Orth""",
[n("bereits","已經"),n("noch keine Antwort erhalten","尚未收到回覆"),n("Falls … verloren gegangen ist","若……遺失了"),n("Neulieferung","重新配達"),n("Erstattung","退款")],
[p("Leider habe ich noch keine … erhalten","二次催問","Leider habe ich noch keine Rückmeldung erhalten."),p("Falls …, möchte ich …","條件請求","Falls es nicht geht, möchte ich stornieren."),p("Status mitteilen","請告知狀態","Bitte teilen Sie mir den Termin mit.")],
["催問信引用前次日期，語氣仍專業。"],["郵件","客服"]),
(
"b1-23","dialogue","醫療進階","Überweisung","轉診",
"""Ärztin: Die Entzündung geht zurück, aber wir brauchen ein Bild vom Gelenk.
Patient: Bedeutet das eine Überweisung?
Ärztin: Ja, zum Radiologen. Ich schreibe sie Ihnen gleich.
Patient: Wie schnell sollte ich den Termin machen?
Ärztin: Innerhalb von zwei Wochen wäre ideal.
Patient: In Ordnung, ich kümmere mich darum.""",
"""醫生：發炎在消退，但我們需要關節影像。
病人：意思是要轉診嗎？
醫生：對，轉放射科。我現在就開給您。
病人：我該多快約診？
醫生：兩週內最理想。
病人：好，我會去處理。""",
[n("geht zurück","消退"),n("Überweisung","轉診單"),n("Radiologen","放射科醫師"),n("wäre ideal","會是理想的", "虛擬式建議。"),n("kümmere mich darum","我來處理這事")],
[p("Bedeutet das …?","確認理解","Bedeutet das, dass ich warten muss?"),p("Innerhalb von … wäre ideal","建議時限","Morgen wäre ideal."),p("sich um etwas kümmern","負責處理","Ich kümmere mich um die Tickets.")],
["醫病溝通：解釋→確認→行動。"],["健康","虛擬式"]),
(
"b1-24","story","文化衝擊","Andere Pünktlichkeit","不同的準時觀",
"""In meinem Heimatland sind Treffen oft flexibler.
Hier erwarten viele Leute, dass man pünktlich ist.
Am Anfang kam ich öfter fünf Minuten zu spät und fühlte mich schlecht.
Jetzt plane ich Absichtlich Pufferzeit ein.
Das reduziert Stress und wirkt respektvoller.
Kulturelle Unterschiede merkt man besonders im Alltag.""",
"""在我的家鄉，約見常較彈性。
這裡很多人期待你準時。
一開始我常晚五分鐘，感覺很糟。
現在我會故意排緩衝時間。
這樣減少壓力，也顯得更尊重。
文化差異在日常生活裡特別明顯。""",
[n("erwarten, dass","期待……"),n("Absichtlich","故意地"),n("Pufferzeit einplanen","安排緩衝時間"),n("wirkt respektvoller","顯得更尊重"),n("besonders im Alltag","尤其在日常")],
[p("erwarten, dass …","期待從句","Ich erwarte, dass du schreibst."),p("Absichtlich + 動詞","刻意行為","Ich komme absichtlich früher."),p("wirkt + 比較級形容詞","給人印象","Das wirkt professioneller.")],
["文化比較短文：觀察→問題→調整。"],["文化","dass"]),
(
"b1-25","notice","資安","Passwort-Regeln","密碼規則",
"""IT-Hinweis: Passwörter
Verwenden Sie mindestens 12 Zeichen mit Zahlen und Sonderzeichen.
Nutzen Sie für dienstliche Konten keine privaten Passwörter erneut.
Bei Verdacht auf Phishing melden Sie die Mail sofort.
Das Zurücksetzen ist über das Portal möglich; die IT gibt keine Passwörter telefonisch durch.""",
"""IT 提示：密碼
請使用至少 12 碼並含數字與特殊符號。
公務帳號勿重複使用私人密碼。
懷疑釣魚郵件請立即回報。
可經入口網站重設；IT 不會電話告知密碼。""",
[n("mindestens","至少"),n("Sonderzeichen","特殊符號"),n("erneut nutzen","再次使用"),n("Bei Verdacht auf","若懷疑……"),n("gibt … durch","告知／通報")],
[p("Verwenden Sie …","正式指令","Verwenden Sie den Nebeneingang."),p("Bei Verdacht auf + 名詞","警戒情境","Bei Verdacht auf Betrug anrufen."),p("ist über … möglich","可透過……完成","ist online möglich")],
["資安公告：規則＋禁止＋通報方式。"],["數位","規定"]),
(
"b1-26","story","財務","Monatliches Budget","每月預算",
"""Seit ich ein Budget führe, weiß ich besser, wohin mein Geld geht.
Ich teile die Ausgaben in Miete, Essen, Transport und Freizeit.
Was übrig bleibt, spare ich oder nutze ich für unerwartete Kosten.
Am schwierigsten ist die Kategorie „Kleinigkeiten“, weil sie sich summieren.
Deshalb notiere ich auch kleine Beträge.
Nach drei Monaten habe ich weniger Schulden und mehr Überblick.""",
"""自從做預算後，我更清楚錢花去哪。
我把支出分成房租、飲食、交通與休閒。
剩下的就存起來或留作突發費用。
最難的是「零碎開銷」類，因為會累加。
所以連小金額我也記。
三個月後我負債更少、也更有全貌。""",
[n("ein Budget führen","做預算"),n("wohin … geht","錢流向何處"),n("was übrig bleibt","剩下的"),n("sich summieren","累加"),n("Überblick","總覽／掌握")],
[p("Seit ich …, weiß ich …","習慣帶來認知","Seit ich laufe, schlafe ich besser."),p("Was übrig bleibt, …","剩餘處理","Was übrig ist, spende ich."),p("sich summieren","逐漸累積","Kleine Fehler summieren sich.")],
["財務主題訓練抽象名詞與總結。"],["生活","論述"]),
(
"b1-27","email","推薦信請求","Bitte um Referenz","請求推薦",
"""Sehr geehrte Frau Dr. Hartmann,

in den letzten zwei Jahren habe ich in Ihrem Team als Werkstudentin gearbeitet.
Nun bewerbe ich mich um eine Vollzeitstelle und benötige eine kurze Referenz.
Könnten Sie mir bitte bis Ende des Monats eine Einschätzung zu meiner Arbeit schreiben?
Gerne sende ich Ihnen meine Unterlagen und den Stellenlink.

Herzlichen Dank im Voraus
Yasmin Korkmaz""",
"""敬愛的 Hartmann 博士：

過去兩年我在您的團隊擔任工讀生。
現在我申請全職，需要一封簡短推薦。
可否請您在月底前就我的工作表現寫一段評估？
我很樂意寄上資料與職缺連結。

先行致謝
Yasmin Korkmaz""",
[n("Werkstudentin","工讀生（女性）"),n("Referenz","推薦／參考查證"),n("Einschätzung","評估"),n("im Voraus","事先／先行"),n("Stellenlink","職缺連結")],
[p("Nun bewerbe ich mich um …","說明當前目標","Nun suche ich eine neue Aufgabe."),p("Könnten Sie mir bitte bis …?","含期限的請求","Könnten Sie bis Freitag antworten?"),p("Dank im Voraus","先行感謝","Vielen Dank im Voraus.")],
["請求推薦要給期限與你能提供的材料。"],["職場","正式郵件"]),
(
"b1-28","dialogue","租車","Schaden am Mietwagen","租車損傷",
"""Mitarbeiter: Bitte prüfen Sie das Auto vor der Abfahrt.
Kundin: Hier vorne rechts sehe ich einen Kratzer. Ist der schon dokumentiert?
Mitarbeiter: Ja, der steht im Übergabeprotokoll.
Kundin: Gut. Was passiert, wenn unterwegs etwas passiert?
Mitarbeiter: Melden Sie den Schaden sofort der Hotline und machen Sie Fotos.
Kundin: Verstanden, danke.""",
"""職員：出發前請檢查車輛。
顧客：右前方有刮痕。有記錄嗎？
職員：有，交接單上有。
顧客：好。若路上出狀況怎麼辦？
職員：立刻打熱線通報並拍照。
顧客：了解，謝謝。""",
[n("vor der Abfahrt","出發前"),n("Kratzer","刮痕"),n("dokumentiert","已記錄"),n("Übergabeprotokoll","交接紀錄"),n("Hotline","服務專線")],
[p("Ist … schon dokumentiert?","確認是否記錄","Ist der Mangel notiert?"),p("Was passiert, wenn …?","問突發流程","Was passiert, wenn ich zu spät komme?"),p("Melden Sie … sofort","緊急指示","Melden Sie sich sofort.")],
["服務流程對話：檢查→確認→緊急步驟。"],["旅行","服務"]),
(
"b1-29","story","人際","Missverständnis klären","澄清誤會",
"""Gestern war mein Freund kurz angebunden und ich dachte, er sei sauer auf mich.
Später hat er erklärt, dass er nur unter Termindruck stand.
Ich war erleichtert, aber auch ein bisschen peinlich berührt.
Deshalb haben wir vereinbart, in solchen Momenten klarer zu schreiben.
Zum Beispiel: „Ich habe Stress, später mehr.“
Kleine Sätze verhindern große Missverständnisse.""",
"""昨天朋友回覆很簡短，我以為他在生我氣。
後來他解釋只是行程壓力大。
我鬆了一口氣，但也有點不好意思。
因此我們約定這種時候要把話說清楚。
例如：「我很忙，稍後再談。」
小句子能避免大誤會。""",
[n("kurz angebunden","愛理不理／回得很短"),n("sauer auf mich","在生我的氣"),n("unter Termindruck","處於時間壓力"),n("peinlich berührt","感到尷尬"),n("vereinbart","約定")],
[p("ich dachte, er sei …","過去以為（虛擬）","Ich dachte, sie wäre krank."),p("erklärt, dass …","解釋原因","Er sagt, dass er keine Zeit hat."),p("Deshalb haben wir vereinbart, zu …","約定改善","Wir haben vereinbart, früher zu kommen.")],
["人際文：誤會→澄清→約定。"],["社交","虛擬式","dass"]),
(
"b1-30","notice","校園","Bibliotheksregeln erweitert","圖書館規則（進階）",
"""Ergänzung der Bibliotheksordnung
Gruppenarbeit ist nur in den gekennzeichneten Räumen erlaubt.
Getränke mit Deckel sind gestattet; offene Speisen nicht.
Wer Bücher beschädigt, muss Ersatz leisten oder die Reparaturkosten tragen.
Ausleihen können online verlängert werden, sofern keine Vormerkung vorliegt.
Bei wiederholten Verstößen kann das Nutzerkonto gesperrt werden.""",
"""圖書館規則補充
團體討論僅限標示空間。
有蓋飲料可；開放食物不行。
損壞書籍須賠償或負擔修理費。
可線上續借，前提是無人預約。
重複違規可能停權。""",
[n("gekennzeichnet","有標示的"),n("gestaltet? gestattet","被允許"),n("Ersatz leisten","賠償"),n("Vormerkung","預約／保留"),n("Nutzerkonto","使用者帳號")],
[p("ist nur … erlaubt","僅允許","ist nur mit Ausweis erlaubt"),p("sofern keine … vorliegt","前提不存在某狀況","sofern kein Fehler vorliegt"),p("kann … gesperrt werden","可能被停用","kann gelöscht werden")],
["長公告要會抓『允許／禁止／後果』。"],["規定","被動","校園"]),
]
for t in BATCH3:
    B1.append(item(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9], t[10]))

BATCH4 = [
(
"b1-31","story","職業規劃","Zwischen Abschluss und Job","畢業與工作之間",
"""Bald bin ich mit dem Studium fertig und unsicher, wie es weitergeht.
Einerseits möchte ich Berufserfahrung sammeln, andererseits noch einen Kurs machen.
Deshalb habe ich Gespräche mit der Studienberatung geführt.
Dort wurde mir empfohlen, zuerst ein Praktikum zu suchen.
So kann ich testen, welches Feld zu mir passt.
Unsicherheit gehört dazu, aber ein Plan macht sie kleiner.""",
"""我快畢業了，不確定接下來怎麼辦。
一方面想累積工作經驗，另一方面想再修一門課。
因此我找了學習諮詢談過。
他們建議我先找實習。
這樣能測試哪個領域適合我。
不確定感是正常的，但有計畫會讓它變小。""",
[n("mit … fertig","完成……"),n("Einerseits … andererseits …","一方面……另一方面……"),n("Studienberatung","學習諮詢"),n("wurde mir empfohlen","我被建議", "被動。"),n("Unsicherheit gehört dazu","不確定是過程的一部分")],
[p("Einerseits …, andererseits …","兩難","Einerseits günstig, andererseits weit."),p("wurde mir empfohlen, zu …","被建議去做","Es wurde empfohlen, früher zu starten."),p("So kann ich …","因此能夠","So kann ich vergleichen.")],
["生涯短文常用雙方面與被動建議。"],["職涯","被動","連接詞"]),
(
"b1-32","email","保險理賠","Schadensmeldung","損害通報",
"""Sehr geehrte Damen und Herren,

hiermit melde ich einen Wasserschaden in meiner Küche vom 2. Mai.
Durch ein undichtes Rohr ist der Boden beschädigt worden.
Ich habe Fotos und die Rechnung des Notdienstes beigefügt.
Bitte teilen Sie mir mit, welche nächsten Schritte nötig sind und ob ein Gutachter kommt.

Mit freundlichen Grüßen
Ralf Neumann
Polizzennummer: H-22981""",
"""敬啟者：

謹通報 5 月 2 日廚房水損。
因水管滲漏，地板受損。
已附上照片與緊急維修收據。
請告知後續步驟，以及是否會派鑑定人。

此致問候
Ralf Neumann
保單號碼：H-22981""",
[n("hiermit melde ich","謹此通報"),n("undicht","滲漏的"),n("beschädigt worden","被損壞", "狀態被動／過程。"),n("beigefügt","已附上"),n("Gutachter","鑑定人")],
[p("hiermit melde ich …","正式通報","Hiermit melde ich den Verlust."),p("ist … worden","被動完成","ist geliefert worden"),p("Bitte teilen Sie mir mit, ob …","請告知是否","teilen Sie mir mit, wann …")],
["保險信：事件＋證據＋明確問題。"],["保險","被動","正式"]),
(
"b1-33","dialogue","面試","Vorstellungsgespräch Ausschnitt","面試片段",
"""Personaler: Warum möchten Sie bei uns arbeiten?
Bewerberin: Weil Ihr Unternehmen nachhaltig produziert und ich dazu beitragen möchte.
Personaler: Welche Aufgabe lag Ihnen bisher am meisten?
Bewerberin: Die Kundenberatung, bei der ich Probleme schnell lösen konnte.
Personaler: Und wo sehen Sie sich in drei Jahren?
Bewerberin: Ich hoffe, mehr Verantwortung im Projektmanagement zu übernehmen.""",
"""人資：為什麼想在我們這工作？
應徵者：因為貴公司永續生產，而我想參與其中。
人資：到目前哪項任務最適合你？
應徵者：客戶諮詢，我能快速解問題。
人資：三年後你期待自己在哪？
應徵者：希望在專案管理承擔更多責任。""",
[n("nachhaltig","永續地"),n("dazu beitragen","為此貢獻"),n("lag Ihnen … am meisten","最契合你的是"),n("Verantwortung übernehmen","承擔責任")],
[p("Warum möchten Sie …? — Weil …","面試動機","Weil ich dazulernen will."),p("bei der ich … konnte","關係子句說成就","ein Job, bei dem ich wuchs"),p("Ich hoffe, zu + 不定式","未來希望","Ich hoffe, zu bestehen.")],
["面試標準三問可整段練習。"],["職場","面試","關係句"]),
(
"b1-34","story","親子／照護","Hilfe für die Großeltern","協助祖父母",
"""Meine Großeltern werden älter und brauchen mehr Unterstützung im Alltag.
Einmal pro Woche gehe ich mit ihnen einkaufen und helfe bei Formularen.
Manchmal ist das anstrengend, weil sie alles genau erklärt haben wollen.
Trotzdem bin ich dankbar, Zeit mit ihnen zu verbringen.
Wir haben auch einen Pflegedienst organisiert, der mittags vorbeikommt.
Geteilte Verantwortung macht die Situation leichter.""",
"""祖父母年紀漸長，日常需要更多協助。
我每週陪他們採買一次，並幫忙填表格。
有時很累，因為他們希望每件事都解釋得很清楚。
儘管如此，我很珍惜共處時間。
我們也安排了中午來訪的居家照顧。
分擔責任讓情況輕鬆些。""",
[n("Unterstützung","協助"),n("Formularen","表格"),n("Pflegedienst","居家照顧服務"),n("Geteilte Verantwortung","分擔的責任")],
[p("brauchen mehr Unterstützung bei …","需求表達","brauchen Hilfe beim Lernen"),p("wollen … erklärt haben","希望被解釋清楚","Er will alles schriftlich haben."),p("… organisiert, der/die …","安排＋關係子句","ein Kurs, der abends stattfindet")],
["照護主題：事實＋情感＋資源。"],["家庭","社會","關係句"]),
(
"b1-35","notice","公共","Hitzewarnung","高溫警報",
"""Aktuelle Hitzewarnung für Samstag und Sonntag
Bitte trinken Sie ausreichend und vermeiden Sie schwere Arbeit in der Mittagssonne.
Öffentliche Kühlräume sind in Bibliothek und Rathaus geöffnet.
Ältere Menschen und Kinder besonders beobachten.
Notruf bei Kreislaufproblemen: 112.""",
"""週六日高溫警報
請充足飲水，避免正午做粗重工作。
圖書館與市政廳開放公共降溫空間。
請特別留意長者與孩童。
循環系統不適請打 112。""",
[n("ausreichend","足夠地"),n("vermeiden Sie","請避免"),n("Kühlräume","降溫空間"),n("Kreislaufproblemen","循環／暈眩不適"),n("Notruf","緊急電話")],
[p("Bitte … und vermeiden Sie …","雙重指示","Bitte warten und vermeiden Sie Lärm."),p("sind … geöffnet","開放告知","sind bis 18 Uhr geöffnet"),p("Notruf: 112","緊急資訊","Bei Feuer: 112")],
["公共警告短而明確，先抓行動指示。"],["公共","健康"]),
(
"b1-36","story","語言交換","Tandem-Treffen","語言交換聚會",
"""Alle zwei Wochen treffe ich mich mit meinem Tandempartner.
Eine Stunde sprechen wir Deutsch, eine Stunde seine Muttersprache.
Wir korrigieren uns höflich und notieren neue Wendungen.
Was besonders hilft, sind Themen aus dem echten Leben: Behördengänge, Arbeit, Humor.
Nach dem Treffen schicken wir uns eine kurze Sprachnachricht zur Wiederholung.
So bleibt das Lernen lebendig und verbindlich.""",
"""我每兩週與語伴見面一次。
一小時說德文，一小時說他的母語。
我們禮貌糾正並記下新說法。
特別有幫助的是真實生活主題：辦行政、工作、幽默。
結束後互傳語音訊息複習。
這樣學習既生動又有約束力。""",
[n("Tandempartner","語伴"),n("Wendungen","表達／片語"),n("Behördengänge","跑行政機關"),n("Sprachnachricht","語音訊息"),n("verbindlich","有約束力／可靠的")],
[p("Alle zwei Wochen …","每兩週","Alle drei Tage sportlich."),p("Was besonders hilft, sind …","強調有效方法","Was hilft, sind Beispiele."),p("höflich korrigieren","禮貌糾錯","Bitte korrigiere mich höflich.")],
["學習策略文，可直接仿作你的語伴計畫。"],["學習","社交"]),
(
"b1-37","email","房東通知","Geplante Renovierung","計畫整修通知",
"""Sehr geehrte Mieterinnen und Mieter,

vom 8. bis 12. Juli werden die Flure gestrichen.
In dieser Zeit kann es zu Geruch und eingeschränktem Zugang kommen.
Bitte entfernen Sie Fußmatten und persönliche Gegenstände aus dem Treppenhaus.
Bei Fragen erreichen Sie die Hausverwaltung unter der bekannten Nummer.

Mit freundlichen Grüßen
Hausverwaltung Nord""",
"""親愛的住戶們：

7 月 8 日至 12 日將粉刷走廊。
期間可能有氣味且通行受限。
請將踏墊與個人物品移出樓梯間。
問題請以既有電話聯絡管委。

此致問候
北區管委會""",
[n("werden … gestrichen","將被粉刷", "未來被動。"),n("eingeschränktem Zugang","受限通行"),n("entfernen","移除"),n("Treppenhaus","樓梯間"),n("Hausverwaltung","大樓管理")],
[p("vom … bis … werden …","時段工程被動","vom Montag bis Freitag wird gebaut"),p("kann es zu … kommen","可能出現……","kann es zu Lärm kommen"),p("Bei Fragen erreichen Sie …","聯絡方式","Bei Fragen mailen Sie uns.")],
["大樓通知：時間、影響、住戶要做的事。"],["住房","被動","公告"]),
(
"b1-38","dialogue","客服技術","Account gesperrt","帳號被鎖",
"""Kundin: Ich komme nicht mehr in meinen Account. Es heißt, er sei gesperrt.
Support: Das passiert nach mehreren falschen Passworteingaben.
Kundin: Kann ich das selbst zurücksetzen?
Support: Ja, über „Passwort vergessen“. Falls das nicht geht, prüfen wir Ihre Identität.
Kundin: Per Ausweis-Upload?
Support: Genau, verschlüsselt über das Formular.""",
"""顧客：我登不進帳號。顯示被鎖定。
客服：密碼連續錯誤就會這樣。
顧客：我能自己重設嗎？
客服：可以，用「忘記密碼」。若不行，我們會核對身分。
顧客：用上傳證件？
客服：對，經加密表單。""",
[n("es heißt, er sei gesperrt","顯示／據說被鎖", "間接引語虛擬。"),n("Passworteingaben","密碼輸入"),n("Identität prüfen","核對身分"),n("verschlüsselt","加密的")],
[p("Es heißt, … sei …","轉述系統訊息","Es heißt, der Zug habe Verspätung."),p("Falls das nicht geht, …","備案","Falls das nicht geht, rufen Sie an."),p("über + 功能名","操作路徑","über das Menü einstellen")],
["數位客服：原因→自助→升級驗證。"],["數位","虛擬式"]),
(
"b1-39","story","志工活動組織","Stadtclean-up","城市清潔活動",
"""Letzten Sonntag habe ich bei einem Clean-up im Park mitgemacht.
Wir haben Müll gesammelt und nach Typen getrennt.
Überraschend viele Passanten haben spontan geholfen.
Organisiert wurde die Aktion von einer lokalen Initiative, die regelmäßig aufruft.
Danach gab es Wasser und eine kurze Dankesrunde.
Solche Aktionen zeigen, dass Engagement ansteckend sein kann.""",
"""上週日我參加公園清潔活動。
我們撿垃圾並分類。
意外地許多路人自發幫忙。
活動由在地團體籌辦，他們定期號召。
結束後有水與簡短致謝。
這類活動說明投入可以有感染力。""",
[n("mitgemacht","參加"),n("Passanten","路人"),n("spontan","自發地"),n("Organisiert wurde … von","由……籌辦", "被動置前。"),n("ansteckend","有感染力的")],
[p("Organisiert wurde … von …","被動強調籌辦者","Geschrieben wurde der Text von …"),p("Überraschend viele …","驚訝量化","Überraschend wenig Zeit"),p("zeigen, dass …","結論從句","Das zeigt, dass Übung hilft.")],
["活動報導：過程＋被動＋反思。"],["社會","被動","dass"]),
(
"b1-40","story","遠距友誼","Freundschaft über Distanz","遠距離友誼",
"""Meine beste Freundin wohnt jetzt in einer anderen Stadt.
Am Anfang hatten wir Angst, den Kontakt zu verlieren.
Deshalb haben wir einen festen Video-Abend alle zwei Wochen.
Dazwischen schreiben wir Sprachnachrichten, wenn etwas Wichtiges passiert.
Natürlich ersetzt das nicht echte Treffen, aber es hält die Nähe.
Nächsten Monat besuche ich sie endlich wieder.""",
"""我最好的朋友現在住另一座城市。
一開始我們怕失去聯繫。
因此每兩週固定視訊一晚。
其間若有要事就互傳語音。
當然不能取代見面，但能維持親近。
下個月我終於要再去看她。""",
[n("Angst haben, zu + 不定式","害怕做／發生"),n("festen Video-Abend","固定視訊夜"),n("Dazwischen","其間"),n("ersetzt das nicht","不能取代"),n("hält die Nähe","維持親近感")],
[p("Angst haben, zu …","害怕","Ich habe Angst, Fehler zu machen."),p("Am Anfang … Deshalb …","問題到解法","Am Anfang chaotisch. Deshalb Plan."),p("ersetzt nicht, aber hält …","限制與功能","Das heilt nicht, aber hilft.")],
["情感敘事仍要有結構與連接詞。"],["社交","不定式"]),
]
for t in BATCH4:
    B1.append(item(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9], t[10]))

BATCH5 = [
(
"b1-41","email","正式道歉","Entschuldigung für die Verspätung","延誤致歉",
"""Sehr geehrte Frau Saito,

hiermit entschuldige ich mich für meine Verspätung zum Meeting gestern.
Aufgrund einer Signalstörung im Nahverkehr bin ich 25 Minuten später angekommen.
Künftig plane ich einen größeren Zeitpuffer ein.
Die besprochenen Aufgaben habe ich heute Vormittag bereits erledigt.

Mit freundlichen Grüßen
Tobias Kranz""",
"""敬愛的 Saito 女士：

謹為昨日會議遲到致歉。
因捷運號誌故障，我晚到 25 分鐘。
往後會安排更大時間緩衝。
會中交付的任務我今早已完成。""",
[n("hiermit entschuldige ich mich für","謹為……道歉"),n("Signalstörung","號誌故障"),n("Künftig","今後"),n("Zeitpuffer","時間緩衝"),n("bereits erledigt","已經完成")],
[p("hiermit entschuldige ich mich für + 第四格","正式道歉","Hiermit entschuldige ich mich für den Fehler."),p("Aufgrund + Genitiv","原因","Aufgrund der Störung …"),p("Künftig + 改進","承諾改善","Künftig melde ich mich früher.")],
["道歉信：原因＋改進＋已補救。"],["正式郵件","職場"]),
(
"b1-42","dialogue","住房糾紛調解","Lärmprotokoll","噪音紀錄",
"""Vermittlung: Haben Sie ein Lärmprotokoll geführt?
Mieter: Ja, mit Datum, Uhrzeit und Dauer.
Vermittlung: Das ist hilfreich. Wir sprechen als Nächstes mit der Gegenseite.
Mieter: Was passiert, wenn sich nichts ändert?
Vermittlung: Dann können weitere Schritte bis zur Abmahnung folgen.
Mieter: Verstehe. Ich bleibe erstmal sachlich und dokumentiere weiter.""",
"""調解：您有做噪音紀錄嗎？
房客：有，含日期、時間與持續長度。
調解：這很有幫助。下一步我們會跟對方談。
房客：若沒改善會怎樣？
調解：可能進一步到警告。
房客：了解。我先保持理性並繼續記錄。""",
[n("Lärmprotokoll","噪音紀錄"),n("Gegenseite","對方"),n("als Nächstes","接下來"),n("sachlich bleiben","保持就事論事"),n("dokumentieren","記錄存證")],
[p("Was passiert, wenn sich nichts ändert?","問升級後果","Was passiert, wenn ich ablehne?"),p("weitere Schritte bis zu …","程序升級","Schritte bis zur Kündigung"),p("sachlich bleiben","衝突策略","ruhig und sachlich")],
["糾紛溝通：證據→程序→態度。"],["住房","調解"]),
(
"b1-43","story","永續時尚","Second Hand zuerst","二手優先",
"""Bevor ich neue Kleidung kaufe, schaue ich zuerst in Second-Hand-Läden.
Oft finde ich qualitativ gute Stücke zu einem fairen Preis.
Wenn etwas nicht passt, gebe ich es weiter, statt es wegzuwerfen.
Natürlich kaufe ich manchmal neu, etwa Schuhe für die Arbeit.
Wichtig ist mir die bewusste Entscheidung statt Impuls.
So verbindet sich Stil mit Verantwortung.""",
"""買新衣服前我先逛二手店。
常能找到質感好、價格合理的單品。
不合身就轉送，而不是丟掉。
當然有時仍會買新的，例如工作鞋。
對我重要的是有意識的選擇，而非衝動。
這樣風格能與責任並存。""",
[n("qualitativ gut","品質好"),n("weitergeben","轉送"),n("statt es wegzuwerfen","而不是丟掉"),n("bewusste Entscheidung","有意識的決定"),n("Impuls","衝動")],
[p("Bevor ich …, schaue ich …","優先順序","Bevor ich bestelle, vergleiche ich."),p("statt zu + 不定式","取代","statt zu klagen, handeln"),p("etwa + 例子","例如","etwa am Wochenende")],
["消費議題：原則＋例外＋價值。"],["環境","論述"]),
(
"b1-44","notice","交通新制","Tempolimit in der Innenstadt","市區速限",
"""Ab 1. August gilt in der Innenstadt Tempo 30.
Ziel ist weniger Lärm und mehr Sicherheit für Radfahrende.
Verstöße werden mit Bußgeld geahndet.
Lieferverkehr behält Zufahrtsrechte zu bestimmten Zeiten.
Details stehen auf der Stadtwebsite unter „Mobilität“.""",
"""自 8 月 1 日起市區實施時速 30。
目標是減少噪音並提升對騎車者的安全。
違規將處以罰鍰。
物流車在特定時段仍保有進出權。
詳見市政網站「交通移動」頁。""",
[n("gilt … Tempo 30","實施速限 30"),n("Radfahrende","騎自行車者"),n("Bußgeld","罰鍰"),n("geahndet","被處罰"),n("Zufahrtsrechte","進出權")],
[p("Ab + 日期 gilt …","新制生效","Ab Montag gilt die Regel."),p("werden mit … geahndet","處罰方式","wird mit Verwarnung geahndet"),p("unter + 欄位名","網站路徑","unter Kontakt finden")],
["政策公告：生效日、目的、罰則、例外。"],["公共","被動"]),
(
"b1-45","dialogue","教育諮詢","Abendgymnasium","夜間高中諮詢",
"""Berater: Mit Ihrem Abschluss könnten Sie das Abendgymnasium besuchen.
Interessentin: Wie lange dauert das neben dem Job?
Berater: In der Regel drei bis vier Jahre, je nach Anrechnung.
Interessentin: Und die Kosten?
Berater: Das öffentliche Angebot ist weitgehend kostenfrei; Lernmaterialien zahlen Sie selbst.
Interessentin: Dann beantrage ich zuerst die Einstufung.""",
"""顧問：以您的學歷可就讀夜間高中。
諮詢者：邊工作要念多久？
顧問：通常三到四年，視抵免而定。
諮詢者：費用呢？
顧問：公立大致免費；教材自付。
諮詢者：那我先申請分班測驗。""",
[n("je nach Anrechnung","視抵免而定"),n("weitgehend kostenfrei","大致免費"),n("Lernmaterialien","教材"),n("beantrage","申請"),n("Einstufung","程度／分班鑑定")],
[p("In der Regel …, je nach …","通則＋條件","In der Regel 2 Jahre, je nach Tempo"),p("weitgehend + 形容詞","大致上","weitgehend klar"),p("zuerst + 動詞","先做步驟","zuerst informieren")],
["教育路徑諮詢含時間成本與下一步。"],["學習","行政"]),
(
"b1-46","story","心理健康","Überforderung erkennen","察覺過載",
"""Im letzten Monat war mein Kalender zu voll.
Ich habe Zug um Zug Termine abgesagt, die nicht dringend waren.
Außerdem spreche ich offener mit Freunden, wenn ich Pause brauche.
Überforderung ist kein persönliches Versagen, sondern ein Signal.
Wer früh gegensteuert, verhindert einen größeren Crash.
Heute plane ich bewusst freie Abende ein.""",
"""上個月我的行程太滿。
我逐步取消了不緊急的約會。
此外需要休息時，我也更坦率跟朋友說。
過載不是個人失敗，而是訊號。
及早調整可避免更大崩潰。
現在我會刻意安排空閒晚上。""",
[n("Zug um Zug","逐步地"),n("dringend","緊急的"),n("Überforderung","過載／不堪負荷"),n("Versagen","失敗"),n("gegensteuern","採取對策／糾偏")],
[p("Zug um Zug + 動詞","逐步行動","Zug um Zug aufräumen"),p("ist kein …, sondern ein …","重新定義","ist kein Ende, sondern ein Anfang"),p("Wer früh …, verhindert …","條件忠告","Wer übt, verhindert Panik.")],
["B1 可談抽象主題，但仍用清楚結構。"],["健康","論述","關係句"]),
(
"b1-47","email","合作提案","Kooperationsanfrage","合作詢問",
"""Guten Tag Herr Meier,

wir organisieren einen Sprachtreff für Neuankommende und suchen Räume.
Ihre Nachbarschaftsinitiative wäre ein idealer Partner.
Könnten wir nächste Woche kurz online sprechen?
Anbei finden Sie ein einseitiges Konzept.

Freundliche Grüße
Team Ankommen""",
"""Meier 先生您好，

我們為新住民籌辦語言聚會，正在找場地。
貴鄰里團體會是理想夥伴。
下週可否短線上聊聊？
附件有一頁構想。

問候
Team Ankommen""",
[n("Neuankommende","新到者"),n("Nachbarschaftsinitiative","鄰里倡議團體"),n("Anbei","附件於此"),n("einseitiges Konzept","一頁企劃")],
[p("suchen … und …","需求並列","suchen Räume und Helfer"),p("wäre ein idealer Partner","客氣評價","wäre eine gute Lösung"),p("Anbei finden Sie …","附件套語","Anbei die Unterlagen.")],
["合作信：需求、為何找對方、具體下一步。"],["正式郵件","社區"]),
(
"b1-48","dialogue","簽證／居留","Termin bei der Ausländerbehörde","外國人管理局預約",
"""Sachbearbeiterin: Welche Aufenthaltsfrage betrifft Sie?
Antragsteller: Die Verlängerung meiner Aufenthaltserlaubnis zum Studium.
Sachbearbeiterin: Bitte Immatrikulationsbescheinigung und Finanzierungsnachweis vorlegen.
Antragsteller: Reicht eine Sperrkonto-Bestätigung?
Sachbearbeiterin: Ja, aktuell. Und bitte biometrische Fotos.
Antragsteller: Alles dabei. Wann erfahre ich das Ergebnis?""",
"""承辦：您的居留問題是哪一類？
申請人：學生居留許可延期。
承辦：請提出在學證明與財力證明。
申請人：凍結帳戶證明可以嗎？
承辦：目前可以。還需要證件照。
申請人：都帶了。何時能知道結果？""",
[n("Aufenthaltserlaubnis","居留許可"),n("Immatrikulationsbescheinigung","在學證明"),n("Finanzierungsnachweis","財力證明"),n("Sperrkonto","凍結帳戶"),n("biometrische Fotos","生物辨識照片")],
[p("Welche … betrifft Sie?","分類提問","Welches Anliegen haben Sie?"),p("Bitte … vorlegen","請提出文件","Bitte Pass vorlegen."),p("Wann erfahre ich …?","問結果時程","Wann erfahre ich Bescheid?")],
["機關對話：目的＋文件＋結果時程。"],["行政","居留"]),
(
"b1-49","story","城市參與","Bürgerbeteiligung","公民參與",
"""In meiner Stadt gab es eine Umfrage zur Neugestaltung des Marktplatzes.
Ich habe online abgestimmt und einen Kommentar geschrieben.
Später fand eine öffentliche Sitzung statt, an der auch Anwohnende teilnahmen.
Nicht alle Wünsche können erfüllt werden, aber Transparenz ist wichtig.
Wenn Bürgerinnen und Bürger mitreden, steigt oft die Akzeptanz von Entscheidungen.
Ich werde die Ergebnisse verfolgen.""",
"""我市舉辦市集廣場改造問卷。
我線上投票並寫了評論。
之後有一場公聽會，住戶也參加。
不是所有願望都能實現，但透明很重要。
若公民能參與討論，決策接受度常會提高。
我會持續追蹤結果。""",
[n("Neugestaltung","重新規劃"),n("abgestimmt","投票"),n("an der … teilnahmen","參加該場……", "關係子句。"),n("Transparenz","透明"),n("Akzeptanz","接受度")],
[p("eine Sitzung, an der … teilnehmen","活動＋關係句","ein Kurs, an dem ich teilnehme"),p("Nicht alle …, aber …","現實限制","Nicht alles klappt, aber wir üben."),p("Wenn … mitreden, steigt …","條件與社會結果","Wenn man fragt, steigt Vertrauen.")],
["公民參與文：參與方式＋限制＋意義。"],["社會","關係句","論述"]),
(
"b1-50","story","總複習","Was ich auf B1 anders mache","B1 階段我怎麼學",
"""Auf A2 habe ich vor allem kurze Texte und Dialoge geübt.
Jetzt auf B1 lese ich längere Beiträge und markiere Konnektoren wie deshalb, obwohl, seitdem.
Außerdem schreibe ich E-Mails, in denen ich höflich bitte, begründe und eine Frist nenne.
Wenn ich unsicher bin, formuliere ich Alternativen mit könnte und würde.
Fehler gehören dazu; wichtig ist, dass ich sie korrigiere und wiederverwende.
So wird aus vielen kleinen Texten ein sicherer Stil.""",
"""在 A2 我主要練短文與對話。
現在到 B1，我讀較長文章並標出 deshalb、obwohl、seitdem 等連接詞。
此外我寫郵件：客氣請求、說明理由、提出期限。
不確定時會用 könnte、würde 寫替代說法。
犯錯難免；重要的是改正並再次使用。
如此許多短文會變成更穩的表達風格。""",
[n("Konnektoren","連接詞"),n("begründe","說明理由"),n("Frist nenne","提出期限"),n("formuliere Alternativen","提出替代說法"),n("wiederverwende","再次使用")],
[p("Jetzt auf B1 …","階段對照","Früher …, jetzt …"),p("E-Mails, in denen ich …","關係子句描述文類","Texte, in denen ich argumentiere"),p("wichtig ist, dass …","強調重點","Wichtig ist, dass du übst.")],
["把本篇當 B1 學習宣言，對照你自己的方法。","長度、從句與客氣表達是與 A2 的主要差別。"],
["複習","連接詞","正式寫作","虛擬式"]),
]
for t in BATCH5:
    B1.append(item(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9], t[10]))

assert len(B1) == 50, len(B1)

# Fix typo gestattet in b1-30 notes if present
for it in B1:
    for note in it["notes"]:
        if "gestaltet?" in note.get("zh", ""):
            note["zh"] = "被允許"
        if note["span"] == "gestaltet? gestattet":
            note["span"] = "gestattet"

data = json.loads(PATH.read_text(encoding="utf-8"))
# remove any previous B1
data["items"] = [i for i in data["items"] if i.get("level") != "B1"]
data["items"].extend(B1)
data["levels"] = ["A1", "A2", "B1"]
data["note"] = (
    "A1：短句／對話／告示；A2：段落／郵件／公告；"
    "B1：較長文章與正式情境，含從句、被動與客氣表達。"
)
PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

lens = [len(i["text"]) for i in B1]
print(
    f"B1={len(B1)} avg_len={sum(lens)//len(lens)} "
    f"min={min(lens)} max={max(lens)} total_items={len(data['items'])}"
)
