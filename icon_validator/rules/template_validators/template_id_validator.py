from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException
from icon_validator.workflow.model import Workflow
from icon_validator.workflow.unmarshal import read_workflow


class TemplateIDValidator(KomandPluginValidator):

    @staticmethod
    def id_exists(workflow: Workflow):
        if workflow.kom.workflowVersions[0].id:
            return True
        return False

    def validate(self, spec):
        """
        Validates template ensuring ID
        """
        wf: Workflow = read_workflow(spec=spec)

        if not self.id_exists(workflow=wf):
            raise ValidationException(
                "Template Validator: Template missing ID"
            )

