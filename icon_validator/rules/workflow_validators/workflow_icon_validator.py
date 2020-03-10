from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException

import os
import json


class WorkflowICONFileValidator(KomandPluginValidator):

    @staticmethod
    def validate_workflow_versions_steps(step, value):
        try:
            if value["nodeId"] != step:
                raise ValidationException(
                    f"The nodeId key in {step} is not defined. Try exporting the .icon file again")
        except KeyError:
            raise ValidationException(
                f"ICON file is missing the nodeId key in {step}. Try exporting the .icon file again")

        try:
            if value["name"] is None or value["name"] == "":
                raise ValidationException(
                    f"The name key in {step} is not defined. Try exporting the .icon file again")
        except KeyError:
            raise ValidationException(
                f"ICON file is missing the name key in {step}. Try exporting the .icon file again")

        try:
            if value["type"] is None or value["type"] == "":
                raise ValidationException(
                    f"The type key in {step} is not defined. Try exporting the .icon file again")
        except KeyError:
            raise ValidationException(
                f"ICON file is missing the type key in {step}. Try exporting the .icon file again")

        # Must be a bool value
        try:
            if not isinstance(value["continueOnFailure"], bool):
                raise ValidationException(
                    f"The continueOnFailure key in {step} is not defined. Try exporting the .icon file again")
        except KeyError:
            raise ValidationException(
                f"ICON file is missing the continueOnFailure key in {step}. Try exporting the .icon file again")

        # Must be a bool value
        try:
            if not isinstance(value["continueOnFailure"], bool):
                raise ValidationException(
                    f"The isDisabled key in {step} is not defined. Try exporting the .icon file again")
        except KeyError:
            raise ValidationException(
                f"ICON file is missing the isDisabled key in {step}. Try exporting the .icon file again")

    @staticmethod
    def validate_workflow_versions(workflow_versions):
        try:
            if workflow_versions["name"] is None or workflow_versions["name"] == "":
                raise ValidationException(
                    "The name key in workflowVersions is not defined. Try exporting the .icon file again")
        except KeyError:
            raise ValidationException(
                "ICON file is missing the name key in workflowVersions. Try exporting the .icon file again")

        try:
            if workflow_versions["type"] is None or workflow_versions["type"] == "":
                raise ValidationException(
                    "The type key in workflowVersions is not defined. Try exporting the .icon file again")
        except KeyError:
            raise ValidationException(
                "ICON file is missing the type key in workflowVersions. Try exporting the .icon file again")

        # The version key may be a blank string
        try:
            if workflow_versions["version"] is None:
                raise ValidationException(
                    "The version key in workflowVersions is not defined. Try exporting the .icon file again")
        except KeyError:
            raise ValidationException(
                "ICON file is missing the version key in workflowVersions. Try exporting the .icon file again")

        # The description key may be a blank string
        try:
            if workflow_versions["description"] is None:
                raise ValidationException(
                    "The description key in workflowVersions is not defined. Try exporting the .icon file again")
        except KeyError:
            raise ValidationException(
                "ICON file is missing the description key in workflowVersions. Try exporting the .icon file again")

        # The tags key may be None or a list
        try:
            if workflow_versions["tags"] is not None and not isinstance(workflow_versions["tags"], list):
                raise ValidationException(
                    "The description tags in workflowVersions is not defined. Try exporting the .icon file again")
        except KeyError:
            raise ValidationException(
                "ICON file is missing the tags key in workflowVersions. Try exporting the .icon file again")

        for step, value in workflow_versions["steps"].items():
            WorkflowICONFileValidator.validate_workflow_versions_steps(step, value)

    @staticmethod
    def validate_triggers(triggers):
        try:
            if triggers["id"] is None or triggers["id"] == "":
                raise ValidationException(
                    "The id key in triggers is not defined. Try exporting the .icon file again")
        except KeyError:
            raise ValidationException(
                "ICON file is missing the id key in triggers. Try exporting the .icon file again")

        try:
            if triggers["name"] is None or triggers["name"] == "":
                raise ValidationException(
                    "The name key in triggers is not defined. Try exporting the .icon file again")
        except KeyError:
            raise ValidationException(
                "ICON file is missing the name key in triggers. Try exporting the .icon file again")

        # Description can be blank string
        try:
            if triggers["description"] is None:
                raise ValidationException(
                    "The description key in triggers is not defined. Try exporting the .icon file again")
        except KeyError:
            raise ValidationException(
                "ICON file is missing the description key in triggers. Try exporting the .icon file again")

    def validate(self, spec):
        d = spec.directory
        for file_name in os.listdir(d):
            if file_name.endswith(".icon"):
                data = dict()
                with open(f"{d}/{file_name}") as json_file:
                    try:
                        data = json.load(json_file)
                    except json.JSONDecodeError:
                        raise ValidationException("ICON file is not in JSON format try exporting the .icon file again")

                try:
                    data = data["kom"]
                except KeyError:
                    raise ValidationException("ICON file is missing the kom key. Try exporting the .icon file again")

                try:
                    if data["komandVersion"] is None or data["komandVersion"] == "":
                        raise ValidationException(
                            "The komandVersion key is not defined. Try exporting the .icon file again")
                except KeyError:
                    raise ValidationException(
                        "ICON file is missing the komandVersion key. Try exporting the .icon file again")

                try:
                    if data["komFileVersion"] is None or data["komFileVersion"] == "":
                        raise ValidationException(
                            "The komFileVersion key is not defined. Try exporting the .icon file again")
                except KeyError:
                    raise ValidationException(
                        "ICON file is missing the komFileVersion key. Try exporting the .icon file again")

                try:
                    if data["exportedAt"] is None or data["exportedAt"] == "":
                        raise ValidationException(
                            "The exportedAt key is not defined. Try exporting the .icon file again")
                except KeyError:
                    raise ValidationException(
                        "ICON file is missing the exportedAt key. Try exporting the .icon file again")

                try:
                    workflow_versions = data["workflowVersions"]
                except KeyError:
                    raise ValidationException(
                        "ICON file is missing the workflowVersions key. Try exporting the .icon file again")
                try:
                    triggers = data["triggers"]
                except KeyError:
                    raise ValidationException(
                        "ICON file is missing the triggers key. Try exporting the .icon file again")

                for item in workflow_versions:
                    WorkflowICONFileValidator.validate_workflow_versions(item)

                for item in triggers:
                    WorkflowICONFileValidator.validate_triggers(item)