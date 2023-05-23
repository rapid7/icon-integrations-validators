from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException
from icon_validator.rules.lists.lists import title_validation_list
import os
import json


class WorkflowTitleValidator(KomandPluginValidator):

    @staticmethod
    def validate_title(title, file_type):
        if not isinstance(title, str):
            raise ValidationException(f"Title must not be blank in {file_type} file.")
        if title == "":
            raise ValidationException(f"Title must not be blank in {file_type} file.")
        if title.endswith("."):
            raise ValidationException(f"Title ends with period when it should not in {file_type} file.")
        if title[0].islower():
            # This plugin title is OK: minFraud
            # This plugin title is OK: ifconfig.co
            raise ValidationException(f"Title should not start with a lower case letter in {file_type} file.")
        if title[0].isspace():
            raise ValidationException(f"Title should not start with a whitespace character in {file_type} file.")
        for word in title.split():
            if not title.startswith(word):
                if word in title_validation_list:
                    raise ValidationException(f"Title contains a capitalized '{word}' when it should not in {file_type} file.")
                elif "By" == word and not title.endswith("By"):
                    # This is OK: Order By
                    # This is NOT OK: Search By String
                    raise ValidationException(f"Title contains a capitalized 'By' when it should not in {file_type} file.")
                elif "Of" == word and not title.endswith("Of"):
                    # This is OK: Member Of
                    # This is NOT OK: Type Of String
                    raise ValidationException(f"Title contains a capitalized 'Of' when it should not in {file_type} file.")
                elif not word[0].isupper() and not word.capitalize() in title_validation_list:
                    if not word.isnumeric():
                        if word.lower() not in ("by", "of", "-"):
                            raise ValidationException(f"Title contains a lowercase '{word}' when it should not in {file_type} file.")

    @staticmethod
    def get_icon_steps(spec):
        icon_file = spec.directory
        for file_name in os.listdir(icon_file):
            if file_name.endswith(".icon"):
                data = dict()
                with open(f"{icon_file}/{file_name}") as json_file:
                    try:
                        data = json.load(json_file)
                    except json.JSONDecodeError:
                        raise ValidationException("ICON file is not in JSON format try exporting the .icon file again")
                workflow_versions = data.get("kom", {}).get("workflowVersions", [])
                if workflow_versions:
                    return workflow_versions[0].get("steps")

        raise ValidationException("ICON file is not in JSON format try exporting the .icon file again")

    @staticmethod
    def validate_icon_titles(spec):
        steps = WorkflowTitleValidator.get_icon_steps(spec).values()
        for step in steps:
            WorkflowTitleValidator.validate_title(step.get("name"), ".icon")

    @staticmethod
    def get_title_from_spec(spec):
        if "title" not in spec.spec_dictionary():
            raise ValidationException("Workflow title is missing.")

        return spec.spec_dictionary()["title"]

    def validate(self, spec):
        """
        Checks that title is not blank.
        Checks that title does not end with a period.
        Checks that title does not start with a lower case letter.
        Checks that title does not start with a space.
        Checks that title is 6 words or less.
        Checks that title is properly capitalized.
        """
        self.validate_title(self.get_title_from_spec(spec), ".spec")
        self.validate_icon_titles(spec)
