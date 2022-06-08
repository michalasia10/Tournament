import jsonschema
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import BaseValidator
from jsonschema.exceptions import ValidationError as JsonValidationError


class JSONMatchSchemaValidator(BaseValidator):
    def compare(self, value, schema):
        try:
            jsonschema.validate(value, schema)
        except JsonValidationError:
            raise DjangoValidationError(f"({value} field JSON schema check)")
