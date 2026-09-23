import { SpeakPair } from './lib/SpeakControls'
import { genderClass } from './lib/richText'

type PrepCase = 'Akk' | 'Dat' | 'Wechsel'

type PrepCard = {
  prep: string
  zh: string
  tip: string
  example: string
  exampleZh: string
}

const AKK_PREPS: PrepCard[] = [
  {
    prep: 'für',
    zh: '為了；給',
    tip: '固定第四格',
    example: 'Das Geschenk ist für dich.',
    exampleZh: '這份禮物是給你的。',
  },
  {
    prep: 'durch',
    zh: '穿過；藉由',
    tip: '固定第四格',
    example: 'Wir gehen durch den Park.',
    exampleZh: '我們穿過公園。',
  },
  {
    prep: 'ohne',
    zh: '沒有',
    tip: '固定第四格',
    example: 'Ich trinke Kaffee ohne Milch.',
    exampleZh: '我喝不加牛奶的咖啡。',
  },
  {
    prep: 'um',
    zh: '圍繞；在…點',
    tip: '時間「整點」也用 um',
    example: 'Wir treffen uns um drei Uhr.',
    exampleZh: '我們三點碰面。',
  },
  {
    prep: 'gegen',
    zh: '對抗；大約',
    tip: '也可表「大約」（時間）',
    example: 'Das Spiel ist gegen Bayern.',
    exampleZh: '這場比賽對上拜仁。',
  },
  {
    prep: 'bis',
    zh: '直到',
    tip: '常跟 zu 連用：bis zum…',
    example: 'Ich bleibe bis Freitag.',
    exampleZh: '我待到星期五。',
  },
]

const DAT_PREPS: PrepCard[] = [
  {
    prep: 'mit',
    zh: '和；用',
    tip: '固定第三格：mit dem Bus',
    example: 'Ich fahre mit dem Bus.',
    exampleZh: '我搭公車。',
  },
  {
    prep: 'zu',
    zh: '去（某人／某處）',
    tip: 'zum = zu dem；zur = zu der',
    example: 'Ich gehe zum Arzt.',
    exampleZh: '我去看醫生。',
  },
  {
    prep: 'von',
    zh: '從；屬於',
    tip: 'vom = von dem',
    example: 'Der Zug kommt von Berlin.',
    exampleZh: '這班火車從柏林來。',
  },
  {
    prep: 'bei',
    zh: '在…旁邊／家',
    tip: 'bei mir = 在我家',
    example: 'Ich wohne bei meinen Eltern.',
    exampleZh: '我住在父母家。',
  },
  {
    prep: 'nach',
    zh: '往（城市／國）；之後',
    tip: '城市多數用 nach Berlin',
    example: 'Wir fahren nach Deutschland.',
    exampleZh: '我們去德國。',
  },
  {
    prep: 'aus',
    zh: '從…出來；來自',
    tip: 'Ich komme aus Taiwan.',
    example: 'Ich komme aus Taiwan.',
    exampleZh: '我來自台灣。',
  },
  {
    prep: 'seit',
    zh: '自從',
    tip: '固定第三格：seit dem Montag',
    example: 'Ich lerne seit einem Jahr Deutsch.',
    exampleZh: '我學德文一年了。',
  },
  {
    prep: 'außer',
    zh: '除了',
    tip: '固定第三格',
    example: 'Außer mir kommt niemand.',
    exampleZh: '除了我沒人來。',
  },
]

const WECHSEL_PREPS: PrepCard[] = [
  {
    prep: 'in',
    zh: '在…裡／進…裡',
    tip: '位置 Dat · 方向 Akk',
    example: 'Ich bin in der Schule. / Ich gehe in die Schule.',
    exampleZh: '我在學校。／我去學校。',
  },
  {
    prep: 'an',
    zh: '在…旁／到…旁',
    tip: '牆邊、水邊常用 an',
    example: 'Das Bild hängt an der Wand.',
    exampleZh: '畫掛在牆上。',
  },
  {
    prep: 'auf',
    zh: '在…上／到…上',
    tip: '平面上方：auf dem Tisch',
    example: 'Das Buch liegt auf dem Tisch.',
    exampleZh: '書在桌子上。',
  },
  {
    prep: 'über',
    zh: '在…上方；關於',
    tip: '「關於」常用第四格',
    example: 'Wir sprechen über das Wetter.',
    exampleZh: '我們聊天氣。',
  },
  {
    prep: 'unter',
    zh: '在…下面',
    tip: '位置 Dat · 方向 Akk',
    example: 'Die Katze sitzt unter dem Tisch.',
    exampleZh: '貓坐在桌子下面。',
  },
  {
    prep: 'vor',
    zh: '在…前面；之前',
    tip: '時間「之前」也用 vor',
    example: 'Wir treffen uns vor dem Bahnhof.',
    exampleZh: '我們在火車站前面碰面。',
  },
  {
    prep: 'hinter',
    zh: '在…後面',
    tip: '位置 Dat · 方向 Akk',
    example: 'Das Auto steht hinter dem Haus.',
    exampleZh: '車停在房子後面。',
  },
  {
    prep: 'neben',
    zh: '在…旁邊',
    tip: '位置 Dat · 方向 Akk',
    example: 'Sie sitzt neben mir.',
    exampleZh: '她坐在我旁邊。',
  },
  {
    prep: 'zwischen',
    zh: '在…之間',
    tip: '複數第三格：zwischen den Häusern',
    example: 'Der Park liegt zwischen den Häusern.',
    exampleZh: '公園在房子之間。',
  },
]

const FIXED_PHRASES = [
  { de: 'zu Hause', zh: '在家（位置）' },
  { de: 'nach Hause', zh: '回家（方向）' },
  { de: 'im Moment', zh: '目前（in dem）' },
  { de: 'am Morgen', zh: '在早上（an dem）' },
  { de: 'mit dem Auto', zh: '坐汽車' },
  { de: 'zur Arbeit', zh: '去上班（zu der）' },
  { de: 'vom Bahnhof', zh: '從火車站（von dem）' },
  { de: 'für mich', zh: '為了我' },
]

const CASE_BADGE: Record<PrepCase, string> = {
  Akk: '第四格 Akk',
  Dat: '第三格 Dat',
  Wechsel: '兩用 Wechsel',
}

function PrepGrid({
  title,
  caseKind,
  items,
}: {
  title: string
  caseKind: PrepCase
  items: PrepCard[]
}) {
  return (
    <section className="ai-block">
      <h3>
        {title}{' '}
        <span className={`prep-badge prep-badge-${caseKind.toLowerCase()}`}>
          {CASE_BADGE[caseKind]}
        </span>
      </h3>
      <p className="ai-lead-sm">
        {caseKind === 'Akk' &&
          '這些介詞後面的名詞／代詞用第四格（Akkusativ）。陽性：der → den。'}
        {caseKind === 'Dat' &&
          '這些介詞後面用第三格（Dativ）。陽性／中性：dem；陰性：der；複數：den。'}
        {caseKind === 'Wechsel' &&
          '同一介詞兩種用法：回答 wo?（在哪裡）→ 第三格；回答 wohin?（去哪裡）→ 第四格。'}
      </p>
      <div className="prep-grid">
        {items.map((p) => (
          <article key={p.prep} className="prep-card">
            <div className="prep-card-top">
              <strong>{p.prep}</strong>
              <span>{p.zh}</span>
            </div>
            <p className="prep-tip">{p.tip}</p>
            <p className="prep-ex">
              <em>{p.example}</em>
              <span>{p.exampleZh}</span>
            </p>
            <div className="speak-row">
              <SpeakPair
                text={p.example}
                normalLabel="聽例句"
                slowLabel="慢速"
              />
            </div>
          </article>
        ))}
      </div>
    </section>
  )
}

export default function PrepositionsIntro() {
  return (
    <div className="articles-intro prep-intro">
      <section className="ai-hero-card">
        <p className="ai-eyebrow">A1–A2 必備 · 獨立篇章</p>
        <h2>介係詞入門：mit · für · in · zu…</h2>
        <p className="ai-lead">
          德文介係詞（Präposition）不只表「在／去／和」，還會決定後面用哪一格。先分三組記：
          <strong>固定第四格</strong>、<strong>固定第三格</strong>、以及
          <strong>位置／方向兩用</strong>。冠詞顏色規則不變：
          <span className={genderClass.der}> der 藍</span>、
          <span className={genderClass.die}> die 紅</span>、
          <span className={genderClass.das}> das 綠</span>
          —看介詞後面的名詞性別與格。
        </p>
        <div className="ai-trio" aria-label="三組介詞">
          {(
            [
              ['Akk', '固定第四格', 'für / durch / ohne'],
              ['Dat', '固定第三格', 'mit / zu / von / bei'],
              ['Wechsel', '兩用介詞', 'in / an / auf · wo≠wohin'],
            ] as const
          ).map(([k, title, eg]) => (
            <div key={k} className="ai-art-card">
              <strong className={`prep-badge prep-badge-${k.toLowerCase()}`}>
                {k}
              </strong>
              <span>{title}</span>
              <em>{eg}</em>
            </div>
          ))}
        </div>
        <p className="ai-note">
          建議順序：先背固定第三／第四格 → 再練兩用介詞的 wo / wohin。
        </p>
      </section>

      <section className="ai-block">
        <h3>為什麼介係詞這麼重要？</h3>
        <ul className="ai-points">
          <li>
            同一個名詞，格不同形式就不同：
            <strong> mit dem Mann</strong>（三格）≠{' '}
            <strong>für den Mann</strong>（四格）。
          </li>
          <li>
            位置與方向意思差很多：
            <strong> in der Schule</strong>（在學校）≠{' '}
            <strong>in die Schule</strong>（去學校）。
          </li>
          <li>
            日常生活超高頻：搭車 <strong>mit dem Bus</strong>、回家{' '}
            <strong>nach Hause</strong>、在家 <strong>zu Hause</strong>。
          </li>
          <li>先背「介詞＋哪一格」整組，不要把介詞跟格拆開硬背。</li>
        </ul>
      </section>

      <PrepGrid title="固定第四格介詞" caseKind="Akk" items={AKK_PREPS} />
      <PrepGrid title="固定第三格介詞" caseKind="Dat" items={DAT_PREPS} />
      <PrepGrid
        title="兩用介詞（Wechselpräpositionen）"
        caseKind="Wechsel"
        items={WECHSEL_PREPS}
      />

      <section className="ai-block">
        <h3>兩用介詞怎麼選格？</h3>
        <div className="grammar-table-wrap">
          <table className="grammar-table">
            <thead>
              <tr>
                <th>問法</th>
                <th>意思</th>
                <th>用格</th>
                <th>例子</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>
                  <strong>wo?</strong>
                </td>
                <td>在哪裡？（位置）</td>
                <td>第三格 Dat</td>
                <td>
                  Ich bin <strong>in der</strong> Küche.
                </td>
              </tr>
              <tr>
                <td>
                  <strong>wohin?</strong>
                </td>
                <td>去哪裡？（方向）</td>
                <td>第四格 Akk</td>
                <td>
                  Ich gehe <strong>in die</strong> Küche.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div className="ai-examples">
          <p>
            Das Buch liegt <strong>auf dem</strong> Tisch.（在上面 → Dat）
          </p>
          <p>
            Ich lege das Buch <strong>auf den</strong> Tisch.（放到上面 → Akk）
          </p>
          <SpeakPair
            text="Ich bin in der Küche. Ich gehe in die Küche. Das Buch liegt auf dem Tisch."
            normalLabel="聽對照"
            slowLabel="慢速"
          />
        </div>
      </section>

      <section className="ai-block">
        <h3>高頻固定說法（先整句背）</h3>
        <p className="ai-lead-sm">
          這些幾乎每天都會用到，先當搭配記，比拆開分析更快上手。
        </p>
        <ul className="prep-phrases">
          {FIXED_PHRASES.map((p) => (
            <li key={p.de}>
              <div>
                <strong>{p.de}</strong>
                <span>{p.zh}</span>
              </div>
              <SpeakPair text={p.de} normalLabel="聽" slowLabel="慢" />
            </li>
          ))}
        </ul>
      </section>

      <section className="ai-block tips beginner">
        <h3>學習提醒</h3>
        <ul className="ai-points">
          <li>
            縮寫很常見：<strong>zum</strong>=zu dem、<strong>zur</strong>=zu der、
            <strong>vom</strong>=von dem、<strong>im</strong>=in dem、
            <strong>am</strong>=an dem。
          </li>
          <li>
            <strong>nach</strong>＋城市／多數國家（nach Berlin）；有冠詞的國名用{' '}
            <strong>in die</strong>（in die Schweiz）。
          </li>
          <li>
            想練更多題，到「文法」找：地點介詞、固定三／四格介詞、兩用介詞。
          </li>
        </ul>
      </section>
    </div>
  )
}
