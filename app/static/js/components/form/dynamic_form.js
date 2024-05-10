import { createFieldHTML } from "./dynamic_field_templates/html_field_template.js";
import { summernoteInitialise } from "../summernote_initialise.js";
import { Modal, PreviewModal } from "../modal.js";


export class DynamicForm {
    constructor({
      button,
    }) {
      this.button = button;
      this.fieldList;
      this.formArea = document.getElementById("dynamic-field-area");
      this.fields = this.getDynamicFields();
      // this.modals = this.getModals();

      this.updateDraggableItems(this.formArea);
      this.bindCloseModalEvents();

      // Bind "this" to the instance for the addNewField method
      this.addNewField = this.addNewField.bind(this);
      this.button.addEventListener("click", this.addNewField);
    }
  
    getDynamicFields() {
      var fields = [];
      var dynamicFields = document.getElementsByClassName("dynamic-field");
      Array.from(dynamicFields).forEach((element, index) => {
        var newField = new DynamicField({
          type: "html",
          element: element,
          index: index + 1,
        })
        fields.push(newField);
    })
      return fields;
    }

    addNewField() {

      // Create page elements and insert in DOM
      var dynamicFieldCount = document.getElementsByClassName("dynamic-field").length + 1;
      this.formArea.insertAdjacentHTML("beforeend", createFieldHTML(dynamicFieldCount));
      
      // Insert modals into DOM
      // close modal
      // htmlPreviewModal
    
      // Initialise new summernote editor
      var id = `-dynamic-${dynamicFieldCount}`;
      summernoteInitialise(
        id,
        "OPTIONAL",
        null,
        true,
        true
      );

      // Add event listeners to all summernote modals
      this.bindCloseModalEvents();
  
      // Create instance of Field class
      var newField = new DynamicField({
        type: "html",
        element: document.getElementById(`event-dynamic-field-${dynamicFieldCount}`),
        index: dynamicFieldCount,
      })
      this.fields.push(newField);

      // Destroy the existing SortableJS instance to prevent iOS devices breaking
      this.fieldList.destroy();

      // Re-initialize SortableJS
      this.updateDraggableItems(this.formArea);
    }

    updateDraggableItems(formArea) {
      this.fieldList = new Sortable(formArea, {
        handle: ".handle",
        animation: 150,
        onEnd: function(event) {
          var items = event.from.getElementsByClassName("dynamic-field");
          for (var index = 0; index < items.length; index++) {
            var inputs = items[index].getElementsByTagName("input");
            for (var index2 = 0; index2 < inputs.length; index2++) {
              inputs[index2].name = inputs[index2].name.replace(/dynamic_fields-\d+-/, "dynamic_fields-" + index + "-");
            }
            var textAreas = items[index].getElementsByTagName("textarea");
            for (var index3 = 0; index3 < textAreas.length; index3++) {
              textAreas[index3].name = textAreas[index3].name.replace(/dynamic_fields-\d+-/, "dynamic_fields-" + index + "-");
            }
          }
        }
      });
    }

    bindCloseModalEvents() {
      var summernoteModals = document.getElementsByClassName("note-modal");
      Array.from(summernoteModals).forEach(modal => {
          var modalCloseButton = modal.querySelector(".close");
          modal.addEventListener("click", (event) => {
              if (event.target.classList.contains("note-modal")) {
                modalCloseButton.click();
              }
          });
      });
    }

  }


class DynamicField {
  constructor({
    type,
    element,
    index
  }) {
    this.type = type;
    this.element = element;
    this.index = index;
    this.previewButton;
    this.closeButton;

    // this.closeModal = new Modal({
    //   modal: "",
    //   button: "",
    //   span: "",
    // })
  }

  close () {

  }

}
