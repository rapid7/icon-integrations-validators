import unittest
from icon_validator.validate import validate

# Import plugin validators to pass to tests
from icon_validator.rules.plugin_validators.title_validator import TitleValidator
from icon_validator.rules.plugin_validators.profanity_validator import ProfanityValidator


class TestPluginValidate(unittest.TestCase):

    def test_plugin_validate(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_plugin"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, False)
        self.assertFalse(result)

    def test_title_validator(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/title_tests"
        file_to_test = "plugin_no_title.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [TitleValidator()])
        self.assertTrue(result)

    def test_title_validator_with_number_in_title(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_number_title"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [TitleValidator()])
        self.assertEqual(result, 0)

    def test_profanity_validator(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/profanity_tests"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [ProfanityValidator()])
        self.assertTrue(result)

    def test_plugin_with_false_for_required_on_output(self):
        # TODO This validator is not correctly made: fix
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_no_required_key_in_output"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True)
        self.assertTrue(result)
