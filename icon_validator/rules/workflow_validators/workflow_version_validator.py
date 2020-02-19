import re

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class WorkflowVersionValidator(KomandPluginValidator):

    @staticmethod
    def validate_version(version):
        """
        Check that version conforms to semver format.
        """
        if re.match("[1-9]+.[0-9]+.[0-9]+$", version) is None:
            raise ValidationException("Version does not match required semver format. "
                                      "Version should be in form X.Y.Z with X, Y, and Z "
                                      "being numbers. No special characters or spaces allowed. "
                                      "Versions start at 1.0.0, see https://semver.org/ for more information.")

    @staticmethod
    def validate_version_quotes(spec):
        """
        Check for quotes around the version.
        """
        # Requires raw spec to see the quotes
        for line in spec.splitlines():
            if line.startswith("version:"):
                val = line[line.find(" ") + 1:]
                if "'" in val or '"' in val:
                    raise ValidationException("Vendor is surrounded by or contains quotes when it should not.")

    @staticmethod
    def validate_workflow_version(spec):
        """
        Check that version key exists.
        Check that version is a string.
        """
        if "version" not in spec.spec_dictionary():
            raise ValidationException("Workflow version is missing.")
        if not isinstance(spec.spec_dictionary()["version"], str):
            raise ValidationException("Workflow version does not contain a string.")

    def validate(self, spec):
        WorkflowVersionValidator.validate_workflow_version(spec)
        WorkflowVersionValidator.validate_version(spec.spec_dictionary()["version"])
        WorkflowVersionValidator.validate_version_quotes(spec.raw_spec())
