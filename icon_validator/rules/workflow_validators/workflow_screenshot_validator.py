import os

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class WorkflowScreenshotValidator(KomandPluginValidator):

    def __init__(self):
        super().__init__()
        self._files_list = list()
        self._names_list = list()

    @staticmethod
    def validate_title(title):
        """
        Checks that title is not blank.
        Checks that title does not end with a period.
        Checks that title does not start with a lower case letter.
        Checks that title does not start with a space.
        Checks that title is 6 words or less.
        Checks that title is properly capitalized.
        """
        if not isinstance(title, str):
            raise ValidationException("Title must not be blank")
        if title.endswith("."):
            raise ValidationException("Title ends with period when it should not.")
        if title[0].islower():
            # This plugin title is OK: minFraud
            # This plugin title is OK: ifconfig.co
            raise ValidationException("Title should not start with a lower case letter.")
        if title[0].isspace():
            raise ValidationException("Title should not start with a whitespace character.")
        if len(title.split()) > 7:
            raise ValidationException(f"Title is too long, 6 words or less: contains {str(len(title.split()))}")
        for word in title.split():
            if not title.startswith(word):
                # TODO I want to pull from a list file rather than having to update this list in 3 areas every time we need a change
                word_list = ["The", "From", "A", "An", "And", "Is", "But", "For",
                             "Nor", "Or", "So", "Of", "To", "On", "At", "As"]
                if word in word_list:
                    raise ValidationException(f"Title contains a capitalized '{word}' when it should not.")
                elif "By" == word and not title.endswith("By"):
                    # This is OK: Order By
                    # This is NOT OK: Search By String
                    raise ValidationException("Title contains a capitalized 'By' when it should not.")
                elif "Of" == word and not title.endswith("Of"):
                    # This is OK: Member Of
                    # This is NOT OK: Type Of String
                    raise ValidationException("Title contains a capitalized 'Of' when it should not.")
                elif not word[0].isupper() and not word.capitalize() in word_list:
                    if not word.lower() == "by" or word.lower() == "of":
                        raise ValidationException(f"Title contains a lowercase '{word}' when it should not.")

    @staticmethod
    def validate_screenshot_titles(spec):
        """
        Checks that all screenshot objects have a title key.
        Runs validate_title method on all title keys.
        """
        screenshots = spec.spec_dictionary()["resources"]["screenshots"]
        titles_list = list()
        for screenshot in screenshots:
            try:
                titles_list.append(screenshot["title"])
            except KeyError:
                raise ValidationException("Each screenshot must have a 'title' key."
                                          f" {screenshot} is missing this key.")
        for item in titles_list:
            WorkflowScreenshotValidator.validate_title(item)

    def validate_screenshots_keys_exist(self, spec):
        """
        Checks that screenshots key exists.
        Checks that screenshots key has at lest one entry.
        """
        try:
            screenshots = spec.spec_dictionary()["resources"]["screenshots"]
        except KeyError:
            raise ValidationException("The screenshots key under the resources key does not exist in the yaml."
                                      " please add this key.")
        if not isinstance(screenshots, list):
            raise ValidationException("There are no screenshots listed in the yaml."
                                      " At lest one screenshot must be listed.")
        if len(screenshots) == 0:
            raise ValidationException("There are no screenshots listed in the yaml."
                                      " At lest one screenshot must be listed.")

        for screenshot in screenshots:
            try:
                self._names_list.append(screenshot["name"])
            except KeyError:
                raise ValidationException("Each screenshot must have a 'name' key that coresposnds to the file name of the screenshot."
                                          f" {screenshot} is missing this key.")

    def validate_screenshot_files_exist(self, spec):
        """
        Check that screenshots directory exists.
        Check that screenshots directory contains one or more files.
        Check that all files in screenshots directory are .png files.
        """
        directory = spec.directory
        try:
            for file_name in os.listdir(f"{directory}/screenshots"):
                self._files_list.append(file_name)
        except FileNotFoundError:
            raise ValidationException(f"The screenshots directory could not be found at: {directory}\n"
                                      "Please ensure that the screenshots directory exists.")
        if len(self._files_list) == 0:
            raise ValidationException("There are no files in the screenshots directory."
                                      " Please add at lest one screenshot.")
        for screenshot in self._files_list:
            if not screenshot.endswith(".png"):
                raise ValidationException(f"All screenshots must be .png files. {screenshot} is not a .png file")

    def validate_names_not_null(self):
        """
        Check that name keys in yaml are not null or blank strings.
        """
        for name in self._names_list:
            if not isinstance(name, str):
                raise ValidationException("The name key for a screenshot must not be null")
        if any(names == "" for names in self._names_list):
            raise ValidationException("The name key for a screenshot may not be a blank string")

    def validate_screenshot_files_and_keys_match(self):
        """
        Check that screenshot file names match name keys in yaml.
        Check that there are not file names that do not exist in yaml and vice versa.
        """
        sorted_names = sorted(self._names_list)
        sorted_files = sorted(self._files_list)
        if not sorted_files == sorted_names:
            raise ValidationException("The screenshot files names and the screenshot names in the yaml do not match.")

    def validate(self, spec):
        self.validate_screenshots_keys_exist(spec)
        self.validate_screenshot_files_exist(spec)
        self.validate_names_not_null()
        self.validate_screenshot_files_and_keys_match()
        WorkflowScreenshotValidator.validate_screenshot_titles(spec)
