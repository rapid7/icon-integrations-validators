from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException

class NameValidator(KomandPluginValidator):

    @staticmethod
    def validate_name(name, plugin_name=False):
        if not isinstance(name, str) or name == "":
            raise ValidationException("Name must not be blank")
        if any(character.isupper() for character in name):
            raise ValidationException("Name should not contain upper case characters.")
        if " " in name:
            raise ValidationException("Name should not contain any whitespace characters.")
        if not name.replace("_", "").isalnum():
            raise ValidationException("Name should only contain alphanumeric values.")
        if len(name.split("_")) > 7:
            raise ValidationException(f"Name is too long, 7 words or less: contains {str(len(name.split('_')))}")

    @staticmethod
    def validate_plugin_name(spec):
        if "name" not in spec.spec_dictionary():
            raise ValidationException("Plugin name is missing.")
        try:
            NameValidator.validate_name(spec.spec_dictionary()["name"], plugin_name=True)
        except Exception as error:
            raise ValidationException("Plugin name not valid.", error)

    def validate(self, spec):
        NameValidator.validate_plugin_name(spec)
