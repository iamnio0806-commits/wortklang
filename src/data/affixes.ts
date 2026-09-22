/** Shared meanings for German prefixes / suffixes (A1–B1 focus). */

export type AffixKind = 'separable' | 'inseparable' | 'either' | 'suffix'

export type AffixEntry = {
  form: string
  kind: AffixKind
  zh: string
  tip: string
  examples: { de: string; zh: string }[]
}

/** Verb / adjective prefixes — longest forms first for matching. */
export const PREFIX_MEANINGS: AffixEntry[] = [
  {
    form: 'auseinander',
    kind: 'separable',
    zh: '彼此分開',
    tip: '可分；「拆開、分開」。',
    examples: [
      { de: 'auseinandergehen', zh: '散開／分開走' },
      { de: 'auseinandernehmen', zh: '拆開' },
    ],
  },
  {
    form: 'gegenüber',
    kind: 'separable',
    zh: '對面／相對',
    tip: '可分；位置或態度上的「對面」。',
    examples: [
      { de: 'gegenüberstehen', zh: '對面站著；面對' },
      { de: 'gegenübersitzen', zh: '對坐' },
    ],
  },
  {
    form: 'zusammen',
    kind: 'separable',
    zh: '一起／合起來',
    tip: '可分；「聚攏、一起做」。',
    examples: [
      { de: 'zusammenkommen', zh: '聚會' },
      { de: 'zusammenarbeiten', zh: '合作' },
    ],
  },
  {
    form: 'zurück',
    kind: 'separable',
    zh: '回／向後',
    tip: '可分；「回去、還回」。',
    examples: [
      { de: 'zurückkommen', zh: '回來' },
      { de: 'zurückgeben', zh: '歸還' },
    ],
  },
  {
    form: 'weiter',
    kind: 'separable',
    zh: '繼續／往前',
    tip: '可分；「接著做下去」。',
    examples: [
      { de: 'weitergehen', zh: '繼續走' },
      { de: 'weitermachen', zh: '繼續做' },
    ],
  },
  {
    form: 'wieder',
    kind: 'separable',
    zh: '再／又',
    tip: '可分時多半「再次」；wiederholen 是例外（不可分）。',
    examples: [
      { de: 'wiederkommen', zh: '再來' },
      { de: 'wiedersehen', zh: '再見／重逢' },
    ],
  },
  {
    form: 'herunter',
    kind: 'separable',
    zh: '向下／下來',
    tip: '可分；從高處下來。',
    examples: [
      { de: 'herunterkommen', zh: '下來' },
      { de: 'herunterladen', zh: '下載' },
    ],
  },
  {
    form: 'hinein',
    kind: 'separable',
    zh: '進入（向內）',
    tip: '可分；往裡頭去。',
    examples: [{ de: 'hineingehen', zh: '走進去' }],
  },
  {
    form: 'heraus',
    kind: 'separable',
    zh: '出來（向外）',
    tip: '可分；從裡面出來。',
    examples: [{ de: 'herauskommen', zh: '出來' }],
  },
  {
    form: 'durch',
    kind: 'either',
    zh: '穿過／徹底',
    tip: '可分＝實體穿過；不可分＝徹底做完（durchqueren）。',
    examples: [
      { de: 'durchgehen', zh: '走過；檢查' },
      { de: 'durchschauen', zh: '看穿' },
    ],
  },
  {
    form: 'über',
    kind: 'either',
    zh: '越過／過度',
    tip: '可分＝翻過、過來；不可分＝過多、關於（übersehen）。',
    examples: [
      { de: 'überqueren', zh: '穿越（马路）' },
      { de: 'übersetzen', zh: '翻譯' },
    ],
  },
  {
    form: 'unter',
    kind: 'either',
    zh: '在下／不足',
    tip: '可分＝放到下面；不可分＝中斷、簽名（unterschreiben）。',
    examples: [
      { de: 'untergehen', zh: '沉沒；沒落' },
      { de: 'unterschreiben', zh: '簽名' },
    ],
  },
  {
    form: 'um',
    kind: 'either',
    zh: '圍繞／改變',
    tip: '可分＝繞過、翻倒；不可分＝改變（umarmen 擁抱）。',
    examples: [
      { de: 'umsteigen', zh: '轉車' },
      { de: 'umarmen', zh: '擁抱' },
    ],
  },
  {
    form: 'aus',
    kind: 'separable',
    zh: '向外／結束',
    tip: '可分；出來、關掉、結束。',
    examples: [
      { de: 'aussteigen', zh: '下車' },
      { de: 'ausmachen', zh: '關掉；約定' },
    ],
  },
  {
    form: 'auf',
    kind: 'separable',
    zh: '向上／打開',
    tip: '可分；打開、起來、開始。',
    examples: [
      { de: 'aufmachen', zh: '打開' },
      { de: 'aufstehen', zh: '起床' },
    ],
  },
  {
    form: 'ein',
    kind: 'separable',
    zh: '進入／進去',
    tip: '可分；上車、進入、買進。',
    examples: [
      { de: 'einsteigen', zh: '上車' },
      { de: 'einkaufen', zh: '購物' },
    ],
  },
  {
    form: 'an',
    kind: 'separable',
    zh: '靠近／開始',
    tip: '可分；接觸、開始、穿上。',
    examples: [
      { de: 'ankommen', zh: '抵達' },
      { de: 'anziehen', zh: '穿上' },
    ],
  },
  {
    form: 'ab',
    kind: 'separable',
    zh: '離開／下來',
    tip: '可分；出發、取下、分離。',
    examples: [
      { de: 'abfahren', zh: '出發' },
      { de: 'abschließen', zh: '鎖上；完成' },
    ],
  },
  {
    form: 'mit',
    kind: 'separable',
    zh: '一起／帶著',
    tip: '可分；「一起做、帶去」。',
    examples: [
      { de: 'mitkommen', zh: '一起來' },
      { de: 'mitbringen', zh: '帶來' },
    ],
  },
  {
    form: 'nach',
    kind: 'separable',
    zh: '跟隨／再做',
    tip: '可分；跟著、補做、查證。',
    examples: [
      { de: 'nachdenken', zh: '思考' },
      { de: 'nachmachen', zh: '模仿' },
    ],
  },
  {
    form: 'vor',
    kind: 'separable',
    zh: '向前／預先',
    tip: '可分；在前面、事先準備。',
    examples: [
      { de: 'vorbereiten', zh: '準備' },
      { de: 'vorstellen', zh: '介紹；想像' },
    ],
  },
  {
    form: 'zu',
    kind: 'separable',
    zh: '關閉／朝向',
    tip: '可分；關上、朝某方向。',
    examples: [
      { de: 'zumachen', zh: '關上' },
      { de: 'zuhören', zh: '傾聽' },
    ],
  },
  {
    form: 'weg',
    kind: 'separable',
    zh: '離開／弄走',
    tip: '可分；走開、拿走。',
    examples: [
      { de: 'weggehen', zh: '走開' },
      { de: 'wegnehmen', zh: '拿走' },
    ],
  },
  {
    form: 'los',
    kind: 'separable',
    zh: '開始／脫離',
    tip: '可分；「開始吧、鬆開」。',
    examples: [
      { de: 'losgehen', zh: '出發；開始' },
      { de: 'loswerden', zh: '擺脫' },
    ],
  },
  {
    form: 'fest',
    kind: 'separable',
    zh: '固定／牢固',
    tip: '可分；綁緊、確定。',
    examples: [{ de: 'festhalten', zh: '抓住；堅持' }],
  },
  {
    form: 'teil',
    kind: 'separable',
    zh: '分享／參與',
    tip: '可分；參加（teilnehmen）。',
    examples: [{ de: 'teilnehmen', zh: '參加' }],
  },
  {
    form: 'statt',
    kind: 'separable',
    zh: '舉行／發生',
    tip: '可分；stattfinden＝舉行。',
    examples: [{ de: 'stattfinden', zh: '舉行' }],
  },
  {
    form: 'miss',
    kind: 'inseparable',
    zh: '錯誤／不好',
    tip: '不可分；否定、失敗意味。',
    examples: [
      { de: 'missverstehen', zh: '誤解' },
      { de: 'misslingen', zh: '失敗' },
    ],
  },
  {
    form: 'zer',
    kind: 'inseparable',
    zh: '粉碎／弄壞',
    tip: '不可分；弄碎、破壞。',
    examples: [
      { de: 'zerstören', zh: '摧毀' },
      { de: 'zerbrechen', zh: '打破' },
    ],
  },
  {
    form: 'ver',
    kind: 'inseparable',
    zh: '改變／錯／完成',
    tip: '不可分；意思很廣：弄丟、完成、弄錯。',
    examples: [
      { de: 'verstehen', zh: '理解' },
      { de: 'verkaufen', zh: '賣' },
      { de: 'vergessen', zh: '忘記' },
    ],
  },
  {
    form: 'ent',
    kind: 'inseparable',
    zh: '離開／去除／開始',
    tip: '不可分；離開、拿掉、或「開始產生」。',
    examples: [
      { de: 'entfernen', zh: '移除' },
      { de: 'entschuldigen', zh: '道歉' },
      { de: 'entwickeln', zh: '發展' },
    ],
  },
  {
    form: 'emp',
    kind: 'inseparable',
    zh: '感受／接收（ent 變體）',
    tip: '不可分；多出現在 empfinden、empfehlen。',
    examples: [
      { de: 'empfinden', zh: '感受' },
      { de: 'empfehlen', zh: '推薦' },
    ],
  },
  {
    form: 'be',
    kind: 'inseparable',
    zh: '使成為／作用於',
    tip: '不可分；常把不及物變成及物（arbeiten→bearbeiten）。',
    examples: [
      { de: 'besuchen', zh: '拜訪' },
      { de: 'bestellen', zh: '點餐／訂購' },
    ],
  },
  {
    form: 'er',
    kind: 'inseparable',
    zh: '達成／結果',
    tip: '不可分；得到結果、經歷完成。',
    examples: [
      { de: 'erzählen', zh: '講述' },
      { de: 'erklären', zh: '解釋' },
      { de: 'erreichen', zh: '達到' },
    ],
  },
  {
    form: 'ge',
    kind: 'inseparable',
    zh: '集合／過去分詞標記',
    tip: '動詞過去分詞常加 ge-；名詞如 Gefühl 是固定字首。',
    examples: [
      { de: 'gefallen', zh: '喜歡（令…喜歡）' },
      { de: 'gehören', zh: '屬於' },
    ],
  },
  {
    form: 'un',
    kind: 'inseparable',
    zh: '不／非（否定）',
    tip: '多加在形容詞前：möglich→unmöglich。',
    examples: [
      { de: 'unglücklich', zh: '不幸的' },
      { de: 'unmöglich', zh: '不可能的' },
    ],
  },
  {
    form: 'ur',
    kind: 'inseparable',
    zh: '原始／最初',
    tip: '多在名詞：Ursache、Urlaub。',
    examples: [
      { de: 'Ursache', zh: '原因' },
      { de: 'Urlaub', zh: '假期' },
    ],
  },
]

export const SUFFIX_MEANINGS: AffixEntry[] = [
  {
    form: 'schaft',
    kind: 'suffix',
    zh: '群體／狀態（陰性）',
    tip: '多半 die：Freundschaft、Wissenschaft。',
    examples: [
      { de: 'Freundschaft', zh: '友誼' },
      { de: 'Landschaft', zh: '風景' },
    ],
  },
  {
    form: 'igkeit',
    kind: 'suffix',
    zh: '性質／狀態（陰性）',
    tip: 'die；由形容詞變來（möglich→Möglichkeit）。',
    examples: [{ de: 'Möglichkeit', zh: '可能性' }],
  },
  {
    form: 'heit',
    kind: 'suffix',
    zh: '性質／狀態（陰性）',
    tip: 'die：Freiheit、Krankheit。',
    examples: [
      { de: 'Freiheit', zh: '自由' },
      { de: 'Krankheit', zh: '疾病' },
    ],
  },
  {
    form: 'keit',
    kind: 'suffix',
    zh: '性質／狀態（陰性）',
    tip: 'die；常接 -ig／-lich 形容詞後。',
    examples: [
      { de: 'Freundlichkeit', zh: '友善' },
      { de: 'Schwierigkeit', zh: '困難' },
    ],
  },
  {
    form: 'ung',
    kind: 'suffix',
    zh: '動作／結果名詞（陰性）',
    tip: 'die；動詞→名詞：prüfen→Prüfung。',
    examples: [
      { de: 'Übung', zh: '練習' },
      { de: 'Wohnung', zh: '公寓' },
    ],
  },
  {
    form: 'tion',
    kind: 'suffix',
    zh: '外來抽象名詞（陰性）',
    tip: 'die；多來自拉丁／法文。',
    examples: [
      { de: 'Information', zh: '資訊' },
      { de: 'Situation', zh: '情況' },
    ],
  },
  {
    form: 'ismus',
    kind: 'suffix',
    zh: '主義／體系（陽性）',
    tip: 'der：Tourismus、Optimismus。',
    examples: [{ de: 'Tourismus', zh: '觀光業' }],
  },
  {
    form: 'chen',
    kind: 'suffix',
    zh: '小稱（中性）',
    tip: '一律 das；常變母音（Hund→Hündchen）。',
    examples: [
      { de: 'Mädchen', zh: '女孩' },
      { de: 'Brötchen', zh: '小麵包' },
    ],
  },
  {
    form: 'lein',
    kind: 'suffix',
    zh: '小稱（中性）',
    tip: 'das；較文雅／南方：Kindlein。',
    examples: [{ de: 'Kindlein', zh: '小小孩（文）' }],
  },
  {
    form: 'tum',
    kind: 'suffix',
    zh: '狀態／領域',
    tip: '多 das（Eigentum），少數 der（Irrtum）。',
    examples: [
      { de: 'Eigentum', zh: '財產' },
      { de: 'Wachstum', zh: '成長' },
    ],
  },
  {
    form: 'nis',
    kind: 'suffix',
    zh: '結果／狀態',
    tip: 'das 或 die：Ergebnis、Kenntnis。',
    examples: [
      { de: 'Ergebnis', zh: '結果' },
      { de: 'Erlaubnis', zh: '許可' },
    ],
  },
  {
    form: 'bar',
    kind: 'suffix',
    zh: '可…的',
    tip: '形容詞：lesbar＝可讀的。',
    examples: [
      { de: 'essbar', zh: '可食用的' },
      { de: 'sichtbar', zh: '可見的' },
    ],
  },
  {
    form: 'lich',
    kind: 'suffix',
    zh: '…的／…地',
    tip: '形容詞或副詞：freundlich、möglich。',
    examples: [
      { de: 'freundlich', zh: '友善的' },
      { de: 'täglich', zh: '每天的' },
    ],
  },
  {
    form: 'isch',
    kind: 'suffix',
    zh: '…風格／來源的',
    tip: '形容詞：typisch、chinesisch。',
    examples: [
      { de: 'typisch', zh: '典型的' },
      { de: 'praktisch', zh: '實用的' },
    ],
  },
  {
    form: 'ig',
    kind: 'suffix',
    zh: '具有…性質',
    tip: '形容詞：wichtig、richtig、hungrig。',
    examples: [
      { de: 'wichtig', zh: '重要的' },
      { de: 'hungrig', zh: '飢餓的' },
    ],
  },
  {
    form: 'sam',
    kind: 'suffix',
    zh: '帶有…特質',
    tip: '形容詞：langsam、einsam。',
    examples: [
      { de: 'langsam', zh: '慢的' },
      { de: 'gemeinsam', zh: '共同的' },
    ],
  },
  {
    form: 'haft',
    kind: 'suffix',
    zh: '…般的',
    tip: '形容詞：schmerzhaft、lebhaft。',
    examples: [{ de: 'lebhaft', zh: '生動的' }],
  },
  {
    form: 'los',
    kind: 'suffix',
    zh: '沒有…的',
    tip: '形容詞：arbeitslos、kostenlos。',
    examples: [
      { de: 'arbeitslos', zh: '失業的' },
      { de: 'kostenlos', zh: '免費的' },
    ],
  },
  {
    form: 'voll',
    kind: 'suffix',
    zh: '充滿…的',
    tip: '形容詞：erfolgreich 更常見；sinnvoll＝有意義。',
    examples: [
      { de: 'sinnvoll', zh: '有意義的' },
      { de: 'hoffnungsvoll', zh: '充滿希望的' },
    ],
  },
  {
    form: 'er',
    kind: 'suffix',
    zh: '人／器具（陽性）',
    tip: 'der：Lehrer、Computer；女性再加 -in。',
    examples: [
      { de: 'Lehrer', zh: '男老師' },
      { de: 'Fahrer', zh: '司機' },
    ],
  },
  {
    form: 'in',
    kind: 'suffix',
    zh: '女性（陰性）',
    tip: 'die：Lehrerin、Freundin。',
    examples: [
      { de: 'Lehrerin', zh: '女老師' },
      { de: 'Freundin', zh: '女朋友／女性朋友' },
    ],
  },
]

const prefixByForm = new Map(
  PREFIX_MEANINGS.map((e) => [e.form.toLowerCase(), e]),
)
const suffixByForm = new Map(
  SUFFIX_MEANINGS.map((e) => [e.form.toLowerCase(), e]),
)

export function lookupPrefix(form: string): AffixEntry | undefined {
  return prefixByForm.get(form.toLowerCase())
}

export function lookupSuffix(form: string): AffixEntry | undefined {
  return suffixByForm.get(form.toLowerCase())
}

export function affixMeaningLine(
  kind: 'prefix' | 'suffix',
  form: string,
): string | undefined {
  const e = kind === 'prefix' ? lookupPrefix(form) : lookupSuffix(form)
  return e ? `${form}${kind === 'prefix' ? '-' : ''}=${e.zh}` : undefined
}
