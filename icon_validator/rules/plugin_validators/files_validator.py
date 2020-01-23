import os

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class FilesValidator(KomandPluginValidator):

    def validate(self, spec):
        d = spec.directory

        # Go plugins
        if os.path.isdir(f"{d}/connection"):
            if not os.path.isfile(f"{d}/Makefile"):
                raise ValidationException("File Makefile does not exist in: ", d)
            if not os.path.isfile(f"{d}/plugin.spec.yaml"):
                raise ValidationException("File plugin.spec.yaml does not exist in: ", d)
            if not os.path.isfile(f"{d}/Dockerfile"):
                raise ValidationException("File Dockerfile does not exist in: ", d)
        else:
            # Python plugins
            if os.path.isdir(f"{d}/bin"):
                if not os.path.isfile(f"{d}/Dockerfile"):
                    raise ValidationException("File Dockerfile does not exist in: ", d)
                if not os.path.isfile(f"{d}/Makefile"):
                    raise ValidationException("File Makefile does not exist in: ", d)
                if not os.path.isfile(f"{d}/plugin.spec.yaml"):
                    raise ValidationException("File plugin.spec.yaml does not exist in: ", d)
                if not os.path.isfile(f"{d}/setup.py"):
                    raise ValidationException("File setup.py does not exist in: ", d)
                if not os.path.isfile(f"{d}/requirements.txt"):
                    raise ValidationException("File requirements.txt does not exist in: ", d)
