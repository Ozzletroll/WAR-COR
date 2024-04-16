import { Modal } from "../../components/modal.js";
import { CharCount } from "../../components/char_count.js";
import { SuffixExample } from "../../components/suffix_example.js";


// Create instances of SuffixExamples to update the suffix preview text 
const dateSuffixExample = new SuffixExample({
  suffixField: document.getElementById("campaign-form-suffix"),
  suffixExample: document.getElementById("example-date")
})

const negativeDateSuffixExample = new SuffixExample({
  suffixField: document.getElementById("campaign-form-negative-suffix"),
  suffixExample: document.getElementById("negative-example-date")
})

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

const imageHelpModal = new Modal({
  modal: document.getElementById("help-modal-1"),
  button: document.getElementById("campaign-image-help-button"),
  span: document.getElementById("help-close-1"),
})

// Create char count instances
const systemCharCount = new CharCount({
  charField: document.getElementById("campaign-form-system"),
  charCount: document.getElementById("remaining-chars-system"),
})

const descCharCount = new CharCount({
  charField: document.getElementsByClassName("note-editable")[0],
  charCount: document.getElementById("remaining-chars"),
  summernote: true
})
