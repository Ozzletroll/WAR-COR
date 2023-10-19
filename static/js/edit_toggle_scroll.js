function getCentralElement() {
  // Get screen dimensions and calculate "centre" coordinates. 
  // The "centre" here actually targets the top 1/3rd of the screen,
  // matching the average scrollMarginTop value for the page elements.
  const screenWidth = window.innerWidth || document.documentElement.clientWidth;
  const screenHeight = window.innerHeight || document.documentElement.clientHeight;
  const screenTarget = {
    x: Math.floor(screenWidth / 2),
    y: Math.floor(screenHeight / 3)
  };

  // Get all potential scroll target elements on page, removing ones with no id
  let elementList = Array.from(document.querySelectorAll(".timeline-event .timeline-event, .epoch-container, .timeline-year-header, .campaigns-heading, .campaign-overview, .last-edited-area"))
  .filter(element => element.id !== "");  

  let closestElement = null;
  let closestDistance = Number.MAX_SAFE_INTEGER;

  // For each element, check if it is closest to centre of screen
  elementList.forEach(function(element) {
    const rect = element.getBoundingClientRect();
    const elementCentre = {
      x: Math.floor(rect.left + rect.width / 2),
      y: Math.floor(rect.top + rect.height / 2)
    };
    
    const distance = Math.abs(elementCentre.y - screenTarget.y);

    // Update closest element variable
    if (distance < closestDistance) {
      closestElement = element;
      closestDistance = distance;
    }
  });

  return closestElement;
}


function setScrollTarget(targetURL, csrfToken, destinationURL) {

  targetElement = getCentralElement();

  // Send fetch request to target url
  fetch(targetURL, {
    method: "POST",
    headers: {
      "X-CSRF-TOKEN": csrfToken,
      "Content-Type": 'application/json',
    },
    body : JSON.stringify({"target": targetElement.id}),
  })
  // Once the fetch request completes, proceed to the new page
  .finally(() => {
    window.location.href = destinationURL;
  });
}
