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
    this.templatesButton = templatesButton;
    this.menuState = false;
    this.templateMenu = templateMenu;
    this.tooltips = this.bindTooltips();

    this.formSubmit = this.formSubmit.bind(this);
    this.updateButton.addEventListener("click", this.formSubmit);

    this.toggleTemplatesMenu = this.toggleTemplatesMenu.bind(this);
    this.templatesButton.addEventListener("click", this.toggleTemplatesMenu);

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

  toggleTemplatesMenu() {
    if (this.menuState == false) {
      this.templateMenu.style.height = "500px";
    }
    else {
      this.templateMenu.style.height = "0px";
    }
    this.menuState = !this.menuState;
  }

  bindTooltips() {
    var buttons = document.getElementsByClassName("form-footer-button");
    var tooltips = [];
    Array.from(buttons).forEach(button => {
      var newTooltip = new Tooltip({
        parentButton: button,
        tooltip: document.getElementById(button.getAttribute("aria-describedby"))
      })
      tooltips.push(newTooltip);
    })

    return tooltips;
  }
}


export class TimelineFooter {
  constructor() {
    this.tooltips = this.bindTooltips();
  }

  bindTooltips() {
    var buttons = document.getElementsByClassName("form-footer-button");
    var tooltips = [];
    Array.from(buttons).forEach(button => {
      var newTooltip = new Tooltip({
        parentButton: button,
        tooltip: document.getElementById(button.getAttribute("aria-describedby"))
      })
      tooltips.push(newTooltip);
    })

    return tooltips;
  }
}


class Tooltip{
  constructor({
    parentButton,
    tooltip,
  }) {
    this.parentButton = parentButton;
    this.tooltip = tooltip;


    // Mouse events
    this.parentButton.addEventListener("mouseover", this.openTooltip.bind(this))
    this.parentButton.addEventListener("mouseout", this.closeTooltip.bind(this))
    // Keyboard events
    this.parentButton.addEventListener("focus", function(event) {
      if (event.target.matches(":focus-visible")) {
        this.openTooltip();
      }
    }.bind(this));
    this.parentButton.addEventListener("blur", this.closeTooltip.bind(this))
  }

  openTooltip() {
    this.tooltip.style.display = "flex";
  }

  closeTooltip() {
    this.tooltip.style.display = "none";
  }
}
