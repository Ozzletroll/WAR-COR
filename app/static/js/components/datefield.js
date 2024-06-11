export class DateField {
  constructor({
    element,
  })
  {
    this.element = element;
    this.element.addEventListener("change", () => {
      var number = this.element.value;
      if (number == 0) {
        number = "1"
      }
      if (number.length < 2 && number != 0) {
        var value = number.padStart(2, "0");
        this.element.value = value;
      }
      var value = number.padStart(2, "0");
      this.element.value = value;
    });
  }
}
