import re
from distutils.version import LooseVersion
from icon_validator.exceptions import ValidationException

from icon_validator.styling import *
from icon_validator.rules.validator import KomandPluginValidator


class WorkflowChangelogValidator(KomandPluginValidator):

    @staticmethod
    def get_versions(help_content):
        """
        Extracts the version history from help.md.
        This data is used as input for the validaters.
        """
        raw_versions = re.findall(r"Version History\n\n.*?\n\n", help_content, re.DOTALL)
        if not raw_versions:
            raise ValidationException("Incorrect Version History in help.md.")

        versions_history = raw_versions[0].replace("Version History\n\n", "").replace("\n\n", "").split("\n")
        return versions_history

    @staticmethod
    def validate_version_numbers(versions_history):
        """
        Checks that version history complies with semver format.
        """
        violated = False
        violations = []
        for version in versions_history:
            version_number = version.split(" - ")
            version_found = re.findall(r"^\*\s\d+\.\d+\.\d+$", version_number[0])

            if not version_found:
                violations.append(version_number[0].replace("* ", ""))
                violated = True

        if violated:
            raise ValidationException(f"Incorrect version numbers specified in help.md: {YELLOW}{violations}."
                                      " version numbers must be in semver format."
                                      " See https://semver.org/ for more information.")

    @staticmethod
    def validate_order(versions_history):
        """
        Checks that version history is in descending order.
        """
        versions = []

        for version in versions_history:
            version_number = version.split(" - ")[0]
            versions.append(version_number)

        sorted_versions = sorted(versions, key=LooseVersion, reverse=True)

        if versions != sorted_versions:
            raise ValidationException("Version numbers in help.md are not sorted in descending order.")

    @staticmethod
    def validate_version_history_updated(versions_history, spec):
        """
        Checks that version history has been updated
        """
        violation = True
        spec_version = spec.spec_dictionary()["version"]

        for version_detail in versions_history:
            help_version = re.search(r"^\*\s\d+\.\d+\.\d+$", version_detail.split(" - ")[0])
            if spec_version in help_version.group():
                violation = False
                break

        if violation:
            raise ValidationException(f"Version history of help.md missing version {spec_version}. Please add missing version.")

    def validate(self, spec):
        versions_history = WorkflowChangelogValidator.get_versions(spec.raw_help())
        WorkflowChangelogValidator.validate_version_numbers(versions_history)
        WorkflowChangelogValidator.validate_order(versions_history)
        WorkflowChangelogValidator.validate_version_history_updated(versions_history, spec)
