import unittest
from icon_validator.validate import validate

# Import workflow validators to pass to tests
from icon_validator.rules.workflow_validators.workflow_profanity_validator import WorkflowProfanityValidator
from icon_validator.rules.workflow_validators.workflow_vendor_validator import WorkflowVendorValidator
from icon_validator.rules.workflow_validators.workflow_support_validator import WorkflowSupportValidator
from icon_validator.rules.workflow_validators.workflow_version_validator import WorkflowVersionValidator
from icon_validator.rules.workflow_validators.workflow_change_log_validator import WorkflowChangelogValidator
from icon_validator.rules.workflow_validators.workflow_extension_validator import WorkflowExtensionValidator
from icon_validator.rules.workflow_validators.workflow_files_validator import WorkflowFilesValidator
from icon_validator.rules.workflow_validators.workflow_help_validator import WorkflowHelpValidator
from icon_validator.rules.workflow_validators.workflow_png_hash_validator import WorkflowPNGHashValidator
from icon_validator.rules.workflow_validators.workflow_icon_filename_validator import WorkflowICONFileNameValidator
from icon_validator.rules.workflow_validators.workflow_screenshot_validator import WorkflowScreenshotValidator
from icon_validator.rules.workflow_validators.workflow_title_validator import WorkflowTitleValidator
from icon_validator.rules.workflow_validators.workflow_description_validator import WorkflowDescriptionValidator
from icon_validator.rules.workflow_validators.workflow_name_validator import WorkflowNameValidator
from icon_validator.rules.workflow_validators.workflow_icon_validator import WorkflowICONFileValidator
from icon_validator.rules.workflow_validators.workflow_help_plugin_utilization_validator import WorkflowHelpPluginUtilizationValidator
from icon_validator.rules.workflow_validators.workflow_spelling_validator import WorkflowSpellingValidator


class TestWorkflowValidate(unittest.TestCase):

    def test_good_workflow_validator(self):
        # Test good workflow. This should pass all validation
        directory_to_test = "workflow_examples/Automated_Indicator_Enrichment"
        file_to_test = "workflow.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True)
        self.assertFalse(result)

    def test_vendor_validator(self):
        # Test bad workflows. This will test the workflow_vendor_validator
        directory_to_test = "workflow_examples/vendor_tests"
        file_to_test = "workflow_no_vendor.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [WorkflowVendorValidator()])
        self.assertTrue(result)

    def test_version_validator(self):
        # Test bad workflows. This will test the workflow_version_validator
        directory_to_test = "workflow_examples/version_tests"
        file_to_test = "workflow_version_too_low.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [WorkflowVersionValidator()])
        self.assertTrue(result)

    def test_support_validator(self):
        # Test bad workflows. This will test the workflow_support_validator
        directory_to_test = "workflow_examples/support_tests"
        file_to_test = "workflow_no_supporter.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [WorkflowSupportValidator()])
        self.assertTrue(result)

    def test_extension_validator(self):
        # Test bad workflows. This will test the workflow_extension_validator
        directory_to_test = "workflow_examples/extension_tests"
        file_to_test = "workflow_extension_not_workflow.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [WorkflowExtensionValidator()])
        self.assertTrue(result)

    def test_help_validator(self):
        # Test bad workflows. This will test the workflow_help_validator
        directory_to_test = "workflow_examples/help_tests"
        file_to_test = "workflow.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [WorkflowHelpValidator()])
        self.assertTrue(result)

    def test_change_log_validator(self):
        # Test bad workflows. This will test the workflow_change_log_validator
        directory_to_test = "workflow_examples/change_log_tests"
        file_to_test = "workflow.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [WorkflowChangelogValidator()])
        self.assertTrue(result)

    def test_files_validator(self):
        # Test bad workflows. This will test the workflow_files_validator
        directory_to_test = "workflow_examples/files_tests"
        file_to_test = "workflow.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [WorkflowFilesValidator()])
        self.assertTrue(result)

    def test_profanity_validator(self):
        # Test bad workflows. This will test the workflow_profanity_validator
        directory_to_test = "workflow_examples/profanity_tests"
        file_to_test = "workflow_profanity.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [WorkflowProfanityValidator()])
        self.assertTrue(result)

    def test_png_hash_validator(self):
        # Test bad workflows. This will test the workflow_png_hash_validator
        directory_to_test = "workflow_examples/png_hash_tests"
        file_to_test = "workflow.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [WorkflowPNGHashValidator()])
        self.assertTrue(result)

    def test_icon_filename_validator(self):
        # Test bad workflows. This will test the workflow_icon_filename_validator
        directory_to_test = "workflow_examples/icon_filename_tests"
        file_to_test = "workflow.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [WorkflowICONFileNameValidator()])
        self.assertTrue(result)

    def test_screenshots_validator(self):
        # Test bad workflows. This will test the workflow_screenshot_validator
        directory_to_test = "workflow_examples/screenshot_tests"
        file_to_test = "workflow_bad_title.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [WorkflowScreenshotValidator()])
        self.assertTrue(result)
        file_to_test = "workflow_missing_key.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [WorkflowScreenshotValidator()])
        self.assertTrue(result)
        file_to_test = "workflow_missing_name.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [WorkflowScreenshotValidator()])
        self.assertTrue(result)
        file_to_test = "workflow_missing_title.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [WorkflowScreenshotValidator()])
        self.assertTrue(result)

    def test_title_validator(self):
        # Test bad workflows. This will test the workflow_title_validator
        directory_to_test = "workflow_examples/title_tests"
        file_to_test = "workflow_no_title.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [WorkflowTitleValidator()])
        self.assertTrue(result)
        file_to_test = "workflow_ends_with_period.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [WorkflowTitleValidator()])
        self.assertTrue(result)
        file_to_test = "workflow_bad_caps.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [WorkflowTitleValidator()])
        self.assertTrue(result)
        file_to_test = "numeric_in_title.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [WorkflowTitleValidator()])
        self.assertEqual(result, 0)  # Should be a valid title

    def test_description_validator(self):
        # Test bad workflows. This will test the workflow_description_validator
        directory_to_test = "workflow_examples/description_tests"
        file_to_test = "workflow_no_description.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [WorkflowDescriptionValidator()])
        self.assertTrue(result)
        file_to_test = "workflow_no_period.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [WorkflowDescriptionValidator()])
        self.assertTrue(result)
        file_to_test = "workflow_whitespace.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [WorkflowDescriptionValidator()])
        self.assertTrue(result)
        file_to_test = "workflow_blank_description.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [WorkflowDescriptionValidator()])
        self.assertTrue(result)
        file_to_test = "workflow_lower_case.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [WorkflowDescriptionValidator()])
        self.assertTrue(result)

    def test_name_validator(self):
        # Test bad workflows. This will test the workflow_icon_filename_validator
        directory_to_test = "workflow_examples/name_tests"
        file_to_test = "workflow_bad_name.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [WorkflowNameValidator()])
        self.assertTrue(result)

    def test_icon_validator(self):
        directory_to_test = "workflow_examples/icon_file_tests"
        file_to_test = "workflow_bad_icon_file.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [WorkflowICONFileValidator()])
        self.assertTrue(result)

    def test_workflow_plugin_utilization_validator(self):
        directory_to_test = "workflow_examples/plugin_utilization_tests"
        file_to_test = "workflow_bad_utilization.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [WorkflowHelpPluginUtilizationValidator()])
        self.assertTrue(result)

    def test_spelling_validator(self):
        # Test bad workflows. This will test the workflow_spelling_validator
        directory_to_test = "workflow_examples/spelling_tests"
        file_to_test = "workflow_spelling.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [WorkflowSpellingValidator()])
        self.assertTrue(result)