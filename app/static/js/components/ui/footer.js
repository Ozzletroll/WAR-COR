import { TemplateMenu } from "./template_menu.js";
import { Tooltip } from "./tooltip.js";


export class FormFooter {
  constructor({
    formSubmitButton,
    formDeleteButton,
    updateButton,
    deleteButton,
    templatesButton,
    templateMenu
  }) {
    this.formSubmitButton = formSubmitButton;
    this.formDeleteButton = formDeleteButton;
    this.updateButton = updateButton;
    this.deleteButton = deleteButton;
    this.templateMenu = new TemplateMenu({
      element: templateMenu,
      button: templatesButton,
    });
    this.tooltips = this.bindTooltips();

    this.formSubmit = this.formSubmit.bind(this);
    this.updateButton.addEventListener("click", this.formSubmit);

    if (this.formDeleteButton != null) {
      this.formDelete = this.formDelete.bind(this);
      this.deleteButton.addEventListener("click", this.formDelete);
    }
  }

  formSubmit() {
    this.formSubmitButton.click();
  }

  formDelete() {
    var event = new CustomEvent(
      "click", 
      { 
        bubbles: true, 
        detail: { originButton: this.deleteButton } 
      }
    );
    this.formDeleteButton.dispatchEvent(event);
  }

  bindTooltips() {
    var buttons = document.getElementsByClassName("form-footer-button");
    var tooltips = [];
    Array.from(buttons).forEach(button => {
      var newTooltip = new Tooltip({
        parentButton: button,
        tooltip: document.getElementById(button.getAttribute("aria-describedby")),
        mode: "flex"
      })
      tooltips.push(newTooltip);
    })

    return tooltips;
  }
}


export class TimelineFooter {
  constructor({
    newButton,
    menu
  }) {
    this.newButton = newButton;
    this.menu = menu;
    this.buttons = this.menu.querySelectorAll(".footer-new-button");
    this.tooltips = this.bindTooltips();
    this.state = false;

    this.newButton.addEventListener("click", () => {
      this.toggleNewMenu();
      this.buttons[0].focus();
    });
  }

  toggleNewMenu() {
    var focusableElements = this.menu.querySelectorAll("a");

    if (this.state == false) {
      this.menu.style.height = "70px";
      focusableElements.forEach(element => {
        element.setAttribute("tabindex", "0");
      })
    }
    else {
      this.menu.style.height = "0px";
      focusableElements.forEach(element => {
        element.setAttribute("tabindex", "-1");
      })
    }
    this.state = !this.state;
  }

  bindTooltips() {
    var buttons = document.getElementsByClassName("form-footer-button");
    var tooltips = [];
    Array.from(buttons).forEach(button => {
      var newTooltip = new Tooltip({
        parentButton: button,
        tooltip: document.getElementById(button.getAttribute("aria-describedby")),
        mode: "flex"
      })
      tooltips.push(newTooltip);
    })

    return tooltips;
  }
}
