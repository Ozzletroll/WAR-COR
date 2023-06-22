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
    this.tab.style.maxHeight = "2000px";
    this.tab.style.marginTop = "20px";
    this.state = true
  }

  closeTab() {
    this.tab.style.maxHeight = "0";
    this.tab.style.marginTop = "-20px";
    this.state = false
  }

}

// Create tabs
const tab_1 = new Tab({
  tab: "tab-1",
  button: "t1-button",
})

