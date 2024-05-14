// Store a flag indicating if inputs have changed
var fieldDataChanged = false;

// Add event listener to each input field
const fields = [
    // CAMPAIGN FORM
    "#campaign-form-title",
    "#campaign-form-suffix",
    "#campaign-form-negative-suffix",
    // EPOCH FORM
    "#epoch-form-start-date",
    "#epoch-form-end-date",
    "#epoch-form-title",
]
fields.forEach(field => {
    var element = document.querySelector(field);
    if (element) {
        element.addEventListener("change", () => {
            fieldDataChanged = true;
        });
    }
});

// Listen for summernote editor change event
$(document).on('summernoteFieldChanged', function(event, content) {
    fieldDataChanged = true;
});

// Exclude submit and delete buttons from triggering message
const excludedButtons = [
    "#submit",
    "#button-delete"
]
excludedButtons.forEach(button => {
    var element = document.querySelector(button);
    if (element) {
        element.addEventListener("click", () => {
            fieldDataChanged = false;
        });
    }
})

// Add event listener to show message before navigating away
window.addEventListener("beforeunload", (event) => {
    if (fieldDataChanged) {
        event.preventDefault();
    }
});
