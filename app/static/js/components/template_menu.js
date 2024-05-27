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
          "field_title": field.querySelector(".campaign-form-label-title").value,
          "field_width": field.querySelector(".field-size-toggle").checked,
        })
      }
      else if (field.classList.contains("belligerents-field")) {
        formStructure.push({
          "field_type": "composite",
          "field_title": field.querySelector(".campaign-form-label-title").value,
          "field_width": null,
        })
      }
      else if (field.classList.contains("html-field")) {
        formStructure.push({
          "field_type": "html",
          "field_title": field.querySelector(".campaign-form-label-title").value,
          "field_width": null,
        })
      }
    })

    var csrfToken = this.element.querySelector("#save-template-csrf").value;
    var url = this.element.querySelector("#save-template-url").value;
    
    fetch(url, {
      method: "POST",
      redirect: "follow",
      headers: {
        "Content-Type": "application/json",
        "X-CSRF-TOKEN": csrfToken,
      },
      body: JSON.stringify(formStructure),
    })
    .then((response)=>{ 
      console.log(response)
    })
  };
}
