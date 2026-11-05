import { useEffect, useRef, useState } from 'react';
import { useLocation } from 'react-router-dom';
import {
  Activity,
  ChevronDown,
  Clock,
  Droplets,
  Eye,
  FastForward,
  HeartPulse,
  Sparkles,
  Trophy,
} from 'lucide-react';
import { useWellnessStore } from '../../store/wellnessStore';
import { WellnessCategory } from '../../utils/wellnessQuotes';

function formatTimer(minutes: number): string {
  if (minutes < 60) return `${minutes}m`;
  const hrs = Math.floor(minutes / 60);
  const mins = minutes % 60;
  return `${hrs}h ${mins}m`;
}

export default function WellnessCompanion() {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const location = useLocation();
  const {
    elapsedMinutes,
    triggerManualReminder,
    fastForwardMinutes,
  } = useWellnessStore();

  const isAssessmentRoute =
    location.pathname.startsWith('/attempts') ||
    location.pathname.startsWith('/assessments') ||
    location.pathname.startsWith('/results');

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
      }
    }
    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  const handleTestCategory = (cat: WellnessCategory) => {
    if (isAssessmentRoute) return;
    triggerManualReminder(cat);
    setIsOpen(false);
  };

  return (
    <div className="relative" ref={dropdownRef}>
      {/* Navbar Pill */}
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="flex shrink-0 items-center gap-1.5 rounded-full border border-navy-700 bg-navy-850 px-2.5 sm:px-3 py-1 text-xs font-medium text-navy-200 transition-colors hover:border-navy-600 hover:bg-navy-800 hover:text-white"
        title={
          isAssessmentRoute
            ? 'Study Companion - Paused during assessment'
            : 'Study Companion - Active in Learning & Practice'
        }
        aria-expanded={isOpen}
      >
        <span
          className={`flex h-2 w-2 shrink-0 rounded-full ${
            isAssessmentRoute
              ? 'bg-amber-400'
              : 'bg-emerald-400 animate-pulse'
          }`}
        />
        <Clock className="h-3.5 w-3.5 shrink-0 text-sky-400" />
        <span className="font-semibold text-white whitespace-nowrap">
          {formatTimer(elapsedMinutes)}
        </span>
        <ChevronDown className="h-3 w-3 shrink-0 text-navy-400" />
      </button>

      {/* Popover Menu */}
      {isOpen && (
        <div className="absolute right-0 top-full mt-2 w-76 rounded-2xl border border-navy-700 bg-navy-900/95 p-4 text-white shadow-2xl backdrop-blur-md z-50 animate-in fade-in zoom-in-95 duration-150">
          <div className="flex items-center justify-between pb-3 border-b border-navy-800">
            <div>
              <div className="text-xs font-semibold uppercase tracking-wider text-navy-400">
                Study Companion
              </div>
              <div className="text-sm font-bold text-white">
                Active for {elapsedMinutes} min{elapsedMinutes === 1 ? '' : 's'}
              </div>
            </div>
            {isAssessmentRoute ? (
              <span className="rounded-full bg-amber-500/10 px-2 py-0.5 text-[11px] font-medium text-amber-400 border border-amber-500/20">
                Paused (Exam)
              </span>
            ) : (
              <span className="rounded-full bg-emerald-500/10 px-2 py-0.5 text-[11px] font-medium text-emerald-400 border border-emerald-500/20">
                Learn &amp; Practice
              </span>
            )}
          </div>

          {/* Context Banner */}
          {isAssessmentRoute ? (
            <div className="my-2.5 rounded-lg bg-amber-500/10 border border-amber-500/20 px-2.5 py-1.5 text-[11px] text-amber-300 leading-snug">
              Reminder popups are paused during assessments to protect your exam concentration.
            </div>
          ) : (
            <div className="my-2.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20 px-2.5 py-1.5 text-[11px] text-emerald-300 leading-snug flex items-center gap-1.5">
              <span className="h-1.5 w-1.5 shrink-0 rounded-full bg-emerald-400" />
              <span>Reminders active for Learning &amp; Practice sections</span>
            </div>
          )}

          {/* Schedule Matrix Info */}
          <div className="my-3 space-y-1.5 text-xs text-navy-300">
            <div className="flex items-center justify-between">
              <span className="flex items-center gap-1.5 text-sky-300">
                <Eye className="h-3.5 w-3.5" /> Eye Care:
              </span>
              <span className="text-navy-400 font-mono">Every 20m</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="flex items-center gap-1.5 text-blue-300">
                <Droplets className="h-3.5 w-3.5" /> Hydration:
              </span>
              <span className="text-navy-400 font-mono">Every 35m</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="flex items-center gap-1.5 text-emerald-300">
                <Activity className="h-3.5 w-3.5" /> Movement:
              </span>
              <span className="text-navy-400 font-mono">Every 50m</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="flex items-center gap-1.5 text-violet-300">
                <HeartPulse className="h-3.5 w-3.5" /> Well-being:
              </span>
              <span className="text-navy-400 font-mono">&gt;60m (q45m)</span>
            </div>
          </div>

          {/* Test Reminders Section */}
          <div className="pt-2 border-t border-navy-800">
            <div className="mb-2 flex items-center justify-between text-[11px]">
              <span className="font-semibold uppercase tracking-wider text-navy-400">
                Preview Reminders
              </span>
              {isAssessmentRoute && (
                <span className="text-[10px] text-amber-400">Disabled in exam</span>
              )}
            </div>
            <div className="grid grid-cols-2 gap-1.5">
              <button
                type="button"
                disabled={isAssessmentRoute}
                onClick={() => handleTestCategory('EYE_CARE')}
                className={`flex items-center gap-1.5 rounded-lg px-2.5 py-1.5 text-xs transition-colors ${
                  isAssessmentRoute
                    ? 'bg-navy-850 text-navy-500 cursor-not-allowed'
                    : 'bg-navy-850 text-sky-300 hover:bg-navy-800'
                }`}
              >
                <Eye className="h-3.5 w-3.5" />
                <span>Eye Care</span>
              </button>
              <button
                type="button"
                disabled={isAssessmentRoute}
                onClick={() => handleTestCategory('HYDRATION')}
                className={`flex items-center gap-1.5 rounded-lg px-2.5 py-1.5 text-xs transition-colors ${
                  isAssessmentRoute
                    ? 'bg-navy-850 text-navy-500 cursor-not-allowed'
                    : 'bg-navy-850 text-blue-300 hover:bg-navy-800'
                }`}
              >
                <Droplets className="h-3.5 w-3.5" />
                <span>Hydration</span>
              </button>
              <button
                type="button"
                disabled={isAssessmentRoute}
                onClick={() => handleTestCategory('MOVEMENT')}
                className={`flex items-center gap-1.5 rounded-lg px-2.5 py-1.5 text-xs transition-colors ${
                  isAssessmentRoute
                    ? 'bg-navy-850 text-navy-500 cursor-not-allowed'
                    : 'bg-navy-850 text-emerald-300 hover:bg-navy-800'
                }`}
              >
                <Activity className="h-3.5 w-3.5" />
                <span>Movement</span>
              </button>
              <button
                type="button"
                disabled={isAssessmentRoute}
                onClick={() => handleTestCategory('MENTAL_WELLBEING')}
                className={`flex items-center gap-1.5 rounded-lg px-2.5 py-1.5 text-xs transition-colors ${
                  isAssessmentRoute
                    ? 'bg-navy-850 text-navy-500 cursor-not-allowed'
                    : 'bg-navy-850 text-violet-300 hover:bg-navy-800'
                }`}
              >
                <HeartPulse className="h-3.5 w-3.5" />
                <span>Mental</span>
              </button>
            </div>
          </div>

          {/* Fast-Forward Simulation */}
          <div className="mt-2.5 pt-2 border-t border-navy-800 flex items-center justify-between text-xs">
            <span className="text-navy-400 flex items-center gap-1">
              <FastForward className="h-3 w-3" /> Simulate:
            </span>
            <div className="flex gap-1.5">
              <button
                type="button"
                disabled={isAssessmentRoute}
                onClick={() => fastForwardMinutes(20)}
                className={`rounded px-2 py-0.5 text-[11px] transition-colors ${
                  isAssessmentRoute
                    ? 'bg-navy-850 text-navy-600 cursor-not-allowed'
                    : 'bg-navy-800 text-navy-300 hover:bg-navy-700 hover:text-white'
                }`}
                title="Fast forward 20 minutes to test eye care"
              >
                +20m
              </button>
              <button
                type="button"
                disabled={isAssessmentRoute}
                onClick={() => fastForwardMinutes(35)}
                className={`rounded px-2 py-0.5 text-[11px] transition-colors ${
                  isAssessmentRoute
                    ? 'bg-navy-850 text-navy-600 cursor-not-allowed'
                    : 'bg-navy-850 text-navy-300 hover:bg-navy-700 hover:text-white'
                }`}
                title="Fast forward 35 minutes to test hydration"
              >
                +35m
              </button>
              <button
                type="button"
                disabled={isAssessmentRoute}
                onClick={() => fastForwardMinutes(60)}
                className={`rounded px-2 py-0.5 text-[11px] transition-colors ${
                  isAssessmentRoute
                    ? 'bg-navy-850 text-navy-600 cursor-not-allowed'
                    : 'bg-navy-850 text-navy-300 hover:bg-navy-700 hover:text-white'
                }`}
                title="Fast forward 60 minutes to test long session"
              >
                +60m
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
