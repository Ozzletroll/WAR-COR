export function addHeaderIdMarker(element) {

  var fieldId = element.id;
  var headers = element.querySelectorAll("h1, h2, h3");
  
  for (let index = 0; index < headers.length; index++) {
    headers[index].classList.add(`${fieldId}-header-${index + 1}`)
  }
}
