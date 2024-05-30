import { TemplateModal } from "../components/modal.js";


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
    this.templateDeleteModalElement = document.getElementById("template-modal-1");
    this.modalConfirmButton = document.getElementById("template-modal-confirm");
    this.templateModal;

    // Reference to modal delete function, so that it can be unbound from modal
    // button after use.
    this.modalDeleteFunction;

    this.saveFlash = this.element.querySelector("#save-templates-flash");
    this.importFlash = this.element.querySelector("#import-templates-flash");
  
    this.importButton = this.element.querySelector("#share-code-submit");
    this.saveButton = this.element.querySelector("#save-template-button");

    this.toggleMenu = this.toggleMenu.bind(this);
    this.toggleButton.addEventListener("click", this.toggleMenu);

    this.saveTemplate = this.saveTemplate.bind(this);
    this.saveButton.addEventListener("click", this.saveTemplate);

    this.importTemplate = this.importTemplate.bind(this);
    this.importButton.addEventListener("click", this.importTemplate);

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

  bindCopyButtons() {
    var copyButtons = this.element.querySelectorAll(".template-copy");
    copyButtons.forEach(button => {
      button.addEventListener("click", function() {
        var shareCode = button.dataset.code;

        navigator.clipboard.writeText(shareCode).then(function() {
          var label = button.querySelector(".template-button-tooltip");
          label.innerText = "COPIED";
          setTimeout(() => {
            label.innerText = "COPY SHARE CODE";
          }, 1500);
        }, function(error) {
          console.error("Could not copy text: ", error);
        }); 
      });
    });
  }

  bindDeleteButtons() {
    var deleteButtons = this.element.querySelectorAll(".template-delete");

    deleteButtons.forEach(button => {
      button.addEventListener("click", () => {

        var templateName = button.dataset.name;
        var templateID = button.dataset.templateid;
        
        this.templateModal = new TemplateModal({
          modal: document.getElementById("template-modal-1"),
          span: document.getElementById("template-close-1"),
          text: templateName,
        })

        // Unbind any existing listener on modal confirm button
        this.modalConfirmButton.removeEventListener("click", this.modalDeleteFunction)

        // Update reference to delete function, so that it can be unbound after calling
        this.modalDeleteFunction = () => {
          this.deleteTemplate(templateID);
        };
        this.modalConfirmButton.addEventListener("click", this.modalDeleteFunction);
      });
    });
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
      this.bindCopyButtons();
      this.bindDeleteButtons();
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

  importTemplate() {
    var url = this.element.querySelector("#import-template-url").value;
    var shareCode = this.element.querySelector("#share-code-input").value;

    if (!shareCode) {
      this.flashMessage(this.importFlash, "ENTER SHARE CODE");
      return;
    }
    
    var data = {
      "share_code": shareCode,
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
    .then((response) => {
      if (response.status === 200) {
        response.json().then((data) => {
          var message = data.message;
          this.element.querySelector("#share-code-input").value = "";
          this.flashMessage(this.importFlash, message);
          this.getTemplates();
        });
      } else {
        console.error("Error:", response.statusText);
      }
    })
    .catch((error) => {
      console.error("Fetch error:", error);
    });
  }

  deleteTemplate(templateID) {
    this.modalConfirmButton.removeEventListener("click", this.modalDeleteFunction)

    var url = this.modalConfirmButton.dataset.url;
    var data = {
      "template_id": templateID,
    };

    fetch(url, {
      method: "DELETE",
      redirect: "follow",
      headers: {
        "Content-Type": "application/json",
        "X-CSRF-TOKEN": this.csrfToken,
      },
      body: JSON.stringify(data),
    })
    .then((response)=>{ 
      if (response.status == 200) {
        this.templateModal.closeModal();
        this.getTemplates();
      }
    }).catch((error) => console.warn(error));
  }

  flashMessage(element, message) {
    element.innerText = message;
    setTimeout(() => {
      element.innerText = "";
    }, 1500);
  }
}
