const fadeValue = "30%";

class Result {
  constructor({
    baseElement,
    textElement,
  }) {
    this.positive = false;
    this.baseElement = document.querySelector(baseElement);
    this.textElement = this.baseElement.querySelector(textElement);
    this.initialHTML = this.textElement.innerHTML;
    this.queryMatches = [];
  }

  stylePositive(searchQuery) {

    if (this.textElement.classList.contains("event-elem-body")) {
      this.queryMatches.push(this.baseElement);
    }
    else {
      var elements = this.textElement.querySelectorAll(".event-desc > p, .event-desc > ul > li, .event-desc > ol > li");

      elements.forEach((element, index) => {
  
        // Create a regular expression with the "gi" flags (global, case-insensitive)
        const regex = new RegExp(searchQuery, "gi");
  
        // Replace all matching instances with the wrapped version
        element.innerHTML = element.innerText.replace(regex, (match) => {
          return `<strong class="search-highlight">${match}</strong>`;
        });

        // Get all newly created search highlighted elements 
        // and push them to the queryMatches array
        var searchHighlights = element.querySelectorAll(".search-highlight");
        searchHighlights.forEach((element) => {
          this.queryMatches.push(element);
        })
      });
    }
    

  }

  styleNegative() {
    this.baseElement.style.opacity = fadeValue;
  }
  
  styleReset() {
    this.baseElement.style.opacity = "";
    this.textElement.innerHTML = this.initialHTML;
    this.queryMatches = [];
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
    this.matchingElements = [];
    this.searchQuery = this.searchBar.value.toLowerCase();
    this.scrollIndex = 0;
  }

  /**
  * Event page search method
  * Takes the searchBar input and iterates through all fields on event page
  * Returns Result objects and appends them to results array.
  */
  eventSearch() {

    this.searchQuery = this.searchBar.value.toLowerCase();

    // Check if old results are still valid
    this.resultsCheck(this.searchQuery);
    this.scrollIndex = 0;

    this.updateUI();

    // Clear results and end operation if searchbar cleared
    if (this.searchQuery.length == 0){
      // Reset styling for each result
      this.results.forEach(result => {
        result.styleReset();
      });
      // Clear all existing search attributes
      this.results = [];
      this.scrollIndex = 0;
      this.updateUI();
      return;
    }

  // Get page fields and create result object for each if they exist on page
  this.results = []

  var element = document.querySelector(".event-location");
  if (element) {
    var eventLocation = new Result({
      baseElement: ".event-location",
      textElement: ".event-elem-body",
    });
    this.results.push(eventLocation);
  }

  var element = document.querySelector(".event-belligerents");
  if (element) {
    var eventBelligerents = new Result({
      baseElement: ".event-belligerents",
      textElement: ".event-elem-body"
    });
    this.results.push(eventBelligerents);
  }

  var element = document.querySelector(".event-page-description");
  if (element) {
    var eventDesc = new Result({
      baseElement: ".event-page-description",
      textElement: ".event-desc"
    });
    this.results.push(eventDesc);
  }

  var element = document.querySelector(".event-page-result");
  if (element) {
    var eventResults = new Result({
      baseElement: ".event-page-result",
      textElement: ".event-elem-body"
    });
    this.results.push(eventResults);
  }

  // Flag positive matching result elements
  this.resultsCheck();

  // Apply styles to all elements
  this.applyStyles();

  this.populateMatchingElements();

  this.updateUI();
  
  }


  applyStyles() {
    this.results.forEach((result, index) => {
      result.styleReset();
      if (result.positive) {
        result.stylePositive(this.searchQuery);
      }
      else {
        result.styleNegative();
      }
    });
  }

  resultsCheck() {
    this.results.forEach((result, index) => {
      result.styleReset();
      if (result.textElement.innerText.toLowerCase().includes(this.searchQuery)) {
        result.positive = true;
      }
      else {
        result.positive = false;
      }
      });
  }

  populateMatchingElements() {
    this.matchingElements = [];

    this.results.forEach((result, index) => {
      result.queryMatches.forEach((element) => {
        this.matchingElements.push(element);
      });
    });
  }

  /**
  * Method to update ui hits counter
  */
  updateUI() {
    var positiveResults = this.results.filter(result => result.positive);
    // Sum total of all query matches
    var totalMatches = 0;
    positiveResults.forEach((result, index) => {
      totalMatches += result.queryMatches.length;
    });

    if (this.searchQuery.length == 0) {
      this.hitsCounter.innerText = initialValue;
    }
    else {
      this.hitsCounter.innerText = `${totalMatches} RESULTS`;
    }
  }

  /**
  * Method to scroll through any results.
  * Called via event listener.
  */
  scrollToResults() {

    var positiveResults = this.matchingElements;

    if (positiveResults.length === 0) {
      // No results
      return; 
    }
    if (this.scrollIndex >= positiveResults.length) {
      // Reset index if reached the end
      this.scrollIndex = 0; 
    }

    const element = positiveResults[this.scrollIndex];

    // Scroll to element and highlight matching result
    element.scrollIntoView();
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
