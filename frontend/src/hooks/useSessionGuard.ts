import { useEffect } from 'react';
import { useAuthStore } from '../store/authStore';
import { SESSION_MAX_DURATION_MS, STORAGE, getWsUrl } from '../utils/constants';
import { useWebSocket } from './useWebSocket';

interface SessionEvent {
  type?: string;
  reason?: string;
}

/**
 * Listens on /ws/session/{device_id}. When another device logs in (or an admin revokes this
 * session) the server pushes SESSION_REVOKED and we end the local session immediately.
 * Also monitors the 10-hour session duration and automatically logs out when expired.
 */
export function useSessionGuard(): void {
  const { isAuthenticated, accessToken, deviceId, endSession } = useAuthStore();
  const wsBase = getWsUrl();
  const url = isAuthenticated && accessToken ? `${wsBase}/ws/session/${encodeURIComponent(deviceId)}?token=${encodeURIComponent(accessToken)}` : null;

  useWebSocket(url, (data) => {
    const msg = data as SessionEvent;
    if (msg?.type === 'SESSION_REVOKED') {
      endSession(msg.reason ?? "Your account was accessed from another device. You've been logged out.");
    }
  });

  useEffect(() => {
    if (!isAuthenticated) return;

    const checkExpiry = () => {
      const loginTimeRaw = localStorage.getItem(STORAGE.loginTime);
      if (!loginTimeRaw) return;
      const loginTime = parseInt(loginTimeRaw, 10);
      if (isNaN(loginTime)) return;

      if (Date.now() - loginTime >= SESSION_MAX_DURATION_MS) {
        endSession('Your session has expired after 10 hours. Please sign in again.');
      }
    };

    // 1. Initial check
    checkExpiry();

    // 2. Set timeout for the remaining time
    let timerId: ReturnType<typeof setTimeout> | undefined;
    const loginTimeRaw = localStorage.getItem(STORAGE.loginTime);
    if (loginTimeRaw) {
      const loginTime = parseInt(loginTimeRaw, 10);
      if (!isNaN(loginTime)) {
        const remaining = (loginTime + SESSION_MAX_DURATION_MS) - Date.now();
        if (remaining > 0) {
          timerId = setTimeout(() => {
            endSession('Your session has expired after 10 hours. Please sign in again.');
          }, remaining);
        }
      }
    }

    // 3. Periodic check every 30 seconds for background tab throttling or system sleep
    const intervalId = setInterval(checkExpiry, 30_000);

    // 4. Check immediately upon visibility change or window focus
    const onFocusOrVisible = () => {
      if (document.visibilityState === 'visible') {
        checkExpiry();
      }
    };

    window.addEventListener('visibilitychange', onFocusOrVisible);
    window.addEventListener('focus', onFocusOrVisible);

    return () => {
      if (timerId) clearTimeout(timerId);
      clearInterval(intervalId);
      window.removeEventListener('visibilitychange', onFocusOrVisible);
      window.removeEventListener('focus', onFocusOrVisible);
    };
  }, [isAuthenticated, endSession]);
}
