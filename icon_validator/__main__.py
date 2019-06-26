import sys
from .validate import validate


def main():
    args = sys.argv

    if not len(args) >= 2:
        print("Invalid call")
        exit(0)

    print(f"Validating plugin at {args[1]}")
    validate(directory=args[1])


if __name__ == '__main__':
    main()
