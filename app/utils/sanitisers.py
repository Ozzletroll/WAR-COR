import bleach
from bleach.css_sanitizer import CSSSanitizer


def sanitise_input(value):
    """ Method to sanitise user submitted html input. Uses Bleach
        and CSSSanitizer. """
    
    allowed_tags = ["p", "b", "i", "em", "h1", "h2", "h3", "a", "br", "u", "img", "li", "ul", "ol"]
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
    
    return value
