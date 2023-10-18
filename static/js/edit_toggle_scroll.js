function getScrollPercentage() {
  const scrollTop = window.scrollY;
  const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
  const percentage = (scrollTop / totalHeight) * 100;

  return percentage.toFixed(2);
};


function setScrollTarget(targetURL, csrfToken, destinationURL) {

  target = getScrollPercentage();
  console.log(target)

  // Send fetch request to target url
  fetch(targetURL, {
    method: "POST",
    headers: {
      "X-CSRF-TOKEN": csrfToken,
      "Content-Type": 'application/json',
    },
    body : JSON.stringify({"target": target}),
  })
  // Once the fetch request completes, proceed to the new page
  .finally(() => {
    window.location.href = destinationURL;
  });
}
