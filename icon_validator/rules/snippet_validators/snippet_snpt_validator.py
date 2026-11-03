from typing import Any

from icon_plugin_spec.plugin_spec import KomandPluginSpec

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException
from icon_validator.snippet.unmarshal import read_snippet


class SnippetSNPTFileValidator(KomandPluginValidator):

    # The keys InsightConnect needs to import a snippet from a .snpt file
    _REQUIRED_KEYS = ["name", "summary", "tags", "notes", "inputSchema", "outputSchema", "steps", "graph"]
    _REQUIRED_STEP_KEYS = ["nodeId", "name", "type"]

    @staticmethod
    def validate_keys_exist(snippet: dict) -> None:
        missing_keys = [key for key in SnippetSNPTFileValidator._REQUIRED_KEYS if key not in snippet]
        if missing_keys:
            raise ValidationException(
                f"The .snpt file is missing the following keys: {', '.join(missing_keys)}. "
                "Try exporting the snippet again."
            )

    @staticmethod
    def validate_name(name: Any) -> None:
        if not isinstance(name, str) or not name.strip():
            raise ValidationException("The name key in the .snpt file is not defined. Try exporting the snippet again.")

    @staticmethod
    def validate_summary_and_notes(snippet: dict) -> None:
        # The summary and notes keys may be blank strings
        for key in ("summary", "notes"):
            if not isinstance(snippet[key], str):
                raise ValidationException(
                    f"The {key} key in the .snpt file is not defined. Try exporting the snippet again."
                )

    @staticmethod
    def validate_tags(tags: Any) -> None:
        if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
            raise ValidationException(
                "The tags key in the .snpt file must be a list of strings. Try exporting the snippet again."
            )

    @staticmethod
    def validate_schemas(snippet: dict) -> None:
        for key in ("inputSchema", "outputSchema"):
            if not isinstance(snippet[key], dict):
                raise ValidationException(
                    f"The {key} key in the .snpt file must be a JSON object. Try exporting the snippet again."
                )

    @staticmethod
    def validate_steps(steps: Any) -> None:
        if not isinstance(steps, list) or not steps:
            raise ValidationException(
                "The .snpt file has no steps. A snippet needs at least one step. Try exporting the snippet again."
            )
        for index, step in enumerate(steps):
            if not isinstance(step, dict):
                raise ValidationException(
                    f"steps[{index}] in the .snpt file is not a JSON object. Try exporting the snippet again."
                )
            for key in SnippetSNPTFileValidator._REQUIRED_STEP_KEYS:
                value = step.get(key)
                if not isinstance(value, str) or not value:
                    raise ValidationException(
                        f"The {key} key in steps[{index}] of the .snpt file is not defined. "
                        "Try exporting the snippet again."
                    )

    @staticmethod
    def validate_graph(graph: Any) -> None:
        if (
            not isinstance(graph, dict)
            or not isinstance(graph.get("nodes"), list)
            or not isinstance(graph.get("edges"), list)
        ):
            raise ValidationException(
                "The graph key in the .snpt file must contain nodes and edges lists. Try exporting the snippet again."
            )

    @staticmethod
    def validate_snippet(snippet: dict) -> None:
        SnippetSNPTFileValidator.validate_keys_exist(snippet)
        SnippetSNPTFileValidator.validate_name(snippet["name"])
        SnippetSNPTFileValidator.validate_summary_and_notes(snippet)
        SnippetSNPTFileValidator.validate_tags(snippet["tags"])
        SnippetSNPTFileValidator.validate_schemas(snippet)
        SnippetSNPTFileValidator.validate_steps(snippet["steps"])
        SnippetSNPTFileValidator.validate_graph(snippet["graph"])

    def validate(self, spec: KomandPluginSpec) -> None:
        """
        Checks that the directory has exactly one .snpt file, that it is JSON,
        and that it has the keys InsightConnect needs to import the snippet
        """
        SnippetSNPTFileValidator.validate_snippet(read_snippet(spec.directory))
