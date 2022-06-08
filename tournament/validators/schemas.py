MATCH_JSON_SCHEMA = {
    'schema': 'http://json-schema.org/draft-07/schema#',
    'type': 'object',
    'properties': {
        'team_a': {
            'type': 'object',
            "properties": {
                "score": {"type": "integer"}
            }
        },
        "team_b": {
            "type": "object",
            "properties": {
                "score": {"type": "integer"}
            }
        },
    },
    'required': ['team_a',"team_b"]
}
