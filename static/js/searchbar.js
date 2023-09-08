// Sidebar class
class SearchbarTab {
  constructor({
    tab,
    button,
  }) {
    this.tab = document.getElementById(tab);
    this.button = document.getElementById(button);
    this.state = false
   
    document.getElementById(button).onclick = event => {

      if (this.state == false) {
        this.openTab(event)
      }
      else if (this.state == true) {
        this.closeTab(event)
      }
    }
  }

  openTab() {
    this.tab.style.transform = "translateX(0)";
    this.state = true;
  }

  closeTab() {
    this.tab.style.transform = "translateX(310px)";
    this.state = false;
  }

}

// Create sidebar
const searchbar = new SearchbarTab({
  tab: "searchbar",
  button: "searchbar-button",
})
