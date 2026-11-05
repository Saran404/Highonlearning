import { CameraOff, UserCheck, UserX } from 'lucide-react';
import { useState, type RefObject } from 'react';
import Webcam from 'react-webcam';

interface Props {
  webcamRef: RefObject<Webcam>;
  ready: boolean;
  error: string | null;
  personVisible?: boolean;
  onUserMedia: () => void;
  onUserMediaError: (e: string | DOMException) => void;
}

/** Small self-view. The same <Webcam> is what the proctoring hook captures snapshots from. */
export default function CameraPreview({
  webcamRef,
  ready,
  error,
  personVisible = true,
  onUserMedia,
  onUserMediaError,
}: Props) {
  const [expanded, setExpanded] = useState(false);

  const hasWarning = ready && !error && !personVisible;

  return (
    <>
      <button
        type="button"
        onClick={() => setExpanded((prev) => !prev)}
        className={`group relative h-11 w-14 overflow-hidden rounded-md bg-navy-800 transition-all sm:h-14 sm:w-[4.5rem] focus:outline-hidden ${
          hasWarning
            ? 'ring-2 ring-danger-500 ring-offset-2 ring-offset-navy animate-pulse'
            : 'ring-1 ring-white/20 hover:ring-white/40'
        }`}
        title={
          error ??
          (hasWarning
            ? 'Warning: Person not visible in camera!'
            : ready
            ? 'Camera active · Tap to expand'
            : 'Starting camera…')
        }
        aria-label="Proctoring camera preview"
      >
        <Webcam
          ref={webcamRef}
          audio={false}
          mirrored
          screenshotFormat="image/jpeg"
          screenshotQuality={0.7}
          videoConstraints={{ facingMode: 'user', width: 640, height: 480 }}
          onUserMedia={onUserMedia}
          onUserMediaError={onUserMediaError}
          className="h-full w-full object-cover"
          playsInline
        />

        {error && (
          <div className="absolute inset-0 flex items-center justify-center bg-danger text-danger-700">
            <CameraOff className="h-5 w-5" aria-label={error} />
          </div>
        )}

        {hasWarning && (
          <div className="absolute inset-x-0 bottom-0 flex items-center justify-center gap-0.5 bg-danger-600/95 py-0.5 text-[8px] font-bold text-white uppercase tracking-tight sm:text-[9px]">
            <UserX className="h-2.5 w-2.5" /> NO FACE
          </div>
        )}

        {/* Status Indicator Dot */}
        <span
          className={`absolute bottom-1 right-1 h-2 w-2 rounded-full ring-1 ring-black/40 ${
            error
              ? 'bg-danger-600'
              : hasWarning
              ? 'bg-danger-500 animate-ping'
              : ready
              ? 'bg-mint-500'
              : 'bg-cream-600'
          }`}
          aria-hidden
        />
      </button>

      {/* Expanded Modal/Overlay for checking face alignment on mobile & desktop */}
      {expanded && ready && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4 backdrop-blur-xs"
          onClick={() => setExpanded(false)}
        >
          <div
            className="relative w-full max-w-xs overflow-hidden rounded-2xl border-2 border-white/20 bg-navy-900 p-4 text-white shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="mb-2 flex items-center justify-between">
              <span className="flex items-center gap-1.5 text-xs font-semibold">
                {hasWarning ? (
                  <span className="flex items-center gap-1 text-danger-400 font-bold">
                    <UserX className="h-4 w-4" /> Face Not Detected
                  </span>
                ) : (
                  <span className="flex items-center gap-1 text-mint-400 font-bold">
                    <UserCheck className="h-4 w-4" /> Face Visible
                  </span>
                )}
              </span>
              <button
                type="button"
                onClick={() => setExpanded(false)}
                className="rounded-full bg-white/10 px-2 py-0.5 text-xs text-white/80 hover:bg-white/20"
              >
                Close
              </button>
            </div>

            <div className={`relative aspect-4/3 overflow-hidden rounded-xl bg-black ${hasWarning ? 'ring-2 ring-danger-500' : 'ring-1 ring-white/20'}`}>
              <Webcam
                audio={false}
                mirrored
                className="h-full w-full object-cover"
                videoConstraints={{ facingMode: 'user' }}
                playsInline
              />
              <div className="pointer-events-none absolute inset-4 rounded-full border-2 border-dashed border-white/40" />
            </div>

            <p className="mt-2 text-center text-[11px] text-white/70">
              {hasWarning
                ? 'Please center your face inside the circle guide.'
                : 'Your face is clearly visible to the proctoring system.'}
            </p>
          </div>
        </div>
      )}
    </>
  );
}
