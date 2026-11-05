import { Bookmark } from 'lucide-react';
import type { Question } from '../../types';
import OptionButton from './OptionButton';

interface Props {
  question: Question;
  index: number;
  total: number;
  selected: number | null;
  marked: boolean;
  onSelect: (index: number) => void;
  disabled?: boolean;
  language?: 'en' | 'ta';
  onToggleLanguage?: () => void;
}

export default function QuestionCard({
  question,
  index,
  total,
  selected,
  marked,
  onSelect,
  disabled,
  language = 'en',
  onToggleLanguage,
}: Props) {
  const displayText = language === 'ta' && question.text_ta ? question.text_ta : question.text;
  const displayOptions =
    language === 'ta' && question.options_ta && question.options_ta.length === question.options.length
      ? question.options_ta
      : question.options;

  return (
    <article className="panel no-select p-4 sm:p-6" aria-labelledby={`q-${question.id}`}>
      <div className="mb-3 flex items-center justify-between text-sm text-navy-500">
        <div className="flex items-center gap-3">
          <span>
            {language === 'ta' ? `வினா ${index + 1} / ${total}` : `Question ${index + 1} of ${total}`}
          </span>
          {question.text_ta && onToggleLanguage && (
            <button
              type="button"
              onClick={onToggleLanguage}
              className="rounded bg-navy-100/70 px-2 py-0.5 text-xs font-semibold text-navy-700 hover:bg-navy-200 transition-colors"
            >
              {language === 'en' ? '🇮🇳 தமிழ்' : '🇬🇧 English'}
            </button>
          )}
        </div>
        {marked && (
          <span className="inline-flex items-center gap-1 rounded-full bg-cream px-2.5 py-1 text-xs font-medium text-cream-700">
            <Bookmark className="h-3.5 w-3.5" /> {language === 'ta' ? 'மறுஆய்வுக்குக் குறிக்கப்பட்டது' : 'Marked for review'}
          </span>
        )}
      </div>
      <h2 id={`q-${question.id}`} className="paper mb-5 font-normal tracking-normal text-navy-900 leading-relaxed">
        {displayText}
      </h2>
      <div className="space-y-2.5" role="group" aria-label="Answer options">
        {displayOptions.map((opt, i) => (
          <OptionButton
            key={i}
            letter={String.fromCharCode(65 + i)}
            text={opt}
            state={selected === i ? 'selected' : 'idle'}
            onClick={() => onSelect(i)}
            disabled={disabled}
          />
        ))}
      </div>
    </article>
  );
}
