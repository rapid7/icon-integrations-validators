from .validator import KomandPluginValidator
import re
from icon_validator.styling import *


class HelpInputOutputValidator(KomandPluginValidator):
    raw_help = ""
    violations = []
    violated = 0

    @staticmethod
    def validate_input(action_title: str, action_input: list):
        regex = r"#### " + action_title + "\n.*?#+ Output"
        action_input_section = re.findall(regex, HelpInputOutputValidator.raw_help, re.DOTALL)

        if not action_input_section:
            print(f'{YELLOW}Action/Trigger \"{action_title}\" could be missing from help.md{RESET_ALL}')
            HelpInputOutputValidator.violated = 1
            return

        for input_fields in action_input:
            if input_fields not in action_input_section[0]:
                HelpInputOutputValidator.violations.append(input_fields)

    @staticmethod
    def validate_output(action_title: str, action_output: list):
        regex = r"#### " + action_title + "\n.*?#+ Output\n\n.*?\n\n"
        action_help_section = re.findall(regex, HelpInputOutputValidator.raw_help, re.DOTALL)

        if not action_help_section:
            print(f'{YELLOW}Action/Trigger \"{action_title}\" could be missing from help.md{RESET_ALL}')
            HelpInputOutputValidator.violated = 1
            return
        action_output_section = re.findall(r'#+ Output\n\n.*?\n\n', action_help_section[0], re.DOTALL)

        for output_fields in action_output:
            if output_fields not in action_output_section[0]:
                HelpInputOutputValidator.violations.append(output_fields)

    @staticmethod
    def get_spec_input(input_content: dict) -> list:
        action_input = []

        for k, v in input_content.items():
            name_ = k
            type_ = input_content.get(k).get('type')
            default_ = input_content.get(k).get('default', None)
            required = input_content.get(k).get('required')
            description = input_content.get(k).get('description')
            enum = input_content.get(k).get('enum', None)
            action_input.append(f'|{name_}|{type_}|{default_}|{required}|{description}|{enum}|')
        return action_input

    @staticmethod
    def get_spec_output(output_content: dict) -> list:
        action_output = []
        for k, v in output_content.items():
            name_ = k
            type_ = output_content.get(k).get('type')
            required = output_content.get(k).get('required')
            description = output_content.get(k).get('description')
            action_output.append(f'|{name_}|{type_}|{required}|{description}|')
        return action_output

    def validate(self, spec):
        HelpInputOutputValidator.raw_help = spec.raw_help()
        raw_spec_yaml = spec.spec_dictionary()
        actions = raw_spec_yaml.get('actions', {})
        actions.update(raw_spec_yaml.get('triggers', {}))

        for key, value in actions.items():
            action_name = actions[key].get('title')
            input_section = actions[key].get('input')
            output_section = actions[key].get('output')

            # Action with no input will skip validation
            if input_section:
                action_input_fields = HelpInputOutputValidator.get_spec_input(input_section)
                HelpInputOutputValidator.validate_input(action_name, action_input_fields)

                if HelpInputOutputValidator.violations:
                    print(f'{YELLOW}Input violations: Action/Trigger -> \"{action_name}\": Missing {HelpInputOutputValidator.violations} in help.md{RESET_ALL}')
                    HelpInputOutputValidator.violations = []
                    HelpInputOutputValidator.violated = 1

            # Action with no output will skip validation
            if output_section:
                action_output_fields = HelpInputOutputValidator.get_spec_output(output_section)
                HelpInputOutputValidator.validate_output(action_name, action_output_fields)

                if HelpInputOutputValidator.violations:
                    print(f'{YELLOW}Output violations: Action/Trigger -> \"{action_name}\": Missing {HelpInputOutputValidator.violations} in help.md{RESET_ALL}')
                    HelpInputOutputValidator.violations = []
                    HelpInputOutputValidator.violated = 1

        if HelpInputOutputValidator.violated:
            raise Exception("Help.md is not in sync with plugin.spec.yaml. Please check and rectify above violations")
