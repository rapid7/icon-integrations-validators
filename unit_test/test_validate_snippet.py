import json
import unittest
from typing import Callable

from icon_plugin_spec.plugin_spec import KomandPluginSpec
from parameterized import parameterized

from icon_validator.exceptions import ValidationException
from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.validate import validate

# Import snippet validators to pass to tests
from icon_validator.rules.snippet_validators.snippet_directory_name_match_validator import (
    SnippetDirectoryNameMatchValidator,
)
from icon_validator.rules.snippet_validators.snippet_extension_validator import (
    SnippetExtensionValidator,
)
from icon_validator.rules.snippet_validators.snippet_files_validator import (
    SnippetFilesValidator,
)
from icon_validator.rules.snippet_validators.snippet_help_validator import (
    SnippetHelpValidator,
)
from icon_validator.rules.snippet_validators.snippet_name_validator import (
    SnippetNameValidator,
)
from icon_validator.rules.snippet_validators.snippet_python_script_use_validator import (
    SnippetPythonScriptUseValidator,
)
from icon_validator.rules.snippet_validators.snippet_screenshot_validator import (
    SnippetScreenshotValidator,
)
from icon_validator.rules.snippet_validators.snippet_snpt_filename_validator import (
    SnippetSNPTFileNameValidator,
)
from icon_validator.rules.snippet_validators.snippet_snpt_validator import (
    SnippetSNPTFileValidator,
)
from icon_validator.rules.snippet_validators.snippet_title_validator import (
    SnippetTitleValidator,
)

GOOD_SNIPPET_DIRECTORY = "snippet_examples/Quarantine_asset_with_InsightAgent"
SNIPPET_SPEC = "snippet.spec.yaml"


def load_good_snippet() -> dict:
    with open(f"{GOOD_SNIPPET_DIRECTORY}/Quarantine_asset_with_InsightAgent.snpt", encoding="utf-8") as snpt_file:
        return json.load(snpt_file)


class TestSnippetValidate(unittest.TestCase):
    def assert_validation_fails(
        self, validator: KomandPluginValidator, directory_to_test: str, file_to_test: str, message: str
    ) -> None:
        with self.assertRaises(ValidationException) as context:
            validator.validate(KomandPluginSpec(directory_to_test, file_to_test))
        self.assertIn(message, str(context.exception))

    def test_good_snippet_validator(self):
        # Test good snippet, with no extension.png or screenshots. This should pass all validation
        result = validate(GOOD_SNIPPET_DIRECTORY, SNIPPET_SPEC, False, True)
        self.assertFalse(result)

    def test_files_validator_should_success(self):
        result = validate(GOOD_SNIPPET_DIRECTORY, SNIPPET_SPEC, False, True, [SnippetFilesValidator()])
        self.assertEqual(result, 0)

    def test_files_validator_missing_snpt_should_fail(self):
        self.assert_validation_fails(
            SnippetFilesValidator(),
            "snippet_examples/snpt_file_tests/missing_snpt",
            SNIPPET_SPEC,
            "Snippet file (.snpt) does not exist",
        )

    def test_snpt_file_validator_should_success(self):
        result = validate(GOOD_SNIPPET_DIRECTORY, SNIPPET_SPEC, False, True, [SnippetSNPTFileValidator()])
        self.assertEqual(result, 0)

    @parameterized.expand([
        ("missing_snpt", "snippet_examples/snpt_file_tests/missing_snpt", "No .snpt file was found"),
        (
            "two_snpt_files",
            "snippet_examples/snpt_file_tests/two_snpt_files",
            "must contain exactly one .snpt file, found 2: Copy_of_two_snpt_files.snpt, two_snpt_files.snpt",
        ),
        ("invalid_json", "snippet_examples/snpt_file_tests/invalid_json", "invalid_json.snpt is not in JSON format"),
    ])
    def test_snpt_file_validator_should_fail(self, _name: str, directory_to_test: str, message: str):
        self.assert_validation_fails(SnippetSNPTFileValidator(), directory_to_test, SNIPPET_SPEC, message)

    @parameterized.expand([
        ("missing_name", lambda snippet: snippet.pop("name"), "missing the following keys: name"),
        ("blank_name", lambda snippet: snippet.update(name=" "), "The name key in the .snpt file is not defined"),
        ("missing_steps", lambda snippet: snippet.pop("steps"), "missing the following keys: steps"),
        ("empty_steps", lambda snippet: snippet.update(steps=[]), "The .snpt file has no steps"),
        ("step_missing_type", lambda snippet: snippet["steps"][1].pop("type"), "The type key in steps[1]"),
        ("step_blank_node_id", lambda snippet: snippet["steps"][0].update(nodeId=""), "The nodeId key in steps[0]"),
        ("summary_not_string", lambda snippet: snippet.update(summary=None), "The summary key in the .snpt file"),
        ("tags_not_list", lambda snippet: snippet.update(tags="Asset Management"), "The tags key in the .snpt file"),
        ("missing_input_schema", lambda snippet: snippet.pop("inputSchema"), "missing the following keys: inputSchema"),
        ("graph_missing_edges", lambda snippet: snippet["graph"].pop("edges"), "must contain nodes and edges lists"),
    ])
    def test_snpt_file_validator_fields_should_fail(self, _name: str, break_snippet: Callable, message: str):
        snippet = load_good_snippet()
        break_snippet(snippet)
        with self.assertRaises(ValidationException) as context:
            SnippetSNPTFileValidator.validate_snippet(snippet)
        self.assertIn(message, str(context.exception))

    def test_extension_validator_should_success(self):
        result = validate(GOOD_SNIPPET_DIRECTORY, SNIPPET_SPEC, False, True, [SnippetExtensionValidator()])
        self.assertEqual(result, 0)

    @parameterized.expand([
        ("extension_not_snippet", "snippet_extension_not_snippet.spec.yaml", "must have a value of snippet"),
        ("no_extension", "snippet_no_extension.spec.yaml", "Snippet extension key is missing"),
        ("no_products", "snippet_no_products.spec.yaml", "must be a list that includes insightconnect"),
        (
            "products_not_insightconnect",
            "snippet_products_not_insightconnect.spec.yaml",
            "must be a list that includes insightconnect",
        ),
    ])
    def test_extension_validator_should_fail(self, _name: str, file_to_test: str, message: str):
        self.assert_validation_fails(
            SnippetExtensionValidator(), "snippet_examples/extension_tests", file_to_test, message
        )

    def test_help_validator_should_success(self):
        result = validate(GOOD_SNIPPET_DIRECTORY, SNIPPET_SPEC, False, True, [SnippetHelpValidator()])
        self.assertEqual(result, 0)

    def test_help_validator_missing_header_should_fail(self):
        self.assert_validation_fails(
            SnippetHelpValidator(),
            "snippet_examples/help_tests",
            SNIPPET_SPEC,
            "Help section is missing header: # Key Features.",
        )

    def test_help_validator_initial_workflow_should_fail(self):
        with self.assertRaises(ValidationException):
            SnippetHelpValidator.validate_version_history("# Version History\n\n* 1.0.0 - Initial workflow\n\n")

    def test_directory_name_match_and_name_validators_should_success(self):
        result = validate(
            GOOD_SNIPPET_DIRECTORY,
            SNIPPET_SPEC,
            False,
            True,
            [SnippetDirectoryNameMatchValidator(), SnippetNameValidator(), SnippetSNPTFileNameValidator()],
        )
        self.assertEqual(result, 0)

    def test_directory_name_match_validator_should_fail(self):
        self.assert_validation_fails(
            SnippetDirectoryNameMatchValidator(),
            "snippet_examples/name_tests",
            SNIPPET_SPEC,
            "Expected name_tests.snpt",
        )

    def test_name_validator_should_fail(self):
        self.assert_validation_fails(
            SnippetNameValidator(),
            "snippet_examples/name_tests",
            SNIPPET_SPEC,
            "(name_tests) and the name of the .snpt snippet file (Other_Snippet_Name) do not match",
        )

    def test_snpt_filename_validator_should_fail(self):
        self.assert_validation_fails(
            SnippetSNPTFileNameValidator(),
            "snippet_examples/snpt_filename_tests",
            SNIPPET_SPEC,
            "may not contain spaces",
        )

    def test_screenshot_validator_without_screenshots_should_success(self):
        result = validate(GOOD_SNIPPET_DIRECTORY, SNIPPET_SPEC, False, True, [SnippetScreenshotValidator()])
        self.assertEqual(result, 0)

    def test_screenshot_validator_with_screenshots_should_success(self):
        directory_to_test = "snippet_examples/screenshot_tests"
        file_to_test = "snippet_with_screenshots.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [SnippetScreenshotValidator()])
        self.assertEqual(result, 0)

    def test_screenshot_validator_unlisted_screenshots_should_fail(self):
        self.assert_validation_fails(
            SnippetScreenshotValidator(),
            "snippet_examples/screenshot_tests",
            "snippet_unlisted_screenshots.spec.yaml",
            "The screenshots key under the resources key does not exist",
        )

    def test_screenshot_validator_listed_screenshots_without_directory_should_fail(self):
        self.assert_validation_fails(
            SnippetScreenshotValidator(),
            "snippet_examples/screenshot_tests_no_directory",
            SNIPPET_SPEC,
            "The screenshots directory could not be found",
        )

    def test_title_validator_should_success(self):
        result = validate(GOOD_SNIPPET_DIRECTORY, SNIPPET_SPEC, False, True, [SnippetTitleValidator()])
        self.assertEqual(result, 0)

    def test_title_validator_for_snpt_step_should_fail(self):
        with self.assertRaises(ValidationException) as context:
            SnippetTitleValidator.validate_snpt_titles({"steps": [{"name": "Loop over User RRNs"}]})
        self.assertIn("Title contains a lowercase 'over' when it should not in .snpt file.", str(context.exception))

    def test_python_script_use_validator_should_success(self):
        result = validate(GOOD_SNIPPET_DIRECTORY, SNIPPET_SPEC, False, True, [SnippetPythonScriptUseValidator()])
        self.assertEqual(result, 0)

    def test_python_script_use_validator_finds_python_steps(self):
        snippet = load_good_snippet()
        snippet["steps"].append({
            "nodeId": "8c4f3b52-6d0e-4f7a-9b1c-2e5d7a9f0c13",
            "name": "Run Script",
            "type": "action",
            "metadata": {"plugin": {"name": "python_3_script", "vendor": "rapid7", "version": "4.0.10"}},
        })
        self.assertEqual(SnippetPythonScriptUseValidator().python_plugin_used(snippet), ["Run Script"])
