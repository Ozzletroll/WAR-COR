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

    // Get the content of the CKEditor field
    var editor = CKEDITOR.instances['form-contents'];
    var content = editor.getData();
  
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



// Create modals HTML Preview Area Modal
const modal_preview = new PreviewModal({
  modal: "modal-preview",
  button: "html-preview-button",
  span: "close-preview",
})


// Close modals if the user clicks anywhere else
window.onclick = function(event) {

  if (event.target == modal_preview.modal) {
    modal_preview.closeModal();
  }

}


// Get the date suffix input field and the element to update
var inputField = document.getElementById("suffix-input");
var exampleDate = document.getElementById("example-date");

// Store the initial suffix text
var suffixText = exampleDate.textContent;

// Add event listener to the input field
inputField.addEventListener("input", function() {
  // Get the input value
  var inputValue = inputField.value;

  // If the input value is shorter than the stored suffix text,
  // remove the last character from the suffix text
  if (inputValue.length < suffixText.length) {
    suffixText = suffixText.slice(0, -1);
  }

  // Add the input value as a suffix to the element's text
  exampleDate.textContent = suffixText + inputValue;
});
