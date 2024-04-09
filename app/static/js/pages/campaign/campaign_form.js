// Get the date suffix input field and the element to update
var suffixField = document.getElementById("campaign-form-suffix");
var negativeSuffixField = document.getElementById("campaign-form-negative-suffix");

var exampleSuffixDate = document.getElementById("example-date");
var exampleNegativeSuffixDate = document.getElementById("negative-example-date");

// Store the initial suffix text
var suffixText = exampleSuffixDate.textContent;
var negativeSuffixText = exampleNegativeSuffixDate.textContent;

// Function to update suffix example
function updateSuffix(suffixField, exampleSuffixDate) {

  var inputValue = suffixField.value;

  // If the input value is shorter than the stored suffix text,
  // remove the last character from the suffix text
  if (inputValue.length < suffixText.length) {
    suffixText = suffixText.slice(0, -1);
  }

  // Add the input value as a suffix to the element's text
  exampleSuffixDate.textContent = suffixText + inputValue;
}

// Call updateSuffix once when the page loads to display the initial values
updateSuffix(suffixField, exampleSuffixDate);
updateSuffix(negativeSuffixField, exampleNegativeSuffixDate);

// Add event listener to the input field
suffixField.addEventListener("input", function() {
  updateSuffix(suffixField, exampleSuffixDate);
});

negativeSuffixField.addEventListener("input", function() {
  updateSuffix(negativeSuffixField, exampleNegativeSuffixDate);
});


// Function to match the "Date Suffix" header height with 
// the "Negative Suffix" header when the negative suffix text
// splits onto two lines.
function matchSuffixFieldHeights() {

  var dateSuffix = document.getElementById("date-suffix-label");
  var negativeSuffix = document.getElementById("negative-suffix-label");

  var dateSuffixHeight = dateSuffix.offsetHeight;
  var negativeSuffixHeight = negativeSuffix.offsetHeight;

  if (negativeSuffixHeight > dateSuffixHeight && window.innerWidth > 800) {
    dateSuffix.style.height = `${negativeSuffixHeight}px`;
    var words = dateSuffix.innerText.split(" ");
    dateSuffix.innerHTML = words.join("<br>");
  }
  else if (dateSuffixHeight > negativeSuffixHeight) {
    dateSuffix.style.height = "";
    dateSuffix.innerHTML = "Date Suffix";
  }
  
}

window.addEventListener("load", matchSuffixFieldHeights);
window.addEventListener("resize", matchSuffixFieldHeights);
