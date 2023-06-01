import unittest

from icon_validator.rules import HelpExampleValidator, ExampleInputValidator
from icon_validator.validate import validate


class TestHelpExampleValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.file_to_test = "plugin.spec.yaml"

    def test_help_example_spaces_and_json_should_success(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_plugin"

        result = validate(
            directory_to_test, self.file_to_test, False, True, [HelpExampleValidator()]
        )

        self.assertEqual(result, 0)

    def test_help_example_spaces_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_help_example_wrong_spaces"

        result = validate(
            directory_to_test, self.file_to_test, False, True, [HelpExampleValidator()]
        )

        self.assertEqual(result, 1)

    def test_help_example_json_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_help_example_wrong_json"

        result = validate(
            directory_to_test, self.file_to_test, False, True, [HelpExampleValidator()]
        )

        self.assertEqual(result, 1)
