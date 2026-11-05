import React, { Component, ErrorInfo, ReactNode } from 'react';
import { AlertTriangle, RefreshCw, Home } from 'lucide-react';
import Button from './Button';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export default class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error in component tree:', error, errorInfo);

    // Auto-reload once for dynamic chunk loading failures in Vite
    const message = error?.message || '';
    const isChunkFailure =
      message.includes('Failed to fetch dynamically imported module') ||
      message.includes('error loading dynamically imported module') ||
      message.includes('Loading chunk') ||
      message.includes('ChunkLoadError');

    if (isChunkFailure) {
      const reloaded = sessionStorage.getItem('exampro_chunk_retry');
      if (!reloaded) {
        sessionStorage.setItem('exampro_chunk_retry', 'true');
        window.location.reload();
      }
    }
  }

  private handleReload = () => {
    sessionStorage.removeItem('exampro_chunk_retry');
    window.location.reload();
  };

  private handleGoHome = () => {
    sessionStorage.removeItem('exampro_chunk_retry');
    window.location.href = '/dashboard';
  };

  public render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-canvas flex items-center justify-center p-4">
          <div className="max-w-md w-full bg-white rounded-2xl border border-line p-6 sm:p-8 text-center shadow-lg">
            <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-amber-100 text-amber-700 mb-4 shadow-xs">
              <AlertTriangle className="h-7 w-7" />
            </div>
            <h2 className="text-xl font-bold text-navy-950">Something went wrong</h2>
            <p className="mt-2 text-sm text-navy-600 leading-relaxed">
              We encountered an unexpected issue while displaying this page. Refreshing usually resolves it immediately.
            </p>
            {this.state.error?.message && (
              <div className="mt-3 rounded-lg bg-navy-50 p-2.5 text-xs text-navy-600 font-mono text-left truncate">
                {this.state.error.message}
              </div>
            )}
            <div className="mt-6 flex flex-col sm:flex-row items-center justify-center gap-3">
              <Button
                variant="primary"
                onClick={this.handleReload}
                icon={<RefreshCw className="h-4 w-4" />}
                className="w-full sm:w-auto"
              >
                Refresh Page
              </Button>
              <Button
                variant="secondary"
                onClick={this.handleGoHome}
                icon={<Home className="h-4 w-4" />}
                className="w-full sm:w-auto"
              >
                Go to Dashboard
              </Button>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
