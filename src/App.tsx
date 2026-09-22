import { useEffect, useMemo, useState } from 'react'
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
import { ensureVoicesLoaded, speakGerman, stopSpeaking } from './lib/speech'
import './App.css'

type Mode = 'browse' | 'flash'
type LevelFilter = Level | '全部'

const LEARNED_KEY = 'wortklang-learned'

const genderClass: Record<NonNullable<Gender>, string> = {
  der: 'gender-der',
  die: 'gender-die',
  das: 'gender-das',
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
  if (!article) {
    return <span className="badge badge-neutral">無冠詞</span>
  }
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

function WordDetail({
  word,
  learned,
  onToggleLearned,
}: {
  word: VocabWord
  learned: boolean
  onToggleLearned: () => void
}) {
  const lemma = word.article ? `${word.article} ${word.word}` : word.word

  return (
    <article className="detail" key={word.id}>
      <div className="detail-top">
        <WordBadge article={word.article} />
        <span className={`level-pill level-${word.level}`}>{word.level}</span>
      </div>

      <h2 className="lemma">
        {word.article && <span className="article">{word.article}</span>}
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
            <dd>die {word.plural}</dd>
          </>
        )}
        <dt>等級</dt>
        <dd>{word.level}</dd>
        <dt>分類</dt>
        <dd>{word.category}</dd>
      </dl>

      <div className="speak-row">
        <SpeakButton label="聽單字" text={lemma} />
        <SpeakButton label="慢速" text={lemma} slow />
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
        <p className="example-de">{word.example}</p>
        <p className="example-zh">{word.exampleTranslation}</p>
        <div className="speak-row">
          <SpeakButton label="聽例句" text={word.example} />
          <SpeakButton label="慢速例句" text={word.example} slow />
        </div>
      </section>
    </article>
  )
}

function FlashCard({
  word,
  revealed,
  onReveal,
  onNext,
  onMarkLearned,
}: {
  word: VocabWord
  revealed: boolean
  onReveal: () => void
  onNext: () => void
  onMarkLearned: () => void
}) {
  const lemma = word.article ? `${word.article} ${word.word}` : word.word

  return (
    <div className={`flash ${revealed ? 'revealed' : ''}`}>
      <div className="flash-front">
        <WordBadge article={word.article} />
        <span className={`level-pill level-${word.level}`}>{word.level}</span>
        <p className="flash-prompt">這是什麼意思？</p>
        <h2 className="lemma">
          {word.article && <span className="article">{word.article}</span>}
          <span className="word">{word.word}</span>
        </h2>
        <SpeakButton label="聽發音" text={lemma} />
      </div>

      {revealed && (
        <div className="flash-back">
          <p className="translation">{word.translation}</p>
          <p className="example-de">{word.example}</p>
          <p className="example-zh">{word.exampleTranslation}</p>
          <SpeakButton label="聽例句" text={word.example} />
        </div>
      )}

      <div className="flash-actions">
        {!revealed ? (
          <button type="button" className="primary" onClick={onReveal}>
            顯示意思
          </button>
        ) : (
          <>
            <button type="button" className="learned-btn on" onClick={onMarkLearned}>
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
  const [query, setQuery] = useState('')
  const [levelFilter, setLevelFilter] = useState<LevelFilter>('A1')
  const [category, setCategory] = useState<Category | '全部'>('全部')
  const [gender, setGender] = useState<'全部' | 'der' | 'die' | 'das' | '無冠詞'>(
    '全部',
  )
  const [selectedId, setSelectedId] = useState(vocabulary[0]?.id ?? '')
  const [mode, setMode] = useState<Mode>('browse')
  const [flashIndex, setFlashIndex] = useState(0)
  const [revealed, setRevealed] = useState(false)
  const [voiceReady, setVoiceReady] = useState(false)
  const [learned, setLearned] = useState<Set<string>>(() => loadLearned())
  const [hideLearned, setHideLearned] = useState(false)

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
      return { level, total, done, pct: total ? Math.round((done / total) * 100) : 0 }
    })
  }, [learned])

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase()
    return vocabulary.filter((w) => {
      if (levelFilter !== '全部' && w.level !== levelFilter) return false
      if (hideLearned && learned.has(w.id)) return false
      if (category !== '全部' && w.category !== category) return false
      if (gender === 'der' || gender === 'die' || gender === 'das') {
        if (w.article !== gender) return false
      } else if (gender === '無冠詞' && w.article !== null) {
        return false
      }
      if (!q) return true
      const hay = [
        w.word,
        w.article ?? '',
        w.translation,
        w.example,
        w.exampleTranslation,
        w.plural ?? '',
        w.level,
      ]
        .join(' ')
        .toLowerCase()
      return hay.includes(q)
    })
  }, [query, category, gender, levelFilter, hideLearned, learned])

  useEffect(() => {
    if (!filtered.some((w) => w.id === selectedId) && filtered[0]) {
      setSelectedId(filtered[0].id)
    }
  }, [filtered, selectedId])

  useEffect(() => {
    setFlashIndex(0)
    setRevealed(false)
  }, [filtered])

  const selected = filtered.find((w) => w.id === selectedId) ?? filtered[0]
  const flashWord = filtered[flashIndex % Math.max(filtered.length, 1)]

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
    stopSpeaking()
    setRevealed(false)
    setFlashIndex((i) => i + 1)
  }

  return (
    <div className="app">
      <div className="atmosphere" aria-hidden />

      <header className="hero">
        <p className="brand">Wortklang</p>
        <h1>聽得見的德文單字</h1>
        <p className="tagline">
          850+ 個 A1／A2 單字：冠詞、例句、發音，依等級一步步學完。
        </p>
        <div className="cta-row">
          <button
            type="button"
            className={mode === 'browse' ? 'primary' : 'ghost'}
            onClick={() => {
              stopSpeaking()
              setMode('browse')
            }}
          >
            單字瀏覽
          </button>
          <button
            type="button"
            className={mode === 'flash' ? 'primary' : 'ghost'}
            onClick={() => {
              stopSpeaking()
              setMode('flash')
              setRevealed(false)
            }}
          >
            閃卡練習
          </button>
        </div>
        {!voiceReady && <p className="voice-hint">正在載入語音引擎…</p>}
      </header>

      <section className="level-board" aria-label="等級進度">
        <div className="level-tabs" role="tablist" aria-label="選擇等級">
          {(['A1', 'A2', '全部'] as LevelFilter[]).map((lv) => (
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
          ))}
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
                aria-label={`${level} 進度`}
              >
                <span style={{ width: `${pct}%` }} />
              </div>
              {pct === 100 && <p className="done-note">{level} 已完成！</p>}
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
            placeholder="搜尋德文、中文或例句…"
            type="search"
          />
        </label>

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
            {levelFilter === '全部' ? '全部' : levelFilter} · {filtered.length}{' '}
            個單字
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
                    setSelectedId(w.id)
                  }}
                >
                  <WordBadge article={w.article} />
                  <span className="row-word">
                    {w.word}
                    {isLearned ? ' ✓' : ''}
                  </span>
                  <span className="row-zh">
                    {w.translation} · {w.level}
                  </span>
                </button>
              )
            })}
            {!filtered.length && (
              <p className="empty">
                {hideLearned
                  ? '這個等級的單字都學會了！可以取消「隱藏已學會」或切換等級。'
                  : '找不到符合的單字，試試其他關鍵字。'}
              </p>
            )}
          </aside>
          <WordDetail
            word={selected}
            learned={learned.has(selected.id)}
            onToggleLearned={() => toggleLearned(selected.id)}
          />
        </main>
      )}

      {mode === 'flash' && (
        <main className="flash-wrap">
          <p className="flash-progress">
            {filtered.length
              ? `${(flashIndex % filtered.length) + 1} / ${filtered.length} · ${levelFilter}`
              : '0 / 0'}
          </p>
          {filtered.length && flashWord ? (
            <FlashCard
              word={flashWord}
              revealed={revealed}
              onReveal={() => setRevealed(true)}
              onNext={() => {
                stopSpeaking()
                setRevealed(false)
                setFlashIndex((i) => i + 1)
              }}
              onMarkLearned={() => markAndNext(flashWord.id)}
            />
          ) : (
            <p className="empty">
              {hideLearned
                ? '這個篩選條件下沒有未學會的單字了。'
                : '沒有可練習的單字。'}
            </p>
          )}
        </main>
      )}

      <footer className="footer">
        <p>
          建議先完成 A1，再進入 A2。發音使用瀏覽器德文語音（de-DE），Chrome /
          Edge 效果較佳。
        </p>
      </footer>
    </div>
  )
}
