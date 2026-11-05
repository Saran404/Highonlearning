import { BookOpen, LayoutDashboard, ShieldAlert } from 'lucide-react';
import type { LucideIcon } from 'lucide-react';
import type { Role } from '../../types';

export interface NavItem {
  to: string;
  label: string;
  icon: LucideIcon;
  roles?: Role[];
}

export const NAV_ITEMS: NavItem[] = [
  { to: '/courses', label: 'Courses', icon: BookOpen },
  { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/admin', label: 'Admin', icon: ShieldAlert, roles: ['ADMIN'] },
];
