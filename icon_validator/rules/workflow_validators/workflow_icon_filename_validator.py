import os

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class WorkflowICONFileNameValidator(KomandPluginValidator):

    def validate(self, spec):
        """
        Checks that .icon file names do not contain spaces
        """
        d = spec.directory
        for file_name in os.listdir(d):
            if file_name.endswith(".icon"):
                if " " in file_name:
                    raise ValidationException(f"The .icon file name was '{file_name}'.\n "
                                              ".icon file may not contain spaces use a '_' instead.")
