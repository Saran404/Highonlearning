import { Link } from 'react-router-dom';
import Button from '../components/common/Button';

export default function NotFoundPage() {
  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center px-4 text-center">
      <p className="text-5xl font-semibold text-sky">404</p>
      <h1 className="mt-2 text-xl">This page doesn't exist</h1>
      <p className="mt-1 text-sm text-navy-500">The link may be old or mistyped.</p>
      <Link to="/dashboard" className="mt-5"><Button>Go to dashboard</Button></Link>
    </div>
  );
}
