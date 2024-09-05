// Base class for all layouts
export class Layout {
    constructor({
      localStorageName,
      button,
      minAllowedScreenWidth
    })
    {
      this.layoutManager;
      this.localStorageName = localStorageName;
      this.button = button;
      this.minAllowedScreenWidth = minAllowedScreenWidth;
      this.allButtons = document.querySelectorAll(".campaign-view-toggle .radio");
      this.button.addEventListener("click", () => {
        localStorage.setItem("campaignLayout", this.localStorageName);
        this.layoutManager.storedLayout = this;
        this.layoutManager.setLayout(this);
      });
      this.resetButtonStyle();
    }
  
    resetButtonStyle() {
      this.allButtons.forEach(button => {
        button.parentElement.style.backgroundColor = "";
      })
    }
  
    applyButtonStyle() {
      this.button.checked = true;
      this.button.parentElement.style.backgroundColor = "var(--elem_dark)";
    }
  
    applyLayoutStyle() {
      // This is overridden by individual layouts
    }
  }
