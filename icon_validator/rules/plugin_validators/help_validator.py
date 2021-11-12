import re

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class HelpValidator(KomandPluginValidator):
    taskExist = False

    HELP_HEADERS_LIST = [
        "# Description",
        "# Key Features",
        "# Requirements",
        "# Documentation",
        "## Setup",
        "## Technical Details",
        "### Actions",
        "### Triggers",
        "### Custom Output Types",
        "## Troubleshooting",
        "# Version History",
        "# Links",
        "## References"
    ]

    @staticmethod
    def validate_help_exists(spec):
        if "help" in spec:
            raise ValidationException("Help section should exist in help.md and not in the plugin.spec.yaml file.")

    @staticmethod
    def validate_version_history(help_str):
        if "- Initial plugin" not in help_str:
            raise ValidationException("Initial plugin version line is missing: 1.0.0 - Initial plugin.")

        if "Support web server mode" not in help_str and "1.0.0 - Initial plugin" not in help_str:
            # Match legacy versioning which indicates this plugin came before web server mode existed
            if "* 0." in help_str:
                # Takes advantage of the fact that versioning used to start from 0.1.0 instead of 1.0.0
                raise ValidationException(
                    "Initial plugin was released prior to schema V2 but versioning history."
                    "does not document the upgrade to web server mode: Support web server mode."
                )

    @staticmethod
    def validate_same_actions_title(spec, help_):
        if "actions" in spec:
            HelpValidator.validate_same_actions_loop(spec["actions"], help_)
        if "triggers" in spec:
            HelpValidator.validate_same_actions_loop(spec["triggers"], help_)
        if "tasks" in spec:
            HelpValidator.validate_same_actions_loop(spec["tasks"], help_)

    @staticmethod
    def validate_same_actions_loop(section, help_str):
        for i in section:
            if "title" in section[i]:
                if f"#### {section[i]['title']}" not in help_str:
                    raise ValidationException(f"Help section is missing title of: #### {section[i]['title']}")

    @staticmethod
    def remove_example_output(help_content):
        example_outputs = re.findall(r"Example output:\n\n```\n.*?```\n\n", help_content, re.DOTALL)
        for example_output in example_outputs:
            help_content = help_content.replace(example_output, "")
        return help_content

    @staticmethod
    def validate_title_spelling(spec, help_):
        if "title" in spec:
            title = spec["title"]
            lower_title = title.lower()
            help_ = HelpValidator.remove_example_output(help_)
            for line in help_.split("\n"):
                lower_line = line.lower()
                if lower_title in lower_line:
                    if title not in line:
                        if lower_line[lower_line.find(title.lower()) - 1].isspace():
                            if line.startswith("$"):
                                pass
                            elif line.startswith(">>>"):
                                pass
                            else:
                                raise ValidationException(
                                    "Help section contains non-matching title in line: {}".format(line))

    @staticmethod
    def validate_help_headers(help_str):
        # if plugin without tasks needs not to be regenerated, help.md won't be having Tasks section
        # Only raise exception if plugin.spec.yaml contains task and help.md does not
        if HelpValidator.taskExist and "### Tasks" not in help_str:
            raise ValidationException("Help section is missing header: ### Tasks")

        help_headers_errors = []
        for header in HelpValidator.HELP_HEADERS_LIST:
            if header not in help_str:
                help_headers_errors.append(f"Help section is missing header: {header}")

        if help_headers_errors:
            raise ValidationException("\n".join(help_headers_errors))

    @staticmethod
    def validate_duplicate_headings(help_raw: str):
        header_errors = []
        for header in HelpValidator.HELP_HEADERS_LIST:
            normalize_header = header.strip(" #")
            pattern = re.compile(f"#[ ]*{normalize_header}")
            if len(pattern.findall(help_raw)) > 1:
                header_errors.append(f"Please check {header} headings and remove duplicates.")

        if header_errors:
            joined_errors = "\n".join(header_errors)
            raise ValidationException(f"More than one headings in type was found. \n{joined_errors}")

    def validate(self, spec):
        HelpValidator.validate_help_exists(spec.spec_dictionary())
        HelpValidator.validate_help_headers(spec.raw_help())
        if spec.spec_dictionary().get("tasks"):
            HelpValidator.taskExist = True
        HelpValidator.validate_version_history(spec.raw_help())
        HelpValidator.validate_same_actions_title(spec.spec_dictionary(), spec.raw_help())
        HelpValidator.validate_title_spelling(spec.spec_dictionary(), spec.raw_help())
        HelpValidator.validate_duplicate_headings(spec.raw_help())
