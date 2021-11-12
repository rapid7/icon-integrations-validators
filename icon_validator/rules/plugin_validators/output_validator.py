import json
import os
import re
import sys

from jsonschema import validate, exceptions

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class OutputValidator(KomandPluginValidator):
    def __init__(self):
        super().__init__()
        self.missing_outputs = []

    def validate_output(self, process_output, spec_schema, process_name, process_type):
        try:
            validate(process_output, spec_schema)
        except(exceptions.ValidationError, exceptions.SchemaError) as e:
            self.missing_outputs.append((f'{process_type}:{process_name}', e))

    @staticmethod
    def get_schemas(spec):
        schemas = {}
        sys.path.append(spec.directory)
        for path, _, files in os.walk(spec.directory):
            for file in files:
                if "schema.py" in file and os.path.basename(path) != "connection":
                    full_path = os.path.join(path, file)
                    schemas[os.path.basename(path)] = OutputValidator.read_schema(full_path)
        return schemas

    @staticmethod
    def read_schema(path):
        with open(path) as schema:
            text = schema.read()
        text = text.strip()
        output_pattern = '(?s)"""(.*?)"""'
        results = re.findall(output_pattern, text)
        if len(results) == 2:
            json_ = json.loads(results[1])  # Action: 0 for input, 1 for output
        else:
            json_ = json.loads(results[2])  # Task: 0 for input, 1 for state, 2 for output
        return json_

    def validate(self, spec):
        schemas = OutputValidator.get_schemas(spec)
        actions, tasks = {}, {}
        # Prevent parsing action and task less plugin
        if spec.actions():
            actions = spec.actions()
        if spec.tasks():
            tasks = spec.tasks()
        if not actions and not tasks:
            return

        for action in actions:
            path = os.path.join(spec.directory, f".output/action_{action}.json")
            if os.path.exists(path):
                with open(path, 'r') as output:  # if test output has been generated
                    self.validate_output(json.load(output), schemas[action], action, "Action")

        for task in tasks:
            path = os.path.join(spec.directory, f".output/task_{task}.json")
            if os.path.exists(path):
                with open(path, 'r') as output:  # if test output has been generated
                    self.validate_output(json.load(output), schemas[task], task, "Task")

        if len(self.missing_outputs) > 0:
            raise ValidationException(f"Action/Task output does not match spec. List of (TYPE:NAME, ERROR): {self.missing_outputs}")
