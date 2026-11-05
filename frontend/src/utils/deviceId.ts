import { STORAGE } from './constants';

function uuid(): string {
  if (typeof crypto !== 'undefined' && 'randomUUID' in crypto) return crypto.randomUUID();
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    return (c === 'x' ? r : (r & 0x3) | 0x8).toString(16);
  });
}

/** One stable id per browser profile (persisted in localStorage). */
export function getDeviceId(): string {
  try {
    const existing = localStorage.getItem(STORAGE.deviceId);
    if (existing) return existing;
    const id = uuid();
    localStorage.setItem(STORAGE.deviceId, id);
    return id;
  } catch {
    return uuid(); // storage blocked: the id lasts for this page load only
  }
}
