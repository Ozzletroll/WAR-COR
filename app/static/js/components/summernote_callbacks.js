
// Prevent individual delete key presses from deleting opening tags
function preventDelete(event, editor) {
  if (event.keyCode == 46 || event.keyCode == 8 ) {
    if ($(editor).summernote("isEmpty")) {
      event.preventDefault(); 
    }
  }
}


// Prevent deletion of opening <p> tags
function handleUnwrappedTags(editor, $editable) {
  var initialContent = $editable[0].innerHTML;
  if (initialContent.startsWith("<br>")) {
    $(editor).summernote("formatPara");
  }
}


// Convert clipboard text into plain text
function pastePlainText (event, editor, charLimit) {
  var bufferText = ((event.originalEvent || event).clipboardData || window.clipboardData).getData('Text');
  event.preventDefault();

  if (charLimit != "None") {
    charLimit = parseInt(charLimit);
    var text = event.currentTarget.innerText;
    var maxPaste = bufferText.length;
    if (text.length + bufferText.length > charLimit){
      maxPaste = charLimit - text.length;
    }

    if (maxPaste > 0){
      $(editor).summernote("insertText", bufferText.substring(0, maxPaste));
    }
  }
  else {
    $(editor).summernote("insertText", bufferText);
  }
}


// Prevent adding more characters if char limit reached
function enforceCharLimit(event, charLimit) {

  charLimit = parseInt(charLimit);
  var innerTextLength = event.currentTarget.innerText.trim().length;

  if (innerTextLength >= charLimit) {
    if (event.keyCode != 8 && 
      !(event.keyCode >=37 && event.keyCode <=40) 
      && event.keyCode != 46 && 
      !(event.keyCode == 88 && event.ctrlKey) && 
      !(event.keyCode == 67 && event.ctrlKey) && 
      !(event.keyCode == 65 && event.ctrlKey)) {
      event.preventDefault(); 
    }
  }
}
