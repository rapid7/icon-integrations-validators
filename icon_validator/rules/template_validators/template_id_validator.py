import os
import json
from typing import List
from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException
from icon_validator.workflow.marshal import read_workflow
from icon_validator.workflow.model import Workflow
from icon_validator.styling import YELLOW

class TemplateIDValidator(KomandPluginValidator):

    def id_exists(self, workflow: Workflow):
        if workflow.kom.workflowVersions[0].id:
            return True
        return False

    def validate(self, spec):
        """
        Validates template ensuring ID
        """
        wf = Workflow
        d = spec.directory
        for file_name in os.listdir(d):
            if file_name.endswith(".icon"):
                try:
                    wf = read_workflow(spec=spec, file_name=file_name)
                except json.JSONDecodeError:
                    raise ValidationException(
                        "ICON file is not in JSON format, try exporting the workflow file again"
                    )
        if not self.id_exists(workflow=wf):
            raise ValidationException(
                "Template Validator: Template missing ID"
            )

