import unittest
from icon_validator.validate import validate

class TestPluginValidate(unittest.TestCase):

    def test_plugin_validate(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_plugin"
        file_to_test = "plugin.spec.yaml"
        validate(directory_to_test, file_to_test, False, True)

    def test_plugin_with_false_for_required_on_output(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_no_required_key_in_output"
        file_to_test = "plugin.spec.yaml"
        validate(directory_to_test, file_to_test, False, True)
