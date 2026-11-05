import { useEffect, useState, useRef, useCallback } from 'react';
import { createPortal } from 'react-dom';
import { ShieldAlert, Lock, Smartphone, Laptop } from 'lucide-react';
import toast from 'react-hot-toast';
import { useAuthStore } from '../../store/authStore';

const RESTRICTED_NOTICE =
  'SCREENSHOT RESTRICTED: Capturing course materials and assessments on HighOnLearning is strictly prohibited.';

// Cached 100% solid-black blank PNG image blob (Zero text, pure black)
let cachedBlankPngBlob: Blob | null = null;

function getBlankPngBlob(): Promise<Blob> {
  if (cachedBlankPngBlob) {
    return Promise.resolve(cachedBlankPngBlob);
  }
  return new Promise((resolve) => {
    try {
      const canvas = document.createElement('canvas');
      canvas.width = 1920;
      canvas.height = 1080;
      const ctx = canvas.getContext('2d');
      if (ctx) {
        // Pure solid pitch black - 100% #000000 with zero text or markings
        ctx.fillStyle = '#000000';
        ctx.fillRect(0, 0, 1920, 1080);
      }
      canvas.toBlob((blob) => {
        cachedBlankPngBlob = blob || new Blob([], { type: 'image/png' });
        resolve(cachedBlankPngBlob);
      }, 'image/png');
    } catch {
      resolve(new Blob([], { type: 'image/png' }));
    }
  });
}

// Dedicated full-screen solid black shield DOM element
let solidBlackShield: HTMLDivElement | null = null;

function getOrCreateSolidBlackShield(): HTMLDivElement {
  if (!solidBlackShield) {
    let el = document.getElementById('hl-solid-black-shield') as HTMLDivElement | null;
    if (!el) {
      el = document.createElement('div');
      el.id = 'hl-solid-black-shield';
      el.style.position = 'fixed';
      el.style.top = '0';
      el.style.left = '0';
      el.style.width = '100vw';
      el.style.height = '100vh';
      el.style.backgroundColor = '#000000';
      el.style.zIndex = '2147483645';
      el.style.display = 'none';
      el.style.pointerEvents = 'auto';
      document.body.appendChild(el);
    }
    solidBlackShield = el;
  }
  return solidBlackShield;
}

/**
 * Synchronous instant blanking of the entire document viewport and display of restriction screen.
 * Forces an immediate DOM layout reflow so the compositor commits the restriction screen with 0 latency.
 */
function applyInstantBlank(reason?: string, source?: 'web' | 'mobile') {
  const shield = getOrCreateSolidBlackShield();
  shield.style.display = 'block';
  document.documentElement.style.backgroundColor = '#000000';
  document.body.style.backgroundColor = '#000000';
  document.documentElement.classList.add('screen-capture-protected');
  document.body.classList.add('screen-capture-protected');

  const root = document.getElementById('root');
  if (root) {
    root.style.visibility = 'hidden';
    root.style.opacity = '0';
    root.style.pointerEvents = 'none';
  }

  const overlay = document.getElementById('hl-restriction-overlay');
  if (overlay) {
    overlay.style.display = 'flex';
    if (reason) {
      const descEl = document.getElementById('screenshot-modal-desc');
      if (descEl) descEl.textContent = reason;
    }
    if (source) {
      const titleEl = document.getElementById('hl-restriction-platform-title');
      const descEl = document.getElementById('hl-restriction-platform-desc');
      if (titleEl) {
        titleEl.textContent =
          source === 'mobile'
            ? 'Mobile Protection Active'
            : 'System Protection Active (PrintScreen & Snipping Tool Blocked)';
      }
      if (descEl) {
        descEl.textContent =
          source === 'mobile'
            ? 'Screenshots via buttons (Power + Volume) and gestures are restricted across all sections.'
            : 'PrintScreen (normal click or long press) and Snipping Tool are restricted across all sections.';
      }
    }
    // Force layout flush so compositor commits the restriction overlay immediately
    void overlay.offsetHeight;
  }

  // Force layout flush so compositor commits the black shield immediately
  void shield.offsetHeight;
}

function removeInstantBlank() {
  const shield = getOrCreateSolidBlackShield();
  shield.style.display = 'none';

  const overlay = document.getElementById('hl-restriction-overlay');
  if (overlay) {
    overlay.style.display = 'none';
  }

  document.documentElement.style.backgroundColor = '';
  document.body.style.backgroundColor = '';
  document.documentElement.classList.remove('screen-capture-protected');
  document.body.classList.remove('screen-capture-protected');

  const root = document.getElementById('root');
  if (root) {
    root.style.visibility = '';
    root.style.opacity = '';
    root.style.pointerEvents = '';
  }
}

/**
 * Enterprise Screenshot & Screen-Capture Neutralization System:
 * - Active ONLY after user login for regular users/students (Admins are exempt).
 * - System (Desktop):
 *   - Normal click or LONG PRESS of PrintScreen immediately results in the restriction screen
 *     and solid black canvas, preventing course materials from being captured.
 *   - Snipping Tool (Win+Shift+S / Snipping Tool app) immediately results in the restriction screen.
 * - Mobile:
 *   - Hardware shortcuts (Power + Volume Down / Volume Up): immediately results in restriction screen.
 *   - Screenshot buttons (Quick settings / notification shade / recent apps): results in restriction screen.
 *   - Multi-touch gestures (3-finger swipe): results in restriction screen.
 * - Guarantees that any screenshot taken results only with the restriction screen and black canvas.
 */
export default function ScreenshotProtection() {
  const { user, isAuthenticated } = useAuthStore();

  // Restriction applies ONLY after user login for regular users (Admins are completely exempt)
  const isRestrictedUser = Boolean(isAuthenticated && user && user.role !== 'ADMIN');

  // Check accurately if user is on mobile platform (phones/tablets), not touch laptops
  const isMobilePlatform =
    typeof navigator !== 'undefined' &&
    (/Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ||
      (navigator.userAgent.includes('Macintosh') && navigator.maxTouchPoints > 2));

  const [modalActive, setModalActive] = useState(false);
  const [modalReason, setModalReason] = useState('');
  const [triggerSource, setTriggerSource] = useState<'web' | 'mobile'>(
    isMobilePlatform ? 'mobile' : 'web'
  );

  const lastToastTime = useRef(0);
  const wasBlurredRef = useRef(false);
  const wasScreenshotAttemptRef = useRef(false);

  // References to handle continuous long-press of PrintScreen button
  const isPrtScnHeldRef = useRef(false);
  const prtScnHoldIntervalRef = useRef<number | null>(null);
  const activeWipeTimersRef = useRef<number[]>([]);

  const notifyToast = useCallback((msg: string) => {
    const now = Date.now();
    if (now - lastToastTime.current > 2000) {
      lastToastTime.current = now;
      toast.error(msg, { id: 'anti-screenshot-toast', duration: 2500 });
    }
  }, []);

  /**
   * Overwrite clipboard with 100% pure solid black PNG image and plain text notice.
   */
  const overwriteClipboardWithPureBlack = useCallback(() => {
    // 1. Synchronous plain-text overwrite via execCommand
    try {
      const textarea = document.createElement('textarea');
      textarea.value = RESTRICTED_NOTICE;
      textarea.setAttribute('readonly', '');
      textarea.style.position = 'fixed';
      textarea.style.left = '-9999px';
      textarea.style.top = '-9999px';
      textarea.style.opacity = '0';
      document.body.appendChild(textarea);
      textarea.focus();
      textarea.select();
      textarea.setSelectionRange(0, 99999);
      document.execCommand('copy');
      document.body.removeChild(textarea);
    } catch {
      /* ignore execCommand failure */
    }

    // 2. Modern Clipboard API: Overwrite clipboard with pure black PNG
    getBlankPngBlob().then((blankBlob) => {
      try {
        if (navigator.clipboard && navigator.clipboard.write) {
          const item = new ClipboardItem({
            'image/png': blankBlob,
            'text/plain': new Blob([RESTRICTED_NOTICE], { type: 'text/plain' }),
          });
          navigator.clipboard.write([item]).catch(() => {});
        }
      } catch {
        /* ignore */
      }
    });
  }, []);

  /**
   * Schedule multi-interval clipboard wipes (with extended support for long-press).
   */
  const scheduleClipboardWipes = useCallback(
    (extended = false) => {
      overwriteClipboardWithPureBlack();
      activeWipeTimersRef.current.forEach((t) => window.clearTimeout(t));
      activeWipeTimersRef.current = [];

      const delays = extended
        ? [10, 30, 60, 100, 200, 400, 800, 1200, 1800, 2500, 3500, 5000]
        : [10, 30, 60, 120, 250, 500, 1000, 2000];

      delays.forEach((delay) => {
        const id = window.setTimeout(overwriteClipboardWithPureBlack, delay);
        activeWipeTimersRef.current.push(id);
      });
    },
    [overwriteClipboardWithPureBlack]
  );

  /**
   * Trigger the prominent "Screenshot is Restricted" modal popup with 0ms delay.
   */
  const triggerRestrictionModal = useCallback(
    (reason: string, source: 'web' | 'mobile' = 'web') => {
      applyInstantBlank(reason, source);
      scheduleClipboardWipes(true);
      setModalReason(reason);
      setTriggerSource(source);
      setModalActive(true);
      notifyToast(reason);
    },
    [scheduleClipboardWipes, notifyToast]
  );

  /**
   * Continuous scrubbing while PrintScreen is being long-pressed.
   */
  const startPrtScnHold = useCallback(() => {
    isPrtScnHeldRef.current = true;
    wasScreenshotAttemptRef.current = true;
    const defaultReason = isMobilePlatform
      ? 'Mobile screenshot attempt was restricted. Application page was blanked.'
      : 'Screenshot key (PrintScreen) is restricted. Application page was blanked.';
    const defaultSource = isMobilePlatform ? 'mobile' : 'web';

    triggerRestrictionModal(defaultReason, defaultSource);

    if (prtScnHoldIntervalRef.current) {
      window.clearInterval(prtScnHoldIntervalRef.current);
    }

    prtScnHoldIntervalRef.current = window.setInterval(() => {
      applyInstantBlank(defaultReason, defaultSource);
      overwriteClipboardWithPureBlack();
    }, 30);
  }, [triggerRestrictionModal, overwriteClipboardWithPureBlack, isMobilePlatform]);

  const stopPrtScnHold = useCallback(() => {
    isPrtScnHeldRef.current = false;
    if (prtScnHoldIntervalRef.current) {
      window.clearInterval(prtScnHoldIntervalRef.current);
      prtScnHoldIntervalRef.current = null;
    }
    scheduleClipboardWipes(true);
  }, [scheduleClipboardWipes]);

  const dismissModal = useCallback(() => {
    stopPrtScnHold();
    removeInstantBlank();
    setModalActive(false);
    wasBlurredRef.current = false;
    wasScreenshotAttemptRef.current = false;
  }, [stopPrtScnHold]);

  useEffect(() => {
    // Only logged-in regular users are restricted; unauthenticated visitors and admins are exempt
    if (!isRestrictedUser) {
      removeInstantBlank();
      return;
    }

    // Pre-cache pure black PNG blob
    void getBlankPngBlob();

    // Attach direct click handler to Resume Learning button
    const resumeBtn = document.getElementById('hl-resume-learning-btn');
    if (resumeBtn) {
      resumeBtn.addEventListener('click', dismissModal);
    }

    // ----------------------------------------------------
    // 1. Key Interception: PrintScreen (Normal & Long Press), Snipping shortcuts, and Mobile Volume shortcuts
    // ----------------------------------------------------
    const handleKeyDown = (e: KeyboardEvent) => {
      const key = (e.key || '').toLowerCase();
      const code = (e.code || '').toLowerCase();
      const isMod = e.ctrlKey || e.metaKey;

      // A. PrintScreen / Snapshot key (Handles initial press and long-press)
      if (
        key === 'printscreen' ||
        key === 'snapshot' ||
        code === 'printscreen' ||
        e.keyCode === 44 ||
        e.which === 44
      ) {
        startPrtScnHold();
        e.preventDefault();
        e.stopPropagation();
        e.stopImmediatePropagation();
        wasScreenshotAttemptRef.current = true;
        return false;
      }

      // B. Snipping Tool Shortcuts (Win+Shift+S / Ctrl+Shift+S / Meta+Shift+S)
      if (isMod && e.shiftKey && (key === 's' || code === 'keys')) {
        applyInstantBlank(
          'Snipping Tool shortcut (Win+Shift+S) is restricted. Application page was blanked.',
          'web'
        );
        scheduleClipboardWipes(true);
        e.preventDefault();
        e.stopPropagation();
        e.stopImmediatePropagation();
        wasScreenshotAttemptRef.current = true;
        triggerRestrictionModal(
          'Snipping Tool shortcut (Win+Shift+S) is restricted. Application page was blanked.',
          'web'
        );
        return false;
      }

      // C. macOS Screenshot shortcuts (Cmd+Shift+3, Cmd+Shift+4, Cmd+Shift+5, Cmd+Shift+6)
      if (e.metaKey && e.shiftKey && ['3', '4', '5', '6'].includes(key)) {
        applyInstantBlank(
          'macOS Screenshot shortcut is restricted. Application page was blanked.',
          'web'
        );
        scheduleClipboardWipes(true);
        e.preventDefault();
        e.stopPropagation();
        e.stopImmediatePropagation();
        wasScreenshotAttemptRef.current = true;
        triggerRestrictionModal(
          'macOS Screenshot shortcut is restricted. Application page was blanked.',
          'web'
        );
        return false;
      }

      // D. Alt + PrintScreen (active window screenshot)
      if (e.altKey && (key === 'printscreen' || code === 'printscreen' || e.keyCode === 44)) {
        startPrtScnHold();
        e.preventDefault();
        e.stopPropagation();
        e.stopImmediatePropagation();
        wasScreenshotAttemptRef.current = true;
        triggerRestrictionModal(
          'Window screenshot shortcut (Alt+PrintScreen) is restricted. Application page was blanked.',
          'web'
        );
        return false;
      }

      // E. Mobile Hardware Screenshot Shortcuts (Power + Volume Down / Volume Up)
      const isMobileVolumeShortcut =
        key === 'audiovolumedown' ||
        key === 'audiovolumeup' ||
        key === 'volumedown' ||
        key === 'volumeup' ||
        code === 'audiovolumedown' ||
        code === 'audiovolumeup' ||
        e.keyCode === 174 ||
        e.keyCode === 175 ||
        e.which === 174 ||
        e.which === 175;

      if (isMobilePlatform && isMobileVolumeShortcut) {
        applyInstantBlank(
          'Mobile screenshot button shortcut is restricted. Application page was blanked.',
          'mobile'
        );
        scheduleClipboardWipes(true);
        wasScreenshotAttemptRef.current = true;
        triggerRestrictionModal(
          'Mobile screenshot button shortcut is restricted. Application page was blanked.',
          'mobile'
        );
        return;
      }

      // F. Print / PDF export (Ctrl+P / Cmd+P)
      if (isMod && (key === 'p' || code === 'keyp')) {
        applyInstantBlank('Printing course materials is restricted.', 'web');
        e.preventDefault();
        e.stopPropagation();
        e.stopImmediatePropagation();
        scheduleClipboardWipes();
        triggerRestrictionModal(
          'Printing course materials is restricted.',
          'web'
        );
        return false;
      }

      // Proactive blanking if modifier keys commonly used for snipping are pressed
      if (
        (e.metaKey && e.shiftKey) ||
        (e.ctrlKey && e.shiftKey && (key === 's' || code === 'keys'))
      ) {
        applyInstantBlank(
          'Screenshot shortcut detected. Application page was blanked.',
          'web'
        );
        scheduleClipboardWipes(true);
      }
    };

    const handleKeyUp = (e: KeyboardEvent) => {
      const key = (e.key || '').toLowerCase();
      const code = (e.code || '').toLowerCase();

      // On key release after normal click OR after long-press:
      if (
        key === 'printscreen' ||
        key === 'snapshot' ||
        code === 'printscreen' ||
        e.keyCode === 44 ||
        e.which === 44
      ) {
        stopPrtScnHold();
        applyInstantBlank(
          isMobilePlatform
            ? 'Mobile screenshot attempt was restricted. Application page was blanked.'
            : 'Screenshot key (PrintScreen) is restricted. Application page was blanked.',
          isMobilePlatform ? 'mobile' : 'web'
        );
        e.preventDefault();
        e.stopPropagation();
        e.stopImmediatePropagation();
        wasScreenshotAttemptRef.current = true;
        triggerRestrictionModal(
          isMobilePlatform
            ? 'Mobile screenshot attempt was restricted. Application page was blanked.'
            : 'Screenshot key (PrintScreen) is restricted. Application page was blanked.',
          isMobilePlatform ? 'mobile' : 'web'
        );
        return false;
      }
    };

    // ----------------------------------------------------
    // 2. Mobile View: Intercept Multi-Touch Screenshot Gestures (3-finger swipe)
    // ----------------------------------------------------
    const handleTouchStart = (e: TouchEvent) => {
      const touchCount = e.touches ? e.touches.length : 0;
      if (touchCount >= 3) {
        applyInstantBlank(
          'Mobile screenshot gesture (3-finger swipe) is restricted. Application page was blanked.',
          'mobile'
        );
        if (e.cancelable) {
          e.preventDefault();
        }
        e.stopPropagation();
        scheduleClipboardWipes(true);
        wasScreenshotAttemptRef.current = true;

        if (typeof navigator !== 'undefined' && navigator.vibrate) {
          try {
            navigator.vibrate([100, 50, 100]);
          } catch {
            /* ignore */
          }
        }

        triggerRestrictionModal(
          'Mobile screenshot gesture (3-finger swipe) is restricted. Application page was blanked.',
          'mobile'
        );
        return false;
      }
    };

    const handleTouchMove = (e: TouchEvent) => {
      const touchCount = e.touches ? e.touches.length : 0;
      if (touchCount >= 3) {
        applyInstantBlank(
          'Mobile screenshot gesture (3-finger swipe) is restricted. Application page was blanked.',
          'mobile'
        );
        if (e.cancelable) {
          e.preventDefault();
        }
        e.stopPropagation();
        scheduleClipboardWipes(true);
        wasScreenshotAttemptRef.current = true;
        return false;
      }
    };

    // ----------------------------------------------------
    // 3. Instant Restriction on Window Blur (Snipping Tool & Mobile Screenshot Buttons)
    // - The moment Snipping Tool or screen capture tool activates, window blurs.
    // - Immediately trigger the restriction screen so that any snip or capture results in the restriction screen!
    // ----------------------------------------------------
    const handleWindowBlur = () => {
      wasBlurredRef.current = true;
      startPrtScnHold();
      triggerRestrictionModal(
        isMobilePlatform
          ? 'Mobile screenshot attempt was restricted. Application page was blanked.'
          : 'Screenshot key (PrintScreen) or Snipping Tool was restricted. Application page was blanked.',
        isMobilePlatform ? 'mobile' : 'web'
      );
    };

    const handleVisibilityChange = () => {
      if (document.hidden) {
        wasBlurredRef.current = true;
        startPrtScnHold();
        triggerRestrictionModal(
          isMobilePlatform
            ? 'Mobile screenshot attempt was restricted. Application page was blanked.'
            : 'Screenshot key (PrintScreen) or Snipping Tool was restricted. Application page was blanked.',
          isMobilePlatform ? 'mobile' : 'web'
        );
      }
    };

    const handleWindowFocus = () => {
      stopPrtScnHold();
      scheduleClipboardWipes(true);
      // Keep restriction modal active if blurred or screenshot was attempted
      if (wasBlurredRef.current || wasScreenshotAttemptRef.current) {
        triggerRestrictionModal(
          isMobilePlatform
            ? 'Mobile screenshot attempt was restricted. Application page was blanked.'
            : 'Screenshot key (PrintScreen) or Snipping Tool was restricted. Application page was blanked.',
          isMobilePlatform ? 'mobile' : 'web'
        );
      }
    };

    // ----------------------------------------------------
    // 4. Mobile & Web: Context Menu & Touch Callout Suppression
    // ----------------------------------------------------
    const handleContextMenu = (e: MouseEvent | TouchEvent) => {
      const target = e.target as HTMLElement | null;
      if (
        target &&
        (target.tagName === 'INPUT' ||
          target.tagName === 'TEXTAREA' ||
          target.isContentEditable)
      ) {
        return;
      }
      e.preventDefault();
      e.stopPropagation();
      return false;
    };

    const handleDragStart = (e: DragEvent) => {
      e.preventDefault();
    };

    // ----------------------------------------------------
    // 5. Print Dialog Interception
    // ----------------------------------------------------
    const handleBeforePrint = (e: Event) => {
      applyInstantBlank('Printing course materials is restricted.', 'web');
      e.preventDefault();
      scheduleClipboardWipes();
      triggerRestrictionModal('Printing course materials is restricted.', 'web');
      return false;
    };

    // Attach listeners with capture = true across window and document
    window.addEventListener('keydown', handleKeyDown, { capture: true });
    document.addEventListener('keydown', handleKeyDown, { capture: true });
    window.addEventListener('keyup', handleKeyUp, { capture: true });
    document.addEventListener('keyup', handleKeyUp, { capture: true });

    window.addEventListener('touchstart', handleTouchStart, { passive: false, capture: true });
    document.addEventListener('touchstart', handleTouchStart, { passive: false, capture: true });
    window.addEventListener('touchmove', handleTouchMove, { passive: false, capture: true });
    document.addEventListener('touchmove', handleTouchMove, { passive: false, capture: true });

    window.addEventListener('blur', handleWindowBlur);
    window.addEventListener('focus', handleWindowFocus);
    document.addEventListener('visibilitychange', handleVisibilityChange);

    window.addEventListener('contextmenu', handleContextMenu, { capture: true });
    document.addEventListener('contextmenu', handleContextMenu, { capture: true });
    window.addEventListener('dragstart', handleDragStart, { capture: true });

    window.addEventListener('beforeprint', handleBeforePrint);

    return () => {
      stopPrtScnHold();
      activeWipeTimersRef.current.forEach((t) => window.clearTimeout(t));
      activeWipeTimersRef.current = [];

      if (resumeBtn) {
        resumeBtn.removeEventListener('click', dismissModal);
      }

      window.removeEventListener('keydown', handleKeyDown, true);
      document.removeEventListener('keydown', handleKeyDown, true);
      window.removeEventListener('keyup', handleKeyUp, true);
      document.removeEventListener('keyup', handleKeyUp, true);

      window.removeEventListener('touchstart', handleTouchStart, true);
      document.removeEventListener('touchstart', handleTouchStart, true);
      window.removeEventListener('touchmove', handleTouchMove, true);
      document.removeEventListener('touchmove', handleTouchMove, true);

      window.removeEventListener('blur', handleWindowBlur);
      window.removeEventListener('focus', handleWindowFocus);
      document.removeEventListener('visibilitychange', handleVisibilityChange);

      window.removeEventListener('contextmenu', handleContextMenu, true);
      document.removeEventListener('contextmenu', handleContextMenu, true);
      window.removeEventListener('dragstart', handleDragStart, true);

      window.removeEventListener('beforeprint', handleBeforePrint);

      removeInstantBlank();
    };
  }, [isRestrictedUser, startPrtScnHold, stopPrtScnHold, triggerRestrictionModal, dismissModal, scheduleClipboardWipes, isMobilePlatform]);

  // When user is not logged in or is an administrator, do not render modal or attach listeners
  if (!isRestrictedUser) {
    return null;
  }

  // Render modal directly onto document.body using createPortal; permanent DOM node enables synchronous 0ms display
  return createPortal(
    <>
      {/* Dedicated "Screenshot is Restricted" Modal Dialog - Permanently in DOM for 0ms instant display */}
      <div
        id="hl-restriction-overlay"
        style={{ display: modalActive ? 'flex' : 'none' }}
        className="fixed inset-0 z-[2147483647] items-center justify-center bg-black/98 p-4 sm:p-6 select-none"
        role="alertdialog"
        aria-modal="true"
        aria-labelledby="screenshot-modal-title"
        aria-describedby="screenshot-modal-desc"
      >
        <div
          className="relative w-full max-w-md overflow-hidden rounded-3xl border border-red-500/40 bg-zinc-950 p-6 sm:p-8 text-center text-white shadow-2xl ring-1 ring-red-500/20"
        >
          {/* Subtle Red Ambient Glow */}
          <div className="pointer-events-none absolute -top-24 -left-24 h-48 w-48 rounded-full bg-red-600/20 blur-3xl" />
          <div className="pointer-events-none absolute -bottom-24 -right-24 h-48 w-48 rounded-full bg-rose-600/15 blur-3xl" />

          {/* Shield Alert Icon */}
          <div className="mx-auto mb-4 flex h-20 w-20 items-center justify-center rounded-2xl bg-red-500/15 border border-red-500/30 text-red-400 shadow-inner">
            <ShieldAlert className="h-10 w-10 text-red-500 animate-pulse" />
          </div>

          {/* Security Badge */}
          <div className="inline-flex items-center gap-1.5 rounded-full bg-red-500/10 px-3 py-1 text-xs font-semibold uppercase tracking-wider text-red-400 border border-red-500/20 mb-3">
            <Lock className="h-3.5 w-3.5" />
            <span>Screen Blanked · Protected</span>
          </div>

          {/* Modal Title */}
          <h2
            id="screenshot-modal-title"
            className="text-xl sm:text-2xl font-bold tracking-tight text-white"
          >
            Screenshot is Restricted
          </h2>

          {/* Modal Description */}
          <p
            id="screenshot-modal-desc"
            className="mt-3 text-sm text-zinc-300 leading-relaxed"
          >
            {modalReason ||
              'The application page was blanked to prevent screen capture. Taking screenshots or recording course materials is strictly prohibited.'}
          </p>

          {/* Mode Detail Badge (Web View or Mobile View) */}
          <div className="mt-5 rounded-2xl bg-zinc-900/90 border border-zinc-800 p-3.5 text-xs text-zinc-400 text-left space-y-2">
            <div className="flex items-center gap-2 text-zinc-200 font-medium">
              {triggerSource === 'mobile' ? (
                <Smartphone className="h-4 w-4 text-sky-400" />
              ) : (
                <Laptop className="h-4 w-4 text-sky-400" />
              )}
              <span id="hl-restriction-platform-title">
                {triggerSource === 'mobile'
                  ? 'Mobile Protection Active'
                  : 'System Protection Active (PrintScreen & Snipping Tool Blocked)'}
              </span>
            </div>
            <p id="hl-restriction-platform-desc" className="text-[11px] text-zinc-400 leading-normal">
              {triggerSource === 'mobile'
                ? 'Screenshots via buttons (Power + Volume) and gestures are restricted across all sections.'
                : 'PrintScreen (normal click or long press) and Snipping Tool are restricted across all sections.'}
            </p>
          </div>

          {/* Primary Dismiss Button: "Resume Learning" */}
          <div className="mt-6">
            <button
              type="button"
              id="hl-resume-learning-btn"
              onClick={dismissModal}
              className="w-full rounded-xl bg-gradient-to-r from-red-600 via-rose-600 to-red-600 px-5 py-3 text-sm font-bold text-white shadow-lg shadow-red-600/30 hover:shadow-red-600/50 hover:brightness-110 active:scale-[0.98] transition-all cursor-pointer focus:outline-none focus:ring-2 focus:ring-red-400 focus:ring-offset-2 focus:ring-offset-zinc-950"
            >
              Resume Learning
            </button>
          </div>

          <p className="mt-3 text-[11px] text-zinc-500">
            Click &quot;Resume Learning&quot; to restore the application page.
          </p>
        </div>
      </div>
    </>,
    document.body
  );
}

