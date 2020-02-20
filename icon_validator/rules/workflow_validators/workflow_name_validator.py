from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException
from os import listdir


class WorkflowNameValidator(KomandPluginValidator):

    def validate(self, spec):
        """
        Checks that the name key in .yaml is the same as the name of the .icon file without the .icon part
        """
        d = spec.directory
        icon_file = ""
        for file_name in listdir(d):
            if file_name.endswith(".icon"):
                icon_file = file_name[:-5]
        if "name" not in spec.spec_dictionary():
            raise ValidationException("The workflow name is missing in the .yaml file.")
        if not isinstance(spec.spec_dictionary()["name"], str):
            raise ValidationException("The workflow name does not contain a string.")
        name = spec.spec_dictionary()["name"]
        if not name == icon_file:
            raise ValidationException("The workflow name in .yaml and the name of the .icon file do not match."
                                      f" the name in the .yaml is {name}. The .icon file name is {icon_file}")
