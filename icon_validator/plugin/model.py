from typing import List, Optional
from pydantic import BaseModel


class Resources(BaseModel):
    source_url: str
    license_url: str


class HubTags(BaseModel):
    use_cases: List[str]
    keywords: List[str]
    features: List[str]


class Trigger(BaseModel):
    title: str
    description: str
    input: dict
    output: dict


class Input(BaseModel):
    title: str
    type: str
    description: str
    required: bool
    example: str


class Action(BaseModel):
    title: str
    description: str
    input: List[Input] = {}
    output: dict


class Output(BaseModel):
    description: str
    type: str
    required: bool


class Plugin(BaseModel):
    # TODO: types
    # TODO: connection
    plugin_spec_version: str
    extension: str
    products: List[str]
    name: str
    title: str
    description: str
    version: str
    vendor: str
    support: str
    status: List[str]
    resources: Resources
    tags: List[str]
    hub_tags: HubTags
    types: Optional[dict]
    connection: Optional[dict]
    actions: Optional[List[Action]] = []
    triggers: Optional[List[Trigger]] = []