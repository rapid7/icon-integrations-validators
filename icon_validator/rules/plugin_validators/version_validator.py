import re

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class VersionValidator(KomandPluginValidator):

    @staticmethod
    def validate_version(version):
        if re.match("[1-9]+.[0-9]+.[0-9]+$", version) is None:
            raise ValidationException("Version does not match required semver format. "
                            "Version should be in form X.Y.Z with X, Y, and Z "
                            "being numbers. No special characters or spaces allowed. "
                            "Versions start at 1.0.0, see https://semver.org/ for more information.")

    @staticmethod
    def validate_version_quotes(spec):
        """Requires raw spec to see the quotes"""
        for line in spec.splitlines():
            if line.startswith("version:"):
                val = line[line.find(" ") + 1:]
                if "'" in val or '"' in val:
                    raise ValidationException("Vendor is surrounded by or contains quotes when it should not.")

    @staticmethod
    def validate_plugin_version(spec):
        if "version" not in spec.spec_dictionary():
            raise ValidationException("Plugin version is missing.")
        if not isinstance(spec.spec_dictionary()["version"], str):
            raise ValidationException("Plugin version does not contain a string.")

    def validate(self, spec):
        VersionValidator.validate_plugin_version(spec)
        VersionValidator.validate_version(spec.spec_dictionary()["version"])
        VersionValidator.validate_version_quotes(spec.raw_spec())
