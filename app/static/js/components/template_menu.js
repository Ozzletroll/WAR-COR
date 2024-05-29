export class TemplateMenu{
  constructor({
    element,
    button,
  }) {
    this.element = element;
    this.toggleButton = button;
    this.state = false;
    this.csrfToken = this.element.querySelector("#csrf-token").value;
    this.templatesListTab = this.element.querySelector("#template-tab-1");
    this.saveFlash = this.element.querySelector("#save-templates-flash");
  
    this.importButton = this.element.querySelector("#import-template-button");
    this.saveButton = this.element.querySelector("#save-template-button");

    this.toggleMenu = this.toggleMenu.bind(this);
    this.toggleButton.addEventListener("click", this.toggleMenu);

    this.saveTemplate = this.saveTemplate.bind(this);
    this.saveButton.addEventListener("click", this.saveTemplate);

    this.bindTabs();
    this.getTemplates();
  }

  bindTabs() {
    var tabButtons = this.element.querySelectorAll(".templates-tab-button");
    var tabPanels = this.element.querySelectorAll(".templates-tab");

    for (let index = 0; index < tabButtons.length; index++) {
      tabButtons[index].addEventListener("click", function() {

        tabButtons.forEach(tabButton => {
          tabButton.setAttribute("aria-selected", false);
          tabButton.style.borderBottom = "";
          tabButton.style.paddingBottom = "";
        })

        // Deselect all tabs and hide all panels
        tabPanels.forEach(tabPanel => {
          tabPanel.style.display = "none";
        })

        // Select current tab and display panel
        tabPanels[index].style.display = "flex";
        tabButtons[index].style.borderBottom = "none";
        tabButtons[index].style.paddingBottom = "6px";
        tabButtons[index].setAttribute("aria-selected", true)
      })
    }
  }

  toggleMenu() {
    var focusableElements = this.element.querySelectorAll("button, input");

    if (this.state == false) {
      this.element.style.height = "500px";
      this.element.setAttribute("tabindex", "0");
      focusableElements.forEach(element => {
        element.setAttribute("tabindex", "0");
      })
    }
    else {
      this.element.style.height = "0px";
      this.element.setAttribute("tabindex", "-1");
      focusableElements.forEach(element => {
        element.setAttribute("tabindex", "-1");
      })
    }
    this.state = !this.state;
  }

  getTemplates() {
    var url = this.element.querySelector("#get-templates-url").value;

    fetch(url, {
      method: "GET",
      redirect: "follow",
      headers: {
        "X-CSRF-TOKEN": this.csrfToken,
      },
    })
    .then((response) => response.text())
    .then((html) => {
      this.templatesListTab.innerHTML = html;
    })
    .catch((error) => console.warn(error));
  }

  saveTemplate() {
    var url = this.element.querySelector("#save-template-url").value;
    var title = this.element.querySelector("#save-template-title").value;

    if (!title) {
      this.flashMessage(this.saveFlash, "TEMPLATE NAME REQUIRED");
      return;
    }

    var formStructure = [];
    var dynamicFields = document.getElementsByClassName("dynamic-field");
    Array.from(dynamicFields).forEach(field => {
      if (field.classList.contains("basic-field")) {
        formStructure.push({
          "field_type": "basic",
          "is_full_width": field.querySelector(".field-size-toggle").checked,
          "title": field.querySelector(".campaign-form-label-title").value,
        })
      }
      else if (field.classList.contains("belligerents-field")) {
        formStructure.push({
          "field_type": "composite",
          "is_full_width": null,
          "title": field.querySelector(".campaign-form-label-title").value,
        })
      }
      else if (field.classList.contains("html-field")) {
        formStructure.push({
          "field_type": "html",
          "is_full_width": null,
          "title": field.querySelector(".campaign-form-label-title").value,
        })
      }
    })

    var data = {
      "template_name": title,
      "format": formStructure,
    }
    
    fetch(url, {
      method: "POST",
      redirect: "follow",
      headers: {
        "Content-Type": "application/json",
        "X-CSRF-TOKEN": this.csrfToken,
      },
      body: JSON.stringify(data),
    })
    .then((response)=>{ 
      if (response.status == 200) {
        this.element.querySelector("#save-template-title").value = "";
        this.flashMessage(this.saveFlash, "TEMPLATE SAVED");
        this.getTemplates();
      }
      else if (response.status == 400) {
        this.flashMessage(this.saveFlash, "TEMPLATE NAME REQUIRED");
      }
    }).catch((error) => console.warn(error));
  };

  flashMessage(element, message) {
    element.innerText = message;
    setTimeout(() => {
      element.innerText = "";
    }, 1500);
  }
}
