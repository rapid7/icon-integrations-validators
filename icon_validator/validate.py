#! /usr/bin/env python3

import sys
import traceback

from icon_plugin_spec.plugin_spec import KomandPluginSpec
from icon_validator.exceptions import ValidationException

from .rules import VALIDATORS, JENKINS_VALIDATORS, WORKFLOW_VALIDATORS
from .styling import *
from .timing import *


class Validate:

    def __init__(self, validators=None, unit_test=False):
        if validators is None:
            validators = list()
        self.validators = validators
        self.unit_test = unit_test  # Used to stop some of the print outs during unit testing, to increase legibility

    def validate(self, directory, spec_file_name="plugin.spec.yaml", fail_fast=False, run_all=False):
        spec = KomandPluginSpec(directory, spec_file_name)
        status = 0  # Resultant return code
        start_time = time_now()
        print(f"{BULLET_OK} {BOLD}Running Integration Validators...{CEND}")

        if not self.validators:
            if spec_file_name == "plugin.spec.yaml":
                self.validators = VALIDATORS
                if run_all:
                    self.validators += JENKINS_VALIDATORS
            elif spec_file_name == "workflow.spec.yaml":
                self.validators = WORKFLOW_VALIDATORS

        for v in self.validators:
            print(f"{BULLET_OK} Executing validator {v.name}")
            try:
                v.validate(spec)
                success = True

            except ValidationException as e:
                if not self.unit_test:
                    print(f"Validator {v.name} failed!")
                    ex_type, ex, tb = sys.exc_info()
                    traceback.print_exception(Exception, e, tb)
                else:
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
