import { FormEvent, useState } from 'react';
import toast from 'react-hot-toast';
import { Link, useNavigate } from 'react-router-dom';
import { authApi } from '../api/auth';
import { toApiError } from '../api/client';
import Button from '../components/common/Button';
import AuthShell from '../components/layout/AuthShell';

export default function RegisterPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: '', email: '', password: '', confirm: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const set = (k: keyof typeof form) => (e: React.ChangeEvent<HTMLInputElement>) => setForm({ ...form, [k]: e.target.value });

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);
    if (form.password.length < 8) return setError('Use at least 8 characters for your password.');
    if (form.password !== form.confirm) return setError("The two passwords don't match.");
    setLoading(true);
    try {
      await authApi.register({ name: form.name.trim(), email: form.email.trim(), password: form.password });
      toast.success('Account created. Please sign in.');
      navigate('/login', { replace: true });
    } catch (err) {
      const apiErr = toApiError(err);
      setError(apiErr.code === 'VALIDATION_ERROR' ? 'Please check your details and try again.' : apiErr.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthShell title="Create your account" subtitle="Free to start. Takes a minute." footer={<>Already registered? <Link to="/login" className="font-semibold text-sky-700 hover:underline">Sign in</Link></>}>
      <form onSubmit={onSubmit} className="space-y-4" noValidate>
        {error && <div role="alert" className="rounded-lg bg-danger px-3 py-2.5 text-sm text-danger-700">{error}</div>}
        <div><label htmlFor="name" className="label">Full name</label><input id="name" className="field" autoComplete="name" autoCapitalize="words" required value={form.name} onChange={set('name')} /></div>
        <div><label htmlFor="email" className="label">Email</label><input id="email" type="email" inputMode="email" autoCapitalize="none" className="field" autoComplete="email" required value={form.email} onChange={set('email')} /></div>
        <div><label htmlFor="password" className="label">Password</label><input id="password" type="password" className="field" autoComplete="new-password" required value={form.password} onChange={set('password')} /></div>
        <div><label htmlFor="confirm" className="label">Confirm password</label><input id="confirm" type="password" className="field" autoComplete="new-password" required value={form.confirm} onChange={set('confirm')} /></div>
        <Button type="submit" size="lg" fullWidth loading={loading} disabled={!form.name || !form.email || !form.password}>Create account</Button>
      </form>
    </AuthShell>
  );
}
