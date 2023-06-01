import json
import re
from typing import List, Tuple

from icon_plugin_spec.plugin_spec import KomandPluginSpec

from icon_validator.exceptions import ValidationException
from icon_validator.rules.validator import KomandPluginValidator


class HelpExampleValidator(KomandPluginValidator):
    pattern = r"\n[#]{4} (.*?)\n.*?Example input:\n\n(```.*?```)\n.*?Example output:\n\n(```.*?```)\n"

    def __init__(self, name=None):
        super().__init__(name)
        self.validate_errors: List[ValidationException] = []

    def get_objects(self, function_pattern: str, raw_help: str) -> List[Tuple[str]]:
        raw_object = re.findall(function_pattern, raw_help, re.DOTALL)
        if not raw_object:
            return
        return re.findall(self.pattern, raw_object[0], re.DOTALL)

    def add_json_error(self, input_output: str, function_type: str, title: str) -> None:
        self.validate_errors.append(
            f"Invalid JSON example identified in Example {input_output} of {function_type} titled {title}. "
            "Please correct the JSON example in help.md."
        )

    def validate_json(
        self, input_output: str, function_type: str, json_object: str, title: str
    ) -> bool:
        try:
            json.loads(json_object)
            return True
        except json.JSONDecodeError:
            self.add_json_error(input_output, function_type, title)
            return False

    def validate_spaces(
        self, input_output: str, function_type: str, json_object: str, title: str
    ) -> None:
        indent_json = json.dumps(json.loads(json_object), indent=2)
        if indent_json.count(" ") != json_object.count(" "):
            self.validate_errors.append(
                f"Improperly formatted JSON example identified in Example {input_output} of {function_type} "
                f"titled {title}. "
                "Please updated the JSON example in help.md with 2 space indentation."
            )

    def validate_examples(self, function_type: str, objects: List[Tuple[str]]) -> None:
        if not objects:
            return

        for name, input_example, output_example in objects:
            input_example = self._clean_json_example(input_example)
            output_example = self._clean_json_example(output_example)
            if self.validate_json("input", function_type, input_example, name):
                self.validate_spaces("input", function_type, input_example, name)

            if self.validate_json("output", function_type, output_example, name):
                self.validate_spaces("output", function_type, output_example, name)

    def _clean_json_example(self, input_example: str) -> str:
        return input_example.replace("```", "").strip()

    def validate(self, spec: KomandPluginSpec) -> None:
        actions_objects = self.get_objects(r"###[ ]*Actions.*?\n### ", spec.raw_help())
        trigger_objects = self.get_objects(r"###[ ]*Triggers.*?\n### ", spec.raw_help())

        self.validate_examples("action", actions_objects)
        self.validate_examples("trigger", trigger_objects)

        if self.validate_errors:
            raise ValidationException("\n\t".join(self.validate_errors))
