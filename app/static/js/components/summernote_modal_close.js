window.addEventListener('DOMContentLoaded', function() {
  const summernoteModals = document.getElementsByClassName("note-modal");
  
  Array.from(summernoteModals).forEach(modal => {
    var modalCloseButton = modal.querySelector(".close");
    modal.addEventListener("click", (event) => {
        if (event.target.classList.contains("note-modal")) {
            closeModal(modalCloseButton);
        }
    });
  });
  
  function closeModal(modalCloseButton) {
      modalCloseButton.click();
  }
})
