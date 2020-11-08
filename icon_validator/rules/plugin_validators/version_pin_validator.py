import re
import os

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class VersionPinValidator(KomandPluginValidator):

    @staticmethod
    def read_schema(spec):
        with open(os.path.join(spec.directory, "requirements.txt")) as requirements:
            return requirements.read().strip()

    def validate(self, spec):
        requirements_text = self.read_schema(spec).split("\n")
        for requirements_text_one_element in requirements_text:
            if requirements_text_one_element.startswith("#"):
                continue
            if not re.match(r'[^=]*?==[^=]*?', requirements_text_one_element):
                raise ValidationException(
                    "All Python dependencies must be version pinned. "
                    "Please update all modules in requirements.txt with a specific version pin e.g. lxml==3.7.1"
                )
