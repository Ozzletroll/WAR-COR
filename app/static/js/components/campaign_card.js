export class CampaignCard {
    constructor({
      tab,
      button,
    }) {
      this.tab = tab;
      this.button = button;
      this.state = false;
  
      const handleClick = event => {
        var screenWidth = window.innerWidth || document.documentElement.clientWidth;
        if (screenWidth <= 500) {
          if (this.state == false) {
            this.openTab(event)
          } 
          else {
            this.closeTab(event)
          }
        }
      }
  
      this.button.addEventListener("click", handleClick);
      this.button.addEventListener('keydown', event => {
        // Handle enter key
        if (event.keyCode === 13) {
          handleClick(event);
        }
      });
    }
    
    openTab() {
      this.tab.style.display = "flex";
      this.tab.style.maxHeight = "fit-content";
      this.button.style.borderBottomLeftRadius = "0px";
      this.button.style.borderBottomRightRadius = "0px";
      this.state = true
    }
  
    closeTab() {
      this.tab.style.maxHeight = "0";
      this.tab.style.display = "none";
      this.button.style.borderBottomLeftRadius = "5px";
      this.button.style.borderBottomRightRadius = "5px";
      this.state = false;
    }
  
    checkStatus() {
      var screenWidth = window.innerWidth || document.documentElement.clientWidth;
      if (screenWidth >= 500) {
        this.button.setAttribute("role", "generic");
        this.button.setAttribute("tabIndex", "-1");
      }
      else {
        this.button.setAttribute("role", "button");
        this.button.setAttribute("tabIndex", "0");
      }
    }
  
  }