import { ShieldAlert } from 'lucide-react';
import type { MalpracticeType } from '../../types';
import { MALPRACTICE_LABEL } from '../../utils/constants';
import Button from '../common/Button';
import Modal from '../common/Modal';

interface Props {
  open: boolean;
  count: number;
  max: number;
  type: MalpracticeType | null;
  onContinue: () => void;
}

export default function MalpracticeModal({ open, count, max, type, onContinue }: Props) {
  const left = Math.max(0, max - count);
  return (
    <Modal
      open={open}
      dismissible={false}
      tone="danger"
      title={
        <span className="flex items-center gap-2 text-danger-700">
          <ShieldAlert className="h-5 w-5" /> Warning {count} of {max}
        </span>
      }
      footer={<Button onClick={onContinue}>Return to the test</Button>}
    >
      <p className="font-medium text-navy">{type ? MALPRACTICE_LABEL[type] : 'A rule violation was detected'}.</p>
      <p className="mt-2">
        This was recorded and the administrators can see it.{' '}
        {left > 0 ? (
          <>
            You have <strong>{left}</strong> {left === 1 ? 'warning' : 'warnings'} left. After that your test is submitted automatically and marked as flagged.
          </>
        ) : (
          'Your test is being submitted.'
        )}
      </p>
      <p className="mt-2 text-xs text-navy-400">Your timer keeps running. Stay in fullscreen, on this tab, until you submit.</p>
    </Modal>
  );
}
