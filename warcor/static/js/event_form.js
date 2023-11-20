// Modal class
class Modal {
  constructor({
    modal,
    button,
    span,
  }) {
    this.modal = document.getElementById(modal);
    this.button = button;
    this.span = span;

    document.getElementById(this.button).onclick = event => {
      this.openModal(event)
    } 

    document.getElementById(this.span).onclick = event => {
      this.closeModal(event)
    } 

  }
  
  openModal() {
    this.modal.style.display = "flex";
  }

  closeModal() {
    this.modal.style.display = "none";
  }

}



// Preview Area Modal class
class PreviewModal {
  constructor({
    modal,
    button,
    span,
  }) {
    this.modal = document.getElementById(modal);
    this.button = button;
    this.span = span;

    document.getElementById(this.button).onclick = event => {
      this.openModal(event)
    } 

    document.getElementById(this.span).onclick = event => {
      this.closeModal(event)
    } 

  }
  
  openModal() {
    this.modal.style.display = "flex";
    this.htmlPreview()
  }

  closeModal() {
    this.modal.style.display = "none";
  }

  htmlPreview() {

    // Get the content of the Summernote
    var editor = document.querySelector('.note-editable');
    var content = editor.innerHTML;

    // Get the preview modal text area and add html
    var modalBody = document.getElementById("preview-modal-body");
    modalBody.innerHTML = content;
   
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



// Create modals
const modal_1 = new Modal({
  modal: "modal-1",
  button: "event-date-help-button",
  span: "close-1",
})

const modal_2 = new Modal({
  modal: "modal-2",
  button: "event-belligerents-help-button",
  span: "close-2",
})

const modal_3 = new Modal({
  modal: "modal-3",
  button: "event-format-help-button",
  span: "close-3",
})

// HTML Preview Area Modal
const modal_preview = new PreviewModal({
  modal: "modal-preview",
  button: "html-preview-button",
  span: "close-preview",
})

// Check if page has delete button
const deleteButton = document.getElementById("modal-delete");
let modal_delete;
if (deleteButton != null) {
  // If delete button is present, creating modal instance
  modal_delete = new Modal({
    modal: "modal-delete",
    button: "button-delete",
    span: "close-delete",
  })
}

// Close modals if the user clicks anywhere else
window.onclick = function(event) {
  if (event.target == modal_1.modal) {
    modal_1.closeModal();
  }
  if (event.target == modal_2.modal) {
    modal_2.closeModal();
  }
  if (event.target == modal_3.modal) {
    modal_3.closeModal();
  }
  if (event.target == modal_preview.modal) {
    modal_preview.closeModal();
  }
  if (deleteButton != null) {
    if (event.target == modal_delete.modal) {
      modal_delete.closeModal();
    }
  }
}


// Check and disable "hide_time" option if "block_header" is selected

// Get references to the header and hide_time form fields
const headerField = document.getElementById("header-input");
const hideTimeField = document.getElementById("hide-time-input");

// Initialise checkbox values
if (headerField.checked) {
  hideTimeField.checked = true;
  hideTimeField.disabled = true;
  hideTimeField.style.opacity = "30%";
}
else {
  hideTimeField.disabled = false;
  hideTimeField.style.opacity = "";
}

// Listen for the change event on the header field
headerField.addEventListener('change', function() {
// Check if the header field is checked
if (headerField.checked) {
// Check and disable the hide_time field
hideTimeField.checked = true;
hideTimeField.disabled = true;
hideTimeField.style.opacity = "30%";
} 
else {
// If the header field is unchecked, enable the hide_time field
hideTimeField.checked = false;
hideTimeField.disabled = false;
hideTimeField.style.opacity = "";
}
});
