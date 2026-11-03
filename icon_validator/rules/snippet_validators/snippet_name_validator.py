from icon_plugin_spec.plugin_spec import KomandPluginSpec

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException
from icon_validator.snippet.unmarshal import SNPT_FILE_EXTENSION, snpt_file_names


class SnippetNameValidator(KomandPluginValidator):

    def validate(self, spec: KomandPluginSpec) -> None:
        """
        Checks that the name key in .yaml is the same as the name of the .snpt file without the .snpt part
        """
        spec_dictionary = spec.spec_dictionary()
        if "name" not in spec_dictionary:
            raise ValidationException("The snippet name is missing in snippet.spec.yaml.")
        name = spec_dictionary["name"]
        if not isinstance(name, str):
            raise ValidationException("The snippet name does not contain a string.")

        snpt_names = [file_name[:-len(SNPT_FILE_EXTENSION)] for file_name in snpt_file_names(spec.directory)]
        if name not in snpt_names:
            raise ValidationException(f"The snippet name in snippet.spec.yaml ({name}) and the name of the "
                                      f".snpt snippet file ({', '.join(snpt_names)}) do not match.")
