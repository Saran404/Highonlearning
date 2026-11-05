import axios, { AxiosError, AxiosRequestConfig, InternalAxiosRequestConfig } from 'axios';
import type { ApiErrorBody } from '../types';
import { getApiOrigin, getApiUrl, STORAGE } from '../utils/constants';

/** Normalised error shape used across the UI. */
export interface ApiError {
  status: number;
  code: string;
  message: string;
  details?: unknown;
}

export function toApiError(err: unknown): ApiError {
  if (axios.isAxiosError(err)) {
    const e = err as AxiosError<ApiErrorBody>;
    if (e.response) {
      const body = e.response.data;
      return {
        status: e.response.status,
        code: body?.code ?? 'HTTP_ERROR',
        message: body?.message ?? e.message,
        details: body?.details,
      };
    }
    const currentTarget = getApiUrl();
    const isHttps = typeof window !== 'undefined' && window.location.protocol === 'https:';
    const isTargetHttp = currentTarget.startsWith('http://');
    let message = 'Cannot reach the server. Check your connection.';
    if (isHttps && isTargetHttp) {
      message = `Cannot reach insecure HTTP server (${currentTarget}) from a secure HTTPS site. Please configure your live HTTPS backend URL or tunnel in Server Settings.`;
    }
    return { status: 0, code: 'NETWORK_ERROR', message };
  }
  return { status: 0, code: 'UNKNOWN', message: err instanceof Error ? err.message : 'Something went wrong.' };
}

/** Resolve a backend-relative URL (e.g. signed snapshot links) to an absolute one. */
export function assetUrl(path: string): string {
  return /^https?:/i.test(path) ? path : `${getApiOrigin()}${path}`;
}

/* ---- auth handlers are registered by authStore (avoids an import cycle) ---- */
interface AuthHandlers {
  onSessionEnded: (message: string) => void;
}
let handlers: AuthHandlers = { onSessionEnded: () => undefined };
export function setAuthHandlers(h: AuthHandlers): void {
  handlers = h;
}

const read = (key: string): string | null => {
  try {
    return localStorage.getItem(key);
  } catch {
    return null;
  }
};

export const api = axios.create({ baseURL: getApiUrl(), timeout: 60_000 });

api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  config.baseURL = getApiUrl();
  const token = read(STORAGE.access);
  if (token) config.headers.set('Authorization', `Bearer ${token}`);
  return config;
});

/** One refresh at a time: parallel 401s share the same request (the server rotates refresh tokens). */
let refreshing: Promise<string> | null = null;

function refreshAccessToken(): Promise<string> {
  if (!refreshing) {
    const refreshToken = read(STORAGE.refresh);
    if (!refreshToken) return Promise.reject(new Error('no refresh token'));
    refreshing = axios
      .post<{ access_token: string; refresh_token: string }>(`${getApiUrl()}/auth/refresh`, { refresh_token: refreshToken })
      .then((res) => {
        localStorage.setItem(STORAGE.access, res.data.access_token);
        localStorage.setItem(STORAGE.refresh, res.data.refresh_token);
        return res.data.access_token;
      })
      .finally(() => {
        refreshing = null;
      });
  }
  return refreshing;
}

type RetriableConfig = AxiosRequestConfig & { _retry?: boolean };

api.interceptors.response.use(
  (res) => res,
  async (error: AxiosError<ApiErrorBody>) => {
    const original = error.config as RetriableConfig | undefined;
    const status = error.response?.status;
    const code = error.response?.data?.code;

    if (status === 401 && (code === 'SESSION_REVOKED' || code === 'SESSION_EXPIRED')) {
      handlers.onSessionEnded(
        code === 'SESSION_EXPIRED'
          ? 'Your session has expired after 10 hours. Please sign in again.'
          : 'Session ended.'
      );
      return Promise.reject(error);
    }

    const isAuthCall = original?.url?.includes('/auth/login') || original?.url?.includes('/auth/refresh');
    if (status === 401 && !isAuthCall && original && !original._retry && read(STORAGE.access)) {
      original._retry = true;
      try {
        const token = await refreshAccessToken();
        original.headers = { ...(original.headers as Record<string, string> | undefined), Authorization: `Bearer ${token}` };
        return api(original);
      } catch (err: unknown) {
        try {
          localStorage.removeItem(STORAGE.access);
          localStorage.removeItem(STORAGE.refresh);
        } catch {
          /* ignore */
        }
        const refreshErr = err as AxiosError<ApiErrorBody> | undefined;
        const refreshCode = refreshErr?.response?.data?.code;
        const msg = refreshCode === 'SESSION_EXPIRED'
          ? 'Your session has expired after 10 hours. Please sign in again.'
          : 'Please sign in again.';
        handlers.onSessionEnded(msg);
      }
    }
    return Promise.reject(error);
  },
);
