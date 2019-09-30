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
            text = f.readlines()

        violating_lines = []
        pattern = "raise [A-Za-z]*"
        for line_num in range(len(text)):
            matches = re.findall(pattern, text[line_num])
            violations = list(filter(lambda m: ExceptionValidator.violation_check(m), matches))
            if len(violations) > 0:
                violating_lines.append(str(line_num + 1))

        if len(violating_lines) > 0:
            self._violating_files.append(f"{os.path.relpath(joined_path, spec_dir)}: {', '.join(violating_lines)}")

    @staticmethod
    def violation_check(match):
        allowed = ["PluginException", "ConnectionTestException"]
        for e in allowed:
            if e in match:
                return False
        return True

    @staticmethod
    def should_search(path, name):
        return (f"icon_{name}" in path) or (f"komand_{name}" in path)

    def validate(self, spec):
        plugin_name = spec.plugin_name()
        d = spec.directory
        for path, _, files in os.walk(d):
            if not ExceptionValidator.should_search(path, plugin_name):
                continue
            for name in files:
                if name.endswith(".py"):
                    self.validate_exceptions(d, path, name)
        if len(self._violating_files) > 0:
            raise Exception(f"Please use 'PluginException' or"
                            f" 'ConnectionTestException' when raising an exception. "
                            f"The following files violated this rule: {self._violating_files}")

