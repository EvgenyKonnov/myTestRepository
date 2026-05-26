STORE_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer"
        },
        "petId": {
            "type": "integer"
        },
        "quantity": {
            "type": "integer"
        },
        "shipDate": {
            "type": "string"
        },
        "complete": {
            "type": "boolean"
        },
        "status": {
            "type": "string",
            "enum": [
                "placed",
                "approved",
                "delivered "
            ]
        }
    },
    "required": ["id", "petId", "quantity", "complete", "status"],
    "additionalProperties": False
}
