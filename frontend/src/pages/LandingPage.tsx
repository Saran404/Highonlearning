import { BarChart3, Camera, Repeat, ShieldCheck, Timer } from 'lucide-react';
import { Link } from 'react-router-dom';
import Button from '../components/common/Button';
import BrandLogo from '../components/common/BrandLogo';
import { useAuthStore } from '../store/authStore';
import { EXAMS } from '../utils/constants';

/** A static miniature of the exam screen: this is what the product actually feels like. */
function ExamMock() {
  const states = ['a', 'a', 'a', 'r', 'c', 'n', 'n', 'n', 'a', 'n', 'n', 'n'];
  const cls: Record<string, string> = { a: 'bg-mint text-mint-700 border-mint-300', r: 'bg-cream text-cream-700 border-cream-300', c: 'bg-navy text-white border-navy', n: 'bg-white text-navy-500 border-line' };
  return (
    <div className="panel overflow-hidden" aria-hidden>
      <div className="flex items-center justify-between bg-navy px-4 py-2.5 text-xs text-white">
        <span className="font-medium">Percentage · Test 1</span>
        <span className="rounded-full bg-white/10 px-2.5 py-1 font-semibold tabular-nums">24:10</span>
      </div>
      <div className="flex gap-4 p-4">
        <div className="min-w-0 flex-1">
          <p className="text-xs text-navy-500">Question 5 of 12</p>
          <p className="paper mt-1 !text-base">A number increases from 80 to 100. What is the percentage increase?</p>
          <div className="mt-3 space-y-2 text-sm">
            {['20%', '30%', '25%', '15%'].map((o, i) => (
              <div key={o} className={`flex items-center gap-2.5 rounded-lg border px-3 py-2 ${i === 2 ? 'border-navy bg-sky-50 ring-1 ring-navy' : 'border-line'}`}>
                <span className={`flex h-6 w-6 items-center justify-center rounded-full text-xs font-semibold ${i === 2 ? 'bg-navy text-white' : 'bg-navy-50 text-navy-600'}`}>{String.fromCharCode(65 + i)}</span>
                {o}
              </div>
            ))}
          </div>
        </div>
        <div className="hidden w-28 shrink-0 sm:block">
          <p className="mb-2 text-xs text-navy-500">Palette</p>
          <div className="grid grid-cols-4 gap-1.5">
            {states.map((s, i) => <span key={i} className={`flex h-6 items-center justify-center rounded border text-[10px] font-semibold ${cls[s]}`}>{i + 1}</span>)}
          </div>
        </div>
      </div>
    </div>
  );
}

const features = [
  { icon: ShieldCheck, title: 'Graded and proctored', text: 'Fullscreen lockdown, camera snapshots and a three-warning rule. One attempt, like the real exam.' },
  { icon: Repeat, title: 'Unlimited practice', text: 'No timer, no camera. Every answer shows the explanation straight away. Repeat as often as you like.' },
  { icon: BarChart3, title: 'Rank and solutions', text: 'See your marks, time, rank among all test-takers and a worked solution for every question.' },
];

export default function LandingPage() {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  return (
    <div className="min-h-screen bg-white">
      <header className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4">
        <BrandLogo to="/" size="md" showTagline />
        <nav className="flex items-center gap-2">
          {isAuthenticated ? (
            <Link to="/courses"><Button size="sm">Open courses</Button></Link>
          ) : (
            <>
              <Link to="/login"><Button size="sm" variant="ghost">Sign in</Button></Link>
              <Link to="/register"><Button size="sm">Get started</Button></Link>
            </>
          )}
        </nav>
      </header>

      <section className="relative mx-auto grid max-w-6xl items-center gap-10 px-4 pb-16 pt-8 lg:grid-cols-2 lg:pt-16">
        <div>
          <div className="inline-flex items-center gap-2 rounded-full border border-amber-200 bg-amber-50 px-3 py-1 text-xs font-semibold text-amber-800 shadow-xs mb-4">
            <span className="flex h-2 w-2 rounded-full bg-amber-500 animate-pulse" />
            Learn • Practice • Achieve
          </div>
          <h1 className="text-4xl leading-tight sm:text-5xl font-extrabold text-navy-900 tracking-tight">
            Practise like it's the <span className="bg-gradient-to-r from-sky-600 to-navy-900 bg-clip-text text-transparent">exam hall</span>.
          </h1>
          <p className="mt-4 max-w-lg text-lg text-navy-600 leading-relaxed">
            Timed, proctored mock tests for government exam aspirants. Learn from structured practice, then prove your skills under authentic test conditions.
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <Link to={isAuthenticated ? '/courses' : '/register'}>
              <Button size="lg" variant="accent">
                {isAuthenticated ? 'Explore courses' : 'Start free today'}
              </Button>
            </Link>
            {!isAuthenticated && (
              <Link to="/login">
                <Button size="lg" variant="secondary">
                  I have an account
                </Button>
              </Link>
            )}
          </div>
          <ul className="mt-8 flex flex-wrap gap-2 text-sm">
            {EXAMS.map((e) => (
              <li key={e} className="rounded-full border border-sky-200/80 bg-sky-50/50 px-3 py-1 font-semibold text-navy-800 hover:border-sky-300 transition-colors">
                {e}
              </li>
            ))}
          </ul>
        </div>
        <ExamMock />
      </section>

      <section className="border-t border-line bg-canvas">
        <div className="mx-auto grid max-w-6xl gap-8 px-4 py-14 md:grid-cols-3">
          {features.map(({ icon: Icon, title, text }) => (
            <div key={title} className="panel p-6 border-line hover:border-sky-200 transition-all hover:shadow-highlight">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-sky-100 text-sky-700">
                <Icon className="h-5 w-5" aria-hidden />
              </div>
              <h2 className="mt-4 text-lg font-bold text-navy-900">{title}</h2>
              <p className="mt-1.5 text-sm text-navy-600 leading-relaxed">{text}</p>
            </div>
          ))}
        </div>
      </section>

      <footer className="border-t border-line px-4 py-6 text-center text-xs text-navy-400">
        <span className="inline-flex items-center gap-1"><Camera className="h-3.5 w-3.5" /><Timer className="h-3.5 w-3.5" /></span> HighonLearning LMS · Built for TNPSC, SSC, Banking, UPSC, RRB and IBPS aspirants
      </footer>
    </div>
  );
}
