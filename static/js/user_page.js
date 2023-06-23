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
    this.tab.style.display = "flex"
    this.tab.style.flexDirection = "column"
    this.tab.style.maxHeight = "fit-content";
    this.state = true
  }

  closeTab() {
    this.tab.style.maxHeight = "0";
    this.tab.style.marginTop = "-20px";
    this.tab.style.display = "none"
    this.state = false
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
