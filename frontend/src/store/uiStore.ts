import { create } from 'zustand';

interface UiState {
  sidebarOpen: boolean;
  paletteOpen: boolean;
  setSidebarOpen: (open: boolean) => void;
  setPaletteOpen: (open: boolean) => void;
}

export const useUiStore = create<UiState>((set) => ({
  sidebarOpen: false,
  paletteOpen: false,
  setSidebarOpen: (sidebarOpen) => set({ sidebarOpen }),
  setPaletteOpen: (paletteOpen) => set({ paletteOpen }),
}));
