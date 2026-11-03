import os

from icon_plugin_spec.plugin_spec import KomandPluginSpec

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException
from icon_validator.snippet.unmarshal import snpt_file_names


class SnippetFilesValidator(KomandPluginValidator):

    def validate(self, spec: KomandPluginSpec) -> None:
        """
        Checks that a help.md, snippet.spec.yaml, and a .snpt file exist.
        Unlike workflows, extension.png is optional: without one the Extension Library shows its default snippet logo.
        """
        directory = spec.directory

        if not os.path.isfile(f"{directory}/snippet.spec.yaml"):
            raise ValidationException(f"File snippet.spec.yaml does not exist in: {directory}")
        if not os.path.isfile(f"{directory}/help.md"):
            raise ValidationException(f"File help.md does not exist in: {directory}")
        if not snpt_file_names(directory):
            raise ValidationException(f"Snippet file (.snpt) does not exist in: {directory}")
