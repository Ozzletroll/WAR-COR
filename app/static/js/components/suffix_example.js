export class SuffixExample {
  constructor({
    suffixField,
    suffixExample,
  }) {
    this.suffixField = suffixField;
    this.suffixExample = suffixExample;

    this.updateSuffix();
    this.suffixField.addEventListener("input", this.updateSuffix.bind(this));
    this.suffixField.addEventListener("keydown", this.updateSuffix.bind(this));
  }

  updateSuffix() {
    this.suffixExample.innerText = this.suffixField.value;
  }
}
