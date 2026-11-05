import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { useWellnessStore } from '../store/wellnessStore';

/**
 * Hook to manage study session wellness reminder timers and periodic interval checks.
 * Reminders only run during learning & practice sections, and are paused during assessments.
 */
export function useWellnessReminder() {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const location = useLocation();
  const {
    sessionStartTime,
    initSession,
    resetSession,
    setAssessmentActive,
    checkIntervals,
    activeReminder,
    dismissReminder,
    triggerManualReminder,
    triggerEndOfSession,
    isEndOfSessionOpen,
    dismissEndOfSession,
    elapsedMinutes,
    elapsedSeconds,
    fastForwardMinutes,
  } = useWellnessStore();

  // Check if current route is part of an assessment (proctored attempt, pre-start, or result)
  const isAssessmentRoute =
    location.pathname.startsWith('/attempts') ||
    location.pathname.startsWith('/assessments') ||
    location.pathname.startsWith('/results');

  // Synchronize assessment active flag with store and dismiss any active reminder on assessment entry
  useEffect(() => {
    setAssessmentActive(isAssessmentRoute);
    if (isAssessmentRoute && activeReminder) {
      dismissReminder();
    }
  }, [isAssessmentRoute, setAssessmentActive, activeReminder, dismissReminder]);

  // Initialize session timer as soon as user is authenticated
  useEffect(() => {
    if (isAuthenticated) {
      if (!sessionStartTime) {
        initSession();
      }
    } else {
      resetSession();
    }
  }, [isAuthenticated, sessionStartTime, initSession, resetSession]);

  // Periodic interval runner (checks every 5 seconds) - ONLY active in Learning & Practice sections
  useEffect(() => {
    if (!isAuthenticated || isAssessmentRoute) return;

    // Run immediate check
    checkIntervals();

    const intervalId = window.setInterval(() => {
      checkIntervals();
    }, 5000);

    return () => {
      window.clearInterval(intervalId);
    };
  }, [isAuthenticated, isAssessmentRoute, checkIntervals]);

  return {
    activeReminder,
    dismissReminder,
    triggerManualReminder,
    triggerEndOfSession,
    isEndOfSessionOpen,
    dismissEndOfSession,
    elapsedMinutes,
    elapsedSeconds,
    fastForwardMinutes,
  };
}
