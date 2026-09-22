import { useEffect, useMemo, useState } from 'react'
import {
  countGrammarByLevel,
  grammarCategories,
  grammarLevels,
  grammarTopics,
  type GrammarLevel,
  type GrammarTopic,
} from './data/grammar'
import { speakGerman, stopSpeaking } from './lib/speech'

type LevelFilter = GrammarLevel | '全部'

const LEARNED_KEY = 'wortklang-grammar-learned'

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

function SpeakButton({ label, text }: { label: string; text: string }) {
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

function FormTable({
  label,
  headers,
  rows,
}: {
  label: string
  headers: string[]
  rows: string[][]
}) {
  return (
    <div className="grammar-table-wrap">
      <h4>{label}</h4>
      <table className="grammar-table">
        <thead>
          <tr>
            {headers.map((h) => (
              <th key={h}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, i) => (
            <tr key={`${label}-${i}`}>
              {row.map((cell, j) => (
                <td key={`${i}-${j}`}>{cell}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function TopicDetail({
  topic,
  learned,
  onToggleLearned,
  onPrev,
  onNext,
  positionLabel,
  onOpenRelated,
}: {
  topic: GrammarTopic
  learned: boolean
  onToggleLearned: () => void
  onPrev: () => void
  onNext: () => void
  positionLabel: string
  onOpenRelated: (id: string) => void
}) {
  const relatedTopics = topic.related
    .map((id) => grammarTopics.find((t) => t.id === id))
    .filter(Boolean) as GrammarTopic[]

  return (
    <article className="detail grammar-detail">
      <div className="detail-top">
        <div className="detail-nav">
          <button type="button" className="ghost" onClick={onPrev}>
            ← 上一個
          </button>
          <span className="pos">{positionLabel}</span>
          <button type="button" className="ghost" onClick={onNext}>
            下一個 →
          </button>
        </div>
        <span className={`level-pill level-${topic.level}`}>{topic.level}</span>
      </div>

      <p className="grammar-cat">{topic.category}</p>
      <h2 className="grammar-title">{topic.title}</h2>
      <p className="grammar-title-de">{topic.titleDe}</p>
      <p className="grammar-summary">{topic.summary}</p>

      <div className="detail-actions">
        <SpeakButton label="聽標題" text={topic.titleDe} />
        <button
          type="button"
          className={`learned-btn ${learned ? 'on' : ''}`}
          onClick={onToggleLearned}
        >
          {learned ? '已學會 ✓' : '標記已學會'}
        </button>
      </div>

      <section className="grammar-section">
        <h3>重點</h3>
        <ul className="grammar-points">
          {topic.points.map((p) => (
            <li key={p}>{p}</li>
          ))}
        </ul>
      </section>

      {topic.forms.map((form) => (
        <FormTable key={form.label} {...form} />
      ))}

      <section className="grammar-section">
        <h3>例句</h3>
        <ul className="grammar-examples">
          {topic.examples.map((ex) => (
            <li key={ex.de}>
              <div className="ex-row">
                <p className="ex-de">{ex.de}</p>
                <SpeakButton label="聽例句" text={ex.de} />
              </div>
              <p className="ex-zh">{ex.zh}</p>
            </li>
          ))}
        </ul>
      </section>

      {topic.tips.length > 0 && (
        <section className="grammar-section tips">
          <h3>記憶提示</h3>
          <ul className="grammar-points">
            {topic.tips.map((t) => (
              <li key={t}>{t}</li>
            ))}
          </ul>
        </section>
      )}

      {relatedTopics.length > 0 && (
        <section className="grammar-section">
          <h3>相關主題</h3>
          <div className="related-topics">
            {relatedTopics.map((r) => (
              <button
                key={r.id}
                type="button"
                className="related-chip"
                onClick={() => onOpenRelated(r.id)}
              >
                {r.level} · {r.title}
              </button>
            ))}
          </div>
        </section>
      )}
    </article>
  )
}

export default function GrammarView() {
  const [levelFilter, setLevelFilter] = useState<LevelFilter>('A1')
  const [category, setCategory] = useState<string>('全部')
  const [query, setQuery] = useState('')
  const [selectedId, setSelectedId] = useState(grammarTopics[0]?.id ?? '')
  const [learned, setLearned] = useState<Set<string>>(() => loadLearned())
  const [hideLearned, setHideLearned] = useState(false)

  useEffect(() => {
    localStorage.setItem(LEARNED_KEY, JSON.stringify([...learned]))
  }, [learned])

  const progress = useMemo(() => {
    return grammarLevels.map((level) => {
      const total = countGrammarByLevel(level)
      const done = grammarTopics.filter(
        (t) => t.level === level && learned.has(t.id),
      ).length
      return {
        level,
        total,
        done,
        pct: total ? Math.round((done / total) * 100) : 0,
      }
    })
  }, [learned])

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase()
    return grammarTopics.filter((t) => {
      if (levelFilter !== '全部' && t.level !== levelFilter) return false
      if (category !== '全部' && t.category !== category) return false
      if (hideLearned && learned.has(t.id)) return false
      if (!q) return true
      const hay = [
        t.title,
        t.titleDe,
        t.summary,
        t.category,
        t.level,
        ...t.points,
        ...t.examples.map((e) => `${e.de} ${e.zh}`),
      ]
        .join(' ')
        .toLowerCase()
      return hay.includes(q)
    })
  }, [levelFilter, category, query, hideLearned, learned])

  useEffect(() => {
    if (!filtered.some((t) => t.id === selectedId) && filtered[0]) {
      setSelectedId(filtered[0].id)
    }
  }, [filtered, selectedId])

  const selectedIndex = Math.max(
    0,
    filtered.findIndex((t) => t.id === selectedId),
  )
  const selected = filtered[selectedIndex] ?? filtered[0]

  const go = (delta: number) => {
    if (!filtered.length) return
    stopSpeaking()
    const next = (selectedIndex + delta + filtered.length) % filtered.length
    setSelectedId(filtered[next].id)
  }

  useEffect(() => {
    const onKey = (ev: KeyboardEvent) => {
      const tag = (ev.target as HTMLElement)?.tagName
      if (tag === 'INPUT' || tag === 'SELECT' || tag === 'TEXTAREA') return
      if (ev.key === 'ArrowRight' || ev.key === 'j') {
        ev.preventDefault()
        go(1)
      } else if (ev.key === 'ArrowLeft' || ev.key === 'k') {
        ev.preventDefault()
        go(-1)
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filtered, selectedIndex])

  const toggleLearned = (id: string) => {
    setLearned((prev) => {
      const next = new Set(prev)
      if (next.has(id)) next.delete(id)
      else next.add(id)
      return next
    })
  }

  return (
    <>
      <section className="level-board" aria-label="文法等級進度">
        <div className="level-tabs" role="tablist" aria-label="選擇文法等級">
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
                {lv}
                {lv !== '全部' && (
                  <span className="tab-count">{countGrammarByLevel(lv)}</span>
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

      <section className="toolbar" aria-label="文法篩選">
        <label className="search">
          <span className="sr-only">搜尋文法</span>
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="搜尋文法主題、規則或例句…"
            type="search"
          />
        </label>

        <div className="filters">
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            aria-label="文法分類"
          >
            <option value="全部">全部分類</option>
            {grammarCategories.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
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
          <p className="count">文法主題 · {filtered.length} 個</p>
        </div>
      </section>

      {selected ? (
        <main className="layout">
          <aside className="word-list" aria-label="文法主題列表">
            {filtered.map((t) => {
              const active = t.id === selected.id
              const isLearned = learned.has(t.id)
              return (
                <button
                  key={t.id}
                  type="button"
                  className={`word-row ${active ? 'active' : ''} ${isLearned ? 'learned' : ''}`}
                  onClick={() => {
                    stopSpeaking()
                    setSelectedId(t.id)
                  }}
                >
                  <span className={`badge level-pill level-${t.level}`}>
                    {t.level}
                  </span>
                  <span className="row-word">
                    {t.title}
                    {isLearned ? ' ✓' : ''}
                  </span>
                  <span className="row-zh">
                    {t.category} · {t.titleDe}
                  </span>
                </button>
              )
            })}
            {!filtered.length && <p className="empty">找不到符合的文法主題。</p>}
          </aside>

          <TopicDetail
            topic={selected}
            learned={learned.has(selected.id)}
            onToggleLearned={() => toggleLearned(selected.id)}
            onPrev={() => go(-1)}
            onNext={() => go(1)}
            positionLabel={`${selectedIndex + 1} / ${filtered.length}`}
            onOpenRelated={(id) => {
              stopSpeaking()
              const topic = grammarTopics.find((t) => t.id === id)
              if (!topic) return
              setLevelFilter('全部')
              setCategory('全部')
              setSelectedId(id)
            }}
          />
        </main>
      ) : (
        <p className="empty">目前沒有文法主題。</p>
      )}
    </>
  )
}
