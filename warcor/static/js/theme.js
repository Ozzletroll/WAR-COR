// Check for stored theme preferences
var storedTheme = localStorage.getItem('theme')
if (storedTheme) {
  document.documentElement.setAttribute('theme', storedTheme)

  // Get the stylesheet
  var stylesheet = document.styleSheets[0];
  var iconRule
  
  // Iterate through all the rules and get the icon rule
  for(let i = 0; i < stylesheet.cssRules.length; i++) {
    if(stylesheet.cssRules[i].selectorText === '.icon-invert') {
      iconRule = stylesheet.cssRules[i];
    }
  }

  // Set the icon rules to reflect the current theme
  if (storedTheme == "dark" || storedTheme == "ironbow" || storedTheme == "green") {
    iconRule.style.setProperty("filter", "100");
  }
  else {
    iconRule.style.setProperty("filter", "none");
  }

}
else {
  document.documentElement.setAttribute('theme', null)
  localStorage.setItem('theme', null);
}
