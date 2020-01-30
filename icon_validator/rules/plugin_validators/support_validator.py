from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class SupportValidator(KomandPluginValidator):

    @staticmethod
    def validate_support(support):
        lsupport = support.lower()
        if lsupport == "komand":
            raise ValidationException("Support 'komand' not allowed. It's likely you meant 'rapid7'.")
        if support.endswith("."):
            raise ValidationException("Support ends with period when it should not.")
        if not support[0].islower():
            raise ValidationException("Support starts with a capital letter when it should not.")
        if " " in support:
            raise ValidationException("Support should be separated by underscores, not spaces.")

    @staticmethod
    def validate_support_quotes(spec):
        """Requires raw spec to see the quotes"""
        for line in spec.splitlines():
            if line.startswith("support:"):
                val = line[line.find(" ") + 1:]
                if '"' in val or "'" in val:
                    raise ValidationException("Support is surrounded by or contains quotes when it should not.")

    @staticmethod
    def validate_plugin_support(spec):
        if "support" not in spec.spec_dictionary():
            raise ValidationException("Plugin supporter is missing.")
        if not isinstance(spec.spec_dictionary()["support"], str):
            raise ValidationException("Plugin supporter does not contain a string.")

    def validate(self, spec):
        SupportValidator.validate_plugin_support(spec)
        SupportValidator.validate_support(spec.spec_dictionary()["support"])
        SupportValidator.validate_support_quotes(spec.raw_spec())
