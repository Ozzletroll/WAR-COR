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

    // Handle basic event page elements
    if (this.textElement.classList.contains("event-elem-body")
    || this.textElement.classList.contains("event-input")) {
      this.queryMatches.push(this.baseElement);
    }
    // Handle user submitted html elements
    else {
      this.initialHTML = this.textElement.innerHTML;
      var selector = `.event-desc > p,
                       .event-desc > ul > li,
                       .event-desc > ol > li,
                       .note-editable > ul > li,
                       .note-editable > ol > li,
                       .note-editable > p`;

      var elements = this.textElement.querySelectorAll(selector);

      // Exclude user image elements
      elements = Array.from(elements).filter(function(element) {
        if (element.matches('.note-editable > p')) {
          if (element.querySelector('img') !== null) {
            return false;
          }
        }
        return true;
      });

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

  this.results = []

  if (editPage == false) {
    // Get event and epoch page fields and create result object for each if they exist on page
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

    var element = document.querySelector(".epoch-events-container");
    if (element) {
      var epochResults = new Result({
        baseElement: ".epoch-events-container",
        textElement: ".epoch-events-list"
      });
      this.results.push(epochResults);
    }
  }
  else {
    // Get edit event page fields and create result object for each if they exist on page
    var editFields = [
      "#date-field", 
      "#title-field", 
      "#type-field", 
      "#location-field", 
      "#belligerents-field",  
      "#result-field"
    ]

    editFields.forEach((field) => {
      var element = document.querySelector(field);
      if (element) {
        var newResultObject = new Result({
          baseElement: field,
          textElement: ".event-input",
        });
        this.results.push(newResultObject);
      }
    })

    var element = document.querySelector(".note-editor");
      if (element) {
        var newResultObject = new Result({
          baseElement: ".note-editor",
          textElement: ".note-editable",
        });
        this.results.splice(5, 0, newResultObject);
      }

  }

  this.resultsCheck();
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
        if (editPage == false) {
          if (result.textElement.innerText.toLowerCase().includes(this.searchQuery)) {
            result.positive = true;
          }
          else {
            result.positive = false;
          }
        }
        else {
          // Handle event description field
          if (result.baseElement.classList.contains("note-editor")) {
            if (result.textElement.innerText.toLowerCase().includes(this.searchQuery)) {
              result.positive = true;
            }
            else {
              result.positive = false;
            }
          }
          // Handle all other edit event fields
          else {
            if (result.textElement.value.toLowerCase().includes(this.searchQuery)) {
              result.positive = true;
            }
            else {
              result.positive = false;
            }
          }
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

  // Method to clear search input and remove all applied result styling
  // Called when closing searchbar tab, interacting with the event desc input field,
  // or submitting the form
  clearSearch() {
    this.searchBar.value = "";
    this.searchBar.blur();
    this.results.forEach((result, index) => {
      result.styleReset();
    });
    this.results = [];
    this.updateUI();

  }

  // Method called when input detected in description field
  // Updates the description field result object's stored inital value
  updateDescription() {
    this.results.forEach((result, index) => {
      if (index == 5) {
        result.initialHTML = result.textElement.innerHTML;
      }
    });
  }

}

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
const searchEngine = new SearchEngine(searchBar, hitsCounter)

// Functions called by searchbar "Search" button
function triggerEventSearch() {
  searchEngine.scrollToResults();
}

function triggerEpochSearch() {
  searchEngine.scrollToResults();
}

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

