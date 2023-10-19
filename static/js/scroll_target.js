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
        var targetElement = document.getElementById(data["target"]);
        if (targetElement != null) {
          targetElement.scrollIntoView({behavior: "instant"});
        }
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
