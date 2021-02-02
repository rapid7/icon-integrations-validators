import os
import re
import spellchecker
from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class SpellingValidator(KomandPluginValidator):

    @staticmethod
    def validate_spelling(spec):
        lst = spec.raw_spec().split()
        spell = spellchecker.SpellChecker()

        custom_dict = os.path.join(spec.directory, 'custom_dict.json')
        if os.path.exists(custom_dict):
            spell.word_frequency.load_text_file(custom_dict)

        en_dict = os.path.abspath('../icon_validator/rules/lists/en_dict.json')
        spell.word_frequency.load_text_file(en_dict)
        parsed_lst = SpellingValidator.parse_lst(lst)
        misspelled = spell.unknown(parsed_lst)

        for word in misspelled:
            raise ValidationException(f"{spec.spec_file_name} may contain misspellings: did you mean "
                                      f"{spell.correction(word)} instead of {word}?")

        help_lst = spec.raw_help().split()
        parsed_help_lst = SpellingValidator.parse_lst(help_lst)
        misspelled = spell.unknown(parsed_help_lst)

        for word in misspelled:
            raise ValidationException(f"help.md may contain misspellings: did you mean "
                                      f"{spell.correction(word)} instead of {word}?")

    @staticmethod
    def parse_lst(lst):
        parsed_lst = []
        for word in lst:
            if 'http' not in word:
                word = re.sub('[^0-9a-zA-Z]+', ' ', word)
                words = word.split()
                for parsed_word in words:
                    if parsed_word != '' and re.search('[a-zA-Z]', parsed_word):
                        parsed_lst.append(parsed_word)
        return parsed_lst

    def validate(self, spec):
        SpellingValidator.validate_spelling(spec)
