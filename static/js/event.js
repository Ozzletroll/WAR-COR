// Modal class
class Modal {
  constructor({
    modal,
    button,
    span,
  }) {
    this.modal = modal;
    this.button = button;
    this.span = span;

    this.button.onclick = event => {
      this.openModal(event)
    } 

    this.span.onclick = event => {
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

// Create array to hold dropdown objects
const modalItems = []

// Select all dropdown elements
var modals = document.querySelectorAll('[id^="modal-"]');
var buttons = document.querySelectorAll('[id^="button-"]');
var spans = document.querySelectorAll('[id^="close-"]');

// Iterate through both arrays, creating dropdown objects
buttons.forEach((button, index) => {

  var modal = new Modal({
    modal: modals[index],
    button: button,
    span: spans[index],
  })

  // Append object to array
  modalItems.push(modal)
});
