import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import type { Role } from '../../types';

interface Props {
  roles?: Role[];
}

/** Wrap routes that need a signed-in user (and optionally a role). Renders nested routes via <Outlet />. */
export default function ProtectedRoute({ roles }: Props) {
  const { isAuthenticated, user } = useAuthStore();
  const location = useLocation();

  if (!isAuthenticated || !user) return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  if (roles && !roles.includes(user.role)) return <Navigate to="/courses" replace />;
  return <Outlet />;
}
