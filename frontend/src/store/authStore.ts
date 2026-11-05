import { create } from 'zustand';
import { authApi } from '../api/auth';
import { setAuthHandlers } from '../api/client';
import type { Role, User } from '../types';
import { SESSION_MAX_DURATION_MS, STORAGE } from '../utils/constants';
import { getDeviceId } from '../utils/deviceId';
import { finalizeSessionSummary } from '../utils/sessionTracker';
import { useResumeSessionStore } from './resumeSessionStore';
import { useWellnessStore } from './wellnessStore';

interface AuthState {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  deviceId: string;
  isAuthenticated: boolean;
  /** Set when the session was ended remotely; the root component shows a modal for it. */
  revokedReason: string | null;
  login: (email: string, password: string) => Promise<User>;
  logout: () => Promise<void>;
  /** Clear local auth without calling the server (the session is already dead). */
  clearAuth: () => void;
  endSession: (reason: string) => void;
  dismissRevoked: () => void;
  hasRole: (...roles: Role[]) => boolean;
}

const safeGet = (k: string): string | null => {
  try {
    return localStorage.getItem(k);
  } catch {
    return null;
  }
};

export function isSessionExpired(): boolean {
  const loginTimeRaw = safeGet(STORAGE.loginTime);
  if (!loginTimeRaw) return false;
  const loginTime = parseInt(loginTimeRaw, 10);
  if (isNaN(loginTime)) return true;
  return Date.now() - loginTime >= SESSION_MAX_DURATION_MS;
}

function loadUser(): User | null {
  const raw = safeGet(STORAGE.user);
  if (!raw) return null;
  try {
    return JSON.parse(raw) as User;
  } catch {
    return null;
  }
}

function wipeStorage(): void {
  try {
    localStorage.removeItem(STORAGE.access);
    localStorage.removeItem(STORAGE.refresh);
    localStorage.removeItem(STORAGE.user);
    localStorage.removeItem(STORAGE.loginTime);
  } catch {
    /* storage unavailable */
  }
}

const expiredOnBoot = isSessionExpired();
if (expiredOnBoot) {
  wipeStorage();
}

const initialAccess = expiredOnBoot ? null : safeGet(STORAGE.access);
const initialUser = initialAccess ? loadUser() : null;

// Graceful initialization for existing active sessions without loginTime recorded
if (initialAccess && !safeGet(STORAGE.loginTime)) {
  try {
    localStorage.setItem(STORAGE.loginTime, String(Date.now()));
  } catch {
    /* ignore */
  }
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: initialAccess ? initialUser : null,
  accessToken: initialAccess,
  refreshToken: expiredOnBoot ? null : safeGet(STORAGE.refresh),
  deviceId: getDeviceId(),
  isAuthenticated: Boolean(initialAccess && initialUser),
  revokedReason: expiredOnBoot ? 'Your session has expired after 10 hours. Please sign in again.' : null,

  login: async (email, password) => {
    const res = await authApi.login({ email, password, device_id: get().deviceId });
    const now = Date.now();
    localStorage.setItem(STORAGE.access, res.access_token);
    localStorage.setItem(STORAGE.refresh, res.refresh_token);
    localStorage.setItem(STORAGE.user, JSON.stringify(res.user));
    localStorage.setItem(STORAGE.loginTime, String(now));
    useWellnessStore.getState().initSession();
    set({ user: res.user, accessToken: res.access_token, refreshToken: res.refresh_token, isAuthenticated: true, revokedReason: null });
    // Trigger resume popup check
    useResumeSessionStore.getState().checkAndTriggerResume(res.user).catch(() => {});
    return res.user;
  },

  logout: async () => {
    const current = get().user;
    if (current?.id) {
      finalizeSessionSummary(current.id, current.name);
      try {
        sessionStorage.removeItem(`exampro_resume_shown_${current.id}`);
      } catch {
        /* ignore */
      }
    }
    try {
      await authApi.logout();
    } catch {
      /* the session may already be gone - log out locally regardless */
    }
    get().clearAuth();
  },

  clearAuth: () => {
    const current = get().user;
    if (current?.id) {
      finalizeSessionSummary(current.id, current.name);
      try {
        sessionStorage.removeItem(`exampro_resume_shown_${current.id}`);
      } catch {
        /* ignore */
      }
    }
    wipeStorage();
    useWellnessStore.getState().resetSession();
    set({ user: null, accessToken: null, refreshToken: null, isAuthenticated: false });
  },

  endSession: (reason) => {
    if (!get().isAuthenticated) return;
    const current = get().user;
    if (current?.id) {
      finalizeSessionSummary(current.id, current.name);
      try {
        sessionStorage.removeItem(`exampro_resume_shown_${current.id}`);
      } catch {
        /* ignore */
      }
    }
    wipeStorage();
    useWellnessStore.getState().resetSession();
    set({ user: null, accessToken: null, refreshToken: null, isAuthenticated: false, revokedReason: reason });
  },

  dismissRevoked: () => set({ revokedReason: null }),

  hasRole: (...roles) => {
    const u = get().user;
    return Boolean(u && roles.includes(u.role));
  },
}));

// The axios layer reports dead sessions through this callback.
setAuthHandlers({ onSessionEnded: (message) => useAuthStore.getState().endSession(message) });
