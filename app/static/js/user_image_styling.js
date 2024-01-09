function formatImageElements(selector) {
  const elements = document.querySelectorAll(selector);
  let imageCount = 0;

  elements.forEach((element) => {
    if (element.querySelector("img")) {
      imageCount++;

      // Create surrounding element
      const newDiv1 = document.createElement("div");
      newDiv1.classList.add("user-image-area");

      // Wrap the element within the new div
      element.parentNode.insertBefore(newDiv1, element);
      newDiv1.appendChild(element);

      // Create surrounding element
      const newDiv2 = document.createElement("div");
      newDiv2.classList.add("user-image-elem");
      newDiv2.classList.add("campaign-image-elem");

      // Wrap the element within the new div
      element.parentNode.insertBefore(newDiv2, element);
      newDiv2.appendChild(element);

      // Centre img elements in user submitted p elements
      element.style.display = "flex";
      element.style.justifyContent = "center";
      element.style.margin = "0";
    }
  });
}