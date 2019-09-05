from .validator import KomandPluginValidator
import os
import json


class CredentialsValidator(KomandPluginValidator):
    def validate(self, spec):
        tests_dir = os.path.join(spec.directory, "tests")
        violating_files = []
        for path, _, files in os.walk(tests_dir):
            for name in list(filter(lambda x: x.endswith(".json"), files)):
                with open(os.path.join(tests_dir, name)) as test:
                    data = json.load(test)
                    try:
                        creds = data.get("body").get("connection").get("credentials")
                        if creds is None:
                            continue
                        else:
                            for key in creds:
                                if creds[key] != "":
                                    violating_files.append(f"tests/{name}")
                                    continue
                    except AttributeError:
                        continue
        if len(violating_files) > 0:
            raise Exception(f"Remove credentials from the following files: {violating_files}")
