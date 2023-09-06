/**
* Search engine class
* Takes the search bar input element in the constructor.
*/
class SearchEngine {
  constructor(searchBar) {
    this.searchBar = searchBar;
    this.results = [];
  }

  /**
  * Timeline search method
  * Takes the searchBar input and iterates through all event headers on the page.
  * Returns Result objects and appends them to results array.
  */
  timelineSearch() {

    var searchQuery = this.searchBar.value.toLowerCase();

    // Check if old results are still valid
    this.resultsCheck(searchQuery);

    // Clear results and end operation if searchbar cleared
    if (searchQuery.length == 0){
      this.results = [];
      return;
    }

    var monthOuters = document.getElementsByClassName("month-outer");
  
    // Iterate through all month-outer elements
    for (var outerIndex = 0; outerIndex < monthOuters.length; outerIndex++) {

      // Get the current month-outer element
      var container = monthOuters[outerIndex];

      // Find all the elements with the class "event-header" within the container
      var eventHeaders = container.querySelectorAll(".event-header");
  
      // Iterate through all the event-header elements
      for (var headerIndex = 0; headerIndex < eventHeaders.length; headerIndex++) {
        var eventHeader = eventHeaders[headerIndex];
        var elementText = eventHeader.innerText.toLowerCase();
  
        // Compare searchQuery against event header text
        if (elementText.includes(searchQuery)) {

          // Check if result is already in results array
          var exists = this.results.some(result => result.elementText === elementText);
          if (!exists) {

            // If result doesn't already exist, create result object
            var result = new Result({
              elementText: elementText,
              outerIndex: outerIndex,
              headerIndex: headerIndex,
              resultBelow: null,
              scrollTarget: eventHeaders[headerIndex].closest('.timeline-event'),
              elements: {
                headerElement: eventHeaders[headerIndex], 
                rightBranchLabel: eventHeaders[headerIndex].closest('.right-branch-label'), 
                eventLine: eventHeaders[headerIndex].closest('.event-line'),
              }
            })

            // Append new result object to result list
            this.results.push(result)

          }

        }
          
      } 

      // Check if month outer has any matching results
      this.results.forEach((result, index) => {

        // Check if result is from current month outer
        if (result.outerIndex == outerIndex) {
          // Reset any styling that other searches may have applied
          container.style.opacity = "100%";
        }

        // If month outer has no resuls within it, set opacity to 50%
        else {
          container.style.opacity = "50%";
        }
  
      });

    }


  }



  /**
  * Method to iterate through all current results objects
  * and remove ones that no longer match the search query.
  */
  resultsCheck(searchQuery) {

    this.results.forEach((result, index) => {

      // Remove result if it no longer matches the search query string
      if (!result.elementText.includes(searchQuery)) {
        this.results = this.results.splice(index, index)
      }

    });

  }


  
}


class Result {
  constructor({
    elementText, 
    outerIndex, 
    headerIndex, 
    resultBelow, 
    scrollTarget,
    elements,
  }) {
    this.elementText = elementText;
    this.outerIndex = outerIndex;
    this.headerIndex = headerIndex;
    this.resultBelow = resultBelow;
    this.scrollTarget = scrollTarget;
    this.elements = elements;
  }

  /**
    * Method to style result object
    */
  styleResult(result) {

    result.elements["headerElement"].style.opacity = "100%";

  }

  /**
  * Method to style negative result object
  */
  styleNegativeResult(result) {

    result.elements["headerElement"].style.opacity = "50%";

  }


}



// Get searchbar and create search engine
const searchBar = document.getElementById("search-bar");
const searchEngine = new SearchEngine(searchBar)

// Add event listener to the input field
searchBar.addEventListener("input", () => searchEngine.timelineSearch());

