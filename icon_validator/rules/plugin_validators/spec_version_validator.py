from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class SpecVersionValidator(KomandPluginValidator):

    def validate(self, spec):
        plugin_spec_version = spec.spec_dictionary()["plugin_spec_version"]
        if plugin_spec_version != "v2":
            raise ValidationException("Plugin spec version is not v2.")
