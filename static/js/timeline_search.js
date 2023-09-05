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
            })

            // Append new result object to result list
            this.results.push(result)

          }

        
        }
          
      }
  
    }

    console.log("End of timeline search function:")
    console.log(this.results)


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
  }) {
    this.elementText = elementText;
    this.outerIndex = outerIndex;
    this.headerIndex = headerIndex;
    this.resultBelow = resultBelow;
    this.scrollTarget = scrollTarget;
  }


}



// Get searchbar and create search engine
const searchBar = document.getElementById("search-bar");
const searchEngine = new SearchEngine(searchBar)

// Add event listener to the input field
searchBar.addEventListener("input", () => searchEngine.timelineSearch());

