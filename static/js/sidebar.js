// Sidebar class
class Tab {
  constructor({
    tab,
    button,
    icon,
    timeline,
    monthConnectors,
  }) {
    this.tab = document.getElementById(tab);
    this.button = button;
    this.button_elem = document.getElementById(button);
    this.state = false
    this.icon = document.getElementById(icon);
    this.timeline = document.getElementById(timeline);
    this.monthConnectors = document.getElementsByClassName("month-connector");

    this.updateTimelineMargin();

    window.addEventListener('resize', this.updateTimelineMargin.bind(this));

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
    this.tab.style.marginRight = "0"
    this.state = true
    this.icon.src = "/static/images/icons/chevron_left.svg"

    // Iterate through all month connectors, and alter width
    for (let i = 0; i < this.monthConnectors.length; i++) {
      this.monthConnectors[i].style.minWidth = "15%";
    }

    this.updateTimelineMargin();
  }

  closeTab() {
    this.tab.style.transform = "translateX(-300px)"
    this.button_elem.style.transform = "translateX(0)"
    this.tab.style.marginRight = "-300px"
    this.state = false
    this.icon.src = "/static/images/icons/chevron_right.svg"

      // Iterate through all month connectors, and alter width
      for (let i = 0; i < this.monthConnectors.length; i++) {
        this.monthConnectors[i].style.minWidth = "30%";
      }

    this.timeline.style.marginLeft = "0"
  }

  // Adjust margin if sidebar deployed and screen between 800 and 850px
  updateTimelineMargin() {
    if (window.innerWidth >= 800 && window.innerWidth <= 900 && this.state == true) {
      this.timeline.style.marginLeft = "-15%";
    } else {
      this.timeline.style.marginLeft = "";
    }
  }
}


// Create sidebar
const sidebar = new Tab({
  tab: "sidebar",
  button: "sidebar-deploy",
  icon: "sidebar-icon",
  timeline: "timeline-container",
  monthConnectors: "month-connector",
})
