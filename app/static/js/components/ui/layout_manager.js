export class LayoutManager {
  constructor({
    layoutLocalStorage,
    layouts
  })
  {
    this.layouts = layouts;
    var currentLayoutName = localStorage.getItem(layoutLocalStorage) || "list"
    this.currentLayout = this.getLayout(currentLayoutName);
    this.setLayout(this.currentLayout);
  }

  setLayout(layout) {
    layout.resetButtonStyle();
    layout.applyButtonStyle();
    layout.applyLayoutStyle();
  }

  getLayout(layoutName) {
    for (let layout of this.layouts) {
      if (layout.localStorageName == layoutName) {
        return layout;
      }
    }
  }
}


class Layout {
  constructor({
    localStorageName,
    button,
  })
  {
    this.localStorageName = localStorageName;
    this.button = button;
    this.allButtons = document.querySelectorAll(".radio");
    this.button.addEventListener("click", () => {
      this.resetButtonStyle();
      this.applyButtonStyle();
      this.applyLayoutStyle();
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
    
  }
}


export class ListLayout extends Layout {

  applyLayoutStyle() {
    localStorage.setItem("campaignLayout", "list");
  }

}

export class GridLayout extends Layout {

  applyLayoutStyle() {
    localStorage.setItem("campaignLayout", "grid");
  }

}

