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
var suffixField = document.getElementById("suffix-input");
var negativeSuffixField = document.getElementById("negative-suffix-input");

var exampleSuffixDate = document.getElementById("example-date");
var exampleNegativeSuffixDate = document.getElementById("negative-example-date");

// Store the initial suffix text
var suffixText = exampleSuffixDate.textContent;
var negativeSuffixText = exampleNegativeSuffixDate.textContent;

// Function to update suffix example
function updateSuffix(suffixField, exampleSuffixDate) {

  var inputValue = suffixField.value;

  // If the input value is shorter than the stored suffix text,
  // remove the last character from the suffix text
  if (inputValue.length < suffixText.length) {
    suffixText = suffixText.slice(0, -1);
  }

  // Add the input value as a suffix to the element's text
  exampleSuffixDate.textContent = suffixText + inputValue;
}

// Call updateSuffix once when the page loads to display the initial values
updateSuffix(suffixField, exampleSuffixDate);
updateSuffix(negativeSuffixField, exampleNegativeSuffixDate);

// Add event listener to the input field
suffixField.addEventListener("input", function() {
  updateSuffix(suffixField, exampleSuffixDate);
});

negativeSuffixField.addEventListener("input", function() {
  updateSuffix(negativeSuffixField, exampleNegativeSuffixDate);
});
