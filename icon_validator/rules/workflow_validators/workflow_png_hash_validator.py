from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException
from hashlib import sha256


class WorkflowPNGHashValidator(KomandPluginValidator):

    _GOOD_HASH = "02094da9b8d40d9411eb10f45cb1cd1627d24bd7006bc105375b00a97ea66d3e"

    def validate(self, spec):
        """
        Check that the extension.png file is the correct file
        """
        d = spec.directory
        hasher = sha256()
        with open(f"{d}/extension.png", "rb") as file:
            temp = file.read()
            hasher.update(temp)
        hash_ = hasher.hexdigest()
        if not hash_ == self._GOOD_HASH:
            raise ValidationException("The extention.png file in the workflow directory is incorrect."
                                      " The File should have a SHA2 hash of"
                                      f" {self._GOOD_HASH}."
                                      f" The files hash was {hash_}")
