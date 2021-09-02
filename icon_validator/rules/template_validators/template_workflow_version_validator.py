from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException
from icon_validator.workflow.model import Workflow
from icon_validator.workflow.unmarshal import read_workflow


class TemplateWorkflowVersionValidator(KomandPluginValidator):

    def version_exists(self, wf: Workflow) -> bool:
        if len(wf.kom.workflowVersions) > 0 and wf.kom.workflowVersions[0].version:
            return True
        return False

    def validate(self, spec):
        """
        Validates template ensuring version
        """
        wf: Workflow = read_workflow(spec=spec)

        if not self.version_exists(wf=wf):
            raise ValidationException(
                "Template Validator: Template missing workflow version"
            )
