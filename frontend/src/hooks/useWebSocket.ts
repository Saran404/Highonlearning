import { useEffect, useRef, useState } from 'react';

export type SocketStatus = 'idle' | 'connecting' | 'open' | 'closed';

/**
 * Reconnecting WebSocket with a keep-alive ping. Pass ``null`` to stay disconnected.
 * Close codes 4401 (bad token) and 4403 (forbidden) are final - no reconnect.
 */
export function useWebSocket(url: string | null, onMessage: (data: unknown) => void): SocketStatus {
  const [status, setStatus] = useState<SocketStatus>('idle');
  const handler = useRef(onMessage);
  handler.current = onMessage;

  useEffect(() => {
    if (!url) {
      setStatus('idle');
      return;
    }
    let ws: WebSocket | null = null;
    let stopped = false;
    let attempt = 0;
    let retryTimer: number | undefined;
    let pingTimer: number | undefined;

    const connect = () => {
      setStatus('connecting');
      ws = new WebSocket(url);
      ws.onopen = () => {
        attempt = 0;
        setStatus('open');
        pingTimer = window.setInterval(() => {
          if (ws && ws.readyState === WebSocket.OPEN) ws.send('ping');
        }, 25_000);
      };
      ws.onmessage = (ev: MessageEvent<string>) => {
        if (ev.data === 'pong') return;
        try {
          handler.current(JSON.parse(ev.data));
        } catch {
          /* ignore malformed frames */
        }
      };
      ws.onerror = () => ws?.close();
      ws.onclose = (ev) => {
        window.clearInterval(pingTimer);
        setStatus('closed');
        if (stopped || ev.code === 4401 || ev.code === 4403) return;
        attempt += 1;
        retryTimer = window.setTimeout(connect, Math.min(30_000, 1000 * 2 ** attempt));
      };
    };

    connect();
    return () => {
      stopped = true;
      window.clearTimeout(retryTimer);
      window.clearInterval(pingTimer);
      ws?.close();
    };
  }, [url]);

  return status;
}
