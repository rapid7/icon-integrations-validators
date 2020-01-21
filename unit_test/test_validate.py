from unittest import TestCase
from icon_validator.validate import validate
from icon_validator.rules.workflow_validators import *


class TestPluginValidate(TestCase):

    def test_plugin_validate(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples"
        file_to_test = "plugin.spec.yaml"
        validate(directory_to_test, file_to_test, False, True)


class TestWorkflowValidate(TestCase):

    def test_good_workflow_validate(self):
        # Test good workflow. This should pass all validation
        directory_to_test = "workflow_examples"
        file_to_test = "workflow.spec.yaml"
        validate(directory_to_test, file_to_test, False, True)

    def test_bad_change_log_validator(self):
        # Test bad workflows. This will test the workflow_change_log_validator
        directory_to_test = "workflow_examples/vendor_tests"
        file_to_test = "workflow.spec.yaml"
        validate(directory_to_test, file_to_test, False, True)
