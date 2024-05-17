// Modal class
export class Modal {
    constructor({
      modal,
      button,
      span,
    }) {
      this.modal = modal;
      this.button = button;
      this.span = span;
      this.innerElement = this.modal.querySelector(".modal-content");
      this.hiddenElements = document.querySelectorAll(".scrollpage, .ui-buttons");
      this.lastClicked = null;
   
      this.button.onclick = event => {
        this.lastClicked = event.detail.originButton || this.button;
        this.openModal();
      } 
  
      this.span.onclick = event => {
        this.closeModal();
      }
      
      this.modal.addEventListener("click", event => {
        if (event.target == this.modal) {
          this.closeModal();
        }
      });
  
    }
    
    openModal() {
      this.modal.style.display = "flex";
      this.innerElement.setAttribute("aria-modal", "true")
      Array.from(this.hiddenElements).forEach(element => {
        element.inert = true;
      })
      this.span.focus();
    }
  
    closeModal() {
      this.modal.style.display = "none";
      this.innerElement.setAttribute("aria-modal", "false")
      Array.from(this.hiddenElements).forEach(element => {
        element.inert = false;
      })
      this.lastClicked.focus();
    }
  
  }
  

  // Preview Area Modal class
export class PreviewModal extends Modal{
  constructor({
    modal,
    button,
    span,
    editor,
  }) {
    super({ modal, button, span });
    this.editor = editor.querySelector(".note-editable");

    this.button.onclick = event => {
      this.openModal(event)
      this.htmlPreview()
    } 

    this.span.onclick = event => {
      this.closeModal(event)
    } 

  }
  
  htmlPreview() {

    // Get the content of the Summernote editor and add it to the modal
    var content = this.editor.innerHTML;
    var modalBody = this.modal.querySelector(".modal-body-preview");
    modalBody.innerHTML = content;

    var labelContainer = this.button.closest(".dynamic-form-label-container");
    if (labelContainer != null) {
      var fieldTitle = labelContainer.querySelector(".dynamic-field-title").value;
      var modalTitle = this.modal.querySelector(".dynamic-preview-header");
      modalTitle.innerText = fieldTitle;
    }

    this.formatImages();
  }

  formatImages() {
    // Apply styling to user submitted image links
    const elements = document.querySelectorAll(".modal-body-preview p");
    let imageCount = 0;

    elements.forEach((element) => {
      if (element.querySelector("img")) {
        imageCount++;

        // Create surrounding element
        const newDiv1 = document.createElement("div");
        newDiv1.classList.add("user-image-area");

        // Wrap the element within the new div
        element.parentNode.insertBefore(newDiv1, element);
        newDiv1.appendChild(element);

        // Create surrounding element
        const newDiv2 = document.createElement("div");
        newDiv2.classList.add("user-image-elem");

        // Wrap the element within the new div
        element.parentNode.insertBefore(newDiv2, element);
        newDiv2.appendChild(element);

        // Create header
        const newHeader = document.createElement("div");
        newHeader.classList.add("user-image-header");
        newHeader.textContent = `Image::Data_${String(imageCount).padStart(2, "0")}`;

        // Insert the header
        element.parentNode.insertBefore(newHeader, element);

        // Centre img elements in user submitted p elements
        element.style.display = "flex";
        element.style.width = "auto";
        element.style.justifyContent = "center";
        element.style.margin = "0";

      }});

  }

}