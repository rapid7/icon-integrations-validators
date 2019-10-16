from .validator import KomandPluginValidator
import os
import json
import re
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
                    full_path = os.path.join(path, file)
                    print(full_path)
                    schemas[os.path.basename(path)] = OutputValidator.read_schema(full_path)
        return schemas

    @staticmethod
    def read_schema(path):
        with open(path) as schema:
            text = schema.read()
        text = text.strip()
        output_pattern = '(?s)"""(.*?)"""'
        json_ = json.loads(re.findall(output_pattern, text)[1]) # 0 for input, 1 for output
        return json_

    def validate(self, spec):
        schemas = OutputValidator.get_schemas(spec)
        for action in spec.actions():
            path = os.path.join(spec.directory, f".output/{action}.json")
            if os.path.exists(path):
                with open(path, 'r') as output:  # if test output has been generated
                    self.validate_output(json.load(output), schemas[action], action)

        if len(self.missing_outputs) > 0:
            raise Exception(f"Action output does not match spec. List of (ACTION, ERROR): {self.missing_outputs}")