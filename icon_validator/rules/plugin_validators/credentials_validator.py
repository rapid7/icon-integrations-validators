import json
import os

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class CredentialsValidator(KomandPluginValidator):
    def validate(self, spec):
        tests_dir = os.path.join(spec.directory, "tests")
        violating_files = []
        for path, _, files in os.walk(tests_dir):
            for name in list(filter(lambda x: x.endswith(".json"), files)):
                with open(os.path.join(tests_dir, name)) as test:
                    data = json.load(test)
                    added = False
                    try:
                        creds = data.get("body").get("connection").get("credentials")
                        if creds is not None:
                            for key in creds:
                                if creds[key] != "":
                                    violating_files.append(f"tests/{name}")
                                    added = True
                                    break
                    except AttributeError:
                        pass

                    if added:
                        continue

                    try:
                        creds = data.get("body").get("connection").get("username_password")
                        if creds is not None:
                            for key in creds:
                                if creds[key] != "":
                                    violating_files.append(f"tests/{name}")
                                    break
                    except AttributeError:
                        pass
        if len(violating_files) > 0:
            raise ValidationException(f"Remove credentials from the following files: {violating_files}.")
