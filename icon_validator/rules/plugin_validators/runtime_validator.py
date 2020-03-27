import os

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class RuntimeValidator(KomandPluginValidator):

    @staticmethod
    def validate_setup(spec):
        if "setup.py" in os.listdir(spec.directory):
            with open("setup.py", "r") as file:
                setup_str = file.read().replace("\n", "")

                if f"install_requires=['insightconnect-plugin-runtime']" not in setup_str:
                    raise ValidationException("Komand is no longer used in setup.py. "
                                              "Use insightconnect-plugin-runtime instead.")

    @staticmethod
    def validate_icon(spec):
        for subdir, dirs, files in os.walk(spec.directory):
            for file in files:
                with open(file, 'r') as open_file:
                    file_str = open_file.read().replace("\n", "")

                    if "import komand" in file_str or "FROM komand" in file_str:
                        raise ValidationException("Komand is no longer used in imports. "
                                                  "Use insightconnect-plugin-runtime instead.")

    @staticmethod
    def validate_caching(spec):
        # os.path.join(spec.directory, "")
        pass

    def validate(self, spec):
        RuntimeValidator.validate_setup(spec)
        RuntimeValidator.validate_icon(spec)
        # RuntimeValidator.validate_caching(spec)
