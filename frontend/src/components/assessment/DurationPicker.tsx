interface Props {
  min: number;
  max: number;
  value: number;
  onChange: (minutes: number) => void;
}

export default function DurationPicker({ min, max, value, onChange }: Props) {
  const mid = Math.round((min + max) / 2);
  const presets = Array.from(new Set([min, mid, max]));
  return (
    <fieldset>
      <legend className="label">How long do you want?</legend>
      <div className="flex items-end justify-between">
        <span className="text-3xl font-semibold tabular-nums">{value}<span className="ml-1 text-base font-normal text-navy-500">min</span></span>
        <div className="flex gap-2">
          {presets.map((p) => (
            <button key={p} type="button" onClick={() => onChange(p)} className={`rounded-full border px-3 py-1 text-xs font-medium ${p === value ? 'border-navy bg-navy text-white' : 'border-line bg-white text-navy-600 hover:bg-navy-50'}`}>
              {p} min
            </button>
          ))}
        </div>
      </div>
      <input type="range" min={min} max={max} step={1} value={value} onChange={(e) => onChange(Number(e.target.value))} className="mt-3 w-full accent-sky" aria-label="Duration in minutes" />
      <div className="flex justify-between text-xs text-navy-400"><span>{min} min</span><span>{max} min</span></div>
      {value < max && <p className="mt-2 text-xs text-navy-500">When {value} minutes end you can add the remaining {max - value} minutes once.</p>}
    </fieldset>
  );
}
