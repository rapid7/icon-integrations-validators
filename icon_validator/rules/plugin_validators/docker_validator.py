import os
import subprocess

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class DockerValidator(KomandPluginValidator):

    # Substrings that indicate a build failed because a dependency could not be
    # downloaded (e.g. an artifactory/registry lookup). These are environment
    # specific and should not fail validation.
    NETWORK_ERROR_MARKERS = [
        "artifactory",
        "could not resolve",
        "connection refused",
        "connection timed out",
        "temporary failure in name resolution",
        "network is unreachable",
        "failed to fetch",
        "timeout",
    ]

    def validate(self, spec):
        # Using subprocess so we don't have to deal with connecting to different Docker environments
        # e.g docker-machine vs Docker for Mac vs native Docker
        # Directory of current plugin
        d = spec.directory
        build_image = ["docker", "build", "-q", "--pull", "-t", "docker_validator", d]
        run_image = ["docker", "run", "--rm", "-t", "docker_validator", "info"]

        with open(os.devnull, "w") as fd:
            try:
                subprocess.check_call(["which", "docker"], stdout=fd, stderr=fd)
            except subprocess.CalledProcessError:
                print("DockerValidator: docker binary missing in PATH, skipping...")
                return

            # Build the image capturing stderr so a failure can be inspected
            build = subprocess.run(build_image, stdout=fd, stderr=subprocess.PIPE, text=True)
            if build.returncode != 0:
                # Extract the error message from process
                error_message = (build.stderr or "").strip()

                # A build that fails because a dependency could not be downloaded
                # can be related to no access to artifactory, so skip rather than fail the plugin
                if any(marker in error_message.lower() for marker in DockerValidator.NETWORK_ERROR_MARKERS):
                    print("DockerValidator: Docker build could not download a dependency "
                          "(environment-specific network issue), skipping...")
                    return

                # Otherwise, in case build fails with any other error, fail the plugin
                raise ValidationException("The plugin is either broken or the image might not be built. "
                                          "Please try 'make image' to rebuild the image. "
                                          "'insight-plugin shell' will open a bash shell on the build container. "
                                          f"Error:\n{error_message}")

            # Run the image to check it properly starts
            # In case of any error, raise validation exception
            try:
                subprocess.check_call(run_image, stdout=fd, stderr=fd)
            except subprocess.CalledProcessError as error:
                raise ValidationException("Docker failed at running info command. "
                                          f"Error:\n{error}")
