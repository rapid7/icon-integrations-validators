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

                if 'install_requires=["insightconnect-plugin-runtime"]' not in setup_str\
                        and "install_requires=['insightconnect-plugin-runtime']" not in setup_str:
                    raise ValidationException("Komand is no longer used for install_requires in setup.py. "
                                              "Use insightconnect-plugin-runtime instead.")

    @staticmethod
    def validate_imports(spec):
        for root, dirs, files in os.walk(spec.directory):
            for file in files:
                if file.endswith(".py"):
                    with open(os.path.join(root, file), "r") as open_file:
                        file_str = open_file.read()

                        if "import komand\n" in file_str or "from komand " in file_str or "from komand." in file_str:
                            raise ValidationException(f"Komand import found in {str(os.path.join(root, file))}. "
                                                      "Komand is no longer used here. "
                                                      "Use insightconnect-plugin-runtime instead.")

    @staticmethod
    def validate_caching(spec):
        if spec.spec_dictionary().get("cloud_ready") is True:
            paths = []
            actions_path = glob.glob(f"{spec.directory}/*/actions")
            paths.append(actions_path[0])
            tasks_path = glob.glob(f"{spec.directory}/*/tasks")
            # It is possible for existing plugins to not have /tasks directory, It will be when code
            # needs not to be regenerated(e.g. update action/triggers run() method) using icon-plugin-tool.
            if tasks_path:
                paths.append(tasks_path[0])
            for path in paths:
                for root, dirs, files in os.walk(path):
                    for file in files:
                        with open(os.path.join(root, file), 'r') as open_file:
                            file_str = open_file.read().replace("\n", "")

                            if "cache" in file_str:
                                raise ValidationException(f"Cloud ready plugins cannot contain caching. "
                                                          f"Update {str(os.path.join(root, file))}.")

    @staticmethod
    def validate_dockerfile(spec, latest_images):
        if "setup.py" in os.listdir(spec.directory):
            with open(f"{spec.directory}/setup.py", "r") as setup_file:
                setup_str = setup_file.read().replace("\n", "")

                if "insightconnect-plugin-runtime" in setup_str:
                    with open(f"{spec.directory}/Dockerfile", "r") as docker_file:
                        docker_str = docker_file.read().replace("\n", "")

                        if not any(image in docker_str for image in latest_images):
                            raise ValidationException("insightconnect-plugin-runtime is being used in setup.py. "
                                                      "Update Dockerfile accordingly to use latest base image.")

    def validate(self, spec):
        latest_images = ["rapid7/insightconnect-python-3-38-plugin",
                         "rapid7/insightconnect-python-3-38-slim-plugin"]
        RuntimeValidator.validate_dockerfile(spec, latest_images)

        with open(f"{spec.directory}/Dockerfile", "r") as file:
            docker_str = file.read().replace("\n", "")

            if any(image in docker_str for image in latest_images):
                RuntimeValidator.validate_setup(spec)
                RuntimeValidator.validate_imports(spec)
                RuntimeValidator.validate_caching(spec)
