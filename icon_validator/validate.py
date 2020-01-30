#! /usr/bin/env python3

from icon_plugin_spec.plugin_spec import KomandPluginSpec
from icon_validator.exceptions import ValidationException

from .rules import VALIDATORS, JENKINS_VALIDATORS, WORKFLOW_VALIDATORS
from .styling import *
from .timing import *


def validate(directory, spec_file_name="plugin.spec.yaml", fail_fast=False, run_all=False, validators=list()):
    spec = KomandPluginSpec(directory, spec_file_name)
    status = 0  # Resultant return code
    start_time = time_now()
    print(f"{BULLET_OK} {BOLD}Running Integration Validators...{CEND}")

    if not validators:
        if spec_file_name == "plugin.spec.yaml":
            validators = VALIDATORS
            if run_all:
                validators += JENKINS_VALIDATORS
        elif spec_file_name == "workflow.spec.yaml":
            validators = WORKFLOW_VALIDATORS

    for v in validators:
        print(f"{BULLET_OK} Executing validator {v.name}")
        try:
            v.validate(spec)
            success = True

        except ValidationException as e:
            print(f"Validator {v.name} failed!")
            print(e)
            status = 1
            success = False

        if not success and fail_fast:
            break

    end_time = time_now()
    time_elapsed = format_time(start=start_time, end=end_time)

    extension = spec_file_name.split(".")[0].capitalize()

    if status == 0:
        print(f"{BULLET_OK} {BOLD}{extension} successfully validated!{CEND}")
    else:
        print(f"{BULLET_FAIL}{extension} failed validation!")

    print(f"\n----\n{BULLET_OK}{BOLD} Total time elapsed: {time_elapsed}ms{CEND}")
    return status
