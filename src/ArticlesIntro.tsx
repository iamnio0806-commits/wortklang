import { SpeakPair } from './lib/SpeakControls'
import { genderClass } from './lib/richText'

type Article = 'der' | 'die' | 'das'

const INTRO_WORDS: {
  article: Article
  word: string
  zh: string
  tip: string
}[] = [
  { article: 'der', word: 'Mann', zh: '男人', tip: '人／職位很多是 der' },
  { article: 'der', word: 'Vater', zh: '爸爸', tip: '家庭男性成員常是 der' },
  { article: 'der', word: 'Tisch', zh: '桌子', tip: '常見日用品，陽性' },
  { article: 'der', word: 'Stuhl', zh: '椅子', tip: '跟 Tisch 一起記' },
  { article: 'der', word: 'Tag', zh: '日子', tip: '時間詞：der Tag' },
  { article: 'der', word: 'Apfel', zh: '蘋果', tip: '很多水果是 der' },
  { article: 'die', word: 'Frau', zh: '女人', tip: '陰性對照 der Mann' },
  { article: 'die', word: 'Mutter', zh: '媽媽', tip: '家庭女性成員常是 die' },
  { article: 'die', word: 'Stadt', zh: '城市', tip: '地名類常是 die' },
  { article: 'die', word: 'Schule', zh: '學校', tip: '-e 結尾常是 die' },
  { article: 'die', word: 'Tür', zh: '門', tip: '家中常見陰性詞' },
  { article: 'die', word: 'Milch', zh: '牛奶', tip: '飲品：die Milch' },
  { article: 'das', word: 'Kind', zh: '孩子', tip: '中性經典例' },
  { article: 'das', word: 'Haus', zh: '房子', tip: '空間／建築常是 das' },
  { article: 'das', word: 'Buch', zh: '書', tip: '學習必備：das Buch' },
  { article: 'das', word: 'Auto', zh: '汽車', tip: '外來詞常是 das' },
  { article: 'das', word: 'Wasser', zh: '水', tip: '物質名詞常是 das' },
  { article: 'das', word: 'Brot', zh: '麵包', tip: '飲食：das Brot' },
]

const CASE_CARDS = [
  {
    num: '一格',
    de: 'Nominativ',
    zh: '主格',
    use: '主語：誰／什麼在做？',
  },
  {
    num: '四格',
    de: 'Akkusativ',
    zh: '直接受詞',
    use: '看到／需要／買誰／什麼？陽性會變。',
  },
  {
    num: '三格',
    de: 'Dativ',
    zh: '間接受詞',
    use: '給誰／幫誰？跟 mit、zu、von…',
  },
  {
    num: '二格',
    de: 'Genitiv',
    zh: '所有格',
    use: '誰的？A1 先認識，少主動用。',
  },
] as const

/** 格 × 陰陽中性：定冠詞 */
const DEFINITE_ROWS = [
  ['一格 Nom.', 'der', 'die', 'das', 'die'],
  ['四格 Akk.', 'den', 'die', 'das', 'die'],
  ['三格 Dat.', 'dem', 'der', 'dem', 'den'],
  ['二格 Gen.', 'des', 'der', 'des', 'der'],
]

/** 不定冠詞「一個」ein — 複數沒有 ein */
const INDEFINITE_ROWS = [
  ['一格 Nom.', 'ein', 'eine', 'ein', '—'],
  ['四格 Akk.', 'einen', 'eine', 'ein', '—'],
  ['三格 Dat.', 'einem', 'einer', 'einem', '—'],
  ['二格 Gen.', 'eines', 'einer', 'eines', '—'],
]

/** kein「沒有一個」— 變化跟 ein 同一套，複數有 keine */
const KEIN_ROWS = [
  ['一格 Nom.', 'kein', 'keine', 'kein', 'keine'],
  ['四格 Akk.', 'keinen', 'keine', 'kein', 'keine'],
  ['三格 Dat.', 'keinem', 'keiner', 'keinem', 'keinen'],
  ['二格 Gen.', 'keines', 'keiner', 'keines', 'keiner'],
]

const NUMBER_ONE = [
  {
    article: 'der' as const,
    form: 'ein',
    phrase: 'ein Mann',
    zh: '一個男人',
    alone: 'einer',
  },
  {
    article: 'die' as const,
    form: 'eine',
    phrase: 'eine Frau',
    zh: '一個女人',
    alone: 'eine',
  },
  {
    article: 'das' as const,
    form: 'ein',
    phrase: 'ein Kind',
    zh: '一個孩子',
    alone: 'eins / eines',
  },
]

const SEIN_ROWS = [
  ['ich', 'bin', '我是／在'],
  ['du', 'bist', '你是／在'],
  ['er / sie / es', 'ist', '他／她／它是／在'],
  ['wir', 'sind', '我們是／在'],
  ['ihr', 'seid', '你們是／在'],
  ['sie / Sie', 'sind', '他們／您是／在'],
]

const HABEN_ROWS = [
  ['ich', 'habe', '我有'],
  ['du', 'hast', '你有'],
  ['er / sie / es', 'hat', '他／她／它有'],
  ['wir', 'haben', '我們有'],
  ['ihr', 'habt', '你們有'],
  ['sie / Sie', 'haben', '他們／您有'],
]

function GenderTable({
  caption,
  rows,
}: {
  caption: string
  rows: string[][]
}) {
  return (
    <div className="ai-case">
      <h4>{caption}</h4>
      <div className="grammar-table-wrap">
        <table className="grammar-table">
          <thead>
            <tr>
              <th>格</th>
              <th className="gender-der">陽性</th>
              <th className="gender-die">陰性</th>
              <th className="gender-das">中性</th>
              <th>複數</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row[0]}>
                <td>{row[0]}</td>
                <td className="gender-der">{row[1]}</td>
                <td className="gender-die">{row[2]}</td>
                <td className="gender-das">{row[3]}</td>
                <td>{row[4]}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default function ArticlesIntro() {
  return (
    <div className="articles-intro">
      <section className="ai-hero-card">
        <p className="ai-eyebrow">A1 必備 · 獨立介紹</p>
        <h2>冠詞入門：der · die · das</h2>
        <p className="ai-lead">
          德文名詞幾乎都要帶性別。先把三個定冠詞記熟，再記最常見的那一批名詞；顏色會一直跟著你：
          <span className="gender-der"> der 藍</span>、
          <span className="gender-die"> die 紅</span>、
          <span className="gender-das"> das 綠</span>
          。同一頁也收了最常用的 <strong>bin／bist／ist</strong> 與 haben。
        </p>
        <div className="ai-trio" aria-label="三個定冠詞">
          {(
            [
              ['der', '陽性', '像 der Mann'],
              ['die', '陰性', '像 die Frau'],
              ['das', '中性', '像 das Kind'],
            ] as const
          ).map(([art, gender, eg]) => (
            <div key={art} className={`ai-art-card ${genderClass[art]}`}>
              <strong className={genderClass[art]}>{art}</strong>
              <span>{gender}</span>
              <em>{eg}</em>
              <div className="speak-row">
                <SpeakPair text={art} normalLabel="聽" slowLabel="慢速" />
              </div>
            </div>
          ))}
        </div>
        <p className="ai-note">每張卡片可聽正常／慢速發音。</p>
      </section>

      <section className="ai-block">
        <h3>為什麼一定要記冠詞？</h3>
        <ul className="ai-points">
          <li>同一個拼法，冠詞不同意思可能完全不同（之後學格變也靠它）。</li>
          <li>複數定冠詞一律是 <span className="gender-die">die</span>（先記這個不變的點）。</li>
          <li>不定冠詞「一個」：陽性／中性 <strong>ein</strong>，陰性 <span className="gender-die">eine</span>。</li>
          <li>背單字請連冠詞：不要只背 Haus，要背 <span className="gender-das">das</span> Haus。</li>
        </ul>
      </section>

      <section className="ai-block">
        <h3>sein：bin · bist · ist</h3>
        <p className="ai-lead-sm">
          字典寫 <strong>sein</strong>（是／在），但句子裡幾乎都是變位：ich{' '}
          <strong>bin</strong>、du <strong>bist</strong>、er/sie/es{' '}
          <strong>ist</strong>。單字卡記原形 sein；這裡先把最常用變位背熟。
        </p>
        <div className="grammar-table-wrap">
          <table className="grammar-table ai-conj-table">
            <thead>
              <tr>
                <th>人稱</th>
                <th>sein</th>
                <th>意思</th>
              </tr>
            </thead>
            <tbody>
              {SEIN_ROWS.map((row) => (
                <tr key={row[0]}>
                  <td>{row[0]}</td>
                  <td>
                    <strong>{row[1]}</strong>
                  </td>
                  <td>{row[2]}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="ai-examples">
          <p>
            Ich <strong>bin</strong> Student.／Du <strong>bist</strong> hier.／Das{' '}
            <span className="gender-das">Kind</span> <strong>ist</strong> klein.
          </p>
          <p>
            Wir <strong>sind</strong> in Berlin.／Seid ihr bereit?／Sie{' '}
            <strong>sind</strong> Lehrerin.
          </p>
          <SpeakPair
            text="Ich bin Student. Du bist hier. Das Kind ist klein. Wir sind in Berlin."
            normalLabel="聽 sein"
            slowLabel="慢速"
          />
        </div>

        <h4 className="ai-subhead">haben：habe · hast · hat</h4>
        <p className="ai-lead-sm">
          字典寫 <strong>haben</strong>（有）。跟 sein 一樣，先記變位，單字卡仍用原形。
        </p>
        <div className="grammar-table-wrap">
          <table className="grammar-table ai-conj-table">
            <thead>
              <tr>
                <th>人稱</th>
                <th>haben</th>
                <th>意思</th>
              </tr>
            </thead>
            <tbody>
              {HABEN_ROWS.map((row) => (
                <tr key={row[0]}>
                  <td>{row[0]}</td>
                  <td>
                    <strong>{row[1]}</strong>
                  </td>
                  <td>{row[2]}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="ai-examples">
          <p>
            Ich <strong>habe</strong> ein <span className="gender-das">Buch</span>
            .／Hast du Zeit?／Er <strong>hat</strong> ein{' '}
            <span className="gender-das">Auto</span>.
          </p>
          <SpeakPair
            text="Ich habe ein Buch. Hast du Zeit? Er hat ein Auto."
            normalLabel="聽 haben"
            slowLabel="慢速"
          />
        </div>
        <ul className="ai-points">
          <li>
            單字頁會看到原形 <strong>sein</strong>／<strong>haben</strong>
            ，例句會寫出原形方便對照；變位表以這一頁為準。
          </li>
          <li>
            極常用口頭短句：Wie geht&apos;s? — Mir geht&apos;s gut.／Ich{' '}
            <strong>bin</strong> müde.／Ich <strong>habe</strong> Hunger.
          </li>
        </ul>
      </section>

      <section className="ai-block">
        <h3>四格 × 陰陽中性</h3>
        <p className="ai-lead-sm">
          教科書常寫「一格、四格、三格、二格」——這是<strong>格</strong>；再乘上陽性／陰性／中性／複數，就是冠詞變化表。A1
          先把一格、四格摸熟，三格跟著介系詞學，二格先認識即可。
        </p>
        <div className="ai-case-grid" aria-label="四個格">
          {CASE_CARDS.map((c) => (
            <article key={c.num} className="ai-case-card">
              <p className="ai-case-num">{c.num}</p>
              <p className="ai-case-de">{c.de}</p>
              <p className="ai-case-zh">{c.zh}</p>
              <p className="ai-case-use">{c.use}</p>
            </article>
          ))}
        </div>

        <GenderTable caption="定冠詞 der / die / das" rows={DEFINITE_ROWS} />
        <p className="ai-note ai-table-note">
          入門捷徑：一格→四格，只有陽性 <span className="gender-der">der→den</span>
          ；陰性、中性外形不變。三格陽性／中性都變 <span className="gender-der">dem</span>
          ，陰性變 <span className="gender-die">der</span>。
        </p>

        <GenderTable
          caption="不定冠詞 ein / eine（「一個」）"
          rows={INDEFINITE_ROWS}
        />
        <p className="ai-note ai-table-note">
          複數沒有「一個」：要說 die Bücher，不能說 *ein Bücher。mein／dein／sein
          等物主代詞變化跟 ein 同一套。
        </p>

        <GenderTable caption="kein（沒有一個／不是）" rows={KEIN_ROWS} />
        <p className="ai-note ai-table-note">
          否定名詞用 kein，不要說 *nicht ein Auto → 正確是{' '}
          <span className="gender-das">kein</span> Auto。
        </p>

        <div className="ai-examples">
          <p>
            <span className="gender-der">Der</span> Mann kommt.／Ich sehe{' '}
            <span className="gender-der">den</span> Mann.／Ich helfe{' '}
            <span className="gender-der">dem</span> Mann.
          </p>
          <p>
            <span className="gender-die">Die</span> Frau wartet.／Ich treffe{' '}
            <span className="gender-die">die</span> Frau.／mit{' '}
            <span className="gender-die">der</span> Frau
          </p>
          <p>
            <span className="gender-das">Das</span> Kind spielt.／Ich habe{' '}
            <span className="gender-das">das</span> Kind.／von{' '}
            <span className="gender-das">dem</span> Kind
          </p>
          <SpeakPair
            text="Der Mann kommt. Ich sehe den Mann. Die Frau wartet. Das Kind spielt."
            normalLabel="聽例句"
            slowLabel="慢速"
          />
        </div>
      </section>

      <section className="ai-block">
        <h3>數詞「一」也分陰陽中</h3>
        <p className="ai-lead-sm">
          只有「一」會隨性別變；二、三、四……本身不換陰陽中（後面的名詞冠詞／形容詞才變）。
        </p>
        <div className="ai-one-grid">
          {NUMBER_ONE.map((item) => (
            <article key={item.phrase} className="ai-one-card">
              <p className="ai-lemma">
                <span className={genderClass[item.article]}>{item.form}</span>{' '}
                {item.phrase.split(' ')[1]}
              </p>
              <p className="ai-zh">{item.zh}</p>
              <p className="ai-tip">
                單獨說「一個」時常用{' '}
                <span className={genderClass[item.article]}>{item.alone}</span>
              </p>
              <SpeakPair text={item.phrase} normalLabel="聽" slowLabel="慢速" />
            </article>
          ))}
        </div>
        <ul className="ai-points">
          <li>
            帶名詞：<span className="gender-der">ein</span> Apfel、
            <span className="gender-die">eine</span> Banane、
            <span className="gender-das">ein</span> Brot。
          </li>
          <li>
            單獨回答「幾個？」：陽性 <span className="gender-der">einer</span>
            、陰性 <span className="gender-die">eine</span>、中性常說{' '}
            <span className="gender-das">eins</span>。
          </li>
          <li>
            zwei／drei／vier… 數字本身不變性別：zwei Äpfel、drei Bücher。
          </li>
        </ul>
        <SpeakPair
          text="ein Apfel, eine Banane, ein Brot"
          normalLabel="聽：一個蘋果、一個香蕉、一個麵包"
          slowLabel="慢速"
        />
      </section>

      <section className="ai-block">
        <h3>最普通、最好先背的一批</h3>
        <p className="ai-lead-sm">
          先把下面這些高頻詞連冠詞背熟；之後看例句、點連結會輕鬆很多。
        </p>
        <div className="ai-word-grid">
          {INTRO_WORDS.map((item) => {
            const lemma = `${item.article} ${item.word}`
            return (
              <article key={lemma} className="ai-word">
                <p className="ai-lemma">
                  <span className={genderClass[item.article]}>
                    {item.article}
                  </span>{' '}
                  {item.word}
                </p>
                <p className="ai-zh">{item.zh}</p>
                <p className="ai-tip">{item.tip}</p>
                <SpeakPair text={lemma} normalLabel="聽" slowLabel="慢速" />
              </article>
            )
          })}
        </div>
      </section>

      <section className="ai-block tips beginner">
        <h3>初學者記憶法</h3>
        <ul className="ai-points">
          <li>
            顏色綁定：<span className="gender-der">der＝藍</span>、
            <span className="gender-die">die＝紅</span>、
            <span className="gender-das">das＝綠</span>。
          </li>
          <li>
            先記「格＋性別」兩軸：橫看陰陽中，豎看一／四／三／二格。
          </li>
          <li>
            sein 口訣：bin／bist／ist，複數多半 sind（ihr 是 seid）。
          </li>
          <li>ein 跟 kein、mein 是同一套尾巴，背一組等於背三組。</li>
          <li>單字卡正面只寫「冠詞＋名詞」，反面再寫中文。</li>
          <li>先求正確，不要先追「為什麼是這個性別」——很多只能硬記。</li>
        </ul>
      </section>
    </div>
  )
}
