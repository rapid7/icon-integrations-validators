from unittest import TestCase
from icon_validator.validate import validate


class TestValidate(TestCase):
    def test_plugin_validate(self):
        # example workflow in plugin_example directory. Run tests with these files
        directory_to_test = "plugin_example"
        file_to_test = "plugin.spec.yaml"
        validate(directory_to_test, file_to_test, False, True)

    def test_workflow_validate(self):
        # example workflow in workflow_example directory. Run tests with these files
        directory_to_test = "workflow_example"
        file_to_test = "workflow.spec.yaml"
        validate(directory_to_test, file_to_test, False, True)
