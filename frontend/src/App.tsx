import { Suspense, lazy } from 'react';
import { Navigate, Route, Routes } from 'react-router-dom';
import Button from './components/common/Button';
import Modal from './components/common/Modal';
import { PageSkeleton } from './components/common/Skeleton';
import WellnessToast from './components/common/WellnessToast';
import EndOfSessionModal from './components/common/EndOfSessionModal';
import ResumeSessionModal from './components/common/ResumeSessionModal';
import ScreenshotProtection from './components/common/ScreenshotProtection';
import AppLayout from './components/layout/AppLayout';
import ProtectedRoute from './components/layout/ProtectedRoute';
import { useSessionGuard } from './hooks/useSessionGuard';
import { useWellnessReminder } from './hooks/useWellnessReminder';
import { useAntiCopy } from './hooks/useAntiCopy';
import CourseCatalogPage from './pages/CourseCatalogPage';
import CourseDetailPage from './pages/CourseDetailPage';
import DashboardPage from './pages/DashboardPage';
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import NotFoundPage from './pages/NotFoundPage';
import RegisterPage from './pages/RegisterPage';
import { useAuthStore } from './store/authStore';
import { useResumeSessionStore } from './store/resumeSessionStore';
import { useEffect } from 'react';

// Heavy screens (webcam, admin tooling) load on demand.
const GradedAssessmentPage = lazy(() => import('./pages/GradedAssessmentPage'));
const AssessmentPreStartPage = lazy(() => import('./pages/AssessmentPreStartPage'));
const PracticeAssessmentPage = lazy(() => import('./pages/PracticeAssessmentPage'));
const ResultPage = lazy(() => import('./pages/ResultPage'));
const AdminDashboardPage = lazy(() => import('./pages/AdminDashboardPage'));

export default function App() {
  useSessionGuard();
  useWellnessReminder();
  useAntiCopy();
  const { revokedReason, dismissRevoked, user, isAuthenticated } = useAuthStore();

  useEffect(() => {
    if (isAuthenticated && user?.id && user.role !== 'ADMIN') {
      useResumeSessionStore.getState().checkAndTriggerResume(user).catch(() => {});
    }
  }, [isAuthenticated, user]);

  return (
    <>
      <Suspense fallback={<div className="mx-auto max-w-3xl p-6"><PageSkeleton /></div>}>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          <Route element={<ProtectedRoute />}>
            {/* The exam screen has no navigation chrome on purpose */}
            <Route path="/attempts/:attemptId" element={<GradedAssessmentPage />} />
            <Route element={<AppLayout />}>
              <Route path="/dashboard" element={<DashboardPage />} />
              <Route path="/courses" element={<CourseCatalogPage />} />
              <Route path="/courses/:slug" element={<CourseDetailPage />} />
              <Route path="/assessments/:id" element={<AssessmentPreStartPage />} />
              <Route path="/practice/:id" element={<PracticeAssessmentPage />} />
              <Route path="/results/:attemptId" element={<ResultPage />} />
            </Route>
          </Route>

          <Route element={<ProtectedRoute roles={['ADMIN']} />}>
            <Route element={<AppLayout />}>
              <Route path="/admin" element={<AdminDashboardPage />} />
            </Route>
          </Route>

          <Route path="/home" element={<Navigate to="/" replace />} />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </Suspense>

      {/* Floating wellness reminders toast */}
      <WellnessToast />

      {/* End of session wrap-up modal on logout */}
      <EndOfSessionModal />

      {/* Resume what the user finished in the last login modal */}
      <ResumeSessionModal />

      {/* Enterprise Screenshot and Screen Capture protection for Web and Mobile */}
      <ScreenshotProtection />

      {/* Shown when the session ended remotely (another device logged in, or an admin revoked it) */}
      <Modal
        open={Boolean(revokedReason)}
        dismissible={false}
        tone="warning"
        title="You've been logged out"
        footer={<Button onClick={() => { dismissRevoked(); window.location.assign('/login'); }}>Go to sign in</Button>}
      >
        <p>{revokedReason === 'Session ended.' || !revokedReason ? 'Your account was accessed from another device. You\'ve been logged out.' : revokedReason}</p>
      </Modal>
    </>
  );
}
