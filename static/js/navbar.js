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
    this.tab.style.borderTop = "1px solid var(--elem_border)"
    this.state = true
  }

  closeTab() {
    this.tab.style.marginBottom = "0"
    this.tab.style.height = "0"
    this.tab.style.borderBottom = "0px solid var(--elem_border)"
    this.tab.style.borderTop = "0px solid var(--elem_border)"

    this.state = false
  }

}

// Create sidebar
const messages_tab = new messageTab({
  tab: "messages-tab",
  button: "messages-button",
})


// Continously check screen size
function handleResize() {
  let newHeight = window.innerHeight;
  let newWidth = window.innerWidth;
  var menu = document.getElementById("hamburgerMenu");

  // Hide hamburger menu if screen has been resized beyond 700px
  if (newWidth >= 700) {
    menu.style.display = "none"
  }

}

window.addEventListener("resize", handleResize);

// calling the resize function for the first time
handleResize();

// Display the hamburger menu on click
function hamburgerClick() {
  var menu = document.getElementById("hamburgerMenu");
  if (menu.style.display === "flex") {
    menu.style.display = "none";
  } else {
    menu.style.display = "flex";
  }
}
