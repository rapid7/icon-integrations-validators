import os
import json
from icon_validator.workflow.model import Workflow
from pydantic import parse_obj_as

def read_workflow(spec: dict, file_name: str) -> Workflow:
    """
    read_workflow takes a raw file and tries to load into a Workflow dataclass
    :param spec: workflow spec
    :param file_name: workflow file ending in kom or icon
    :return: Workflow dataclass
    """
    with open(os.path.join(spec.directory, file_name)) as workflow_file:
        try:
            wf = json.load(workflow_file)
        except Exception as e:
            raise Exception('Unable to read workflow', e)
        return parse_obj_as(Workflow, wf)


