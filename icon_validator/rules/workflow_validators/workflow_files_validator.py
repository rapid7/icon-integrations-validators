import os

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class WorkflowFilesValidator(KomandPluginValidator):

    def validate(self, spec):
        """
        Checks that a help.md, extension.png, workflow.spec.yaml, and a .icon file exist
        """
        d = spec.directory

        if not os.path.isfile(f"{d}/workflow.spec.yaml"):
            raise ValidationException("File workflow.spec.yaml does not exist in: ", d)
        if not os.path.isfile(f"{d}/help.md"):
            raise ValidationException("File help.md does not exist in: ", d)
        if not os.path.isfile(f"{d}/extension.png"):
            raise ValidationException("File extension.png does not exist in: ", d)
        if not any(file_name.endswith(".icon") for file_name in os.listdir(d)):
            raise ValidationException("Workflow file does not exist in: ", d)
