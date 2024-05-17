export class FormFooter {
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

    this.formDelete = this.formDelete.bind(this);
    this.deleteButton.addEventListener("click", this.formDelete);
  }

  formSubmit() {
    this.formSubmitButton.click();
  }

  formDelete() {
    this.formDeleteButton.click();
  }
}
