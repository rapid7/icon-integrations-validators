import sys
import traceback

from .plugin_spec import KomandPluginSpec
from .validation import VALIDATORS
from .timing import *

from . import OUTPUT

RED = '\033[31m'
YELLOW = '\033[33m'
BOLD = '\033[1m'
CEND = '\033[0m'


def validate(directory, spec_file_name='plugin.spec.yaml', fail_fast=False):
    spec = KomandPluginSpec(directory, spec_file_name)

    out = {
        'plugin': spec.spec_dictionary().get('name'),
        'validators': []
    }

    status = 0
    total_time_start = time_now()

    success = False

    print('[' + YELLOW + '*' + CEND + ']' + ' ' + BOLD + "Running CI Validators..." + CEND)

    for v in VALIDATORS:
        print('[' + YELLOW + '*' + CEND + ']' + " Executing validator %s" % v.name)
        try:
            start_time = time_now()
            v.validate(spec)
            success = True
        except Exception as e:
            print("Validator %s failed" % v.name)
            ex_type, ex, tb = sys.exc_info()
            traceback.print_exception(Exception, e, tb)
            status = 1
            success = False
        else:
            end_time = time_now()
            out['validators'].append({
                'name': v.name,
                'time_ms': format_time(start_time, end_time),
                'success': success
            })
        if not success and fail_fast:
            break

    if status == 0:
        print('[' + YELLOW + 'SUCCESS' + CEND + ']' + " Plugin successfully validated")
    else:
        print('[' + RED + 'FAIL' + CEND + ']' + " Plugin did not pass validation")

    total_time_end = time_now()
    out['time_ms'] = format_time(total_time_start, total_time_end)

    OUTPUT.add_result('validate', out)

    return status
