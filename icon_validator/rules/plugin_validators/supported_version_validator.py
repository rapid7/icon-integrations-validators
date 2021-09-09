from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class SupportedVersionValidator(KomandPluginValidator):

    @staticmethod
    def validate_spec(spec):
        sup_vers = "supported_versions"

        if sup_vers not in spec.spec_dictionary():
            raise ValidationException(f"{sup_vers} is missing from plugin.spec.yaml.")
        if not isinstance(spec.spec_dictionary()[sup_vers], list):
            raise ValidationException(f"{sup_vers} does not contain a list of values.")
        if len(spec.spec_dictionary()[sup_vers]) == 0:
            raise ValidationException(f"{sup_vers} list does not contain values.")

    def validate(self, spec):
        SupportedVersionValidator.validate_spec(spec)
