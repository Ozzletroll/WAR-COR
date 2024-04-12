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
    this.page = document.querySelector(".page");
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
    this.getWidth();
    this.tab.style.transform = `translateX(calc(-100% + ${40}px)`;
    this.areaInner.setAttribute("aria-hidden", "false");
    this.areaInner.setAttribute("tabindex", "0");
    if (this.goButton != null) {
      this.goButton.setAttribute("tabindex", "0");
    }
    if (this.advancedSearch != null) {
      this.advancedSearch.setAttribute("tabindex", "0");
      this.advancedSearch.setAttribute("aria-hidden", "false");
    }
    this.hitsLabel.setAttribute("aria-hidden", "false");
    this.state = true;
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
      this.advancedSearch.setAttribute("aria-hidden", "true");
    }
    this.hitsLabel.setAttribute("aria-hidden", "true");
    this.state = false;

    // Trigger event to searchEngine class to clear search
    var clearSearchEvent = new CustomEvent("clearSearchEvent");
    document.dispatchEvent(clearSearchEvent)
  }

  getWidth() {
    if (window.innerWidth <= 600) {
      this.outer.style.justifyContent = "space-between";
      this.tab.style.width = `${window.innerWidth - this.getScrollbarWidth()}px`;
      this.area.style.marginLeft = "10px";
      this.area.style.width = "100%";
      this.areaInner.style.width = "100%";
    }
    else {
      this.outer.style.justifyContent = "";
      this.tab.style.width = "";
      this.area.style.width = "";
      this.area.style.marginLeft = "";
      this.areaInner.style.width = "";
    }
  }

  getScrollbarWidth() {
    var scrollbarWidth = window.innerWidth - document.documentElement.clientWidth;
    return scrollbarWidth;
  }
}

// Create searchbar
const searchbar = new SearchbarTab({
  tab: "searchbar",
  button: "searchbar-button",
})
