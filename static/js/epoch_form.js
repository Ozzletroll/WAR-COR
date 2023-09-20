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


// // Create modals
// const modal_1 = new Modal({
//   modal: "modal-1",
//   button: "event-date-help-button",
//   span: "close-1",
// })

// const modal_2 = new Modal({
//   modal: "modal-2",
//   button: "event-belligerents-help-button",
//   span: "close-2",
// })


const modal_delete = new Modal({
  modal: "modal-delete",
  button: "button-delete",
  span: "close-delete",
})

// Close modals if the user clicks anywhere else
window.onclick = function(event) {
  // if (event.target == modal_1.modal) {
  //   modal_1.closeModal();
  // }
  // if (event.target == modal_2.modal) {
  //   modal_2.closeModal();
  // }
  if (event.target == modal_delete.modal) {
    modal_delete.closeModal();
  }

}
