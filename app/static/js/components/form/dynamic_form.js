import { createFieldHTML } from "./html_field_template.js";
import { summernoteInitialise } from "../../components/summernote_initialise.js";



export class DynamicForm {
    constructor({
      button,
    }) {
      this.button = button;
      this.fieldList;
      this.formArea = document.getElementById("dynamic-field-area");
      this.fields = this.getDynamicFields();
      this.updateDraggableItems(this.formArea);

      // Bind "this" to the instance for the addNewField method
      this.addNewField = this.addNewField.bind(this);
      this.button.addEventListener("click", this.addNewField);
    }
  
    getDynamicFields() {
      var fields = [];
      var dynamicFields = document.getElementsByClassName("dynamic-field");
      Array.from(dynamicFields).forEach(element => {
        var newField = new DynamicField({
          type: "html",
          element: element,
        })
        fields.push(newField);
      })
      return fields;
    }

    addNewField() {

      // Create page elements and insert in DOM
      var newDiv = document.createElement("div");
      var dynamicFieldCount = document.getElementsByClassName("dynamic-field").length + 1;
      newDiv.innerHTML = createFieldHTML(dynamicFieldCount);
      this.formArea.appendChild(newDiv);
    
      // Initialise new summernote editor
      var id = `-dynamic-${dynamicFieldCount}`;
      summernoteInitialise(
        id,
        "OPTIONAL",
        null,
        false,
        false
      );

      var newField = new DynamicField({
        type: "html",
        element: newDiv,
      })

      this.fields.push(newField);

      // Destroy the existing SortableJS instance to prevent iOS devices breaking
      this.fieldList.destroy();

      // Re-initialize SortableJS
      this.updateDraggableItems(this.formArea);

      console.log(this.fields)
    }

    removeField() {
  
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


  }


class DynamicField {
  constructor({
    type,
    element,
  }) {
    this.type = type;
    this.element = element;
    this.previewButton;
    this.closeButton;
  }


}
