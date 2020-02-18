from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class WorkflowDescriptionValidator(KomandPluginValidator):

    @staticmethod
    def validate_workflow_description_exists(spec):
        if "description" not in spec.spec_dictionary():
            raise ValidationException("Workflow description in yaml is missing.")

        description = spec.spec_dictionary()["description"]
        if description == "":
            raise ValidationException("Workflow description in yaml can not be blank")

    @staticmethod
    def validate_workflow_description_punctuation(description):
        if not description.endswith("."):
            raise ValidationException("Description does not end with a period when it should.")
        if description[0].islower():
            raise ValidationException("Description should not start with a lower case letter.")
        if description[0].isspace():
            raise ValidationException("Description should not start with a whitespace character.")

    def validate(self, spec):
        WorkflowDescriptionValidator.validate_workflow_description_exists(spec)
        WorkflowDescriptionValidator.validate_workflow_description_punctuation(spec.spec_dictionary()["description"])
