import json
import re
from icon_validator.exceptions import ValidationException
from icon_validator.rules.validator import KomandPluginValidator


class HelpExampleValidator(KomandPluginValidator):
    validate_errors = []
    pattern = r"#### (.*?)\n\n.*?Example input:\n\n```\n(.*?)\n\n#.*?Example output:\n\n```\n(.*?)\n\n#"

    @staticmethod
    def get_objects(function_pattern, raw_help):
        raw_object = re.findall(function_pattern, raw_help, re.DOTALL)

        if not raw_object:
            return

        return re.findall(HelpExampleValidator.pattern, raw_object[0], re.DOTALL)

    @staticmethod
    def add_json_error(input_output, function_type, title):
        HelpExampleValidator.validate_errors.append(
            f"Invalid JSON example identified in Example {input_output} of {function_type} titled {title}. "
            "Please correct the JSON example in help.md."
        )

    @staticmethod
    def validate_json(input_output, function_type, json_object, title):
        try:
            json.loads(json_object)
            return True
        except json.JSONDecodeError:
            HelpExampleValidator.add_json_error(input_output, function_type, title)
            return False

    @staticmethod
    def validate_spaces(input_output, function_type, json_object, title):
        indent_json = json.dumps(json.loads(json_object), indent=2)
        if indent_json.count(' ') != json_object.count(' '):
            HelpExampleValidator.validate_errors.append(
                f"Improperly formatted JSON example identified in Example {input_output} of {function_type} "
                f"titled {title}. "
                "Please updated the JSON example in help.md with 2 space indentation."
            )

    def validate_examples(self, function_type, objects):
        if not objects:
            return

        for function_object in objects:
            for i in range(1, 2):
                if not function_object[i] or function_object[i] == "```":
                    continue
                input_output = "input" if i == 1 else "output"
                title = function_object[0]

                if not function_object[i].strip().startswith("{"):
                    HelpExampleValidator.add_json_error(input_output, function_type, title)

                for json_object in re.findall(r"({[^}]+(}|`))", function_object[i], re.MULTILINE):
                    if self.validate_json(input_output, function_type, json_object[0], title):
                        self.validate_spaces(input_output, function_type, json_object[0], title)

    def validate(self, spec):
        HelpExampleValidator.validate_errors = []
        actions_objects = self.get_objects(r"###[ ]*Actions.*?\n### ", spec.raw_help())
        trigger_objects = self.get_objects(r"###[ ]*Triggers.*?\n### ", spec.raw_help())

        self.validate_examples("action", actions_objects)
        self.validate_examples("trigger", trigger_objects)

        if HelpExampleValidator.validate_errors:
            raise ValidationException(
                "\n\t".join(HelpExampleValidator.validate_errors)
            )
