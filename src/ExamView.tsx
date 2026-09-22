import { useEffect, useMemo, useState } from 'react'
import {
  EXAM_KIND_LABEL,
  countScoredItems,
  examLevels,
  examNote,
  examPapers,
  getPaper,
  paperFormatLabel,
  papersForLevel,
  sectionTabLabel,
  type ExamItem,
  type ExamItemGap,
  type ExamItemMc,
  type ExamItemSchreiben,
  type ExamItemSprechen,
  type ExamItemTf,
  type ExamKind,
  type ExamLevel,
  type ExamPaper,
  type ExamSection,
} from './data/exams'
import { speakGerman, stopSpeaking } from './lib/speech'

type Phase = 'lobby' | 'taking' | 'results'
type TfChoice = 'ja' | 'nein' | 'nicht'

type Answers = Record<string, string | number | TfChoice | undefined>

function normalizeGap(s: string): string {
  return s.trim().toLowerCase().replace(/\s+/g, ' ')
}

function gapCorrect(item: ExamItemGap, raw: string): boolean {
  const n = normalizeGap(raw)
  if (!n) return false
  const accepted = [item.answer, ...(item.accept ?? [])].map(normalizeGap)
  return accepted.includes(n)
}

function isScored(item: ExamItem): item is ExamItemMc | ExamItemTf | ExamItemGap {
  return item.type === 'mc' || item.type === 'tf' || item.type === 'gap'
}

function scoreItem(item: ExamItem, answers: Answers): boolean | null {
  if (!isScored(item)) return null
  const a = answers[item.id]
  if (a === undefined || a === '') return false
  if (item.type === 'mc') return a === item.answer
  if (item.type === 'tf') {
    const map: Record<TfChoice, true | false | 'nicht'> = {
      ja: true,
      nein: false,
      nicht: 'nicht',
    }
    return map[a as TfChoice] === item.answer
  }
  return gapCorrect(item, String(a))
}

function wordCount(text: string): number {
  return text.trim().split(/\s+/).filter(Boolean).length
}

function formatTime(sec: number): string {
  const m = Math.floor(sec / 60)
  const s = sec % 60
  return `${m}:${s.toString().padStart(2, '0')}`
}

function SpeakBtn({ text, label }: { text: string; label: string }) {
  return (
    <button
      type="button"
      className="speak-btn"
      onClick={() => speakGerman(text.replace(/\n/g, '. '), 0.88)}
    >
      <span className="speak-icon" aria-hidden>
        ♪
      </span>
      {label}
    </button>
  )
}

function McBlock({
  item,
  value,
  onChange,
  review,
}: {
  item: ExamItemMc
  value: number | undefined
  onChange: (v: number) => void
  review: boolean
}) {
  const correct = review ? scoreItem(item, { [item.id]: value }) : null
  return (
    <fieldset className={`exam-q ${review ? (correct ? 'ok' : 'bad') : ''}`}>
      <legend className="exam-prompt">{item.prompt}</legend>
      {item.promptZh && <p className="exam-prompt-zh">{item.promptZh}</p>}
      <div className="exam-options" role="radiogroup">
        {item.options.map((opt, i) => (
          <label key={i} className="exam-option">
            <input
              type="radio"
              name={item.id}
              checked={value === i}
              disabled={review}
              onChange={() => onChange(i)}
            />
            <span>{opt}</span>
          </label>
        ))}
      </div>
      {review && (
        <p className="exam-explain">
          {correct ? '正確。' : `正解：${item.options[item.answer]}。`}
          {item.explainZh}
        </p>
      )}
    </fieldset>
  )
}

function TfBlock({
  item,
  value,
  onChange,
  review,
}: {
  item: ExamItemTf
  value: TfChoice | undefined
  onChange: (v: TfChoice) => void
  review: boolean
}) {
  const correct = review ? scoreItem(item, { [item.id]: value }) : null
  const labels: { k: TfChoice; de: string }[] = [
    { k: 'ja', de: 'Ja / Richtig' },
    { k: 'nein', de: 'Nein / Falsch' },
    { k: 'nicht', de: 'Steht nicht im Text' },
  ]
  const answerLabel =
    item.answer === true
      ? 'Ja'
      : item.answer === false
        ? 'Nein'
        : 'Steht nicht im Text'
  return (
    <fieldset className={`exam-q ${review ? (correct ? 'ok' : 'bad') : ''}`}>
      <legend className="exam-prompt">{item.prompt}</legend>
      {item.promptZh && <p className="exam-prompt-zh">{item.promptZh}</p>}
      <div className="exam-options" role="radiogroup">
        {labels.map(({ k, de }) => (
          <label key={k} className="exam-option">
            <input
              type="radio"
              name={item.id}
              checked={value === k}
              disabled={review}
              onChange={() => onChange(k)}
            />
            <span>{de}</span>
          </label>
        ))}
      </div>
      {review && (
        <p className="exam-explain">
          {correct ? '正確。' : `正解：${answerLabel}。`}
          {item.explainZh}
        </p>
      )}
    </fieldset>
  )
}

function GapBlock({
  item,
  value,
  onChange,
  review,
}: {
  item: ExamItemGap
  value: string
  onChange: (v: string) => void
  review: boolean
}) {
  const correct = review ? scoreItem(item, { [item.id]: value }) : null
  return (
    <fieldset className={`exam-q ${review ? (correct ? 'ok' : 'bad') : ''}`}>
      <legend className="exam-prompt">{item.prompt}</legend>
      {item.promptZh && <p className="exam-prompt-zh">{item.promptZh}</p>}
      <input
        className="exam-gap"
        type="text"
        value={value}
        disabled={review}
        onChange={(e) => onChange(e.target.value)}
        placeholder="填空…"
        autoComplete="off"
      />
      {review && (
        <p className="exam-explain">
          {correct ? '正確。' : `正解：${item.answer}。`}
          {item.explainZh}
        </p>
      )}
    </fieldset>
  )
}

function SchreibenBlock({
  item,
  value,
  onChange,
  checks,
  onToggleCheck,
  review,
}: {
  item: ExamItemSchreiben
  value: string
  onChange: (v: string) => void
  checks: boolean[]
  onToggleCheck: (i: number) => void
  review: boolean
}) {
  const wc = wordCount(value)
  return (
    <div className="exam-q exam-write">
      <p className="exam-prompt">{item.prompt}</p>
      <p className="exam-prompt-zh">{item.promptZh}</p>
      <p className="exam-meta">建議至少約 {item.minWords} 詞 · 目前 {wc} 詞</p>
      <textarea
        className="exam-textarea"
        rows={8}
        value={value}
        disabled={review}
        onChange={(e) => onChange(e.target.value)}
        placeholder="在此寫作…"
      />
      {review && (
        <div className="exam-model">
          <h4>參考範文</h4>
          <SpeakBtn text={item.modelAnswer} label="聽範文" />
          <pre className="exam-model-text">{item.modelAnswer}</pre>
          <h4>自評檢核（不計入自動分數）</h4>
          <ul className="exam-checklist">
            {item.checklist.map((c, i) => (
              <li key={c}>
                <label>
                  <input
                    type="checkbox"
                    checked={!!checks[i]}
                    onChange={() => onToggleCheck(i)}
                  />
                  {c}
                </label>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

function SprechenBlock({
  item,
  review,
}: {
  item: ExamItemSprechen
  review: boolean
}) {
  return (
    <div className="exam-q exam-speak">
      <p className="exam-prompt">{item.prompt}</p>
      <p className="exam-prompt-zh">{item.promptZh}</p>
      <ul className="exam-cues">
        {item.cues.map((c) => (
          <li key={c}>{c}</li>
        ))}
      </ul>
      <p className="exam-meta">口說為選練：可對著提示說，再聽範例對照。不計分。</p>
      <div className="exam-model">
        <SpeakBtn text={item.modelAnswer} label="聽口說範例" />
        {review && <pre className="exam-model-text">{item.modelAnswer}</pre>}
      </div>
    </div>
  )
}

function SectionBody({
  section,
  answers,
  writing,
  checks,
  review,
  setAnswer,
  setWriting,
  toggleCheck,
}: {
  section: ExamSection
  answers: Answers
  writing: Record<string, string>
  checks: Record<string, boolean[]>
  review: boolean
  setAnswer: (id: string, v: string | number | TfChoice) => void
  setWriting: (id: string, v: string) => void
  toggleCheck: (id: string, i: number, len: number) => void
}) {
  return (
    <div className="exam-section-body">
      <header className="exam-sec-head">
        <span className="type-pill">{EXAM_KIND_LABEL[section.kind]}</span>
        <h3>
          {section.title}
          <span className="exam-sec-zh"> · {section.titleZh}</span>
        </h3>
        <p className="exam-instructions">{section.instructionsZh}</p>
        <p className="exam-instructions-de">{section.instructions}</p>
      </header>

      {section.kind === 'hoeren' && section.audioText && (
        <div className="exam-audio">
          <p className="exam-meta">
            聽力以語音朗讀腳本模擬（可重播）。作答時建議先聽再看題。
          </p>
          <SpeakBtn text={section.audioText} label="播放聽力腳本" />
          <button type="button" className="ghost" onClick={() => stopSpeaking()}>
            停止
          </button>
          {review && (
            <details className="exam-script">
              <summary>查看聽力稿（檢討用）</summary>
              <pre>{section.audioText}</pre>
            </details>
          )}
        </div>
      )}

      {section.passage && (
        <div className="exam-passage">
          <h4>Text</h4>
          <pre className="exam-passage-text">{section.passage}</pre>
          {review && section.passageZh && (
            <p className="exam-passage-zh">{section.passageZh}</p>
          )}
        </div>
      )}

      <div className="exam-items">
        {section.items.map((item) => {
          if (item.type === 'mc') {
            return (
              <McBlock
                key={item.id}
                item={item}
                value={answers[item.id] as number | undefined}
                onChange={(v) => setAnswer(item.id, v)}
                review={review}
              />
            )
          }
          if (item.type === 'tf') {
            return (
              <TfBlock
                key={item.id}
                item={item}
                value={answers[item.id] as TfChoice | undefined}
                onChange={(v) => setAnswer(item.id, v)}
                review={review}
              />
            )
          }
          if (item.type === 'gap') {
            return (
              <GapBlock
                key={item.id}
                item={item}
                value={String(answers[item.id] ?? '')}
                onChange={(v) => setAnswer(item.id, v)}
                review={review}
              />
            )
          }
          if (item.type === 'schreiben') {
            return (
              <SchreibenBlock
                key={item.id}
                item={item}
                value={writing[item.id] ?? ''}
                onChange={(v) => setWriting(item.id, v)}
                checks={checks[item.id] ?? []}
                onToggleCheck={(i) =>
                  toggleCheck(item.id, i, item.checklist.length)
                }
                review={review}
              />
            )
          }
          return <SprechenBlock key={item.id} item={item} review={review} />
        })}
      </div>
    </div>
  )
}

export default function ExamView() {
  const [level, setLevel] = useState<ExamLevel>('A1')
  const [phase, setPhase] = useState<Phase>('lobby')
  const [paperId, setPaperId] = useState<string | null>(null)
  const [secIdx, setSecIdx] = useState(0)
  const [answers, setAnswers] = useState<Answers>({})
  const [writing, setWriting] = useState<Record<string, string>>({})
  const [checks, setChecks] = useState<Record<string, boolean[]>>({})
  const [secondsLeft, setSecondsLeft] = useState<number | null>(null)

  const paper = paperId ? getPaper(paperId) : undefined
  const lobbyPapers = useMemo(() => papersForLevel(level), [level])

  useEffect(() => {
    if (phase !== 'taking' || secondsLeft === null) return
    if (secondsLeft <= 0) return
    const t = window.setTimeout(() => setSecondsLeft((s) => (s ?? 1) - 1), 1000)
    return () => window.clearTimeout(t)
  }, [phase, secondsLeft])

  const scoredTotal = paper ? countScoredItems(paper) : 0
  const scoredResult = useMemo(() => {
    if (!paper) return { correct: 0, byKind: {} as Record<ExamKind, { c: number; t: number }> }
    let correct = 0
    const byKind = {} as Record<ExamKind, { c: number; t: number }>
    for (const sec of paper.sections) {
      if (!byKind[sec.kind]) byKind[sec.kind] = { c: 0, t: 0 }
      for (const item of sec.items) {
        if (!isScored(item)) continue
        byKind[sec.kind].t += 1
        if (scoreItem(item, answers)) {
          correct += 1
          byKind[sec.kind].c += 1
        }
      }
    }
    return { correct, byKind }
  }, [paper, answers])

  function startPaper(p: ExamPaper) {
    stopSpeaking()
    setPaperId(p.id)
    setSecIdx(0)
    setAnswers({})
    setWriting({})
    setChecks({})
    setSecondsLeft(p.durationMin * 60)
    setPhase('taking')
  }

  function submit() {
    stopSpeaking()
    setPhase('results')
  }

  function backLobby() {
    stopSpeaking()
    setPhase('lobby')
    setPaperId(null)
    setSecondsLeft(null)
  }

  if (phase === 'lobby') {
    return (
      <div className="exam-view">
        <section className="level-board" aria-label="測驗等級">
          <p className="ai-lead-sm reading-banner">{examNote}</p>
          <div className="level-tabs" role="tablist" aria-label="選擇等級">
            {examLevels.map((lv) => (
              <button
                key={lv}
                type="button"
                role="tab"
                aria-selected={level === lv}
                className={`level-tab ${level === lv ? 'active' : ''}`}
                onClick={() => setLevel(lv)}
              >
                {lv}
                <span className="tab-count">
                  {papersForLevel(lv).length}
                </span>
              </button>
            ))}
          </div>
        </section>

        <div className="exam-lobby-grid">
          {lobbyPapers.map((p) => (
            <article
              key={p.id}
              className={`exam-card ${p.format === 'goethe' ? 'exam-card-goethe' : ''}`}
            >
              <div className="detail-top">
                <span className={`level-pill level-${p.level}`}>{p.level}</span>
                <span className="type-pill">{paperFormatLabel(p)}</span>
                <span className="type-pill">第 {p.round} 回</span>
              </div>
              <h2 className="grammar-title">{p.titleZh}</h2>
              <p className="grammar-title-de">{p.title}</p>
              <p className="exam-card-meta">
                約 {p.durationMin} 分鐘 · 自動計分 {countScoredItems(p)} 題 ·{' '}
                {p.format === 'goethe'
                  ? `${p.sections.length} 個 Teil（對齊 Goethe 分節）`
                  : '綜合卷（含語法詞彙）'}
              </p>
              <ul className="exam-kind-row">
                {[...new Set(p.sections.map((s) => EXAM_KIND_LABEL[s.kind]))].map(
                  (lab) => (
                    <li key={lab}>{lab}</li>
                  ),
                )}
              </ul>
              <button
                type="button"
                className="primary"
                onClick={() => startPaper(p)}
              >
                開始{paperFormatLabel(p)} · 第 {p.round} 回
              </button>
            </article>
          ))}
        </div>

        <p className="exam-footnote">
          共 {examPapers.length} 份。練習版＝綜合訓練；考場版＝依 Goethe 分
          Teil（Lesen／Hören／Schreiben／Sprechen）。聽力以瀏覽器德文語音朗讀腳本；口說選練不計分。
        </p>
      </div>
    )
  }

  if (!paper) {
    return (
      <div className="exam-view">
        <p className="empty">找不到這份考卷。</p>
        <button type="button" className="ghost" onClick={backLobby}>
          回模考列表
        </button>
      </div>
    )
  }

  const section = paper.sections[secIdx]
  const review = phase === 'results'
  const pct =
    scoredTotal > 0
      ? Math.round((scoredResult.correct / scoredTotal) * 100)
      : 0

  return (
    <div className="exam-view">
      <div className="exam-topbar">
        <button type="button" className="ghost nav-back" onClick={backLobby}>
          ← 模考列表
        </button>
        <div className="exam-topbar-main">
          <strong>{paper.titleZh}</strong>
          <span className={`level-pill level-${paper.level}`}>{paper.level}</span>
        </div>
        {phase === 'taking' && secondsLeft !== null && (
          <span
            className={`exam-timer ${secondsLeft < 300 ? 'warn' : ''}`}
            aria-live="polite"
          >
            剩餘 {formatTime(secondsLeft)}
          </span>
        )}
        {phase === 'results' && (
          <span className="exam-score-pill">
            {scoredResult.correct}/{scoredTotal}（{pct}%）
          </span>
        )}
      </div>

      {phase === 'results' && (
        <section className="exam-results-summary" aria-label="成績">
          <h2>自動計分成績</h2>
          <p>
            閱讀／聽力／語法詞彙：<strong>{scoredResult.correct}</strong> /{' '}
            {scoredTotal}（{pct}%）
          </p>
          <div className="exam-kind-scores">
            {(Object.keys(EXAM_KIND_LABEL) as ExamKind[]).map((k) => {
              const row = scoredResult.byKind[k]
              if (!row || row.t === 0) return null
              return (
                <div key={k} className="exam-kind-score">
                  <span>{EXAM_KIND_LABEL[k]}</span>
                  <strong>
                    {row.c}/{row.t}
                  </strong>
                </div>
              )
            })}
          </div>
          <p className="exam-meta">
            寫作請對照範文與檢核表自評；口說為選練，皆不計入上方分數。
          </p>
        </section>
      )}

      <div className="exam-sec-tabs" role="tablist" aria-label="大題">
        {paper.sections.map((s, i) => (
          <button
            key={s.id}
            type="button"
            role="tab"
            aria-selected={secIdx === i}
            className={`level-tab ${secIdx === i ? 'active' : ''}`}
            onClick={() => {
              stopSpeaking()
              setSecIdx(i)
            }}
          >
            {sectionTabLabel(s)}
          </button>
        ))}
      </div>

      <SectionBody
        section={section}
        answers={answers}
        writing={writing}
        checks={checks}
        review={review}
        setAnswer={(id, v) => setAnswers((prev) => ({ ...prev, [id]: v }))}
        setWriting={(id, v) => setWriting((prev) => ({ ...prev, [id]: v }))}
        toggleCheck={(id, i, len) =>
          setChecks((prev) => {
            const cur = [...(prev[id] ?? Array(len).fill(false))]
            cur[i] = !cur[i]
            return { ...prev, [id]: cur }
          })
        }
      />

      <div className="exam-nav-row">
        <button
          type="button"
          className="ghost"
          disabled={secIdx === 0}
          onClick={() => {
            stopSpeaking()
            setSecIdx((i) => Math.max(0, i - 1))
          }}
        >
          ← 上一大題
        </button>
        {secIdx < paper.sections.length - 1 ? (
          <button
            type="button"
            className="primary"
            onClick={() => {
              stopSpeaking()
              setSecIdx((i) => i + 1)
            }}
          >
            下一大題 →
          </button>
        ) : phase === 'taking' ? (
          <button type="button" className="primary" onClick={submit}>
            交卷看成績
          </button>
        ) : (
          <button type="button" className="primary" onClick={backLobby}>
            完成，回列表
          </button>
        )}
      </div>
    </div>
  )
}
