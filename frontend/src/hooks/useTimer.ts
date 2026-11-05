import { useEffect, useRef, useState } from 'react';

interface Options {
  /** Deadline as epoch ms (server time). 0 = not started. */
  deadlineMs: number;
  /** server clock - client clock, in ms */
  offsetMs: number;
  /** true while an extension can still be requested */
  canExtend: boolean;
  onExtensionAvailable: () => void;
  onExpire: () => void;
}

/**
 * Countdown driven by the wall clock (not by counting ticks), so throttled background tabs and
 * sleeping laptops cannot drift. At zero it either opens the extension flow or expires the attempt,
 * once per deadline.
 */
export function useTimer({ deadlineMs, offsetMs, canExtend, onExtensionAvailable, onExpire }: Options) {
  const [remaining, setRemaining] = useState<number>(() => (deadlineMs ? Math.max(0, Math.ceil((deadlineMs - (Date.now() + offsetMs)) / 1000)) : 0));
  const firedFor = useRef<number | null>(null);
  const canExtendRef = useRef(canExtend);
  const extRef = useRef(onExtensionAvailable);
  const expireRef = useRef(onExpire);
  canExtendRef.current = canExtend;
  extRef.current = onExtensionAvailable;
  expireRef.current = onExpire;

  useEffect(() => {
    if (!deadlineMs) return;
    const tick = () => {
      const left = Math.max(0, Math.ceil((deadlineMs - (Date.now() + offsetMs)) / 1000));
      setRemaining(left);
      if (left <= 0 && firedFor.current !== deadlineMs) {
        firedFor.current = deadlineMs;
        if (canExtendRef.current) extRef.current();
        else expireRef.current();
      }
    };
    tick();
    const id = window.setInterval(tick, 250);
    return () => window.clearInterval(id);
  }, [deadlineMs, offsetMs]);

  return { remaining, isLow: remaining <= 300, isCritical: remaining <= 60 };
}
