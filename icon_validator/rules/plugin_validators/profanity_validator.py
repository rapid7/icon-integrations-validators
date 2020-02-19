from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException
from icon_validator.rules.lists.lists import profanity_list


class ProfanityValidator(KomandPluginValidator):

    @staticmethod
    def validate_profanity(spec):
        raw_spec = spec.raw_spec()
        spec_words = raw_spec.split()

        for word in spec_words:
            if word in profanity_list:
                raise ValidationException(f"{spec.spec_file_name} contains banned word: {word}.")

        help_lst = spec.raw_help().split()
        for word in help_lst:
            if word in profanity_list:
                raise ValidationException(f"help.md contains banned word: {word}.")

    def validate(self, spec):
        ProfanityValidator.validate_profanity(spec)
