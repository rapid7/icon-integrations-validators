import os
import json
from typing import List
from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException
from icon_validator.workflow.unmarshal import read_workflow
from icon_validator.workflow.model import Workflow
from icon_validator.styling import YELLOW
from icon_validator.workflow.unmarshal import read_workflow

class TemplateIDValidator(KomandPluginValidator):

    def id_exists(self, workflow: Workflow):
        if workflow.kom.workflowVersions[0].id:
            return True
        return False

    def validate(self, spec):
        """
        Validates template ensuring ID
        """
        wf = read_workflow(spec=spec)
        d = spec.directory

        if not self.id_exists(workflow=wf):
            raise ValidationException(
                "Template Validator: Template missing ID"
            )

