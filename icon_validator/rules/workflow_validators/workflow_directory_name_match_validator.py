import os

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class WorkflowDirectoryNameMatchValidator(KomandPluginValidator):
    def validate(self, spec):
        """
        Checks that a directory name matches a workflow filename (.icon file).
        Mismatch causes an import issue in the Extension library
        """
        d = spec.directory

        # Get directory name
        directory_name = d.split("/")[-1]

        directory_contents = set(os.listdir(d))

        if f"{directory_name}.icon" not in directory_contents:
            raise ValidationException(
                "Workflow directory name does not match the workflow filename!"
            )
