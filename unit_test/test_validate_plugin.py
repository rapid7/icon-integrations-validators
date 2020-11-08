import unittest
from icon_validator.validate import validate

# Import plugin validators to pass to tests
from icon_validator.rules.plugin_validators.title_validator import TitleValidator
from icon_validator.rules.plugin_validators.profanity_validator import ProfanityValidator
from icon_validator.rules.plugin_validators.help_input_output_validator import HelpInputOutputValidator
from icon_validator.rules.plugin_validators.version_validator import VersionValidator
from icon_validator.rules.plugin_validators.version_pin_validator import VersionPinValidator
import requests


class TestPluginValidate(unittest.TestCase):

    def test_plugin_validate(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_plugin"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, False)
        self.assertFalse(result)

    def test_plugin_validate_with_task(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_plugin_with_task"
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

    def test_array_in_help(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_plugin"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [HelpInputOutputValidator()])
        self.assertEqual(result, 0, "Result should be success")

    def test_bad_array_in_help(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_array_in_help"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [HelpInputOutputValidator()])
        # TODO this clear violations for other tests
        HelpInputOutputValidator.violations = []
        HelpInputOutputValidator.violated = 0
        self.assertEqual(result, 1, "Result should be failed")

    def test_version_validator(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/version_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionValidator()])
        self.assertEqual(result, 0)

    def test_version_validator_should_faile_when_version_same_in_api(self):
        # example workflow in plugin_examples directory. Run tests with these files
        version = requests.get(
            url=f"https://extensions-api.rapid7.com/v1/public/extensions/active_directory_ldap",
            timeout=3
        ).json()["version"]

        f = open("plugin_examples/version_validator/plugin.spec_bad.yaml", 'w')
        f.write(f"plugin_spec_version: v2\nname: active_directory_ldap\nversion: {version}")
        f.close()
        directory_to_test = "plugin_examples/version_validator"
        file_to_test = "plugin.spec_bad.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionValidator()])

    def test_version_pin_validator_should_success(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_test"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionPinValidator()])
        self.assertEqual(result, 0)

    def test_version_pin_validator_should_fail_when_question_mark(self):
        self.replace_requirements("plugin_examples/version_pin_validator/requirements.txt", "?ldap3")
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/version_pin_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionPinValidator()])
        self.assertEqual(result, 1)

    def test_version_pin_validator_should_fail_when_one_equal_sign(self):
        self.replace_requirements("plugin_examples/version_pin_validator/requirements.txt", "ldap3=2.6")
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/version_pin_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionPinValidator()])
        self.assertEqual(result, 1)

    def test_version_pin_validator_should_fail_when_no_version_pin(self):
        self.replace_requirements("plugin_examples/version_pin_validator/requirements.txt", "ldap3")
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/version_pin_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionPinValidator()])
        self.assertEqual(result, 1)

    def test_plugin_with_false_for_required_on_output(self):
        # TODO This validator is not correctly made: fix
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_no_required_key_in_output"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True)
        self.assertTrue(result)

    @staticmethod
    def replace_requirements(path, text):
        f = open(path, 'w')
        f.write(text)
        f.close()
