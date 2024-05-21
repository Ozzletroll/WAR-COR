export class Footer {
  constructor({
    formSubmitButton,
    formDeleteButton,
    updateButton,
    deleteButton,
  }) {
    this.formSubmitButton = formSubmitButton;
    this.formDeleteButton = formDeleteButton;
    this.updateButton = updateButton;
    this.deleteButton = deleteButton;

    this.formSubmit = this.formSubmit.bind(this);
    this.updateButton.addEventListener("click", this.formSubmit);

    if (this.formDeleteButton != null) {
      this.formDelete = this.formDelete.bind(this);
      this.deleteButton.addEventListener("click", this.formDelete);
    }
  }

  formSubmit() {
    this.formSubmitButton.click();
  }

  formDelete() {
    var event = new CustomEvent(
      "click", 
      { 
        bubbles: true, 
        detail: { originButton: this.deleteButton } 
      }
    );
    this.formDeleteButton.dispatchEvent(event);
  }
}
