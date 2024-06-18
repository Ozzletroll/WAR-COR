export class Tooltip{
    constructor({
      parentButton,
      tooltip,
      mode
    }) {
      this.parentButton = parentButton;
      this.tooltip = tooltip;
      this.mode = mode;

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
      if (this.mode == "flex") {
        this.tooltip.style.display = "flex";
      }
      else if (this.mode == "visibility") {
        this.tooltip.style.visibility = "visible";
        this.tooltip.style.animation = "fadein 1s ease-out 0s 1 forwards";
        this.tooltip.style.WebkitAnimation = "fadein 1s ease-out 0s 1 forwards";  
      }
    }
  
    closeTooltip() {
      if (this.mode == "flex") {
        this.tooltip.style.display = "none";
      }
      else if (this.mode == "visibility") {
        this.tooltip.style.visibility = "hidden";
        this.tooltip.style.animation = "";
        this.tooltip.style.WebkitAnimation = "";  
      }
    }
  }
  