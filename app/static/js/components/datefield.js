export class DateField {
  constructor({
    element,
  })
  {
    this.element = element;
    this.element.addEventListener("input", () => {
      var number = this.element.value;
      this.element.value = number.slice(0, 2);
      if (number.length < 2 && number != 0) {
        var value = number.padStart(2, "0");
        this.element.value = value;
      }
    });
    this.element.addEventListener("change", () => {
      var number = this.element.value;
      if (number == 0) {
        number = "1"
      }
      var value = number.padStart(2, "0");
      this.element.value = value;
    });
  }
}
