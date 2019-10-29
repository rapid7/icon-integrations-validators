import sys
import logging
from .validate import validate
from .styling import *


def main():
    args = sys.argv

    if len(args) == 3:
        if args[2] != "--all" and args[2] != "-a":
            logging.error(f"{BULLET_FAIL} Error parsing arguments! Example usage: icon-validate my_plugin/ --all")
            exit(1)
        print(f"{BULLET_OK} Validating plugin with all validators at {args[1]}\n")
        validate(directory=args[1], run_all=True)
    elif not len(args) == 2:
        logging.error(f"{BULLET_FAIL} Error parsing arguments! Example usage: icon-validate my_plugin/")
        exit(1)

    print(f"{BULLET_OK} Validating plugin at {args[1]}\n")
    validate(directory=args[1])


if __name__ == '__main__':
    main()
