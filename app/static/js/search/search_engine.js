import { Result } from './classes/result.js';
import { HTMLResult } from './classes/html_result.js';
import { Day } from './classes/day.js';
import { Month } from './classes/month.js';


export class SearchEngine {
  constructor(searchBar, hitsCounter, editPage, initialValue, type) {
    this.searchBar = searchBar;
    this.hitsCounter = hitsCounter;
    this.results = [];
    this.htmlResults = [];
    this.matchingElements = [];
    this.months = [];
    this.searchQuery = this.searchBar.value.toLowerCase();
    this.scrollIndex = 0;
    this.editPage = editPage;
    this.initialValue = initialValue;
    this.type = type;
  }

  /**
  * Timeline page search method
  * Takes the searchBar input and iterates through all event headers on the page.
  * Returns Result objects and appends them to results array.
  */
  timelineSearch() {

    this.searchQuery = this.searchBar.value.toLowerCase();
    this.resultsCheck(this.searchQuery);
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

    // Iterate through all month-outer elements
    var monthOuters = document.getElementsByClassName("month-outer");
    for (var outerIndex = 0; outerIndex < monthOuters.length; outerIndex++) {

      // Get the current month-outer element
      var monthOuter = monthOuters[outerIndex];
      var month = new Month({
        element: monthOuter,
        days: [],
        containsPositiveResult: false,
        editPage: this.editPage
      })

      // Get all the days within the month and iterate through them
      var days = monthOuter.querySelectorAll(".timeline-day-outer");
      for (var dayIndex = 0; dayIndex < days.length; dayIndex++) {

        var dayContainer = days[dayIndex];
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

        // Iterate through all event-header elements within day
        var eventHeaders = dayContainer.querySelectorAll(".event-header");
        for (var headerIndex = 0; headerIndex < eventHeaders.length; headerIndex++) {
          var eventHeader = eventHeaders[headerIndex];
          var elementText = eventHeader.innerText.toLowerCase();
          
          // Get elements for result styling
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
            // If not already present, append new result object to searchEngine result array
            var exists = this.results.some(result => result.elementText === elementText);
            if (!exists) {
              // 
              this.results.push(result)
            }
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
    this.updateUI();
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
      this.htmlResults.forEach(result => {
        result.styleReset();
      });
      // Clear all existing search attributes
      this.htmlResults = [];
      this.scrollIndex = 0;
      this.updateUI();
      return;
    }

    this.htmlResults = []

    if (this.editPage == false) {
      // Get event and epoch page fields and create result object for each if they exist on page
      var element = document.querySelector(".event-location");
      if (element) {
        var eventLocation = new HTMLResult({
          baseElement: ".event-location",
          textElement: ".event-elem-body",
        });
        this.htmlResults.push(eventLocation);
      }

      var element = document.querySelector(".event-belligerents");
      if (element) {
        var eventBelligerents = new HTMLResult({
          baseElement: ".event-belligerents",
          textElement: ".event-elem-body"
        });
        this.htmlResults.push(eventBelligerents);
      }

      var element = document.querySelector(".event-page-description");
      if (element) {
        var eventDesc = new HTMLResult({
          baseElement: ".event-page-description",
          textElement: ".event-desc"
        });
        this.htmlResults.push(eventDesc);
      }

      var element = document.querySelector(".event-page-result");
      if (element) {
        var eventResults = new HTMLResult({
          baseElement: ".event-page-result",
          textElement: ".event-elem-body"
        });
        this.htmlResults.push(eventResults);
      }

      var element = document.querySelector(".epoch-events-container");
      if (element) {
        var epochResults = new HTMLResult({
          baseElement: ".epoch-events-container",
          textElement: ".epoch-events-list"
        });
        this.htmlResults.push(epochResults);
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
          var newResultObject = new HTMLResult({
            baseElement: field,
            textElement: ".event-input",
          });
          this.htmlResults.push(newResultObject);
        }
      })

      var element = document.querySelector(".note-editor");
      if (element) {
        var newResultObject = new HTMLResult({
          baseElement: ".note-editor",
          textElement: ".note-editable",
        });
        this.htmlResults.splice(5, 0, newResultObject);
      }
    }

    this.resultsCheck();
    this.applyStyles();
    this.populateMatchingElements();
    this.updateUI();
  
  }

  applyStyles() {
    if (this.type == "timeline") {
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
    else if (this.type == "event") {
      this.htmlResults.forEach((result, index) => {
        result.styleReset();
        if (result.positive) {
          result.stylePositive(this.searchQuery);
        }
        else {
          result.styleNegative();
        }
      });
    }
  }

  /**
  * Method to iterate through all current results objects in this.results
  * and remove ones that no longer match the search query.
  */
  resultsCheck(searchQuery) {
    if (this.type == "timeline") {
      this.results.forEach((result, index) => {
        // Remove result if it no longer matches the search query string
        if (!result.elementText.includes(searchQuery)) {
          this.results = this.results.splice(index, index)
        }
      });
    }
    else if (this.type == "event") {
      this.htmlResults.forEach((result, index) => {
        result.styleReset();
        if (this.editPage == false) {
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
  }


  populateMatchingElements() {
    this.matchingElements = [];
    this.htmlResults.forEach((result, index) => {
      result.queryMatches.forEach((element) => {
        this.matchingElements.push(element);
      });
    });
  }

  /**
  * Method to update ui hits counter
  */
  updateUI() {
    if (this.type == "timeline") {
      if (this.searchQuery.length == 0) {
        this.hitsCounter.innerText = this.initialValue;
      }
      else {
        if (this.results.length == 1) {
          this.hitsCounter.innerText = `${this.results.length} RESULT`;
        }
        else {
          this.hitsCounter.innerText = `${this.results.length} RESULTS`;
        }
      }
    }
    else if (this.type == "event") {
      var positiveResults = this.htmlResults.filter(htmlResult => htmlResult.positive);
      var totalMatches = 0;
      positiveResults.forEach((result, index) => {
        totalMatches += result.queryMatches.length;
      });
  
      if (this.searchQuery.length == 0) {
        this.hitsCounter.innerText = this.initialValue;
      }
      else {
        this.hitsCounter.innerText = `${totalMatches} RESULTS`;
      }
    }
  }

  /**
  * Method to scroll through any results.
  * Called via event listener.
  */
  scrollToResults() {
    var totalResults = this.results.length + this.matchingElements.length;

    if (totalResults === 0) {
      // No results
      return; 
    }
    if (this.scrollIndex >= totalResults) {
      // Reset index if reached the end
      this.scrollIndex = 0; 
    }
    var allResults = this.matchingElements.concat(this.results);
    const element = allResults[this.scrollIndex];
    // Scroll to element
    if (element instanceof Result) {
      element.scrollTarget.scrollIntoView(); 
    }
    else {
      element.scrollIntoView();
    }

    if (totalResults == 1) {
      this.hitsCounter.innerText = `${this.scrollIndex + 1} OF ${totalResults} RESULT`;
    }
    else {
      this.hitsCounter.innerText = `${this.scrollIndex + 1} OF ${totalResults} RESULTS`;
    }

    // Increment the index for the next call
    this.scrollIndex++; 
  }

  // Method to clear search input and remove all applied result styling
  // Called when closing searchbar tab, interacting with the event desc input field,
  // or submitting the form
  clearSearch() {
    this.searchBar.value = "";
    this.searchBar.blur();
    this.htmlResults.forEach((result, index) => {
      result.styleReset();
    });
    this.htmlResults = [];
    this.updateUI();
    console.log("CALLED")
  }

  // Method called when input detected in description field
  // Updates the description field result object's stored inital value
  updateDescription() {
    this.htmlResults.forEach((result, index) => {
      if (index == 5) {
        result.initialHTML = result.textElement.innerHTML;
      }
    });
  }
}
