export class CharCount {
  constructor({charField, charCount, summernote=false}) {
    this.charField = charField;
    this.charCount = charCount;
    this.charLimit = parseInt(this.charCount.innerText);
    this.summernote = summernote;

    this.updateCharCount();
    this.charField.addEventListener("input", this.updateCharCount.bind(this));
    $(document).on('summernoteFieldChanged', this.updateCharCount.bind(this)); 
  }

  updateCharCount() {
    if (this.summernote) {
      var currentChars = this.charField.textContent.length;
    }
    else {
      var currentChars = this.charField.value.length;
    }

    var remainingChars = this.charLimit - currentChars;
    this.charCount.innerText = remainingChars;
  }
}
