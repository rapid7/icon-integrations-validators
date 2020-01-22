from unittest import TestCase
from icon_validator.validate import validate

# Import validators to pass to tests
from icon_validator.rules.workflow_validators.workflow_profanity_validator import WorkflowProfanityValidator
from icon_validator.rules.workflow_validators.workflow_vendor_validator import WorkflowVendorValidator
from icon_validator.rules.workflow_validators.workflow_support_validator import WorkflowSupportValidator
from icon_validator.rules.workflow_validators.workflow_version_validator import WorkflowVersionValidator
from icon_validator.rules.workflow_validators.workflow_change_log_validator import WorkflowChangelogValidator
from icon_validator.rules.workflow_validators.workflow_extension_validator import WorkflowExtensionValidator
from icon_validator.rules.workflow_validators.workflow_files_validator import WorkflowFilesValidator
from icon_validator.rules.workflow_validators.workflow_help_validator import WorkflowHelpValidator


class TestPluginValidate(TestCase):

    def test_plugin_validate(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples"
        file_to_test = "plugin.spec.yaml"
        validate(directory_to_test, file_to_test, False, True)


class TestWorkflowValidate(TestCase):

    # TODO bad tests need to run in a way where they will pass with bad data rather than fail
    def test_good_workflow_validator(self):
        # Test good workflow. This should pass all validation
        directory_to_test = "workflow_examples/good_test"
        file_to_test = "workflow.spec.yaml"
        validate(directory_to_test, file_to_test, False, True)

    def test_vendor_validator(self):
        # Test bad workflows. This will test the workflow_vendor_validator
        directory_to_test = "workflow_examples/vendor_tests"
        file_to_test = "workflow_no_vendor.spec.yaml"
        validate(directory_to_test, file_to_test, False, True, [WorkflowVendorValidator()])

    def test_version_validator(self):
        # Test bad workflows. This will test the workflow_version_validator
        directory_to_test = "workflow_examples/version_tests"
        file_to_test = "workflow_version_too_low.spec.yaml"
        validate(directory_to_test, file_to_test, False, True, [WorkflowVersionValidator()])

    def test_support_validator(self):
        # Test bad workflows. This will test the workflow_support_validator
        directory_to_test = "workflow_examples/support_tests"
        file_to_test = "workflow_no_supporter.spec.yaml"
        validate(directory_to_test, file_to_test, False, True, [WorkflowSupportValidator()])

    def test_extension_validator(self):
        # Test bad workflows. This will test the workflow_extension_validator
        directory_to_test = "workflow_examples/extension_tests"
        file_to_test = "workflow_extension_not_workflow.spec.yaml"
        validate(directory_to_test, file_to_test, False, True, [WorkflowExtensionValidator()])

    def test_help_validator(self):
        # Test bad workflows. This will test the workflow_help_validator
        directory_to_test = "workflow_examples/help_tests"
        file_to_test = "workflow.spec.yaml"
        validate(directory_to_test, file_to_test, False, True, [WorkflowHelpValidator()])

    def test_change_log_validator(self):
        # Test bad workflows. This will test the workflow_change_log_validator
        directory_to_test = "workflow_examples/change_log_tests"
        file_to_test = "workflow.spec.yaml"
        validate(directory_to_test, file_to_test, False, True, [WorkflowChangelogValidator()])

    def test_files_validator(self):
        # Test bad workflows. This will test the workflow_files_validator
        directory_to_test = "workflow_examples/files_tests"
        file_to_test = "workflow.spec.yaml"
        validate(directory_to_test, file_to_test, False, True, [WorkflowFilesValidator()])

    def test_profanity_validator(self):
        # Test bad workflows. This will test the workflow_profanity_validator
        directory_to_test = "workflow_examples/profanity_tests"
        file_to_test = "workflow_profanity.spec.yaml"
        validate(directory_to_test, file_to_test, False, True, [WorkflowProfanityValidator()])
