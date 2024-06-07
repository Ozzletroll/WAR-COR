const fadeValue = "30%";

export class HTMLResult {
  constructor({
    baseElement,
    textElement,
  }) {
    this.positive = false;
    this.baseElement = baseElement;
    this.textElement = textElement;
    this.initialHTML = this.textElement.innerHTML;
    this.queryMatches = [];
  }

  stylePositive(searchQuery) {
    // Handle basic event page elements
    if (this.textElement.classList.contains("event-elem-body")
    || this.textElement.classList.contains("event-input")) {
      this.queryMatches.push(this.baseElement);
    }
    // Handle composite/belligerents fields
    else if (this.textElement.classList.contains("belligerents-container")) {
      this.queryMatches.push(this.baseElement);
    }
    // Handle user submitted html elements
    else {
      this.initialHTML = this.textElement.innerHTML;
      var selector = `
      .event-desc > h1,
      .event-desc > h2,
      .event-desc > h3,
      .event-desc > p,
      .event-desc > ul > li,
      .event-desc > ol > li,
      .note-editable > h1,
      .note-editable > h2,
      .note-editable > h3,
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
        element.childNodes.forEach(childNode => {
          // Handle text nodes
          if (childNode.nodeType === Node.TEXT_NODE) {
            
            var replacedText = this.replaceText("text", childNode, searchQuery);
      
            // Create a new element and set its innerHTML to the replaced text
            const newElement = document.createElement("span");
            newElement.innerHTML = replacedText;
      
            // Replace the text node with the new element
            childNode.replaceWith(newElement);
          }
          // Handle other elements
          else if (childNode.nodeType === Node.ELEMENT_NODE) {
            // Search within underline, italic and bold elements
            if (["U", "I", "B", "A"].includes(childNode.nodeName)) {
              // Exclude elements with no text
              if (childNode.textContent.trim() !== "") {
                childNode.innerHTML = this.replaceText("html", childNode, searchQuery);
              }
            }
          }
        });
      
        // Get all newly created search highlighted elements 
        // and push them to the queryMatches array
        var searchHighlights = element.querySelectorAll(".search-highlight");
        searchHighlights.forEach((element) => {
          this.queryMatches.push(element);
        });
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

  replaceText(type, textElement, searchQuery) {
    // Create a regular expression with the "gi" flags (global, case-insensitive)
    const regex = new RegExp(searchQuery, "gi");
      
    // Determine the type of content to replace
    var content = type === "html" ? textElement.innerHTML : textElement.textContent;
      
    // Replace all matching instances with the wrapped version
    var replacedText = content.replace(regex, (match) => {
      return `<strong class="search-highlight">${match}</strong>`;
    });

    // Update the content based on the type
    if (type === "html") {
      textElement.innerHTML = replacedText;
    } else {
      textElement.textContent = replacedText;
    }

    return replacedText;
  }
}
