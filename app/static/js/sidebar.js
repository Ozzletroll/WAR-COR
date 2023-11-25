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
    this.buttonElem = document.getElementById(button);
    this.state = false
    this.icon = document.getElementById(icon);
    this.timeline = document.getElementById(timeline);
    this.monthConnectors = document.getElementsByClassName("month-connector");

    // Call check screensize on initialisation, 
    // and again anytime the viewport is resized
    this.checkScreenSize();
    window.addEventListener('resize', this.checkScreenSize.bind(this));

    document.getElementById(this.button).onclick = event => {

      if (this.state == false) {
        this.openTab(event)
      }
      else if (this.state == true) {
        this.closeTab(event)
      }
    }
  }

  checkScreenSize() {
    if (window.innerWidth >= 1200 && this.state == true) {
      this.tab.style.marginRight = "300px";
    }
    else {
      this.tab.style.marginRight = "0px"
    }
  }

  openTab() {
    this.tab.style.transform = "translateX(300px)";

    if (window.innerWidth >= 1200 ) {
      this.tab.style.marginRight = "300px"
    }

    this.state = true;
    this.icon.src = "/static/images/icons/chevron_left.svg";
  }

  closeTab() {
    this.tab.style.transform = "translateX(0)";
    this.state = false;
    this.checkScreenSize();
    this.icon.src = "/static/images/icons/chevron_right.svg";

  }

  // Adjust margin if sidebar deployed and screen between 800 and 1000px
  updateTimelineMargin() {
    if (window.innerWidth >= 800 && window.innerWidth <= 1000 && this.state == true) {
      this.timeline.style.marginLeft = "-15%";
      this.adjustMonthConnectors()
    } else {
      this.timeline.style.marginLeft = "";
      this.adjustMonthConnectors()
    }
  }

  adjustMonthConnectors() {
    if (window.innerWidth >= 800 && window.innerWidth <= 900 && this.state == true) {
      // Iterate through all month connectors, and alter width
      for (let i = 0; i < this.monthConnectors.length; i++) {
        this.monthConnectors[i].style.minWidth = "15%";
      }
    }
    else {
      // Iterate through all month connectors, and alter width
      for (let i = 0; i < this.monthConnectors.length; i++) {
        this.monthConnectors[i].style.minWidth = "30%";
      }
    }

  }

}


// Function to animate the highlight for scrollTo behavior
function scrollToAnim(targetEvent) {
  console.log(targetEvent)

  // Get the scrollTo target
  var parentElem = document.getElementById(targetEvent);
  // Select the header element for animation
  var headerElem = parentElem.querySelector('.event-header');
  headerElem.style.transition = "0.1s"

  var count = 0;
  var interval = setInterval(function() {
    if (count >= 6) {
      clearInterval(interval); // Stop the flashing after 3 cycles
      headerElem.style.backgroundColor = ""; // Reset the background color
      headerElem.style.transition = "" // Reset transition 
      return;
    }

    // Alternate between two CSS variables
    if (count % 2 === 0) {
      headerElem.style.backgroundColor = "var(--darker_red)";
    } else {
      headerElem.style.backgroundColor = "var(--bright_red)";   
    }

    count++;
  }, 200); // Flashing interval in milliseconds
}


// Create sidebar
const sidebar = new Tab({
  tab: "sidebar-outer",
  button: "sidebar-deploy",
  icon: "sidebar-icon",
  timeline: "timeline-container",
  monthConnectors: "month-connector",
})



