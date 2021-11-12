import re
import os

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class VersionPinValidator(KomandPluginValidator):

    @staticmethod
    def read_requirements(spec):
        try:
            with open(os.path.join(spec.directory, "requirements.txt")) as requirements:
                return requirements.read().strip()
        except FileNotFoundError:
            raise ValidationException("requirements.txt not found. Please be sure to include this file in your plugin directory.")

    def validate(self, spec):
        requirements_text = self.read_requirements(spec).split("\n")
        for requirements_text_elements in requirements_text:
            requirements_text_elements = requirements_text_elements.strip()
            if requirements_text_elements.startswith("#"):
                continue
            for requirements_text_one_element in requirements_text_elements.split(","):
                requirements_text_one_element = requirements_text_one_element.strip()
                if not requirements_text_one_element.startswith("git+") and not re.match(r'.*?(==|===|<|<=|!=|>=|>|~=).*?', requirements_text_one_element):
                    raise ValidationException(
                        "All Python dependencies must be version pinned. "
                        "Please update all modules in requirements.txt with a specific version pin e.g. lxml==3.7.1"
                    )
