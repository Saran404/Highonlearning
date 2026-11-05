import { AlertCircle } from 'lucide-react';
import { FormEvent, useState } from 'react';
import toast from 'react-hot-toast';
import { Link, Navigate, useLocation, useNavigate } from 'react-router-dom';
import { toApiError } from '../api/client';
import Button from '../components/common/Button';
import AuthShell from '../components/layout/AuthShell';
import { useAuthStore } from '../store/authStore';
import { useResumeSessionStore } from '../store/resumeSessionStore';

export default function LoginPage() {
  const { login, isAuthenticated, user } = useAuthStore();
  const navigate = useNavigate();
  const location = useLocation();
  const from = (location.state as { from?: string } | null)?.from;
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (isAuthenticated && user) return <Navigate to={from ?? (user.role === 'ADMIN' ? '/admin' : '/courses')} replace />;

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const u = await login(email.trim(), password);
      if (u.role !== 'ADMIN') {
        await useResumeSessionStore.getState().checkAndTriggerResume(u).catch(() => {});
      }
      navigate(from ?? (u.role === 'ADMIN' ? '/admin' : '/courses'), { replace: true });
    } catch (err) {
      const apiErr = toApiError(err);
      if (apiErr.code === 'ALREADY_LOGGED_IN') {
        toast.error('Already logged in on another device.');
        setError('Your account is signed in on another device. Log out there first, then try again.');
      } else {
        setError(apiErr.message);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthShell title="Welcome back" subtitle="Sign in to continue your preparation." footer={<>New here? <Link to="/register" className="font-semibold text-sky-700 hover:underline">Create an account</Link></>}>
      <form onSubmit={onSubmit} className="space-y-4" noValidate>
        {error && (
          <div role="alert" className="flex items-start gap-2 rounded-lg bg-danger px-3 py-2.5 text-sm text-danger-700">
            <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" /> {error}
          </div>
        )}
        <div>
          <label htmlFor="email" className="label">Email</label>
          <input id="email" type="email" inputMode="email" autoCapitalize="none" autoComplete="email" required className="field" value={email} onChange={(e) => setEmail(e.target.value)} />
        </div>
        <div>
          <label htmlFor="password" className="label">Password</label>
          <input id="password" type="password" autoComplete="current-password" required className="field" value={password} onChange={(e) => setPassword(e.target.value)} />
        </div>
        <Button type="submit" size="lg" fullWidth loading={loading} disabled={!email || !password}>Sign in</Button>
      </form>
    </AuthShell>
  );
}
