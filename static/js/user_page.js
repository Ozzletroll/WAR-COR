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
    this.state = true
  }

  closeTab() {
    this.tab.style.maxHeight = "0";
    this.tab.style.marginTop = "-20px";
    this.tab.style.display = "none";
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


function themeToggle() {

  var theme = document.querySelector('input[name="theme"]:checked').value;
  console.log(theme);

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
