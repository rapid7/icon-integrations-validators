from .validator import KomandPluginValidator
import os
import json


class OutputValidator(KomandPluginValidator):
    def __init__(self):
        super().__init__()
        self.missing_outputs = []

    def validate_output(self, action_output, spec_output):
        for key in spec_output:
            if spec_output[key].get("required") and action_output.get(key) is None:
                self.missing_outputs.append(key)

    def validate(self, spec):
        for action in spec.actions():
            path = os.path.join(spec.directory, f"test-output/{action}.json")
            if os.path.exists(path):
                with open(path, 'r') as output:  # if test output has been generated
                    self.validate_output(json.load(output), spec.spec_dictionary()["actions"][action]["output"])

        if len(self.missing_outputs) > 0:
            raise Exception(f"Action output does not match spec. Missing required fields: {self.missing_outputs}")
