// Get the input field and the element to update
var inputField = document.getElementById("suffix-input");
var exampleDate = document.getElementById("example-date");

// Store the initial suffix text
var suffixText = exampleDate.textContent;

// Add event listener to the input field
inputField.addEventListener("input", function() {
  // Get the input value
  var inputValue = inputField.value;

  // If the input value is shorter than the stored suffix text,
  // remove the last character from the suffix text
  if (inputValue.length < suffixText.length) {
    suffixText = suffixText.slice(0, -1);
  }

  // Add the input value as a suffix to the element's text
  exampleDate.textContent = suffixText + inputValue;
});
