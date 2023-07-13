// Check for stored theme preferences
var storedTheme = localStorage.getItem('theme')
if (storedTheme) {
  document.documentElement.setAttribute('theme', storedTheme)
}

