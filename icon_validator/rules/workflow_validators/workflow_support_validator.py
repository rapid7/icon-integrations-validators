from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class WorkflowSupportValidator(KomandPluginValidator):

    @staticmethod
    def validate_support(support):
        """
        Check that support is not komand.
        Check that support does not end with a .
        Check that support does not start with a capital letter.
        Check that support does not contain spaces.
        """
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
        """
        Check for quotes around the support.
        """
        # Requires raw spec to see the quotes
        for line in spec.splitlines():
            if line.startswith("support:"):
                val = line[line.find(" ") + 1:]
                if '"' in val or "'" in val:
                    raise ValidationException("Support is surrounded by or contains quotes when it should not.")

    @staticmethod
    def validate_workflow_support(spec):
        """
        Check that support key exists.
        Check that support is a string.
        """
        if "support" not in spec.spec_dictionary():
            raise ValidationException("Plugin supporter is missing.")
        if not isinstance(spec.spec_dictionary()["support"], str):
            raise ValidationException("Plugin supporter does not contain a string.")

    def validate(self, spec):
        WorkflowSupportValidator.validate_workflow_support(spec)
        WorkflowSupportValidator.validate_support(spec.spec_dictionary()["support"])
        WorkflowSupportValidator.validate_support_quotes(spec.raw_spec())
