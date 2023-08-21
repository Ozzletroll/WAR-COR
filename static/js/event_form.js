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

// Create modals
const modal_1 = new Modal({
  modal: "modal-1",
  button: "event-date-help-button",
  span: "close-1",
})

// Create modals
const modal_2 = new Modal({
  modal: "modal-2",
  button: "event-belligerents-help-button",
  span: "close-2",
})

// Create modals
const modal_3 = new Modal({
  modal: "modal-3",
  button: "event-format-help-button",
  span: "close-3",
})


function htmlPreview() {
  console.log("Preview")

}