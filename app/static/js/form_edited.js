class Field {
  constructor({
    elementID,
    summernote,
  }) {
    this.element = document.getElementById(elementID);
    this.editMarker = document.getElementById(elementID + "-edit");
    this.summernote = summernote;
    this.initialValue = this.element.value;
  }

  checkEditStatus() {
    if (this.element.value != this.initialValue) {
      this.editMarker.checked = true;
    }
    else {
      this.editMarker.checked = false;
    }
  }

}


class Form {
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

const editEventForm = new Form({
  form: "edit-event-form",
  fields: [
    "event-form-title",
    "event-form-type",
    "event-form-date",
    "event-form-location",
    "event-form-belligerents",
    "summernote",
    "event-form-result"]
})
