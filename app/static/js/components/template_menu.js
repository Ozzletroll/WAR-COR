export class TemplateMenu{
  constructor({
    element,
    button
  }) {
    this.element = element;
    this.button = button;
    this.state = false;

    this.toggleMenu = this.toggleMenu.bind(this);
    this.button.addEventListener("click", this.toggleMenu);

  }

  toggleMenu() {
    if (this.state == false) {
      this.element.style.height = "500px";
    }
    else {
      this.element.style.height = "0px";
    }
    this.state = !this.state;
  }
}
