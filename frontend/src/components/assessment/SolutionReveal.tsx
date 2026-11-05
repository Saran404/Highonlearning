import { useMemo, useState } from 'react';
import type { ResultQuestion } from '../../types';
import OptionButton, { OptionState } from './OptionButton';

type Filter = 'all' | 'wrong' | 'skipped';

function stateFor(q: ResultQuestion, i: number): OptionState {
  if (i === q.correct_index) return q.selected_index === i ? 'correct' : 'missed';
  if (q.selected_index === i) return 'wrong';
  return 'idle';
}

/** Full solutions: your answer, the correct answer and the explanation for every question. */
export default function SolutionReveal({ questions }: { questions: ResultQuestion[] }) {
  const [filter, setFilter] = useState<Filter>('all');
  const [language, setLanguage] = useState<'en' | 'ta'>(() => {
    const saved = localStorage.getItem('exampro_lang');
    return saved === 'ta' ? 'ta' : 'en';
  });

  const counts = useMemo(
    () => ({
      all: questions.length,
      wrong: questions.filter((q) => q.selected_index != null && !q.is_correct).length,
      skipped: questions.filter((q) => q.selected_index == null).length,
    }),
    [questions],
  );
  const shown = questions
    .map((q, i) => ({ q, n: i + 1 }))
    .filter(({ q }) => (filter === 'all' ? true : filter === 'wrong' ? q.selected_index != null && !q.is_correct : q.selected_index == null));

  return (
    <div>
      <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
        <div className="flex flex-wrap gap-2" role="tablist" aria-label="Filter solutions">
          {([['all', 'All'], ['wrong', 'Wrong'], ['skipped', 'Skipped']] as [Filter, string][]).map(([key, label]) => (
            <button
              key={key}
              role="tab"
              aria-selected={filter === key}
              onClick={() => setFilter(key)}
              className={`rounded-full border px-3.5 py-1.5 text-sm font-medium ${
                filter === key ? 'border-navy bg-navy text-white' : 'border-line bg-white text-navy-600 hover:bg-navy-50'
              }`}
            >
              {label} <span className="opacity-70">{counts[key]}</span>
            </button>
          ))}
        </div>

        {/* Language Switcher */}
        <div className="flex items-center gap-1 rounded-lg bg-navy-50 p-1 border border-line text-xs font-semibold">
          <button
            type="button"
            onClick={() => {
              setLanguage('en');
              localStorage.setItem('exampro_lang', 'en');
            }}
            className={`rounded px-2.5 py-1 transition-all ${
              language === 'en' ? 'bg-sky-600 text-white shadow-xs' : 'text-navy-600 hover:bg-navy-200/50'
            }`}
          >
            🇬🇧 EN
          </button>
          <button
            type="button"
            onClick={() => {
              setLanguage('ta');
              localStorage.setItem('exampro_lang', 'ta');
            }}
            className={`rounded px-2.5 py-1 transition-all ${
              language === 'ta' ? 'bg-sky-600 text-white shadow-xs' : 'text-navy-600 hover:bg-navy-200/50'
            }`}
          >
            🇮🇳 தமிழ்
          </button>
        </div>
      </div>

      {shown.length === 0 && <p className="rounded-lg bg-mint px-4 py-3 text-sm text-mint-700">Nothing here — nice work.</p>}
      <ol className="space-y-4">
        {shown.map(({ q, n }) => {
          const displayText = language === 'ta' && q.question_text_ta ? q.question_text_ta : q.question_text;
          const displayOptions = language === 'ta' && q.options_ta && q.options_ta.length === q.options.length ? q.options_ta : q.options;
          const displayExplanation = language === 'ta' && q.explanation_ta ? q.explanation_ta : q.explanation;

          return (
            <li key={q.question_id} className="panel p-4 sm:p-5">
              <div className="mb-2 flex items-center justify-between text-xs">
                <span className="text-navy-500">{language === 'ta' ? `வினா ${n}` : `Question ${n}`}</span>
                <span className={`rounded-full px-2.5 py-1 font-medium ${q.is_correct ? 'bg-mint text-mint-700' : q.selected_index == null ? 'bg-navy-100 text-navy-600' : 'bg-danger text-danger-700'}`}>
                  {q.is_correct ? (language === 'ta' ? 'சரி' : 'Correct') : q.selected_index == null ? (language === 'ta' ? 'விடையளிக்கவில்லை' : 'Not answered') : (language === 'ta' ? 'தவறு' : 'Incorrect')}
                </span>
              </div>
              <p className="paper mb-3 font-normal text-navy-900 leading-relaxed">{displayText}</p>
              <div className="space-y-2">
                {displayOptions.map((opt, i) => (
                  <OptionButton key={i} letter={String.fromCharCode(65 + i)} text={opt} state={stateFor(q, i)} disabled />
                ))}
              </div>
              {displayExplanation && (
                <div className="mt-3 rounded-lg border-l-4 border-sky bg-sky-50 px-3.5 py-3 text-sm">
                  <div className="mb-0.5 font-semibold text-sky-800">{language === 'ta' ? 'விளக்கம்' : 'Explanation'}</div>
                  <p className="text-navy-800 leading-relaxed">{displayExplanation}</p>
                </div>
              )}
            </li>
          );
        })}
      </ol>
    </div>
  );
}
