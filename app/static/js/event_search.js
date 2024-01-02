const fadeValue = "30%";

class Result {
  constructor({
    baseElement,
    textElement,
  }) {
    this.positive = false;
    this.baseElement = document.querySelector(baseElement);
    this.textElement = this.baseElement.querySelector(textElement);
    this.scrollTarget = this.baseElement;
  }

  stylePositive() {
  
  }

  styleNegative() {
    this.baseElement.style.opacity = fadeValue;
  }
  
  styleReset() {
    this.baseElement.style.opacity = "";
  }
}


/**
* Search engine class
* Takes the search bar input element in the constructor.
*/
class SearchEngine {
  constructor(searchBar, hitsCounter) {
    this.searchBar = searchBar;
    this.hitsCounter = hitsCounter;
    this.results = [];
    this.searchQuery = this.searchBar.value.toLowerCase();
    this.scrollIndex = 0;
  }

  /**
  * Timeline search method
  * Takes the searchBar input and iterates through all fields on event page
  * Returns Result objects and appends them to results array.
  */
  eventSearch() {

    this.searchQuery = this.searchBar.value.toLowerCase();

    // Check if old results are still valid
    this.resultsCheck(this.searchQuery);

    this.updateUI();

    // Clear results and end operation if searchbar cleared
    if (this.searchQuery.length == 0){

      // Reset styling for each result
      this.results.forEach(result => {
        result.styleReset();
      });
      // Clear all existing search attributes
      this.results = [];
      this.updateUI();
      return;
    }

  // Get page fields and create result object for each
  var eventLocation = new Result({
    baseElement: ".event-location",
    textElement: ".event-elem-body",
  });
  var eventBelligerents = new Result({
    baseElement: ".event-belligerents",
    textElement: ".event-elem-body"
  });
  var eventDesc = new Result({
    baseElement: ".event-page-description",
    textElement: ".event-desc"
  });
  var eventResults = new Result({
    baseElement: ".event-page-result",
    textElement: ".event-elem-body"
  });

  this.results = [eventLocation, eventBelligerents, eventDesc, eventResults];

  // Flag positive matching result elements
  this.resultsCheck();

  // Apply styles to all elements
  this.applyStyles();
  
  }


  applyStyles() {

  this.results.forEach((result, index) => {

    result.styleReset();

    if (result.positive) {
      result.stylePositive();
    }
    else {
      result.styleNegative();
    }
  
  });

  }


  /**
  * Method to iterate through all current results objects in this.results
  * and remove ones that do not match the search query.
  */
  resultsCheck() {

  this.results.forEach((result, index) => {

    if (result.textElement.innerText.toLowerCase().includes(this.searchQuery)) {
      result.positive = true;
    }
    else {
      result.positive = false;
    }
  
  });

  }


  /**
  * Method to update ui hits counter
  */
  updateUI() {
    var positiveResults = this.results.filter(result => result.positive);

    if (this.searchQuery.length == 0) {
      this.hitsCounter.innerText = initialValue;
    }
    else {
      this.hitsCounter.innerText = `${positiveResults.length} RESULTS`;
    }
  }

  /**
  * Method to scroll through any results.
  * Called via event listener.
  */
  scrollToResults() {

    var positiveResults = this.results.filter(result => result.positive);

    if (this.results.length === 0) {
      // No results
      return; 
    }

    if (this.scrollIndex >= positiveResults.length) {
      // Reset index if reached the end
      this.scrollIndex = 0; 
    }

    const element = positiveResults[this.scrollIndex];
    // Scroll to element
    element.scrollTarget.scrollIntoView(); 
    this.hitsCounter.innerText = `${this.scrollIndex + 1} OF ${positiveResults.length} RESULTS`;

    // Increment the index for the next call
    this.scrollIndex++; 
  }

}

// Determine if we are on the edit page
var editPageElem = document.getElementById("editPageVariable").getAttribute("editPage");
editPage = false;
if (editPageElem == "true") {
  editPage = true;
}

// Get searchbar and create search engine
const searchBar = document.getElementById("search-bar");
const hitsCounter = document.getElementById("hits-counter");
const initialValue = hitsCounter.innerText;
const searchEngine = new SearchEngine(searchBar, hitsCounter)

// Function called by timeline searchbar "Search" button
function triggerEventSearch() {
  searchEngine.scrollToResults();
}

// Add event listener to the timeline input field to listen for enter keypress
searchBar.addEventListener("input", () => searchEngine.eventSearch());
searchBar.addEventListener("keydown", function(event) {
  if (event.key === "Enter" && searchBar.value.length > 0) {
  searchEngine.scrollToResults();
  }
});
