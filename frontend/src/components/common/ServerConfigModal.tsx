import { AlertCircle, CheckCircle2, Globe, RefreshCw, Server, X } from 'lucide-react';
import { useState } from 'react';
import toast from 'react-hot-toast';
import { getApiUrl, setCustomApiUrl } from '../../utils/constants';
import Button from './Button';

interface Props {
  onClose: () => void;
  onSaved: () => void;
}

export default function ServerConfigModal({ onClose, onSaved }: Props) {
  const currentUrl = getApiUrl();
  const [url, setUrl] = useState(currentUrl);
  const [testing, setTesting] = useState(false);
  const [testResult, setTestResult] = useState<{ ok: boolean; message: string } | null>(null);

  const isHttps = typeof window !== 'undefined' && window.location.protocol === 'https:';
  const isTargetHttp = url.trim().toLowerCase().startsWith('http://') && !url.includes('localhost') && !url.includes('127.0.0.1');
  const isMixedContentRisk = isHttps && url.trim().toLowerCase().startsWith('http://');

  const handleTestConnection = async () => {
    const target = url.trim().replace(/\/$/, '');
    if (!target) {
      setTestResult({ ok: false, message: 'Please enter a valid URL' });
      return;
    }

    setTesting(true);
    setTestResult(null);

    try {
      const healthEndpoint = target.endsWith('/api') ? `${target}/health` : `${target}/api/health`;
      const res = await fetch(healthEndpoint, { method: 'GET', mode: 'cors' });
      if (res.ok) {
        setTestResult({ ok: true, message: 'Connected successfully! Backend is healthy and responding.' });
      } else {
        setTestResult({ ok: false, message: `Server reached but responded with status ${res.status} (${res.statusText})` });
      }
    } catch (err: unknown) {
      let detail = err instanceof Error ? err.message : 'Connection failed';
      if (isMixedContentRisk) {
        detail = 'Blocked by browser (Mixed Content: Insecure HTTP request from secure HTTPS website).';
      }
      setTestResult({ ok: false, message: `Cannot connect: ${detail}` });
    } finally {
      setTesting(false);
    }
  };

  const handleSave = () => {
    const trimmed = url.trim();
    if (!trimmed) {
      toast.error('URL cannot be empty');
      return;
    }
    setCustomApiUrl(trimmed);
    toast.success('Backend URL updated!');
    onSaved();
  };

  const handleReset = () => {
    setCustomApiUrl(null);
    setUrl(getApiUrl());
    setTestResult(null);
    toast.success('Reset to default backend URL');
    onSaved();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-navy/60 backdrop-blur-xs animate-in fade-in duration-150">
      <div className="relative w-full max-w-lg rounded-2xl bg-white p-6 shadow-xl border border-line">
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-line">
          <div className="flex items-center gap-2.5">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-sky-50 text-sky-600 border border-sky-100">
              <Server className="h-5 w-5" />
            </div>
            <div>
              <h3 className="text-base font-semibold text-navy">Backend Server Settings</h3>
              <p className="text-xs text-navy-500">Configure the API endpoint used by this application.</p>
            </div>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="rounded-lg p-1.5 text-navy-400 hover:bg-navy-50 hover:text-navy transition-colors"
            aria-label="Close"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Form Body */}
        <div className="mt-5 space-y-4">
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-navy-600 mb-1.5">
              API Server URL
            </label>
            <div className="relative">
              <input
                type="text"
                value={url}
                onChange={(e) => {
                  setUrl(e.target.value);
                  setTestResult(null);
                }}
                placeholder="https://your-backend.onrender.com/api"
                className="w-full rounded-xl border border-line bg-surface px-3.5 py-2.5 text-sm text-navy placeholder:text-navy-300 focus:border-sky focus:outline-hidden focus:ring-2 focus:ring-sky/20 transition-all font-mono"
              />
            </div>
            <p className="mt-1.5 text-xs text-navy-400">
              Must include <code className="rounded bg-navy-50 px-1 py-0.5 text-navy-700">/api</code> suffix. Example: <code className="text-sky-700 font-mono">https://backend-service.onrender.com/api</code>
            </p>
          </div>

          {/* Mixed Content Warning */}
          {isMixedContentRisk && (
            <div className="rounded-xl border border-amber-200 bg-amber-50 p-3.5 text-xs text-amber-900 flex items-start gap-2.5">
              <AlertCircle className="h-4 w-4 text-amber-600 shrink-0 mt-0.5" />
              <div>
                <p className="font-semibold">Mixed Content Warning</p>
                <p className="mt-0.5 text-amber-800">
                  You are viewing this site over <strong>HTTPS</strong> (Netlify). Browsers automatically block requests to insecure <strong>HTTP</strong> addresses. Use an HTTPS URL or cloud tunnel (e.g. ngrok / cloudflared).
                </p>
              </div>
            </div>
          )}

          {/* Test connection result badge */}
          {testResult && (
            <div
              className={`rounded-xl border p-3 text-xs flex items-start gap-2 ${
                testResult.ok
                  ? 'border-mint-200 bg-mint-50 text-mint-900'
                  : 'border-coral-200 bg-coral-50 text-coral-900'
              }`}
            >
              {testResult.ok ? (
                <CheckCircle2 className="h-4 w-4 text-mint-600 shrink-0 mt-0.5" />
              ) : (
                <AlertCircle className="h-4 w-4 text-coral-600 shrink-0 mt-0.5" />
              )}
              <span className="font-medium">{testResult.message}</span>
            </div>
          )}

          <div className="flex items-center gap-2">
            <Button
              type="button"
              variant="secondary"
              size="sm"
              onClick={handleTestConnection}
              loading={testing}
              icon={<RefreshCw className="h-3.5 w-3.5" />}
            >
              Test Connection
            </Button>
            <Button
              type="button"
              variant="ghost"
              size="sm"
              onClick={handleReset}
            >
              Reset to Default
            </Button>
          </div>

          {/* Netlify Deployment Tip */}
          <div className="rounded-xl border border-line bg-surface/50 p-3 text-xs text-navy-500">
            <p className="font-semibold text-navy-700 flex items-center gap-1.5">
              <Globe className="h-3.5 w-3.5 text-sky-600" /> Netlify Permanent Setup:
            </p>
            <p className="mt-1">
              To configure this permanently for all users, set environment variable{' '}
              <code className="rounded bg-white px-1.5 py-0.5 font-mono text-navy-800 border border-line">
                VITE_API_URL
              </code>{' '}
              in your Netlify dashboard under <em>Site configuration &gt; Environment variables</em>, then redeploy.
            </p>
          </div>
        </div>

        {/* Footer Actions */}
        <div className="mt-6 flex items-center justify-end gap-3 pt-4 border-t border-line">
          <Button type="button" variant="ghost" onClick={onClose}>
            Cancel
          </Button>
          <Button type="button" onClick={handleSave}>
            Save &amp; Connect
          </Button>
        </div>
      </div>
    </div>
  );
}
