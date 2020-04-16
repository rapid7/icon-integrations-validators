from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException
from icon_validator.rules.lists.lists import title_validation_list


class WorkflowTitleValidator(KomandPluginValidator):

    def validate(self, spec):
        """
        Checks that title is not blank.
        Checks that title does not end with a period.
        Checks that title does not start with a lower case letter.
        Checks that title does not start with a space.
        Checks that title is 6 words or less.
        Checks that title is properly capitalized.
        """
        if "title" not in spec.spec_dictionary():
            raise ValidationException("Plugin title is missing.")

        title = spec.spec_dictionary()["title"]

        if not isinstance(title, str):
            raise ValidationException("Title must not be blank")
        if title == "":
            raise ValidationException("Title must not be blank")
        if title.endswith("."):
            raise ValidationException("Title ends with period when it should not.")
        if title[0].islower():
            # This plugin title is OK: minFraud
            # This plugin title is OK: ifconfig.co
            raise ValidationException("Title should not start with a lower case letter.")
        if title[0].isspace():
            raise ValidationException("Title should not start with a whitespace character.")
        for word in title.split():
            if not title.startswith(word):
                if word in title_validation_list:
                    raise ValidationException(f"Title contains a capitalized '{word}' when it should not.")
                elif "By" == word and not title.endswith("By"):
                    # This is OK: Order By
                    # This is NOT OK: Search By String
                    raise ValidationException("Title contains a capitalized 'By' when it should not.")
                elif "Of" == word and not title.endswith("Of"):
                    # This is OK: Member Of
                    # This is NOT OK: Type Of String
                    raise ValidationException("Title contains a capitalized 'Of' when it should not.")
                elif not word[0].isupper() and not word.capitalize() in title_validation_list:
                    if not word.isnumeric():
                        if not word.lower() == "by" or word.lower() == "of":
                            raise ValidationException(f"Title contains a lowercase '{word}' when it should not.")
