from icon_plugin_spec.plugin_spec import KomandPluginSpec

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.rules.workflow_validators.workflow_title_validator import WorkflowTitleValidator
from icon_validator.snippet.unmarshal import read_snippet


class SnippetTitleValidator(KomandPluginValidator):

    @staticmethod
    def validate_snpt_titles(snippet: dict) -> None:
        """
        Checks the step names in the .snpt file with the same title rules as the spec title
        """
        steps = snippet.get("steps")
        if not isinstance(steps, list):
            # SnippetSNPTFileValidator reports a missing or malformed steps key
            return
        for step in steps:
            if isinstance(step, dict):
                WorkflowTitleValidator.validate_title(step.get("name"), ".snpt")

    def validate(self, spec: KomandPluginSpec) -> None:
        """
        Checks that title is not blank.
        Checks that title does not end with a period.
        Checks that title does not start with a lower case letter.
        Checks that title does not start with a space.
        Checks that title is properly capitalized.
        """
        WorkflowTitleValidator.validate_title(WorkflowTitleValidator.get_title_from_spec(spec), ".spec")
        SnippetTitleValidator.validate_snpt_titles(read_snippet(spec.directory))
