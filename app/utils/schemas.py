# JSON validation schemas

# Schema for composite field groups and entries
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

# Schema for main dynamic fields
DYNAMIC_FIELD_SCHEMA =  {
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
                "title": { "type": "string" },
                "description": { "type": "string" },
                "image_url": { "type": "string" },
                "date_suffix": { "type": "string" },
                "negative_date_suffix": { "type": "string" },
                "system": { "type": "string" }
            },
            "required": ["title", "description"]
        },
        "events": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": { "type": "string" },
                    "title": { "type": "string" },
                    "date": { "type": "string" },
                    "hide_time": { "type": "boolean" },
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
                    "title": { "type": "string" },
                    "start_date": { "type": "string" },
                    "end_date": { "type": "string" },
                    "overview": { "type": "string" },
                    "dynamic_fields": DYNAMIC_FIELD_SCHEMA,
                },
                "required": ["title", "start_date", "end_date"]
            }
        }
    },
    "required": ["campaign_data", "events", "epochs"]
}
