import unittest
from icon_validator.validate import Validate

# Import validators to pass to tests
from icon_validator.rules.workflow_validators.workflow_profanity_validator import WorkflowProfanityValidator
from icon_validator.rules.workflow_validators.workflow_vendor_validator import WorkflowVendorValidator
from icon_validator.rules.workflow_validators.workflow_support_validator import WorkflowSupportValidator
from icon_validator.rules.workflow_validators.workflow_version_validator import WorkflowVersionValidator
from icon_validator.rules.workflow_validators.workflow_change_log_validator import WorkflowChangelogValidator
from icon_validator.rules.workflow_validators.workflow_extension_validator import WorkflowExtensionValidator
from icon_validator.rules.workflow_validators.workflow_files_validator import WorkflowFilesValidator
from icon_validator.rules.workflow_validators.workflow_help_validator import WorkflowHelpValidator


class TestPluginValidate(unittest.TestCase):

    def test_plugin_validate(self):
        # example workflow in plugin_examples directory. Run tests with these files
        validater = Validate()
        directory_to_test = "plugin_examples"
        file_to_test = "plugin.spec.yaml"
        validater.validate(directory_to_test, file_to_test, False, True)


class TestWorkflowValidate(unittest.TestCase):

    def test_good_workflow_validator(self):
        # Test good workflow. This should pass all validation
        validater = Validate()
        directory_to_test = "workflow_examples/good_test"
        file_to_test = "workflow.spec.yaml"
        result = validater.validate(directory_to_test, file_to_test, False, True)
        self.assertFalse(result)

    def test_vendor_validator(self):
        # Test bad workflows. This will test the workflow_vendor_validator
        validater = Validate([WorkflowVendorValidator()], True)
        directory_to_test = "workflow_examples/vendor_tests"
        file_to_test = "workflow_no_vendor.spec.yaml"
        result = validater.validate(directory_to_test, file_to_test, False, True)
        self.assertTrue(result)

    def test_version_validator(self):
        # Test bad workflows. This will test the workflow_version_validator
        validater = Validate([WorkflowVersionValidator()], True)
        directory_to_test = "workflow_examples/version_tests"
        file_to_test = "workflow_version_too_low.spec.yaml"
        result = validater.validate(directory_to_test, file_to_test, False, True)
        self.assertTrue(result)

    def test_support_validator(self):
        # Test bad workflows. This will test the workflow_support_validator
        validater = Validate([WorkflowSupportValidator()], True)
        directory_to_test = "workflow_examples/support_tests"
        file_to_test = "workflow_no_supporter.spec.yaml"
        result = validater.validate(directory_to_test, file_to_test, False, True)
        self.assertTrue(result)

    def test_extension_validator(self):
        # Test bad workflows. This will test the workflow_extension_validator
        validater = Validate([WorkflowExtensionValidator()], True)
        directory_to_test = "workflow_examples/extension_tests"
        file_to_test = "workflow_extension_not_workflow.spec.yaml"
        result = validater.validate(directory_to_test, file_to_test, False, True)
        self.assertTrue(result)

    def test_help_validator(self):
        # Test bad workflows. This will test the workflow_help_validator
        validater = Validate([WorkflowHelpValidator()], True)
        directory_to_test = "workflow_examples/help_tests"
        file_to_test = "workflow.spec.yaml"
        result = validater.validate(directory_to_test, file_to_test, False, True)
        self.assertTrue(result)

    def test_change_log_validator(self):
        # Test bad workflows. This will test the workflow_change_log_validator
        validater = Validate([WorkflowChangelogValidator()], True)
        directory_to_test = "workflow_examples/change_log_tests"
        file_to_test = "workflow.spec.yaml"
        result = validater.validate(directory_to_test, file_to_test, False, True)
        self.assertTrue(result)

    def test_files_validator(self):
        # Test bad workflows. This will test the workflow_files_validator
        validater = Validate([WorkflowFilesValidator()], True)
        directory_to_test = "workflow_examples/files_tests"
        file_to_test = "workflow.spec.yaml"
        result = validater.validate(directory_to_test, file_to_test, False, True)
        self.assertTrue(result)

    def test_profanity_validator(self):
        # Test bad workflows. This will test the workflow_profanity_validator
        validater = Validate([WorkflowProfanityValidator()], True)
        directory_to_test = "workflow_examples/profanity_tests"
        file_to_test = "workflow_profanity.spec.yaml"
        result = validater.validate(directory_to_test, file_to_test, False, True)
        self.assertTrue(result)
