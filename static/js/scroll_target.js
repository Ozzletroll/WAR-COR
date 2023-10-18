function scrollToTarget(target_url, csrfToken) {
  // Send fetch request to target url
  fetch(target_url, {
    "method": "GET",
    "headers": {
      'X-CSRF-TOKEN': csrfToken,
    },
  })
  .then(function(response) {
    if (response.status == 200) {
      return response.json();
    }
  })
  .then(function(data) {
    if (data) {
      if (data["type"] == "relative") {

        const percentage = data["target"];

        // Get the total height of the page
        const pageHeight = document.documentElement.scrollHeight || document.body.scrollHeight;

        // Calculate the scroll position based on the percentage
        const scrollPosition = (pageHeight * percentage) / 100;

        window.scrollTo({
          top: scrollPosition,
          behavior: "instant"
        });
      }
      else if (data["type"] == "element") {
        var targetElement = document.getElementById(data["target"]);
        if (targetElement != null) {
          targetElement.scrollIntoView();
        }
      }
    }
  });
}
