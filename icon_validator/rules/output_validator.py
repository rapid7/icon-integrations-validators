from .validator import KomandPluginValidator
import os
import json
import importlib
import sys

from jsonschema import validate


class OutputValidator(KomandPluginValidator):
    def __init__(self):
        super().__init__()
        self.missing_outputs = []

    def validate_output(self, action_output, spec_schema, action_name):
        try:
            validate(action_output, spec_schema)
        except Exception as e:
            self.missing_outputs.append((action_name, e))

    @staticmethod
    def get_schemas(spec):
        schemas = {}
        sys.path.append(spec.directory)
        for path, _, files in os.walk(spec.directory):
            for file in files:
                if "schema.py" in file and os.path.basename(path) != "connection":
                    action_name = "".join([str(x.capitalize()) for x in os.path.basename(path).split("_")])
                    full_path = os.path.join(path, file)
                    full_path = full_path.split(os.path.basename(spec.directory), 1)[1][1:-3]
                    full_path = full_path.replace("/", ".")
                    class_name = f"{action_name}Output"
                    output = __import__(str(full_path), fromlist=[class_name])
                    output_class = getattr(output, class_name)
                    schemas[os.path.basename(path)] = output_class.schema
        return schemas

    def validate(self, spec):
        schemas = OutputValidator.get_schemas(spec)
        for action in spec.actions():
            path = os.path.join(spec.directory, f".output/{action}.json")
            if os.path.exists(path):
                with open(path, 'r') as output:  # if test output has been generated
                    self.validate_output(json.load(output), schemas[action], action)

        if len(self.missing_outputs) > 0:
            raise Exception(f"Action output does not match spec. List of (ACTION, ERROR): {self.missing_outputs}")
