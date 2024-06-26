export function summernoteInitialise(
  idSuffix,
  placeholder,
  charLimit,
  allowImages,
  allowURLS,
  htmlPreview
) {
  charLimit = parseInt(charLimit) || null;
  var editor = "#summernote" + idSuffix;

  // Get jinja macro arguments
  if (allowImages == "True") {
    allowImages = "picture";
  }
  if (allowURLS == "True") {
    allowURLS = "link";
  }
  if (htmlPreview == "True") {
    htmlPreview = ['mybutton', ['HTMLPreview']];
  }
  
  $(editor).summernote({
    callbacks: {
      onInit: function(event) {
        var editable = event.editable;
        setHORUSstyling(editable);
      },
      onKeydown: function(event) {
        enforceCharLimit(event, charLimit);
        preventDelete(event, editor);
      },
      onChange: function(contents, $editable) {
        handleUnwrappedTags(editor, $editable);
        setHORUSstyling($editable);
        $(document).trigger("summernoteFieldChanged", [$(this).summernote("code")]);
      },
      onPaste: function(event) {
        pastePlainText(event, editor, charLimit);
      },
    },
    stickyToolbar: {
      enabled: true,
      offset: 54,
      zIndex: 9999
    },
    disableDragAndDrop: true,
    placeholder: "<p>" + placeholder + "</p>",
    dialogsClass: "summernote-dialog",
    dialogsInBody: true,
    dialogsFade: true, 
    tabsize: 2,
    height: "fit-content",
    styleTags: [
      'p', 
      'h1', 
      'h2', 
      'h3',
      {
        tag : 'p',
        title : 'Flavour Text',
        style : 'user-flavour-text',
        className : 'user-flavour-text',
        value : 'p'
      },
      {
        tag : 'p',
        title : 'CASTIGATE THE ENEMIES OF THE GODHEAD',
        style : 'horus',
        className : 'summernote-horus',
        value : 'p'
      },
    ],
    toolbar: [
      ['style', ['style']],
      ['font', ['bold', 'italic', 'underline', 'clear']],
      ['para', ['ul', 'ol', 'paragraph']],
      ['insert', [allowURLS, allowImages]],
      htmlPreview,

    ],
    buttons: {
      HTMLPreview: HTMLPreviewButton
    },
    popover: {
      image: [
        ['remove', ['removeMedia']]
      ]
    },
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
  var bufferText = ((event.originalEvent || event).clipboardData || window.clipboardData).getData("Text");
  event.preventDefault();

  if (charLimit != null) {
    charLimit = charLimit;
    var currentTextLength = event.currentTarget.textContent.length;
    var pasteLength = bufferText.length;
    var proposedTextLength = currentTextLength + pasteLength;

    if (proposedTextLength > charLimit) {
      pasteLength = pasteLength - (proposedTextLength - charLimit);
    }

    $(editor).summernote("insertText", bufferText.substring(0, pasteLength));
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
  var innerTextLength = event.currentTarget.textContent.length; // Summernote's default formatting adds 1 char

  const isCtrlKeyCombination = (keyCode) => [65, 67, 88].includes(keyCode);
  const isArrowKey = (keyCode) => keyCode >= 37 && keyCode <= 40;
  const isDeleteOrBackspace = (keyCode) => [8, 46].includes(keyCode);

  if (innerTextLength >= charLimit) {
    if (!isDeleteOrBackspace(event.keyCode) && 
        !isArrowKey(event.keyCode) && 
        !(isCtrlKeyCombination(event.keyCode) && event.ctrlKey)) {
      event.preventDefault(); 
    }
  }
}


// Update styling of horus text elements
function setHORUSstyling(editable) {
  var horusElements = editable.find(".summernote-horus");
  horusElements.each(function() {
    $(this).attr("data-content", $(this).text());
  })
}


// Preview HTML Button
var HTMLPreviewButton = function (context) {
  var ui = $.summernote.ui;

  // Create button
  var button = ui.button({
    contents: '<i class="fa fa-child"/> PREVIEW',
    tooltip: "View HTML Preview",
    click: function () {
    },
    container: context.layoutInfo.editor,
  });
  return button.render();
}
