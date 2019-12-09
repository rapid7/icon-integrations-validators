from .validator import KomandPluginValidator


class WorkflowHelpValidator(KomandPluginValidator):

    @staticmethod
    def validate_help_exists(spec):
        if 'help' in spec:
            raise Exception('Help section should exist in help.md and not in the workflow.spec.yaml file')

    @staticmethod
    def validate_version_history(help_str):
        if '- Initial workflow' not in help_str:
            raise Exception("Initial workflow version line is missing: 1.0.0 - Initial workflow")

    @staticmethod
    def validate_help_headers(help_str):
        if '# Description' not in help_str:
            raise Exception("Help section is missing header: # Description")
        if '# Key Features' not in help_str:
            raise Exception("Help section is missing header: # Key Features")
        if '# Requirements' not in help_str:
            raise Exception("Help section is missing header: # Requirements")
        if '# Documentation' not in help_str:
            raise Exception("Help section is missing header: # Documentation")
        if '## Setup' not in help_str:
            raise Exception("Help section is missing header: ## Setup")
        if '## Technical Details' not in help_str:
            raise Exception("Help section is missing header: ## Technical Details")
        if '## Troubleshooting' not in help_str:
            raise Exception("Help section is missing header: ## Troubleshooting")
        if '# Version History' not in help_str:
            raise Exception("Help section is missing header: # Version History")
        if '# Links' not in help_str:
            raise Exception("Help section is missing header: # Links")
        if '## References' not in help_str:
            raise Exception("Help section is missing header: ## References")

    def validate(self, spec):
        WorkflowHelpValidator.validate_help_exists(spec.spec_dictionary())
        WorkflowHelpValidator.validate_help_headers(spec.raw_help())
        WorkflowHelpValidator.validate_version_history(spec.raw_help())

