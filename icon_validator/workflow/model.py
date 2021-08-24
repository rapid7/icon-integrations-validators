from typing import List, Optional, Type, Union
from dataclasses import field
from pydantic import BaseModel


# Kom/Icon file

class PropertiesType(BaseModel):
    description: str = ""
    order: int = 0
    title: str = ""
    type: str = ""

class PropertiesTimeStamp(BaseModel):
    description: str = ""
    order: int = 0
    title: str = ""
    type: str = ""

class PropertiesMessage(BaseModel):
   ref: str = ""
   description: str = ""
   order: int = 0
   title: str = ""

class TriggersOutputJsonSchemaProperties(BaseModel):
    message: PropertiesMessage = PropertiesMessage
    timeStamp: PropertiesTimeStamp = PropertiesTimeStamp
    type: PropertiesType = PropertiesType

class UserId(BaseModel):
    description: str = ""
    order: int = 0
    title: str = ""
    type: str = ""

class PropertiesUser(BaseModel):
    description: str = ""
    order: int = 0
    title: str = ""
    type: str = ""

class PropertiesTs(BaseModel):
    description: str = ""
    order: int = 0
    title: str = ""
    type: str = ""

class PropertiesText(BaseModel):
    description: str = ""
    order: int = 0
    title: str = ""
    type: str = ""

class ChannelId(BaseModel):
    description: str = ""
    order: int = 0
    title: str = ""
    type: str = ""

class PropertiesChannel(BaseModel):
    description: str = ""
    order: int = 0
    title: str = ""
    type: str = ""

class Channel(BaseModel):
    description: str = ""
    order: int = 0
    title: str = ""
    type: str = ""

class MessageProperties(BaseModel):
    channel: Channel = Channel
    channel_id: ChannelId = ChannelId
    text: PropertiesText = PropertiesText
    ts: PropertiesTs = PropertiesTs
    user:PropertiesUser = PropertiesUser
    user_id: UserId = UserId

class Message(BaseModel):
    properties: MessageProperties = MessageProperties
    title: str = ""
    type: str = ""

class OutputJsonSchemaProperties(BaseModel):
    message: Message = Message

class Definitions(BaseModel):
    message: Message = Message

class Type(BaseModel):
    default: str = ""
    description: str = ""
    enum: List = []
    order: str = ""
    title: str = ""
    type: str = ""

class MatchText(BaseModel):
    description: str = ""
    order: int = 0
    title: str = ""
    type: str = ""

class MatchChannel(BaseModel):
    description: str = ""
    order: int = 0
    title: str = ""
    type: str = ""

class TriggersInputJsonSchemaProperties(BaseModel):
    matchChannel: MatchChannel = MatchChannel
    matchText: dict = {}
    type: dict = {}

class TriggersOutputJsonSchema(BaseModel):
    definitions: Definitions = Definitions
    properties: OutputJsonSchemaProperties = OutputJsonSchemaProperties
    title: str = ""
    type: str = ""

class TriggersInputJsonSchema(BaseModel):
    properties: MatchChannel = MatchChannel
    required: List = []
    title: str = ""
    type: str = ""

class TriggerInput(BaseModel):
    matchChannel: str = ""
    matchText: str = ""
    type: str = ""

class Trigger(BaseModel):
    id: str = ""
    name: str = ""
    description: str = ""
    input: Optional[TriggerInput] = [TriggerInput]
    inputJsonSchema: TriggersInputJsonSchema = TriggersInputJsonSchema
    outputJsonSchema: TriggersOutputJsonSchema = TriggersOutputJsonSchema
    tags: List = []
    type: str = ""
    chatOpsAppName: str = ""
    chatOpsAppIdentifier: str = ""


class WorkflowVersionGraph(BaseModel):
    edges: dict = {}
    nodes: dict = {}

class WorkflowVersion(BaseModel):
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
