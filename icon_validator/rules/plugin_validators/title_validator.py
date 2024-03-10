from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException
from icon_validator.rules.lists.lists import title_validation_list


class TitleValidator(KomandPluginValidator):
    def __init__(self):
        super().__init__()

        # TODO - Make this a list and append everything then iterate through and print with newline
        self.all_offenses: str = ""

    def validate_title(self, title: str, plugin_title: bool = False) -> None:
        """

        :param title:
        :param plugin_title:

        """

        title_validation_list_lowercase = '", "'.join(title_validation_list).lower()

        if not isinstance(title, str):
            self.all_offenses += (
                f"Title must be a string, not a number or other value: {title}\n"
            )
        if title == "":
            self.all_offenses += f"Title must not be blank: {title}\n"
        if title.endswith("."):
            self.all_offenses += f"Title ends with period when it should not: {title}\n"
        if title[0].islower() and not plugin_title:
            # This plugin title is OK: minFraud
            # This plugin title is OK: ifconfig.co
            self.all_offenses += (
                f"Title should not start with a lower case letter: {title}\n"
            )
        if title[0].isspace():
            self.all_offenses += (
                f"Title should not start with a whitespace character: {title}\n"
            )
        if len(title.split()) > 7:
            self.all_offenses += f"Title is too long, 6 words or less: contains {str(len(title.split()))}: {title}\n"
        for word in title.split():
            if not title.startswith(word):
                if word in title_validation_list:
                    if not title.endswith(word):
                        self.all_offenses += f"English articles and conjunctions should be lowercase when in the middle of the sentence:'{title_validation_list_lowercase}': {title}\n"

                elif "By" == word and not title.endswith("By"):
                    # This is OK: Order By
                    # This is NOT OK: Search By String
                    self.all_offenses += f"Title contains a capitalized 'By' when it should not: {title}\n"
                elif "Of" == word and not title.endswith("Of"):
                    # This is OK: Member Of
                    # This is NOT OK: Type Of String
                    self.all_offenses += f"Title contains a capitalized 'Of' when it should not: {title}\n"
                elif (
                    not word[0].isupper()
                    and not word.capitalize() in title_validation_list
                ):
                    if not word.lower() == "by" or word.lower() == "of":
                        if word.isalpha():
                            self.all_offenses += f"Title contains a lowercase '{word}' when it should not: {title}\n"

    def validate_actions(self, spec: dict, spec_section: str):
        """

        :param spec:
        :param spec_section:

        """

        if spec_section in spec:
            self.validate_dictionary(spec, spec_section)
            for key, value in spec[spec_section].items():
                if "input" in value:
                    self.all_offenses += self.validate_dictionary(
                        value, "input"
                    )
                if "output" in value:
                    self.all_offenses += self.validate_dictionary(
                        value, "output"
                    )
                if "state" in value:
                    self.all_offenses += self.validate_dictionary(
                        value, "state"
                    )
                if "schedule" in value:
                    self.all_offenses += self.validate_dictionary(
                        {"schedule": value}, "schedule"
                    )

    def validate_dictionary(self, spec: dict, section: str) -> None:
        """

        :param spec:
        :param section:

        """

        if section in spec:
            if not spec[section]:
                return

            for key, value in spec[section].items():
                if "title" in value:
                    self.all_offenses += self.validate_title(
                        value["title"], plugin_title=False
                    )

                if "name" in value:
                    self.all_offenses += f"Deprecated 'name' key '{value}' found when 'title' should be used instead: {value}\n"

    def validate_plugin_title(self, spec) -> None:
        """

        :param spec:

        """

        if "title" not in spec.spec_dictionary():
            self.all_offenses += f"Plugin title is missing"
        try:
            self.validate_title(
                spec.spec_dictionary()["title"], plugin_title=True
            )
        except Exception as error:
            self.all_offenses += f"Plugin title not valid: {error}"

    def validate(self, spec):
        """

        :param spec:

        """

        self.validate_plugin_title(spec)
        self.validate_actions(spec.spec_dictionary(), "actions")
        self.validate_actions(spec.spec_dictionary(), "triggers")
        self.validate_actions(spec.spec_dictionary(), "tasks")
        self.validate_actions(spec.spec_dictionary(), "connection")
        if self.all_offenses:
            raise ValidationException(self.all_offenses)
