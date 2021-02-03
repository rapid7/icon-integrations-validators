"""
The rules package provides the array VALIDATORS which contains all the validators for
validating InsightConnect plugins and workflows.
"""

# Plugin validators
from icon_validator.rules.plugin_validators.acronym_validator import *
from icon_validator.rules.plugin_validators.changelog_validator import *
from icon_validator.rules.plugin_validators.confidential_validator import *
from icon_validator.rules.plugin_validators.cloud_ready_connection_credential_token_validator import *
from icon_validator.rules.plugin_validators.credentials_validator import *
from icon_validator.rules.plugin_validators.default_value_validator import *
from icon_validator.rules.plugin_validators.description_validator import *
from icon_validator.rules.plugin_validators.docker_validator import *
from icon_validator.rules.plugin_validators.dockerfile_parent_validator import *
from icon_validator.rules.plugin_validators.encoding_validator import *
from icon_validator.rules.plugin_validators.exception_validator import *
from icon_validator.rules.plugin_validators.files_validator import *
from icon_validator.rules.plugin_validators.help_input_output_validator import *
from icon_validator.rules.plugin_validators.help_validator import *
from icon_validator.rules.plugin_validators.icon_validator import *
from icon_validator.rules.plugin_validators.json_validator import *
from icon_validator.rules.plugin_validators.logging_validator import *
from icon_validator.rules.plugin_validators.output_validator import *
from icon_validator.rules.plugin_validators.password_validator import *
from icon_validator.rules.plugin_validators.print_validator import *
from icon_validator.rules.plugin_validators.profanity_validator import *
from icon_validator.rules.plugin_validators.regeneration_validator import *
from icon_validator.rules.plugin_validators.required_keys_validator import *
from icon_validator.rules.plugin_validators.required_validator import *
from icon_validator.rules.plugin_validators.spec_properties_validator import *
from icon_validator.rules.plugin_validators.spec_version_validator import *
from icon_validator.rules.plugin_validators.tag_validator import *
from icon_validator.rules.plugin_validators.title_validator import *
from icon_validator.rules.plugin_validators.url_validator import *
from icon_validator.rules.plugin_validators.use_case_validator import *
from icon_validator.rules.plugin_validators.vendor_validator import *
from icon_validator.rules.plugin_validators.version_validator import *
from icon_validator.rules.plugin_validators.version_pin_validator import *
from icon_validator.rules.plugin_validators.support_validator import *
from icon_validator.rules.plugin_validators.runtime_validator import *
from icon_validator.rules.plugin_validators.version_pin_validator import *
from icon_validator.rules.plugin_validators.example_input_validator import *

# Workflow validators
from icon_validator.rules.workflow_validators.workflow_directory_name_match_validator import *
from icon_validator.rules.workflow_validators.workflow_help_validator import *
from icon_validator.rules.workflow_validators.workflow_files_validator import *
from icon_validator.rules.workflow_validators.workflow_extension_validator import *
from icon_validator.rules.workflow_validators.workflow_change_log_validator import *
from icon_validator.rules.workflow_validators.workflow_vendor_validator import *
from icon_validator.rules.workflow_validators.workflow_version_validator import *
from icon_validator.rules.workflow_validators.workflow_support_validator import *
from icon_validator.rules.workflow_validators.workflow_profanity_validator import *
from icon_validator.rules.workflow_validators.workflow_png_hash_validator import *
from icon_validator.rules.workflow_validators.workflow_icon_filename_validator import *
from icon_validator.rules.workflow_validators.workflow_screenshot_validator import *
from icon_validator.rules.workflow_validators.workflow_title_validator import *
from icon_validator.rules.workflow_validators.workflow_description_validator import *
from icon_validator.rules.workflow_validators.workflow_name_validator import *
from icon_validator.rules.workflow_validators.workflow_icon_validator import *
from icon_validator.rules.workflow_validators.workflow_help_plugin_utilization_validator import *
from icon_validator.rules.workflow_validators.workflow_encoding_validator import *

# The order of this list is the execution order of the validators.
VALIDATORS = [
    HelpValidator(),
    ChangelogValidator(),
    CloudReadyConnectionCredentialTokenValidator(),
    RequiredKeysValidator(),
    UseCaseValidator(),
    SpecPropertiesValidator(),
    SpecVersionValidator(),
    FilesValidator(),
    TagValidator(),
    DescriptionValidator(),
    TitleValidator(),
    VendorValidator(),
    DefaultValueValidator(),
    IconValidator(),
    RequiredValidator(),
    VersionValidator(),
    DockerfileParentValidator(),
    LoggingValidator(),
    ProfanityValidator(),
    AcronymValidator(),
    JSONValidator(),
    OutputValidator(),
    RegenerationValidator(),
    HelpInputOutputValidator(),
    SupportValidator(),
    RuntimeValidator(),
    VersionPinValidator(),
    EncodingValidator(),
    ExampleInputValidator(),
]

JENKINS_VALIDATORS = [
    ExceptionValidator(),
    CredentialsValidator(),
    PasswordValidator(),
    PrintValidator(),
    ConfidentialValidator(),
    DockerValidator(),
    URLValidator(),
]

WORKFLOW_VALIDATORS = [
    WorkflowDirectoryNameMatchValidator(),
    WorkflowFilesValidator(),
    WorkflowHelpValidator(),
    WorkflowChangelogValidator(),
    WorkflowVendorValidator(),
    WorkflowVersionValidator(),
    WorkflowExtensionValidator(),
    WorkflowSupportValidator(),
    WorkflowPNGHashValidator(),
    WorkflowICONFileNameValidator(),
    WorkflowScreenshotValidator(),
    WorkflowTitleValidator(),
    WorkflowDescriptionValidator(),
    WorkflowNameValidator(),
    WorkflowProfanityValidator(),
    WorkflowHelpPluginUtilizationValidator(),
    WorkflowICONFileValidator(),
    WorkflowEncodingValidator(),
]
