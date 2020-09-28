from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException
from icon_validator.rules.lists.lists import title_validation_list


class TitleValidator(KomandPluginValidator):

    @staticmethod
    def validate_title(title, plugin_title=False):
        if not isinstance(title, str):
            raise ValidationException("Title must not be blank")
        if title == "":
            raise ValidationException("Title must not be blank")
        if title.endswith("."):
            raise ValidationException("Title ends with period when it should not.")
        if title[0].islower() and not plugin_title:
            # This plugin title is OK: minFraud
            # This plugin title is OK: ifconfig.co
            raise ValidationException("Title should not start with a lower case letter.")
        if title[0].isspace():
            raise ValidationException("Title should not start with a whitespace character.")
        if len(title.split()) > 7:
            raise ValidationException(f"Title is too long, 6 words or less: contains {str(len(title.split()))}")
        for word in title.split():
            if not title.startswith(word):
                if word in title_validation_list:
                    if not title.endswith(word):
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
                    if not word.lower() == "by" or word.lower() == "of":
                        if word.isalpha():
                            raise ValidationException(f"Title contains a lowercase '{word}' when it should not.")

    @staticmethod
    def validate_actions(dict_, dict_key):
        if dict_key in dict_:
            TitleValidator.validate_dictionary(dict_, dict_key)
            for key, value in dict_[dict_key].items():
                if "input" in value:
                    TitleValidator.validate_dictionary(value, "input")
                if "output" in value:
                    TitleValidator.validate_dictionary(value, "output")
                if "state" in value:
                    TitleValidator.validate_dictionary(value, "state")
                if "schedule" in value:
                    TitleValidator.validate_dictionary({"schedule": value}, "schedule")

    @staticmethod
    def validate_dictionary(dict_, dict_key):
        if dict_key in dict_:
            if not dict_[dict_key]:
                return

            for key, value in dict_[dict_key].items():
                if "name" in value:
                    raise ValidationException(f"Deprecated 'name' key '{value}' found when 'title' should be used instead.")
                if "title" in value:
                    try:
                        TitleValidator.validate_title(value["title"], plugin_title=False)
                    except Exception as e:
                        raise ValidationException(f"{dict_key} key '{key}' error.", e)

    @staticmethod
    def validate_plugin_title(spec):
        if "title" not in spec.spec_dictionary():
            raise ValidationException("Plugin title is missing.")

        try:
            TitleValidator.validate_title(spec.spec_dictionary()["title"], plugin_title=True)
        except Exception as e:
            raise ValidationException("Plugin title not valid.", e)

    def validate(self, spec):
        TitleValidator.validate_plugin_title(spec)
        TitleValidator.validate_actions(spec.spec_dictionary(), "actions")
        TitleValidator.validate_actions(spec.spec_dictionary(), "triggers")
        TitleValidator.validate_actions(spec.spec_dictionary(), "connection")
        TitleValidator.validate_actions(spec.spec_dictionary(), "tasks")
