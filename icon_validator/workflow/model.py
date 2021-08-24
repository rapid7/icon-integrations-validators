from typing import List, Optional, Type, Union
from dataclasses import field
from pydantic import BaseModel


# Kom/Icon file
class Trigger(BaseModel):
    id: str = ""
    name: str = ""
    description: str = ""
    input: dict = {}
    inputJsonSchema: dict = {}
    outputJsonSchema: dict = {}
    tags: List = []
    type: str = ""
    chatOpsAppName: str = ""
    chatOpsAppIdentifier: str = ""


class WorkflowVersionGraph(BaseModel):
    edges: dict = {}
    nodes: dict = {}

class WorkflowVersion(BaseModel):
    id: str = ""
    name: str = ""
    type: str = ""
    version: str = ""
    description: str = ""
    graph: WorkflowVersionGraph = WorkflowVersionGraph
    steps: dict = {}
    tags: Optional[List[str]] = []
    humanCostSeconds: int = 0
    humanCostDisplayUnit: str = ""

    def get_steps_contents(self) -> List[dict]:
        """
        get_step_contents parses the workflow version steps and grabs the
        contents of each step
        :return:  List of step contents as dictionaries
        """
        content = []
        for step, value in self.steps.items():
            content.append(value)
        return content

    def get_plugin_steps(self) -> List[dict]:
        """
        get_plugin_steps filters a collection of steps that contain the use of
        a plugin
        :return: List of steps that contain a plugin
        """
        steps = []
        steps_content = self.get_steps_contents()
        for content in steps_content:
            if "plugin" in content.keys():
                steps.append(content)
        return steps

    def get_plugins_used(self) -> List[dict]:
        """
        get_plugins_used fetches a collection of  dicts containing node name
         and the plugin used in that node
        :return: List of dicts containing 'node_name' and 'plugin_name'
        """
        plugins = []
        plugin_steps = self.get_plugin_steps()
        for step in plugin_steps:
            plugins.append(
                {"plugin_name": step["plugin"]["name"], "node_name": step["name"]}
            )
        return plugins

class Kom(BaseModel):
    workflowVersions: List[WorkflowVersion] = [WorkflowVersion]
    triggers: List[Trigger] = [Trigger]
    komandVersion: str = ""
    komFileVersion: str = ""
    exportedAt: str = ""

    def get_latest_workflow_version(
            self,
    ) -> WorkflowVersion:
        if len(self.workflowVersions) <= 0:
            return WorkflowVersion
        return self.workflowVersions[0]


class Workflow(BaseModel):
    kom: Kom

# Workflow Spec
class WorkflowSpec(BaseModel):
    status: List[str]
    tags: List[str]
    name: str = ""
    title: str = ""
    description: str = ""
    version: str = ""
    vendor: str = ""
    support: str = ""

class Plugin(BaseModel):
    name: str = ""
    version: str = ""
