import argparse
import os
import sys

from pkg_resources import get_distribution

from icon_validator.styling import *
from icon_validator.validate import validate


def main():
    version_string = (f"{BULLET_OK} " + str(get_distribution("insightconnect-integrations-validators")))
    if "--version" in sys.argv:
        print(version_string)
        sys.exit(0)

    arguments_parser = argparse.ArgumentParser(epilog=version_string,
                                               description="Linting rules for plugins and workflows")
    # required
    arguments_parser.add_argument("path", help="Path to find the plugin or workflow code", default=".")

    # optional
    arguments_parser.add_argument("--all", help="Run all Validators", default=False,
                                  dest="run_all_validators", action="store_true")
    arguments_parser.add_argument("-a", help="Run all validators", default=False,
                                  dest="run_all_validators", action="store_true")

    the_arguments = arguments_parser.parse_args()

    # this is a required field, and argparse enforces it, so we are 100% sure this key exists:
    path = the_arguments.path

    if os.path.exists(path + "/workflow.spec.yaml"):
        spec_file_name = "workflow.spec.yaml"
        if the_arguments.run_all_validators:
            sys.stderr.write(
                f"{BULLET_OK}Option '--all' and '-a' only works with plugins. Executing workflow supported validators\n")
    else:
        spec_file_name = "plugin.spec.yaml"

    if not os.path.exists(path):
        sys.stderr.write(f"{BULLET_FAIL} Path '{path}' does not exist\n")
        sys.exit(1)

    extension = spec_file_name.split(".")[0]

    if extension == "plugin" and the_arguments.run_all_validators:
        print(f"{BULLET_OK} Validating {extension} with all validators at {path}\n")
        validate(directory=path, run_all=True)
    else:
        print(f"{BULLET_OK} Validating {extension} at {path}\n")
        validate(directory=path, spec_file_name=spec_file_name)


if __name__ == "__main__":
    main()
