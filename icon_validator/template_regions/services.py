from loguru import logger
from icon_validator.workflow.model import Workflow
from rules.template_validators import TemplateWorkflowIDAndRegionValidator
from template_regions.validation import *


def validate_region_workflowid(workflow: Workflow, templates: dict, force: bool) -> (bool, [str]):
    """
    Validates only the regions workflow ID and the workflow to be updated
    :param workflow: Workflow models
    :param templates: collection of templates
    :param force: to force
    :return: bool if its not valid, list of errors
    """
    if force:
        logger.info("Skipping workflowID validation")
        return True, []
    workflow_validate = Validate(workflow=workflow, templates=templates)
    return workflow_validate.validate(validators=ValidateRegionWorkflowID)