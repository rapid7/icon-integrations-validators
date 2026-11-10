from icon_plugin_spec.plugin_spec import KomandPluginSpec

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException
from icon_validator.snippet.unmarshal import snpt_file_names


class SnippetSNPTFileNameValidator(KomandPluginValidator):

    def validate(self, spec: KomandPluginSpec) -> None:
        """
        Checks that .snpt file names do not contain spaces
        """
        for file_name in snpt_file_names(spec.directory):
            if " " in file_name:
                raise ValidationException(f"The .snpt file name was '{file_name}'.\n "
                                          ".snpt file may not contain spaces use a '_' instead.")
