from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException
from icon_validator.styling import  *


class RequiredValidator(KomandPluginValidator):

    @staticmethod
    def validate_required(required):
        if not isinstance(required, bool):
            raise ValidationException("required must be boolean.")

    @staticmethod
    def validate_actions(dict_, dict_key):
        if dict_key in dict_:
            for key, value in dict_[dict_key].items():
                if "input" in value:
                    RequiredValidator.validate_dictionary(value, "input")
                if "output" in value:
                    RequiredValidator.validate_dictionary(value, "output")

    @staticmethod
    def validate_connection(dict_, dict_key):
        if dict_key in dict_:
            RequiredValidator.validate_dictionary(dict_, dict_key)

    @staticmethod
    def validate_dictionary(dict_, dict_key):
        if dict_key in dict_:
            if not dict_[dict_key]:
                return

            for key, value in dict_[dict_key].items():
                if "required" not in value:
                    raise ValidationException(f"{YELLOW}{dict_key} key '{key}' is missing required field{RESET_ALL}")
                try:
                    RequiredValidator.validate_required(value["required"])
                except Exception as e:
                    raise ValidationException(f"{YELLOW}{dict_key} key '{key}'\'s required must be boolean{RESET_ALL}", e)

    def validate(self, spec):
        RequiredValidator.validate_actions(spec.spec_dictionary(), "actions")
        RequiredValidator.validate_actions(spec.spec_dictionary(), "triggers")
        RequiredValidator.validate_actions(spec.spec_dictionary(), "tasks")
        RequiredValidator.validate_connection(spec.spec_dictionary(), "connection")
