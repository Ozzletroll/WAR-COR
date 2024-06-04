# JSON validation schemas
COMPOSITE_FIELD_SCHEMA =  {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "position": {"type": "string"},
            "entries": {
                "type": "array",
                "items": {
                    "type": "string",
                },
            },
        },
        "required": ["title", "position", "entries"],
    },
}

TEMPLATE_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "value": {"type": ["string", "null"]},
            "field_type": {"type": "string"},
            "is_full_width": {"type": ["boolean", "null"]},
        },
        "required": ["title", "value", "field_type"],
    },
}
