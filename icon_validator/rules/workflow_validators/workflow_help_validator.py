from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class WorkflowHelpValidator(KomandPluginValidator):

    @staticmethod
    def validate_help_exists(spec):
        """
        Checks that 'help' is not in .yaml
        In old code help was included in the yaml. It should no longer be there
        """
        if "help" in spec:
            raise ValidationException("Help section should exist in help.md and not in the workflow.spec.yaml file.")

    @staticmethod
    def validate_version_history(help_str):
        """
        Checks that the first line in version history is 1.0.0 - Initial workflow
        """
        if "- Initial workflow" not in help_str:
            raise ValidationException("Initial workflow version line is missing: 1.0.0 - Initial workflow.")

    @staticmethod
    def validate_help_headers(help_str):
        """
        Checks that all the expected headers are included in help.md
        """
        if "# Description" not in help_str:
            raise ValidationException("Help section is missing header: # Description.")
        if "# Key Features" not in help_str:
            raise ValidationException("Help section is missing header: # Key Features.")
        if "# Requirements" not in help_str:
            raise ValidationException("Help section is missing header: # Requirements.")
        if "# Documentation" not in help_str:
            raise ValidationException("Help section is missing header: # Documentation.")
        if "## Setup" not in help_str:
            raise ValidationException("Help section is missing header: ## Setup.")
        if "## Technical Details" not in help_str:
            raise ValidationException("Help section is missing header: ## Technical Details.")
        if "## Troubleshooting" not in help_str:
            raise ValidationException("Help section is missing header: ## Troubleshooting.")
        if "# Version History" not in help_str:
            raise ValidationException("Help section is missing header: # Version History.")
        if "# Links" not in help_str:
            raise ValidationException("Help section is missing header: # Links.")
        if "## References" not in help_str:
            raise ValidationException("Help section is missing header: ## References.")

    def validate(self, spec):
        WorkflowHelpValidator.validate_help_exists(spec.spec_dictionary())
        WorkflowHelpValidator.validate_help_headers(spec.raw_help())
        WorkflowHelpValidator.validate_version_history(spec.raw_help())
