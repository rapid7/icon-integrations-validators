import os
import re

from icon_plugin_spec.plugin_spec import KomandPluginSpec

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class ConfidentialValidator(KomandPluginValidator):
    # emails allowed
    emails = ["user@example.com"]

    # store violations per file
    violations = []

    # Search help file
    @staticmethod
    def validate_help(plugin_path: str):
        with open(f"{plugin_path}/help.md") as h:
            help_lines: [str] = h.readlines()

        ConfidentialValidator.validate_emails(help_lines, "help.md")

    # Check content line by line for emails that validate the rule
    @staticmethod
    def validate_emails(content: [str], path_to_file: str):
        email_pattern = re.compile(r"([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+){0,}")
        for i in range(0, len(content)):
            matches = email_pattern.findall(content[i])
            while "" in matches:
                matches.remove("")
            for match in matches:
                if match not in ConfidentialValidator.emails:
                    ConfidentialValidator.violations.append(f"{path_to_file}, line: {i + 1}")
                    break

    # Search code base
    @staticmethod
    def validate_code(plugin_path: str):
        for path, _, files in os.walk(plugin_path):
            for file in files:
                if file.endswith(".py"):
                    with open(f"{path}/{file}") as f:
                        contents = f.readlines()
                    path_to_file = f"{os.path.relpath(path, plugin_path)}/{file}"
                    ConfidentialValidator.validate_emails(contents, path_to_file)

    # Search tests
    @staticmethod
    def validate_tests(plugin_path: str):
        for path, _, files in os.walk(f"{plugin_path}/tests"):
            for file in files:
                if file.endswith(".json"):
                    with open(f"{path}/{file}") as f:
                        contents = f.readlines()
                    path_to_file = f"{os.path.relpath(path, plugin_path)}/{file}"
                    ConfidentialValidator.validate_emails(contents, path_to_file)

    def validate(self, spec: KomandPluginSpec):
        ConfidentialValidator.validate_help(spec.directory)
        # ConfidentialValidator.validate_code(spec.directory)
        ConfidentialValidator.validate_tests(spec.directory)

        if len(ConfidentialValidator.violations):
            for violation in ConfidentialValidator.violations:
                print(f"violation: {violation}")
            raise ValidationException(f"Please use 'user@example.com' when including emails. The above items violated this.")
