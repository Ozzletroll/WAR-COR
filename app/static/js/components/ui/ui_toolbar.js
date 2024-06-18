import { Tooltip } from "./tooltip.js";


export class Toolbar {
  constructor()
  {
    this.buttons = document.getElementsByClassName("toolbar-button");
    this.tooltips = this.bindTooltips();
  }

  bindTooltips() {
    var buttons = this.buttons;
    var tooltips = [];
    Array.from(buttons).forEach(button => {
      var newTooltip = new Tooltip({
        parentButton: button,
        tooltip: document.getElementById(button.getAttribute("aria-describedby")),
        mode: "visibility"
      })
      tooltips.push(newTooltip);
    })

    return tooltips;
  }
}
