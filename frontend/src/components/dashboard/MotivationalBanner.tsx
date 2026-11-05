import { Quote } from 'lucide-react';

export default function MotivationalBanner({ name, quote }: { name: string; quote: string }) {
  return (
    <div className="flex items-start gap-3.5 rounded-xl border border-amber-200/80 bg-gradient-to-r from-amber-50/90 via-amber-50/50 to-sky-50/40 px-4 py-4 sm:px-5 shadow-xs">
      <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-amber-500/10 text-amber-600">
        <Quote className="h-4 w-4" aria-hidden />
      </div>
      <div>
        <h1 className="text-xl sm:text-2xl text-navy-900 font-bold">Hi, {name.split(' ')[0]} 👋</h1>
        <p className="mt-1 text-sm text-navy-700 leading-relaxed">{quote}</p>
      </div>
    </div>
  );
}
