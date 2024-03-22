class Field {
  constructor({
    elementID,
    summernote,
  }) {
    this.element = document.getElementById(elementID);
    this.editMarker = document.getElementById(elementID + "-edit");
    this.summernote = summernote;

    if (this.element.type === "checkbox") {
      this.initialValue = this.element.checked;
    }
    else {
      this.initialValue = this.element.value;
    }
  }

  checkEditStatus() {
    if (this.element.type === "checkbox") {
      if (this.element.checked != this.initialValue) {
        this.editMarker.checked = true;
      }
      else {
        this.editMarker.checked = false;
      }
    }
    if (this.element.value != this.initialValue) {
      this.editMarker.checked = true;
    }
    else {
      this.editMarker.checked = false;
    }
  }
}


export class Form {
  constructor({
      form,
      fields
    }) {
    this.form = document.getElementById(form);
    this.fields = [];

    fields.forEach(field => {
      var isSummernote = field == "summernote";
      var element = new Field({
        elementID: field,
        summernote: isSummernote,
      })
      this.fields.push(element);
    });
    
    this.form.addEventListener("submit", this.checkFields.bind(this));
  }

  checkFields(event) {
    this.fields.forEach(field => {
      field.checkEditStatus();
    })
  }

}
