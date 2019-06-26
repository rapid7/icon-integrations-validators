"""
The rules package provides the array VALIDATORS which contains all the validators for
validating InsightConnect plugins.
"""

from .files_validator import *
from .description_validator import *
from .title_validator import *
from .required_keys_validator import *
from .tag_validator import *
from .dockerfile_parent_validator import *
from .default_value_validator import *
from .vendor_validator import *
from .icon_validator import *
from .required_validator import *
from .makefile_validator import *
from .version_validator import *
from .help_validator import *
from .spec_version_validator import *
from .docker_validator import *
from .logging_validator import *
from .spec_properties_validator import *

# The order of this list is the execution order of the validators.
VALIDATORS = [
    SpecPropertiesValidator(),
    FilesValidator(),
    RequiredKeysValidator(),
    TagValidator(),
    DescriptionValidator(),
    TitleValidator(),
    VendorValidator(),
    DefaultValueValidator(),
    IconValidator(),
    RequiredValidator(),
    MakefileValidator(),
    VersionValidator(),
    HelpValidator(),
    SpecVersionValidator(),
    DockerfileParentValidator(),
    DockerValidator(),
    LoggingValidator(),
]
