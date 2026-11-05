import { useEffect, useRef, useCallback } from 'react';
import toast from 'react-hot-toast';
import { useAuthStore } from '../store/authStore';

/**
 * Enterprise Content Protection Hook:
 * - Prevents copying, cutting, dragging, and selecting of curriculum materials.
 * - Suppresses right-click context menu on protected page elements.
 * - Blocks Ctrl+C, Cmd+C, Ctrl+A, Cmd+A outside of input fields.
 * - Form fields (input, textarea) remain fully functional for typing and editing.
 * - Administrators (user?.role === 'ADMIN') are exempt so they can author course content.
 */
export function useAntiCopy() {
  const { user } = useAuthStore();
  const isAdmin = user?.role === 'ADMIN';
  const lastToastTime = useRef(0);

  const notify = useCallback((msg: string) => {
    const now = Date.now();
    if (now - lastToastTime.current > 2000) {
      lastToastTime.current = now;
      toast.error(msg, { id: 'anti-copy-toast', duration: 2000 });
    }
  }, []);

  useEffect(() => {
    if (isAdmin) return;

    // 2. Block Copy Events and clear clipboard buffer
    const handleCopy = (e: ClipboardEvent) => {
      const target = e.target as HTMLElement | null;
      if (target) {
        const tag = target.tagName?.toLowerCase();
        if (tag === 'input' || tag === 'textarea' || target.isContentEditable) {
          return;
        }
      }
      e.preventDefault();
      if (e.clipboardData) {
        e.clipboardData.setData('text/plain', '');
      }
      notify('Copying course materials is strictly prohibited.');
    };

    // 3. Block Cut Events
    const handleCut = (e: ClipboardEvent) => {
      const target = e.target as HTMLElement | null;
      if (target) {
        const tag = target.tagName?.toLowerCase();
        if (tag === 'input' || tag === 'textarea' || target.isContentEditable) {
          return;
        }
      }
      e.preventDefault();
      notify('Copying is prohibited.');
    };

    // 4. Block Dragging of text and images
    const handleDragStart = (e: DragEvent) => {
      e.preventDefault();
    };

    // 5. Block Selection Start outside form fields
    const handleSelectStart = (e: Event) => {
      const target = e.target as HTMLElement | null;
      if (target) {
        const tag = target.tagName?.toLowerCase();
        if (tag === 'input' || tag === 'textarea' || target.isContentEditable) {
          return;
        }
      }
      e.preventDefault();
    };

    // 6. Keyboard Shortcuts Protection: Ctrl+C, Cmd+C, Ctrl+A outside of input fields
    const handleKeyDown = (e: KeyboardEvent) => {
      const k = e.key ? e.key.toLowerCase() : '';
      const mod = e.ctrlKey || e.metaKey;
      const target = e.target as HTMLElement | null;
      const isInput = target && (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA' || target.isContentEditable);

      if (mod && k === 'c' && !isInput) {
        e.preventDefault();
        notify('Copying is prohibited.');
        return;
      }

      if (mod && k === 'a' && !isInput) {
        e.preventDefault();
        return;
      }
    };

    document.addEventListener('copy', handleCopy);
    document.addEventListener('cut', handleCut);
    document.addEventListener('dragstart', handleDragStart);
    document.addEventListener('selectstart', handleSelectStart);
    window.addEventListener('keydown', handleKeyDown, true);

    return () => {
      document.removeEventListener('copy', handleCopy);
      document.removeEventListener('cut', handleCut);
      document.removeEventListener('dragstart', handleDragStart);
      document.removeEventListener('selectstart', handleSelectStart);
      window.removeEventListener('keydown', handleKeyDown, true);
    };
  }, [notify, isAdmin]);
}
