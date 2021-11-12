from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException
import os
import json


class WorkflowDescriptionValidator(KomandPluginValidator):

    @staticmethod
    def walk_icon_workflows(spec, callback):
        for file_name in os.listdir(spec.directory):
            if file_name.endswith(".icon"):
                for workflow_version in WorkflowDescriptionValidator.read_icon(spec, file_name)\
                        .get("kom", {})\
                        .get("workflowVersions", []):
                    callback(spec, workflow_version)

    @staticmethod
    def validate_icon_description_exist_callback(spec, workflow_version):
        if "description" not in workflow_version:
            raise ValidationException("Workflow description in workflow .icon file is missing.")

    @staticmethod
    def validate_icon_description_empty_callback(spec, workflow_version):
        if workflow_version.get("description") == "":
            raise ValidationException("Workflow description in workflow .icon file can not be blank")

    @staticmethod
    def validate_icon_description_exists(spec):
        WorkflowDescriptionValidator.walk_icon_workflows(
            spec,
            WorkflowDescriptionValidator.validate_icon_description_exist_callback
        )
        WorkflowDescriptionValidator.walk_icon_workflows(
            spec,
            WorkflowDescriptionValidator.validate_icon_description_empty_callback
        )

    @staticmethod
    def validate_workflow_description_exists(spec):
        if "description" not in spec.spec_dictionary():
            raise ValidationException("Workflow description in yaml is missing.")

        description = spec.spec_dictionary()["description"]
        if description == "":
            raise ValidationException("Workflow description in yaml can not be blank")

    @staticmethod
    def validate_workflow_description_punctuation(description):
        if not description.endswith("."):
            raise ValidationException("Description does not end with a period when it should.")
        if description[0].islower():
            raise ValidationException("Description should not start with a lower case letter.")
        if description[0].isspace():
            raise ValidationException("Description should not start with a whitespace character.")

    def validate(self, spec):
        WorkflowDescriptionValidator.validate_workflow_description_exists(spec)
        WorkflowDescriptionValidator.validate_workflow_description_punctuation(spec.spec_dictionary()["description"])
        WorkflowDescriptionValidator.validate_icon_description_exists(spec)

    @staticmethod
    def read_icon(spec, file_name):
        with open(os.path.join(spec.directory, file_name)) as icon_file:
            return json.load(icon_file)
