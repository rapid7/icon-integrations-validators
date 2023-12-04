from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class DockerfileParentValidator(KomandPluginValidator):
    def validate(self, spec):
        spec_str = "".join(spec.raw_dockerfile())

        valid_images = [
            "komand/go-plugin-2", "komand/python-3-plugin", "komand/python-pypy3-plugin",
            "komand/python-3-slim-plugin",
            "komand/python-3-37-slim-plugin",
            "komand/python-3-37-plugin",
            "komand/python-pypy3-full-plugin",
            "rapid7/insightconnect-python-3-38-plugin", "rapid7/insightconnect-python-3-38-slim-plugin",
            "rapid7/insightconnect-python-3-plugin", "rapid7/insightconnect-python-3-slim-plugin"
        ]
        root_spec_found = False
        for line in spec.raw_dockerfile():
            if line.startswith("FROM"):
                parent = line.replace("FROM", "").replace("--platform=linux/amd64", "").strip()
                parts = parent.split(":")
                image = parts[0].strip()
                if image == "komand/python-plugin":
                    raise ValidationException("Parent Dockerfile komand/python-plugin is no longer supported. "
                                              "Use komand/python-2-plugin, komand/python-3-plugin, or komand/python-pypy3-plugin instead.")
                elif image == "komand/go-plugin":
                    raise ValidationException("Parent Dockerfile komand/go-plugin is no longer supported. "
                                              "Use komand/go-plugin-2 instead.")
                elif image not in valid_images:
                    raise ValidationException("Unrecognized parent Dockerfile.")
            if line.startswith("ADD ./plugin.spec.yaml /plugin.spec.yaml"):
                root_spec_found = True

        # Komand code checks for /plugin.spec.yaml in the plugin container
        if not root_spec_found:
            raise ValidationException("Dockerfile missing line: ADD ./plugin.spec.yaml /plugin.spec.yaml")
