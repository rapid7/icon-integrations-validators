import unittest
from icon_validator.exceptions import NO_LOCAL_CON_VERSION, NO_CON_VERSION_CHANGE, \
    INVALID_CON_VERSION_CHANGE, INCORRECT_CON_VERSION_CHANGE, FIRST_TIME_CON_VERSION_ISSUE
from icon_validator.validate import validate
from icon_validator.exceptions import ValidationException
from icon_plugin_spec.plugin_spec import KomandPluginSpec

# Import plugin validators to pass to tests
from icon_validator.rules.plugin_validators.title_validator import TitleValidator
from icon_validator.rules.plugin_validators.profanity_validator import ProfanityValidator
from icon_validator.rules.plugin_validators.version_validator import VersionValidator
from icon_validator.rules.plugin_validators.version_pin_validator import VersionPinValidator
from icon_validator.rules.plugin_validators.encoding_validator import EncodingValidator
from icon_validator.rules.plugin_validators.example_input_validator import ExampleInputValidator
from icon_validator.rules.plugin_validators.cloud_ready_connection_credential_token_validator import \
    CloudReadyConnectionCredentialTokenValidator
from icon_validator.rules.plugin_validators.use_case_validator import UseCaseValidator
from icon_validator.rules.plugin_validators.help_validator import HelpValidator
from icon_validator.rules.plugin_validators.confidential_validator import ConfidentialValidator
from icon_validator.rules.plugin_validators.description_validator import DescriptionValidator
from icon_validator.rules.plugin_validators.cloud_ready_validator import CloudReadyValidator
from icon_validator.rules.plugin_validators.acronym_validator import AcronymValidator
from icon_validator.rules.plugin_validators.unapproved_keywords_validator import UnapprovedKeywordsValidator
from icon_validator.rules.plugin_validators.version_bump_validator import VersionBumpValidator
from icon_validator.rules.plugin_validators.supported_version_validator import SupportedVersionValidator
from icon_validator.rules.plugin_validators.help_input_output_validator import convert_to_valid_datetime
from icon_validator.rules.plugin_validators.name_validator import NameValidator
from icon_validator.rules.plugin_validators.output_validator import OutputValidator

import requests
from unittest.mock import MagicMock, patch
import os
from parameterized import parameterized


class TestPluginValidate(unittest.TestCase):

    NAME_TESTS_DIRECTORY = "plugin_examples/name_tests"
    GOOD_PLUGIN_DIRECTORY = "plugin_examples/good_plugin"

    @parameterized.expand([
        ('2023-12-24 12:56:15+05:00', '2023-12-24T12:56:15+05:00'),
        ('2023-12-24 12:56:15', '2023-12-24T12:56:15')
    ])
    def test_convert_valid_datetime(self, table_string: str, expected: str):
        response = convert_to_valid_datetime(table_string)
        self.assertEqual(expected, response)

    def test_plugin_validate(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_plugin"
        file_to_test = "plugin.spec.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, False)
        self.assertEqual(result, 0)

    def test_plugin_validate_with_task(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_plugin_with_task"
        file_to_test = "plugin.spec.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, False)
        self.assertEqual(result, 0)

    def test_title_validator(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/title_tests"
        file_to_test = "plugin_no_title.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [TitleValidator()])
        self.assertEqual(result, 1)

    def test_title_validator_with_number_in_title(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_number_title"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [TitleValidator()])
        self.assertEqual(result, 0)

    def test_title_validator_validator_capitalized_word_where_should_not_should_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_no_example_in_spec"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [TitleValidator()])
        self.assertEqual(result, 1)

    def test_profanity_validator(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/profanity_tests"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [ProfanityValidator()])
        self.assertEqual(result, 1)

    def test_encoding_validator_should_success(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/encoding_tests"
        file_to_test = "plugin_good_encoding.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [EncodingValidator()])
        self.assertEqual(result, 0)

    def test_encoding_validator(self):
        directory_to_test = "plugin_examples/encoding_tests"
        file_to_test = "plugin_bad_encoding.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [EncodingValidator()])
        self.assertEqual(result, 1)

    def test_version_validator(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/version_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionValidator()])
        self.assertEqual(result, 0)

    def test_version_validator_major_version_ten(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/version_validator"
        file_to_test = "plugin.spec_ten.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionValidator()])
        self.assertEqual(result, 0)

    def test_version_validator_should_fail_when_version_same_in_api(self):
        # example workflow in plugin_examples directory. Run tests with these files
        version = requests.get(
            url=f"https://extensions-api.rapid7.com/v2/public/extensions/active_directory_ldap",
            timeout=3
        ).json()["version"]

        f = open("./plugin_examples/version_validator/plugin.spec_bad.yaml", 'w')
        f.write(f"plugin_spec_version: v2\nname: active_directory_ldap\nversion: {version}")
        f.close()
        directory_to_test = "plugin_examples/version_validator"
        file_to_test = "plugin.spec_bad.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionValidator()])
        self.assertEqual(result, 1)

    def test_version_pin_validator_should_success(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_test"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionPinValidator()])
        self.assertEqual(result, 0)

    def test_version_pin_validator_should_fail_when_question_mark(self):
        self.replace_requirements("./plugin_examples/version_pin_validator/requirements.txt", "?ldap3")
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/version_pin_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionPinValidator()])
        self.assertEqual(result, 1)

    def test_version_pin_validator_should_fail_when_one_equal_sign(self):
        self.replace_requirements("./plugin_examples/version_pin_validator/requirements.txt", "ldap3=2.6")
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/version_pin_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionPinValidator()])
        self.assertEqual(result, 1)

    def test_version_pin_validator_should_fail_when_no_version_pin(self):
        self.replace_requirements("./plugin_examples/version_pin_validator/requirements.txt", "ldap3")
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/version_pin_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionPinValidator()])
        self.assertEqual(result, 1)

    def test_version_pin_validator_should_fail_when_no_version_pin_in_one_of_multiple_version_first_test(self):
        self.replace_requirements("./plugin_examples/version_pin_validator/requirements.txt",
                                  "ldap3===1.2.3,ldap3xxxx1.2.3")
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/version_pin_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionPinValidator()])
        self.assertEqual(result, 1)

    def test_version_pin_validator_should_fail_when_no_version_pin_in_one_of_multiple_version_second_test(self):
        self.replace_requirements("./plugin_examples/version_pin_validator/requirements.txt",
                                  "ldap3xxxx1.2.3,ldap3===1.2.3")
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/version_pin_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionPinValidator()])
        self.assertEqual(result, 1)

    def test_version_pin_validator_should_success_when_three_equal(self):
        self.replace_requirements("./plugin_examples/version_pin_validator/requirements.txt", "ldap3===1.2.3")
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/version_pin_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionPinValidator()])
        self.assertEqual(result, 0)

    def test_version_pin_validator_should_success_when_minority_sign(self):
        self.replace_requirements("./plugin_examples/version_pin_validator/requirements.txt", "ldap3<1.2.3")
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/version_pin_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionPinValidator()])
        self.assertEqual(result, 0)

    def test_version_pin_validator_should_success_when_minority_equal_sign(self):
        self.replace_requirements("./plugin_examples/version_pin_validator/requirements.txt", "ldap3<=1.2.3")
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/version_pin_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionPinValidator()])
        self.assertEqual(result, 0)

    def test_version_pin_validator_should_success_when_git(self):
        self.replace_requirements("./plugin_examples/version_pin_validator/requirements.txt",
                                  "git+git://github.com/komand/pycrits@1.0.0#egg=pycrits")
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/version_pin_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionPinValidator()])
        self.assertEqual(result, 0)

    def test_version_pin_validator_should_success_when_majority_sign(self):
        self.replace_requirements("./plugin_examples/version_pin_validator/requirements.txt", "ldap3>1.2.3")
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/version_pin_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionPinValidator()])
        self.assertEqual(result, 0)

    def test_version_pin_validator_should_success_when_majority_equal_sign(self):
        self.replace_requirements("./plugin_examples/version_pin_validator/requirements.txt", "ldap3>=1.2.3")
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/version_pin_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionPinValidator()])
        self.assertEqual(result, 0)

    def test_version_pin_validator_should_success_when_not_equal_sign(self):
        self.replace_requirements("./plugin_examples/version_pin_validator/requirements.txt", "ldap3!=1.2.3")
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/version_pin_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionPinValidator()])
        self.assertEqual(result, 0)

    def test_version_pin_validator_should_success_when_tilda_equal_sign(self):
        self.replace_requirements("./plugin_examples/version_pin_validator/requirements.txt", "ldap3~=1.2.3")
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/version_pin_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionPinValidator()])
        self.assertEqual(result, 0)

    def test_version_pin_validator_should_success_when_many_versions(self):
        self.replace_requirements("./plugin_examples/version_pin_validator/requirements.txt", "ldap3<1.2.3,ldap3==1-2-3")
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/version_pin_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [VersionPinValidator()])
        self.assertEqual(result, 0)

    def test_plugin_with_false_for_required_on_output(self):
        # TODO This validator is not correctly made: fix
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_no_required_key_in_output"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True)
        self.assertEqual(result, 1)

    def test_example_input_validator_should_success(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_test"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [ExampleInputValidator()])
        self.assertEqual(result, 0)

    def test_example_input_validator_should_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_no_example_in_spec"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [ExampleInputValidator()])
        self.assertEqual(result, 1)

    def test_example_input_validator_should_fail_when_not_all_exists(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_array_in_help"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [ExampleInputValidator()])
        self.assertEqual(result, 1)

    def test_example_input_validator_should_success_when_example_are_0_false(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_plugin_example_in_spec_0_false"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [ExampleInputValidator()])
        self.assertEqual(result, 0)

    def test_example_input_validator_pass_with_no_action_input(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_plugin_no_input"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [ExampleInputValidator()])
        self.assertEqual(result, 0)

    def test_cloud_ready_connection_credential_token_validator_should_fail(self):
        directory_to_test = "plugin_examples/cloud_ready_connection_credential_token_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True,
                          [CloudReadyConnectionCredentialTokenValidator()])
        self.assertEqual(result, 1)

    def test_use_case_validator_should_success(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_plugin"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [UseCaseValidator()])
        self.assertEqual(result, 0)

    def test_use_case_validator_use_case_not_from_list_should_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_bad_use_case_in_spec"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [UseCaseValidator()])
        self.assertEqual(result, 1)

    def test_use_case_validator_use_case_empty_should_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_no_use_case_in_spec"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [UseCaseValidator()])
        self.assertEqual(result, 1)

    def test_use_case_validator_keywords_from_use_case_list_should_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_keywords_from_use_case_list_in_spec"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [UseCaseValidator()])
        self.assertEqual(result, 1)

    def test_help_validator_duplicate_headings_should_success(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_plugin"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [HelpValidator()])
        self.assertEqual(result, 0)

    def test_help_validator_duplicate_headings_should_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_duplicate_headings_in_help"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [HelpValidator()])
        self.assertEqual(result, 1)

    def test_help_validator_help_headers_should_success(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_plugin"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [HelpValidator()])
        self.assertEqual(result, 0)

    def test_help_validator_help_headers_missing_should_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_missing_headings_in_help"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [HelpValidator()])
        self.assertEqual(result, 1)

    def test_help_validator_help_headers_not_found_should_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_headings_not_found_in_help"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [HelpValidator()])
        self.assertEqual(result, 1)

    def test_confidential_validator_validate_email_should_print_warning(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_plugin_warning_keywords"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [ConfidentialValidator()])
        self.assertEqual(result, 0)

    def test_confidential_validator_validate_email_should_success(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_plugin_validate_email"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [ConfidentialValidator()])
        self.assertEqual(result, 0)

    def test_description_validator_validate_existed_description_should_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_no_description"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [DescriptionValidator()])
        self.assertEqual(result, 1)

    def test_description_validator_validate_existed_description_should_success(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_plugin"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [DescriptionValidator()])
        self.assertEqual(result, 0)

    def test_cloud_ready_validator_bad_python_image_should_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_cloud_ready_bad_docker_image"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [CloudReadyValidator()])
        self.assertEqual(result, 1)

    def test_cloud_ready_validator_user_root_should_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_cloud_ready_user_root"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [CloudReadyValidator()])
        self.assertEqual(result, 1)

    def test_cloud_ready_validator_dockerfile_apt_should_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_cloud_ready_dockerfile_apt_apk"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [CloudReadyValidator()])
        self.assertEqual(result, 1)

    def test_cloud_ready_validator_enable_cache_true_should_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_cloud_ready_enable_cache_true"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [CloudReadyValidator()])
        self.assertEqual(result, 1)

    def test_cloud_ready_validator_system_command_should_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/bad_plugin_cloud_ready_system_command"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [CloudReadyValidator()])
        self.assertEqual(result, 1)

    def test_cloud_ready_validator_should_success(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_plugin_cloud_ready"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [CloudReadyValidator()])
        self.assertEqual(result, 0)

    def test_cloud_ready_validator_should_success_latest_version_string(self):
        # Test when a cloud ready plugin specifies ':latest' as SDK image regex still validates
        docker_file = directory_to_test = "plugin_examples/good_plugin_cloud_ready/Dockerfile"
        with open(docker_file, "r") as file:
            docker_str = file.read().replace(":5", ":latest")
            try:
                CloudReadyValidator().validate_python_version_in_dockerfile(docker_str)
            except ValidationException:
                raise Exception("We do not expect the supplied docker string to fail. We should support ':latest'")

    def test_acronym_validator_should_success(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_plugin"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [AcronymValidator()])
        self.assertEqual(result, 0)

    def test_acronym_validator_lower_acronym_help_should_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/acronym_validator_help_bad"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [AcronymValidator()])
        self.assertEqual(result, 1)

    def test_acronym_validator_lower_acronym_plugin_spec_should_fail(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/acronym_validator_spec_bad"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [AcronymValidator()])
        self.assertEqual(result, 1)

    def test_unapproved_keywords_validator_should_success_without_warning(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_plugin"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [UnapprovedKeywordsValidator()])
        self.assertEqual(result, 0)

    def test_unapproved_keywords_validator_should_print_warning(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/good_plugin_warning_keywords"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [UnapprovedKeywordsValidator()])
        self.assertEqual(result, 0)

    def test_major_version_action_removed_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_major_version_bump_all"
        file_to_test = "plugin.spec.bad.action.removed.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_major_version_action_title_changed_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_major_version_bump_all"
        file_to_test = "plugin.spec.bad.action.title.changed.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_major_version_connection_input_removed_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_major_version_bump_all"
        file_to_test = "plugin.spec.bad.connection.input.removed.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_major_version_input_now_required_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_major_version_bump_all"
        file_to_test = "plugin.spec.bad.input.now.required.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_major_version_input_removed_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_major_version_bump_all"
        file_to_test = "plugin.spec.bad.input.removed.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_major_version_title_changes_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_major_version_bump_all"
        file_to_test = "plugin.spec.bad.input.title.changes.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_major_version_type_change_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_major_version_bump_all"
        file_to_test = "plugin.spec.bad.input.type.change.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_major_version_new_required_connection_input_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_major_version_bump_all"
        file_to_test = "plugin.spec.bad.new.input.required.connection.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_major_version_new_required_input_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_major_version_bump_all"
        file_to_test = "plugin.spec.bad.new.required.input.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_major_version_output_nolonger_required_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_major_version_bump_all"
        file_to_test = "plugin.spec.bad.output.nolonger.required.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_major_version_trigger_removed_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_major_version_bump_all"
        file_to_test = "plugin.spec.bad.trigger.removed.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_major_version_trigger_renamed_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_major_version_bump_all"
        file_to_test = "plugin.spec.bad.trigger.renamed.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_major_version_type_changed_connection_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_major_version_bump_all"
        file_to_test = "plugin.spec.bad.type.changed.connection.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_major_version_type_removed_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_major_version_bump_all"
        file_to_test = "plugin.spec.bad.type.removed.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_major_version_type_subtype_removed_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_major_version_bump_all"
        file_to_test = "plugin.spec.bad.type.subtype.removed.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_major_version_action_removed_bump_applied_succeed(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_major_version_bump_all"
        file_to_test = "plugin.spec.good.action.removedandbumped.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 0)

    def test_major_version_new_optional_connection_input_succeed(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_major_version_bump_all"
        file_to_test = "plugin.spec.good.new.connection.input.optional.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 0)

    def test_version_new_optional_action_input_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_minor_version_bump_all"
        file_to_test = "plugin.spec.bad.new.input.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_version_new_action_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_minor_version_bump_all"
        file_to_test = "plugin.spec.bad.new.action.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_version_new_trigger_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_minor_version_bump_all"
        file_to_test = "plugin.spec.bad.new.trigger.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_version_new_output_should_fail(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_minor_version_bump_all"
        file_to_test = "plugin.spec.bad.new.output.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 1)

    def test_version_new_output_bumped_succeed(self):
        # example spec in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/plugin_minor_version_bump_all"
        file_to_test = "plugin.spec.good.new.output.bumped.yaml"
        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(directory_to_test)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec)
        result = validate(directory_to_test, file_to_test, False, True, [VersionBumpValidator()])
        self.assertEqual(result, 0)

    @parameterized.expand([
        # ('test_name', new_yaml, exception, mock_local_spec)
        ('initial_no_connection', "plugin.spec.good.new.nonrequired.input.yaml", NO_LOCAL_CON_VERSION, False),
        ('changed_con_schema_no_ver_bump', "plugin.spec.bad.new.connection.yaml", NO_CON_VERSION_CHANGE, True),
        ('changed_con_schema_with_ver_bump', "plugin.spec.good.new.connection.yaml", None, True),
        ('invalid_con_ver_bump', "plugin.spec.bad.connection.change.yaml", INVALID_CON_VERSION_CHANGE, True),
        ('incorrect_con_ver_bump', "plugin.spec.bad.new.connection.version.yaml", INCORRECT_CON_VERSION_CHANGE, True),
        ('initial_version_connection', "plugin.spec.good.new.connection.yaml", None, True),
        ('bad_initial_version_con', "plugin.spec.bad.new.connection.version.yaml", FIRST_TIME_CON_VERSION_ISSUE, True)
    ])
    @patch('builtins.print')
    def test_plugin_connection_version(self, test_name, local_yaml, exp_exception, mock_spec, mock_print):
        """
        Tests and explanation of passing vs error reasoning. If mocking the remote_spec our util file looks in the
        specified directory for the spec file named: `plugin.spec.remote.yaml`
        - #1: connection params are present but no version has been specified, we should error.
        - #2: connection details have changed from previous plugin spec, the version should have been bumped.
        - #3: happy path that we have updated connection details and bumped the connection version correctly.
        - #4: connection version has changed when it was not required, we want to error on this.
        - #5: connection version should match the plugin version major version, error that these do not match.
        - #6: first time plugin is released with a connection version specified, previously no con version was included.
        - #7: first time plugin is specifying the connection version and this does not match the plugin major version.
        """
        directory_to_test = "plugin_examples/plugin_major_version_bump_all"

        if test_name in ["initial_version_connection", "bad_initial_version_con"]:
            remote_dir = "plugin_examples/plugin_minor_version_bump_all"  # no remote connection version in this spec
        else:
            remote_dir = directory_to_test

        remote_spec = MockRepoSpecResponse.mock_patch_remote_spec_major_version(remote_dir)
        VersionBumpValidator.get_remote_spec = MagicMock(return_value=remote_spec if mock_spec else None)

        result = validate(directory_to_test, local_yaml, False, True, [VersionBumpValidator()])
        exit_code = 0
        if exp_exception:
            exit_code = 1
            for mocked_print in mock_print.call_args_list:
                if f'Validator "{VersionBumpValidator().name}" failed!' in mocked_print[0][0]:
                    self.assertIn(exp_exception, mocked_print[0][0])
        self.assertEqual(result, exit_code)

    def test_supported_version_validator(self):
        # example workflow in plugin_examples directory. Run tests with these files
        directory_to_test = "plugin_examples/supported_version_validator"
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [SupportedVersionValidator()])
        self.assertEqual(result, 0)

    def test_supported_version_validator_sup_vers_null(self):
        directory_to_test = "plugin_examples/supported_version_validator"
        file_to_test = "plugin.spec_bad.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [SupportedVersionValidator()])
        self.assertEqual(result, 1)

    def test_supported_version_validator_spec_empty(self):
        directory_to_test = "plugin_examples/supported_version_validator"
        file_to_test = "plugin.spec_bad_empty.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [SupportedVersionValidator()])
        self.assertEqual(result, 1)

    def test_supported_version_validator_sup_vers_empty(self):
        directory_to_test = "plugin_examples/supported_version_validator"
        file_to_test = "plugin.spec_bad_missing_value.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [SupportedVersionValidator()])
        self.assertEqual(result, 1)

    @parameterized.expand([
        ('long_name', 'long_name.spec.yaml'),
        ('blank_name', 'blank_name.spec.yaml'),
        ('missing_name', 'missing_name.spec.yaml'),
        ('non_alphanumeric_name', 'non_alphanumeric_name.spec.yaml'),
        ('not_string_name', 'not_string_name.spec.yaml'),
        ('uppercase_name.spec', 'uppercase_name.spec.yaml'),
        ('whitespace_name', 'whitespace_name.spec.yaml')
    ])
    def test_bad_name_validator(self, _test_name: str, test_plugin_spec: str):
        directory_to_test = self.NAME_TESTS_DIRECTORY
        file_to_test = test_plugin_spec
        result = validate(directory_to_test, file_to_test, False, True, [NameValidator()])
        self.assertEqual(result, 1)

    def test_good_name_validator(self):
        directory_to_test = self.NAME_TESTS_DIRECTORY
        file_to_test = "good_name.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [NameValidator()])
        self.assertEqual(result, 0)

    def test_schema_output_validator(self) -> None:
        directory_to_test = self.GOOD_PLUGIN_DIRECTORY
        file_to_test = "plugin.spec.yaml"
        result = validate(directory_to_test, file_to_test, False, True, [OutputValidator()])
        self.assertEqual(result, 0)

    @staticmethod
    def replace_requirements(path, text):
        f = open(path, 'w')
        f.write(text)
        f.close()


class MockRepoSpecResponse:
    @staticmethod
    def mock_patch_remote_spec_major_version(directory):
        final_name = "plugin.spec.remote.yaml"
        # if the "remote" spec exists, use that
        if os.path.exists(os.path.join(directory, final_name)):
            spec = KomandPluginSpec(directory, final_name)
        # otherwise, just use a copy of the existing spec
        else:
            spec = KomandPluginSpec(directory, "plugin.spec.yaml")
        spec_dict = spec.spec_dictionary()
        return spec_dict
