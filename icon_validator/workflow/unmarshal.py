import os
import json
from icon_validator.workflow.model import Workflow
from icon_plugin_spec.plugin_spec import KomandPluginSpec
from pydantic import parse_obj_as


def read_workflow(spec: KomandPluginSpec, file_name: str = None) -> Workflow:
    """
    read_workflow takes a raw file and tries to load into a Workflow pydantic model
    :param spec: workflow spec
    :param file_name: workflow file ending in kom or icon
    :return: Workflow dataclass
    """

    if not file_name:
        directory = os.listdir(spec.directory)
        for f in directory:
            if f.endswith(".icon"):
                file_name = f
        if not file_name:
            print("Not found")

    with open(os.path.join(spec.directory, file_name)) as workflow_file:
        try:
            wf = json.load(workflow_file)
            return parse_obj_as(Workflow, wf)
        except Exception as e:
            raise Exception('Unable to read and parse workflow', e)



