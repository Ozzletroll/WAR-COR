export class DateField {
  constructor({
    element,
    allowZero,
  })
  {
    this.element = element;
    this.allowZero = allowZero;
    this.element.addEventListener("change", () => {
      var number = this.element.value;
      if (number == 0 &! this.allowZero) {
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
