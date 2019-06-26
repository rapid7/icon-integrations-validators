import sys
from .validate import validate
from .styling import *



def main():
    args = sys.argv

    if not len(args) == 2:
        print(f"{BULLET_FAIL} Error parsing arguments! Example usage: icon-validate my_plugin/")
        exit(1)

    print(f"{BULLET_OK} Validating plugin at {args[1]}\n")
    validate(directory=args[1])


if __name__ == '__main__':
    main()
