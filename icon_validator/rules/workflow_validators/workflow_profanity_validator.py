from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException
from os import path
from json import load


class WorkflowProfanityValidator(KomandPluginValidator):

    def __init__(self):
        super().__init__()
        # Build a path to the profanity_list.json file
        with open(path.realpath(path.join(path.dirname(__file__), '..'))
                  + "/lists/profanity_list.json", "r") as file:
            self.banned_words = load(file)

    def validate_profanity(self, spec):
        """
        Check that yaml and help do not contain banned words.
        """
        raw_spec = spec.raw_spec()
        spec_words = raw_spec.split()

        for word in spec_words:
            if word in self.banned_words:
                raise ValidationException(f"{spec.spec_file_name} contains banned word: {word}.")

        help_lst = spec.raw_help().split()
        for word in help_lst:
            if word in self.banned_words:
                raise ValidationException(f"help.md contains banned word: {word}.")

    def validate(self, spec):
        self.validate_profanity(spec)
