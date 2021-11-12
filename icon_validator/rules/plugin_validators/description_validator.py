from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class DescriptionValidator(KomandPluginValidator):
    errors = []

    @staticmethod
    def validate_description(description, key):
        if description.endswith("."):
            DescriptionValidator.errors.append(f"Description ends with a period when it should not in {key}.")
        if description[0].islower():
            DescriptionValidator.errors.append(f"Description should not start with a lower case letter {key}.")
        if description[0].isspace():
            DescriptionValidator.errors.append(f"Description should not start with a whitespace character {key}.")

    @staticmethod
    def validate_actions(dict_, dict_key):
        if dict_key in dict_:
            DescriptionValidator.validate_dictionary(dict_, dict_key)
            for key, value in dict_[dict_key].items():
                if "input" in value:
                    DescriptionValidator.validate_dictionary(value, "input")
                if "output" in value:
                    DescriptionValidator.validate_dictionary(value, "output")
                if "state" in value:
                    DescriptionValidator.validate_dictionary(value, "state")

    @staticmethod
    def validate_dictionary(dict_, dict_key):
        if dict_key in dict_:
            if not dict_[dict_key]:
                return

            for key, value in dict_[dict_key].items():
                if "description" not in value or not value["description"]:
                    DescriptionValidator.errors.append(f"{dict_key} key '{key}' is missing description field.")
                else:
                    DescriptionValidator.validate_description(value["description"], f"{dict_key} key {key}")

    @staticmethod
    def validate_plugin_description(spec):
        if "description" not in spec.spec_dictionary():
            DescriptionValidator.errors.append("Plugin description is missing.")
        else:
            DescriptionValidator.validate_description(spec.spec_dictionary()["description"], "plugin spec")

    def validate(self, spec):
        DescriptionValidator.validate_plugin_description(spec)
        DescriptionValidator.validate_actions(spec.spec_dictionary(), "actions")
        DescriptionValidator.validate_actions(spec.spec_dictionary(), "triggers")
        DescriptionValidator.validate_actions(spec.spec_dictionary(), "tasks")

        if DescriptionValidator.errors:
            errors = DescriptionValidator.errors
            DescriptionValidator.errors = []
            raise ValidationException("\n\t\t" + "\n\t\t".join(errors))


        # Types do not have descriptions but their keys do.
        # TODO: disabling type descriptions until better plugin autogen support exists (for swagger, wasdl, etc)
        # if "types" in spec.spec_dictionary():
        #     for key, value in spec.spec_dictionary()["types"].items():
        #         DescriptionValidator.validate_dictionary(spec.spec_dictionary()["types"], key)
