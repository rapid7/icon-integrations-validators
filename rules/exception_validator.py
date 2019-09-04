from .validator import KomandPluginValidator
import os


class ExceptionValidator(KomandPluginValidator):
    violating_files = []

    @staticmethod
    def validate_exceptions(spec_dir, path, name):
        joined_path = os.path.join(path, name)
        with open(joined_path, 'r') as f:
            text = f.read()
        if "raise Exception" in text:
            ExceptionValidator.violating_files.append(os.path.relpath(joined_path, spec_dir))

    def validate(self, spec):
        d = spec.directory
        for path, _, files in os.walk(d):
            for name in files:
                if name.endswith(".py"):
                    ExceptionValidator.validate_exceptions(d, path, name)
        if len(ExceptionValidator.violating_files) > 0:
            raise Exception(f"Please use 'PluginException' and"
                            f" 'ConnectionTestException' instead of 'Exception'. "
                            f"The following files violated this rule: {ExceptionValidator.violating_files}")

