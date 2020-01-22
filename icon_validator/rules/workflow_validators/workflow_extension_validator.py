from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class WorkflowExtensionValidator(KomandPluginValidator):

    @staticmethod
    def validate_extension(extension):
        if not extension == "workflow":
            raise ValidationException("Extension key must have a value of workflow.")

    @staticmethod
    def validate_extension_exists(spec):
        if "extension" not in spec.spec_dictionary():
            raise ValidationException("Workflow extension key is missing.")

    def validate(self, spec):
        WorkflowExtensionValidator.validate_extension_exists(spec)
        WorkflowExtensionValidator.validate_extension(spec.spec_dictionary()["extension"])
