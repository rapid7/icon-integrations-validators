import re

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException
import requests


class SupportedVersionValidator(KomandPluginValidator):

    @staticmethod
    def validate_spec(spec):
        if "supported_versions" not in spec.spec_dictionary():
            raise ValidationException("Plugin supported_versions is missing.")
        if not isinstance(spec.spec_dictionary()["supported_versions"], list):
            raise ValidationException("Plugin supported_versions does not contain a list of values.")
        if len(spec.spec_dictionary()["supported_versions"]) == 0:
            raise ValidationException("Plugin supported_versions list does not contain values.")

    def validate(self, spec):
        SupportedVersionValidator.validate_spec(spec)
