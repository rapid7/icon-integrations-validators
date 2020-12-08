
from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException
import yaml


class EncodingValidator(KomandPluginValidator):

    @staticmethod
    def validate_encoding(spec_dict):
        for key, value in spec_dict.items():
            if not isinstance(value, dict):
                EncodingValidator.compare_encodings(key, value)
            else:
                sub_yaml = yaml.safe_load(str(value))
                EncodingValidator.validate_encoding(sub_yaml)

    @staticmethod
    def compare_encodings(key, value):
        unicode_string = str(value)
        decoded_string = unicode_string.encode("ascii", "ignore").decode("utf-8")
        if unicode_string != decoded_string:
            raise ValidationException(f"A forbidden character was found in the '{key}' field of the spec.yaml file: {value}")

    def validate(self, spec):
        EncodingValidator.validate_encoding(spec.spec_dictionary())
