/** Shared meanings for German prefixes, roots, and suffixes — ordered by CEFR difficulty. */

export type AffixKind =
  | 'separable'
  | 'inseparable'
  | 'either'
  | 'suffix'
  | 'root'

export type AffixLevel = 'A1' | 'A2' | 'B1' | 'B2'

export type AffixEntry = {
  form: string
  kind: AffixKind
  level: AffixLevel
  zh: string
  tip: string
  examples: { de: string; zh: string }[]
}

const LEVEL_RANK: Record<AffixLevel, number> = {
  A1: 0,
  A2: 1,
  B1: 2,
  B2: 3,
}

export function sortByLevel<T extends { level: AffixLevel }>(items: T[]): T[] {
  return [...items].sort((a, b) => LEVEL_RANK[a.level] - LEVEL_RANK[b.level])
}

/** All prefixes with meanings. Matching uses longest form first via PREFIX_MATCH_FORMS. */
export const PREFIX_MEANINGS: AffixEntry[] = [
  // ── A1 separable (direction / daily) ──
  {
    form: 'ein',
    kind: 'separable',
    level: 'A1',
    zh: '進入／進去',
    tip: '可分；上車、進入、買進。',
    examples: [
      { de: 'einsteigen', zh: '上車' },
      { de: 'einkaufen', zh: '購物' },
      { de: 'einladen', zh: '邀請' },
    ],
  },
  {
    form: 'aus',
    kind: 'separable',
    level: 'A1',
    zh: '向外／結束',
    tip: '可分；出來、關掉、結束。',
    examples: [
      { de: 'aussteigen', zh: '下車' },
      { de: 'ausmachen', zh: '關掉；約定' },
      { de: 'aussehen', zh: '看起來' },
    ],
  },
  {
    form: 'auf',
    kind: 'separable',
    level: 'A1',
    zh: '向上／打開',
    tip: '可分；打開、起來、開始。',
    examples: [
      { de: 'aufmachen', zh: '打開' },
      { de: 'aufstehen', zh: '起床' },
      { de: 'aufräumen', zh: '整理' },
    ],
  },
  {
    form: 'ab',
    kind: 'separable',
    level: 'A1',
    zh: '離開／下來',
    tip: '可分；出發、取下、分離。',
    examples: [
      { de: 'abfahren', zh: '出發' },
      { de: 'abholen', zh: '接（人）' },
      { de: 'abschließen', zh: '鎖上；完成' },
    ],
  },
  {
    form: 'an',
    kind: 'separable',
    level: 'A1',
    zh: '靠近／開始',
    tip: '可分；接觸、開始、穿上。',
    examples: [
      { de: 'ankommen', zh: '抵達' },
      { de: 'anziehen', zh: '穿上' },
      { de: 'anfangen', zh: '開始' },
    ],
  },
  {
    form: 'zu',
    kind: 'separable',
    level: 'A1',
    zh: '關閉／朝向',
    tip: '可分；關上、朝某方向。',
    examples: [
      { de: 'zumachen', zh: '關上' },
      { de: 'zuhören', zh: '傾聽' },
      { de: 'zugeben', zh: '承認' },
    ],
  },
  {
    form: 'mit',
    kind: 'separable',
    level: 'A1',
    zh: '一起／帶著',
    tip: '可分；一起做、帶去。',
    examples: [
      { de: 'mitkommen', zh: '一起來' },
      { de: 'mitbringen', zh: '帶來' },
      { de: 'mitmachen', zh: '一起做；參加' },
    ],
  },
  {
    form: 'vor',
    kind: 'separable',
    level: 'A1',
    zh: '向前／預先',
    tip: '可分；在前面、事先準備。',
    examples: [
      { de: 'vorbereiten', zh: '準備' },
      { de: 'vorstellen', zh: '介紹；想像' },
      { de: 'vorschlagen', zh: '建議' },
    ],
  },
  {
    form: 'nach',
    kind: 'separable',
    level: 'A1',
    zh: '跟隨／再做',
    tip: '可分；跟著、補做、查證。',
    examples: [
      { de: 'nachdenken', zh: '思考' },
      { de: 'nachmachen', zh: '模仿' },
      { de: 'nachfragen', zh: '再詢問' },
    ],
  },
  {
    form: 'weg',
    kind: 'separable',
    level: 'A1',
    zh: '離開／弄走',
    tip: '可分；走開、拿走。',
    examples: [
      { de: 'weggehen', zh: '走開' },
      { de: 'wegnehmen', zh: '拿走' },
    ],
  },
  // ── A1 inseparable ──
  {
    form: 'be',
    kind: 'inseparable',
    level: 'A1',
    zh: '使成為／作用於',
    tip: '不可分；常把不及物變成及物。',
    examples: [
      { de: 'besuchen', zh: '拜訪' },
      { de: 'bestellen', zh: '點餐／訂購' },
      { de: 'bezahlen', zh: '付錢' },
    ],
  },
  {
    form: 'ver',
    kind: 'inseparable',
    level: 'A1',
    zh: '改變／錯／完成',
    tip: '不可分；意思很廣：弄丟、完成、弄錯、理解。',
    examples: [
      { de: 'verstehen', zh: '理解' },
      { de: 'verkaufen', zh: '賣' },
      { de: 'vergessen', zh: '忘記' },
    ],
  },
  {
    form: 'er',
    kind: 'inseparable',
    level: 'A1',
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
    level: 'A1',
    zh: '集合／過去分詞標記',
    tip: '動詞過去分詞常加 ge-；也可當固定字首。',
    examples: [
      { de: 'gefallen', zh: '喜歡（令…喜歡）' },
      { de: 'gehören', zh: '屬於' },
      { de: 'gewinnen', zh: '贏得' },
    ],
  },

  // ── A2 separable ──
  {
    form: 'zurück',
    kind: 'separable',
    level: 'A2',
    zh: '回／向後',
    tip: '可分；回去、還回。',
    examples: [
      { de: 'zurückkommen', zh: '回來' },
      { de: 'zurückgeben', zh: '歸還' },
      { de: 'zurückrufen', zh: '回電話' },
    ],
  },
  {
    form: 'zusammen',
    kind: 'separable',
    level: 'A2',
    zh: '一起／合起來',
    tip: '可分；聚攏、一起做。',
    examples: [
      { de: 'zusammenkommen', zh: '聚會' },
      { de: 'zusammenarbeiten', zh: '合作' },
      { de: 'zusammenfassen', zh: '總結' },
    ],
  },
  {
    form: 'weiter',
    kind: 'separable',
    level: 'A2',
    zh: '繼續／往前',
    tip: '可分；接著做下去。',
    examples: [
      { de: 'weitergehen', zh: '繼續走' },
      { de: 'weitermachen', zh: '繼續做' },
    ],
  },
  {
    form: 'wieder',
    kind: 'separable',
    level: 'A2',
    zh: '再／又',
    tip: '可分多半「再次」；wiederholen 例外（不可分）。',
    examples: [
      { de: 'wiederkommen', zh: '再來' },
      { de: 'wiedersehen', zh: '再見／重逢' },
    ],
  },
  {
    form: 'los',
    kind: 'separable',
    level: 'A2',
    zh: '開始／脫離',
    tip: '可分；出發、開始、鬆開。',
    examples: [
      { de: 'losgehen', zh: '出發；開始' },
      { de: 'loswerden', zh: '擺脫' },
    ],
  },
  {
    form: 'fest',
    kind: 'separable',
    level: 'A2',
    zh: '固定／牢固',
    tip: '可分；綁緊、確定。',
    examples: [
      { de: 'festhalten', zh: '抓住；堅持' },
      { de: 'feststellen', zh: '確認；發現' },
    ],
  },
  {
    form: 'teil',
    kind: 'separable',
    level: 'A2',
    zh: '分享／參與',
    tip: '可分；teilnehmen＝參加。',
    examples: [
      { de: 'teilnehmen', zh: '參加' },
      { de: 'teilen', zh: '分享／分割' },
    ],
  },
  {
    form: 'statt',
    kind: 'separable',
    level: 'A2',
    zh: '舉行／發生',
    tip: '可分；stattfinden＝舉行。',
    examples: [{ de: 'stattfinden', zh: '舉行' }],
  },
  {
    form: 'her',
    kind: 'separable',
    level: 'A2',
    zh: '到這裡來',
    tip: '可分；朝說話者方向。',
    examples: [
      { de: 'herkommen', zh: '過來；出身' },
      { de: 'herstellen', zh: '製造' },
    ],
  },
  {
    form: 'hin',
    kind: 'separable',
    level: 'A2',
    zh: '到那裡去',
    tip: '可分；朝遠方／目標方向。',
    examples: [
      { de: 'hingehen', zh: '去那邊' },
      { de: 'hinfallen', zh: '跌倒' },
    ],
  },
  {
    form: 'herum',
    kind: 'separable',
    level: 'A2',
    zh: '圍繞／到處',
    tip: '可分；繞著、閒晃。',
    examples: [
      { de: 'herumfahren', zh: '到處開' },
      { de: 'herumstehen', zh: '閒站著' },
    ],
  },
  {
    form: 'vorbei',
    kind: 'separable',
    level: 'A2',
    zh: '經過／結束',
    tip: '可分；走過、過去了。',
    examples: [
      { de: 'vorbeikommen', zh: '過來一趟' },
      { de: 'vorbeigehen', zh: '走過；過去' },
    ],
  },
  {
    form: 'entlang',
    kind: 'separable',
    level: 'A2',
    zh: '沿著',
    tip: '可分；多跟第四格／介系詞。',
    examples: [{ de: 'entlanggehen', zh: '沿著走' }],
  },
  // ── A2 inseparable ──
  {
    form: 'ent',
    kind: 'inseparable',
    level: 'A2',
    zh: '離開／去除／開始',
    tip: '不可分；離開、拿掉、或開始產生。',
    examples: [
      { de: 'entfernen', zh: '移除' },
      { de: 'entschuldigen', zh: '道歉' },
      { de: 'entwickeln', zh: '發展' },
    ],
  },
  {
    form: 'emp',
    kind: 'inseparable',
    level: 'A2',
    zh: '感受／接收（ent 變體）',
    tip: '不可分；empfinden、empfehlen。',
    examples: [
      { de: 'empfinden', zh: '感受' },
      { de: 'empfehlen', zh: '推薦' },
    ],
  },
  {
    form: 'un',
    kind: 'inseparable',
    level: 'A2',
    zh: '不／非（否定）',
    tip: '多加在形容詞前。',
    examples: [
      { de: 'unglücklich', zh: '不幸的' },
      { de: 'unmöglich', zh: '不可能的' },
      { de: 'unbekannt', zh: '未知的' },
    ],
  },
  {
    form: 'zer',
    kind: 'inseparable',
    level: 'A2',
    zh: '粉碎／弄壞',
    tip: '不可分；弄碎、破壞。',
    examples: [
      { de: 'zerstören', zh: '摧毀' },
      { de: 'zerbrechen', zh: '打破' },
    ],
  },

  // ── A2 / B1 either ──
  {
    form: 'durch',
    kind: 'either',
    level: 'A2',
    zh: '穿過／徹底',
    tip: '可分＝實體穿過；不可分＝徹底做完。',
    examples: [
      { de: 'durchgehen', zh: '走過；檢查' },
      { de: 'durchschauen', zh: '看穿' },
    ],
  },
  {
    form: 'über',
    kind: 'either',
    level: 'A2',
    zh: '越過／過度',
    tip: '可分＝翻過；不可分＝過多、翻譯。',
    examples: [
      { de: 'überqueren', zh: '穿越（馬路）' },
      { de: 'übersetzen', zh: '翻譯' },
      { de: 'überraschen', zh: '使驚訝' },
    ],
  },
  {
    form: 'unter',
    kind: 'either',
    level: 'A2',
    zh: '在下／不足',
    tip: '可分＝放到下面；不可分＝簽名、中斷。',
    examples: [
      { de: 'untergehen', zh: '沉沒；沒落' },
      { de: 'unterschreiben', zh: '簽名' },
      { de: 'unterstützen', zh: '支持' },
    ],
  },
  {
    form: 'um',
    kind: 'either',
    level: 'A2',
    zh: '圍繞／改變',
    tip: '可分＝繞過、轉車；不可分＝擁抱等。',
    examples: [
      { de: 'umsteigen', zh: '轉車' },
      { de: 'umziehen', zh: '搬家；換衣服' },
      { de: 'umarmen', zh: '擁抱' },
    ],
  },

  // ── B1 separable (direction compounds) ──
  {
    form: 'hinein',
    kind: 'separable',
    level: 'B1',
    zh: '進入（向內）',
    tip: '可分；往裡頭去。',
    examples: [
      { de: 'hineingehen', zh: '走進去' },
      { de: 'hineinschauen', zh: '往裡看' },
    ],
  },
  {
    form: 'heraus',
    kind: 'separable',
    level: 'B1',
    zh: '出來（向外）',
    tip: '可分；從裡面出來。',
    examples: [
      { de: 'herauskommen', zh: '出來' },
      { de: 'herausfinden', zh: '查明' },
    ],
  },
  {
    form: 'herein',
    kind: 'separable',
    level: 'B1',
    zh: '進來（朝說話者）',
    tip: '可分；請進來。',
    examples: [
      { de: 'hereinkommen', zh: '進來' },
      { de: 'hereinbitten', zh: '請進來' },
    ],
  },
  {
    form: 'hinaus',
    kind: 'separable',
    level: 'B1',
    zh: '出去（向遠方）',
    tip: '可分；往外走。',
    examples: [{ de: 'hinausgehen', zh: '走出去' }],
  },
  {
    form: 'hinauf',
    kind: 'separable',
    level: 'B1',
    zh: '往上（去）',
    tip: '可分；往高處去。',
    examples: [{ de: 'hinaufgehen', zh: '走上去' }],
  },
  {
    form: 'hinunter',
    kind: 'separable',
    level: 'B1',
    zh: '往下（去）',
    tip: '可分；往低處去。',
    examples: [{ de: 'hinuntergehen', zh: '走下去' }],
  },
  {
    form: 'herunter',
    kind: 'separable',
    level: 'B1',
    zh: '向下／下來',
    tip: '可分；從高處下來；下載。',
    examples: [
      { de: 'herunterkommen', zh: '下來' },
      { de: 'herunterladen', zh: '下載' },
    ],
  },
  {
    form: 'herauf',
    kind: 'separable',
    level: 'B1',
    zh: '上來（朝說話者）',
    tip: '可分；往上來到這邊。',
    examples: [{ de: 'heraufkommen', zh: '上來' }],
  },
  {
    form: 'hervor',
    kind: 'separable',
    level: 'B1',
    zh: '向前／顯現',
    tip: '可分；出現、突顯。',
    examples: [
      { de: 'hervorkommen', zh: '出現' },
      { de: 'hervorheben', zh: '強調' },
    ],
  },
  {
    form: 'hinzu',
    kind: 'separable',
    level: 'B1',
    zh: '另外加上',
    tip: '可分；補充、外加。',
    examples: [
      { de: 'hinzufügen', zh: '添加' },
      { de: 'hinzukommen', zh: '另外出現' },
    ],
  },
  {
    form: 'entgegen',
    kind: 'separable',
    level: 'B1',
    zh: '迎向／相反',
    tip: '可分；朝對方走去。',
    examples: [
      { de: 'entgegenkommen', zh: '迎面而來；讓步' },
      { de: 'entgegensehen', zh: '期待／面對' },
    ],
  },
  {
    form: 'gegenüber',
    kind: 'separable',
    level: 'B1',
    zh: '對面／相對',
    tip: '可分；位置或態度上的對面。',
    examples: [
      { de: 'gegenüberstehen', zh: '對面站著；面對' },
      { de: 'gegenüberstellen', zh: '對比' },
    ],
  },
  {
    form: 'auseinander',
    kind: 'separable',
    level: 'B1',
    zh: '彼此分開',
    tip: '可分；拆開、分開。',
    examples: [
      { de: 'auseinandergehen', zh: '散開' },
      { de: 'auseinandernehmen', zh: '拆開' },
    ],
  },
  {
    form: 'hinter',
    kind: 'either',
    level: 'B1',
    zh: '在後面',
    tip: '介系詞很常見；動詞字首較少，多為不可分（hinterlassen）。',
    examples: [
      { de: 'hinterlassen', zh: '留下' },
      { de: 'hinterfragen', zh: '質疑' },
    ],
  },
  {
    form: 'zwischen',
    kind: 'either',
    level: 'B1',
    zh: '在之間',
    tip: '介系詞為主；動詞如 zwischenspeichern。',
    examples: [{ de: 'zwischenspeichern', zh: '暫存' }],
  },
  // ── B1 inseparable ──
  {
    form: 'miss',
    kind: 'inseparable',
    level: 'B1',
    zh: '錯誤／不好',
    tip: '不可分；否定、失敗意味。',
    examples: [
      { de: 'missverstehen', zh: '誤解' },
      { de: 'misslingen', zh: '失敗' },
      { de: 'misstrauen', zh: '不信任' },
    ],
  },
  {
    form: 'ur',
    kind: 'inseparable',
    level: 'B1',
    zh: '原始／最初',
    tip: '多在名詞：Ursache、Urlaub。',
    examples: [
      { de: 'Ursache', zh: '原因' },
      { de: 'Urlaub', zh: '假期' },
      { de: 'Ursprung', zh: '起源' },
    ],
  },
  {
    form: 'voll',
    kind: 'separable',
    level: 'B1',
    zh: '完成／裝滿',
    tip: '可分動詞字首較少見；vollenden 是不可分。',
    examples: [
      { de: 'volltanken', zh: '加滿油' },
      { de: 'vollenden', zh: '完成（不可分）' },
    ],
  },
  {
    form: 'wahr',
    kind: 'separable',
    level: 'B1',
    zh: '真實／察覺',
    tip: '可分：wahrnehmen＝察覺。',
    examples: [{ de: 'wahrnehmen', zh: '察覺；感知' }],
  },
  {
    form: 'kenn',
    kind: 'separable',
    level: 'B1',
    zh: '認識／標示',
    tip: '可分：kennenlernen＝認識。',
    examples: [{ de: 'kennenlernen', zh: '認識' }],
  },
  {
    form: 'stand',
    kind: 'separable',
    level: 'B1',
    zh: '站穩／承受',
    tip: '可分：standhalten＝撐住。',
    examples: [{ de: 'standhalten', zh: '撐住；抵擋' }],
  },

  // ── B2 ──
  {
    form: 'wider',
    kind: 'inseparable',
    level: 'B2',
    zh: '反對／抵抗',
    tip: '不可分；widersprechen、widerstand。',
    examples: [
      { de: 'widersprechen', zh: '反駁' },
      { de: 'widerstehen', zh: '抵抗' },
    ],
  },
  {
    form: 'außer',
    kind: 'either',
    level: 'B2',
    zh: '在外／除外',
    tip: '介系詞常見；動詞如 außer Kraft setzen。',
    examples: [{ de: 'außergewöhnlich', zh: '非凡的' }],
  },
  {
    form: 'neben',
    kind: 'either',
    level: 'B2',
    zh: '在旁邊',
    tip: '介系詞為主；複合如 Nebeneffekt。',
    examples: [{ de: 'Nebeneffekt', zh: '副作用' }],
  },
  {
    form: 'innerhalb',
    kind: 'either',
    level: 'B2',
    zh: '在…之內',
    tip: '介系詞／副詞；第二格。',
    examples: [{ de: 'innerhalb einer Woche', zh: '一週之內' }],
  },
  {
    form: 'außerhalb',
    kind: 'either',
    level: 'B2',
    zh: '在…之外',
    tip: '介系詞／副詞；第二格。',
    examples: [{ de: 'außerhalb der Stadt', zh: '城外' }],
  },
  {
    form: 'ober',
    kind: 'either',
    level: 'B2',
    zh: '上方／較高',
    tip: '多在複合名詞：Oberfläche。',
    examples: [{ de: 'Oberfläche', zh: '表面' }],
  },
  {
    form: 'unterhalb',
    kind: 'either',
    level: 'B2',
    zh: '在下方',
    tip: '介系詞／副詞。',
    examples: [{ de: 'unterhalb der Grenze', zh: '在界線下方' }],
  },
]

export const SUFFIX_MEANINGS: AffixEntry[] = [
  // A1
  {
    form: 'ung',
    kind: 'suffix',
    level: 'A1',
    zh: '動作／結果名詞（陰性）',
    tip: 'die；動詞→名詞：prüfen→Prüfung。',
    examples: [
      { de: 'Übung', zh: '練習' },
      { de: 'Wohnung', zh: '公寓' },
      { de: 'Einladung', zh: '邀請' },
    ],
  },
  {
    form: 'er',
    kind: 'suffix',
    level: 'A1',
    zh: '人／器具（陽性）',
    tip: 'der：Lehrer、Computer；女性再加 -in。',
    examples: [
      { de: 'Lehrer', zh: '男老師' },
      { de: 'Fahrer', zh: '司機' },
      { de: 'Computer', zh: '電腦' },
    ],
  },
  {
    form: 'in',
    kind: 'suffix',
    level: 'A1',
    zh: '女性（陰性）',
    tip: 'die：Lehrerin、Freundin。',
    examples: [
      { de: 'Lehrerin', zh: '女老師' },
      { de: 'Freundin', zh: '女朋友／女性朋友' },
    ],
  },
  {
    form: 'chen',
    kind: 'suffix',
    level: 'A1',
    zh: '小稱（中性）',
    tip: '一律 das；常變母音。',
    examples: [
      { de: 'Mädchen', zh: '女孩' },
      { de: 'Brötchen', zh: '小麵包' },
      { de: 'Häuschen', zh: '小房子' },
    ],
  },
  {
    form: 'heit',
    kind: 'suffix',
    level: 'A1',
    zh: '性質／狀態（陰性）',
    tip: 'die：Freiheit、Krankheit。',
    examples: [
      { de: 'Freiheit', zh: '自由' },
      { de: 'Krankheit', zh: '疾病' },
      { de: 'Schönheit', zh: '美麗' },
    ],
  },
  {
    form: 'keit',
    kind: 'suffix',
    level: 'A1',
    zh: '性質／狀態（陰性）',
    tip: 'die；常接 -ig／-lich 後。',
    examples: [
      { de: 'Freundlichkeit', zh: '友善' },
      { de: 'Schwierigkeit', zh: '困難' },
      { de: 'Möglichkeit', zh: '可能性' },
    ],
  },
  {
    form: 'lich',
    kind: 'suffix',
    level: 'A1',
    zh: '…的／…地',
    tip: '形容詞或副詞。',
    examples: [
      { de: 'freundlich', zh: '友善的' },
      { de: 'täglich', zh: '每天的' },
      { de: 'möglich', zh: '可能的' },
    ],
  },
  {
    form: 'ig',
    kind: 'suffix',
    level: 'A1',
    zh: '具有…性質',
    tip: '形容詞：wichtig、richtig。',
    examples: [
      { de: 'wichtig', zh: '重要的' },
      { de: 'hungrig', zh: '飢餓的' },
      { de: 'richtig', zh: '正確的' },
    ],
  },
  {
    form: 'e',
    kind: 'suffix',
    level: 'A1',
    zh: '陰性名詞常見結尾',
    tip: '很多 die 名詞以 -e 結尾（但不保證）。',
    examples: [
      { de: 'Schule', zh: '學校' },
      { de: 'Straße', zh: '街道' },
      { de: 'Lampe', zh: '燈' },
    ],
  },
  // A2
  {
    form: 'schaft',
    kind: 'suffix',
    level: 'A2',
    zh: '群體／狀態（陰性）',
    tip: 'die：Freundschaft、Wissenschaft。',
    examples: [
      { de: 'Freundschaft', zh: '友誼' },
      { de: 'Landschaft', zh: '風景' },
      { de: 'Wissenschaft', zh: '科學' },
    ],
  },
  {
    form: 'nis',
    kind: 'suffix',
    level: 'A2',
    zh: '結果／狀態',
    tip: 'das 或 die：Ergebnis、Kenntnis。',
    examples: [
      { de: 'Ergebnis', zh: '結果' },
      { de: 'Erlaubnis', zh: '許可' },
      { de: 'Geheimnis', zh: '秘密' },
    ],
  },
  {
    form: 'bar',
    kind: 'suffix',
    level: 'A2',
    zh: '可…的',
    tip: '形容詞：lesbar＝可讀的。',
    examples: [
      { de: 'essbar', zh: '可食用的' },
      { de: 'sichtbar', zh: '可見的' },
      { de: 'machbar', zh: '可行的' },
    ],
  },
  {
    form: 'los',
    kind: 'suffix',
    level: 'A2',
    zh: '沒有…的',
    tip: '形容詞：arbeitslos、kostenlos。',
    examples: [
      { de: 'arbeitslos', zh: '失業的' },
      { de: 'kostenlos', zh: '免費的' },
      { de: 'hoffnungslos', zh: '無望的' },
    ],
  },
  {
    form: 'isch',
    kind: 'suffix',
    level: 'A2',
    zh: '…風格／來源的',
    tip: '形容詞：typisch、chinesisch。',
    examples: [
      { de: 'typisch', zh: '典型的' },
      { de: 'praktisch', zh: '實用的' },
      { de: 'chinesisch', zh: '中文的／中國的' },
    ],
  },
  {
    form: 'tion',
    kind: 'suffix',
    level: 'A2',
    zh: '外來抽象名詞（陰性）',
    tip: 'die；多來自拉丁／法文。',
    examples: [
      { de: 'Information', zh: '資訊' },
      { de: 'Situation', zh: '情況' },
      { de: 'Nation', zh: '國家' },
    ],
  },
  {
    form: 'ion',
    kind: 'suffix',
    level: 'A2',
    zh: '外來抽象名詞（陰性）',
    tip: 'die；與 -tion 同類。',
    examples: [
      { de: 'Diskussion', zh: '討論' },
      { de: 'Religion', zh: '宗教' },
    ],
  },
  {
    form: 'lein',
    kind: 'suffix',
    level: 'A2',
    zh: '小稱（中性）',
    tip: 'das；較文雅／南方。',
    examples: [
      { de: 'Kindlein', zh: '小小孩（文）' },
      { de: 'Büchlein', zh: '小書' },
    ],
  },
  {
    form: 'sam',
    kind: 'suffix',
    level: 'A2',
    zh: '帶有…特質',
    tip: '形容詞：langsam、einsam。',
    examples: [
      { de: 'langsam', zh: '慢的' },
      { de: 'gemeinsam', zh: '共同的' },
      { de: 'einsam', zh: '寂寞的' },
    ],
  },
  // B1
  {
    form: 'tum',
    kind: 'suffix',
    level: 'B1',
    zh: '狀態／領域',
    tip: '多 das（Eigentum），少數 der（Irrtum）。',
    examples: [
      { de: 'Eigentum', zh: '財產' },
      { de: 'Wachstum', zh: '成長' },
      { de: 'Reichtum', zh: '財富' },
    ],
  },
  {
    form: 'ismus',
    kind: 'suffix',
    level: 'B1',
    zh: '主義／體系（陽性）',
    tip: 'der：Tourismus、Optimismus。',
    examples: [
      { de: 'Tourismus', zh: '觀光業' },
      { de: 'Optimismus', zh: '樂觀主義' },
    ],
  },
  {
    form: 'haft',
    kind: 'suffix',
    level: 'B1',
    zh: '…般的',
    tip: '形容詞：lebhaft、schmerzhaft。',
    examples: [
      { de: 'lebhaft', zh: '生動的' },
      { de: 'schmerzhaft', zh: '疼痛的' },
    ],
  },
  {
    form: 'voll',
    kind: 'suffix',
    level: 'B1',
    zh: '充滿…的',
    tip: '形容詞：sinnvoll、hoffnungsvoll。',
    examples: [
      { de: 'sinnvoll', zh: '有意義的' },
      { de: 'hoffnungsvoll', zh: '充滿希望的' },
    ],
  },
  {
    form: 'sal',
    kind: 'suffix',
    level: 'B1',
    zh: '結果／狀態',
    tip: 'das：Schicksal、Rätsel。',
    examples: [
      { de: 'Schicksal', zh: '命運' },
      { de: 'Rätsel', zh: '謎' },
    ],
  },
  {
    form: 'ling',
    kind: 'suffix',
    level: 'B1',
    zh: '小／某一類人（陽性）',
    tip: 'der：Lehrling、Frühling。',
    examples: [
      { de: 'Lehrling', zh: '學徒' },
      { de: 'Frühling', zh: '春天' },
      { de: 'Flüchtling', zh: '難民' },
    ],
  },
  {
    form: 'erei',
    kind: 'suffix',
    level: 'B1',
    zh: '場所／行為（陰性）',
    tip: 'die：Bäckerei、Spielerei。',
    examples: [
      { de: 'Bäckerei', zh: '麵包店' },
      { de: 'Druckerei', zh: '印刷廠' },
    ],
  },
  {
    form: 'ität',
    kind: 'suffix',
    level: 'B1',
    zh: '性質（陰性，外來）',
    tip: 'die：Universität、Qualität。',
    examples: [
      { de: 'Universität', zh: '大學' },
      { de: 'Qualität', zh: '品質' },
      { de: 'Aktivität', zh: '活動' },
    ],
  },
  {
    form: 'enz',
    kind: 'suffix',
    level: 'B1',
    zh: '狀態／性質（陰性）',
    tip: 'die：Differenz、Existenz。',
    examples: [
      { de: 'Differenz', zh: '差異' },
      { de: 'Konferenz', zh: '會議' },
    ],
  },
  {
    form: 'anz',
    kind: 'suffix',
    level: 'B1',
    zh: '狀態／性質（陰性）',
    tip: 'die：Toleranz、Distanz。',
    examples: [
      { de: 'Toleranz', zh: '容忍' },
      { de: 'Distanz', zh: '距離' },
    ],
  },
  {
    form: 'ment',
    kind: 'suffix',
    level: 'B1',
    zh: '結果／工具（中性，外來）',
    tip: 'das：Dokument、Instrument。',
    examples: [
      { de: 'Dokument', zh: '文件' },
      { de: 'Instrument', zh: '儀器／樂器' },
    ],
  },
  // B2
  {
    form: 'igkeit',
    kind: 'suffix',
    level: 'B2',
    zh: '性質／狀態（陰性）',
    tip: 'die；由 -ig 形容詞變來。',
    examples: [
      { de: 'Möglichkeit', zh: '可能性' },
      { de: 'Geschwindigkeit', zh: '速度' },
    ],
  },
  {
    form: 'atur',
    kind: 'suffix',
    level: 'B2',
    zh: '性質／產物（陰性）',
    tip: 'die：Natur、Literatur、Temperatur。',
    examples: [
      { de: 'Natur', zh: '自然' },
      { de: 'Literatur', zh: '文學' },
      { de: 'Temperatur', zh: '溫度' },
    ],
  },
  {
    form: 'ur',
    kind: 'suffix',
    level: 'B2',
    zh: '結果／狀態（陰性）',
    tip: 'die：Kultur、Figur。',
    examples: [
      { de: 'Kultur', zh: '文化' },
      { de: 'Figur', zh: '人物／身材' },
    ],
  },
  {
    form: 'iv',
    kind: 'suffix',
    level: 'B2',
    zh: '…的（形容詞）或中性名詞',
    tip: 'aktiv；das Aktiv／Adjektiv。',
    examples: [
      { de: 'aktiv', zh: '積極的' },
      { de: 'positiv', zh: '正面的' },
    ],
  },
  {
    form: 'abel',
    kind: 'suffix',
    level: 'B2',
    zh: '可…的（外來）',
    tip: '形容詞：variabel、komfortabel。',
    examples: [
      { de: 'komfortabel', zh: '舒適的' },
      { de: 'variabel', zh: '可變的' },
    ],
  },
  {
    form: 'ös',
    kind: 'suffix',
    level: 'B2',
    zh: '充滿…的（外來）',
    tip: '形容詞：nervös、religös。',
    examples: [
      { de: 'nervös', zh: '緊張的' },
      { de: 'religiös', zh: '宗教的' },
    ],
  },
  {
    form: 'eur',
    kind: 'suffix',
    level: 'B2',
    zh: '從事某事的人（陽性）',
    tip: 'der：Friseur、Ingenieur。',
    examples: [
      { de: 'Friseur', zh: '男髮型師' },
      { de: 'Ingenieur', zh: '工程師' },
    ],
  },
  {
    form: 'är',
    kind: 'suffix',
    level: 'B2',
    zh: '人／相關（陽性或形容詞）',
    tip: 'der Sekretär；militär。',
    examples: [
      { de: 'Sekretär', zh: '男秘書' },
      { de: 'Millionär', zh: '百萬富翁' },
    ],
  },
]

/** Common stems / roots shown on the intro page (not all used for auto-split). */
export const ROOT_MEANINGS: AffixEntry[] = [
  // A1 everyday verb stems
  {
    form: 'geh',
    kind: 'root',
    level: 'A1',
    zh: '走／去',
    tip: 'gehen、Ausgang、Eingang。',
    examples: [
      { de: 'gehen', zh: '走；去' },
      { de: 'Ausgang', zh: '出口' },
      { de: 'Eingang', zh: '入口' },
    ],
  },
  {
    form: 'komm',
    kind: 'root',
    level: 'A1',
    zh: '來',
    tip: 'kommen、Ankunft、willkommen。',
    examples: [
      { de: 'kommen', zh: '來' },
      { de: 'Ankunft', zh: '抵達' },
      { de: 'willkommen', zh: '歡迎' },
    ],
  },
  {
    form: 'steh',
    kind: 'root',
    level: 'A1',
    zh: '站／立',
    tip: 'stehen、verstehen、Aufstand。',
    examples: [
      { de: 'stehen', zh: '站' },
      { de: 'verstehen', zh: '理解' },
      { de: 'Aufstehen', zh: '起床（名詞化）' },
    ],
  },
  {
    form: 'seh',
    kind: 'root',
    level: 'A1',
    zh: '看',
    tip: 'sehen、aussehen、Fernsehen。',
    examples: [
      { de: 'sehen', zh: '看' },
      { de: 'aussehen', zh: '看起來' },
      { de: 'Fernseher', zh: '電視' },
    ],
  },
  {
    form: 'hör',
    kind: 'root',
    level: 'A1',
    zh: '聽',
    tip: 'hören、zuhören、Hörspiel。',
    examples: [
      { de: 'hören', zh: '聽' },
      { de: 'zuhören', zh: '傾聽' },
    ],
  },
  {
    form: 'sprech',
    kind: 'root',
    level: 'A1',
    zh: '說',
    tip: 'sprechen、Sprache、Gespräch。',
    examples: [
      { de: 'sprechen', zh: '說' },
      { de: 'Sprache', zh: '語言' },
      { de: 'Gespräch', zh: '談話' },
    ],
  },
  {
    form: 'schreib',
    kind: 'root',
    level: 'A1',
    zh: '寫',
    tip: 'schreiben、Schrift、Beschreibung。',
    examples: [
      { de: 'schreiben', zh: '寫' },
      { de: 'Schrift', zh: '文字／字體' },
      { de: 'Beschreibung', zh: '描述' },
    ],
  },
  {
    form: 'les',
    kind: 'root',
    level: 'A1',
    zh: '讀',
    tip: 'lesen、Vorlesen、Leser。',
    examples: [
      { de: 'lesen', zh: '讀' },
      { de: 'Vorlesen', zh: '朗讀' },
    ],
  },
  {
    form: 'fahr',
    kind: 'root',
    level: 'A1',
    zh: '乘／開',
    tip: 'fahren、Fahrrad、Abfahrt。',
    examples: [
      { de: 'fahren', zh: '開／搭乘' },
      { de: 'Fahrrad', zh: '腳踏車' },
      { de: 'Abfahrt', zh: '出發' },
    ],
  },
  {
    form: 'lauf',
    kind: 'root',
    level: 'A1',
    zh: '跑／流動',
    tip: 'laufen、Ablauf、Verlauf。',
    examples: [
      { de: 'laufen', zh: '跑；走' },
      { de: 'Ablauf', zh: '流程' },
    ],
  },
  {
    form: 'nehm',
    kind: 'root',
    level: 'A1',
    zh: '拿／取',
    tip: 'nehmen、aufnehmen、Teilnahme。',
    examples: [
      { de: 'nehmen', zh: '拿' },
      { de: 'teilnehmen', zh: '參加' },
      { de: 'aufnehmen', zh: '錄取；錄製' },
    ],
  },
  {
    form: 'geb',
    kind: 'root',
    level: 'A1',
    zh: '給',
    tip: 'geben、Ausgabe、Aufgabe。',
    examples: [
      { de: 'geben', zh: '給' },
      { de: 'Aufgabe', zh: '作業／任務' },
      { de: 'Ausgabe', zh: '支出；發行' },
    ],
  },
  {
    form: 'mach',
    kind: 'root',
    level: 'A1',
    zh: '做／弄',
    tip: 'machen、aufmachen、zumachen。',
    examples: [
      { de: 'machen', zh: '做' },
      { de: 'aufmachen', zh: '打開' },
    ],
  },
  {
    form: 'wohn',
    kind: 'root',
    level: 'A1',
    zh: '住',
    tip: 'wohnen、Wohnung、Bewohner。',
    examples: [
      { de: 'wohnen', zh: '住' },
      { de: 'Wohnung', zh: '公寓' },
    ],
  },
  {
    form: 'lern',
    kind: 'root',
    level: 'A1',
    zh: '學',
    tip: 'lernen、Lehrling、gelernt。',
    examples: [
      { de: 'lernen', zh: '學習' },
      { de: 'Lehrling', zh: '學徒' },
    ],
  },
  {
    form: 'arbeit',
    kind: 'root',
    level: 'A1',
    zh: '工作',
    tip: 'arbeiten、Arbeit、bearbeiten。',
    examples: [
      { de: 'arbeiten', zh: '工作' },
      { de: 'Arbeit', zh: '工作（名詞）' },
      { de: 'bearbeiten', zh: '處理' },
    ],
  },
  {
    form: 'spiel',
    kind: 'root',
    level: 'A1',
    zh: '玩／比賽',
    tip: 'spielen、Spiel、Beispiel。',
    examples: [
      { de: 'spielen', zh: '玩；演奏' },
      { de: 'Beispiel', zh: '例子' },
    ],
  },
  {
    form: 'kauf',
    kind: 'root',
    level: 'A1',
    zh: '買',
    tip: 'kaufen、einkaufen、Verkauf。',
    examples: [
      { de: 'kaufen', zh: '買' },
      { de: 'einkaufen', zh: '購物' },
      { de: 'Verkauf', zh: '販售' },
    ],
  },
  {
    form: 'denk',
    kind: 'root',
    level: 'A1',
    zh: '想',
    tip: 'denken、Gedanke、nachdenken。',
    examples: [
      { de: 'denken', zh: '想' },
      { de: 'nachdenken', zh: '思考' },
      { de: 'Gedanke', zh: '想法' },
    ],
  },
  {
    form: 'find',
    kind: 'root',
    level: 'A1',
    zh: '找到',
    tip: 'finden、erfinden、gefunden。',
    examples: [
      { de: 'finden', zh: '找到' },
      { de: 'erfinden', zh: '發明' },
    ],
  },
  {
    form: 'frag',
    kind: 'root',
    level: 'A1',
    zh: '問',
    tip: 'fragen、Frage、anfragen。',
    examples: [
      { de: 'fragen', zh: '問' },
      { de: 'Frage', zh: '問題' },
    ],
  },
  {
    form: 'sag',
    kind: 'root',
    level: 'A1',
    zh: '說',
    tip: 'sagen、Aussage、Absage。',
    examples: [
      { de: 'sagen', zh: '說' },
      { de: 'Aussage', zh: '陳述' },
    ],
  },
  {
    form: 'lieb',
    kind: 'root',
    level: 'A1',
    zh: '愛／親愛',
    tip: 'lieben、Liebe、lieb。',
    examples: [
      { de: 'lieben', zh: '愛' },
      { de: 'Liebe', zh: '愛（名詞）' },
    ],
  },
  {
    form: 'leb',
    kind: 'root',
    level: 'A1',
    zh: '生活／活',
    tip: 'leben、Leben、Erlebnis。',
    examples: [
      { de: 'leben', zh: '生活' },
      { de: 'Erlebnis', zh: '經歷' },
    ],
  },
  {
    form: 'haus',
    kind: 'root',
    level: 'A1',
    zh: '房子／家',
    tip: 'Haus、Haustür、Krankenhaus。',
    examples: [
      { de: 'Haus', zh: '房子' },
      { de: 'Krankenhaus', zh: '醫院' },
    ],
  },
  {
    form: 'zeit',
    kind: 'root',
    level: 'A1',
    zh: '時間',
    tip: 'Zeit、Zeitung、Freizeit。',
    examples: [
      { de: 'Zeit', zh: '時間' },
      { de: 'Zeitung', zh: '報紙' },
      { de: 'Freizeit', zh: '空閒時間' },
    ],
  },
  {
    form: 'tag',
    kind: 'root',
    level: 'A1',
    zh: '日子',
    tip: 'Tag、Alltag、Montag。',
    examples: [
      { de: 'Tag', zh: '天；日子' },
      { de: 'Alltag', zh: '日常生活' },
    ],
  },
  {
    form: 'jahr',
    kind: 'root',
    level: 'A1',
    zh: '年',
    tip: 'Jahr、Jahrestag、Schuljahr。',
    examples: [
      { de: 'Jahr', zh: '年' },
      { de: 'Schuljahr', zh: '學年' },
    ],
  },
  {
    form: 'freund',
    kind: 'root',
    level: 'A1',
    zh: '朋友',
    tip: 'Freund、Freundschaft、freundschaftlich。',
    examples: [
      { de: 'Freund', zh: '朋友' },
      { de: 'Freundschaft', zh: '友誼' },
    ],
  },
  {
    form: 'kind',
    kind: 'root',
    level: 'A1',
    zh: '孩子',
    tip: 'Kind、Kinderzimmer、Kindheit。',
    examples: [
      { de: 'Kind', zh: '孩子' },
      { de: 'Kindheit', zh: '童年' },
    ],
  },
  {
    form: 'wort',
    kind: 'root',
    level: 'A1',
    zh: '詞／話',
    tip: 'Wort、Antwort、Wörterbuch。',
    examples: [
      { de: 'Wort', zh: '詞' },
      { de: 'Antwort', zh: '回答' },
      { de: 'Wörterbuch', zh: '詞典' },
    ],
  },
  {
    form: 'land',
    kind: 'root',
    level: 'A1',
    zh: '土地／國家',
    tip: 'Land、Deutschland、Landschaft。',
    examples: [
      { de: 'Land', zh: '國家／鄉下' },
      { de: 'Deutschland', zh: '德國' },
    ],
  },

  // A2
  {
    form: 'halt',
    kind: 'root',
    level: 'A2',
    zh: '持／停／維持',
    tip: 'halten、Inhalt、Aufenthalt。',
    examples: [
      { de: 'halten', zh: '握住；停' },
      { de: 'Inhalt', zh: '內容' },
      { de: 'Aufenthalt', zh: '停留' },
    ],
  },
  {
    form: 'trag',
    kind: 'root',
    level: 'A2',
    zh: '帶／承擔',
    tip: 'tragen、Auftrag、Beitrag。',
    examples: [
      { de: 'tragen', zh: '拿；穿' },
      { de: 'Auftrag', zh: '委託／訂單' },
      { de: 'Beitrag', zh: '貢獻；文章' },
    ],
  },
  {
    form: 'zieh',
    kind: 'root',
    level: 'A2',
    zh: '拉／穿／搬',
    tip: 'ziehen、anziehen、umziehen。',
    examples: [
      { de: 'ziehen', zh: '拉' },
      { de: 'anziehen', zh: '穿上' },
      { de: 'umziehen', zh: '搬家' },
    ],
  },
  {
    form: 'schließ',
    kind: 'root',
    level: 'A2',
    zh: '關／結',
    tip: 'schließen、Abschluss、entschließen。',
    examples: [
      { de: 'schließen', zh: '關上' },
      { de: 'Abschluss', zh: '結束；畢業' },
    ],
  },
  {
    form: 'öffn',
    kind: 'root',
    level: 'A2',
    zh: '開',
    tip: 'öffnen、Öffnung、öffentlich。',
    examples: [
      { de: 'öffnen', zh: '打開' },
      { de: 'öffentlich', zh: '公開的' },
    ],
  },
  {
    form: 'bind',
    kind: 'root',
    level: 'A2',
    zh: '綁／連結',
    tip: 'binden、Verbindung、verbindlich。',
    examples: [
      { de: 'binden', zh: '綁' },
      { de: 'Verbindung', zh: '連結；轉機' },
    ],
  },
  {
    form: 'bild',
    kind: 'root',
    level: 'A2',
    zh: '形／圖／形成',
    tip: 'Bild、bilden、Ausbildung。',
    examples: [
      { de: 'Bild', zh: '圖／照片' },
      { de: 'bilden', zh: '形成；教育' },
      { de: 'Ausbildung', zh: '培訓' },
    ],
  },
  {
    form: 'stell',
    kind: 'root',
    level: 'A2',
    zh: '放置／呈現',
    tip: 'stellen、vorstellen、Bestellung。',
    examples: [
      { de: 'stellen', zh: '放置' },
      { de: 'vorstellen', zh: '介紹' },
      { de: 'Bestellung', zh: '訂單' },
    ],
  },
  {
    form: 'leg',
    kind: 'root',
    level: 'A2',
    zh: '放／躺下使役',
    tip: 'legen、überlegen、Auslegung。',
    examples: [
      { de: 'legen', zh: '放下' },
      { de: 'überlegen', zh: '考慮' },
    ],
  },
  {
    form: 'setz',
    kind: 'root',
    level: 'A2',
    zh: '放／設',
    tip: 'setzen、übersetzen、Fortsetzung。',
    examples: [
      { de: 'setzen', zh: '使坐下；放置' },
      { de: 'übersetzen', zh: '翻譯' },
    ],
  },
  {
    form: 'fall',
    kind: 'root',
    level: 'A2',
    zh: '掉／發生',
    tip: 'fallen、Zufall、Ausfall。',
    examples: [
      { de: 'fallen', zh: '掉落' },
      { de: 'Zufall', zh: '巧合' },
      { de: 'Ausfall', zh: '取消；故障' },
    ],
  },
  {
    form: 'bleib',
    kind: 'root',
    level: 'A2',
    zh: '留下／停留',
    tip: 'bleiben、übrigbleiben。',
    examples: [
      { de: 'bleiben', zh: '留下' },
      { de: 'übrigbleiben', zh: '剩下' },
    ],
  },
  {
    form: 'flieg',
    kind: 'root',
    level: 'A2',
    zh: '飛',
    tip: 'fliegen、Flug、Flughafen。',
    examples: [
      { de: 'fliegen', zh: '飛' },
      { de: 'Flughafen', zh: '機場' },
    ],
  },
  {
    form: 'schwimm',
    kind: 'root',
    level: 'A2',
    zh: '游泳',
    tip: 'schwimmen、Schwimmbad。',
    examples: [
      { de: 'schwimmen', zh: '游泳' },
      { de: 'Schwimmbad', zh: '游泳池' },
    ],
  },
  {
    form: 'sicher',
    kind: 'root',
    level: 'A2',
    zh: '安全／確定',
    tip: 'sicher、Sicherheit、versichern。',
    examples: [
      { de: 'sicher', zh: '安全的；確定的' },
      { de: 'Sicherheit', zh: '安全' },
    ],
  },
  {
    form: 'frei',
    kind: 'root',
    level: 'A2',
    zh: '自由／空的',
    tip: 'frei、Freiheit、Freizeit。',
    examples: [
      { de: 'frei', zh: '自由的；空的' },
      { de: 'Freizeit', zh: '空閒' },
    ],
  },
  {
    form: 'möglich',
    kind: 'root',
    level: 'A2',
    zh: '可能',
    tip: 'möglich、Möglichkeit、unmöglich。',
    examples: [
      { de: 'möglich', zh: '可能的' },
      { de: 'Möglichkeit', zh: '可能性' },
    ],
  },
  {
    form: 'werk',
    kind: 'root',
    level: 'A2',
    zh: '作品／工廠',
    tip: 'Werk、Netzwerk、Feuerwerk。',
    examples: [
      { de: 'Werk', zh: '作品；工廠' },
      { de: 'Netzwerk', zh: '網路' },
    ],
  },
  {
    form: 'schrift',
    kind: 'root',
    level: 'A2',
    zh: '書寫／字體',
    tip: 'Schrift、Unterschrift、Zeitschrift。',
    examples: [
      { de: 'Schrift', zh: '文字' },
      { de: 'Unterschrift', zh: '簽名' },
      { de: 'Zeitschrift', zh: '雜誌' },
    ],
  },

  // B1 Latin / international
  {
    form: 'graph',
    kind: 'root',
    level: 'B1',
    zh: '寫／畫',
    tip: '國際字根：Fotografie、Autograph。',
    examples: [
      { de: 'Fotografie', zh: '攝影' },
      { de: 'Biografie', zh: '傳記' },
    ],
  },
  {
    form: 'phon',
    kind: 'root',
    level: 'B1',
    zh: '聲音',
    tip: 'Telefon、Mikrofon、Sinfonie。',
    examples: [
      { de: 'Telefon', zh: '電話' },
      { de: 'Mikrofon', zh: '麥克風' },
    ],
  },
  {
    form: 'log',
    kind: 'root',
    level: 'B1',
    zh: '說／學／理',
    tip: 'Biologie、Dialog、Logik。',
    examples: [
      { de: 'Biologie', zh: '生物學' },
      { de: 'Dialog', zh: '對話' },
    ],
  },
  {
    form: 'meter',
    kind: 'root',
    level: 'B1',
    zh: '測量',
    tip: 'Meter、Thermometer、Parameter。',
    examples: [
      { de: 'Meter', zh: '公尺' },
      { de: 'Thermometer', zh: '溫度計' },
    ],
  },
  {
    form: 'bio',
    kind: 'root',
    level: 'B1',
    zh: '生命',
    tip: 'Biologie、Biografie、biologisch。',
    examples: [
      { de: 'Biologie', zh: '生物學' },
      { de: 'biologisch', zh: '生物的；有機的' },
    ],
  },
  {
    form: 'geo',
    kind: 'root',
    level: 'B1',
    zh: '地',
    tip: 'Geografie、Geologie。',
    examples: [
      { de: 'Geografie', zh: '地理' },
      { de: 'Geologie', zh: '地質學' },
    ],
  },
  {
    form: 'tele',
    kind: 'root',
    level: 'B1',
    zh: '遠',
    tip: 'Telefon、Television、Telegramm。',
    examples: [
      { de: 'Telefon', zh: '電話' },
      { de: 'Television', zh: '電視（文）' },
    ],
  },
  {
    form: 'auto',
    kind: 'root',
    level: 'B1',
    zh: '自己／汽車',
    tip: 'Auto、automatisch、Autobiografie。',
    examples: [
      { de: 'Auto', zh: '汽車' },
      { de: 'automatisch', zh: '自動的' },
    ],
  },
  {
    form: 'port',
    kind: 'root',
    level: 'B1',
    zh: '帶／運',
    tip: '拉丁：Transport、importieren、Sport。',
    examples: [
      { de: 'Transport', zh: '運輸' },
      { de: 'importieren', zh: '進口' },
    ],
  },
  {
    form: 'form',
    kind: 'root',
    level: 'B1',
    zh: '形狀／形式',
    tip: 'Form、Information、reformieren。',
    examples: [
      { de: 'Form', zh: '形式' },
      { de: 'Information', zh: '資訊' },
    ],
  },
  {
    form: 'dict',
    kind: 'root',
    level: 'B1',
    zh: '說／指示',
    tip: 'diktieren、Wörterbuch（異形）、Predigt。',
    examples: [
      { de: 'diktieren', zh: '口述；獨裁式下達' },
      { de: 'Diktat', zh: '聽寫；命令' },
    ],
  },
  {
    form: 'spect',
    kind: 'root',
    level: 'B1',
    zh: '看',
    tip: 'Aspekt、Inspektion、Respekt。',
    examples: [
      { de: 'Aspekt', zh: '面向' },
      { de: 'Respekt', zh: '尊重' },
    ],
  },
  {
    form: 'struct',
    kind: 'root',
    level: 'B1',
    zh: '建造',
    tip: 'Struktur、konstruieren、Instruktion。',
    examples: [
      { de: 'Struktur', zh: '結構' },
      { de: 'konstruieren', zh: '建造；構想' },
    ],
  },
  {
    form: 'duc',
    kind: 'root',
    level: 'B1',
    zh: '引導／帶領',
    tip: 'produzieren、reduzieren、Produkt。',
    examples: [
      { de: 'produzieren', zh: '生產' },
      { de: 'Produkt', zh: '產品' },
    ],
  },

  // B2
  {
    form: 'inter',
    kind: 'root',
    level: 'B2',
    zh: '之間',
    tip: 'international、Internet、Interview。',
    examples: [
      { de: 'international', zh: '國際的' },
      { de: 'Interview', zh: '訪談' },
    ],
  },
  {
    form: 'trans',
    kind: 'root',
    level: 'B2',
    zh: '穿過／轉移',
    tip: 'Transport、transparent、Transformation。',
    examples: [
      { de: 'Transport', zh: '運輸' },
      { de: 'transparent', zh: '透明的' },
    ],
  },
  {
    form: 'prä',
    kind: 'root',
    level: 'B2',
    zh: '預先',
    tip: 'Präsens、präsentieren、Präposition。',
    examples: [
      { de: 'präsentieren', zh: '展示' },
      { de: 'Präposition', zh: '介系詞' },
    ],
  },
  {
    form: 're',
    kind: 'root',
    level: 'B2',
    zh: '再／回',
    tip: '外來：reagieren、reparieren、reformieren。',
    examples: [
      { de: 'reagieren', zh: '反應' },
      { de: 'reparieren', zh: '修理' },
    ],
  },
  {
    form: 'anti',
    kind: 'root',
    level: 'B2',
    zh: '反對／抗',
    tip: 'Antibiotikum、antipathisch。',
    examples: [{ de: 'Antibiotikum', zh: '抗生素' }],
  },
  {
    form: 'multi',
    kind: 'root',
    level: 'B2',
    zh: '多',
    tip: 'Multimedia、multipel。',
    examples: [{ de: 'Multimedia', zh: '多媒體' }],
  },
  {
    form: 'mini',
    kind: 'root',
    level: 'B2',
    zh: '小',
    tip: 'Minimum、minimal、Minister。',
    examples: [
      { de: 'Minimum', zh: '最小值' },
      { de: 'minimal', zh: '最小的' },
    ],
  },
  {
    form: 'super',
    kind: 'root',
    level: 'B2',
    zh: '超／上',
    tip: 'Supermarkt、super、Superior。',
    examples: [
      { de: 'Supermarkt', zh: '超市' },
      { de: 'super', zh: '超棒' },
    ],
  },
  {
    form: 'sub',
    kind: 'root',
    level: 'B2',
    zh: '在下／次',
    tip: 'Subjekt、subjektiv、Substanz。',
    examples: [
      { de: 'Subjekt', zh: '主語；主體' },
      { de: 'subjektiv', zh: '主觀的' },
    ],
  },
  {
    form: 'kon',
    kind: 'root',
    level: 'B2',
    zh: '一起／共同',
    tip: 'Kontakt、Konzert、kontrollieren。',
    examples: [
      { de: 'Kontakt', zh: '聯絡' },
      { de: 'Konzert', zh: '音樂會' },
    ],
  },
  {
    form: 'ex',
    kind: 'root',
    level: 'B2',
    zh: '出／前',
    tip: 'Export、existieren、extrem。',
    examples: [
      { de: 'Export', zh: '出口' },
      { de: 'existieren', zh: '存在' },
    ],
  },
  {
    form: 'pro',
    kind: 'root',
    level: 'B2',
    zh: '向前／親',
    tip: 'Problem、produzieren、Profession。',
    examples: [
      { de: 'Problem', zh: '問題' },
      { de: 'produzieren', zh: '生產' },
    ],
  },
]

const allForLookup = [...PREFIX_MEANINGS, ...SUFFIX_MEANINGS]

const prefixByForm = new Map(
  PREFIX_MEANINGS.map((e) => [e.form.toLowerCase(), e]),
)
const suffixByForm = new Map(
  SUFFIX_MEANINGS.map((e) => [e.form.toLowerCase(), e]),
)

/** Longest-first forms for stripping prefixes in enrich.ts */
export const PREFIX_MATCH_FORMS: string[] = [
  ...new Set(PREFIX_MEANINGS.map((e) => e.form.toLowerCase())),
].sort((a, b) => b.length - a.length)

/** Longest-first forms for stripping suffixes */
export const SUFFIX_MATCH_FORMS: string[] = [
  ...new Set(SUFFIX_MEANINGS.map((e) => e.form.toLowerCase())),
].sort((a, b) => b.length - a.length)

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
  if (!e) return undefined
  return kind === 'prefix' ? `${form}-=${e.zh}` : `-${form}=${e.zh}`
}

export function countAffixes(): {
  prefixes: number
  suffixes: number
  roots: number
  total: number
} {
  return {
    prefixes: PREFIX_MEANINGS.length,
    suffixes: SUFFIX_MEANINGS.length,
    roots: ROOT_MEANINGS.length,
    total: allForLookup.length + ROOT_MEANINGS.length,
  }
}
