const charField = document.getElementsByClassName("note-editable")[0];
const charCount = document.getElementById("remaining-chars");
const charLimit = parseInt(charCount.innerText);

function updateCharCount(charField) {
    var currentChars = charField.textContent.length;
    var remainingChars = charLimit - currentChars;
    charCount.innerText = remainingChars;
}

updateCharCount(charField);

// Add event listener to the input field
charField.addEventListener("input", function() {
  updateCharCount(charField);
});
