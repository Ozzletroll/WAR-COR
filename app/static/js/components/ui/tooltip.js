export class Tooltip{
    constructor({
      parentButton,
      tooltip,
    }) {
      this.parentButton = parentButton;
      this.tooltip = tooltip;
  
      // Mouse events
      this.parentButton.addEventListener("mouseover", this.openTooltip.bind(this))
      this.parentButton.addEventListener("mouseout", this.closeTooltip.bind(this))
      // Keyboard events
      this.parentButton.addEventListener("focus", function(event) {
        if (event.target.matches(":focus-visible")) {
          this.openTooltip();
        }
      }.bind(this));
      this.parentButton.addEventListener("blur", this.closeTooltip.bind(this))
    }
  
    openTooltip() {
      this.tooltip.style.display = "flex";
    }
  
    closeTooltip() {
      this.tooltip.style.display = "none";
    }
  }
