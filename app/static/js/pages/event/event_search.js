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
  initialValue
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
if (editPage == true) {

  var summernoteEditor = document.querySelector(".note-editor");
  summernoteEditor.addEventListener("input", function(event) {
    if (searchEngine.searchBar.value != "") {
      searchEngine.clearSearch();
    }
    searchEngine.updateDescription();
  });
  
  summernoteEditor.addEventListener("click", function(event) {
    if (searchEngine.searchBar.value != "") {
      searchEngine.clearSearch();
    }
  });

  var updateButton = document.getElementById("submit");
  updateButton.addEventListener("click", function(event) {
    if (searchEngine.searchBar.value != "") {
      searchEngine.clearSearch();
    }
  });

}

