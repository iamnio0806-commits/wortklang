import {
  PREFIX_MEANINGS,
  SUFFIX_MEANINGS,
  type AffixEntry,
  type AffixKind,
} from './data/affixes'
import { speakGerman, stopSpeaking } from './lib/speech'

const KIND_LABEL: Record<AffixKind, string> = {
  separable: '可分字首',
  inseparable: '不可分字首',
  either: '可分／不可分',
  suffix: '字尾',
}

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
  const display = entry.kind === 'suffix' ? `-${entry.form}` : `${entry.form}-`
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

function AffixGrid({
  title,
  lead,
  items,
}: {
  title: string
  lead: string
  items: AffixEntry[]
}) {
  return (
    <section className="ai-block">
      <h3>{title}</h3>
      <p className="ai-lead-sm">{lead}</p>
      <div className="af-grid">
        {items.map((e) => (
          <AffixCard key={e.form + e.kind} entry={e} />
        ))}
      </div>
    </section>
  )
}

export default function AffixesIntro() {
  const separable = PREFIX_MEANINGS.filter((e) => e.kind === 'separable')
  const inseparable = PREFIX_MEANINGS.filter((e) => e.kind === 'inseparable')
  const either = PREFIX_MEANINGS.filter((e) => e.kind === 'either')

  return (
    <div className="articles-intro affixes-intro">
      <section className="ai-hero-card">
        <p className="ai-eyebrow">A1–B1 · 獨立介紹</p>
        <h2>字首 · 字根 · 字尾</h2>
        <p className="ai-lead">
          德文很多詞可以拆：<strong>字首</strong>改方向或語氣、
          <strong>字根</strong>是核心意思、<strong>字尾</strong>常決定詞性與冠詞。
          先記高頻字首的中文意思，之後看單字頁的彩色碎片會好懂很多。
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
          ver-≈改變／完成語氣；steh≈站／立；合起來常記成「把意思站穩＝懂了」。
        </p>
        <Speak label="聽 verstehen" text="verstehen" />
      </section>

      <section className="ai-block">
        <h3>怎麼用這頁？</h3>
        <ul className="ai-points">
          <li>
            <strong>可分字首</strong>
            ：現在時會飛到句尾（Ich stehe um 7 Uhr <em>auf</em>）。
          </li>
          <li>
            <strong>不可分字首</strong>
            ：永遠黏著，過去分詞通常<strong>不加</strong> ge-（verstanden）。
          </li>
          <li>
            <strong>字尾</strong>：常決定是名詞還是形容詞，以及 der／die／das。
          </li>
          <li>單字詳情裡的碎片會顯示同樣的中文意思，可兩邊對照。</li>
        </ul>
      </section>

      <AffixGrid
        title="可分字首（高頻）"
        lead="意思多半跟方向、一起、開關有關。點卡片可聽例句詞。"
        items={separable}
      />

      <AffixGrid
        title="可分或不可分"
        lead="同一字形兩種用法：重音在字首→可分；重音在字根→不可分。"
        items={either}
      />

      <AffixGrid
        title="不可分字首"
        lead="be-／ver-／er-／ent-／zer-／miss-／un-… 改語氣或詞性，不飛到句尾。"
        items={inseparable}
      />

      <AffixGrid
        title="常見字尾"
        lead="看到字尾先猜詞性：-ung／-heit 多半 die；-chen 一定 das；-er 常是人。"
        items={SUFFIX_MEANINGS}
      />

      <section className="ai-block tips beginner">
        <h3>初學者記憶法</h3>
        <ul className="ai-points">
          <li>方向類先背：ein／aus／auf／ab／an／mit／zurück。</li>
          <li>不可分五兄弟：be-、ver-、er-、ent-、zer-（再加 miss-、un-）。</li>
          <li>
            名詞工廠：動詞 + -ung → die（wohnen→Wohnung）；形容詞 + -heit／-keit
            → die。
          </li>
          <li>小稱 -chen／-lein → 一律 das，常變母音。</li>
        </ul>
      </section>
    </div>
  )
}
