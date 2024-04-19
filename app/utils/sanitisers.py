import nh3
from bs4 import BeautifulSoup


def sanitise_input(value, allow_images=True, message_body=False):
    """ Method to sanitise user submitted html input using nh3. """

    allowed_tags = {"p", "b", "i", "em", "h1", "h2", "h3", "a", "br", "u", "img", "li", "ul", "ol", "strong"}
    if not allow_images:
        allowed_tags.remove("img")

    allowed_attrs = {
        "*": {"class"},
        "a": {"href", "title", "target"},
        "img": {"alt", "src", "style"},
        "p": {"align", "style"},
    }

    cleaned_input = nh3.clean(value,
                              tags=allowed_tags,
                              attributes=allowed_attrs,
                              link_rel="noopener noreferrer nofollow")

    # Wrap any text without tags in <p> tags
    # Not applicable for message body text
    if not message_body:
        soup = BeautifulSoup(cleaned_input, "html.parser")
        for text in soup.find_all(string=True):
            if text.parent.name not in allowed_tags:
                new_tag = soup.new_tag("p")
                text.wrap(new_tag)
        return str(soup)
    else:
        return cleaned_input
