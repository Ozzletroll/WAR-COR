// Opacity value for negative result elements
const fadeValue = "30%";

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
  // Reset styling for self
    this.styleReset();

    if (this.resultsBelow == false) {
      this.elements["eventLine"].style.opacity = fadeValue;
    }
  }

  /**
  * Method to style negative result object
  */
  styleNegative() {
    // Reset styling for self
    this.styleReset();
    // Style downwards line if there are no results below it in the block
    if (this.resultsBelow == false) {
      this.elements["eventLine"].style.opacity = fadeValue;
    }

    this.elements["eventOutline"].style.opacity = fadeValue;
    this.elements["rightBranchLabel"].style.opacity = fadeValue;
  }

  styleReset() {
    this.elements["headerElement"].style.opacity = "";
    this.elements["eventOutline"].style.opacity = "";
    this.elements["eventLine"].style.opacity = "";
    this.elements["rightBranchLabel"].style.opacity = "";
  }

}



class Day {
  constructor({
    elements,
    dayLine,
    events,
    daysBelow,
    containsPositiveResult,
  }) {
    this.elements = elements;
    this.dayLine = dayLine;
    this.events = events;
    this.daysBelow = daysBelow;
    this.containsPositiveResult = containsPositiveResult;
  }

  /**
  * Method to determine if day contains any events which have the property event.positive
  */
  checkDaysResults() {
    const containsPositiveEvent = this.events.some(event => event.positive === true);
    if (containsPositiveEvent) {
      this.containsPositiveResult = true;
    }
    else {
      this.containsPositiveResult = false;
    }
  }


  /**
    * Method to determine if each event in day has elements below it
    * in order to determine appropriate line styling.
    */
  checkResultsBelow() {
    // Set the resultsBelow attribute for days event objects to "true" if there are positive results below it
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

    // Reset day opacity
    this.resetStyles();

    // If there are no days containing results below, set vertical line opacity to 50%
    if (this.daysBelow == false) {
      this.dayLine.style.opacity = fadeValue;
    }

    // Set day block opacity to 50% if it contains no positive results
    const anyPositiveEvent = this.events.some(event => event.positive === true);
    if (!anyPositiveEvent) {
      this.elements["rightBranchLabel"].style.opacity = fadeValue;
      this.elements["eventGroupContainer"].style.opacity = fadeValue;
    }

    // If day block contains positive results, style each result accordingly
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
  resetStyles() {
    this.elements["rightBranchLabel"].style.opacity = "";
    this.elements["eventGroupContainer"].style.opacity = "";
    this.dayLine.style.opacity = "";

    this.events.forEach(result => {
      result.styleReset();
    });
  }

}




class Month {
  constructor({
    element,
    days,
    containsPositiveResult,
  }) {
    this.element = element;
    this.days = days;
    this.containsPositiveResult = containsPositiveResult;
  }

  /**
  * Method to determine if Month has any days that contain positive
  * search query results.
  */
  checkDaysResults() {

    const hasPositiveEvent = this.days.some((day) => {
      const positiveEvent = day.events.find((event) => event.positive === true);
      return positiveEvent !== undefined;
    });
  
    if (hasPositiveEvent) {
      this.containsPositiveResult = true;
    } 
    else {
      this.containsPositiveResult = false;
    }

  }


   /**
    * Method to determine if each day object in this.days has 
    * a day containing positive results below it.
    */
   checkDaysBelow() {
    this.days.forEach((day, index) => {

      day.checkResultsBelow();

      day.daysBelow = this.days.some((nextDay, nextIndex) =>
        nextIndex > index && nextDay.containsPositiveResult
      );
    });
  }


  /**
  * Method to style all search results within month
  */
    setStyle() {

      // Reset month opacity
      this.element.style.opacity = "";

      // Check if each day object contains positive results
      this.checkDaysResults();

      // Check if each day object has day objects containing positive results below it.
      this.checkDaysBelow();

      // If no positive results, set to fade value
      if (this.containsPositiveResult == false) {
        this.element.style.opacity = fadeValue;
        this.days.forEach(day => {
          day.resetStyles();
        });
      }
      // If day block does contain positive results, style each day within month
      else {
        this.days.forEach(day => {
          day.resetStyles();
          day.setStyle();
        });
      }
      
    
    }

    resetStyles() {
      // Reset month opacity
      this.element.style.opacity = "";

      // Reset styles for all days
      this.days.forEach(day => {
        day.resetStyles();
      });
    }


}





/**
* Search engine class
* Takes the search bar input element in the constructor.
* Creates a list of results, as well as formats results into
* Month/Day/Events structure.
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
        month.resetStyles();
      });
      // Clear all existing search attributes
      this.months = [];
      this.results = [];
      return;
    }

    this.months = [];
    this.results = [];

    var monthOuters = document.getElementsByClassName("month-outer");
  
    // Iterate through all month-outer elements
    for (var outerIndex = 0; outerIndex < monthOuters.length; outerIndex++) {

      // Get the current month-outer element
      var monthOuter = monthOuters[outerIndex];

      var month = new Month({
        element: monthOuter,
        days: [],
        containsPositiveResult: false,
      })

      // Get all the days within the month
      var days = monthOuter.querySelectorAll(".timeline-day-outer");

      // Iterate through all days
      for (var dayIndex = 0; dayIndex < days.length; dayIndex++) {

        // Current day
        var dayContainer = days[dayIndex];

        // Create day object instance
        var day = new Day({
          elements: {
            rightBranchLabel: dayContainer.querySelector(".right-branch-label"),
            eventGroupContainer: dayContainer.querySelector(".event-group-container"),
          },
          dayLine: dayContainer.querySelector(".event-line"),
          events: [],
          daysBelow: false,
          containsPositiveEvent: false,
        })

        // Find all the elements with the class "event-header" within the container
        var eventHeaders = dayContainer.querySelectorAll(".event-header");
          
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
              monthOuter: monthOuter,
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
          }

          // Append new result object to day objects events array
          day.events.push(result); 
        }

        // Append day object to month objects day array
        month.days.push(day);

      }
    
      // Add month to searchEngine month list
      this.months.push(month);

    }


    // Apply styles to all elements
    this.applyStyles();
    

  }


  applyStyles() {

    // Finalise data structure
    this.months.forEach(month => {

      month.days.forEach(day => {
        // For each day in month, determine if day contains positive results
        day.checkDaysResults();
        // For each day in month, determine if each event has a positive result after it in the block
        day.checkResultsBelow();
      });

      // For each month, check if each day within month has a day containing positive results after it
      month.checkDaysBelow();


      // Set styling for each month block
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

