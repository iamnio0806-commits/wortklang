import {
  PREFIX_MEANINGS,
  ROOT_MEANINGS,
  SUFFIX_MEANINGS,
  countAffixes,
  sortByLevel,
  type AffixEntry,
  type AffixKind,
  type AffixLevel,
} from './data/affixes'
import { speakGerman, stopSpeaking } from './lib/speech'

const KIND_LABEL: Record<AffixKind, string> = {
  separable: '可分字首',
  inseparable: '不可分字首',
  either: '可分／不可分',
  suffix: '字尾',
  root: '字根',
}

const LEVEL_META: {
  level: AffixLevel
  title: string
  lead: string
}[] = [
  {
    level: 'A1',
    title: 'A1 · 最先背',
    lead: '方向可分字首、be-/ver-/er-，以及最常見字尾與日常字根。先把這一層記熟。',
  },
  {
    level: 'A2',
    title: 'A2 · 接著擴充',
    lead: 'zurück／zusammen、durch／über／um，以及 -schaft／-bar／-tion 等。',
  },
  {
    level: 'B1',
    title: 'B1 · 方向複合與外來字根',
    lead: 'hinein／heraus、miss-/ur-，還有 graph／phon／bio 等國際字根。',
  },
  {
    level: 'B2',
    title: 'B2 · 進階與學術',
    lead: 'wider、inter／trans／prä 等，閱讀長文時特別有用。',
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

function AffixCard({ entry }: { entry: AffixEntry }) {
  const display =
    entry.kind === 'suffix'
      ? `-${entry.form}`
      : entry.kind === 'root'
        ? entry.form
        : `${entry.form}-`
  const sample = entry.examples[0]?.de ?? entry.form
  return (
    <article className={`af-card af-${entry.kind}`}>
      <div className="af-card-top">
        <button
          type="button"
          className="af-form"
          onClick={() => {
            stopSpeaking()
            speakGerman(sample, 0.9)
          }}
          aria-label={`聽 ${display}`}
        >
          {display}
        </button>
        <span className="af-kind">{KIND_LABEL[entry.kind]}</span>
      </div>
      <p className="af-zh">{entry.zh}</p>
      <p className="af-tip">{entry.tip}</p>
      <ul className="af-examples">
        {entry.examples.map((ex) => (
          <li key={ex.de}>
            <strong>{ex.de}</strong>
            <span>{ex.zh}</span>
          </li>
        ))}
      </ul>
    </article>
  )
}

function LevelBlock({
  level,
  title,
  lead,
}: {
  level: AffixLevel
  title: string
  lead: string
}) {
  const prefixes = sortByLevel(
    PREFIX_MEANINGS.filter((e) => e.level === level),
  )
  const suffixes = sortByLevel(
    SUFFIX_MEANINGS.filter((e) => e.level === level),
  )
  const roots = sortByLevel(ROOT_MEANINGS.filter((e) => e.level === level))
  if (!prefixes.length && !suffixes.length && !roots.length) return null

  const sep = prefixes.filter((e) => e.kind === 'separable')
  const insep = prefixes.filter((e) => e.kind === 'inseparable')
  const either = prefixes.filter((e) => e.kind === 'either')

  return (
    <section className="ai-block af-level" data-level={level}>
      <div className="af-level-head">
        <span className={`level-pill level-${level}`}>{level}</span>
        <h3>{title}</h3>
      </div>
      <p className="ai-lead-sm">{lead}</p>

      {sep.length > 0 && (
        <>
          <h4 className="ai-subhead">可分字首</h4>
          <div className="af-grid">
            {sep.map((e) => (
              <AffixCard key={`p-${e.form}`} entry={e} />
            ))}
          </div>
        </>
      )}
      {either.length > 0 && (
        <>
          <h4 className="ai-subhead">可分或不可分</h4>
          <div className="af-grid">
            {either.map((e) => (
              <AffixCard key={`e-${e.form}`} entry={e} />
            ))}
          </div>
        </>
      )}
      {insep.length > 0 && (
        <>
          <h4 className="ai-subhead">不可分字首</h4>
          <div className="af-grid">
            {insep.map((e) => (
              <AffixCard key={`i-${e.form}`} entry={e} />
            ))}
          </div>
        </>
      )}
      {suffixes.length > 0 && (
        <>
          <h4 className="ai-subhead">字尾</h4>
          <div className="af-grid">
            {suffixes.map((e) => (
              <AffixCard key={`s-${e.form}`} entry={e} />
            ))}
          </div>
        </>
      )}
      {roots.length > 0 && (
        <>
          <h4 className="ai-subhead">字根</h4>
          <div className="af-grid">
            {roots.map((e) => (
              <AffixCard key={`r-${e.form}`} entry={e} />
            ))}
          </div>
        </>
      )}
    </section>
  )
}

export default function AffixesIntro() {
  const counts = countAffixes()

  return (
    <div className="articles-intro affixes-intro">
      <section className="ai-hero-card">
        <p className="ai-eyebrow">A1→B2 · 由易到難</p>
        <h2>字首 · 字根 · 字尾</h2>
        <p className="ai-lead">
          共 <strong>{counts.prefixes}</strong> 個字首、
          <strong>{counts.suffixes}</strong> 個字尾、
          <strong>{counts.roots}</strong> 個字根。下面依{' '}
          <strong>A1 → A2 → B1 → B2</strong> 排列，最簡單的在最上面。
        </p>
        <div className="af-hero-row" aria-label="拆字示意">
          <span className="chip chip-prefix">ver-</span>
          <span className="af-plus">+</span>
          <span className="chip chip-root">steh</span>
          <span className="af-plus">+</span>
          <span className="chip chip-suffix">-en</span>
          <span className="af-eq">→</span>
          <strong className="af-result">verstehen＝理解</strong>
        </div>
        <p className="ai-note">
          ver-≈改變／完成；steh≈站；合起來常記「把意思站穩＝懂了」。
        </p>
        <Speak label="聽 verstehen" text="verstehen" />
      </section>

      <section className="ai-block">
        <h3>怎麼用這頁？</h3>
        <ul className="ai-points">
          <li>先把 <strong>A1</strong> 整層背完，再往下翻 A2／B1。</li>
          <li>
            <strong>可分字首</strong>
            ：現在時飛到句尾（Ich stehe um 7 Uhr <em>auf</em>）。
          </li>
          <li>
            <strong>不可分字首</strong>
            ：黏著不動，過去分詞通常不加 ge-（verstanden）。
          </li>
          <li>
            <strong>字根</strong>
            ：同一字根會出現在動詞、名詞、複合詞裡，串起來記。
          </li>
          <li>單字詳情的彩色碎片會顯示同樣的中文意思。</li>
        </ul>
      </section>

      {LEVEL_META.map((meta) => (
        <LevelBlock key={meta.level} {...meta} />
      ))}

      <section className="ai-block tips beginner">
        <h3>初學者記憶法</h3>
        <ul className="ai-points">
          <li>A1 方向：ein／aus／auf／ab／an／zu／mit／vor／nach／weg。</li>
          <li>A1 不可分：be-、ver-、er-、ge-。</li>
          <li>
            名詞工廠：動詞 + -ung → die；形容詞 + -heit／-keit → die；-chen →
            das。
          </li>
          <li>字根先背：geh／komm／steh／seh／hör／sprech／schreib／wohn。</li>
        </ul>
      </section>
    </div>
  )
}
