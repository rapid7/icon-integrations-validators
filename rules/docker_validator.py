from .validator import KomandPluginValidator
import subprocess
import os
import sys


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
                which = subprocess.check_call(['which', 'docker'], stdout=fd, stderr=fd)
            except subprocess.CalledProcessError as e:
                sys.stdout.write('DockerValidator: docker binary missing in PATH, skipping...')
            else:
                try:
                    subprocess.check_call(build_image, stdout=fd, stderr=fd)
                except subprocess.CalledProcessError as e:
                    raise Exception('Docker image did not build successfully.') from e

                try:
                    subprocess.check_call(run_image, stdout=fd, stderr=fd)
                except subprocess.CalledProcessError as e:
                    raise Exception('Docker failed at running info command. '
                                    'Check your plugin code for run-time errors.') from e
