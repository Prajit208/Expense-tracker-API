const THEMES = [
  'daylight',
  'midnight',
  'paper',
  'terminal',
  'ocean',
  'aurora',
  'coffee',
  'forest',
  'mono',
  'monodark',
  'citrus',
]
const DEFAULT_THEME = 'daylight'

function getSavedTheme() {
  try {
    return localStorage.getItem('theme')
  } catch (error) {
    return null
  }
}

function applyTheme(name) {
  if (!THEMES.includes(name)) {
    name = DEFAULT_THEME // unknown or missing name falls back to the default
  }
  document.documentElement.dataset.theme = name
  try {
    localStorage.setItem('theme', name)
  } catch (error) {}
}

// apply right away so the page doesn't flash the wrong theme
applyTheme(getSavedTheme())

// connect the dropdown (it only exists on the dashboard)
document.addEventListener('DOMContentLoaded', function () {
  const switcher = document.getElementById('theme-switcher')
  if (!switcher) return

  switcher.value = document.documentElement.dataset.theme
  switcher.addEventListener('change', function () {
    applyTheme(switcher.value)
  })
})
