export class SortToggle {
  constructor({
    dateButton,
    titleButton,
  })
  {
    this.csrfToken = document.getElementById("sort-toggles").dataset.csrfToken;
    this.URL = document.getElementById("sort-toggles").dataset.url;
    this.initialValue = document.getElementById("sort-toggles").dataset.initialValue;

    this.dateButton = document.getElementById(dateButton);
    this.dateButton.addEventListener("click", () => {
      this.UncheckInputs();
      this.Toggle(this.dateButton);
      this.UpdateSessionVariable(this.dateButton.dataset.storageValue);
    });

    this.titleButton = document.getElementById(titleButton);
    this.titleButton.addEventListener("click", () => {
      this.UncheckInputs();
      this.Toggle(this.titleButton);
      this.UpdateSessionVariable(this.titleButton.dataset.storageValue);
    });

    this.InitialiseToggleState();
  }

  InitialiseToggleState() {
    
    this.UncheckInputs();
    if (this.initialValue == "last_edited") {
      this.Toggle(this.dateButton);
    }
    else {
      this.Toggle(this.titleButton);
    }
  }

  UncheckInputs() {
    this.dateButton.checked = false;
    this.titleButton.checked = false;
    this.dateButton.parentElement.style.backgroundColor = "";
    this.titleButton.parentElement.style.backgroundColor = "";
  }

  Toggle(button) {
    button.checked = !button.checked;
    if (button.checked) {
      button.parentElement.style.backgroundColor = "var(--elem_dark)";
    }
    else {
      button.parentElement.style.backgroundColor = "var(--elem_dark)";
    }
  }

  UpdateSessionVariable(storageValue) {

    const formData = new FormData();
    formData.append("sort_preference", storageValue);

    fetch(this.URL, {
      method: "POST",
      headers: {
        "X-CSRF-TOKEN": this.csrfToken,
      },
      body: formData
    })
    .then((response)=>{ 
      if (response.status == 200) {
        window.location.reload();
      }
    })
  }
}
