import { useEffect, useMemo, useState, type ReactNode } from 'react'
import {
  categories,
  countByLevel,
  levels,
  vocabulary,
  type Category,
  type Gender,
  type Level,
  type VocabWord,
} from './data/vocabulary'
import {
  enrich,
  PLURAL_PATTERN_GUIDE,
  type EnrichedWord,
} from './lib/enrich'
import {
  ArticleText,
  genderClass,
  PosLabel,
  RichText,
} from './lib/richText'
import { LinkedGermanText } from './lib/LinkedGermanText'
import type { VocabHit } from './lib/vocabIndex'
import { searchVocabulary } from './lib/search'
import { ensureVoicesLoaded, speakGerman, stopSpeaking } from './lib/speech'
import GrammarView from './GrammarView'
import ArticlesIntro from './ArticlesIntro'
import AffixesIntro from './AffixesIntro'
import ReadingView from './ReadingView'
import ExamView from './ExamView'
import { lookupPrefix, lookupSuffix } from './data/affixes'
import './App.css'

type Section = 'vocab' | 'grammar' | 'articles' | 'affixes' | 'reading' | 'exam'
type Mode = 'browse' | 'flash' | 'plural' | 'verb' | 'family'
type LevelFilter = Level | '全部'
type WordTypeFilter = '全部' | '名詞' | '動詞' | '形容詞'

type NavSnap = {
  section: Section
  mode: Mode
  selectedId: string
  levelFilter: LevelFilter
  category: Category | '全部'
  wordType: WordTypeFilter
  gender: '全部' | 'der' | 'die' | 'das' | '無冠詞'
  query: string
  hideLearned: boolean
  flashIndex: number
}

const LEARNED_KEY = 'wortklang-learned'

/** Color every der/die/das (any case) inside a text string. */
function ColoredLemma({
  article,
  word,
  as: Tag = 'span',
}: {
  article?: Gender | null
  word: string
  as?: 'span' | 'strong'
}) {
  return (
    <Tag>
      {article ? (
        <>
          <span className={genderClass[article]}>{article}</span>{' '}
        </>
      ) : null}
      {word}
    </Tag>
  )
}

const MODE_LABEL: Record<Mode, string> = {
  browse: '單字瀏覽',
  flash: '閃卡意思',
  plural: '複數記憶',
  verb: '動詞變化',
  family: '字族聯想',
}

function loadLearned(): Set<string> {
  try {
    const raw = localStorage.getItem(LEARNED_KEY)
    if (!raw) return new Set()
    const parsed = JSON.parse(raw) as string[]
    return new Set(Array.isArray(parsed) ? parsed : [])
  } catch {
    return new Set()
  }
}

function WordBadge({ article }: { article: Gender }) {
  if (!article) return <span className="badge badge-neutral">無冠詞</span>
  return <span className={`badge ${genderClass[article]}`}>{article}</span>
}

function SpeakButton({
  label,
  text,
  slow,
}: {
  label: string
  text: string
  slow?: boolean
}) {
  return (
    <button
      type="button"
      className="speak-btn"
      onClick={() => speakGerman(text, slow ? 0.7 : 0.92)}
      aria-label={label}
    >
      <span className="speak-icon" aria-hidden>
        ♪
      </span>
      {label}
    </button>
  )
}

function NavButtons({
  onPrev,
  onNext,
  label,
  onBack,
}: {
  onPrev: () => void
  onNext: () => void
  label: string
  onBack?: () => void
}) {
  return (
    <div className="nav-block">
      {onBack && (
        <button type="button" className="ghost nav-back" onClick={onBack}>
          ← 回上頁
        </button>
      )}
      <div className="nav-row">
        <button type="button" className="ghost nav-btn" onClick={onPrev}>
          ← 上一個
        </button>
        <span className="nav-label">{label}</span>
        <button type="button" className="ghost nav-btn" onClick={onNext}>
          下一個 →
        </button>
      </div>
    </div>
  )
}

function GrammarPanels({ e }: { e: EnrichedWord }) {
  return (
    <>
      {e.parts && (e.parts.prefixes.length > 0 || e.parts.suffixes.length > 0) && (
        <section className="panel">
          <h3>字首／字根／字尾</h3>
          <div className="parts-row">
            {e.parts.prefixes.map((p) => {
              const m = lookupPrefix(p)
              return (
                <span key={p} className="chip chip-prefix" title={m?.tip}>
                  {p}-{m ? <small className="chip-mean">{m.zh}</small> : null}
                </span>
              )
            })}
            <span className="chip chip-root">
              {e.parts.root}
              <small className="chip-mean">字根</small>
            </span>
            {e.parts.suffixes.map((s) => {
              const m = lookupSuffix(s)
              return (
                <span key={s} className="chip chip-suffix" title={m?.tip}>
                  -{s}
                  {m ? <small className="chip-mean">{m.zh}</small> : null}
                </span>
              )
            })}
          </div>
          {e.parts.note && (
            <p className="panel-note">
              <ArticleText text={e.parts.note} />
            </p>
          )}
        </section>
      )}

      {e.wordType === '名詞' && (
        <section className="panel">
          <h3>名詞複數（對照英文記法）</h3>
          <p className="panel-lead">
            {e.plural ? (
              <>
                <ColoredLemma article={e.article} word={e.word} as="strong" />{' '}
                →{' '}
                <ColoredLemma article="die" word={e.plural} as="strong" />
                {e.pluralPattern && (
                  <span className="pattern-tag">{e.pluralPattern}</span>
                )}
              </>
            ) : (
              '此詞複數較少用或不規則，先記單數＋冠詞。'
            )}
          </p>
          {e.pluralHint && (
            <p className="panel-note">
              <ArticleText text={e.pluralHint} />
            </p>
          )}
          <ul className="guide-list">
            {PLURAL_PATTERN_GUIDE.slice(0, 5).map((g) => (
              <li key={g.pattern}>
                <strong>{g.pattern}</strong>：{g.likeEnglish}（例{' '}
                <ArticleText text={g.example} />）
              </li>
            ))}
          </ul>
        </section>
      )}

      {e.verb && (
        <section className="panel">
          <h3>動詞用法與變化</h3>
          <p className="panel-lead">
            <span className="pattern-tag">{e.verb.class}</span>
            {e.verb.separable && (
              <span className="pattern-tag">可分：{e.verb.separable}-</span>
            )}
          </p>
          <p className="panel-note">
            <ArticleText text={e.verb.usage} />
          </p>
          <div className="conj-grid">
            <div>
              <span>ich</span>
              <strong>{e.verb.present.ich}</strong>
            </div>
            <div>
              <span>du</span>
              <strong>{e.verb.present.du}</strong>
            </div>
            <div>
              <span>er/sie/es</span>
              <strong>{e.verb.present.er}</strong>
            </div>
            <div>
              <span>wir</span>
              <strong>{e.verb.present.wir}</strong>
            </div>
            <div>
              <span>ihr</span>
              <strong>{e.verb.present.ihr}</strong>
            </div>
            <div>
              <span>Sie/sie</span>
              <strong>{e.verb.present.sie}</strong>
            </div>
          </div>
          <dl className="meta compact">
            <dt>過去式</dt>
            <dd>{e.verb.preterite}</dd>
            <dt>過去分詞</dt>
            <dd>
              {e.verb.auxiliary} + {e.verb.participle}
            </dd>
          </dl>
          <div className="speak-row">
            <SpeakButton
              label="聽現在時"
              text={`${e.verb.present.ich}. ${e.verb.present.du}. ${e.verb.present.er}.`}
            />
          </div>
        </section>
      )}

      {e.related.length > 0 && (
        <section className="panel">
          <h3>相關詞／字族（像英文 work→worker）</h3>
          <ul className="related-list">
            {e.related.map((r) => (
              <li key={`${r.relation}-${r.word}`}>
                <span className="related-rel">{r.relation}</span>
                <strong>
                  <ColoredLemma article={r.article} word={r.word} />
                </strong>
                <span className="related-zh">{r.translation}</span>
              </li>
            ))}
          </ul>
        </section>
      )}

      <section className="panel tips">
        <h3>記憶法</h3>
        <ul>
          {e.memoryTips.map((t) => (
            <li key={t}>
              <ArticleText text={t} />
            </li>
          ))}
        </ul>
      </section>
    </>
  )
}

function WordDetail({
  word,
  learned,
  onToggleLearned,
  onPrev,
  onNext,
  positionLabel,
  onOpenWord,
  onBack,
}: {
  word: VocabWord
  learned: boolean
  onToggleLearned: () => void
  onPrev: () => void
  onNext: () => void
  positionLabel: string
  onOpenWord: (hit: VocabHit) => void
  onBack?: () => void
}) {
  const e = enrich(word)
  const lemma = word.article ? `${word.article} ${word.word}` : word.word

  return (
    <article className="detail" key={word.id}>
      <NavButtons
        onPrev={onPrev}
        onNext={onNext}
        label={positionLabel}
        onBack={onBack}
      />

      <div className="detail-top">
        <WordBadge article={word.article} />
        <PosLabel type={e.wordType} as="span" />
        <span className={`level-pill level-${word.level}`}>{word.level}</span>
      </div>

      <h2 className="lemma">
        {word.article && (
          <span className={genderClass[word.article]}>{word.article}</span>
        )}
        <span className="word">{word.word}</span>
      </h2>

      <p className="translation">{word.translation}</p>
      <p className="phonetic">/{word.phonetic}/</p>

      <dl className="meta">
        {word.article && (
          <>
            <dt>冠詞</dt>
            <dd className={genderClass[word.article]}>{word.article}</dd>
          </>
        )}
        {word.plural && (
          <>
            <dt>複數</dt>
            <dd>
              <ColoredLemma article="die" word={word.plural} />
            </dd>
          </>
        )}
        <dt>詞性</dt>
        <PosLabel type={e.wordType} as="dd" />
        <dt>等級</dt>
        <dd>{word.level}</dd>
        <dt>分類</dt>
        <dd>
          <RichText text={word.category} />
        </dd>
      </dl>

      <div className="speak-row">
        <SpeakButton label="聽單字" text={lemma} />
        <SpeakButton label="慢速" text={lemma} slow />
        {word.plural && (
          <SpeakButton label="聽複數" text={`die ${word.plural}`} />
        )}
        <button
          type="button"
          className={learned ? 'learned-btn on' : 'learned-btn'}
          onClick={onToggleLearned}
        >
          {learned ? '已學會 ✓' : '標記已學會'}
        </button>
      </div>

      <section className="example">
        <h3>例句</h3>
        <p className="example-hint">點德文詞可跳到該單字</p>
        <p className="example-de">
          <LinkedGermanText
            text={word.example}
            preferLevel={word.level}
            preferId={word.id}
            currentId={word.id}
            onOpenWord={onOpenWord}
          />
        </p>
        <p className="example-zh">
          <ArticleText text={word.exampleTranslation} />
        </p>
        <div className="speak-row">
          <SpeakButton label="聽例句" text={word.example} />
          <SpeakButton label="慢速例句" text={word.example} slow />
        </div>
      </section>

      <GrammarPanels e={e} />
    </article>
  )
}

function PracticeCard({
  mode,
  word,
  revealed,
  onReveal,
  onPrev,
  onNext,
  onMark,
  positionLabel,
  onOpenWord,
  onBack,
}: {
  mode: Mode
  word: VocabWord
  revealed: boolean
  onReveal: () => void
  onPrev: () => void
  onNext: () => void
  onMark: () => void
  positionLabel: string
  onOpenWord: (hit: VocabHit) => void
  onBack?: () => void
}) {
  const e = enrich(word)
  const lemma = word.article ? `${word.article} ${word.word}` : word.word

  let prompt = '這是什麼意思？'
  let frontExtra: ReactNode = null
  let backExtra: ReactNode = null

  if (mode === 'plural') {
    prompt = '複數是什麼？屬於哪種變化？'
    frontExtra = (
      <p className="flash-sub">
        <ColoredLemma article={word.article} word={word.word} />
      </p>
    )
    backExtra = (
      <>
        <p className="translation">
          <ColoredLemma
            article="die"
            word={word.plural ?? '（少用／無）'}
          />
        </p>
        {e.pluralPattern && (
          <p className="pattern-tag">{e.pluralPattern}</p>
        )}
        {e.pluralHint && (
          <p className="example-zh">
            <ArticleText text={e.pluralHint} />
          </p>
        )}
      </>
    )
  } else if (mode === 'verb') {
    prompt = '現在時 ich / du / er 怎麼說？'
    frontExtra = <p className="flash-sub">{word.word}</p>
    backExtra = e.verb ? (
      <>
        <p className="translation">{word.translation}</p>
        <div className="conj-grid mini">
          <div>
            <span>ich</span>
            <strong>{e.verb.present.ich}</strong>
          </div>
          <div>
            <span>du</span>
            <strong>{e.verb.present.du}</strong>
          </div>
          <div>
            <span>er</span>
            <strong>{e.verb.present.er}</strong>
          </div>
        </div>
        <p className="example-zh">
          {e.verb.class} · {e.verb.preterite} / {e.verb.participle}
        </p>
        <p className="panel-note">
          <ArticleText text={e.verb.usage} />
        </p>
      </>
    ) : (
      <p className="translation">{word.translation}</p>
    )
  } else if (mode === 'family') {
    prompt = '有哪些相關詞／字族？'
    frontExtra = (
      <p className="flash-sub">
        <ColoredLemma article={word.article} word={word.word} />
      </p>
    )
    backExtra = (
      <>
        <p className="translation">{word.translation}</p>
        {e.parts?.note && (
          <p className="panel-note">
            <ArticleText text={e.parts.note} />
          </p>
        )}
        <ul className="related-list">
          {e.related.length ? (
            e.related.map((r) => (
              <li key={r.word + r.relation}>
                <span className="related-rel">{r.relation}</span>
                <strong>
                  <ColoredLemma article={r.article} word={r.word} />
                </strong>
                <span className="related-zh">{r.translation}</span>
              </li>
            ))
          ) : (
            <li>此詞暫無內建字族，可看字首字尾拆解。</li>
          )}
        </ul>
      </>
    )
  } else {
    // flash meaning
    frontExtra = (
      <h2 className="lemma">
        {word.article && (
          <span className={genderClass[word.article]}>{word.article}</span>
        )}
        <span className="word">{word.word}</span>
      </h2>
    )
    backExtra = (
      <>
        <p className="translation">{word.translation}</p>
        <p className="example-de">
          <LinkedGermanText
            text={word.example}
            preferLevel={word.level}
            preferId={word.id}
            currentId={word.id}
            onOpenWord={onOpenWord}
          />
        </p>
        <p className="example-zh">
          <ArticleText text={word.exampleTranslation} />
        </p>
      </>
    )
  }

  return (
    <div className={`flash ${revealed ? 'revealed' : ''}`}>
      <NavButtons
        onPrev={onPrev}
        onNext={onNext}
        label={positionLabel}
        onBack={onBack}
      />
      <div className="flash-front">
        <WordBadge article={word.article} />
        <PosLabel type={e.wordType} as="span" />
        <span className={`level-pill level-${word.level}`}>{word.level}</span>
        <p className="flash-prompt">{prompt}</p>
        {mode !== 'flash' ? (
          <h2 className="lemma">
            {word.article && mode !== 'verb' && (
              <span className={genderClass[word.article]}>{word.article}</span>
            )}
            <span className="word">{word.word}</span>
          </h2>
        ) : (
          frontExtra
        )}
        {mode !== 'flash' && frontExtra}
        <SpeakButton label="聽發音" text={lemma} />
      </div>

      {revealed && <div className="flash-back">{backExtra}</div>}

      <div className="flash-actions">
        {!revealed ? (
          <button type="button" className="primary" onClick={onReveal}>
            顯示答案
          </button>
        ) : (
          <>
            <button type="button" className="learned-btn on" onClick={onMark}>
              標記已學會並下一個
            </button>
            <button type="button" className="ghost" onClick={onNext}>
              下一個
            </button>
          </>
        )}
      </div>
    </div>
  )
}

export default function App() {
  const [section, setSection] = useState<Section>('vocab')
  const [query, setQuery] = useState('')
  const [levelFilter, setLevelFilter] = useState<LevelFilter>('A1')
  const [category, setCategory] = useState<Category | '全部'>('全部')
  const [gender, setGender] = useState<'全部' | 'der' | 'die' | 'das' | '無冠詞'>(
    '全部',
  )
  const [wordType, setWordType] = useState<WordTypeFilter>('全部')
  const [selectedId, setSelectedId] = useState(vocabulary[0]?.id ?? '')
  const [mode, setMode] = useState<Mode>('browse')
  const [flashIndex, setFlashIndex] = useState(0)
  const [revealed, setRevealed] = useState(false)
  const [voiceReady, setVoiceReady] = useState(false)
  const [learned, setLearned] = useState<Set<string>>(() => loadLearned())
  const [hideLearned, setHideLearned] = useState(false)
  const [navStack, setNavStack] = useState<NavSnap[]>([])
  const [grammarMounted, setGrammarMounted] = useState(false)
  const [articlesMounted, setArticlesMounted] = useState(false)
  const [affixesMounted, setAffixesMounted] = useState(false)
  const [readingMounted, setReadingMounted] = useState(false)
  const [examMounted, setExamMounted] = useState(false)

  useEffect(() => {
    if (section === 'grammar') setGrammarMounted(true)
    if (section === 'articles') setArticlesMounted(true)
    if (section === 'affixes') setAffixesMounted(true)
    if (section === 'reading') setReadingMounted(true)
    if (section === 'exam') setExamMounted(true)
  }, [section])

  useEffect(() => {
    ensureVoicesLoaded().then(() => setVoiceReady(true))
    return () => stopSpeaking()
  }, [])

  useEffect(() => {
    localStorage.setItem(LEARNED_KEY, JSON.stringify([...learned]))
  }, [learned])

  const progress = useMemo(() => {
    return levels.map((level) => {
      const total = countByLevel(level)
      const done = vocabulary.filter(
        (w) => w.level === level && learned.has(w.id),
      ).length
      return {
        level,
        total,
        done,
        pct: total ? Math.round((done / total) * 100) : 0,
      }
    })
  }, [learned])

  const baseFiltered = useMemo(() => {
    const q = query.trim()
    const pool = vocabulary.filter((w) => {
      if (levelFilter !== '全部' && w.level !== levelFilter) return false
      if (hideLearned && learned.has(w.id)) return false
      if (category !== '全部' && w.category !== category) return false
      if (wordType === '動詞' && w.category !== '動詞') return false
      if (wordType === '形容詞' && w.category !== '形容詞') return false
      if (wordType === '名詞' && !w.article) return false
      if (gender === 'der' || gender === 'die' || gender === 'das') {
        if (w.article !== gender) return false
      } else if (gender === '無冠詞' && w.article !== null) {
        return false
      }
      return true
    })
    return searchVocabulary(pool, q)
  }, [query, category, gender, levelFilter, hideLearned, learned, wordType])

  // Mode-specific pool
  const filtered = useMemo(() => {
    if (mode === 'plural') {
      return baseFiltered.filter((w) => w.article && w.plural)
    }
    if (mode === 'verb') {
      return baseFiltered.filter((w) => w.category === '動詞')
    }
    if (mode === 'family') {
      return baseFiltered.filter((w) => {
        const e = enrich(w)
        return e.related.length > 0 || (e.parts?.prefixes.length ?? 0) > 0
      })
    }
    return baseFiltered
  }, [baseFiltered, mode])

  useEffect(() => {
    if (!filtered.some((w) => w.id === selectedId) && filtered[0]) {
      setSelectedId(filtered[0].id)
    }
  }, [filtered, selectedId])

  useEffect(() => {
    setFlashIndex(0)
    setRevealed(false)
  }, [filtered, mode])

  const selectedIndex = Math.max(
    0,
    filtered.findIndex((w) => w.id === selectedId),
  )
  const selected = filtered[selectedIndex] ?? filtered[0]
  const flashWord = filtered[flashIndex % Math.max(filtered.length, 1)]

  const goBrowse = (delta: number) => {
    if (!filtered.length) return
    stopSpeaking()
    const next =
      (selectedIndex + delta + filtered.length) % filtered.length
    setSelectedId(filtered[next].id)
  }

  const goFlash = (delta: number) => {
    if (!filtered.length) return
    stopSpeaking()
    setRevealed(false)
    setFlashIndex(
      (i) => (i + delta + filtered.length * 10) % filtered.length,
    )
  }

  useEffect(() => {
    if (section !== 'vocab') return
    const onKey = (ev: KeyboardEvent) => {
      const tag = (ev.target as HTMLElement)?.tagName
      if (tag === 'INPUT' || tag === 'SELECT' || tag === 'TEXTAREA') return
      if (ev.key === 'ArrowRight' || ev.key === 'j') {
        ev.preventDefault()
        if (mode === 'browse') goBrowse(1)
        else goFlash(1)
      } else if (ev.key === 'ArrowLeft' || ev.key === 'k') {
        ev.preventDefault()
        if (mode === 'browse') goBrowse(-1)
        else goFlash(-1)
      } else if (ev.key === ' ' && mode !== 'browse') {
        ev.preventDefault()
        setRevealed((r) => !r)
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [section, mode, filtered, selectedIndex, flashIndex])

  const toggleLearned = (id: string) => {
    setLearned((prev) => {
      const next = new Set(prev)
      if (next.has(id)) next.delete(id)
      else next.add(id)
      return next
    })
  }

  const markAndNext = (id: string) => {
    setLearned((prev) => new Set(prev).add(id))
    goFlash(1)
  }

  const clearNavStack = () => setNavStack([])

  const openWordFromLink = (hit: VocabHit) => {
    stopSpeaking()
    setNavStack((prev) => [
      ...prev,
      {
        section,
        mode,
        selectedId,
        levelFilter,
        category,
        wordType,
        gender,
        query,
        hideLearned,
        flashIndex,
      },
    ])
    setSection('vocab')
    setMode('browse')
    setLevelFilter(hit.level)
    setCategory('全部')
    setWordType('全部')
    setGender('全部')
    setQuery('')
    setHideLearned(false)
    setSelectedId(hit.id)
    requestAnimationFrame(() => {
      document.querySelector('.detail')?.scrollIntoView({
        behavior: 'smooth',
        block: 'start',
      })
    })
  }

  const goBackNav = () => {
    if (navStack.length === 0) return
    const snap = navStack[navStack.length - 1]
    setNavStack(navStack.slice(0, -1))
    setSection(snap.section)
    setMode(snap.mode)
    setLevelFilter(snap.levelFilter)
    setCategory(snap.category)
    setWordType(snap.wordType)
    setGender(snap.gender)
    setQuery(snap.query)
    setHideLearned(snap.hideLearned)
    setFlashIndex(snap.flashIndex)
    setSelectedId(snap.selectedId)
    setRevealed(false)
    requestAnimationFrame(() => {
      const target =
        snap.section === 'grammar'
          ? document.querySelector('.grammar-app, .grammar-layout, .layout')
          : document.querySelector('.detail, .flash')
      target?.scrollIntoView({ behavior: 'smooth', block: 'start' })
    })
  }

  const backProp = navStack.length > 0 ? goBackNav : undefined

  return (
    <div className="app">
      <div className="atmosphere" aria-hidden />

      <header className="hero">
        <p className="brand">Wortklang</p>
        <h1>
          {section === 'vocab'
            ? '聽得見的德文單字'
            : section === 'grammar'
              ? '聽得見的德文文法'
              : section === 'affixes'
                ? '字首字根字尾'
                : section === 'reading'
                  ? '分級閱讀'
                  : section === 'exam'
                    ? '德檢模擬測驗'
                    : '冠詞入門'}
        </h1>
        <p className="tagline">
          {section === 'vocab'
            ? '完整 A1→C1：冠詞、複數、字首字根、動詞變化與字族記憶。'
            : section === 'grammar'
              ? '完整 A1→C1 文法：格變、時態、語序、從句、被動與虛擬式。'
              : section === 'affixes'
                ? '可分／不可分字首與常見字尾：每個都有中文意思與例子。'
                : section === 'reading'
                  ? '對齊德檢：練習熱身 → A1／A2／B1／B2 考場長度閱讀，含註解與句型。'
                  : section === 'exam'
                    ? '練習版＋考場版（Goethe 分 Teil）：A1–B2 各多回；聽力 TTS、寫作範文、口說選練。'
                    : 'der／die／das、bin／bist／ist：冠詞與最常用變位一起記。'}
        </p>

        <div
          className="cta-row section-switch"
          role="tablist"
          aria-label="單字、冠詞、字首、閱讀、測驗或文法"
        >
          <button
            type="button"
            role="tab"
            aria-selected={section === 'vocab'}
            className={section === 'vocab' ? 'primary' : 'ghost'}
            onClick={() => {
              stopSpeaking()
              setSection('vocab')
            }}
          >
            單字
          </button>
          <button
            type="button"
            role="tab"
            aria-selected={section === 'articles'}
            className={section === 'articles' ? 'primary' : 'ghost'}
            onClick={() => {
              stopSpeaking()
              setSection('articles')
            }}
          >
            冠詞
          </button>
          <button
            type="button"
            role="tab"
            aria-selected={section === 'affixes'}
            className={section === 'affixes' ? 'primary' : 'ghost'}
            onClick={() => {
              stopSpeaking()
              setSection('affixes')
            }}
          >
            字首
          </button>
          <button
            type="button"
            role="tab"
            aria-selected={section === 'reading'}
            className={section === 'reading' ? 'primary' : 'ghost'}
            onClick={() => {
              stopSpeaking()
              setSection('reading')
            }}
          >
            閱讀
          </button>
          <button
            type="button"
            role="tab"
            aria-selected={section === 'exam'}
            className={section === 'exam' ? 'primary' : 'ghost'}
            onClick={() => {
              stopSpeaking()
              setSection('exam')
            }}
          >
            測驗
          </button>
          <button
            type="button"
            role="tab"
            aria-selected={section === 'grammar'}
            className={section === 'grammar' ? 'primary' : 'ghost'}
            onClick={() => {
              stopSpeaking()
              setSection('grammar')
            }}
          >
            文法
          </button>
        </div>

        {section === 'vocab' && (
          <div className="cta-row modes">
            {(Object.keys(MODE_LABEL) as Mode[]).map((m) => (
              <button
                key={m}
                type="button"
                className={mode === m ? 'primary' : 'ghost'}
                onClick={() => {
                  stopSpeaking()
                  setMode(m)
                  setRevealed(false)
                  if (m === 'plural') {
                    setCategory('全部')
                    setWordType('名詞')
                  }
                  if (m === 'verb') {
                    setCategory('全部')
                    setWordType('動詞')
                  }
                }}
              >
                {MODE_LABEL[m]}
              </button>
            ))}
          </div>
        )}
        <p className="voice-hint">
          快捷鍵：← → 上一個／下一個
          {section === 'vocab' && mode !== 'browse' ? '，空白鍵顯示答案' : ''}
          {!voiceReady ? ' · 語音載入中…' : ''}
        </p>
      </header>

      {grammarMounted && (
        <div hidden={section !== 'grammar'}>
          <GrammarView onOpenWord={openWordFromLink} />
        </div>
      )}
      {articlesMounted && (
        <div hidden={section !== 'articles'}>
          <ArticlesIntro />
        </div>
      )}
      {affixesMounted && (
        <div hidden={section !== 'affixes'}>
          <AffixesIntro />
        </div>
      )}
      {readingMounted && (
        <div hidden={section !== 'reading'}>
          <ReadingView onOpenWord={openWordFromLink} />
        </div>
      )}
      {examMounted && (
        <div hidden={section !== 'exam'}>
          <ExamView />
        </div>
      )}
      {section === 'vocab' && (
      <>
      <section className="level-board" aria-label="等級進度">
        <div className="level-tabs" role="tablist" aria-label="選擇等級">
          {(['A1', 'A2', 'B1', 'B2', 'C1', '全部'] as LevelFilter[]).map(
            (lv) => (
              <button
                key={lv}
                type="button"
                role="tab"
                aria-selected={levelFilter === lv}
                className={`level-tab ${levelFilter === lv ? 'active' : ''}`}
                onClick={() => {
                  stopSpeaking()
                  setLevelFilter(lv)
                }}
              >
                {lv === '全部' ? '全部' : lv}
                {lv !== '全部' && (
                  <span className="tab-count">{countByLevel(lv)}</span>
                )}
              </button>
            ),
          )}
        </div>

        <div className="progress-grid">
          {progress.map(({ level, total, done, pct }) => (
            <div key={level} className="progress-card">
              <div className="progress-head">
                <strong>{level}</strong>
                <span>
                  {done} / {total}（{pct}%）
                </span>
              </div>
              <div
                className="progress-bar"
                role="progressbar"
                aria-valuenow={pct}
                aria-valuemin={0}
                aria-valuemax={100}
              >
                <span style={{ width: `${pct}%` }} />
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="toolbar" aria-label="篩選">
        <label className="search">
          <span className="sr-only">搜尋單字</span>
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="搜單字：Haus、das Haus、房子、wohnen…"
            type="search"
          />
        </label>

        <div className="word-type-tabs" role="tablist" aria-label="詞性">
          {(['全部', '名詞', '動詞', '形容詞'] as WordTypeFilter[]).map((t) => (
            <button
              key={t}
              type="button"
              role="tab"
              aria-selected={wordType === t}
              className={`word-type-tab ${wordType === t ? 'active' : ''} ${t !== '全部' ? `tab-${t}` : ''}`}
              onClick={() => {
                stopSpeaking()
                setWordType(t)
                if (t === '動詞') setCategory('全部')
              }}
            >
              {t === '全部' ? '全部詞性' : t}
            </button>
          ))}
        </div>

        <div className="filters">
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value as Category | '全部')}
            aria-label="分類"
          >
            <option value="全部">全部分類</option>
            {categories.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>

          <select
            value={gender}
            onChange={(e) =>
              setGender(
                e.target.value as '全部' | 'der' | 'die' | 'das' | '無冠詞',
              )
            }
            aria-label="冠詞"
          >
            <option value="全部">全部冠詞</option>
            <option value="der">der（陽性）</option>
            <option value="die">die（陰性）</option>
            <option value="das">das（中性）</option>
            <option value="無冠詞">無冠詞</option>
          </select>
        </div>

        <div className="toolbar-foot">
          <label className="check">
            <input
              type="checkbox"
              checked={hideLearned}
              onChange={(e) => setHideLearned(e.target.checked)}
            />
            隱藏已學會
          </label>
          <p className="count">
            {MODE_LABEL[mode]} · {filtered.length} 個
          </p>
        </div>
      </section>

      {mode === 'browse' && selected && (
        <main className="layout">
          <aside className="word-list" aria-label="單字列表">
            {filtered.map((w) => {
              const active = w.id === selected.id
              const isLearned = learned.has(w.id)
              return (
                <button
                  key={w.id}
                  type="button"
                  className={`word-row ${active ? 'active' : ''} ${isLearned ? 'learned' : ''}`}
                  onClick={() => {
                    stopSpeaking()
                    clearNavStack()
                    setSelectedId(w.id)
                  }}
                >
                  <WordBadge article={w.article} />
                  <span className="row-word">
                    {w.word}
                    {isLearned ? ' ✓' : ''}
                  </span>
                  <span className="row-zh">
                    <PosLabel
                      type={
                        w.category === '動詞'
                          ? '動詞'
                          : w.category === '形容詞'
                            ? '形容詞'
                            : w.article
                              ? '名詞'
                              : '其他'
                      }
                    />{' '}
                    · {w.translation} · {w.level}
                  </span>
                </button>
              )
            })}
            {!filtered.length && (
              <p className="empty">找不到符合的單字。</p>
            )}
          </aside>
          <WordDetail
            word={selected}
            learned={learned.has(selected.id)}
            onToggleLearned={() => toggleLearned(selected.id)}
            onPrev={() => goBrowse(-1)}
            onNext={() => goBrowse(1)}
            positionLabel={`${selectedIndex + 1} / ${filtered.length}`}
            onOpenWord={openWordFromLink}
            onBack={backProp}
          />
        </main>
      )}

      {mode !== 'browse' && (
        <main className="flash-wrap">
          {filtered.length && flashWord ? (
            <PracticeCard
              mode={mode}
              word={flashWord}
              revealed={revealed}
              onReveal={() => setRevealed(true)}
              onPrev={() => goFlash(-1)}
              onNext={() => goFlash(1)}
              onMark={() => markAndNext(flashWord.id)}
              positionLabel={`${(flashIndex % filtered.length) + 1} / ${filtered.length}`}
              onOpenWord={openWordFromLink}
              onBack={backProp}
            />
          ) : (
            <p className="empty">
              這個練習模式目前沒有符合條件的單字，試試切換等級或分類。
            </p>
          )}
        </main>
      )}
      </>
      )}

      <footer className="footer">
        <p>
          {section === 'grammar'
            ? '文法依 CEFR 分級：先掌握規則與例句，再標記已學會。建議 Chrome／Edge 聽發音。'
            : section === 'articles'
              ? '冠詞與 sein／haben 入門：定冠詞、格變，以及 bin／bist／ist。建議 Chrome／Edge 聽發音。'
              : section === 'affixes'
                ? '字首字根字尾：可分／不可分與常見字尾都有中文意思。建議 Chrome／Edge 聽發音。'
                : section === 'reading'
                  ? '分級閱讀（德檢取向）：練習＋A1～B2 各 70 篇。點德文可跳單字。'
                  : section === 'exam'
                    ? '德檢模擬：練習版綜合卷＋考場版分 Teil。建議 Chrome／Edge 聽聽力腳本。'
                    : '複數可對照英文 +s／+es／不規則；動詞看三態與現在時；相關詞幫你串字族。建議 Chrome／Edge 聽發音。'}
        </p>
      </footer>
    </div>
  )
}
