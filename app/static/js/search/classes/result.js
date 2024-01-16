const fadeValue = "30%";


export class Result {
    constructor({
      positive,
      elementText, 
      outerIndex, 
      headerIndex, 
      resultsBelow, 
      scrollTarget,
      elements,
      editPage
    }) {
      this.positive = positive;
      this.elementText = elementText;
      this.outerIndex = outerIndex;
      this.headerIndex = headerIndex;
      this.resultsBelow = resultsBelow;
      this.scrollTarget = scrollTarget;
      this.elements = elements;
      this.editPage = editPage;
    }
  
    /**
      * Method to style result object
      */
    stylePositive() {
    // Reset styling for self
      this.styleReset();
      // On edit page, no additional styling required
      // Normal Page Styling
      if (this.editPage == false) {
  
        // If result has no results below it, set vertical line to fade opacity value
        if (this.resultsBelow == false) {
          this.elements["eventLine"].style.opacity = fadeValue;
        }
  
      }
    }
  
    /**
    * Method to style negative result object
    */
    styleNegative() {
      // Reset styling for self
      this.styleReset();
  
      if (this.editPage == true) {
  
        // Style downwards line if there are no results below it in the block
        if (this.resultsBelow == false) {
          this.elements["eventOutline"].style.opacity = fadeValue;
          this.elements["rightBranchLabel"].style.opacity = fadeValue;
        }
        else {
          this.elements["eventOutline"].style.opacity = fadeValue;
          this.elements["rightBranchLabel"].style.opacity = fadeValue;
        }
  
      }
      else {
  
        // Style downwards line if there are no results below it in the block
        if (this.resultsBelow == false) {
          this.elements["eventLine"].style.opacity = fadeValue;
          this.elements["eventOutline"].style.opacity = fadeValue;
          this.elements["rightBranchLabel"].style.opacity = fadeValue;
        }
        else {
          this.elements["eventLine"].style.opacity = "";
          this.elements["eventOutline"].style.opacity = fadeValue;
          this.elements["rightBranchLabel"].style.opacity = fadeValue;
        }
        
      }
  
    }
  
    styleReset() {
      this.elements["headerElement"].style.opacity = "";
      this.elements["eventOutline"].style.opacity = "";
      this.elements["eventLine"].style.opacity = "";
      this.elements["rightBranchLabel"].style.opacity = "";
  
      if (this.editPage == true) {
        if (this.elements["betweenEvents"] != null) {
          this.elements["betweenEvents"].style.opacity = "";
        }
        if (this.elements["lineLower"] != null) {
          this.elements["lineLower"].style.opacity = "";
        }
      }
    }
  
  }
