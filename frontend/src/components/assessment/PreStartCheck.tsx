import { Camera, CheckCircle2, Loader2, Maximize, Wifi, XCircle } from 'lucide-react';
import { ReactNode, useCallback, useEffect, useState } from 'react';
import Button from '../common/Button';

type Status = 'idle' | 'testing' | 'ok' | 'fail';

interface Props {
  requireCamera: boolean;
  requireFullscreen: boolean;
  onChange: (allPassed: boolean) => void;
}

function Row({ icon, title, hint, status, action }: { icon: ReactNode; title: string; hint: string; status: Status; action?: ReactNode }) {
  return (
    <li className="flex items-center gap-3 py-3">
      <span className="text-navy-400">{icon}</span>
      <div className="min-w-0 flex-1">
        <div className="text-sm font-medium">{title}</div>
        <div className="text-xs text-navy-500">{hint}</div>
      </div>
      {action}
      {status === 'ok' && <CheckCircle2 className="h-5 w-5 text-mint-600" aria-label="Passed" />}
      {status === 'fail' && <XCircle className="h-5 w-5 text-danger-600" aria-label="Failed" />}
      {status === 'testing' && <Loader2 className="h-5 w-5 animate-spin text-sky" aria-label="Checking" />}
    </li>
  );
}

/** System checks: connection, fullscreen support, camera permission. Reports overall pass/fail upward. */
export default function PreStartCheck({ requireCamera, requireFullscreen, onChange }: Props) {
  const [online, setOnline] = useState<boolean>(navigator.onLine);
  const [camera, setCamera] = useState<Status>('idle');
  const fullscreenOk = typeof document.documentElement.requestFullscreen === 'function';

  useEffect(() => {
    const up = () => setOnline(true);
    const down = () => setOnline(false);
    window.addEventListener('online', up);
    window.addEventListener('offline', down);
    return () => {
      window.removeEventListener('online', up);
      window.removeEventListener('offline', down);
    };
  }, []);

  const testCamera = useCallback(async () => {
    setCamera('testing');
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' } });
      stream.getTracks().forEach((t) => t.stop());
      setCamera('ok');
    } catch {
      setCamera('fail');
    }
  }, []);

  const passed = online && (!requireFullscreen || fullscreenOk) && (!requireCamera || camera === 'ok');
  useEffect(() => onChange(passed), [passed, onChange]);

  return (
    <div>
      <h3 className="label">System check</h3>
      <ul className="divide-y divide-line rounded-xl border border-line bg-white px-4">
        <Row icon={<Wifi className="h-5 w-5" />} title="Internet connection" hint={online ? 'Connected' : 'You are offline. Reconnect to continue.'} status={online ? 'ok' : 'fail'} />
        {requireFullscreen && (
          <Row icon={<Maximize className="h-5 w-5" />} title="Fullscreen mode" hint={fullscreenOk ? 'Supported by this browser' : 'Not supported here. Use Chrome, Edge or Firefox on a laptop or desktop.'} status={fullscreenOk ? 'ok' : 'fail'} />
        )}
        {requireCamera && (
          <Row
            icon={<Camera className="h-5 w-5" />}
            title="Camera"
            hint={camera === 'fail' ? 'Blocked or not found. Allow camera access in the address bar, then test again.' : camera === 'ok' ? 'Camera works' : 'Needed for proctoring snapshots'}
            status={camera}
            action={camera !== 'ok' && <Button size="sm" variant="secondary" onClick={testCamera} loading={camera === 'testing'}>{camera === 'fail' ? 'Test again' : 'Test camera'}</Button>}
          />
        )}
      </ul>
    </div>
  );
}
