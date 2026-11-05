import { BookOpen, Dumbbell, LayoutDashboard, Menu } from 'lucide-react';
import { NavLink } from 'react-router-dom';

interface Props {
  onOpenDrawer: () => void;
  onOpenPractice: () => void;
}

export default function MobileNav({ onOpenDrawer, onOpenPractice }: Props) {
  return (
    <nav
      className="fixed inset-x-0 bottom-0 z-30 border-t border-line bg-white/95 backdrop-blur-md pb-[env(safe-area-inset-bottom)] shadow-[0_-4px_16px_rgba(10,46,92,0.06)] lg:hidden"
      aria-label="Mobile Navigation"
    >
      <div className="mx-auto flex h-16 max-w-lg items-center justify-around px-2">
        {/* Destination 1: Courses */}
        <NavLink
          to="/courses"
          className={({ isActive }) =>
            `flex flex-col items-center justify-center flex-1 h-full py-1 text-xs font-semibold transition-all m3-touch select-none ${
              isActive ? 'text-sky-950 font-bold' : 'text-navy-500 hover:text-navy-800'
            }`
          }
        >
          {({ isActive }) => (
            <>
              <div
                className={`flex h-8 items-center justify-center rounded-full px-4 transition-all ${
                  isActive ? 'bg-sky-100 text-sky-900 shadow-xs scale-105' : 'text-navy-500'
                }`}
              >
                <BookOpen className="h-5 w-5" aria-hidden />
              </div>
              <span className="mt-1 text-[11px] leading-none">Courses</span>
            </>
          )}
        </NavLink>

        {/* Destination 2: Dashboard */}
        <NavLink
          to="/dashboard"
          className={({ isActive }) =>
            `flex flex-col items-center justify-center flex-1 h-full py-1 text-xs font-semibold transition-all m3-touch select-none ${
              isActive ? 'text-sky-950 font-bold' : 'text-navy-500 hover:text-navy-800'
            }`
          }
        >
          {({ isActive }) => (
            <>
              <div
                className={`flex h-8 items-center justify-center rounded-full px-4 transition-all ${
                  isActive ? 'bg-sky-100 text-sky-900 shadow-xs scale-105' : 'text-navy-500'
                }`}
              >
                <LayoutDashboard className="h-5 w-5" aria-hidden />
              </div>
              <span className="mt-1 text-[11px] leading-none">Dashboard</span>
            </>
          )}
        </NavLink>

        {/* Destination 3: Practice Sets Quick Action */}
        <button
          type="button"
          onClick={onOpenPractice}
          className="flex flex-col items-center justify-center flex-1 h-full py-1 text-xs font-semibold text-navy-500 hover:text-navy-800 transition-all m3-touch select-none"
          aria-label="Open practice sets"
        >
          <div className="flex h-8 items-center justify-center rounded-full px-4 text-navy-500 active:bg-sky-50 active:text-sky-700">
            <Dumbbell className="h-5 w-5" aria-hidden />
          </div>
          <span className="mt-1 text-[11px] leading-none">Practice</span>
        </button>

        {/* Destination 4: More / Navigation Drawer */}
        <button
          type="button"
          onClick={onOpenDrawer}
          className="flex flex-col items-center justify-center flex-1 h-full py-1 text-xs font-semibold text-navy-500 hover:text-navy-800 transition-all m3-touch select-none"
          aria-label="Open navigation drawer"
        >
          <div className="flex h-8 items-center justify-center rounded-full px-4 text-navy-500 active:bg-navy-100">
            <Menu className="h-5 w-5" aria-hidden />
          </div>
          <span className="mt-1 text-[11px] leading-none">More</span>
        </button>
      </div>
    </nav>
  );
}
