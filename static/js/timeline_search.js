class Result {
  constructor({
    positive,
    elementText, 
    outerIndex, 
    headerIndex, 
    resultsBelow, 
    scrollTarget,
    elements,
  }) {
    this.positive = positive;
    this.elementText = elementText;
    this.outerIndex = outerIndex;
    this.headerIndex = headerIndex;
    this.resultsBelow = resultsBelow;
    this.scrollTarget = scrollTarget;
    this.elements = elements;
  }

  /**
    * Method to style result object
    */
  stylePositive() {

    this.styleReset();

    this.elements["headerElement"].style.opacity = "100%";

    if (this.resultsBelow == false) {
      this.elements["eventLine"].style.opacity = "50%";
    }
  }

  /**
  * Method to style negative result object
  */
  styleNegative() {

    this.styleReset();

    // Style downwards line if there are no results below it in the block
    if (this.resultsBelow == false) {
      this.elements["eventLine"].style.opacity = "50%";
    }

    this.elements["eventOutline"].style.opacity = "50%";
    this.elements["rightBranchLabel"].style.opacity = "50%";

  }

  styleReset() {
    this.elements["eventOutline"].style.opacity = "";
    this.elements["eventLine"].style.opacity = "";
    this.elements["rightBranchLabel"].style.opacity = "";
  }

}

// NOTE: Refactor this to have month.days attribute, that then contains day.events.
// This will allow the day marker to get greyed out properly when a day contains 
// no positive matches.

// Search for "op" and look at "ASD" event for example of bugged behaviour!

class Month {
  constructor({
    element,
    events,
  }) {
    this.element = element;
    this.events = events;
  }

  /**
    * Method to determine if each event in month has elements below it
    * in order to determine appropriate line styling.
    */
  checkResultsBelow() {
    // Set the resultsBelow attribute to "true" if there are positive results below it
    this.events.forEach((result, index) => {
      result.resultsBelow = this.events.some((nextResult, nextIndex) =>
        nextIndex > index && nextResult.positive
      );
    });

  }


  /**
  * Method to style all search results within month
  */
  setStyle() {

    // Reset month opacity
    this.element.style.opacity = "";
    this.resetAllStyles();

    // Set month block opacity to 50% if it contains no positive results
    const anyPositiveEvent = this.events.some(event => event.positive === true);
    if (!anyPositiveEvent) {
      this.element.style.opacity = "50%";
    }

    // If a block contains positive results, style each result accordingly
    if (anyPositiveEvent) { 

      // Reset any styling that may already be applied to result
      this.events.forEach(result => {
        result.styleReset();

        if (result.positive) {
          result.stylePositive();
        }
        else {
          result.styleNegative();
        }
      });
    }
  }


  /**
  * Method to clear all styling from search result within the month
  */
  resetAllStyles() {
    this.events.forEach(result => {
      result.styleReset();
    });
  }

}

/**
* Search engine class
* Takes the search bar input element in the constructor.
*/
class SearchEngine {
  constructor(searchBar) {
    this.searchBar = searchBar;
    this.results = [];
    this.months = [];
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

      // Reset styling for each month block
      this.months.forEach(month => {
        month.resetAllStyles();
      });
      // Clear all existing search attributes
      this.months = [];
      this.results = [];
      return;
    }

    var monthOuters = document.getElementsByClassName("month-outer");
  
    // Iterate through all month-outer elements
    for (var outerIndex = 0; outerIndex < monthOuters.length; outerIndex++) {

      // Get the current month-outer element
      var container = monthOuters[outerIndex];

      var month = new Month({
        element: container,
        events: [],
      })

      // Find all the elements with the class "event-header" within the container
      var eventHeaders = container.querySelectorAll(".event-header");
  
      // Iterate through all the event-header elements
      for (var headerIndex = 0; headerIndex < eventHeaders.length; headerIndex++) {
        var eventHeader = eventHeaders[headerIndex];
        var elementText = eventHeader.innerText.toLowerCase();

        // Get result elements for styling
        var outerContainer = eventHeaders[headerIndex].closest('.event-outer-container');
        var rightBranchLabel = outerContainer.previousElementSibling;
        var eventLine = rightBranchLabel.previousElementSibling;
  
        // Create instance of result object
        var result = new Result({
          positive: false,
          elementText: elementText,
          outerIndex: outerIndex,
          headerIndex: headerIndex,
          resultsBelow: false,
          scrollTarget: eventHeaders[headerIndex].closest('.timeline-event'),
          elements: {
            monthOuter: container,
            headerElement: eventHeaders[headerIndex],
            eventOutline: eventHeaders[headerIndex].closest('.event-outline'), 
            rightBranchLabel: rightBranchLabel, 
            eventLine: eventLine,
          }
        })

        // Compare searchQuery against event header text
        if (elementText.includes(searchQuery)) {

          // Check if result is already in results array
          var exists = this.results.some(result => result.elementText === elementText);
          if (!exists) {
            // Append new result object to searchEngine result array
            this.results.push(result)
          }

          // Flag result as positive query match
          result.positive = true;

          // Append new result object to month objects events array
          month.events.push(result);
        }

        // If result does not match query
        else {
          // Append new result object to month objects positive results array
          month.events.push(result);
        }
          
      }
      
      // Add month to searchEngine month list
      this.months.push(month);

    }

    // Set styling for each month block
    this.months.forEach(month => {
      month.checkResultsBelow();
      month.setStyle();
    });

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




// Get searchbar and create search engine
const searchBar = document.getElementById("search-bar");
const searchEngine = new SearchEngine(searchBar)

// Add event listener to the input field
searchBar.addEventListener("input", () => searchEngine.timelineSearch());

