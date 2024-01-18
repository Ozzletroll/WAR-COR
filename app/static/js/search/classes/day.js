const fadeValue = "30%";


export class Day {
    constructor({
      elements,
      dayLine,
      events,
      daysBelow,
      containsPositiveResult,
      editPage
    }) {
      this.elements = elements;
      this.dayLine = dayLine;
      this.events = events;
      this.daysBelow = daysBelow;
      this.containsPositiveResult = containsPositiveResult;
      this.editPage = editPage;
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
  
        if (this.editPage == true) {
          this.dayLine.style.opacity = "";
        }
        else {
          this.dayLine.style.opacity = fadeValue;
        }
      }
  
      // Set day block opacity to 50% if it contains no positive results
      if (this.containsPositiveResult == false) {
        this.elements["rightBranchLabel"].style.opacity = fadeValue;
        this.elements["eventGroupContainer"].style.opacity = fadeValue;
  
        if (this.elements["missingEventContainer"] != null) {
          this.elements["missingEventContainer"].style.opacity = fadeValue;
        }
      }
  
  
      // If day block contains positive results, style each result accordingly
      if (this.containsPositiveResult == true) { 
  
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
  
      if (this.elements["missingEventContainer"] != null) {
        this.elements["missingEventContainer"].style.opacity = "";
      }
  
      if (this.dayLine != null) {
        this.dayLine.style.opacity = "";
      }
  
      this.events.forEach(result => {
        result.styleReset();
      });
    }
  
  }
