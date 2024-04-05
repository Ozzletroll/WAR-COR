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
var initialValue = hitsCounter.innerText;
const searchEngine = new SearchEngine(
  searchBar, 
  hitsCounter, 
  editPage,
  initialValue
  )

// Function called by timeline searchbar "Search" button
function triggerSearch() {
  searchEngine.scrollToResults();
}
window.triggerSearch = triggerSearch;

// Add event listener to the timeline input field to listen for enter keypress
searchBar.addEventListener("input", () => searchEngine.timelineSearch());
searchBar.addEventListener("keydown", function(event) {
  if (event.key === "Enter" && searchBar.value.length > 0) {
    searchEngine.scrollToResults();
  }
});
