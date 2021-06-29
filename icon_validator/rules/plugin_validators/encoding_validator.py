
from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException
import yaml


class EncodingValidator(KomandPluginValidator):
    validator_errors = []

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

        wrong_characters = unicode_string
        for decoded in set(decoded_string):
            wrong_characters = wrong_characters.replace(decoded, '')

        if unicode_string != decoded_string:
            EncodingValidator.validator_errors.append(f"A forbidden character(s) was found in the '{key}' field of the spec.yaml file: {set(wrong_characters)}")

    def validate(self, spec):
        EncodingValidator.validator_errors = []
        EncodingValidator.validate_encoding(spec.spec_dictionary())
        if EncodingValidator.validator_errors:
            raise ValidationException("\n\t\t".join(EncodingValidator.validator_errors))
