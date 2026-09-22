import { useEffect, useMemo, useState } from 'react'
import { vocabulary, type VocabWord } from './data/vocabulary'
import { LinkedGermanText } from './lib/LinkedGermanText'
import { SpeakPair } from './lib/SpeakControls'
import type { VocabHit } from './lib/vocabIndex'
import { ArticleText } from './lib/richText'
import {
  ROADMAP_DAYS,
  ROADMAP_NOTE,
  type RoadmapDay,
  type RoadmapTask,
} from './data/roadmap'
import {
  getChapter,
  getSeries,
  storyNote,
  storySeries,
  type StoryChapter,
  type StorySeries,
} from './data/stories'
import {
  countDue,
  enrollCard,
  formatDueLabel,
  listDueIds,
  reviewCard,
  saveSrsMap,
  SRS_GRADE_LABEL,
  type SrsCard,
  type SrsGrade,
} from './lib/srs'
import {
  loadLlmSettings,
  requestGermanFeedback,
  saveLlmSettings,
  type LlmSettings,
  type TutorCorrection,
} from './lib/llmTutor'

type LearnTab = 'today' | 'roadmap' | 'stories' | 'tutor'

const ROADMAP_DONE_KEY = 'wortklang-roadmap-done'
const ROADMAP_DAY_KEY = 'wortklang-roadmap-day'

function loadDone(): Set<string> {
  try {
    const raw = localStorage.getItem(ROADMAP_DONE_KEY)
    if (!raw) return new Set()
    const arr = JSON.parse(raw) as string[]
    return new Set(Array.isArray(arr) ? arr : [])
  } catch {
    return new Set()
  }
}

function vocabById(id: string): VocabWord | undefined {
  return vocabulary.find((w) => w.id === id)
}

export default function LearnHub({
  onOpenWord,
  onOpenVocabIds,
  onOpenGrammar,
  onOpenReading,
  srsMap,
  setSrsMap,
}: {
  onOpenWord: (hit: VocabHit) => void
  onOpenVocabIds: (ids: string[]) => void
  onOpenGrammar: (topicId: string) => void
  onOpenReading: (readingId: string) => void
  srsMap: Record<string, SrsCard>
  setSrsMap: (map: Record<string, SrsCard>) => void
}) {
  const [tab, setTab] = useState<LearnTab>('today')
  const [day, setDay] = useState(() => {
    const raw = localStorage.getItem(ROADMAP_DAY_KEY)
    const n = raw ? Number(raw) : 1
    return Number.isFinite(n) && n >= 1 && n <= 30 ? n : 1
  })
  const [done, setDone] = useState<Set<string>>(() => loadDone())

  useEffect(() => {
    localStorage.setItem(ROADMAP_DONE_KEY, JSON.stringify([...done]))
  }, [done])

  useEffect(() => {
    localStorage.setItem(ROADMAP_DAY_KEY, String(day))
  }, [day])

  const dueIds = useMemo(() => listDueIds(srsMap), [srsMap])
  const dueCount = countDue(srsMap)
  const today = ROADMAP_DAYS.find((d) => d.day === day) ?? ROADMAP_DAYS[0]

  function toggleDone(taskId: string) {
    setDone((prev) => {
      const next = new Set(prev)
      if (next.has(taskId)) next.delete(taskId)
      else next.add(taskId)
      return next
    })
  }

  function gradeDue(id: string, grade: SrsGrade) {
    const next = reviewCard(srsMap, id, grade)
    setSrsMap(next)
    saveSrsMap(next)
  }

  function enrollMany(ids: string[]) {
    let map = srsMap
    for (const id of ids) map = enrollCard(map, id)
    setSrsMap(map)
    saveSrsMap(map)
  }

  return (
    <div className="learn-hub">
      <section className="level-board">
        <p className="ai-lead-sm reading-banner">
          自學中樞：今日複習（SRS）→ 30 日路徑 → 故事泛讀 → AI
          家教批改。零基礎建議每天先走路徑，再消化到期複習。
        </p>
        <div className="level-tabs" role="tablist" aria-label="自學分區">
          {(
            [
              ['today', `今日複習${dueCount ? ` ${dueCount}` : ''}`],
              ['roadmap', '30日路徑'],
              ['stories', '故事泛讀'],
              ['tutor', 'AI家教'],
            ] as const
          ).map(([k, label]) => (
            <button
              key={k}
              type="button"
              role="tab"
              className={`level-tab ${tab === k ? 'active' : ''}`}
              aria-selected={tab === k}
              onClick={() => setTab(k)}
            >
              {label}
            </button>
          ))}
        </div>
      </section>

      {tab === 'today' && (
        <TodayReview
          dueIds={dueIds}
          srsMap={srsMap}
          today={today}
          done={done}
          onGrade={gradeDue}
          onOpenVocabIds={onOpenVocabIds}
          onGoRoadmap={() => setTab('roadmap')}
          onTask={toggleDone}
          onOpenGrammar={onOpenGrammar}
          onOpenReading={onOpenReading}
          onOpenStory={(seriesId, chapterId) => {
            sessionStorage.setItem(
              'wortklang-story-jump',
              JSON.stringify({ seriesId, chapterId }),
            )
            setTab('stories')
          }}
          onEnroll={enrollMany}
        />
      )}
      {tab === 'roadmap' && (
        <RoadmapPanel
          day={day}
          setDay={setDay}
          done={done}
          onToggle={toggleDone}
          onOpenVocabIds={onOpenVocabIds}
          onOpenGrammar={onOpenGrammar}
          onOpenReading={onOpenReading}
          onOpenStory={(seriesId, chapterId) => {
            sessionStorage.setItem(
              'wortklang-story-jump',
              JSON.stringify({ seriesId, chapterId }),
            )
            setTab('stories')
          }}
          onEnroll={enrollMany}
        />
      )}
      {tab === 'stories' && <StoriesPanel onOpenWord={onOpenWord} />}
      {tab === 'tutor' && <TutorPanel />}
    </div>
  )
}

function TodayReview({
  dueIds,
  srsMap,
  today,
  done,
  onGrade,
  onOpenVocabIds,
  onGoRoadmap,
  onTask,
  onOpenGrammar,
  onOpenReading,
  onOpenStory,
  onEnroll,
}: {
  dueIds: string[]
  srsMap: Record<string, SrsCard>
  today: RoadmapDay
  done: Set<string>
  onGrade: (id: string, g: SrsGrade) => void
  onOpenVocabIds: (ids: string[]) => void
  onGoRoadmap: () => void
  onTask: (id: string) => void
  onOpenGrammar: (id: string) => void
  onOpenReading: (id: string) => void
  onOpenStory: (seriesId: string, chapterId: string) => void
  onEnroll: (ids: string[]) => void
}) {
  const [idx, setIdx] = useState(0)
  const [revealed, setRevealed] = useState(false)
  const currentId = dueIds[idx]
  const word = currentId ? vocabById(currentId) : undefined

  useEffect(() => {
    setRevealed(false)
    if (idx >= dueIds.length) setIdx(0)
  }, [idx, dueIds.length])

  return (
    <div className="learn-panel">
      <article className="exam-card exam-card-goethe">
        <div className="detail-top">
          <span className="type-pill">Day {today.day}</span>
          <span className="type-pill">{today.titleZh}</span>
        </div>
        <h2 className="grammar-title">今日路徑：{today.titleZh}</h2>
        <p className="exam-card-meta">{today.focusZh}</p>
        <button type="button" className="primary" onClick={onGoRoadmap}>
          打開今日 30 日路徑
        </button>
      </article>

      <section className="panel">
        <h3>SRS 到期複習（艾賓浩斯排程）</h3>
        <p className="panel-note">
          標記「已學會」的單字會在 1→3→7→14
          天後自動回來。依記得程度按下方按鈕，系統會改下次複習日。
        </p>
        {!word ? (
          <p className="empty">
            目前沒有到期單字。去路徑學新字並按「加入複習／已學會」吧。
          </p>
        ) : (
          <div className="srs-card">
            <p className="exam-meta">
              {idx + 1} / {dueIds.length} ·{' '}
              {formatDueLabel(srsMap[word.id])}
            </p>
            <h2 className="lemma">
              {word.article ? `${word.article} ` : ''}
              {word.word}
            </h2>
            <SpeakPair text={word.word} normalLabel="聽" slowLabel="慢速" />
            {!revealed ? (
              <button
                type="button"
                className="primary"
                onClick={() => setRevealed(true)}
              >
                顯示意思
              </button>
            ) : (
              <>
                <p className="translation">{word.translation}</p>
                <p className="example-de">{word.example}</p>
                <p className="example-zh">{word.exampleTranslation}</p>
                <div className="srs-grades">
                  {(Object.keys(SRS_GRADE_LABEL) as SrsGrade[]).map((g) => (
                    <button
                      key={g}
                      type="button"
                      className={g === 'again' ? 'ghost' : 'primary'}
                      onClick={() => {
                        onGrade(word.id, g)
                        setRevealed(false)
                      }}
                    >
                      {SRS_GRADE_LABEL[g]}
                    </button>
                  ))}
                </div>
              </>
            )}
          </div>
        )}
      </section>

      <section className="panel">
        <h3>今日任務速覽</h3>
        <ul className="learn-task-list">
          {today.tasks.map((t) => (
            <li key={t.id}>
              <label>
                <input
                  type="checkbox"
                  checked={done.has(t.id)}
                  onChange={() => onTask(t.id)}
                />
                <strong>{t.titleZh}</strong>
                <span className="exam-meta"> · {t.tipZh}</span>
              </label>
              <TaskActions
                task={t}
                onOpenVocabIds={(ids) => {
                  onEnroll(ids)
                  onOpenVocabIds(ids)
                }}
                onOpenGrammar={onOpenGrammar}
                onOpenReading={onOpenReading}
                onOpenStory={onOpenStory}
              />
            </li>
          ))}
        </ul>
      </section>
    </div>
  )
}

function TaskActions({
  task,
  onOpenVocabIds,
  onOpenGrammar,
  onOpenReading,
  onOpenStory,
}: {
  task: RoadmapTask
  onOpenVocabIds: (ids: string[]) => void
  onOpenGrammar: (id: string) => void
  onOpenReading: (id: string) => void
  onOpenStory?: (seriesId: string, chapterId: string) => void
}) {
  if (task.kind === 'vocab' && task.vocabIds?.length) {
    return (
      <button
        type="button"
        className="ghost"
        onClick={() => onOpenVocabIds(task.vocabIds!)}
      >
        去學這 {task.vocabIds.length} 個字
      </button>
    )
  }
  if (task.kind === 'grammar' && task.grammarId) {
    return (
      <button
        type="button"
        className="ghost"
        onClick={() => onOpenGrammar(task.grammarId!)}
      >
        打開文法
      </button>
    )
  }
  if (task.kind === 'reading' && task.readingId) {
    return (
      <button
        type="button"
        className="ghost"
        onClick={() => onOpenReading(task.readingId!)}
      >
        打開閱讀
      </button>
    )
  }
  if (task.kind === 'story' && task.storyId && onOpenStory) {
    const [seriesId, chapterId] = task.storyId.split('/')
    return (
      <button
        type="button"
        className="ghost"
        onClick={() => onOpenStory(seriesId, chapterId)}
      >
        打開故事
      </button>
    )
  }
  return null
}

function RoadmapPanel({
  day,
  setDay,
  done,
  onToggle,
  onOpenVocabIds,
  onOpenGrammar,
  onOpenReading,
  onOpenStory,
  onEnroll,
}: {
  day: number
  setDay: (n: number) => void
  done: Set<string>
  onToggle: (id: string) => void
  onOpenVocabIds: (ids: string[]) => void
  onOpenGrammar: (id: string) => void
  onOpenReading: (id: string) => void
  onOpenStory: (seriesId: string, chapterId: string) => void
  onEnroll: (ids: string[]) => void
}) {
  const d = ROADMAP_DAYS.find((x) => x.day === day) ?? ROADMAP_DAYS[0]
  const doneCount = d.tasks.filter((t) => done.has(t.id)).length

  return (
    <div className="learn-panel">
      <p className="ai-lead-sm">{ROADMAP_NOTE}</p>
      <div className="roadmap-day-tabs">
        {ROADMAP_DAYS.map((x) => {
          const n = x.tasks.filter((t) => done.has(t.id)).length
          const all = n === x.tasks.length
          return (
            <button
              key={x.day}
              type="button"
              className={`level-tab ${day === x.day ? 'active' : ''}`}
              onClick={() => setDay(x.day)}
            >
              {x.day}
              {all ? '✓' : ''}
            </button>
          )
        })}
      </div>

      <article className="exam-card">
        <div className="detail-top">
          <span className="level-pill level-A1">Day {d.day}</span>
          <span className="type-pill">
            {doneCount}/{d.tasks.length} 完成
          </span>
        </div>
        <h2 className="grammar-title">{d.titleZh}</h2>
        <p className="exam-card-meta">{d.focusZh}</p>
      </article>

      <ul className="learn-task-list">
        {d.tasks.map((t) => (
          <li key={t.id} className="learn-task">
            <label>
              <input
                type="checkbox"
                checked={done.has(t.id)}
                onChange={() => onToggle(t.id)}
              />
              <span>
                <strong>{t.titleZh}</strong>
                {t.titleDe ? ` · ${t.titleDe}` : ''}
              </span>
            </label>
            <p className="exam-meta">{t.tipZh}</p>
            {t.vocabIds && (
              <ul className="learn-vocab-preview">
                {t.vocabIds.map((id) => {
                  const w = vocabById(id)
                  return (
                    <li key={id}>
                      {w
                        ? `${w.article ? w.article + ' ' : ''}${w.word} — ${w.translation}`
                        : id}
                    </li>
                  )
                })}
              </ul>
            )}
            <TaskActions
              task={t}
              onOpenVocabIds={(ids) => {
                onEnroll(ids)
                onOpenVocabIds(ids)
              }}
              onOpenGrammar={onOpenGrammar}
              onOpenReading={onOpenReading}
              onOpenStory={onOpenStory}
            />
          </li>
        ))}
      </ul>
    </div>
  )
}

function StoriesPanel({ onOpenWord }: { onOpenWord: (hit: VocabHit) => void }) {
  const jump = (() => {
    try {
      const raw = sessionStorage.getItem('wortklang-story-jump')
      if (!raw) return null
      sessionStorage.removeItem('wortklang-story-jump')
      return JSON.parse(raw) as { seriesId: string; chapterId: string }
    } catch {
      return null
    }
  })()

  const [seriesId, setSeriesId] = useState(
    jump?.seriesId ?? storySeries[0]?.id ?? '',
  )
  const [chapterId, setChapterId] = useState(
    jump?.chapterId ?? storySeries[0]?.chapters[0]?.id ?? '',
  )
  const [showZh, setShowZh] = useState(false)

  const series = getSeries(seriesId) as StorySeries | undefined
  const chapter = series
    ? (getChapter(seriesId, chapterId) as StoryChapter | undefined)
    : undefined

  return (
    <div className="learn-panel">
      <p className="ai-lead-sm">{storyNote}</p>
      <div className="exam-lobby-grid">
        {storySeries.map((s) => (
          <button
            key={s.id}
            type="button"
            className={`exam-card ${seriesId === s.id ? 'exam-card-goethe' : ''}`}
            onClick={() => {
              setSeriesId(s.id)
              setChapterId(s.chapters[0]?.id ?? '')
            }}
          >
            <div className="detail-top">
              <span className={`level-pill level-${s.level}`}>{s.level}</span>
            </div>
            <h2 className="grammar-title">{s.titleZh}</h2>
            <p className="grammar-title-de">{s.title}</p>
            <p className="exam-card-meta">{s.blurbZh}</p>
          </button>
        ))}
      </div>

      {series && chapter && (
        <article className="detail reading-detail">
          <div className="exam-sec-tabs">
            {series.chapters.map((c) => (
              <button
                key={c.id}
                type="button"
                className={`level-tab ${chapterId === c.id ? 'active' : ''}`}
                onClick={() => setChapterId(c.id)}
              >
                {c.order}. {c.titleZh}
              </button>
            ))}
          </div>
          <h2 className="grammar-title">{chapter.title}</h2>
          <p className="grammar-title-de">{chapter.titleZh}</p>
          <div className="speak-row">
            <SpeakPair
              text={chapter.text}
              normalLabel="聽本章"
              slowLabel="慢速"
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
          <div className="reading-de">
            {chapter.text.split('\n').map((line, i) => (
              <p key={i} className="reading-line">
                {line ? (
                  <LinkedGermanText
                    text={line}
                    preferLevel={series.level}
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
              {chapter.textZh.split('\n').map((line, i) => (
                <p key={i}>{line || '\u00a0'}</p>
              ))}
            </div>
          )}
          <section className="grammar-section">
            <h3>註解</h3>
            <ul className="reading-notes">
              {chapter.notes.map((n) => (
                <li key={n.span + n.zh}>
                  <strong className="reading-note-span">{n.span}</strong>
                  <span className="reading-note-zh">{n.zh}</span>
                  {n.tip && <p className="reading-note-tip">{n.tip}</p>}
                </li>
              ))}
            </ul>
          </section>
        </article>
      )}
    </div>
  )
}

function TutorPanel() {
  const [settings, setSettings] = useState<LlmSettings>(() => loadLlmSettings())
  const [showSettings, setShowSettings] = useState(false)
  const [mode, setMode] = useState<'schreiben' | 'sprechen'>('schreiben')
  const [level, setLevel] = useState('A1')
  const [promptZh, setPromptZh] = useState(
    '寫一封短訊給朋友：約明天喝咖啡（約 40 詞）。',
  )
  const [userText, setUserText] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [result, setResult] = useState<TutorCorrection | null>(null)

  function persist(next: LlmSettings) {
    setSettings(next)
    saveLlmSettings(next)
  }

  async function run() {
    setLoading(true)
    setError('')
    setResult(null)
    try {
      const r = await requestGermanFeedback({
        settings,
        mode,
        promptZh,
        userText,
        level,
      })
      setResult(r)
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="learn-panel">
      <p className="ai-lead-sm">
        把你寫的／準備說的德文貼上來，串接 OpenAI
        相容 API（金鑰只存在本機）即時糾錯：冠詞、動詞位置、格變與語意。
      </p>

      <div className="speak-row">
        <button
          type="button"
          className="ghost"
          onClick={() => setShowSettings((v) => !v)}
        >
          {showSettings ? '收起設定' : 'API 設定'}
        </button>
        <span className="exam-meta">
          {settings.apiKey ? '已設定 Key' : '尚未設定 Key'}
        </span>
      </div>

      {showSettings && (
        <section className="panel">
          <label className="learn-field">
            API Key
            <input
              type="password"
              value={settings.apiKey}
              onChange={(e) => persist({ ...settings, apiKey: e.target.value })}
              placeholder="sk-…"
            />
          </label>
          <label className="learn-field">
            Base URL
            <input
              value={settings.baseUrl}
              onChange={(e) =>
                persist({ ...settings, baseUrl: e.target.value })
              }
            />
          </label>
          <label className="learn-field">
            Model
            <input
              value={settings.model}
              onChange={(e) => persist({ ...settings, model: e.target.value })}
            />
          </label>
          <p className="exam-meta">
            支援 OpenAI／相容端點（含部分 Grok／代理）。金鑰不會上傳到本站伺服器。
          </p>
        </section>
      )}

      <div className="level-tabs">
        <button
          type="button"
          className={`level-tab ${mode === 'schreiben' ? 'active' : ''}`}
          onClick={() => setMode('schreiben')}
        >
          寫作批改
        </button>
        <button
          type="button"
          className={`level-tab ${mode === 'sprechen' ? 'active' : ''}`}
          onClick={() => setMode('sprechen')}
        >
          口說稿批改
        </button>
      </div>

      <label className="learn-field">
        等級
        <select value={level} onChange={(e) => setLevel(e.target.value)}>
          {['A1', 'A2', 'B1', 'B2', 'C1'].map((lv) => (
            <option key={lv} value={lv}>
              {lv}
            </option>
          ))}
        </select>
      </label>
      <label className="learn-field">
        題目／情境（中文）
        <textarea
          rows={2}
          value={promptZh}
          onChange={(e) => setPromptZh(e.target.value)}
        />
      </label>
      <label className="learn-field">
        你的德文
        <textarea
          rows={8}
          className="exam-textarea"
          value={userText}
          onChange={(e) => setUserText(e.target.value)}
          placeholder="Hier schreiben…"
        />
      </label>
      <button
        type="button"
        className="primary"
        disabled={loading}
        onClick={() => void run()}
      >
        {loading ? '批改中…' : '請 AI 批改'}
      </button>
      {error && <p className="exam-explain">{error}</p>}
      {result && (
        <section className="panel">
          <h3>批改結果 · {result.score} 分</h3>
          <p>{result.summaryZh}</p>
          <h4>修正稿</h4>
          <SpeakPair text={result.corrected} normalLabel="聽修正" slowLabel="慢速" />
          <pre className="exam-model-text">{result.corrected}</pre>
          <ul className="reading-notes">
            {result.issues.map((iss, i) => (
              <li key={i}>
                <strong>{iss.span}</strong>
                <span className="reading-note-zh">{iss.issueZh}</span>
                <p className="reading-note-tip">{iss.fixZh}</p>
              </li>
            ))}
          </ul>
          <ul className="grammar-points">
            {result.tipsZh.map((t) => (
              <li key={t}>
                <ArticleText text={t} />
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  )
}

