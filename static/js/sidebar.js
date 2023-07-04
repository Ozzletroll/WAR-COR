// Sidebar class
class Tab {
  constructor({
    tab,
    button,
    icon,
  }) {
    this.tab = document.getElementById(tab);
    this.button = button;
    this.button_elem = document.getElementById(button);
    this.state = false
    this.icon = document.getElementById(icon);

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
    this.tab.style.transform = "translateX(0)"
    this.button_elem.style.transform = "translateX(0)"
    this.state = true
    this.icon.src = "/static/images/icons/chevron_left.svg"
  }

  closeTab() {
    this.tab.style.transform = "translateX(-300px)"
    this.button_elem.style.transform = "translateX(-300px)"
    this.state = false
    this.icon.src = "/static/images/icons/chevron_right.svg"
  }

}


// Create sidebar
const tab_1 = new Tab({
  tab: "sidebar",
  button: "sidebar-deploy",
  icon: "sidebar-icon"
})
