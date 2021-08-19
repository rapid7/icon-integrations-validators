from pydantic import BaseModel


class Tag(BaseModel):
    vendor: str
    plugin_name: str
    semver: str