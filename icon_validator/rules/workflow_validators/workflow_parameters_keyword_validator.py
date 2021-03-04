from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException
import os
import json


class WorkflowParametersKeywordValidator(KomandPluginValidator):

    @staticmethod
    def are_parameters_present_in_icon_file(spec):
        for file_name in os.listdir(spec.directory):
            if file_name.endswith(".icon"):
                icon_content = WorkflowParametersKeywordValidator.read_icon(spec, file_name)

        # Grab the most recent WF version out of the icon file and see if it has parameters
        try:
            workflow_version = icon_content.get("kom").get("workflowVersions")[0]
            workflow_version_keys = list(workflow_version.keys())
        except Exception as e:
            raise ValidationException("The .icon workflow file may be corrupt, could not validate keys.")

        # See if we have a parameters section in the WF and verify it isn't empty
        if "parameters" in workflow_version_keys:
            parameters = workflow_version.get("parameters")
            if parameters:
                return True
        return False

    @staticmethod
    def read_icon(spec, file_name):
        with open(os.path.join(spec.directory, file_name)) as icon_file:
            return json.load(icon_file)

    def validate(self, spec):
        if self.are_parameters_present_in_icon_file(spec):
            spec_dictionary = spec.spec_dictionary()
            keywords = spec_dictionary.get("hub_tags", {}).get("keywords", [])
            if not "parameters" in keywords:
                raise ValidationException("The workflow uses parameters, however the parameters "
                                          "keyword is not present in workflow.spec.yaml keywords")
