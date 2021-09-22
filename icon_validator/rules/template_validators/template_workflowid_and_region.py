"""
Validate workflow ID
"""

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.workflow.model import Workflow
from icon_validator.workflow.unmarshal import read_workflow
import logging



class TemplateWorkflowIDAndRegionValidator(KomandPluginValidator):
    def __init__(self):
        super().__init__()

    @staticmethod
    def run(workflow: Workflow, template: dict = None, templates: dict = None) -> None:
        """
        Runs validator, looks at workflow ID of the workflow and checks the
        provided templates from the target region.
        This is to cover that we are not submitting the same workflow with a
         different workflowID to prevent duplicates templates being pushed to
         the Insight Platform.
        workflow > get ID > Lookup ID in templates > compare > return error
        if ID is different else return ""
        :param workflow: Type Workflow, can be found in models
        :param template: Template
        :param templates: collection of templates from a region
        :return:
        """
        # get workflow info
        workflow_id = workflow.kom.workflowVersions[0].workflowId
        workflow_name = workflow.kom.workflowVersions[0].name

        # get template info
        template = get_template_by_name(name=workflow_name, templates=templates)
        if template:
            template_id = get_template_id(template)
            if workflow_id == template_id:
                logging.info("Workflow ID valid!")
                return
            raise Exception(
                f"Workflow {workflow_name} workflowID didnt match the Template available | Workflow ID {workflow_id} != Template {template_id}"
            )
        raise Exception(f"Unable to find {workflow_name}")


def get_template_by_name(name: str, templates: dict) -> dict:
    """
    Get template by name, looks for the template in list of templates
     by the name provided. The name provided should be from a workflow object
    :param name: Name of template to lookup
    :param templates: a collection of templates
    :return: returns template
    """
    if templates.get("message", ""):
        raise Exception(f"Error: {templates.get('message')}")
    if templates.get("data", ""):
        for template in templates["data"]["workflows"]:
            if template["currentWorkflowVersion"]["name"] == name:
                return template
        return {}


def get_template_id(template: dict) -> str:
    """
    Get template ID takes a template(dict) and returns the workflowID from the
     template.
    :param template: dict of template data thats from a region
    :return: workflowID from the template
    """
    return template["currentWorkflowVersion"]["workflowId"]
