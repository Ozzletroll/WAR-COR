const fadeValue = "30%";

export class HTMLResult {
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

      elements.forEach(element => {
  
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
