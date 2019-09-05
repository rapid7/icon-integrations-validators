from .validator import KomandPluginValidator
import os
import re


class ExceptionValidator(KomandPluginValidator):
    def __init__(self):
        super().__init__()
        self._violating_files = []

    def validate_exceptions(self, spec_dir, path, name):
        joined_path = os.path.join(path, name)
        with open(joined_path, 'r') as f:
            text = f.read()
        pattern = "raise [A-Za-z]*"
        matches = re.findall(pattern, text)
        violations = list(filter(lambda x: "raise PluginException" not in x
                                           and "raise ConnectionTestException" not in x, matches))
        if len(violations) > 0:
            self._violating_files.append(os.path.relpath(joined_path, spec_dir))

    def validate(self, spec):
        d = spec.directory
        for path, _, files in os.walk(d):
            for name in files:
                if name.endswith(".py"):
                    self.validate_exceptions(d, path, name)
        if len(self._violating_files) > 0:
            raise Exception(f"Please use 'PluginException' or"
                            f" 'ConnectionTestException' instead of 'Exception'. "
                            f"The following files violated this rule: {self._violating_files}")

