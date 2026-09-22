import { speakGerman, stopSpeaking } from './lib/speech'
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

const CASES = [
  {
    title: '主格 Nominativ',
    lead: '當主語：誰／什麼在做這件事。',
    rows: [
      ['定冠詞', 'der', 'die', 'das', 'die'],
      ['不定冠詞', 'ein', 'eine', 'ein', '—'],
    ],
  },
  {
    title: '第四格 Akkusativ（入門）',
    lead: '直接受詞：我看到／需要／買誰／什麼。陽性會變。',
    rows: [
      ['定冠詞', 'den', 'die', 'das', 'die'],
      ['不定冠詞', 'einen', 'eine', 'ein', '—'],
    ],
  },
]

function Speak({ text, label }: { text: string; label: string }) {
  return (
    <button
      type="button"
      className="speak-btn"
      onClick={() => speakGerman(text, 0.92)}
      aria-label={label}
    >
      <span className="speak-icon" aria-hidden>
        ♪
      </span>
      {label}
    </button>
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
          <span className="gender-das"> das 綠</span>。
        </p>
        <div className="ai-trio" aria-label="三個定冠詞">
          {(
            [
              ['der', '陽性', '像 der Mann'],
              ['die', '陰性', '像 die Frau'],
              ['das', '中性', '像 das Kind'],
            ] as const
          ).map(([art, gender, eg]) => (
            <button
              key={art}
              type="button"
              className={`ai-art-card ${genderClass[art]}`}
              onClick={() => {
                stopSpeaking()
                speakGerman(art, 0.85)
              }}
            >
              <strong className={genderClass[art]}>{art}</strong>
              <span>{gender}</span>
              <em>{eg}</em>
            </button>
          ))}
        </div>
        <p className="ai-note">點上面三張卡片可聽發音。</p>
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
        <h3>最常用對照表（主格／第四格）</h3>
        {CASES.map((block) => (
          <div key={block.title} className="ai-case">
            <h4>{block.title}</h4>
            <p>{block.lead}</p>
            <div className="grammar-table-wrap">
              <table className="grammar-table">
                <thead>
                  <tr>
                    <th></th>
                    <th className="gender-der">陽性</th>
                    <th className="gender-die">陰性</th>
                    <th className="gender-das">中性</th>
                    <th>複數</th>
                  </tr>
                </thead>
                <tbody>
                  {block.rows.map((row) => (
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
        ))}
        <div className="ai-examples">
          <p>
            <span className="gender-der">Der</span> Mann kommt.／Ich sehe{' '}
            <span className="gender-der">den</span> Mann.
          </p>
          <p>
            <span className="gender-die">Die</span> Frau wartet.／Ich treffe{' '}
            <span className="gender-die">die</span> Frau.
          </p>
          <p>
            <span className="gender-das">Das</span> Kind spielt.／Ich habe{' '}
            <span className="gender-das">das</span> Kind.
          </p>
          <Speak
            label="聽三句"
            text="Der Mann kommt. Die Frau wartet. Das Kind spielt."
          />
        </div>
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
                <Speak label="聽" text={lemma} />
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
          <li>單字卡正面只寫「冠詞＋名詞」，反面再寫中文。</li>
          <li>先求正確，不要先追「為什麼是這個性別」——很多只能硬記。</li>
          <li>
            複數先記：不管單數是誰，複數定冠詞多半是{' '}
            <span className="gender-die">die</span>。
          </li>
        </ul>
      </section>
    </div>
  )
}
