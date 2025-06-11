import { ref, onMounted } from 'vue';

const themes = [
  { key: 'theme-nebula-red', label: 'Nebula Red' },
  { key: 'theme-solar-flare', label: 'Solar Flare' },
  { key: 'theme-stellar-gold', label: 'Stellar Gold' },
  { key: 'theme-cosmic-silver', label: 'Cosmic Silver' },
];

const THEME_KEY = 'galactic-theme';

export function useTheme() {
  const currentTheme = ref<string>(themes[0].key);

  // Apply theme class to body
  const applyTheme = (themeKey: string) => {
    document.body.classList.remove(...themes.map(t => t.key));
    document.body.classList.add(themeKey);
    currentTheme.value = themeKey;
    localStorage.setItem(THEME_KEY, themeKey);
  };

  // On mount, load theme from localStorage or default
  onMounted(() => {
    const saved = localStorage.getItem(THEME_KEY);
    if (saved && themes.some(t => t.key === saved)) {
      applyTheme(saved);
    } else {
      applyTheme(themes[0].key);
    }
  });

  return {
    themes,
    currentTheme,
    applyTheme,
  };
}
