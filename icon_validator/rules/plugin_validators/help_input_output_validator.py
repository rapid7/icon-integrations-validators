import re

from icon_validator.rules.lists.valid_data_types import ExampleOutputDataType
from icon_validator.styling import *
from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException

from datetime import datetime


def detect_valid_datetime(list_entry: str) -> bool:
    """
    This function determines if a valid datetime following
    iso format is detected in a string

    :param list_entry: The entry of the list to be checked for datetime validity
    :type list_entry: str

    :rtype: bool
    """
    try:
        datetime.fromisoformat(list_entry)
        return True
    except ValueError:
        return False


def convert_to_valid_datetime(table_string: str) -> str:
    """
    This function takes a str containing a date in isoformat and converts
    it to the format that matches the format found within the raw help md

    :param table_string: datetime string
    :type table_string: str

    :return final_result: datetime string containing 'T'
    :rtype final_result: str
    """
    # Convert the string to a datetime object so we can work with it
    datetime_object = datetime.fromisoformat(table_string)

    # Create the datetime containing the T using strftime
    new_datetime = datetime_object.strftime("%Y-%m-%dT%H:%M:%S")

    # Extract the timezone separately
    timezone = datetime_object.strftime("%z")

    # If timezone was not found in the string, then just produce the new amended datetime
    if timezone == "":
        final_result = new_datetime
    else:
        # Add the ':' in manually because strftime does not contain an option to convert it like this
        new_timezone = timezone[:3] + ":" + timezone[3:]

        # Combine new datetime and append the amended timezone on the end
        final_result = new_datetime + new_timezone

    # Return the final result
    return final_result


def datetime_formatter(table_string: str) -> str:
    """
    This function uses the other two to perform the actions needed to detect and
    convert the datetime to correct format

    :param table_string: table string for the action from help md
    :type table_string: str

    :return: Newly formatted datetime string
    :rtype: str
    """

    # Take the table string, and split it by the '|' character
    split_action_input = table_string.split("|")

    # Loop through each entry in the newly created list from split
    for entry in split_action_input:
        # Use detect function to detect which entry contains the date
        if detect_valid_datetime(entry):
            # When found, use convert function to convert the list element to the format we need
            new_datetime_value = convert_to_valid_datetime(entry)

            # Replace the old value with the new one
            split_action_input = [old_entry.replace(entry, new_datetime_value) for old_entry in split_action_input]
            # Rejoin the string with '|' character
            return "|".join(split_action_input)

    return table_string


def convert_ais_to_valid_datetime(ais: str) -> list:
    """
    Function to take the string, Action Input Section, and convert
    the datetime contained within that to match the converted datetime
    in the variable, input_fields

    :param ais: Action Input Section
    :type ais: str

    :return: List containing all the string data split by line, with newly converted datetime
    :rtype: list
    """

    lines = ais.splitlines()
    new_lines = []
    lines = [line for line in lines if len(line)]
    lines = [line for line in lines if line[0] == "|"]
    for entry in lines:
        elements = entry.split("|")
        new_elements = []
        for element in elements:
            if detect_valid_datetime(element):
                element = convert_to_valid_datetime(element)
            new_elements.append(element)
        new_lines.append("|".join(new_elements))
    return new_lines


class HelpInputOutputValidator(KomandPluginValidator):
    raw_help = ""
    violations = []
    violated = 0
    action_missing = 0

    @staticmethod
    def validate_input(action_title: str, action_input: list, process_type: str):
        regex = (
            r"### "
            + process_type.capitalize()
            + ".*?#### "
            + action_title
            + "\n.*?#+ Output"
        )
        if process_type == "actions":
            regex = regex + ".*?### Triggers"
        elif process_type == "triggers":
            if "### Tasks" in HelpInputOutputValidator.raw_help:
                regex = regex + ".*?### Tasks"

        action_input_section = re.findall(
            regex, HelpInputOutputValidator.raw_help, re.DOTALL
        )

        if not action_input_section:
            print(
                f'{YELLOW}{process_type[:-1].capitalize()} "{action_title}" could be missing or title is incorrect in help.md{RESET_ALL}.'
            )
            HelpInputOutputValidator.violated = 1
            HelpInputOutputValidator.action_missing = 1
            return

        regex = r"#### " + action_title + "\n.*?#+ Output"
        action_input_section = re.findall(regex, action_input_section[0], re.DOTALL)

        # Function to specifically handle converting the datetimes in action_input_section[0
        converted_ais = convert_ais_to_valid_datetime(action_input_section[0])

        for input_fields in action_input:
            input_fields = datetime_formatter(table_string=input_fields)
            if input_fields not in converted_ais:
                HelpInputOutputValidator.violations.append(input_fields)

    @staticmethod
    def validate_output(action_title: str, action_output: list, process_type: str):
        regex = (
            r"### "
            + process_type.capitalize()
            + ".*?#### "
            + action_title
            + "\n.*?#+ Output\n\n.*?\n\n"
        )
        if process_type == "actions":
            regex = regex + ".*?### Trigger"
        elif process_type == "triggers":
            if "### Tasks" in HelpInputOutputValidator.raw_help:
                regex = regex + ".*?### Tasks"

        action_help_section_temp = re.findall(
            regex, HelpInputOutputValidator.raw_help, re.DOTALL
        )
        regex = r"#### " + action_title + "\n.*?#+ Output\n\n.*?\n\n"

        try:
            action_help_section = re.findall(
                regex, action_help_section_temp[0], re.DOTALL
            )
        except IndexError:
            raise ValidationException(
                "Incorrect formatting in the action/trigger/task headings."
            )

        if (
            "This " + process_type[:-1] + " does not contain any outputs."
            not in action_help_section[0]
        ):
            regex = (
                r"### "
                + process_type.capitalize()
                + ".*?#### "
                + action_title
                + "\n.*?#+ Output\n\n.*?"
                + re.escape("|Name|Type|Required|Description|")
                + ".*?\n\n"
            )
            if process_type == "actions":
                regex = regex + ".*?### Triggers"
            elif process_type == "triggers":
                if "### Tasks" in HelpInputOutputValidator.raw_help:
                    regex = regex + ".*?### Tasks"

            action_help_section_temp = re.findall(
                regex, HelpInputOutputValidator.raw_help, re.DOTALL
            )
            regex = (
                r"#### "
                + action_title
                + "\n.*?#+ Output\n\n.*?"
                + re.escape("|Name|Type|Required|Description|")
                + ".*?\n\n"
            )
            action_output_section_temp = re.findall(
                regex, action_help_section_temp[0], re.DOTALL
            )
            action_output_section = re.findall(
                r"#+ Output\n\n.*?"
                + re.escape("|Name|Type|Required|Description|")
                + ".*?\n\n",
                action_output_section_temp[0],
                re.DOTALL,
            )
        else:
            action_output_section = re.findall(
                r"#+ Output\n\n.*?\n\n", action_help_section[0], re.DOTALL
            )

        for output_fields in action_output:
            if output_fields not in action_output_section[0]:
                HelpInputOutputValidator.violations.append(output_fields)

    @staticmethod
    def get_spec_input(input_content: dict) -> list:
        action_input = []

        for k, v in input_content.items():
            name_ = k
            type_ = input_content.get(k, {}).get("type")
            default_ = input_content.get(k, {}).get("default", None)
            required = input_content.get(k, {}).get("required")
            description = input_content.get(k, {}).get("description")
            enum = input_content.get(k, {}).get("enum", None)
            example = input_content.get(k, {}).get("example", None)
            placeholder = input_content.get(k, {}).get("placeholder", None)
            tooltip = input_content.get(k, {}).get("tooltip", None)
            if example is None:
                raise ValidationException(
                    f"plugin.spec is missing input example for {v}"
                )
            else:
                if isinstance(example, list):
                    example = f"{example}".replace("'", '"')

                if isinstance(default_, list):
                    default_ = f"{default_}".replace("'", '"')

                if isinstance(enum, list):
                    enum = f"{enum}".replace("'", '"')

                action_input.append(
                    f"|{name_}|{type_}|{default_}|{required}|{description}|{enum}|{example}|{placeholder}|{tooltip}|"
                )
        return action_input

    @staticmethod
    def get_spec_output(output_content: dict) -> list:
        action_output = []
        for k, v in output_content.items():
            name_ = k
            type_ = output_content.get(k, {}).get("type")
            required = output_content.get(k, {}).get("required", False)
            description = output_content.get(k, {}).get("description", None)
            example = output_content.get(k, {}).get("example", None)
            if example is None and ExampleOutputDataType.is_valid(type_):
                raise ValidationException(
                    f"plugin.spec is missing output example for {v}"
                )
            else:
                if isinstance(example, list):
                    example = f"{example}".replace("'", '"')
                action_output.append(
                    f"|{name_}|{type_}|{required}|{description}|{example}|"
                )
        return action_output

    def validate(self, spec):
        HelpInputOutputValidator.raw_help = spec.raw_help()
        raw_spec_yaml = spec.spec_dictionary()
        process_type = ["actions", "triggers", "tasks"]
        HelpInputOutputValidator.violated = 0
        for p_type in process_type:
            actions = raw_spec_yaml.get(p_type, {})
            for key, value in actions.items():
                action_name = actions[key].get("title")
                input_section = actions[key].get("input")
                output_section = actions[key].get("output")
                HelpInputOutputValidator.action_missing = 0

                # Action with no input in spec file will skip input validation
                if input_section:
                    action_input_fields = HelpInputOutputValidator.get_spec_input(
                        input_section
                    )
                    HelpInputOutputValidator.validate_input(
                        action_name, action_input_fields, p_type
                    )

                    if HelpInputOutputValidator.violations:
                        print(
                            f'{YELLOW}Input violations: {p_type[:-1].capitalize()} -> "{action_name}": Missing {HelpInputOutputValidator.violations} in help.md{RESET_ALL}'
                        )
                        HelpInputOutputValidator.violations = []
                        HelpInputOutputValidator.violated = 1

                # Actions with no output in spec file will skip output validation.
                # Also, skip output validation for actions not found in help.md
                if output_section and not HelpInputOutputValidator.action_missing:
                    action_output_fields = HelpInputOutputValidator.get_spec_output(
                        output_section
                    )
                    HelpInputOutputValidator.validate_output(
                        action_name, action_output_fields, p_type
                    )

                    if HelpInputOutputValidator.violations:
                        print(
                            f'{YELLOW}Output violations: {p_type[:-1].capitalize()}-> "{action_name}": Missing {HelpInputOutputValidator.violations} in help.md{RESET_ALL}'
                        )
                        HelpInputOutputValidator.violations = []
                        HelpInputOutputValidator.violated = 1
        if HelpInputOutputValidator.violated:
            raise ValidationException(
                "Help.md is not in sync with plugin.spec.yaml. Please regenerate help.md by running 'insight-plugin "
                "refresh' to rectify violations. "
            )
