import os

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class WorkflowScreenshotsSpecMatchValidator(KomandPluginValidator):
    def validate(self, spec):
        """
        Checks that a directory name matches a workflow filename (.icon file).
        Mismatch causes an import issue in the Extension library
        """
        d = spec.directory
        screenshots_directory = f"{d}/screenshots"

        screenshot_files = set(os.listdir(screenshots_directory))
        spec_screenshots = {
            name["name"] for name in spec.spec_dictionary()["resources"]["screenshots"]
        }

        mismatches = screenshot_files.difference(spec_screenshots)

        if mismatches:
            raise ValidationException(
                "Mismatch between provided screenshot files and screenshots in "
                "workflow.spec.yaml!"
            )
