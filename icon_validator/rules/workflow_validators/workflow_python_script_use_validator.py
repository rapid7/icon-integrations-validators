import os
import json
from typing import List
from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException
from icon_validator.workflow.marshal import read_workflow
from icon_validator.workflow.model import Workflow
from icon_validator.styling import YELLOW


class WorkflowPythonScriptUseValidator(KomandPluginValidator):
    @staticmethod
    def python_plugin_used(workflow: Workflow) -> List[dict]:
        """
        python_plugin_used checks if the python plugin is used with node name
        and plugin
        :param workflow: dataclass workflow
        :return: list of steps that use the python plugin
        """
        findings = []
        wf = workflow.kom.get_latest_workflow_version()
        plugins = wf.get_plugins_used()
        for plug in plugins:
            if "Python 3 Script" in plug["plugin_name"]:
                findings.append(plug)
        return findings

    def validate(self, spec):
        """
        Checks if the workflow contains the usage of the python script plugin and warns
        of its use
        """
        wf = dict()
        d = spec.directory
        for file_name in os.listdir(d):
            if file_name.endswith(".icon"):
                try:
                    wf = read_workflow(spec=spec, file_name=file_name)
                except json.JSONDecodeError:
                    raise ValidationException(
                        "ICON file is not in JSON format try exporting the .icon file again"
                    )

        findings = WorkflowPythonScriptUseValidator.python_plugin_used(wf)

        if len(findings) > 0:
            results = f"\t{YELLOW}Python Plugin use found in these steps\n"

            for f in findings:
                results += f'\t\t[-] Step Name - {f["node_name"]}\n'
            results += "\tPlease review these steps carefully before use"
            print(results)
