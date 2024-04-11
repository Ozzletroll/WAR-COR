import bleach
from bleach.css_sanitizer import CSSSanitizer
from bs4 import BeautifulSoup


def sanitise_input(value, allow_images=True):
    """ Method to sanitise user submitted html input. Uses Bleach
        and CSSSanitizer. """

    allowed_tags = ["p", "b", "i", "em", "h1", "h2", "h3", "a", "br", "u", "img", "li", "ul", "ol"]
    if not allow_images:
        allowed_tags.remove("img")
        
    allowed_attrs = {
        "*": ["class"],
        "a": ["href", "rel"],
        "img": ["alt", "src", "style"],
        "p": ["align", "style"],
    }
    allowed_styles = ["height", "width", "margin-left"]

    css_sanitiser = CSSSanitizer(allowed_css_properties=allowed_styles)
    value = bleach.clean(value,
                         tags=allowed_tags,
                         attributes=allowed_attrs,
                         css_sanitizer=css_sanitiser)

    # Wrap any text without tags in <p> tags
    soup = BeautifulSoup(value, "html.parser")
    for text in soup.find_all(string=True):
        if text.parent.name not in allowed_tags:
            new_tag = soup.new_tag("p")
            text.wrap(new_tag)

    return str(soup)
