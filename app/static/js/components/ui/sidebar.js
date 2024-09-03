class Sidebar {
  constructor({
    tab,
    button,
    icon
  }) {
    this.tab = document.getElementById(tab);
    this.button = button;
    this.buttonElem = document.getElementById(button);
    this.state = JSON.parse(localStorage.getItem("sidebarState")) || false
    this.icon = document.getElementById(icon);
    this.scrollElem = this.tab.querySelector(".sidebar-scroll");
    this.childButtons = this.tab.querySelectorAll(".sidebar-button");

    this.initialise();
    window.addEventListener("load", this.afterInitiliase.bind(this));
    this.checkScreenSize();
    window.addEventListener("resize", this.checkScreenSize.bind(this));

    // Bind toggle on click event
    this.buttonElem.onclick = event => {
      if (this.state == false) {
        this.openTab(event)
      }
      else if (this.state == true) {
        this.closeTab(event)
      }
    }

    // Call scrollToItem when each button is clicked
    Array.from(this.childButtons).forEach(button => {
      button.addEventListener("click", () => this.scrollToItem(button.dataset.targetElem));
    });
  }

  initialise() {
    if (this.state == true) {
      this.openTab();
    }
  }

  afterInitiliase() {
    // Set transition value after initial load
    this.tab.style.transition = "0.3s";
  }

  checkScreenSize() {
    if (window.innerWidth >= 1400 && this.state == true) {
      this.tab.style.marginRight = "300px";
    }
    else {
      this.tab.style.marginRight = "0px"
    }
  }

  openTab() {
    this.tab.style.transform = "translateX(300px)";
    this.tab.style.filter = "drop-shadow(3px 0px 5px var(--elem_shadow))"
    if (window.innerWidth >= 1400 ) {
      this.tab.style.marginRight = "300px"
    }
    this.scrollElem.setAttribute("aria-hidden", "false");
    this.buttonElem.setAttribute("aria-label", "Close Sidebar");
    if (this.childButtons != null) {
      Array.from(this.childButtons).forEach(button => {
        button.setAttribute("tabindex", "0");
      })
    }
    this.state = true;
    localStorage.setItem("sidebarState", true);
    this.icon.style.transform = "scaleX(-1)";
  }

  closeTab() {
    this.tab.style.transform = "translateX(0)";
    this.tab.style.filter = "";
    this.scrollElem.setAttribute("aria-hidden", "true");
    this.buttonElem.setAttribute("aria-label", "Deploy Sidebar");
    if (this.childButtons != null) {
      Array.from(this.childButtons).forEach(button => {
        button.setAttribute("tabindex", "-1");
      })
    }
    this.state = false;
    localStorage.setItem("sidebarState", false);
    this.checkScreenSize();
    this.icon.style.transform = "scaleX(1)";
  }

  scrollToItem(targetElement) {

    var element = document.getElementById(targetElement);
    element.scrollIntoView();

    // Ignore year, epoch and field button clicks, otherwise proceed with animation
    if (targetElement.startsWith("year") 
        || targetElement.startsWith("epoch") 
        || targetElement.startsWith("field")) {
      return
    }

    var parentElem = document.getElementById(targetElement);
    // Select the header element for animation
    var flashingElem = parentElem.querySelector('.event-header');
    flashingElem.style.transition = "0.1s"

    var count = 0;
    var interval = setInterval(function() {
      if (count >= 6) {
        clearInterval(interval); // Stop the flashing after 3 cycles
        flashingElem.style.backgroundColor = ""; // Reset the background color
        flashingElem.style.transition = ""; // Reset transition 
        return;
      }

      // Alternate between two CSS variables
      if (count % 2 === 0) {
        flashingElem.style.backgroundColor = "var(--darker_red)";
      } else {
        flashingElem.style.backgroundColor = "var(--bright_red)";   
      }

      count++;
    }, 100); // Flashing interval in milliseconds
  }

}


// Create sidebar
const sidebar = new Sidebar({
  tab: "sidebar-outer",
  button: "sidebar-deploy",
  icon: "sidebar-icon"
})
