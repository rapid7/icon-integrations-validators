from icon_validator.exceptions import ValidationException
from icon_validator.rules.validator import KomandPluginValidator

import re
import os


class CloudReadyValidator(KomandPluginValidator):

    @staticmethod
    def validate_enable_cache_in_plugin_spec(plugin_spec: dict):
        if plugin_spec.get("enable_cache", False):
            raise ValidationException(
                "'enable_cache' must set to 'false' for a plugin to be Cloud Ready."
                "Please check this field in plugin.spec and try again."
            )

    @staticmethod
    def validate_python_version_in_dockerfile(dockerfile: str):
        docker_str = dockerfile.replace(" --platform=linux/amd64 ", " ")  # if user has specified '--platform' remove
        if not re.compile(r"FROM rapid7/insightconnect-python-3(-slim)?-plugin:(([0-9][0-9]+)|[4-9]|latest)")\
                .match(docker_str):
            raise ValidationException(
                "The python runtime must be in 5+ version to be Cloud Ready."
                "Update Dockerfile and try again."
            )

    @staticmethod
    def validate_user_set_to_nobody_in_dockerfile(dockerfile: str):
        if "USER nobody" not in dockerfile:
            raise ValidationException(
                "Plugin 'USER' must be set to 'nobody' in Dockerfile to be Cloud Ready."
                "Please check this field and try again."
            )

    @staticmethod
    def validate_dependencies_in_dockerfile(dockerfile: str):
        if "apt" in dockerfile or "apk" in dockerfile or "dpkg" in dockerfile:
            raise ValidationException(
                "Cloud Ready plugin can't have container/OS level dependencies (eg apt or apk installs). "
                "Please check this in Dockerfile and try again."
            )

    @staticmethod
    def check_command_execution_exists(searched_file: str) -> bool:
        system_level_commands = [
            r".*os.system\s*\(",
            r".*exec\s*\(",
            r".*subprocess.run"
        ]

        for one_command in system_level_commands:
            if re.match(one_command, searched_file, re.DOTALL):
                return True

        return False

    @staticmethod
    def validate_system_level_command_in_plugin(directory_path: str):
        for root, dirs, filenames in os.walk(directory_path):
            for filename in filenames:
                if not filename.endswith(".py"):
                    continue

                relative_directory_name = root.replace(directory_path, "")
                try:
                    with open(os.path.join(root, filename), "r") as file_content:
                        if CloudReadyValidator.check_command_execution_exists(file_content.read()):
                            raise ValidationException(
                                f"In file {os.path.join(relative_directory_name, filename)} "
                                "system level command line utilities was found. "
                                "A Cloud Ready plugin cannot have any calls to system-level command-line utilities. "
                                "Please check this file and try again."
                            )
                except FileNotFoundError:
                    raise ValidationException(
                        f"{os.path.join(relative_directory_name, filename)} file could not be opened. "
                        "Check this file and be sure to include this file in your plugin directory."
                    )

    def validate(self, spec):
        try:
            with open(f"{spec.directory}/Dockerfile", "r") as docker_file:
                dockerfile: str = docker_file.read()
        except FileNotFoundError:
            raise ValidationException(
                "Dockerfile not found. Please be sure to include this file in your plugin directory."
            )

        plugin_spec = spec.spec_dictionary()
        if plugin_spec.get("cloud_ready", False):
            CloudReadyValidator.validate_system_level_command_in_plugin(spec.directory)
            CloudReadyValidator.validate_enable_cache_in_plugin_spec(plugin_spec)
            CloudReadyValidator.validate_python_version_in_dockerfile(dockerfile)
            CloudReadyValidator.validate_user_set_to_nobody_in_dockerfile(dockerfile)
            CloudReadyValidator.validate_dependencies_in_dockerfile(dockerfile)
