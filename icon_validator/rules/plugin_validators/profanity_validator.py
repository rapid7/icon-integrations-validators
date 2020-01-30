from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException

# TODO This list is way too small we need a bigger list and an easier way to update it
bannedWords = ["anal", "anus", "arse", "ass", "ballsack", "balls", "bastard", "bitch", "biatch", "bloody", "blowjob",
               "blow job", "bollock", "bollok", "boner", "boob", "bugger", "bum", "butt", "buttplug", "clitoris",
               "cock", "coon", "crap", "cunt", "damn", "dick", "dildo", "dyke", "fag", "feck", "fellate", "fellatio",
               "felching", "fuck", "f u c k", "fudgepacker", "fudge packer", "flange", "Goddamn", "God damn", "hell",
               "homo", "jerk", "jizz", "knobend", "knob end", "labia", "lmao", "lmfao", "muff", "nigger", "nigga",
               "omg", "penis", "piss", "poop", "prick", "pube", "pussy", "queer", "scrotum", "sex", "shit", "s hit",
               "sh1t", "slut", "smegma", "spunk", "tit", "tosser", "turd", "twat", "vagina", "wank", "whore", "wtf"]


class ProfanityValidator(KomandPluginValidator):

    @staticmethod
    def validate_profanity(spec):
        raw_spec = spec.raw_spec()
        spec_words = raw_spec.split()

        for word in spec_words:
            if word in bannedWords:
                raise ValidationException(f"{spec.spec_file_name} contains banned word: {word}.")

        help_lst = spec.raw_help().split()
        for word in help_lst:
            if word in bannedWords:
                raise ValidationException(f"help.md contains banned word: {word}.")

    def validate(self, spec):
        ProfanityValidator.validate_profanity(spec)
