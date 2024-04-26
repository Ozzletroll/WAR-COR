function summernoteInitialise(idSuffix, 
                              placeholder, 
                              charLimit, 
                              allowImages, 
                              allowURLS) {

  charLimit = parseInt(charLimit) || null;
  var editor = "#summernote" + idSuffix;
  
  $(editor).summernote({
  callbacks: {
    onKeydown: function(event) {
      enforceCharLimit(event, charLimit);
      preventDelete(event, editor);
    },
    onChange: function(contents, $editable) {
      handleUnwrappedTags(editor, $editable);
      $(document).trigger("summernoteFieldChanged", [$(this).summernote("code")]);
    },
    onPaste: function(event) {
      pastePlainText(event, editor, charLimit);
    },
  },
  placeholder: "<p>" + placeholder + "</p>",
  dialogsClass: "summernote-dialog",
  dialogsInBody: true,
  dialogsFade: true, 
  tabsize: 2,
  height: "fit-content",
  styleTags: ['p', 'h1', 'h2', 'h3'],
  toolbar: [
    ['style', ['style']],
    ['font', ['bold', 'italic', 'underline', 'clear']],
    ['para', ['ul', 'ol', 'paragraph']],,
    ['insert', [allowURLS, allowImages]]
  ],
  popover: {
    image: [
      ['remove', ['removeMedia']]
    ]
  }
  });

}

// Callbacks

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

  if (charLimit != null) {
    charLimit = charLimit;
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

  // Do nothing if no char limit set
  if (charLimit == null) {
    return
  }

  charLimit = charLimit;
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
