import type { Gender, VocabWord } from '../data/vocabulary'
import { vocabulary } from '../data/vocabulary'
import { lookupPrefix, lookupSuffix } from '../data/affixes'

export type PluralPattern =
  | '-e'
  | '-er'
  | '-n/-en'
  | '-s'
  | '母音變音 + -e'
  | '母音變音 + -er'
  | '無變化'
  | '其他／不規則'
  | '無複數／少用'

export type VerbClass = '弱變化（規則）' | '強變化（不規則）' | '混合變化' | '情態／助動詞'

export interface VerbForms {
  infinitive: string
  class: VerbClass
  present: {
    ich: string
    du: string
    er: string
    wir: string
    ihr: string
    sie: string
  }
  preterite: string
  participle: string
  auxiliary: 'haben' | 'sein'
  separable?: string
  usage: string
}

export interface WordParts {
  prefixes: string[]
  root: string
  suffixes: string[]
  note?: string
}

export interface RelatedWord {
  word: string
  article?: Gender
  relation: string
  translation: string
}

export interface EnrichedWord extends VocabWord {
  wordType: '名詞' | '動詞' | '形容詞' | '其他'
  pluralPattern?: PluralPattern
  pluralHint?: string
  parts?: WordParts
  verb?: VerbForms
  related: RelatedWord[]
  memoryTips: string[]
}

const PREFIXES = [
  'auseinander',
  'entgegen',
  'gegenüber',
  'zusammen',
  'herunter',
  'herunter',
  'hinein',
  'heraus',
  'hinauf',
  'hinunter',
  'zurück',
  'vorbei',
  'weiter',
  'wieder',
  'entlang',
  'herum',
  'durch',
  'über',
  'unter',
  'hinter',
  'zwischen',
  'ent',
  'emp',
  'miss',
  'zer',
  'ver',
  'be',
  'er',
  'ge',
  'un',
  'ur',
  'aus',
  'auf',
  'ein',
  'an',
  'ab',
  'zu',
  'um',
  'mit',
  'nach',
  'vor',
  'weg',
  'los',
  'fest',
  'teil',
  'statt',
]

const SUFFIXES = [
  'schaft',
  'igkeit',
  'heit',
  'keit',
  'ung',
  'tion',
  'ismus',
  'chen',
  'lein',
  'chen',
  'bar',
  'lich',
  'isch',
  'ig',
  'sam',
  'haft',
  'los',
  'voll',
  'tum',
  'nis',
  'sal',
  'er',
  'in',
  'e',
]

/** Strong / irregular / modal verb stems (present du/er, preterite, participle, aux) */
const STRONG: Record<
  string,
  {
    du?: string
    er?: string
    pret: string
    part: string
    aux?: 'haben' | 'sein'
    cls?: VerbClass
  }
> = {
  sein: { du: 'bist', er: 'ist', pret: 'war', part: 'gewesen', aux: 'sein', cls: '情態／助動詞' },
  haben: { du: 'hast', er: 'hat', pret: 'hatte', part: 'gehabt', cls: '情態／助動詞' },
  werden: { du: 'wirst', er: 'wird', pret: 'wurde', part: 'geworden', aux: 'sein', cls: '情態／助動詞' },
  können: { du: 'kannst', er: 'kann', pret: 'konnte', part: 'gekonnt', cls: '情態／助動詞' },
  müssen: { du: 'musst', er: 'muss', pret: 'musste', part: 'gemusst', cls: '情態／助動詞' },
  wollen: { du: 'willst', er: 'will', pret: 'wollte', part: 'gewollt', cls: '情態／助動詞' },
  sollen: { du: 'sollst', er: 'soll', pret: 'sollte', part: 'gesollt', cls: '情態／助動詞' },
  dürfen: { du: 'darfst', er: 'darf', pret: 'durfte', part: 'gedurft', cls: '情態／助動詞' },
  mögen: { du: 'magst', er: 'mag', pret: 'mochte', part: 'gemocht', cls: '情態／助動詞' },
  gehen: { pret: 'ging', part: 'gegangen', aux: 'sein' },
  kommen: { pret: 'kam', part: 'gekommen', aux: 'sein' },
  fahren: { du: 'fährst', er: 'fährt', pret: 'fuhr', part: 'gefahren', aux: 'sein' },
  laufen: { du: 'läufst', er: 'läuft', pret: 'lief', part: 'gelaufen', aux: 'sein' },
  fliegen: { pret: 'flog', part: 'geflogen', aux: 'sein' },
  schwimmen: { pret: 'schwamm', part: 'geschwommen', aux: 'sein' },
  bleiben: { pret: 'blieb', part: 'geblieben', aux: 'sein' },
  stehen: { pret: 'stand', part: 'gestanden' },
  sitzen: { pret: 'saß', part: 'gesessen' },
  liegen: { pret: 'lag', part: 'gelegen' },
  essen: { du: 'isst', er: 'isst', pret: 'aß', part: 'gegessen' },
  geben: { du: 'gibst', er: 'gibt', pret: 'gab', part: 'gegeben' },
  nehmen: { du: 'nimmst', er: 'nimmt', pret: 'nahm', part: 'genommen' },
  sprechen: { du: 'sprichst', er: 'spricht', pret: 'sprach', part: 'gesprochen' },
  sehen: { du: 'siehst', er: 'sieht', pret: 'sah', part: 'gesehen' },
  lesen: { du: 'liest', er: 'liest', pret: 'las', part: 'gelesen' },
  schreiben: { pret: 'schrieb', part: 'geschrieben' },
  schlafen: { du: 'schläfst', er: 'schläft', pret: 'schlief', part: 'geschlafen' },
  tragen: { du: 'trägst', er: 'trägt', pret: 'trug', part: 'getragen' },
  waschen: { du: 'wäschst', er: 'wäscht', pret: 'wusch', part: 'gewaschen' },
  fallen: { du: 'fällst', er: 'fällt', pret: 'fiel', part: 'gefallen', aux: 'sein' },
  helfen: { du: 'hilfst', er: 'hilft', pret: 'half', part: 'geholfen' },
  treffen: { du: 'triffst', er: 'trifft', pret: 'traf', part: 'getroffen' },
  werfen: { du: 'wirfst', er: 'wirft', pret: 'warf', part: 'geworfen' },
  finden: { pret: 'fand', part: 'gefunden' },
  singen: { pret: 'sang', part: 'gesungen' },
  trinken: { pret: 'trank', part: 'getrunken' },
  beginnen: { pret: 'begann', part: 'begonnen' },
  gewinnen: { pret: 'gewann', part: 'gewonnen' },
  verlieren: { pret: 'verlor', part: 'verloren' },
  vergessen: { du: 'vergisst', er: 'vergisst', pret: 'vergaß', part: 'vergessen' },
  verstehen: { pret: 'verstand', part: 'verstanden' },
  erscheinen: { pret: 'erschien', part: 'erschienen', aux: 'sein' },
  entscheiden: { pret: 'entschied', part: 'entschieden' },
  beschreiben: { pret: 'beschrieb', part: 'beschrieben' },
  empfehlen: { du: 'empfiehlst', er: 'empfiehlt', pret: 'empfahl', part: 'empfohlen' },
  steigen: { pret: 'stieg', part: 'gestiegen', aux: 'sein' },
  rufen: { pret: 'rief', part: 'gerufen' },
  rufen_a: { pret: 'rief', part: 'gerufen' },
  schließen: { pret: 'schloss', part: 'geschlossen' },
  schießen: { pret: 'schoss', part: 'geschossen' },
  fliehen: { pret: 'floh', part: 'geflohen', aux: 'sein' },
  fließen: { pret: 'floss', part: 'geflossen', aux: 'sein' },
  ziehen: { pret: 'zog', part: 'gezogen' },
  bieten: { pret: 'bot', part: 'geboten' },
  lügen: { pret: 'log', part: 'gelogen' },
  biegen: { pret: 'bog', part: 'gebogen' },
  heben: { pret: 'hob', part: 'gehoben' },
  halten: { du: 'hältst', er: 'hält', pret: 'hielt', part: 'gehalten' },
  lassen: { du: 'lässt', er: 'lässt', pret: 'ließ', part: 'gelassen' },
  laden: { du: 'lädst', er: 'lädt', pret: 'lud', part: 'geladen' },
  wachsen: { du: 'wächst', er: 'wächst', pret: 'wuchs', part: 'gewachsen', aux: 'sein' },
  wissen: { du: 'weißt', er: 'weiß', pret: 'wusste', part: 'gewusst', cls: '混合變化' },
  bringen: { pret: 'brachte', part: 'gebracht', cls: '混合變化' },
  denken: { pret: 'dachte', part: 'gedacht', cls: '混合變化' },
  kennen: { pret: 'kannte', part: 'gekannt', cls: '混合變化' },
  nennen: { pret: 'nannte', part: 'genannt', cls: '混合變化' },
  rennen: { pret: 'rannte', part: 'gerannt', aux: 'sein', cls: '混合變化' },
  senden: { pret: 'sandte', part: 'gesandt', cls: '混合變化' },
  wenden: { pret: 'wandte', part: 'gewandt', cls: '混合變化' },
  brennen: { pret: 'brannte', part: 'gebrannt', cls: '混合變化' },
  tun: { pret: 'tat', part: 'getan' },
  sterben: { du: 'stirbst', er: 'stirbt', pret: 'starb', part: 'gestorben', aux: 'sein' },
  gelten: { du: 'giltst', er: 'gilt', pret: 'galt', part: 'gegolten' },
  gelten2: { pret: 'galt', part: 'gegolten' },
}

const SEPARABLE = [
  'auf',
  'an',
  'ab',
  'aus',
  'ein',
  'mit',
  'nach',
  'vor',
  'zu',
  'zurück',
  'weg',
  'los',
  'fest',
  'teil',
  'statt',
  'weiter',
  'wieder',
  'heran',
  'herauf',
  'herunter',
  'hinein',
  'heraus',
]

/** Hand-curated word families (lemma → related) */
const FAMILIES: Record<string, RelatedWord[]> = {
  arbeiten: [
    { word: 'Arbeit', article: 'die', relation: '同源名詞', translation: '工作' },
    { word: 'Arbeiter', article: 'der', relation: '行為者', translation: '工人' },
    { word: 'Arbeitsplatz', article: 'der', relation: '複合詞', translation: '工作崗位' },
  ],
  sprechen: [
    { word: 'Sprache', article: 'die', relation: '同源名詞', translation: '語言' },
    { word: 'Gespräch', article: 'das', relation: '相關名詞', translation: '談話' },
    { word: 'Sprecher', article: 'der', relation: '行為者', translation: '發言人' },
  ],
  lernen: [
    { word: 'Lernen', article: 'das', relation: '動名詞', translation: '學習' },
    { word: 'Schüler', article: 'der', relation: '相關', translation: '學生' },
    { word: 'Lehrer', article: 'der', relation: '相關', translation: '老師' },
  ],
  wohnen: [
    { word: 'Wohnung', article: 'die', relation: '同源名詞', translation: '公寓' },
    { word: 'Bewohner', article: 'der', relation: '行為者', translation: '居民' },
    { word: 'Wohnzimmer', article: 'das', relation: '複合詞', translation: '客廳' },
  ],
  fahren: [
    { word: 'Fahrt', article: 'die', relation: '同源名詞', translation: '行程' },
    { word: 'Fahrer', article: 'der', relation: '行為者', translation: '駕駛' },
    { word: 'Fahrrad', article: 'das', relation: '複合詞', translation: '腳踏車' },
    { word: 'Fahrkarte', article: 'die', relation: '複合詞', translation: '車票' },
  ],
  fliegen: [
    { word: 'Flug', article: 'der', relation: '同源名詞', translation: '航班' },
    { word: 'Flughafen', article: 'der', relation: '複合詞', translation: '機場' },
    { word: 'Flugzeug', article: 'das', relation: '複合詞', translation: '飛機' },
  ],
  schreiben: [
    { word: 'Schrift', article: 'die', relation: '同源名詞', translation: '文字' },
    { word: 'Schreiben', article: 'das', relation: '動名詞', translation: '書寫／信件' },
    { word: 'Schreiber', article: 'der', relation: '行為者', translation: '書寫者' },
  ],
  lesen: [
    { word: 'Leser', article: 'der', relation: '行為者', translation: '讀者' },
    { word: 'Lesung', article: 'die', relation: '活動名詞', translation: '朗讀會' },
  ],
  sehen: [
    { word: 'Sicht', article: 'die', relation: '同源名詞', translation: '視線／能見度' },
    { word: 'Sehenswürdigkeit', article: 'die', relation: '複合詞', translation: '景點' },
  ],
  hören: [
    { word: 'Gehör', article: 'das', relation: '同源名詞', translation: '聽覺' },
    { word: 'Zuhörer', article: 'der', relation: '行為者', translation: '聽眾' },
  ],
  kaufen: [
    { word: 'Kauf', article: 'der', relation: '同源名詞', translation: '購買' },
    { word: 'Käufer', article: 'der', relation: '行為者', translation: '買家' },
    { word: 'Kaufhaus', article: 'das', relation: '複合詞', translation: '百貨公司' },
  ],
  verkaufen: [
    { word: 'Verkauf', article: 'der', relation: '同源名詞', translation: '銷售' },
    { word: 'Verkäufer', article: 'der', relation: '行為者', translation: '店員' },
  ],
  kochen: [
    { word: 'Koch', article: 'der', relation: '行為者', translation: '廚師' },
    { word: 'Küche', article: 'die', relation: '相關名詞', translation: '廚房' },
  ],
  spielen: [
    { word: 'Spiel', article: 'das', relation: '同源名詞', translation: '遊戲／比賽' },
    { word: 'Spieler', article: 'der', relation: '行為者', translation: '球員' },
  ],
  tanzen: [
    { word: 'Tanz', article: 'der', relation: '同源名詞', translation: '舞蹈' },
    { word: 'Tänzer', article: 'der', relation: '行為者', translation: '舞者' },
  ],
  singen: [
    { word: 'Song', article: 'der', relation: '相關', translation: '歌曲（外來）' },
    { word: 'Lied', article: 'das', relation: '相關名詞', translation: '歌曲' },
    { word: 'Sänger', article: 'der', relation: '行為者', translation: '歌手' },
  ],
  helfen: [
    { word: 'Hilfe', article: 'die', relation: '同源名詞', translation: '幫助' },
    { word: 'Helfer', article: 'der', relation: '行為者', translation: '幫手' },
  ],
  denken: [
    { word: 'Gedanke', article: 'der', relation: '同源名詞', translation: '想法' },
    { word: 'Denken', article: 'das', relation: '動名詞', translation: '思考' },
  ],
  wissen: [
    { word: 'Wissen', article: 'das', relation: '同源名詞', translation: '知識' },
    { word: 'Wissenschaft', article: 'die', relation: '衍生', translation: '科學' },
  ],
  fühlen: [
    { word: 'Gefühl', article: 'das', relation: '同源名詞', translation: '感覺' },
  ],
  leben: [
    { word: 'Leben', article: 'das', relation: '同源名詞', translation: '生命／生活' },
    { word: 'Lebewesen', article: 'das', relation: '複合詞', translation: '生物' },
  ],
  sterben: [
    { word: 'Tod', article: 'der', relation: '相關名詞', translation: '死亡' },
    { word: 'tot', relation: '相關形容詞', translation: '死的' },
  ],
  öffnen: [
    { word: 'Öffnung', article: 'die', relation: '同源名詞', translation: '開口' },
    { word: 'offen', relation: '相關形容詞', translation: '開著的' },
  ],
  schließen: [
    { word: 'Schluss', article: 'der', relation: '同源名詞', translation: '結束' },
    { word: 'geschlossen', relation: '分詞形容詞', translation: '關閉的' },
  ],
  beginnen: [
    { word: 'Beginn', article: 'der', relation: '同源名詞', translation: '開始' },
    { word: 'Anfang', article: 'der', relation: '同義名詞', translation: '開頭' },
  ],
  enden: [
    { word: 'Ende', article: 'das', relation: '同源名詞', translation: '結束' },
  ],
  studieren: [
    { word: 'Studium', article: 'das', relation: '同源名詞', translation: '大學學業' },
    { word: 'Student', article: 'der', relation: '行為者', translation: '大學生' },
    { word: 'Studentin', article: 'die', relation: '行為者（女）', translation: '女大學生' },
  ],
  unterrichten: [
    { word: 'Unterricht', article: 'der', relation: '同源名詞', translation: '上課' },
  ],
  prüfen: [
    { word: 'Prüfung', article: 'die', relation: '同源名詞', translation: '考試' },
  ],
  reisen: [
    { word: 'Reise', article: 'die', relation: '同源名詞', translation: '旅行' },
    { word: 'Reisende', article: 'der', relation: '行為者', translation: '旅客' },
  ],
  besuchen: [
    { word: 'Besuch', article: 'der', relation: '同源名詞', translation: '拜訪' },
    { word: 'Besucher', article: 'der', relation: '行為者', translation: '訪客' },
  ],
  einladen: [
    { word: 'Einladung', article: 'die', relation: '同源名詞', translation: '邀請' },
  ],
  bestellen: [
    { word: 'Bestellung', article: 'die', relation: '同源名詞', translation: '訂單' },
  ],
  bezahlen: [
    { word: 'Bezahlung', article: 'die', relation: '同源名詞', translation: '付款' },
    { word: 'Zahlung', article: 'die', relation: '相關', translation: '支付' },
  ],
  erklären: [
    { word: 'Erklärung', article: 'die', relation: '同源名詞', translation: '說明' },
  ],
  erzählen: [
    { word: 'Erzählung', article: 'die', relation: '同源名詞', translation: '敘述／故事' },
  ],
  entscheiden: [
    { word: 'Entscheidung', article: 'die', relation: '同源名詞', translation: '決定' },
  ],
  entwickeln: [
    { word: 'Entwicklung', article: 'die', relation: '同源名詞', translation: '發展' },
  ],
  verbessern: [
    { word: 'Verbesserung', article: 'die', relation: '同源名詞', translation: '改善' },
  ],
  verändern: [
    { word: 'Veränderung', article: 'die', relation: '同源名詞', translation: '改變' },
  ],
  informieren: [
    { word: 'Information', article: 'die', relation: '同源名詞', translation: '資訊' },
  ],
  organisieren: [
    { word: 'Organisation', article: 'die', relation: '同源名詞', translation: '組織' },
  ],
  fotografieren: [
    { word: 'Foto', article: 'das', relation: '相關名詞', translation: '照片' },
    { word: 'Fotografie', article: 'die', relation: '同源名詞', translation: '攝影' },
  ],
  Haus: [
    { word: 'Haushalt', article: 'der', relation: '複合詞', translation: '家務／家庭' },
    { word: 'Zuhause', article: 'das', relation: '相關', translation: '家' },
    { word: 'häuslich', relation: '衍生形容詞', translation: '居家的' },
  ],
  Schule: [
    { word: 'Schüler', article: 'der', relation: '相關', translation: '學生' },
    { word: 'Lehrer', article: 'der', relation: '相關', translation: '老師' },
    { word: 'schulisch', relation: '衍生形容詞', translation: '學校的' },
  ],
  Freund: [
    { word: 'Freundin', article: 'die', relation: '陰性對應', translation: '女性朋友' },
    { word: 'Freundschaft', article: 'die', relation: '抽象名詞', translation: '友誼' },
    { word: 'freundlich', relation: '衍生形容詞', translation: '友善的' },
  ],
  Kind: [
    { word: 'Kinder', article: null, relation: '複數', translation: '小孩們' },
    { word: 'Kindheit', article: 'die', relation: '抽象名詞', translation: '童年' },
    { word: 'kindlich', relation: '衍生形容詞', translation: '孩子氣的' },
  ],
  Arbeit: [
    { word: 'arbeiten', relation: '同源動詞', translation: '工作' },
    { word: 'Arbeiter', article: 'der', relation: '行為者', translation: '工人' },
    { word: 'arbeitslos', relation: '衍生形容詞', translation: '失業的' },
  ],
  Sprache: [
    { word: 'sprechen', relation: '同源動詞', translation: '說' },
    { word: 'sprachlich', relation: '衍生形容詞', translation: '語言的' },
  ],
  Reise: [
    { word: 'reisen', relation: '同源動詞', translation: '旅行' },
    { word: 'Reiseführer', article: 'der', relation: '複合詞', translation: '導遊／旅遊書' },
  ],
  Stadt: [
    { word: 'städtisch', relation: '衍生形容詞', translation: '城市的' },
    { word: 'Hauptstadt', article: 'die', relation: '複合詞', translation: '首都' },
  ],
  Land: [
    { word: 'ländlich', relation: '衍生形容詞', translation: '鄉村的' },
    { word: 'Landschaft', article: 'die', relation: '衍生', translation: '風景' },
  ],
  Buch: [
    { word: 'Bibliothek', article: 'die', relation: '相關', translation: '圖書館' },
    { word: 'Buchhandlung', article: 'die', relation: '複合詞', translation: '書店' },
  ],
  Wasser: [
    { word: 'wässrig', relation: '衍生形容詞', translation: '含水的' },
    { word: 'Wasserglas', article: 'das', relation: '複合詞', translation: '水杯' },
  ],
  Essen: [
    { word: 'essen', relation: '同源動詞', translation: '吃' },
    { word: 'Esszimmer', article: 'das', relation: '複合詞', translation: '餐廳' },
  ],
  schön: [
    { word: 'Schönheit', article: 'die', relation: '抽象名詞', translation: '美麗' },
    { word: 'verschönern', relation: '衍生動詞', translation: '美化' },
  ],
  groß: [
    { word: 'Größe', article: 'die', relation: '抽象名詞', translation: '大小／尺寸' },
    { word: 'Großstadt', article: 'die', relation: '複合詞', translation: '大城市' },
  ],
  klein: [
    { word: 'Kleinigkeit', article: 'die', relation: '抽象名詞', translation: '小事' },
  ],
  gut: [
    { word: 'Gute', article: 'das', relation: '名詞化', translation: '好處' },
    { word: 'Güte', article: 'die', relation: '抽象名詞', translation: '善意' },
  ],
  krank: [
    { word: 'Krankheit', article: 'die', relation: '抽象名詞', translation: '疾病' },
    { word: 'Krankenhaus', article: 'das', relation: '複合詞', translation: '醫院' },
  ],
  gesund: [
    { word: 'Gesundheit', article: 'die', relation: '抽象名詞', translation: '健康' },
  ],
  frei: [
    { word: 'Freiheit', article: 'die', relation: '抽象名詞', translation: '自由' },
  ],
  möglich: [
    { word: 'Möglichkeit', article: 'die', relation: '抽象名詞', translation: '可能性' },
  ],
  wichtig: [
    { word: 'Wichtigkeit', article: 'die', relation: '抽象名詞', translation: '重要性' },
  ],
  sicher: [
    { word: 'Sicherheit', article: 'die', relation: '抽象名詞', translation: '安全' },
  ],
  freundlich: [
    { word: 'Freundlichkeit', article: 'die', relation: '抽象名詞', translation: '友善' },
    { word: 'Freund', article: 'der', relation: '字根名詞', translation: '朋友' },
  ],
}

function stripPrefix(word: string): { prefix?: string; rest: string } {
  const lower = word.toLowerCase()
  // handle "sich X"
  const bare = lower.replace(/^sich\s+/, '')
  for (const p of PREFIXES) {
    if (bare.startsWith(p) && bare.length > p.length + 2) {
      return { prefix: p, rest: bare.slice(p.length) }
    }
  }
  return { rest: bare }
}

function analyzeParts(word: string): WordParts {
  const original = word.replace(/^sich\s+/, '')
  const prefixes: string[] = []
  let rest = original.toLowerCase()

  // collect separable / inseparable prefixes
  let guard = 0
  while (guard++ < 3) {
    const { prefix, rest: r } = stripPrefix(rest)
    if (!prefix) break
    prefixes.push(prefix)
    rest = r
  }

  const suffixes: string[] = []
  let core = rest
  for (const s of SUFFIXES) {
    if (core.endsWith(s) && core.length > s.length + 1) {
      suffixes.unshift(s)
      core = core.slice(0, -s.length)
      break // one productive suffix is enough for display
    }
  }

  const noteParts: string[] = []
  if (prefixes.length) {
    const withMeaning = prefixes.map((p) => {
      const m = lookupPrefix(p)
      return m ? `${p}-（${m.zh}）` : `${p}-`
    })
    noteParts.push(`字首 ${withMeaning.join(' + ')}`)
  }
  if (suffixes.length) {
    const withMeaning = suffixes.map((s) => {
      const m = lookupSuffix(s)
      return m ? `-${s}（${m.zh}）` : `-${s}`
    })
    noteParts.push(`字尾 ${withMeaning.join(' + ')}`)
  }

  return {
    prefixes,
    root: core || rest,
    suffixes,
    note: noteParts.length
      ? `${noteParts.join('，')}；字根約為「${core || rest}」`
      : undefined,
  }
}

function detectPluralPattern(
  singular: string,
  plural: string | undefined,
): { pattern?: PluralPattern; hint?: string } {
  if (!plural) {
    return { pattern: '無複數／少用', hint: '此詞通常不強調複數，或複數較少見。' }
  }
  if (plural === singular) {
    return {
      pattern: '無變化',
      hint: `單複數同形：${singular} → ${plural}（像英文部分詞的零複數）。`,
    }
  }

  const s = singular
  const p = plural

  // umlaut detection helper
  const hasUmlaut =
    (/[aou]/i.test(s) && /[äöü]/.test(p)) ||
    (s.includes('a') && p.includes('ä')) ||
    (s.includes('o') && p.includes('ö')) ||
    (s.includes('u') && p.includes('ü'))

  if (p === s + 's' || p === s + 's') {
    return {
      pattern: '-s',
      hint: `加 -s（多為外來語／縮寫，類似英文一般 +s）：${s} → ${p}`,
    }
  }
  if (p.endsWith('er') && (p === s + 'er' || hasUmlaut)) {
    return {
      pattern: hasUmlaut ? '母音變音 + -er' : '-er',
      hint: hasUmlaut
        ? `變音 + -er（經典不規則，如 Buch→Bücher）：${s} → ${p}`
        : `加 -er：${s} → ${p}`,
    }
  }
  if (p === s + 'e' || (hasUmlaut && p.endsWith('e') && p.length === s.length + 1)) {
    return {
      pattern: hasUmlaut ? '母音變音 + -e' : '-e',
      hint: hasUmlaut
        ? `變音 + -e（多見於陽性名詞）：${s} → ${p}`
        : `加 -e：${s} → ${p}`,
    }
  }
  if (p.endsWith('en') || p.endsWith('n')) {
    // -n / -en
    if (p === s + 'n' || p === s + 'en' || p === s.slice(0, -1) + 'en') {
      return {
        pattern: '-n/-en',
        hint: `加 -n／-en（陰性與弱變化常見，類似英文 +es 的「加尾」感）：${s} → ${p}`,
      }
    }
    return {
      pattern: '-n/-en',
      hint: `複數結尾為 -n／-en：${s} → ${p}`,
    }
  }
  if (p.endsWith('s')) {
    return {
      pattern: '-s',
      hint: `加 -s：${s} → ${p}`,
    }
  }
  return {
    pattern: '其他／不規則',
    hint: `不規則複數，建議整組記：${s} → ${p}`,
  }
}

function weakConjugate(inf: string): VerbForms['present'] {
  const stem = inf.endsWith('en')
    ? inf.slice(0, -2)
    : inf.endsWith('n')
      ? inf.slice(0, -1)
      : inf
  // -t/-d/-chn/-fn/-gn stems need -e-
  const needsE = /[td]$/.test(stem) || /[a-zäöüß][mn]$/.test(stem)
  const e = needsE ? 'e' : ''
  return {
    ich: stem + 'e',
    du: stem + e + 'st',
    er: stem + e + 't',
    wir: inf,
    ihr: stem + e + 't',
    sie: inf,
  }
}

function buildVerb(infRaw: string): VerbForms | undefined {
  const inf = infRaw.replace(/^sich\s+/, '').trim()
  if (!inf || inf.includes(' ')) {
    // multi-word like "weh tun" — skip structured table
    if (inf.includes(' ')) return undefined
  }

  let separable: string | undefined
  let base = inf
  for (const sep of SEPARABLE) {
    if (inf.startsWith(sep) && inf.length > sep.length + 2 && !STRONG[inf]) {
      // only treat as separable if remaining looks like verb
      const rest = inf.slice(sep.length)
      if (rest.endsWith('en') || rest.endsWith('n')) {
        separable = sep
        base = rest
        break
      }
    }
  }

  const key = separable ? base : inf
  const strong = STRONG[inf] || STRONG[key] || STRONG[base]

  const present = weakConjugate(separable ? base : inf)
  if (strong?.du) present.du = strong.du
  if (strong?.er) present.er = strong.er

  // separable present: ich stehe auf
  if (separable) {
    present.ich = `${present.ich} ${separable}`
    present.du = `${present.du} ${separable}`
    present.er = `${present.er} ${separable}`
    present.wir = `${inf}`
    present.ihr = `${present.ihr} ${separable}`
    present.sie = `${inf}`
  }

  let participle: string
  let preterite: string
  let cls: VerbClass = '弱變化（規則）'
  let aux: 'haben' | 'sein' = 'haben'

  if (strong) {
    cls = strong.cls ?? '強變化（不規則）'
    preterite = strong.pret
    participle = strong.part
    aux = strong.aux ?? 'haben'
  } else if (separable) {
    // ge- between prefix and stem: aufstehen → aufgestanden is strong; weak: anrufen → angerufen
    const stem = base.endsWith('en') ? base.slice(0, -2) : base.slice(0, -1)
    const weakPart = /[td]$/.test(stem) ? `${stem}et` : `${stem}t`
    participle = `${separable}ge${weakPart}`
    preterite = /[td]$/.test(stem) ? `${stem}ete` : `${stem}te`
    // for separable weak: ich rief an is strong for anrufen... keep simple
    preterite = `${preterite}` // simple weak pret without separable shown in table note
  } else if (
    inf.startsWith('be') ||
    inf.startsWith('ver') ||
    inf.startsWith('er') ||
    inf.startsWith('ent') ||
    inf.startsWith('zer') ||
    inf.startsWith('emp') ||
    inf.startsWith('miss') ||
    inf.startsWith('ge')
  ) {
    // inseparable: no ge- in participle
    const stem = inf.endsWith('en') ? inf.slice(0, -2) : inf.slice(0, -1)
    const weakPart = /[td]$/.test(stem) ? `${stem}et` : `${stem}t`
    participle = weakPart.startsWith('be') || weakPart.startsWith('ver')
      ? weakPart
      : weakPart
    // fix: be- stem already includes prefix
    participle = /[td]$/.test(stem) ? `${stem}et` : `${stem}t`
    preterite = /[td]$/.test(stem) ? `${stem}ete` : `${stem}te`
  } else {
    const stem = inf.endsWith('en') ? inf.slice(0, -2) : inf.slice(0, -1)
    const weakPart = /[td]$/.test(stem) ? `ge${stem}et` : `ge${stem}t`
    participle = weakPart
    preterite = /[td]$/.test(stem) ? `${stem}ete` : `${stem}te`
  }

  if (strong) {
    // ok
  }

  const usageBits: string[] = []
  if (cls === '弱變化（規則）') {
    usageBits.push('規則動詞：字幹穩定，過去式多加 -te，過去分詞 ge-…-t。')
  } else if (cls === '強變化（不規則）') {
    usageBits.push('強變化動詞：字幹母音會變，需整組背（現在／過去／分詞）。')
  } else if (cls === '混合變化') {
    usageBits.push('混合變化：有點像強變化的母音變化，但過去式仍帶 -te。')
  } else {
    usageBits.push('情態／助動詞：常接另一個動詞不定式，語序特別。')
  }
  if (separable) {
    usageBits.push(
      `可分動詞：字首「${separable}」在現在時句末分開（Ich ${present.ich}）。`,
    )
  }
  if (
    inf.startsWith('be') ||
    inf.startsWith('ver') ||
    inf.startsWith('er') ||
    inf.startsWith('ent')
  ) {
    usageBits.push('不可分字首（be-/ver-/er-/ent-…）：過去分詞通常不加 ge-。')
  }
  usageBits.push(`完成式助動詞多用 ${aux}（${aux} + ${participle}）。`)

  return {
    infinitive: infRaw,
    class: cls,
    present,
    preterite: separable && !strong ? `${preterite} (${separable})` : preterite,
    participle,
    auxiliary: aux,
    separable,
    usage: usageBits.join(' '),
  }
}

function simpleWordType(w: VocabWord): EnrichedWord['wordType'] {
  if (w.category === '動詞') return '動詞'
  if (w.category === '形容詞') return '形容詞'
  if (w.article) return '名詞'
  return '其他'
}

function memoryTips(w: VocabWord, type: EnrichedWord['wordType'], pluralPattern?: PluralPattern, parts?: WordParts, verb?: VerbForms): string[] {
  const tips: string[] = []
  if (type === '名詞' && w.article) {
    tips.push(`名詞必記冠詞：用顏色記「${w.article} ${w.word}」。`)
    if (pluralPattern) {
      tips.push(`複數口訣：歸類為「${pluralPattern}」，對照英文的 +s / +es / 不規則整組背。`)
    }
    if (w.plural) {
      tips.push(`大聲連念：${w.article} ${w.word} — die ${w.plural}`)
    }
  }
  if (type === '動詞' && verb) {
    tips.push(`動詞先記三態：${verb.infinitive} / ${verb.preterite} / ${verb.participle}`)
    tips.push(`現在時先抓 ich / du / er：${verb.present.ich} · ${verb.present.du} · ${verb.present.er}`)
    if (verb.separable) {
      tips.push(`可分動詞想像「字首飛到句尾」：${verb.separable}- 分開。`)
    }
  }
  if (type === '形容詞') {
    tips.push('形容詞可記反義對（大／小、好／壞），再配一個短例句。')
  }
  if (parts?.prefixes.length || parts?.suffixes.length) {
    tips.push(
      `拆字記：${[...parts.prefixes.map((p) => p + '-'), parts.root, ...parts.suffixes.map((s) => '-' + s)].join(' + ')}`,
    )
  }
  tips.push('用例句情境記：把中文意思套回例句再說一次德文。')
  return tips
}

function relatedFor(w: VocabWord): RelatedWord[] {
  const direct = FAMILIES[w.word] || FAMILIES[w.word.replace(/^sich\s+/, '')] || []
  const fromVocab: RelatedWord[] = []

  // same root start (first 4 letters) limited
  const root = analyzeParts(w.word).root
  if (root.length >= 4) {
    for (const other of vocabulary) {
      if (other.id === w.id) continue
      if (analyzeParts(other.word).root === root) {
        fromVocab.push({
          word: other.word,
          article: other.article,
          relation: '同字根',
          translation: other.translation,
        })
      }
      if (fromVocab.length >= 4) break
    }
  }

  const merged = [...direct]
  for (const r of fromVocab) {
    if (!merged.some((m) => m.word === r.word)) merged.push(r)
  }
  return merged.slice(0, 8)
}

const cache = new Map<string, EnrichedWord>()

export function enrich(w: VocabWord): EnrichedWord {
  const hit = cache.get(w.id)
  if (hit) return hit

  const wordType = simpleWordType(w)
  const parts = analyzeParts(w.word)
  const { pattern, hint } =
    wordType === '名詞' ? detectPluralPattern(w.word, w.plural) : {}
  const verb = wordType === '動詞' ? buildVerb(w.word) : undefined
  const related = relatedFor(w)
  const tips = memoryTips(w, wordType, pattern, parts, verb)

  const enriched: EnrichedWord = {
    ...w,
    wordType,
    pluralPattern: pattern,
    pluralHint: hint,
    parts,
    verb,
    related,
    memoryTips: tips,
  }
  cache.set(w.id, enriched)
  return enriched
}

export const PLURAL_PATTERN_GUIDE: { pattern: PluralPattern; likeEnglish: string; example: string }[] = [
  { pattern: '-e', likeEnglish: '類似加結尾（不全等 +s）', example: 'Tag → Tage' },
  { pattern: '-er', likeEnglish: '不規則族，整組背', example: 'Kind → Kinder' },
  { pattern: '-n/-en', likeEnglish: '有點像 +es（加尾音）', example: 'Blume → Blumen' },
  { pattern: '-s', likeEnglish: '最像英文 +s', example: 'Hotel → Hotels' },
  { pattern: '母音變音 + -e', likeEnglish: '像 man→men 的變音感', example: 'Zug → Züge' },
  { pattern: '母音變音 + -er', likeEnglish: '變音＋不規則尾', example: 'Buch → Bücher' },
  { pattern: '無變化', likeEnglish: '像 sheep→sheep', example: 'Lehrer → Lehrer' },
  { pattern: '其他／不規則', likeEnglish: '像 child→children', example: '看個別單字' },
]
