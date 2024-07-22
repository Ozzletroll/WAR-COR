export class LayoutManager {
  constructor({
    layoutLocalStorage,
    layouts,
    defaultLayout,
  })
  {
    layouts.forEach(layout => {
      layout.layoutManager = this;
    });
    this.layouts = layouts;
    this.defaultLayout = defaultLayout;
    this.storedLayout = this.getLayout(localStorage.getItem(layoutLocalStorage) || defaultLayout);
    this.selectedLayout = this.storedLayout;
    this.setLayout(this.storedLayout);

    window.addEventListener("resize", () => {
      this.checkLayoutWidth();
    });
  }

  setLayout(layout) {
    if (window.innerWidth < layout.minAllowedScreenWidth) {
      layout = this.getLayout(this.defaultLayout);
    }
    this.selectedLayout = layout;
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

  checkLayoutWidth() {
    if (window.innerWidth < this.storedLayout.minAllowedScreenWidth) {
      this.setLayout(this.getLayout(this.defaultLayout));
    }
    else {
      this.setLayout(this.storedLayout);
    }
  }
}
