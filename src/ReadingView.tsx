import { useEffect, useMemo, useState } from 'react'
import {
  countReadingByLevel,
  READING_KIND_LABEL,
  readingItems,
  readingLevels,
  readingNote,
  readingPreferVocabLevel,
  readingTopicsFor,
  type ReadingItem,
  type ReadingKind,
  type ReadingLevel,
} from './data/reading'
import { LinkedGermanText } from './lib/LinkedGermanText'
import type { VocabHit } from './lib/vocabIndex'
import { scoreTextFields } from './lib/search'
import { stopSpeaking } from './lib/speech'
import { SpeakPair } from './lib/SpeakControls'
import { ArticleText } from './lib/richText'

type LevelFilter = ReadingLevel | '全部'

const LEARNED_KEY = 'wortklang-reading-learned'

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

function ReadingDetail({
  item,
  learned,
  onToggle,
  onOpenWord,
  onPrev,
  onNext,
  positionLabel,
}: {
  item: ReadingItem
  learned: boolean
  onToggle: () => void
  onOpenWord: (hit: VocabHit) => void
  onPrev: () => void
  onNext: () => void
  positionLabel: string
}) {
  const [showZh, setShowZh] = useState(false)

  useEffect(() => {
    setShowZh(false)
  }, [item.id])

  return (
    <article className="detail reading-detail" key={item.id}>
      <div className="nav-block">
        <div className="nav-row">
          <button type="button" className="ghost nav-btn" onClick={onPrev}>
            ← 上一篇
          </button>
          <span className="nav-label">{positionLabel}</span>
          <button type="button" className="ghost nav-btn" onClick={onNext}>
            下一篇 →
          </button>
        </div>
      </div>

      <div className="detail-top">
        <span className={`level-pill level-${item.level}`}>{item.level}</span>
        <span className="type-pill">{READING_KIND_LABEL[item.kind]}</span>
        <span className="type-pill">{item.topic}</span>
      </div>

      <h2 className="grammar-title">{item.title}</h2>
      <p className="grammar-title-de">{item.titleZh}</p>

      <div className="focus-row" aria-label="重點">
        {item.focus.map((f) => (
          <span key={f} className="chip chip-root">
            {f}
          </span>
        ))}
      </div>

      <section className="grammar-section reading-text-panel">
        <div className="reading-toolbar">
          <h3>德文</h3>
          <div className="speak-row">
            <SpeakPair
              text={item.text}
              normalLabel="聽全文"
              slowLabel="慢速全文"
              normalizeNewlines
            />
            <button
              type="button"
              className="ghost"
              onClick={() => setShowZh((v) => !v)}
            >
              {showZh ? '隱藏中文' : '顯示中文'}
            </button>
          </div>
        </div>
        <div className="reading-de">
          {item.text.split('\n').map((line, i) => (
            <p key={`${item.id}-l-${i}`} className="reading-line">
              {line ? (
                <LinkedGermanText
                  text={line}
                  preferLevel={readingPreferVocabLevel(item.level)}
                  onOpenWord={onOpenWord}
                />
              ) : (
                <br />
              )}
            </p>
          ))}
        </div>
        {showZh && (
          <div className="reading-zh">
            {item.textZh.split('\n').map((line, i) => (
              <p key={`${item.id}-z-${i}`}>{line || '\u00a0'}</p>
            ))}
          </div>
        )}
      </section>

      <section className="grammar-section">
        <h3>註解</h3>
        <ul className="reading-notes">
          {item.notes.map((note) => (
            <li key={note.span + note.zh}>
              <div className="speak-row reading-note-speak">
                <SpeakPair
                  text={note.span}
                  normalLabel={note.span}
                  slowLabel="慢速"
                />
              </div>
              <span className="reading-note-zh">{note.zh}</span>
              {note.tip && <p className="reading-note-tip">{note.tip}</p>}
            </li>
          ))}
        </ul>
      </section>

      <section className="grammar-section">
        <h3>句型／用法</h3>
        <ul className="reading-patterns">
          {item.patterns.map((pat) => (
            <li key={pat.pattern}>
              <p className="reading-pat-de">{pat.pattern}</p>
              <p className="reading-pat-zh">{pat.zh}</p>
              <p className="reading-pat-ex">
                例：
                <LinkedGermanText
                  text={pat.example}
                  preferLevel={readingPreferVocabLevel(item.level)}
                  onOpenWord={onOpenWord}
                />
              </p>
            </li>
          ))}
        </ul>
      </section>

      <section className={`grammar-section tips ${item.level === '練習' || item.level === 'A1' ? 'beginner' : ''}`}>
        <h3>學習引導</h3>
        <ul className="grammar-points">
          {item.tips.map((tip) => (
            <li key={tip}>
              <ArticleText text={tip} />
            </li>
          ))}
        </ul>
      </section>

      <div className="speak-row">
        <button
          type="button"
          className={learned ? 'learned-btn on' : 'learned-btn'}
          onClick={onToggle}
        >
          {learned ? '已讀完 ✓' : '標記已讀完'}
        </button>
      </div>
    </article>
  )
}

export default function ReadingView({
  onOpenWord,
  focusId,
}: {
  onOpenWord: (hit: VocabHit) => void
  focusId?: string
}) {
  const [levelFilter, setLevelFilter] = useState<LevelFilter>('練習')
  const [topic, setTopic] = useState('全部')
  const [kind, setKind] = useState<ReadingKind | '全部'>('全部')
  const [query, setQuery] = useState('')
  const [selectedId, setSelectedId] = useState(readingItems[0]?.id ?? '')
  const [learned, setLearned] = useState<Set<string>>(() => loadLearned())
  const [hideLearned, setHideLearned] = useState(false)

  useEffect(() => {
    localStorage.setItem(LEARNED_KEY, JSON.stringify([...learned]))
  }, [learned])

  useEffect(() => {
    if (!focusId) return
    const id = focusId.split('#')[0]
    const item = readingItems.find((i) => i.id === id)
    if (!item) return
    setLevelFilter(item.level)
    setTopic('全部')
    setKind('全部')
    setQuery('')
    setHideLearned(false)
    setSelectedId(id)
    requestAnimationFrame(() => {
      document.querySelector('.reading-detail, .detail')?.scrollIntoView({
        behavior: 'smooth',
        block: 'start',
      })
    })
  }, [focusId])

  const topics = useMemo(() => readingTopicsFor(levelFilter), [levelFilter])

  const filtered = useMemo(() => {
    const q = query.trim()
    const pool = readingItems.filter((it) => {
      if (levelFilter !== '全部' && it.level !== levelFilter) return false
      if (topic !== '全部' && it.topic !== topic) return false
      if (kind !== '全部' && it.kind !== kind) return false
      if (hideLearned && learned.has(it.id)) return false
      return true
    })
    if (!q) return pool
    return pool
      .map((it) => ({
        it,
        score: scoreTextFields(q, {
          primary: [it.title, it.titleZh, it.topic, it.id],
          secondary: [
            ...it.focus,
            ...it.notes.map((n) => `${n.span} ${n.zh}`),
            ...it.patterns.map((p) => `${p.pattern} ${p.zh}`),
          ],
          weak: [it.text, it.textZh, ...it.tips],
        }),
      }))
      .filter((x) => x.score > 0)
      .sort((a, b) => b.score - a.score)
      .map((x) => x.it)
  }, [levelFilter, topic, kind, query, hideLearned, learned])

  useEffect(() => {
    if (!filtered.some((i) => i.id === selectedId) && filtered[0]) {
      setSelectedId(filtered[0].id)
    }
  }, [filtered, selectedId])

  const selectedIndex = Math.max(
    0,
    filtered.findIndex((i) => i.id === selectedId),
  )
  const selected = filtered[selectedIndex] ?? filtered[0]

  const go = (delta: number) => {
    if (!filtered.length) return
    stopSpeaking()
    const next =
      (selectedIndex + delta + filtered.length) % filtered.length
    setSelectedId(filtered[next].id)
  }

  return (
    <div className="reading-view">
      <section className="level-board" aria-label="閱讀等級">
        <p className="ai-lead-sm reading-banner">{readingNote}</p>
        <div className="level-tabs" role="tablist" aria-label="選擇等級">
          {([...readingLevels, '全部'] as LevelFilter[]).map((lv) => (
            <button
              key={lv}
              type="button"
              role="tab"
              aria-selected={levelFilter === lv}
              className={`level-tab ${levelFilter === lv ? 'active' : ''}`}
              onClick={() => {
                stopSpeaking()
                setLevelFilter(lv)
                setTopic('全部')
              }}
            >
              {lv}
              {lv !== '全部' && (
                <span className="tab-count">
                  {countReadingByLevel(lv as ReadingLevel)}
                </span>
              )}
            </button>
          ))}
        </div>
      </section>

      <section className="toolbar" aria-label="閱讀篩選">
        <label className="search">
          <span className="sr-only">搜尋閱讀</span>
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="搜標題、主題、句型…"
            type="search"
          />
        </label>
        <div className="filters">
          <select
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            aria-label="主題"
          >
            <option value="全部">全部主題</option>
            {topics.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
          <select
            value={kind}
            onChange={(e) => setKind(e.target.value as ReadingKind | '全部')}
            aria-label="形式"
          >
            <option value="全部">全部形式</option>
            {(Object.keys(READING_KIND_LABEL) as ReadingKind[]).map((k) => (
              <option key={k} value={k}>
                {READING_KIND_LABEL[k]}
              </option>
            ))}
          </select>
          <label className="check">
            <input
              type="checkbox"
              checked={hideLearned}
              onChange={(e) => setHideLearned(e.target.checked)}
            />
            隱藏已讀
          </label>
        </div>
        <p className="filter-meta">閱讀 · {filtered.length} 篇</p>
      </section>

      <main className="layout">
        <aside className="word-list" aria-label="閱讀列表">
          {filtered.map((it) => {
            const active = it.id === selected?.id
            const done = learned.has(it.id)
            return (
              <button
                key={it.id}
                type="button"
                className={`word-row ${active ? 'active' : ''} ${done ? 'learned' : ''}`}
                onClick={() => {
                  stopSpeaking()
                  setSelectedId(it.id)
                }}
              >
                <span className={`level-pill level-${it.level}`}>
                  {it.level}
                </span>
                <span className="row-word">
                  {it.title}
                  {done ? ' ✓' : ''}
                </span>
                <span className="row-zh">
                  {READING_KIND_LABEL[it.kind]} · {it.topic} · {it.titleZh}
                </span>
              </button>
            )
          })}
          {!filtered.length && <p className="empty">找不到符合的閱讀。</p>}
        </aside>

        {selected ? (
          <ReadingDetail
            item={selected}
            learned={learned.has(selected.id)}
            onToggle={() =>
              setLearned((prev) => {
                const next = new Set(prev)
                if (next.has(selected.id)) next.delete(selected.id)
                else next.add(selected.id)
                return next
              })
            }
            onOpenWord={onOpenWord}
            onPrev={() => go(-1)}
            onNext={() => go(1)}
            positionLabel={`${selectedIndex + 1} / ${filtered.length}`}
          />
        ) : (
          <p className="empty">請選擇一篇閱讀。</p>
        )}
      </main>
    </div>
  )
}
