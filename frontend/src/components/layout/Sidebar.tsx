import { NavLink } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import { NAV_ITEMS } from './navItems';

export default function Sidebar() {
  const hasRole = useAuthStore((s) => s.hasRole);
  return (
    <aside className="hidden w-56 shrink-0 lg:block">
      <nav className="sticky top-20 space-y-1" aria-label="Main">
        {NAV_ITEMS.filter((i) => !i.roles || hasRole(...i.roles)).map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `group flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all ${
                isActive
                  ? 'bg-navy-900 text-white shadow-xs'
                  : 'text-navy-700 hover:bg-sky-50/80 hover:text-sky-900'
              }`
            }
          >
            {({ isActive }) => (
              <>
                <Icon className={`h-5 w-5 transition-colors ${isActive ? 'text-amber-400' : 'text-navy-400 group-hover:text-sky-600'}`} aria-hidden />
                {label}
              </>
            )}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
