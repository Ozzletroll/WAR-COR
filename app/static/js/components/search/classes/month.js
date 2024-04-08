const fadeValue = "30%";


export class Month {
    constructor({
      element,
      days,
      containsPositiveResult,
      editPage
    }) {
      this.element = element;
      this.days = days;
      this.containsPositiveResult = containsPositiveResult;
      this.editPage = editPage;
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
