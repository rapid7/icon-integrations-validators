from icon_plugin_spec.plugin_spec import KomandPluginSpec

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException
from icon_validator.rules.workflow_validators.workflow_help_validator import WorkflowHelpValidator


class SnippetHelpValidator(KomandPluginValidator):

    @staticmethod
    def validate_help_exists(spec_dictionary: dict) -> None:
        """
        Checks that 'help' is not in .yaml
        """
        if "help" in spec_dictionary:
            raise ValidationException("Help section should exist in help.md and not in the snippet.spec.yaml file.")

    @staticmethod
    def validate_version_history(help_str: str) -> None:
        """
        Checks that the version history includes the line 1.0.0 - Initial snippet
        """
        if "- Initial snippet" not in help_str:
            raise ValidationException("Initial snippet version line is missing: 1.0.0 - Initial snippet.")

    def validate(self, spec: KomandPluginSpec) -> None:
        """
        A snippet's help.md has the same headers as a workflow's help.md
        """
        SnippetHelpValidator.validate_help_exists(spec.spec_dictionary())
        WorkflowHelpValidator.validate_help_headers(spec.raw_help())
        SnippetHelpValidator.validate_version_history(spec.raw_help())
