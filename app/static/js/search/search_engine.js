import { Result } from './classes/result.js';
import { Day } from './classes/day.js';
import { Month } from './classes/month.js';


/**
* Search engine class
* Takes the search bar input element in the constructor.
* Creates a list of results, as well as formats results into
* Month/Day/Events structure.
*/
export class SearchEngine {
  constructor(searchBar, hitsCounter, editPage, initialValue) {
    this.searchBar = searchBar;
    this.hitsCounter = hitsCounter;
    this.results = [];
    this.months = [];
    this.searchQuery = this.searchBar.value.toLowerCase();
    this.scrollIndex = 0;
    this.editPage = editPage;
    this.initialValue = initialValue;
  }

  /**
  * Timeline search method
  * Takes the searchBar input and iterates through all event headers on the page.
  * Returns Result objects and appends them to results array.
  */
  timelineSearch() {

    this.searchQuery = this.searchBar.value.toLowerCase();

    // Check if old results are still valid
    this.resultsCheck(this.searchQuery);

    // Reset scroll to index, ready for new search results
    this.scrollIndex = 0;

    // Clear results and end operation if searchbar cleared
    if (this.searchQuery.length == 0){

      // Reset styling for each month block
      this.months.forEach(month => {
        month.resetStyles();
      });
      // Clear all existing search attributes
      this.months = [];
      this.results = [];
      this.updateUI();
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
        editPage: this.editPage
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
            missingEventContainer: dayContainer.querySelector(".missing-event-area"),
          },
          dayLine: dayContainer.querySelector(".day-line"),
          events: [],
          daysBelow: false,
          containsPositiveEvent: false,
          dayHasMissingEvent: false,
          editPage: this.editPage
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

          // Get event-between container if it exists on the page (timeline edit page only)
          try {
            var betweenEvents = eventHeaders[headerIndex].closest('.timeline-day-container')
            .nextElementSibling.querySelector(".event-between");
            var lineLower = betweenEvents.previousElementSibling;
            if (!betweenEvents.classList.contains("event-between")) {
              betweenEvents = null;
              lineLower = null;
            }
          }
          catch (error) {
            betweenEvents = null;
            lineLower = null;
          }


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
              betweenEvents: betweenEvents, 
              lineLower: lineLower,
            },
            editPage: this.editPage
          })

          // Compare searchQuery against event header text
          if (elementText.includes(this.searchQuery)) {

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
      // Update UI counter
      this.updateUI();
    });
  }


  /**
  * Method to iterate through all current results objects in this.results
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


  /**
  * Method to update ui hits counter
  */
  updateUI() {
    if (this.searchQuery.length == 0) {
      this.hitsCounter.innerText = this.initialValue;
    }
    else {
      this.hitsCounter.innerText = `${this.results.length} EVENTS`;
    }
  }

  /**
  * Method to scroll through any results.
  * Called via event listener.
  */
  scrollToResults() {

    if (this.results.length === 0) {
      // No results
      return; 
    }

    if (this.scrollIndex >= this.results.length) {
      // Reset index if reached the end
      this.scrollIndex = 0; 
    }

    const element = this.results[this.scrollIndex];
    // Scroll to element
    element.scrollTarget.scrollIntoView(); 
    this.hitsCounter.innerText = `${this.scrollIndex + 1} OF ${this.results.length} EVENTS`;

    // Increment the index for the next call
    this.scrollIndex++; 
  }

}
