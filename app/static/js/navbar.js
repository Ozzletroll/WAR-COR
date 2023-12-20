
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
    this.handleResize();
  }

  toggleMenu () {

    if (this.state == false) {
      this.menu.style.transform = "translateY(0)";
      this.state = true;
    } 
    else {
      this.menu.style.transform = "";
      this.state = false;
    }
  }

  handleResize() {

    // Hide hamburger menu if screen has been resized beyond 700px
    var newWidth = window.innerWidth;
    if (newWidth >= 700) {
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
