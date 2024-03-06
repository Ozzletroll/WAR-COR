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
   
      this.button.onclick = event => {
        this.openModal(event)
      } 
  
      this.span.onclick = event => {
        this.closeModal(event)
      } 
  
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
      this.button.focus();
    }
  
  }
  