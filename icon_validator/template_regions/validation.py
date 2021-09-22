"""
Validation module is used to perform validation operation on templates that are being uploaded to ICON to ensure templates are correctly verified.
"""
from icon_validator.workflow.model import Workflow
from abc import ABC
from loguru import logger
from typing import List
import sys
import os
import traceback


class Validator(ABC):
    """Abstract class for a Validator"""

    def __init__(self):
        pass

    @staticmethod
    def run(workflow: Workflow, template: dict, templates: dict) -> str:
        """
        Runs validator on provided workflow, template or templates
        :param workflow: Workflow class
        :param template: single template
        :param templates: collection of templates
        :return: error if validation failed
        """
        pass


class Validate:

    """Main class to run validation"""

    def __init__(self, workflow, template=None, templates=None):
        self.workflow: Workflow = workflow
        self.template: dict = template
        self.templates: dict = templates

    def validate(self, validators: [Validator]) -> (bool, [Exception]):
        """
        validate takes a collection of Validators and runs each validator on a
        workflow, template or templates and returns true if what was validated
        is valid or not.

        A validator should provide an error of why the params validated did not
         pass and what the issue was
        :param validators: Collection of Validator
        :return:
        """
        errors: List[Exception] = []

        for validator in validators:
            logger.info(f"Running Validator: {validator.__name__}")
            # skip WorkflowID validator if new
            # if eval(os.environ.get("ICON_TEMPLATE_NEW").capitalize()) and validator.__name__ == "RegionWorkflowIDValidator":
            #    continue
            try:
                validator.run(workflow=self.workflow, template=self.template, templates=self.templates)
            except Exception as err:
                errors.append(err)
                ex_type, ex, tb = sys.exc_info()
                traceback.print_exception(Exception, err, tb)
                continue
        if errors:
            logger.error("Workflow did not pass validation")
            return False, errors
        return True, []
