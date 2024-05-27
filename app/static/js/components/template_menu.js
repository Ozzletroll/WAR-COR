export class TemplateMenu{
  constructor({
    element,
    button,
  }) {
    this.element = element;
    this.toggleButton = button;
    this.state = false;

    this.importButton = this.element.querySelector("#import-template-button");
    this.saveButton = this.element.querySelector("#save-template-button");

    this.toggleMenu = this.toggleMenu.bind(this);
    this.toggleButton.addEventListener("click", this.toggleMenu);

    this.saveTemplate = this.saveTemplate.bind(this);
    this.saveButton.addEventListener("click", this.saveTemplate);

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

  saveTemplate() {
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

    var csrfToken = this.element.querySelector("#save-template-csrf").value;
    var url = this.element.querySelector("#save-template-url").value;
    var title = this.element.querySelector("#save-template-title").value;

    var data = {
      "template_name": title,
      "format": formStructure,
    }
    
    fetch(url, {
      method: "POST",
      redirect: "follow",
      headers: {
        "Content-Type": "application/json",
        "X-CSRF-TOKEN": csrfToken,
      },
      body: JSON.stringify(data),
    })
    .then((response)=>{ 
      console.log(response)
    })
  };
}
