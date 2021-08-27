from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException
from icon_validator.workflow.model import Workflow
from icon_validator.workflow.unmarshal import read_workflow

class TemplateRegionWorkflowIDValidator(KomandPluginValidator):

    def validate(self, spec):
        wf: Workflow = read_workflow(spec=spec)