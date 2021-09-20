from loguru import logger
from .template_validators import RegionWorkflowIDValidator


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