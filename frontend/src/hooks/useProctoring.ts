import { useCallback, useEffect, useRef, useState } from 'react';
import type Webcam from 'react-webcam';
import { proctoringApi } from '../api/proctoring';
import type { TriggerType } from '../types';
import { SNAPSHOT_INTERVAL_MS } from '../utils/constants';
import { detectPersonInVideo, playWarningChime } from '../utils/faceDetector';

interface Options {
  enabled: boolean;
  attemptId: number | null;
  intervalMs?: number;
}

/**
 * Camera proctoring:
 * - START snapshot when camera comes up
 * - INTERVAL snapshots every 30 s
 * - Real-time face/person presence detection with audio/visual warnings
 * - MALPRACTICE and END snapshots on demand
 */
export function useProctoring({ enabled, attemptId, intervalMs = SNAPSHOT_INTERVAL_MS }: Options) {
  const webcamRef = useRef<Webcam>(null);
  const [cameraReady, setCameraReady] = useState(false);
  const [cameraError, setCameraError] = useState<string | null>(null);
  const [personVisible, setPersonVisible] = useState(true);
  const startSent = useRef(false);
  const missingCountRef = useRef(0);
  const chimeDebounceRef = useRef(0);

  const capture = useCallback(
    async (trigger: TriggerType): Promise<boolean> => {
      const shot = webcamRef.current?.getScreenshot();
      if (!shot || attemptId == null) return false;
      try {
        const blob = await (await fetch(shot)).blob();
        await proctoringApi.uploadSnapshot(attemptId, trigger, blob);
        return true;
      } catch (err) {
        console.warn('Snapshot upload failed', err);
        return false;
      }
    },
    [attemptId],
  );

  const onUserMedia = useCallback(() => {
    setCameraReady(true);
    setCameraError(null);
    setPersonVisible(true);
    missingCountRef.current = 0;
    const track = webcamRef.current?.stream?.getVideoTracks()[0];
    track?.addEventListener('ended', () => {
      setCameraReady(false);
      setCameraError('The camera was disconnected.');
    });
  }, []);

  const onUserMediaError = useCallback((err: string | DOMException) => {
    setCameraReady(false);
    setCameraError(
      typeof err === 'string'
        ? err
        : err.name === 'NotAllowedError'
        ? 'Camera permission was denied.'
        : 'The camera could not be started.',
    );
  }, []);

  useEffect(() => {
    if (enabled && cameraReady && !startSent.current) {
      startSent.current = true;
      void capture('START');
    }
  }, [enabled, cameraReady, capture]);

  useEffect(() => {
    if (!enabled || !cameraReady) return;
    const id = window.setInterval(() => void capture('INTERVAL'), intervalMs);
    return () => window.clearInterval(id);
  }, [enabled, cameraReady, capture, intervalMs]);

  // Real-time Face / Person Presence Monitor
  useEffect(() => {
    if (!enabled || !cameraReady) {
      setPersonVisible(true);
      missingCountRef.current = 0;
      return;
    }

    let isCancelled = false;

    const checkPresence = async () => {
      if (isCancelled) return;
      const video = webcamRef.current?.video;
      if (!video) return;

      const res = await detectPersonInVideo(video);
      if (isCancelled) return;

      if (!res.visible) {
        missingCountRef.current += 1;
        // Require 2 consecutive missing cycles (~2.4s) before warning to prevent flutter
        if (missingCountRef.current >= 2) {
          setPersonVisible((prev) => {
            if (prev) {
              const now = Date.now();
              if (now - chimeDebounceRef.current > 12000) {
                chimeDebounceRef.current = now;
                playWarningChime();
              }
            }
            return false;
          });
        }
      } else {
        missingCountRef.current = 0;
        setPersonVisible(true);
      }
    };

    const intervalId = window.setInterval(checkPresence, 1200);

    return () => {
      isCancelled = true;
      window.clearInterval(intervalId);
    };
  }, [enabled, cameraReady]);

  return { webcamRef, cameraReady, cameraError, personVisible, capture, onUserMedia, onUserMediaError };
}
