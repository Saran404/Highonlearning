import { AnimatePresence, motion } from 'framer-motion';
import {
  BookOpen,
  LayoutDashboard,
  LogOut,
  ShieldAlert,
  X,
  Clock,
  Sparkles,
  Languages,
} from 'lucide-react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import { useCourseStore } from '../../store/courseStore';
import { useWellnessStore } from '../../store/wellnessStore';
import BrandLogo from '../common/BrandLogo';

interface Props {
  open: boolean;
  onClose: () => void;
  onOpenPracticeSheet?: () => void;
}

export default function NavigationDrawer({ open, onClose, onOpenPracticeSheet }: Props) {
  const { user, logout, hasRole } = useAuthStore();
  const { elapsedMinutes, triggerEndOfSession } = useWellnessStore();
  const navigate = useNavigate();

  const executeLogout = async () => {
    onClose();
    await logout();
    useCourseStore.getState().reset();
    navigate('/login', { replace: true });
  };

  const handleLogoutClick = () => {
    triggerEndOfSession(executeLogout);
  };

  const currentLang = localStorage.getItem('exampro_lang') === 'ta' ? 'ta' : 'en';

  const toggleLanguage = () => {
    const next = currentLang === 'en' ? 'ta' : 'en';
    localStorage.setItem('exampro_lang', next);
    window.location.reload();
  };

  return (
    <AnimatePresence>
      {open && (
        <div className="fixed inset-0 z-50 flex lg:hidden">
          {/* Backdrop Scrim */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            onClick={onClose}
            className="fixed inset-0 bg-navy-950/60 backdrop-blur-[2px]"
            aria-hidden="true"
          />

          {/* M3 Modal Navigation Drawer */}
          <motion.aside
            role="dialog"
            aria-modal="true"
            aria-label="Navigation drawer"
            initial={{ x: '-100%' }}
            animate={{ x: 0 }}
            exit={{ x: '-100%' }}
            transition={{ type: 'spring', damping: 28, stiffness: 300 }}
            className="relative z-10 flex h-full w-[310px] max-w-[85vw] flex-col rounded-r-3xl bg-white shadow-2xl pb-safe"
          >
            {/* Header / Brand */}
            <div className="flex items-center justify-between border-b border-line px-5 py-4 pt-safe">
              <BrandLogo to="/courses" size="sm" />
              <button
                type="button"
                onClick={onClose}
                className="flex h-11 w-11 items-center justify-center rounded-full text-navy-500 hover:bg-navy-50 active:bg-navy-100"
                aria-label="Close navigation drawer"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            {/* User Profile Card */}
            <div className="border-b border-line bg-navy-50/60 p-5">
              <div className="flex items-center gap-3">
                <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-navy to-sky-700 text-lg font-bold text-white shadow-xs">
                  {user?.name?.slice(0, 1).toUpperCase()}
                </div>
                <div className="min-w-0 flex-1">
                  <div className="truncate font-bold text-navy">{user?.name}</div>
                  <div className="truncate text-xs text-navy-500">{user?.email}</div>
                  <span className="mt-1 inline-flex items-center rounded-full bg-navy-100 px-2 py-0.5 text-[10px] font-semibold text-navy-700">
                    {user?.role === 'ADMIN' ? 'Administrator' : 'Student'}
                  </span>
                </div>
              </div>

              {/* Study session pill */}
              <div className="mt-3 flex items-center justify-between rounded-xl bg-white p-2.5 border border-line text-xs">
                <span className="flex items-center gap-1.5 text-navy-600 font-medium">
                  <Clock className="h-4 w-4 text-sky-600" /> Study Session
                </span>
                <span className="font-bold text-navy">{elapsedMinutes} mins</span>
              </div>
            </div>

            {/* Navigation Destinations */}
            <div className="flex-1 overflow-y-auto px-3 py-4 space-y-1">
              <div className="px-3 pb-1 text-[11px] font-bold uppercase tracking-wider text-navy-400">
                Main Menu
              </div>

              <NavLink
                to="/courses"
                onClick={onClose}
                className={({ isActive }) =>
                  `flex items-center gap-3.5 rounded-full px-4 py-3 text-sm font-semibold transition-all m3-touch min-h-[48px] ${
                    isActive
                      ? 'bg-sky-100 text-sky-950 shadow-xs'
                      : 'text-navy-700 hover:bg-navy-50 active:bg-navy-100'
                  }`
                }
              >
                <BookOpen className="h-5 w-5 text-sky-700" />
                <span>Courses & Syllabus</span>
              </NavLink>

              <NavLink
                to="/dashboard"
                onClick={onClose}
                className={({ isActive }) =>
                  `flex items-center gap-3.5 rounded-full px-4 py-3 text-sm font-semibold transition-all m3-touch min-h-[48px] ${
                    isActive
                      ? 'bg-sky-100 text-sky-950 shadow-xs'
                      : 'text-navy-700 hover:bg-navy-50 active:bg-navy-100'
                  }`
                }
              >
                <LayoutDashboard className="h-5 w-5 text-sky-700" />
                <span>My Dashboard</span>
              </NavLink>

              {onOpenPracticeSheet && (
                <button
                  type="button"
                  onClick={() => {
                    onClose();
                    onOpenPracticeSheet();
                  }}
                  className="flex w-full items-center gap-3.5 rounded-full px-4 py-3 text-sm font-semibold text-navy-700 hover:bg-navy-50 active:bg-navy-100 transition-all m3-touch min-h-[48px] text-left"
                >
                  <Sparkles className="h-5 w-5 text-amber-600" />
                  <span>Practice Questions</span>
                </button>
              )}

              {hasRole('ADMIN') && (
                <NavLink
                  to="/admin"
                  onClick={onClose}
                  className={({ isActive }) =>
                    `flex items-center gap-3.5 rounded-full px-4 py-3 text-sm font-semibold transition-all m3-touch min-h-[48px] ${
                      isActive
                        ? 'bg-sky-100 text-sky-950 shadow-xs'
                        : 'text-navy-700 hover:bg-navy-50 active:bg-navy-100'
                    }`
                  }
                >
                  <ShieldAlert className="h-5 w-5 text-amber-600" />
                  <span>Admin Panel</span>
                </NavLink>
              )}

              <div className="pt-4 px-3 pb-1 text-[11px] font-bold uppercase tracking-wider text-navy-400">
                Preferences
              </div>

              {/* Language Switcher */}
              <button
                type="button"
                onClick={toggleLanguage}
                className="flex w-full items-center justify-between rounded-full px-4 py-3 text-sm font-semibold text-navy-700 hover:bg-navy-50 active:bg-navy-100 transition-all m3-touch min-h-[48px]"
              >
                <div className="flex items-center gap-3.5">
                  <Languages className="h-5 w-5 text-sky-700" />
                  <span>Language</span>
                </div>
                <span className="rounded-lg bg-sky-50 px-2 py-0.5 text-xs font-bold text-sky-800 border border-sky-200">
                  {currentLang === 'ta' ? 'தமிழ்' : 'English'}
                </span>
              </button>
            </div>

            {/* Drawer Footer with Logout */}
            <div className="border-t border-line p-4">
              <button
                type="button"
                onClick={handleLogoutClick}
                className="flex w-full items-center justify-center gap-2 rounded-xl border border-line bg-white py-3 text-sm font-semibold text-navy-700 hover:bg-navy-50 active:bg-navy-100 m3-touch min-h-[48px]"
              >
                <LogOut className="h-4 w-4 text-navy-500" />
                <span>Log out</span>
              </button>
            </div>
          </motion.aside>
        </div>
      )}
    </AnimatePresence>
  );
}
