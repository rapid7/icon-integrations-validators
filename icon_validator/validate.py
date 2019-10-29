#! /usr/bin/env python3

import sys
import traceback

from icon_plugin_spec.plugin_spec import KomandPluginSpec
from .rules import VALIDATORS, JENKINS_VALIDATORS
from .timing import *
from .styling import *


def validate(directory, spec_file_name='plugin.spec.yaml', fail_fast=False, run_all=False):
    spec = KomandPluginSpec(directory, spec_file_name)
    status = 0  # Resultant return code

    start_time = time_now()
    print(f"{BULLET_OK} {BOLD}Running Integration Validators...{CEND}")

    validators = VALIDATORS
    if run_all:
        validators += JENKINS_VALIDATORS

    for v in validators:
        print(f"{BULLET_OK} Executing validator {v.name}")
        try:
            v.validate(spec)
            success = True

        except Exception as e:
            print(f"Validator {v.name} failed!")
            ex_type, ex, tb = sys.exc_info()
            traceback.print_exception(Exception, e, tb)
            status = 1
            success = False

        if not success and fail_fast:
            break

    end_time = time_now()
    time_elapsed = format_time(start=start_time, end=end_time)

    if status == 0:
        print(f"{BULLET_OK} {BOLD}Plugin successfully validated!{CEND}")
    else:
        print(f"{BULLET_FAIL} Plugin failed validation!")

    print(f"\n----\n{BULLET_OK}{BOLD} Total time elapsed: {time_elapsed}ms{CEND}")
    return status
