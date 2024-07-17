export class LayoutManager {
  constructor({
    layoutLocalStorage,
    layouts
  })
  {
    this.layouts = layouts;
    this.currentLayout = this.getLayout(JSON.parse(localStorage.getItem(layoutLocalStorage)) || "list");
    this.setLayout(this.currentLayout);
  }

  initialiseLayout() {
    console.log(this.currentLayout)
  }

  setLayout(layout) {
    layout.applyLayoutStyle();
  }

  getLayout(layoutName) {
    for (let layout of this.layouts) {
      if (layout.localStorageName == layoutName) {
        return layout;
      }
      else {
        return null;
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
    this.button.addEventListener("click", () => {
      this.applyLayoutStyle();
    });
  }

  applyLayoutStyle() {}
}


export class ListLayout extends Layout {

  applyLayoutStyle() {
    console.log("APPLIED LIST STYLE");
  }

}

export class GridLayout extends Layout {

  applyLayoutStyle() {
    console.log("APPLIED GRID STYLE");
  }

}

