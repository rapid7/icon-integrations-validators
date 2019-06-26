#! /usr/bin/env python3

import sys
import traceback

from icon_plugin_spec.plugin_spec import KomandPluginSpec
from rules import VALIDATORS
from .timing import *

RED = '\033[31m'
YELLOW = '\033[33m'
BOLD = '\033[1m'
CEND = '\033[0m'

BULLET_OK = f"[{YELLOW}*{CEND}]"
BULLET_FAIL = f"[{RED}*{CEND}]"


def validate(directory, spec_file_name='plugin.spec.yaml', fail_fast=False):
    spec = KomandPluginSpec(directory, spec_file_name)
    status = 0  # Resultant return code

    start_time = time_now()
    print(f"{BULLET_OK} {BOLD}Running Integration Validators...{CEND}")

    for v in VALIDATORS:
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
        print(f"{BULLET_OK} Plugin successfully validated!")
    else:
        print(f"{BULLET_FAIL} Plugin failed validation!")

    print(f"{BULLET_OK} Total time elapsed: {time_elapsed}ms")
    return status


if __name__ == '__main__':
    args = sys.argv

    if not len(args) >= 2:
        print("Invalid call")
        exit(0)

    print(f"Validating plugin at {args[1]}")
    validate(directory=args[1])


