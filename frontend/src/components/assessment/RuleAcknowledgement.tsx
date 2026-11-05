interface Ack {
  no_minimize: boolean;
  consent_camera: boolean;
  single_attempt: boolean;
}

interface Props {
  value: Ack;
  onChange: (v: Ack) => void;
  maxStrikes?: number;
  snapshotSeconds?: number;
}

export default function RuleAcknowledgement({ value, onChange, maxStrikes = 3, snapshotSeconds = 30 }: Props) {
  const rows: { key: keyof Ack; text: string }[] = [
    { key: 'no_minimize', text: `I will stay in fullscreen on this tab. Switching tabs, minimising, opening developer tools, or copy-pasting is recorded, and after ${maxStrikes} warnings my test is submitted automatically.` },
    { key: 'consent_camera', text: `I allow my camera to take a photo every ${snapshotSeconds} seconds and whenever a warning is recorded. I understand the photos are stored and reviewed by administrators.` },
    { key: 'single_attempt', text: "I understand this is a single attempt. Once I start, I can't restart it, and the timer keeps running if I leave." },
  ];
  return (
    <fieldset>
      <legend className="label">Before you begin</legend>
      <ul className="space-y-2.5">
        {rows.map((r) => (
          <li key={r.key}>
            <label className={`flex cursor-pointer items-start gap-3 rounded-xl border p-3 text-sm ${value[r.key] ? 'border-mint-600 bg-mint/50' : 'border-line bg-white'}`}>
              <input type="checkbox" checked={value[r.key]} onChange={(e) => onChange({ ...value, [r.key]: e.target.checked })} className="mt-0.5 h-4 w-4 accent-navy" />
              <span>{r.text}</span>
            </label>
          </li>
        ))}
      </ul>
    </fieldset>
  );
}
