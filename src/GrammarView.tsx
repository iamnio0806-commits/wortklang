import { useEffect, useMemo, useState } from 'react'
import {
  checkFillAnswer,
  countGrammarByLevel,
  grammarCategories,
  grammarLevels,
  grammarTopics,
  type GrammarExercise,
  type GrammarFill,
  type GrammarLevel,
  type GrammarMcq,
  type GrammarTopic,
} from './data/grammar'
import { RichText } from './lib/richText'
import { LinkedGermanText } from './lib/LinkedGermanText'
import type { VocabHit } from './lib/vocabIndex'
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
              <th key={h}>
                <RichText text={h} />
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, i) => (
            <tr key={`${label}-${i}`}>
              {row.map((cell, j) => (
                <td key={`${i}-${j}`}>
                  <RichText text={cell} />
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function QuizPanel({
  topic,
  onPass,
}: {
  topic: GrammarTopic
  onPass: () => void
}) {
  const exercises = topic.exercises ?? []
  const [answers, setAnswers] = useState<Record<string, string>>({})
  const [showHint, setShowHint] = useState<Record<string, boolean>>({})
  const [checked, setChecked] = useState(false)
  const [results, setResults] = useState<Record<string, boolean>>({})

  useEffect(() => {
    setAnswers({})
    setShowHint({})
    setChecked(false)
    setResults({})
  }, [topic.id])

  const mcqs = exercises.filter((e): e is GrammarMcq => e.type === 'mcq')
  const fills = exercises.filter((e): e is GrammarFill => e.type === 'fill')
  const beginner = topic.level === 'A1' || topic.level === 'A2'

  const score = useMemo(() => {
    const vals = Object.values(results)
    if (!vals.length) return null
    const ok = vals.filter(Boolean).length
    return { ok, total: vals.length }
  }, [results])

  const grade = () => {
    const next: Record<string, boolean> = {}
    for (const ex of exercises) {
      const raw = answers[ex.id] ?? ''
      if (ex.type === 'mcq') {
        next[ex.id] = raw === ex.answer
      } else {
        next[ex.id] = checkFillAnswer(ex, raw)
      }
    }
    setResults(next)
    setChecked(true)
    const ok = Object.values(next).filter(Boolean).length
    if (ok === exercises.length && exercises.length > 0) onPass()
  }

  if (!exercises.length) return null

  return (
    <section className="grammar-section quiz-panel" aria-label="確認學會">
      <h3>確認學會</h3>
      <p className="quiz-lead">
        {beginner
          ? '初學者：先做選擇題再做填空；不會就按「提示」。全對會自動標記已學會。'
          : '每單元含選擇題與填空題。全對會自動標記已學會。'}
      </p>

      <div className="quiz-block">
        <h4>選擇題（{mcqs.length}）</h4>
        {mcqs.map((ex, i) => (
          <ExerciseCard
            key={ex.id}
            index={i + 1}
            exercise={ex}
            value={answers[ex.id] ?? ''}
            showHint={!!showHint[ex.id] || beginner}
            forcedHint={beginner && !checked}
            checked={checked}
            correct={results[ex.id]}
            onChange={(v) =>
              setAnswers((prev) => ({ ...prev, [ex.id]: v }))
            }
            onToggleHint={() =>
              setShowHint((prev) => ({ ...prev, [ex.id]: !prev[ex.id] }))
            }
          />
        ))}
      </div>

      <div className="quiz-block">
        <h4>填空題（{fills.length}）</h4>
        {fills.map((ex, i) => (
          <ExerciseCard
            key={ex.id}
            index={i + 1}
            exercise={ex}
            value={answers[ex.id] ?? ''}
            showHint={!!showHint[ex.id] || (beginner && !checked)}
            forcedHint={false}
            checked={checked}
            correct={results[ex.id]}
            onChange={(v) =>
              setAnswers((prev) => ({ ...prev, [ex.id]: v }))
            }
            onToggleHint={() =>
              setShowHint((prev) => ({ ...prev, [ex.id]: !prev[ex.id] }))
            }
          />
        ))}
      </div>

      <div className="quiz-actions">
        <button type="button" className="primary" onClick={grade}>
          {checked ? '再檢查一次' : '提交答案'}
        </button>
        {checked && score && (
          <p
            className={`quiz-score ${score.ok === score.total ? 'pass' : 'fail'}`}
          >
            {score.ok === score.total
              ? `全對 ${score.ok}/${score.total}！已標記為學會。`
              : `目前 ${score.ok}/${score.total} 題正確，看看提示再試一次。`}
          </p>
        )}
      </div>
    </section>
  )
}

function ExerciseCard({
  index,
  exercise,
  value,
  showHint,
  forcedHint,
  checked,
  correct,
  onChange,
  onToggleHint,
}: {
  index: number
  exercise: GrammarExercise
  value: string
  showHint: boolean
  forcedHint: boolean
  checked: boolean
  correct?: boolean
  onChange: (v: string) => void
  onToggleHint: () => void
}) {
  const status =
    checked && correct !== undefined ? (correct ? 'ok' : 'bad') : ''

  return (
    <div className={`exercise-card ${status}`}>
      <p className="exercise-prompt">
        <span className="exercise-num">{index}.</span>{' '}
        <RichText text={exercise.prompt} />
      </p>

      {exercise.type === 'mcq' ? (
        <div className="exercise-options" role="radiogroup">
          {exercise.options.map((opt) => (
            <label key={opt} className="exercise-option">
              <input
                type="radio"
                name={exercise.id}
                checked={value === opt}
                onChange={() => onChange(opt)}
              />
              <span>
                <RichText text={opt} />
              </span>
            </label>
          ))}
        </div>
      ) : (
        <input
          className="exercise-fill"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder="在這裡填空…"
          autoComplete="off"
          spellCheck={false}
        />
      )}

      <div className="exercise-foot">
        {!forcedHint && (
          <button type="button" className="ghost hint-btn" onClick={onToggleHint}>
            {showHint ? '隱藏提示' : '提示'}
          </button>
        )}
        {(showHint || forcedHint) && (
          <p className="exercise-hint">
            <RichText text={exercise.hint} />
          </p>
        )}
        {checked && correct === false && exercise.type === 'fill' && (
          <p className="exercise-answer">
            參考答案：<RichText text={exercise.answer} />
          </p>
        )}
        {checked && correct === false && exercise.type === 'mcq' && (
          <p className="exercise-answer">
            正確選項：<RichText text={exercise.answer} />
          </p>
        )}
      </div>
    </div>
  )
}

function TopicDetail({
  topic,
  learned,
  onToggleLearned,
  onMarkLearned,
  onPrev,
  onNext,
  positionLabel,
  onOpenRelated,
  onOpenWord,
}: {
  topic: GrammarTopic
  learned: boolean
  onToggleLearned: () => void
  onMarkLearned: () => void
  onPrev: () => void
  onNext: () => void
  positionLabel: string
  onOpenRelated: (id: string) => void
  onOpenWord: (hit: VocabHit) => void
}) {
  const relatedTopics = topic.related
    .map((id) => grammarTopics.find((t) => t.id === id))
    .filter(Boolean) as GrammarTopic[]
  const beginner = topic.level === 'A1' || topic.level === 'A2'

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
      <p className="grammar-summary">
        <RichText text={topic.summary} />
      </p>

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

      <section className={`grammar-section tips ${beginner ? 'beginner' : ''}`}>
        <h3>{beginner ? '初學者提示' : '記憶提示'}</h3>
        <ul className="grammar-points">
          {topic.tips.map((t) => (
            <li key={t}>
              <RichText text={t} />
            </li>
          ))}
        </ul>
      </section>

      <section className="grammar-section">
        <h3>重點</h3>
        <ul className="grammar-points">
          {topic.points.map((p) => (
            <li key={p}>
              <RichText text={p} />
            </li>
          ))}
        </ul>
      </section>

      {topic.forms.map((form) => (
        <FormTable key={form.label} {...form} />
      ))}

      <section className="grammar-section">
        <h3>例句</h3>
        <p className="example-hint">點德文詞可跳到單字頁</p>
        <ul className="grammar-examples">
          {topic.examples.map((ex) => (
            <li key={ex.de}>
              <div className="ex-row">
                <p className="ex-de">
                  <LinkedGermanText
                    text={ex.de}
                    preferLevel={topic.level}
                    onOpenWord={onOpenWord}
                  />
                </p>
                <SpeakButton label="聽例句" text={ex.de} />
              </div>
              <p className="ex-zh">
                <RichText text={ex.zh} />
              </p>
            </li>
          ))}
        </ul>
      </section>

      <QuizPanel topic={topic} onPass={onMarkLearned} />

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

export default function GrammarView({
  onOpenWord,
}: {
  onOpenWord: (hit: VocabHit) => void
}) {
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
        ...t.tips,
        ...t.examples.map((e) => `${e.de} ${e.zh}`),
        ...t.exercises.map((e) => e.prompt),
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

  const markLearned = (id: string) => {
    setLearned((prev) => new Set(prev).add(id))
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
            onMarkLearned={() => markLearned(selected.id)}
            onPrev={() => go(-1)}
            onNext={() => go(1)}
            positionLabel={`${selectedIndex + 1} / ${filtered.length}`}
            onOpenWord={onOpenWord}
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
