import { ArrowLeft, LogOut, Menu } from 'lucide-react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import { useCourseStore } from '../../store/courseStore';
import { useWellnessStore } from '../../store/wellnessStore';
import Button from '../common/Button';
import BrandLogo from '../common/BrandLogo';
import WellnessCompanion from './WellnessCompanion';

interface Props {
  onOpenDrawer?: () => void;
}

export default function Navbar({ onOpenDrawer }: Props) {
  const { user, logout } = useAuthStore();
  const { triggerEndOfSession } = useWellnessStore();
  const navigate = useNavigate();
  const { pathname } = useLocation();

  const isSubPage = pathname !== '/courses' && pathname !== '/dashboard' && pathname !== '/admin';

  const executeLogout = async () => {
    await logout();
    useCourseStore.getState().reset();
    navigate('/login', { replace: true });
  };

  const handleLogoutClick = () => {
    triggerEndOfSession(executeLogout);
  };

  return (
    <header className="sticky top-0 z-30 border-b border-navy-800 bg-navy text-white pt-safe shadow-xs">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between gap-3 sm:gap-6 px-2.5 sm:px-4">
        {/* Leading: Back Button on Sub-pages OR Hamburger on Top pages */}
        <div className="flex items-center gap-1 sm:gap-2.5 min-w-0">
          {isSubPage ? (
            <button
              type="button"
              onClick={() => navigate(-1)}
              className="flex h-10 w-10 sm:h-11 sm:w-11 shrink-0 items-center justify-center rounded-full text-white/90 hover:bg-white/10 active:bg-white/20 transition-all m3-touch"
              aria-label="Back"
            >
              <ArrowLeft className="h-5 w-5" />
            </button>
          ) : (
            <button
              type="button"
              onClick={onOpenDrawer}
              className="flex h-10 w-10 sm:h-11 sm:w-11 shrink-0 items-center justify-center rounded-full text-white/90 hover:bg-white/10 active:bg-white/20 transition-all m3-touch lg:hidden"
              aria-label="Open navigation menu"
            >
              <Menu className="h-5 w-5" />
            </button>
          )}

          <BrandLogo to="/courses" size="md" onDark />
        </div>

        {/* Trailing: Wellness Companion, User Profile, Logout */}
        <div className="flex items-center gap-2 sm:gap-3 shrink-0">
          <WellnessCompanion />
          <div className="hidden text-right text-sm leading-tight md:block">
            <div className="font-medium">{user?.name}</div>
            <div className="text-xs text-navy-200">{user?.role === 'ADMIN' ? 'Administrator' : user?.email}</div>
          </div>
          <button
            type="button"
            onClick={onOpenDrawer}
            className="flex h-9 w-9 sm:h-10 sm:w-10 shrink-0 items-center justify-center rounded-full bg-sky text-sm font-bold text-white shadow-xs m3-touch lg:cursor-default"
            aria-label="User profile"
          >
            {user?.name?.slice(0, 1).toUpperCase()}
          </button>
          <Button
            variant="ghost"
            size="sm"
            onClick={handleLogoutClick}
            icon={<LogOut className="h-4 w-4" />}
            className="hidden md:inline-flex !text-white hover:!bg-navy-700"
            aria-label="Log out"
          >
            <span>Log out</span>
          </Button>
        </div>
      </div>
    </header>
  );
}

