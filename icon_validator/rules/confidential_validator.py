from .validator import KomandPluginValidator
from icon_plugin_spec.plugin_spec import KomandPluginSpec

import re


class ConfidentialValidator(KomandPluginValidator):
    emails = ["user@example.com"]
    violations = []

    def __init__(self):
        super().__init__()
        ConfidentialValidator.name = "ConfidentialValidator"

    # Search help file line by line for emails not in allowed list
    @staticmethod
    def validate_help(plugin_path: str):
        email_pattern = "[^@]+@[^@]+\.[^@]+"
        with open(f"{plugin_path}/help.md") as h:
            help_lines: [str] = h.readlines()

        for i in range(0, len(help_lines)):
            matches = re.findall(email_pattern, help_lines[i])
            for match in matches:
                if match not in ConfidentialValidator.emails:
                    ConfidentialValidator.violations.append(f"help.md, {i + 1}")
                    break

    # Search code base for confidential info
    @staticmethod
    def validate_code(plugin_path: str):
        pass

    # Search tests line by line for emails not in allowed list
    @staticmethod
    def validate_tests(plugin_path: str):
        pass

    def validate(self, spec: KomandPluginSpec):
        ConfidentialValidator.validate_help(spec.directory)
        ConfidentialValidator.validate_code(spec.directory)
        ConfidentialValidator.validate_tests(spec.directory)

        if len(ConfidentialValidator.violations):
            raise Exception(f"Please use 'user@example.com' when including emails. The following violated this:"
                            f"{ConfidentialValidator.violations}")
