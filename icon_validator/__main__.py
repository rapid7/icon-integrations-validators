import sys
import argparse
import re
import os
from pkg_resources import get_distribution
from .validate import validate
from .styling import *


def main():
    version_string = (f"{BULLET_OK} " + str(get_distribution('insightconnect-integrations-validators')))
    if '--version' in sys.argv:
        print(version_string)
        sys.exit(0)

    arguments_parser = argparse.ArgumentParser(epilog=version_string,
                                               description='Validate plugin code is ready for publishing to Rapid7 Hub')
    # required
    arguments_parser.add_argument('path', help='Path to find the plugin code', default='.')

    # optional
    arguments_parser.add_argument('--all', help='Run the Jenkins Validators as well', default=False,
                                  dest='run_all_validators', action='store_true')
    arguments_parser.add_argument('-a', help='Run the Jenkins Validators as well', default=False,
                                  dest='run_all_validators', action='store_true')

    the_arguments = arguments_parser.parse_args()

    # this is a required field, and argparse enforces it, so we are 100% sure this key exists:
    path = the_arguments.path
    if not os.path.exists(path):
        sys.stderr.write(f"{BULLET_FAIL} Path '{path}' does not exist\n")
        sys.exit(1)

    if the_arguments.run_all_validators:
        print(f"{BULLET_OK} Validating plugin with all validators at {path}\n")
        validate(directory=path, run_all=True)
    else:
        print(f"{BULLET_OK} Validating plugin at {path}\n")
        validate(directory=path)


if __name__ == '__main__':
    main()
