import os

from icon_plugin_spec.plugin_spec import KomandPluginSpec

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException
from icon_validator.snippet.unmarshal import SNPT_FILE_EXTENSION


class SnippetDirectoryNameMatchValidator(KomandPluginValidator):
    def validate(self, spec: KomandPluginSpec) -> None:
        """
        Checks that a directory name matches a snippet filename (.snpt file),
        as in snippets/<Name>/<Name>.snpt
        """
        directory_name = os.path.basename(spec.directory)
        expected_file_name = f"{directory_name}{SNPT_FILE_EXTENSION}"

        if expected_file_name not in os.listdir(spec.directory):
            raise ValidationException(
                f"Snippet directory name does not match the snippet filename! Expected {expected_file_name}."
            )
