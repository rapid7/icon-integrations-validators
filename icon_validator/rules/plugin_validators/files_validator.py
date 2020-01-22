import os

from icon_validator.rules.validator import KomandPluginValidator


class FilesValidator(KomandPluginValidator):

    def validate(self, spec):
        d = spec.directory

        # Go plugins
        if os.path.isdir("{}/{}".format(d, "connection")):
            if not os.path.isfile("{}/{}".format(d, "Makefile")):
                raise Exception("File Makefile does not exist in: ", d)
            if not os.path.isfile("{}/{}".format(d, "plugin.spec.yaml")):
                raise Exception("File plugin.spec.yaml does not exist in: ", d)
            if not os.path.isfile("{}/{}".format(d, "Dockerfile")):
                raise Exception("File Dockerfile does not exist in: ", d)
        else:
            # Python plugins
            if os.path.isdir("{}/{}".format(d, "bin")):
                if not os.path.isfile("{}/{}".format(d, "Dockerfile")):
                    raise Exception("File Dockerfile does not exist in: ", d)
                if not os.path.isfile("{}/{}".format(d, "Makefile")):
                    raise Exception("File Makefile does not exist in: ", d)
                if not os.path.isfile("{}/{}".format(d, "plugin.spec.yaml")):
                    raise Exception("File plugin.spec.yaml does not exist in: ", d)
                if not os.path.isfile("{}/{}".format(d, "setup.py")):
                    raise Exception("File setup.py does not exist in: ", d)
                if not os.path.isfile("{}/{}".format(d, "requirements.txt")):
                    raise Exception("File requirements.txt does not exist in: ", d)
