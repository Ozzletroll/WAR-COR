// Sidebar class
class Tab {
  constructor({
    tab,
    button,
    icon,
  }) {
    this.tab = document.getElementById(tab);
    this.button = button;
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
    this.tab.style.width = "300px"
    this.state = true
    this.icon.src = "/static/images/icons/chevron_left.svg"
  }

  closeTab() {
    this.tab.style.width = "0"
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
