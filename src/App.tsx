import { useEffect, useMemo, useState } from 'react'
import {
  categories,
  vocabulary,
  type Category,
  type Gender,
  type VocabWord,
} from './data/vocabulary'
import { ensureVoicesLoaded, speakGerman, stopSpeaking } from './lib/speech'
import './App.css'

type Mode = 'browse' | 'flash'

const genderClass: Record<NonNullable<Gender>, string> = {
  der: 'gender-der',
  die: 'gender-die',
  das: 'gender-das',
}

function WordBadge({ article }: { article: Gender }) {
  if (!article) {
    return <span className="badge badge-neutral">無冠詞</span>
  }
  return (
    <span className={`badge ${genderClass[article]}`}>{article}</span>
  )
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

function WordDetail({ word }: { word: VocabWord }) {
  const lemma = word.article ? `${word.article} ${word.word}` : word.word

  return (
    <article className="detail" key={word.id}>
      <div className="detail-top">
        <WordBadge article={word.article} />
        <span className="level">{word.level}</span>
      </div>

      <h2 className="lemma">
        {word.article && <span className="article">{word.article}</span>}
        <span className="word">{word.word}</span>
      </h2>

      <p className="translation">{word.translation}</p>
      <p className="phonetic">/{word.phonetic}/</p>

      {(word.plural || word.article) && (
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
          <dt>分類</dt>
          <dd>{word.category}</dd>
        </dl>
      )}

      <div className="speak-row">
        <SpeakButton label="聽單字" text={lemma} />
        <SpeakButton label="慢速" text={lemma} slow />
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
}: {
  word: VocabWord
  revealed: boolean
  onReveal: () => void
  onNext: () => void
}) {
  const lemma = word.article ? `${word.article} ${word.word}` : word.word

  return (
    <div className={`flash ${revealed ? 'revealed' : ''}`}>
      <div className="flash-front">
        <WordBadge article={word.article} />
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
          <button type="button" className="primary" onClick={onNext}>
            下一個
          </button>
        )}
      </div>
    </div>
  )
}

export default function App() {
  const [query, setQuery] = useState('')
  const [category, setCategory] = useState<Category | '全部'>('全部')
  const [gender, setGender] = useState<'全部' | 'der' | 'die' | 'das' | '無冠詞'>(
    '全部',
  )
  const [selectedId, setSelectedId] = useState(vocabulary[0]?.id ?? '')
  const [mode, setMode] = useState<Mode>('browse')
  const [flashIndex, setFlashIndex] = useState(0)
  const [revealed, setRevealed] = useState(false)
  const [voiceReady, setVoiceReady] = useState(false)

  useEffect(() => {
    ensureVoicesLoaded().then((v) => setVoiceReady(Boolean(v) || true))
    return () => stopSpeaking()
  }, [])

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase()
    return vocabulary.filter((w) => {
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
      ]
        .join(' ')
        .toLowerCase()
      return hay.includes(q)
    })
  }, [query, category, gender])

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

  return (
    <div className="app">
      <div className="atmosphere" aria-hidden />

      <header className="hero">
        <p className="brand">Wortklang</p>
        <h1>聽得見的德文單字</h1>
        <p className="tagline">
          冠詞、例句、標準德文發音——一次記住怎麼說、怎麼用。
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
        {!voiceReady && (
          <p className="voice-hint">正在載入語音引擎…</p>
        )}
      </header>

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
            onChange={(e) =>
              setCategory(e.target.value as Category | '全部')
            }
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

        <p className="count">{filtered.length} 個單字</p>
      </section>

      {mode === 'browse' && selected && (
        <main className="layout">
          <aside className="word-list" aria-label="單字列表">
            {filtered.map((w) => {
              const active = w.id === selected.id
              return (
                <button
                  key={w.id}
                  type="button"
                  className={`word-row ${active ? 'active' : ''}`}
                  onClick={() => {
                    stopSpeaking()
                    setSelectedId(w.id)
                  }}
                >
                  <WordBadge article={w.article} />
                  <span className="row-word">{w.word}</span>
                  <span className="row-zh">{w.translation}</span>
                </button>
              )
            })}
            {!filtered.length && (
              <p className="empty">找不到符合的單字，試試其他關鍵字。</p>
            )}
          </aside>
          <WordDetail word={selected} />
        </main>
      )}

      {mode === 'flash' && flashWord && (
        <main className="flash-wrap">
          <p className="flash-progress">
            {filtered.length
              ? `${(flashIndex % filtered.length) + 1} / ${filtered.length}`
              : '0 / 0'}
          </p>
          {filtered.length ? (
            <FlashCard
              word={flashWord}
              revealed={revealed}
              onReveal={() => setRevealed(true)}
              onNext={() => {
                stopSpeaking()
                setRevealed(false)
                setFlashIndex((i) => i + 1)
              }}
            />
          ) : (
            <p className="empty">沒有可練習的單字。</p>
          )}
        </main>
      )}

      <footer className="footer">
        <p>
          發音使用瀏覽器德文語音（de-DE）。建議用 Chrome / Edge 以獲得較佳聲線。
        </p>
      </footer>
    </div>
  )
}
