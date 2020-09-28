import re

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class HelpValidator(KomandPluginValidator):
    taskExist = False

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
                                raise ValidationException("Help section contains non-matching title in line: {}".format(line))

    @staticmethod
    def validate_help_headers(help_str):
        if "# Description" not in help_str:
            raise ValidationException("Help section is missing header: # Description")
        if "# Key Features" not in help_str:
            raise ValidationException("Help section is missing header: # Key Features")
        if "# Requirements" not in help_str:
            raise ValidationException("Help section is missing header: # Requirements")
        if "# Documentation" not in help_str:
            raise ValidationException("Help section is missing header: # Documentation")
        if "## Setup" not in help_str:
            raise ValidationException("Help section is missing header: ## Setup")
        if "## Technical Details" not in help_str:
            raise ValidationException("Help section is missing header: ## Technical Details")
        if "### Actions" not in help_str:
            raise ValidationException("Help section is missing header: ### Actions")
        if "### Triggers" not in help_str:
            raise ValidationException("Help section is missing header: ### Triggers")
        # if plugin without tasks needs not to be regenerated, help.md won't be having Tasks section
        # Only raise exception if plugin.spec.yaml contains task and help.md does not
        if HelpValidator.taskExist and "### Tasks" not in help_str:
            raise ValidationException("Help section is missing header: ### Tasks")
        if "### Custom Output Types" not in help_str:
            raise ValidationException("Help section is missing header: ### Custom Output Types")
        if "## Troubleshooting" not in help_str:
            raise ValidationException("Help section is missing header: ## Troubleshooting")
        if "# Version History" not in help_str:
            raise ValidationException("Help section is missing header: # Version History")
        if "# Links" not in help_str:
            raise ValidationException("Help section is missing header: # Links")
        if "## References" not in help_str:
            raise ValidationException("Help section is missing header: ## References")

    def validate(self, spec):
        HelpValidator.validate_help_exists(spec.spec_dictionary())
        HelpValidator.validate_help_headers(spec.raw_help())
        if spec.spec_dictionary().get("tasks"):
            HelpValidator.taskExist = True
        HelpValidator.validate_version_history(spec.raw_help())
        HelpValidator.validate_same_actions_title(spec.spec_dictionary(), spec.raw_help())
        HelpValidator.validate_title_spelling(spec.spec_dictionary(), spec.raw_help())
