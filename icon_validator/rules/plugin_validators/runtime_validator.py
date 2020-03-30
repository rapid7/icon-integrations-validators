import os
import glob

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class RuntimeValidator(KomandPluginValidator):

    @staticmethod
    def validate_setup(spec):
        if "setup.py" in os.listdir(spec.directory):
            with open(f"{spec.directory}/setup.py", "r") as file:
                setup_str = file.read().replace("\n", "")

                if "komand" in setup_str and "insightconnect-plugin-runtime" not in setup_str:
                    raise ValidationException("Komand is no longer used in setup.py. "
                                              "Use insightconnect-plugin-runtime instead.")

    @staticmethod
    def validate_icon(spec):
        for root, dirs, files in os.walk(spec.directory):
            for file in files:
                if file.endswith(".py"):
                    with open(os.path.join(root, file), "r") as open_file:
                        file_str = open_file.read().replace("\n", "")

                        if "import komand" in file_str or "FROM komand" in file_str:
                            raise ValidationException(f"Komand import found in {str(os.path.join(root, file))}. "
                                                      "Komand is no longer used here. "
                                                      "Use insightconnect-plugin-runtime instead.")

    @staticmethod
    def validate_caching(spec):
        if spec.spec_dictionary().get("cloud_ready") is True:
            actions_path = glob.glob(f"{spec.directory}/*/actions")
            for root, dirs, files in os.walk(actions_path[0]):
                for file in files:
                    print("file = " + file)
                    with open(os.path.join(root, file), 'r') as open_file:
                        file_str = open_file.read().replace("\n", "")

                        if "cache" in file_str:
                            raise ValidationException(f"Cloud ready plugins cannot contain caching. "
                                                      f"Update {str(os.path.join(root, file))}.")

    def validate(self, spec):
        latest_images = ["rapid7/insightconnect-python-3-38-plugin",
                         "rapid7/insightconnect-python-3-38-slim-plugin"]

        with open(f"{spec.directory}/Dockerfile", "r") as file:
            docker_str = file.read().replace("\n", "")

            if any(image in docker_str for image in latest_images):
                RuntimeValidator.validate_setup(spec)
                RuntimeValidator.validate_icon(spec)
                RuntimeValidator.validate_caching(spec)
