export const STORAGE = {
  deviceId: 'exampro_device_id',
  access: 'exampro_access_token',
  refresh: 'exampro_refresh_token',
  user: 'exampro_user',
  loginTime: 'exampro_login_time',
  apiUrlOverride: 'exampro_api_url',
} as const;

export function getApiUrl(): string {
  // 1. Runtime override stored in localStorage
  try {
    if (typeof window !== 'undefined') {
      const stored = localStorage.getItem(STORAGE.apiUrlOverride);
      if (stored && stored.trim()) {
        return stored.trim().replace(/\/$/, '');
      }
    }
  } catch {
    // Ignore storage errors
  }

  // 2. Build-time environment variable
  const envUrl = import.meta.env.VITE_API_URL;
  if (envUrl && envUrl.trim()) {
    return envUrl.trim().replace(/\/$/, '');
  }

  // 3. Environment heuristic:
  if (typeof window !== 'undefined') {
    const host = window.location.hostname;
    // Local dev
    if (host === 'localhost' || host === '127.0.0.1') {
      return 'http://localhost:8000/api';
    }
    // Remote HTTPS deployment (e.g. Netlify) with no VITE_API_URL:
    // Default to relative '/api' path so Netlify proxy redirects work without CORS / Mixed Content
    return `${window.location.origin}/api`;
  }

  return 'http://localhost:8000/api';
}

/** Origin of the backend (API_URL without the trailing /api) - used to resolve image URLs. */
export function getApiOrigin(): string {
  const url = getApiUrl();
  return url.replace(/\/api$/, '');
}

export function getWsUrl(): string {
  const apiUrl = getApiUrl();
  if (apiUrl.startsWith('/')) {
    if (typeof window !== 'undefined') {
      const proto = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      return `${proto}//${window.location.host}${apiUrl}`;
    }
  }
  return apiUrl.replace(/^http:/i, 'ws:').replace(/^https:/i, 'wss:');
}

export function setCustomApiUrl(url: string | null): void {
  try {
    if (!url || !url.trim()) {
      localStorage.removeItem(STORAGE.apiUrlOverride);
    } else {
      localStorage.setItem(STORAGE.apiUrlOverride, url.trim().replace(/\/$/, ''));
    }
  } catch {
    // Ignore storage errors
  }
}

export const API_URL: string = getApiUrl();
export const API_ORIGIN: string = getApiOrigin();
export const WS_URL: string = getWsUrl();

/** Maximum session lifetime: after 10 hours, user is automatically logged out. */
export const SESSION_MAX_DURATION_MS = 10 * 60 * 60 * 1000;

export const SNAPSHOT_INTERVAL_MS = 30_000;
export const EXTENSION_DECISION_SECONDS = 30;

export const EXAMS = ['TNPSC', 'SSC', 'Banking', 'UPSC', 'RRB', 'IBPS'] as const;

export const MALPRACTICE_LABEL: Record<string, string> = {
  TAB_SWITCH: 'Switched tab or window',
  MINIMIZE: 'Window lost focus',
  FULLSCREEN_EXIT: 'Left fullscreen',
  DEVTOOLS: 'Opened developer tools',
  COPY_PASTE: 'Copy / paste attempt',
  RIGHT_CLICK: 'Right-click attempt',
};
