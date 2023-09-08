// Message tab class
class messageTab {
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
    this.tab.style.marginBottom = "-300px"
    this.tab.style.height = "300px"
    this.tab.style.borderBottom = "1px solid var(--elem_border)"
    this.state = true
  }

  closeTab() {
    this.tab.style.marginBottom = "0"
    this.tab.style.height = "0"
    this.tab.style.borderBottom = "0px solid var(--elem_border)"

    this.state = false
  }

}

// Create messages tab
const messages_tab = new messageTab({
  tab: "messages-tab",
  button: "messages-button",
})
