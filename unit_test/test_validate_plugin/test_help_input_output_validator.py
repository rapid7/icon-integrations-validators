import unittest

from icon_validator.rules import HelpInputOutputValidator
from icon_validator.validate import validate


class TestHelpInputOutputValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.file_to_test = "plugin.spec.yaml"

    def test_array_in_help(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_plugin"

        result = validate(
            directory_to_test,
            self.file_to_test,
            False,
            True,
            [HelpInputOutputValidator()],
        )

        self.assertEqual(result, 0, "Result should be success")

    def test_bad_array_in_help(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_array_in_help"

        result = validate(
            directory_to_test,
            self.file_to_test,
            False,
            True,
            [HelpInputOutputValidator()],
        )
        # TODO this clear violations for other tests

        HelpInputOutputValidator.violations = []
        HelpInputOutputValidator.violated = 0
        self.assertEqual(result, 1, "Result should be failed")

    def test_datetime_in_inputOutputValidators(self):
        directory_to_test = "plugin_examples/good_datetime_example"

        result = validate(
            directory_to_test,
            self.file_to_test,
            False,
            True,
            [HelpInputOutputValidator()],
        )

        self.assertEqual(result, 0)

    def test_input_output_validator_when_output_has_no_example_from_date_types(self):
        directory_to_test = "plugin_examples/good_plugin_without_output_examples"

        result = validate(
            directory_to_test,
            self.file_to_test,
            False,
            True,
            [HelpInputOutputValidator()],
        )

        self.assertEqual(result, 1, "Result should be failed")

    def test_input_output_validator_when_output_has_no_custom_output(self):
        directory_to_test = "plugin_examples/good_plugin_without_custom_output_examples"

        result = validate(
            directory_to_test,
            self.file_to_test,
            False,
            True,
            [HelpInputOutputValidator()],
        )

        self.assertEqual(result, 0, "Result should be success")

    def test_input_output_validator_when_output_has_custom_output(self):
        directory_to_test = "plugin_examples/good_plugin_with_custom_output_examples"

        result = validate(
            directory_to_test,
            self.file_to_test,
            False,
            True,
            [HelpInputOutputValidator()],
        )

        self.assertEqual(result, 0, "Result should be success")

    def test_input_output_validator_with_placeholder_tooltip(self):
        directory_to_test = "plugin_examples/good_plugin_with_placeholder_tooltip"

        result = validate(
            directory_to_test,
            self.file_to_test,
            False,
            True,
            [HelpInputOutputValidator()],
        )

        self.assertEqual(result, 0, "Result should be success")
