import bleach
from bleach.css_sanitizer import CSSSanitizer
from bs4 import BeautifulSoup


def sanitise_input(value, allow_images=True, message_body=False):
    """ Method to sanitise user submitted html input. Uses Bleach
        and CSSSanitizer. """

    allowed_tags = ["p", "b", "i", "em", "h1", "h2", "h3", "a", "br", "u", "img", "li", "ul", "ol", "strong"]
    if not allow_images:
        allowed_tags.remove("img")
        
    allowed_attrs = {
        "*": ["class"],
        "a": ["href", "rel"],
        "img": ["alt", "src", "style"],
        "p": ["align", "style"],
    }
    allowed_styles = ["height", "width", "margin-left"]

    value = bleach.clean(value,
                         tags=allowed_tags,
                         attributes=allowed_attrs,
                         css_sanitizer=CSSSanitizer(allowed_css_properties=allowed_styles))

    # Wrap any text without tags in <p> tags
    # Not applicable for message body text
    if not message_body:
        soup = BeautifulSoup(value, "html.parser")
        for text in soup.find_all(string=True):
            if text.parent.name not in allowed_tags:
                new_tag = soup.new_tag("p")
                text.wrap(new_tag)
        return str(soup)
    else:
        return value
    