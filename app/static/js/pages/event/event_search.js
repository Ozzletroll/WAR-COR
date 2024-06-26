import { SearchEngine } from "../../components/search/search_engine.js"


// Determine if we are on the edit page
var editPageElem = document.getElementById("editPageVariable").getAttribute("editPage");
var editPage = false;
if (editPageElem == "true") {
  editPage = true;
}

// Get searchbar and create search engine
const searchBar = document.getElementById("search-bar");
const hitsCounter = document.getElementById("hits-counter");
const initialValue = hitsCounter.innerText;
const searchEngine = new SearchEngine(
  searchBar, 
  hitsCounter,
  editPage,
  initialValue,
  "eventSearch"
  )

// Function called by searchbar "Search" button
function triggerEventSearch() {
  searchEngine.scrollToResults();
}
window.triggerEventSearch = triggerEventSearch;

// Add event listener to the timeline input field to listen for enter keypress
searchBar.addEventListener("input", () => searchEngine.eventSearch());
searchBar.addEventListener("keydown", function(event) {
  if (event.key === "Enter" && searchBar.value.length > 0) {
  searchEngine.scrollToResults();
  }
});

// Add event listen to the Summernote editor field to listen for user interaction
document.addEventListener("DOMContentLoaded", function() {
  if (editPage == true) {

    var summernoteEditors = document.getElementsByClassName("note-editor");

    function lengthChanged() {
      Array.from(summernoteEditors).forEach(editor => {
        editor.addEventListener("input", function(event) {
          if (searchEngine.searchBar.value != "") {
            searchEngine.clearSearch();
          }
          searchEngine.updateDescription();
        });
        
        editor.addEventListener("click", function(event) {
          if (searchEngine.searchBar.value != "") {
            searchEngine.clearSearch();
          }
        });
      })
  
      var updateButton = document.getElementById("submit");
      updateButton.addEventListener("click", function(event) {
        if (searchEngine.searchBar.value != "") {
          searchEngine.clearSearch();
        }
      });
    }

    // Create a MutationObserver instance to watch for changes in the summernoteEditors collection
    var observer = new MutationObserver(function(mutations) {
      // If any mutation represents a change in child list, call lengthChanged
      if (mutations.some(mutation => mutation.type === 'childList')) {
          lengthChanged();
      }
    });

    // Start observing the document with the configured parameters
    observer.observe(document, { childList: true, subtree: true });
  }
});
