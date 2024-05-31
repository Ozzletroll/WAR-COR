import nh3
import json
import jsonschema
from jsonschema import validate
from bs4 import BeautifulSoup
import base64
import binascii


def sanitise_input(value, allow_images=True, allow_urls=True, wrap=True):
    """ Method to sanitise user submitted html input using nh3. """

    allowed_tags = {"p", "b", "i", "em", "h1", "h2", "h3", "a", "br", "u", "img", "li", "ul", "ol", "strong"}
    if not allow_images:
        allowed_tags.remove("img")
    if not allow_urls:
        allowed_tags.remove("a")

    allowed_attrs = {
        "*": {"class"},
        "a": {"href", "title", "target"},
        "img": {"alt", "src", "style"},
        "h1": {"align", "style"},
        "h2": {"align", "style"},
        "h3": {"align", "style"},
        "p": {"align", "style"},
    }

    cleaned_input = nh3.clean(value,
                              tags=allowed_tags,
                              attributes=allowed_attrs,
                              link_rel="noopener noreferrer nofollow")

    # Wrap any text without tags in <p> tags
    # Not applicable for message body text
    if wrap:
        soup = BeautifulSoup(cleaned_input, "html.parser")
        for text in soup.find_all(string=True):
            if text.parent.name not in allowed_tags:
                new_tag = soup.new_tag("p")
                text.wrap(new_tag)
        return str(soup)
    else:
        return cleaned_input


def sanitise_json(value):

    schema = {
    "type" : "array",
    "items": {
            "type" : "object",
            "properties" : {
                "title" : {"type" : "string"},
                "position" : {"type" : "string"},
                "entries" : {
                    "type" : "array",
                    "items": {
                        "type" : "string",
                    },
                },
            },
            "required": ["title", "position", "entries"],
        },
    }

    value = json.loads(value) 

    try:
        validate(instance=value, schema=schema)
    except jsonschema.exceptions.ValidationError as error:
        return ""

    return value


def sanitise_template_json(template_data):

    schema = {
        "type" : "array",
        "items": {
            "type" : "object",
            "properties" : {
                "title" : {"type" : "string"},
                "value" : {"type" : ["string", "null"]},
                "field_type" : {"type" : "string"},
                "is_full_width" : {"type" : ["boolean", "null"]},
            },
            "required": ["title", "value", "field_type"],
        },
    }

    try:
        validate(instance=template_data, schema=schema)
    except jsonschema.exceptions.ValidationError as error:
        return []

    return template_data


def sanitise_share_code(share_code):
    """ Method to sanitise share codes for template import. """

    # Remove leading/trailing spaces
    sanitised_code = share_code.strip()

    # Check length
    if len(sanitised_code) == 12:
        try:
            base64.urlsafe_b64decode(sanitised_code)            
            return sanitised_code
        except binascii.Error:
            return ""
    else:
        return ""
    