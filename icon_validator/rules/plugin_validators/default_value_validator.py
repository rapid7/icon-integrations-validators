import validators

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class DefaultValueValidator(KomandPluginValidator):

    @staticmethod
    def validate_variables(validate_variables):

        if not validate_variables:
            return

        for k, v in validate_variables.items():
            if "default" in v:
                if k == "domain":
                    if validators.domain(v["default"]) is not True:
                        raise ValidationException(f"Variable {k}'s default value is not a valid domain.")
                elif k == "email" or k == "email_address":
                    if validators.email(v["default"]) is not True:
                        raise ValidationException(f"Variable {k}'s default value is not a valid email address.")

    @staticmethod
    def validate_action(action):

        if not action:
            return

        for key, value in action.items():
            if "input" in value:
                DefaultValueValidator.validate_variables(value["input"])
            if "output" in value:
                DefaultValueValidator.validate_variables(value["output"])
            if "state" in value:
                DefaultValueValidator.validate_variables(value["state"])

    def validate(self, spec):
        plugin_spec = spec.spec_dictionary()
        if "actions" in plugin_spec:
            DefaultValueValidator.validate_action(plugin_spec["actions"])
        if "triggers" in plugin_spec:
            DefaultValueValidator.validate_action(plugin_spec["triggers"])
        if "tasks" in plugin_spec:
            DefaultValueValidator.validate_action(plugin_spec["tasks"])
        if "types" in plugin_spec:
            for k, v in plugin_spec["types"].items():
                DefaultValueValidator.validate_variables(v)
