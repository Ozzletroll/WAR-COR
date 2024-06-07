# JSON validation schemas

# Schema for composite field groups and entries
COMPOSITE_FIELD_SCHEMA = {
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

# Schema for main dynamic fields
DYNAMIC_FIELD_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "field_type": {"type": "string"},
            "is_full_width": {"type": "boolean"},
            "title": {"type": "string"},
            "value": {
                "oneOf": [
                    COMPOSITE_FIELD_SCHEMA,
                    {
                        "type": "string",
                    }
                ],
            },
        },
        "required": ["field_type", "is_full_width", "value", "title"],
    },
}

# Schema for template field structure data
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

# Schema for campaign backups
BACKUP_SCHEMA = {
    "type": "object",
    "properties": {
        "campaign_data": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "description": {"type": "string"},
                "image_url": {"type": ["string", "null"]},
                "date_suffix": {"type": ["string", "null"]},
                "negative_date_suffix": {"type": ["string", "null"]},
                "system": {"type": ["string", "null"]}
            },
            "required": ["title", "description"]
        },
        "events": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {"type": ["string", "null"]},
                    "title": {"type": ["string", "null"]},
                    "date": {"type": ["string", "null"]},
                    "hide_time": {"type": ["boolean", "null"]},
                    "dynamic_fields": DYNAMIC_FIELD_SCHEMA,
                },
                "required": ["type", "title", "date"]
            }
        },
        "epochs": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": ["string", "null"]},
                    "start_date": {"type": ["string", "null"]},
                    "end_date": {"type": ["string", "null"]},
                    "overview": {"type": ["string", "null"]},
                    "dynamic_fields": DYNAMIC_FIELD_SCHEMA,
                },
                "required": ["title", "start_date", "end_date"]
            }
        }
    },
    "required": ["campaign_data", "events", "epochs"]
}
