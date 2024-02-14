// Searchbar class
class SearchbarTab {
  constructor({
    tab,
    button,
  }) {
    this.tab = document.getElementById(tab);
    this.button = document.getElementById(button);
    this.outer = this.tab.querySelector(".searchbar-outer");
    this.area = this.tab.querySelector(".searchbar-area");
    this.areaInner = this.tab.querySelector(".search-bar");
    this.goButton = this.tab.querySelector(".searchbar-go");
    this.advancedSearch = this.tab.querySelector(".advanced-search-area");
    this.hitsLabel = this.tab.querySelector(".hits-area");
    this.state = false
   
    window.addEventListener('resize', this.getWidth.bind(this));
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
    this.tab.style.transform = "translateX(calc(-100% + 40px)";
    this.areaInner.setAttribute("aria-hidden", "false");
    this.areaInner.setAttribute("tabindex", "0");
    if (this.goButton != null) {
      this.goButton.setAttribute("tabindex", "0");
    }
    if (this.advancedSearch != null) {
      this.advancedSearch.setAttribute("tabindex", "0");
    }
    this.hitsLabel.setAttribute("aria-hidden", "false");
    this.state = true;
    this.getWidth();
  }

  closeTab() {
    this.tab.style.width = "";
    this.tab.style.transform = "";
    this.areaInner.setAttribute("aria-hidden", "true");
    this.areaInner.setAttribute("tabindex", "-1");
    if (this.goButton != null) {
      this.goButton.setAttribute("tabindex", "-1");
    }
    if (this.advancedSearch != null) {
      this.advancedSearch.setAttribute("tabindex", "-1");
    }
    this.hitsLabel.setAttribute("aria-hidden", "true");
    this.state = false;
  }

  getWidth() {
    if (window.innerWidth <= 600 && this.state == true) {
      this.outer.style.justifyContent = "space-between";
      this.tab.style.width = "100vw";
      this.area.style.flex = "4 1 0";
      this.area.style.marginLeft = "10px";
      this.areaInner.style.width = "100%";
    }
    else {
      this.outer.style.justifyContent = "";
      this.tab.style.width = "";
      this.area.style.flex = "";
      this.area.style.marginLeft = "";
      this.areaInner.style.width = "";
    }
  }
}

// Create searchbar
const searchbar = new SearchbarTab({
  tab: "searchbar",
  button: "searchbar-button",
})


