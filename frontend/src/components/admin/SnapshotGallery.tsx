import { Camera } from 'lucide-react';
import { useState } from 'react';
import { assetUrl } from '../../api/client';
import type { Snapshot } from '../../types';
import { formatDate } from '../../utils/format';
import EmptyState from '../common/EmptyState';
import Modal from '../common/Modal';

const triggerTone: Record<string, string> = {
  START: 'bg-sky-100 text-sky-800',
  INTERVAL: 'bg-navy-100 text-navy-600',
  MALPRACTICE: 'bg-danger text-danger-700',
  END: 'bg-mint text-mint-700',
};

/** Thumbnail grid; tap a photo to enlarge. Malpractice snapshots are tagged in red. */
export default function SnapshotGallery({ snapshots }: { snapshots: Snapshot[] }) {
  const [open, setOpen] = useState<Snapshot | null>(null);
  if (snapshots.length === 0) return <EmptyState icon={<Camera className="h-8 w-8" />} title="No snapshots" description="No camera photos were captured for this attempt." />;
  return (
    <>
      <ul className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
        {snapshots.map((s) => (
          <li key={s.snapshot_id}>
            <button onClick={() => setOpen(s)} className="group block w-full overflow-hidden rounded-lg border border-line bg-white text-left">
              <img src={assetUrl(s.image_url)} alt={`Snapshot at ${formatDate(s.captured_at, 'h:mm:ss a')}`} loading="lazy" className="aspect-[4/3] w-full object-cover" />
              <div className="flex items-center justify-between gap-2 px-2 py-1.5 text-xs">
                <span className="tabular-nums text-navy-500">{formatDate(s.captured_at, 'h:mm:ss a')}</span>
                <span className={`rounded-full px-2 py-0.5 font-medium ${triggerTone[s.trigger_type]}`}>{s.trigger_type.toLowerCase()}</span>
              </div>
            </button>
          </li>
        ))}
      </ul>
      <Modal open={Boolean(open)} onClose={() => setOpen(null)} size="lg" title={open ? `${open.trigger_type.toLowerCase()} · ${formatDate(open.captured_at)}` : ''}>
        {open && <img src={assetUrl(open.image_url)} alt="Enlarged snapshot" className="w-full rounded-lg" />}
      </Modal>
    </>
  );
}
