import { Hourglass } from 'lucide-react';
import Button from '../common/Button';
import Modal from '../common/Modal';

interface Props {
  open: boolean;
  chosenMinutes: number;
  defaultMinutes: number;
  secondsLeftToDecide: number;
  loading?: boolean;
  onExtend: () => void;
  onSubmit: () => void;
}

/** Shown when the chosen duration ends but the assessment's full duration has not. */
export default function DurationExtensionModal({ open, chosenMinutes, defaultMinutes, secondsLeftToDecide, loading, onExtend, onSubmit }: Props) {
  const extra = defaultMinutes - chosenMinutes;
  return (
    <Modal
      open={open}
      dismissible={false}
      tone="warning"
      title={
        <span className="flex items-center gap-2">
          <Hourglass className="h-5 w-5 text-cream-600" /> Your {chosenMinutes} minutes are up
        </span>
      }
      footer={
        <>
          <Button variant="secondary" onClick={onSubmit} disabled={loading}>Submit now</Button>
          <Button onClick={onExtend} loading={loading}>Add {extra} more minutes</Button>
        </>
      }
    >
      <p>
        This test allows up to {defaultMinutes} minutes. You can use the extra <strong>{extra} minutes</strong> once. Your answers so far are saved.
      </p>
      <p className="mt-2 text-xs text-navy-500">If you don't choose in {secondsLeftToDecide}s, the test is submitted automatically.</p>
    </Modal>
  );
}
