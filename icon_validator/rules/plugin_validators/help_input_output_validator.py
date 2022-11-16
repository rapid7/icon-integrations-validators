import re

from icon_validator.styling import *
from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException

from datetime import datetime


def valid_datetime(list_entry: str) -> bool:
    """
    This function determines if a valid datetime following
    iso format is detected in a string

    :param list_entry: The entry of the list to be checked for datetime validity
    """
    try:
        datetime.fromisoformat(list_entry)
        return True
    except ValueError:
        return False


def convert_add_t_to_datetime(date: str) -> str:
    """
    This function takes a str containing a date and converts it to the format
    that matches the format found within the raw help md

    :param date: datetime string
    :type date: str

    :return final_result: datetime string containing 'T'
    :rtype final_result: str
    """
    datetime_object = datetime.fromisoformat(date)
    timezone = datetime_object.strftime("%z")
    new_timezone = timezone[:3] + ":" + timezone[3:]
    new_datetime = datetime_object.strftime("%Y-%m-%dT%H:%M:%S")
    final_result = new_datetime + new_timezone
    return final_result


def datetime_checker_fixer(action_input: str):
    """


    :param action_input: table string for the action from help md
    :type action_input: str
    """
    split_action_input = action_input.split("|")
    for entry in split_action_input:
        if valid_datetime(entry) is True:
            new_datetime_value = entry.datetime.strftime()


class HelpInputOutputValidator(KomandPluginValidator):
    raw_help = ""
    violations = []
    violated = 0
    action_missing = 0

    @staticmethod
    def validate_input(action_title: str, action_input: list, process_type: str):
        regex = r"### " + process_type.capitalize() + ".*?#### " + action_title + "\n.*?#+ Output"
        if process_type == "actions":
            regex = regex + ".*?### Triggers"
        elif process_type == "triggers":
            if "### Tasks" in HelpInputOutputValidator.raw_help:
                regex = regex + ".*?### Tasks"

        action_input_section = re.findall(regex, HelpInputOutputValidator.raw_help, re.DOTALL)

        if not action_input_section:
            print(
                f"{YELLOW}{process_type[:-1].capitalize()} \"{action_title}\" could be missing or title is incorrect in help.md{RESET_ALL}.")
            HelpInputOutputValidator.violated = 1
            HelpInputOutputValidator.action_missing = 1
            return

        regex = r"#### " + action_title + "\n.*?#+ Output"
        action_input_section = re.findall(regex, action_input_section[0], re.DOTALL)
        import pdb; pdb.set_trace()
        for input_fields in action_input:
            # if input_fields.find('date') is not None:
            #     continue
            if input_fields not in action_input_section[0]:
                HelpInputOutputValidator.violations.append(input_fields)

    @staticmethod
    def validate_output(action_title: str, action_output: list, process_type: str):
        regex = r"### " + process_type.capitalize() + ".*?#### " + action_title + "\n.*?#+ Output\n\n.*?\n\n"
        if process_type == "actions":
            regex = regex + ".*?### Trigger"
        elif process_type == "triggers":
            if "### Tasks" in HelpInputOutputValidator.raw_help:
                regex = regex + ".*?### Tasks"

        action_help_section_temp = re.findall(regex, HelpInputOutputValidator.raw_help, re.DOTALL)
        regex = r"#### " + action_title + "\n.*?#+ Output\n\n.*?\n\n"
        action_help_section = re.findall(regex, action_help_section_temp[0], re.DOTALL)

        if "This " + process_type[:-1] + " does not contain any outputs." not in action_help_section[0]:
            regex = r"### " + process_type.capitalize() + ".*?#### " + action_title + "\n.*?#+ Output\n\n.*?" + re.escape(
                "|Name|Type|Required|Description|") + ".*?\n\n"
            if process_type == "actions":
                regex = regex + ".*?### Triggers"
            elif process_type == "triggers":
                if "### Tasks" in HelpInputOutputValidator.raw_help:
                    regex = regex + ".*?### Tasks"

            action_help_section_temp = re.findall(regex, HelpInputOutputValidator.raw_help, re.DOTALL)
            regex = r"#### " + action_title + "\n.*?#+ Output\n\n.*?" + re.escape(
                "|Name|Type|Required|Description|") + ".*?\n\n"
            action_output_section_temp = re.findall(regex, action_help_section_temp[0], re.DOTALL)
            action_output_section = re.findall(
                r"#+ Output\n\n.*?" + re.escape("|Name|Type|Required|Description|") + ".*?\n\n",
                action_output_section_temp[0], re.DOTALL)
        else:
            action_output_section = re.findall(r"#+ Output\n\n.*?\n\n", action_help_section[0], re.DOTALL)

        for output_fields in action_output:
            if output_fields not in action_output_section[0]:
                HelpInputOutputValidator.violations.append(output_fields)

    @staticmethod
    def get_spec_input(input_content: dict) -> list:
        action_input = []

        for k, v in input_content.items():
            name_ = k
            type_ = input_content.get(k).get("type")
            default_ = input_content.get(k).get("default", None)
            required = input_content.get(k).get("required")
            description = input_content.get(k).get("description")
            enum = input_content.get(k).get("enum", None)
            example = input_content.get(k).get("example", None)
            if example is None:
                raise ValidationException(f"plugin.spec is missing input example for {v}")
            else:
                if isinstance(example, list):
                    example = f"{example}".replace("'", '"')
                action_input.append(f"|{name_}|{type_}|{default_}|{required}|{description}|{enum}|{example}|")
        return action_input

    @staticmethod
    def get_spec_output(output_content: dict) -> list:
        action_output = []
        for k, v in output_content.items():
            name_ = k
            type_ = output_content.get(k).get("type")
            required = output_content.get(k).get("required", False)
            description = output_content.get(k).get("description", None)
            example = output_content.get(k).get("example", None)
            if example is None:
                raise ValidationException(f"plugin.spec is missing output example for {v}")
            else:
                if isinstance(example, list):
                    example = f"{example}".replace("'", '"')
                action_output.append(f"|{name_}|{type_}|{required}|{description}|{example}|")
        return action_output

    def validate(self, spec):
        HelpInputOutputValidator.raw_help = spec.raw_help()
        raw_spec_yaml = spec.spec_dictionary()
        process_type = ["actions", "triggers", "tasks"]

        for p_type in process_type:
            actions = raw_spec_yaml.get(p_type, {})
            for key, value in actions.items():
                action_name = actions[key].get("title")
                input_section = actions[key].get("input")
                output_section = actions[key].get("output")
                HelpInputOutputValidator.action_missing = 0
                import pdb; pdb.set_trace()
                # Action with no input in spec file will skip input validation
                if input_section:
                    action_input_fields = HelpInputOutputValidator.get_spec_input(input_section)
                    HelpInputOutputValidator.validate_input(action_name, action_input_fields, p_type)

                    if HelpInputOutputValidator.violations:
                        print(
                            f"{YELLOW}Input violations: {p_type[:-1].capitalize()} -> \"{action_name}\": Missing {HelpInputOutputValidator.violations} in help.md{RESET_ALL}")
                        HelpInputOutputValidator.violations = []
                        HelpInputOutputValidator.violated = 1

                # Actions with no output in spec file will skip output validation. Also, skip output validation for actions not found in help.md
                if output_section and not HelpInputOutputValidator.action_missing:
                    action_output_fields = HelpInputOutputValidator.get_spec_output(output_section)
                    HelpInputOutputValidator.validate_output(action_name, action_output_fields, p_type)

                    if HelpInputOutputValidator.violations:
                        print(
                            f"{YELLOW}Output violations: {p_type[:-1].capitalize()}-> \"{action_name}\": Missing {HelpInputOutputValidator.violations} in help.md{RESET_ALL}")
                        HelpInputOutputValidator.violations = []
                        HelpInputOutputValidator.violated = 1

        if HelpInputOutputValidator.violated:
            raise ValidationException("Help.md is not in sync with plugin.spec.yaml. Please regenerate help.md by running 'icon-plugin generate python --regenerate' to rectify violations.")
