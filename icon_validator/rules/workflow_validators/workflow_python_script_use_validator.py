import os
import json
from typing import List
from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException
from icon_validator.workflow.unmarshal import read_workflow
from icon_validator.workflow.model import Workflow
from icon_validator.styling import YELLOW


class WorkflowPythonScriptUseValidator(KomandPluginValidator):

    _PLUGIN_NAME = "Python 3 Script"

    def python_plugin_used(self, workflow: Workflow) -> List[dict]:
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
            if self._PLUGIN_NAME in plug["plugin_name"]:
                findings.append(plug)
        return findings

    def validate(self, spec):
        """
        Checks if the workflow contains the usage of the python script plugin and warns
        of its use
        """
        wf = Workflow
        d = spec.directory
        for file_name in os.listdir(d):
            if file_name.endswith(".icon"):
                try:
                    wf = read_workflow(spec=spec, file_name=file_name)
                except json.JSONDecodeError:
                    raise ValidationException(
                        "ICON file is not in JSON format, try exporting the workflow file again"
                    )

        findings = self.python_plugin_used(workflow=wf)

        if len(findings) > 0:
            results = f"\t{YELLOW}{self._PLUGIN_NAME} use found in these steps\n"

            for f in findings:
                results += f'\t\t[-] Step Name - {f["node_name"]}\n'
            results += "\tPlease review these steps carefully before use"
            print(results)
