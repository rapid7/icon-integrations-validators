from typing import List, Optional, Type, Union
from dataclasses import dataclass, field


# Kom/Icon file
@dataclass
class TriggersInputActorProperties:
    assets: dict = field(default_factory=lambda: {})
    users: dict = field(default_factory=lambda: {})


@dataclass
class TriggersInputActor:
    properties: TriggersInputActorProperties = TriggersInputActorProperties
    title: str = ""
    type: str = ""


@dataclass
class TriggersDefinitions:
    actor: TriggersInputActor = TriggersInputActor
    asset: dict = field(default_factory=lambda: {})
    user: dict = field(default_factory=lambda: {})


@dataclass
class TriggersInputJsonSchema:
    definitions: dict = field(default_factory=lambda: {})
    properties: dict = field(default_factory=lambda: {})
    title: str = ""
    type: str = ""


@dataclass
class Trigger:
    id: str = ""
    name: str = ""
    description: str = ""
    input: Optional[dict] = field(default_factory=lambda: {})
    inputJsonSchema: TriggersInputJsonSchema = TriggersInputJsonSchema
    outputJsonSchema: dict = field(default_factory=lambda: {})
    type: str = ""


@dataclass
class WorkflowVersionGraph:
    edges: dict = field(default_factory=lambda: {})
    nodes: dict = field(default_factory=lambda: {})


@dataclass
class WorkflowVersion:
    id: str = ""
    workflowId: str = ""
    name: str = ""
    tags: Optional[List[str]] = field(default_factory=lambda: [])
    type: str = ""
    version: str = ""
    description: str = ""
    meta: dict = field(default_factory=lambda: {})
    graph: WorkflowVersionGraph = WorkflowVersionGraph
    steps: dict = field(default_factory=lambda: {})
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


@dataclass
class Kom:
    workflowVersions: List[WorkflowVersion] = field(
        default_factory=lambda: [WorkflowVersion]
    )
    triggers: List[Trigger] = field(default_factory=lambda: [Trigger])
    komandVersion: str = ""
    komFileVersion: str = ""
    exportedAt: str = ""

    def get_latest_workflow_version(
        self,
    ) -> Union[Type[WorkflowVersion], WorkflowVersion]:
        if len(self.workflowVersions) <= 0:
            return WorkflowVersion
        return self.workflowVersions[0]


@dataclass
class Workflow:
    kom: Kom


# Workflow Spec
@dataclass
class WorkflowSpec:
    status: List[str]
    tags: List[str]
    name: str = ""
    title: str = ""
    description: str = ""
    version: str = ""
    vendor: str = ""
    support: str = ""


@dataclass
class Plugin:
    name: str = ""
    version: str = ""
