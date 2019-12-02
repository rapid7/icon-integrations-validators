from .validator import KomandPluginValidator
import re
from icon_validator.styling import *
from distutils.version import LooseVersion


class ChangelogValidator(KomandPluginValidator):

    @staticmethod
    def get_versions(help_content):
        raw_versions = re.findall(r'Version History\n\n.*?\n\n', help_content, re.DOTALL)
        if not raw_versions:
            raise Exception("Incorrect Version History in help.md")

        versions_history = raw_versions[0].replace('Version History\n\n', '').replace('\n\n', '').split('\n')
        return versions_history

    @staticmethod
    def validate_version_numbers(versions_history):
        violations = 0
        for version in versions_history:
            version_number = version.split(" - ")
            version_found = re.findall(r'^\*\s\d+\.\d+\.\d+$', version_number[0])

            if not version_found:
                print(f"{YELLOW}violation: Invalid version {version_number[0].replace('* ','')} in help.md{RESET_ALL}")
                violations = 1

        if violations:
            raise Exception(f"Incorrect version numbers specified as stated above in help.md")

    @staticmethod
    def validate_order(versions_history):
        versions = []

        for version in versions_history:
            version_number = version.split(" - ")[0]
            versions.append(version_number)

        sorted_versions = sorted(versions, key=LooseVersion, reverse=True)

        if versions != sorted_versions:
            print(f"{YELLOW} Version numbers in help.md are not sorted in descending order{RESET_ALL}")
            raise Exception("Version numbers in help.md need to be in descending order")

    def validate(self, spec):
        versions_history = ChangelogValidator.get_versions(spec.raw_help())
        ChangelogValidator.validate_version_numbers(versions_history)
        ChangelogValidator.validate_order(versions_history)
