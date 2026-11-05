import { useCallback, useEffect, useRef, useState } from 'react';
import type { MalpracticeType } from '../types';

interface Options {
  enabled: boolean;
  onViolation: (type: MalpracticeType, meta?: Record<string, unknown>) => void;
}

/** One physical action (Alt+Tab) fires visibilitychange + blur + fullscreenchange: count it once. */
const DEDUPE_MS = 1500;

const isTouchDevice = (): boolean => 'ontouchstart' in window || navigator.maxTouchPoints > 0;

/**
 * Lockdown browser behaviour for graded attempts:
 *  - fullscreen tracking (exit = violation)
 *  - tab switch / window blur detection
 *  - blocked context menu, copy/cut/paste, view-source, print, save, reload, devtools shortcuts
 *  - devtools-open heuristic (docked panels change the window size)
 *  - "leave page?" prompt
 *
 * Browsers cannot be fully locked down from a web page - these checks deter and record, and the
 * server keeps the authoritative strike count.
 */
export function useLockdown({ enabled, onViolation }: Options) {
  const [isFullscreen, setIsFullscreen] = useState<boolean>(() => Boolean(document.fullscreenElement));
  const fullscreenSupported = typeof document.documentElement.requestFullscreen === 'function';
  const callback = useRef(onViolation);
  callback.current = onViolation;
  const lastFired = useRef(0);

  const fire = useCallback((type: MalpracticeType, meta?: Record<string, unknown>) => {
    const now = Date.now();
    if (now - lastFired.current < DEDUPE_MS) return;
    lastFired.current = now;
    callback.current(type, meta);
  }, []);

  const enterFullscreen = useCallback(async () => {
    try {
      if (!document.fullscreenElement) await document.documentElement.requestFullscreen();
    } catch {
      /* denied or unsupported */
    }
  }, []);

  const exitFullscreen = useCallback(async () => {
    try {
      if (document.fullscreenElement) await document.exitFullscreen();
    } catch {
      /* ignore */
    }
  }, []);

  useEffect(() => {
    const onFs = () => {
      const fs = Boolean(document.fullscreenElement);
      setIsFullscreen(fs);
      if (!fs && enabled) fire('FULLSCREEN_EXIT');
    };
    document.addEventListener('fullscreenchange', onFs);
    return () => document.removeEventListener('fullscreenchange', onFs);
  }, [enabled, fire]);

  useEffect(() => {
    if (!enabled) return;

    const onVisibility = () => {
      if (document.hidden) fire('TAB_SWITCH');
    };
    const onBlur = () => {
      window.setTimeout(() => {
        if (!document.hidden && !document.hasFocus()) fire('MINIMIZE');
      }, 0);
    };
    const block = (e: Event) => e.preventDefault();
    const onContext = (e: Event) => {
      e.preventDefault();
      fire('RIGHT_CLICK');
    };
    const onClipboard = (e: Event) => {
      e.preventDefault();
      fire('COPY_PASTE', { event: e.type });
    };
    const onKey = (e: KeyboardEvent) => {
      const k = e.key.toLowerCase();
      const mod = e.ctrlKey || e.metaKey;
      if (e.key === 'F12' || (mod && e.shiftKey && ['i', 'j', 'c'].includes(k)) || (mod && k === 'u')) {
        e.preventDefault();
        fire('DEVTOOLS', { via: 'shortcut' });
        return;
      }
      if (e.key === 'F5' || (mod && ['r', 'p', 's', 'f', 'g'].includes(k))) e.preventDefault();
    };
    const onBeforeUnload = (e: BeforeUnloadEvent) => {
      e.preventDefault();
      e.returnValue = '';
    };

    document.addEventListener('visibilitychange', onVisibility);
    window.addEventListener('blur', onBlur);
    document.addEventListener('contextmenu', onContext);
    document.addEventListener('copy', onClipboard);
    document.addEventListener('cut', onClipboard);
    document.addEventListener('paste', onClipboard);
    document.addEventListener('selectstart', block);
    document.addEventListener('dragstart', block);
    window.addEventListener('keydown', onKey, true);
    window.addEventListener('beforeunload', onBeforeUnload);

    // Devtools heuristic: only meaningful on desktop while fullscreen (outer vs inner size).
    let devtoolsOpen = false;
    const poll = window.setInterval(() => {
      if (isTouchDevice() || !document.fullscreenElement) return;
      const open = window.outerWidth - window.innerWidth > 160 || window.outerHeight - window.innerHeight > 200;
      if (open && !devtoolsOpen) fire('DEVTOOLS', { via: 'window-size' });
      devtoolsOpen = open;
    }, 2000);

    return () => {
      document.removeEventListener('visibilitychange', onVisibility);
      window.removeEventListener('blur', onBlur);
      document.removeEventListener('contextmenu', onContext);
      document.removeEventListener('copy', onClipboard);
      document.removeEventListener('cut', onClipboard);
      document.removeEventListener('paste', onClipboard);
      document.removeEventListener('selectstart', block);
      document.removeEventListener('dragstart', block);
      window.removeEventListener('keydown', onKey, true);
      window.removeEventListener('beforeunload', onBeforeUnload);
      window.clearInterval(poll);
    };
  }, [enabled, fire]);

  return { isFullscreen, fullscreenSupported, enterFullscreen, exitFullscreen };
}
