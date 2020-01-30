import os
import subprocess
import sys

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class DockerValidator(KomandPluginValidator):
    def validate(self, spec):
        # Using subprocess so we don't have to deal with connecting to different Docker environments
        # e.g docker-machine vs Docker for Mac vs native Docker
        # Directory of current plugin
        d = spec.directory
        build_image = ["docker", "build", "-q", "--pull", "-t", "docker_validator", d]
        run_image = ["docker", "run", "--rm", "-t", "docker_validator", "info"]

        with open(os.devnull, "w") as fd:
            try:
                which = subprocess.check_call(["which", "docker"], stdout=fd, stderr=fd)
            except subprocess.CalledProcessError:
                sys.stdout.write("DockerValidator: docker binary missing in PATH, skipping...")
            else:
                try:
                    subprocess.check_call(build_image, stdout=fd, stderr=fd)
                except subprocess.CalledProcessError as e:
                    raise ValidationException("The plugin is either broken or the image might not be built."
                                              "Please try 'icon-plugin build image' to rebuild the image."
                                              "'icon-plugin run -c bash' will open a bash shell on the build container.") from e

                try:
                    subprocess.check_call(run_image, stdout=fd, stderr=fd)
                except subprocess.CalledProcessError as e:
                    raise ValidationException("Docker failed at running info command. "
                                              "Check your plugin code for run-time errors.") from e
