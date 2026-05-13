PET_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer"
        },
        "name": {
            "type": "string"
        },
        "category": {
            "id": {
                "type": "integer"
            },
            "name": {
                "type": "string"
            }
        },
        "photoUrls": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            },
        "tags": {
                "type": "array",
                "items": {
                    "id": {
                        "type": "string"
                    },
                    "name": {
                        "type": "string"
                    }
                }
            },
        "status": {
                "type": "string",
                "enum": [
                    "available",
                    "pending",
                    "sold"
                ]
            }
        },
    "required": ["id", "name", "photoUrls", "status"],
    "additionalProperties": False
}
