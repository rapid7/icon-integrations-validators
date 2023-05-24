from typing import List


class ExampleOutputDataType:
    boolean = "boolean"
    integer = "integer"
    float = "float"
    string = "string"
    date = "date"
    bytes = "bytes"
    password = "password"
    file = "file"

    @classmethod
    def list(cls) -> List[str]:
        return [type_ for type_ in ExampleOutputDataType.__dict__.keys() if not type_.startswith("__")]

    @classmethod
    def is_valid(cls, arg: str) -> bool:
        return arg in cls.list()
