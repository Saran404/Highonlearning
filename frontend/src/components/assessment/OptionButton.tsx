import { Check, X } from 'lucide-react';

export type OptionState = 'idle' | 'selected' | 'correct' | 'wrong' | 'missed';

interface Props {
  letter: string;
  text: string;
  state?: OptionState;
  disabled?: boolean;
  onClick?: () => void;
}

const styles: Record<OptionState, string> = {
  idle: 'border-line bg-white hover:border-sky hover:bg-sky-50',
  selected: 'border-navy bg-sky-50 ring-1 ring-navy',
  correct: 'border-mint-600 bg-mint',
  wrong: 'border-danger-600 bg-danger',
  missed: 'border-mint-600 border-dashed bg-white',
};

const badge: Record<OptionState, string> = {
  idle: 'bg-navy-50 text-navy-600',
  selected: 'bg-navy text-white',
  correct: 'bg-mint-600 text-white',
  wrong: 'bg-danger-600 text-white',
  missed: 'bg-mint text-mint-700',
};

export default function OptionButton({ letter, text, state = 'idle', disabled, onClick }: Props) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      aria-pressed={state === 'selected'}
      className={`flex w-full items-start gap-3.5 rounded-2xl border px-4 py-3.5 text-left transition-all m3-touch min-h-[52px] select-none disabled:cursor-default ${styles[state]}`}
    >
      <span className={`mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-full text-sm font-semibold ${badge[state]}`}>
        {state === 'correct' ? <Check className="h-4 w-4" /> : state === 'wrong' ? <X className="h-4 w-4" /> : letter}
      </span>
      <span className="paper !text-base sm:!text-[1.0625rem]">{text}</span>
    </button>
  );
}
