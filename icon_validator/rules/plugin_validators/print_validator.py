from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class PrintValidator(KomandPluginValidator):

    @staticmethod
    def validate_print(section):
        print_found = False

        for f in section:
            if "print(" in f:
                print_found = True

        if print_found:
            raise ValidationException("One or more files use print statements, update to use self.logger.")

    def validate(self, spec):
        # Logging update is only for Python plugins
        image = None
        for line in spec.raw_dockerfile():
            if line.startswith("FROM"):
                parent = line.replace("FROM", "").strip()
                parts = parent.split(":")
                image = parts[0].strip()
                break  # Only one FROM within a Dockerfile, so just exit early instead of continuing to loop

        if not image:
            raise ValidationException("No FROM statement found within the Dockerfile.")

        if image == "komand/go-plugin-2":
            return None
        elif image == "komand/go-plugin":
            raise ValidationException("Plugin is using a deprecated Go parent image.")

        PrintValidator.validate_print(spec.raw_trigger_files())
        PrintValidator.validate_print(spec.raw_action_files())
        PrintValidator.validate_print(spec.raw_task_files())
        PrintValidator.validate_print(spec.raw_connection_file())
        PrintValidator.validate_print(spec.raw_util_files())
