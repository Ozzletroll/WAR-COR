class hamburgerMenu {
  constructor({
    button,
    menu,
  }) {
    this.button = document.getElementById(button);
    this.menu = document.getElementById(menu);
    this.state = false;
    this.button.addEventListener("click", this.toggleMenu.bind(this));
    window.addEventListener("resize", this.handleResize.bind(this));
    this.menuItems = this.menu.querySelectorAll(".h-menu-item");
    this.handleResize();
  }

  toggleMenu () {

    if (this.state == false) {
      this.menu.style.transform = "translateY(0)";
      this.menu.setAttribute("aria-hidden", "false");
      this.button.setAttribute("aria-label", "Close Hamburger Menu");
      Array.from(this.menuItems).forEach(element => {
        element.setAttribute("tabIndex", "0");
      })
      this.state = true;
    } 
    else {
      this.menu.style.transform = "";
      this.menu.setAttribute("aria-hidden", "true");
      this.button.setAttribute("aria-label", "Open Hamburger Menu");
      Array.from(this.menuItems).forEach(element => {
        element.setAttribute("tabIndex", "-1");
      })
      this.state = false;
    }
  }

  handleResize() {
    // Hide hamburger menu if screen has been resized beyond 700px
    var newWidth = window.innerWidth;
    if (newWidth > 700) {
      this.menu.style.display = "none";
    }
    else {
      this.menu.style.display = "flex";
    }
  }

}

const hamburger = new hamburgerMenu({
  button: "hamburger-button",
  menu: "hamburger-menu",
})
