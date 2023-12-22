// Tab class
class Tab {
  constructor({
    tab,
    button,
  }) {
    this.tab = document.getElementById(tab);
    this.button = button;
    this.state = false

    document.getElementById(this.button).onclick = event => {
      
      if (this.state == false) {
        this.openTab(event)
      }
      else if (this.state == true) {
        this.closeTab(event)
      }
    } 
  }
  
  openTab() {
    this.tab.style.marginTop = "20px";
    this.tab.style.display = "flex";
    this.tab.style.flexDirection = "column";
    this.tab.style.maxHeight = "fit-content";

    document.getElementById(this.button).style.borderBottomLeftRadius = "0px";
    document.getElementById(this.button).style.borderBottomRightRadius = "0px";


    this.state = true
  }

  closeTab() {
    this.tab.style.maxHeight = "0";
    this.tab.style.marginTop = "-20px";
    this.tab.style.display = "none";

    document.getElementById(this.button).style.borderBottomLeftRadius = "5px";
    document.getElementById(this.button).style.borderBottomRightRadius = "5px";


    this.state = false;
  }

}

// Toggle button class
class ToggleButton {
  constructor({
    form,
    button,
  }) {
    this.form = document.getElementById(form);
    this.button = button;
    this.state = false;

    document.getElementById(this.button).onclick = event => {
      
      if (this.state == false) {
        this.openForm(event);
      }
      else if (this.state == true) {
        this.closeForm(event);
      }
    } 
  }
  
  openForm() {
    this.form.style.display = "flex";
    this.state = true;
  }

  closeForm() {
    this.form.style.display = "none";
    this.state = false;
  }

}

// Create tabs
const tab_1 = new Tab({
  tab: "tab-1",
  button: "t1-button",
})

const tab_2 = new Tab({
  tab: "tab-2",
  button: "t2-button",
})

const tab_3 = new Tab({
  tab: "tab-3",
  button: "t3-button",
})

// Create toggle buttons

const pref_1 = new ToggleButton({
  form: "pref-1",
  button: "p1-button"
})

const toggle_1 = new ToggleButton({
  form: "form-1",
  button: "f1-button"
})

const toggle_2 = new ToggleButton({
  form: "form-2",
  button: "f2-button"
})


// Function called when toggling between different themes
function themeToggle() {

  // Get the stylesheet
  var stylesheet = document.styleSheets[1];
  var iconRule
  
  // Iterate through all the rules and get the icon rule
  for(let i = 0; i < stylesheet.cssRules.length; i++) {
    if(stylesheet.cssRules[i].selectorText === '.icon-invert') {
      iconRule = stylesheet.cssRules[i];
    }
  }

  var targetTheme = document.querySelector('input[name="theme"]:checked').value;
  
  if (targetTheme == "light") {
    targetTheme = null;
    iconRule.style.setProperty("filter", 'none');
  }
  else {
    iconRule.style.setProperty("filter", 'invert(100)');
  }

  var currentTheme = document.documentElement.getAttribute("theme");

  if (currentTheme == null || currentTheme == "null") {
    document.documentElement.setAttribute('theme', targetTheme);
  }
  else if (currentTheme == "dark") {
    document.documentElement.setAttribute('theme', targetTheme);
  }
  else if (currentTheme == "ironbow") {
    document.documentElement.setAttribute('theme', targetTheme);
  }
  else if (currentTheme == "green") {
    document.documentElement.setAttribute('theme', targetTheme);
  }
  else if (currentTheme == "horus") {
    document.documentElement.setAttribute('theme', targetTheme);
  }

  localStorage.setItem('theme', targetTheme);

  // Dispatch a custom event to indicate the change to theme.js
  var event = new CustomEvent("localstoragechange");
  window.dispatchEvent(event);
}

// Set theme radio button to show the current theme
var storedTheme = localStorage.getItem('theme')
if (storedTheme) {

  var radio;

  if (storedTheme == "light" || storedTheme == "null") {
    radio = "theme-1";
  }
  else if (storedTheme == "dark") {
    radio = "theme-2";
  }
  else if (storedTheme == "ironbow") {
    radio = "theme-3";
  }
  else if (storedTheme == "green") {
    radio = "theme-4";
  }
  else if (storedTheme == "horus") {
    radio = "theme-5";
  }
  
  document.getElementById(radio).checked = true;

}