import { useState } from 'react';
import { motion } from 'framer-motion';
import { Outlet, useLocation } from 'react-router-dom';
import MobileNav from './MobileNav';
import Navbar from './Navbar';
import Sidebar from './Sidebar';
import NavigationDrawer from './NavigationDrawer';
import PracticeBottomSheet from './PracticeBottomSheet';

/** Chrome for every page except the exam screen, fully optimized for Android M3 */
export default function AppLayout() {
  const { pathname } = useLocation();
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [practiceOpen, setPracticeOpen] = useState(false);

  return (
    <div className="min-h-screen bg-canvas">
      {/* Material 3 Top App Bar */}
      <Navbar onOpenDrawer={() => setDrawerOpen(true)} />

      {/* Main Content Area with 8dp-grid padding and safe clearance */}
      <div className="mx-auto flex max-w-7xl gap-6 px-3 sm:px-6 pt-4 sm:pt-6 pb-28 lg:pb-12">
        <Sidebar />
        <motion.main
          key={pathname}
          className="min-w-0 flex-1"
          initial={{ opacity: 0, y: 6 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.18, ease: [0.2, 0, 0, 1] }}
        >
          <Outlet />
        </motion.main>
      </div>

      {/* Material 3 Bottom Navigation Bar for Mobile */}
      <MobileNav
        onOpenDrawer={() => setDrawerOpen(true)}
        onOpenPractice={() => setPracticeOpen(true)}
      />

      {/* Material 3 Modal Navigation Drawer */}
      <NavigationDrawer
        open={drawerOpen}
        onClose={() => setDrawerOpen(false)}
        onOpenPracticeSheet={() => setPracticeOpen(true)}
      />

      {/* Material 3 Practice Sets Bottom Sheet */}
      <PracticeBottomSheet
        open={practiceOpen}
        onClose={() => setPracticeOpen(false)}
      />
    </div>
  );
}

