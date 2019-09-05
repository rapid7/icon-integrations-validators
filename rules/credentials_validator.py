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
                        secret_key = data.get("body").get("connection").get("credentials").get("secretKey")
                        if secret_key is None:
                            continue
                        if secret_key != "":
                            violating_files.append(f"tests/{name}")
                    except AttributeError:
                        continue
        if len(violating_files) > 0:
            raise Exception(f"Remove credentials from the following files: {violating_files}")
