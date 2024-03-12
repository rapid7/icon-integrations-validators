from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException
from icon_validator.rules.lists.lists import title_validation_list


class TitleValidator(KomandPluginValidator):
    def __init__(self):
        super().__init__()

        self.all_offenses = []

    def validate_title(self, title: str, plugin_title: bool = False) -> None:
        """
        Helper method to apply all validation rules to most titles throughout the
        plugin.spec minus the plugin title

        :param title: The title to validate
        :param plugin_title: Bool switch to indicate if it is the plugin title

        """

        title_validation_list_lowercase = '", "'.join(title_validation_list).lower()

        if title is None:
            self.all_offenses.append("Empty title found")
            return
        if not isinstance(title, str):
            self.all_offenses.append(
                f"Title must be a string, not a number or other value: {title}"
            )
        if title == "":
            self.all_offenses.append(f"Title must not be blank: {title}")
        if title.endswith("."):
            self.all_offenses.append(
                f"Title ends with period when it should not: {title}"
            )
        if title[0].islower() and not plugin_title:
            # This plugin title is OK: minFraud
            # This plugin title is OK: ifconfig.co
            self.all_offenses.append(
                f"{title} - Title should not start with a lower case letter"
            )
        if title[0].isspace():
            self.all_offenses.append(
                f"{title} - Title should not start with a whitespace character"
            )
        if len(title.split()) > 7:
            self.all_offenses.append(
                f"{title} - Title is too long, 6 words or less: contains {str(len(title.split()))}"
            )
        for word in title.split():
            if not title.startswith(word):
                if word in title_validation_list:
                    if not title.endswith(word):
                        self.all_offenses.append(
                            f"{title} - English articles and conjunctions should be lowercase when in the middle of the sentence:'{title_validation_list_lowercase}'"
                        )

                elif "By" == word and not title.endswith("By"):
                    # This is OK: Order By
                    # This is NOT OK: Search By String
                    self.all_offenses.append(
                        f"{title} - Title contains a capitalized 'By' when it should not"
                    )
                elif "Of" == word and not title.endswith("Of"):
                    # This is OK: Member Of
                    # This is NOT OK: Type Of String
                    self.all_offenses.append(
                        f"{title} - Title contains a capitalized 'Of' when it should not"
                    )
                elif (
                    not word[0].isupper()
                    and not word.capitalize() in title_validation_list
                ):
                    if not word.lower() == "by" or word.lower() == "of":
                        if word.isalpha():
                            self.all_offenses.append(
                                f"{title} - Title contains a lowercase '{word}' when it should not"
                            )

    def validate_actions(self, spec: dict, spec_section: str) -> None:
        """
        Helper method to validate the action titles within the plugin spec

        :param spec: The spec dictionary
        :param spec_section: The name of the section within the spec file

        """

        if spec_section in spec:
            self.validate_dictionary(spec, spec_section)
            for key, value in spec[spec_section].items():
                if "input" in value:
                    self.validate_dictionary(value, "input")
                if "output" in value:
                    self.validate_dictionary(value, "output")
                if "state" in value:
                    self.validate_dictionary(value, "state")
                if "schedule" in value:
                    self.validate_dictionary({"schedule": value}, "schedule")

    def validate_dictionary(self, spec: dict, section: str) -> None:
        """
        A method to validate all the different sections within the spec file

        :param spec: The spec dictionary
        :param section: The section name

        """

        if section in spec:
            if not spec[section]:
                return

            for key, value in spec[section].items():
                if "title" in value:
                    self.validate_title(value["title"], plugin_title=False)

                if "name" in value:
                    self.all_offenses.append(
                        f"Deprecated 'name' key '{value}' found when 'title' should be used instead: {value}"
                    )

    def validate_plugin_title(self, spec) -> None:
        """
        Helper method to validate the plugin title

        :param spec: The spec file before dict conversion

        """

        if "title" not in spec.spec_dictionary():
            self.all_offenses.append(f"Plugin title is missing")
        try:
            self.validate_title(spec.spec_dictionary()["title"], plugin_title=True)
        except Exception as error:
            self.all_offenses.append(f"Plugin title not valid: {error}")

    def validate(self, spec) -> None:
        """
        The main method of the TitleValidator to run validation against all titles
        throughout the plugin spec file.

        :param spec: The plugin spec file

        """

        self.validate_plugin_title(spec)
        self.validate_actions(spec.spec_dictionary(), "actions")
        self.validate_actions(spec.spec_dictionary(), "triggers")
        self.validate_actions(spec.spec_dictionary(), "tasks")
        self.validate_actions(spec.spec_dictionary(), "connection")
        if self.all_offenses:
            joined_errors = "\n".join(self.all_offenses)
            raise ValidationException(joined_errors)
