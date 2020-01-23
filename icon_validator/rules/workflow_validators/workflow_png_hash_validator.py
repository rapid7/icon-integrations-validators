from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException
from hashlib import sha256


class WorkflowPNGHashValidator(KomandPluginValidator):

    _GOOD_HASH = "88d5ed1b033ce1a92dfcfc7607e930ce1ddd1f0344dee86a44dd92a991efca36"

    def validate_hash(self, spec):

        d = spec.directory
        hasher = sha256()
        with open(f"{d}/extension.png", "rb") as file:
            temp = file.read()
            hasher.update(temp)
        hash_ = hasher.hexdigest()
        if not hash_ == self._GOOD_HASH:
            raise ValidationException(f"The extention.png file in the workflow directory is incorrect."
                                      f" The File should have a SHA2 hash of"
                                      f" 88d5ed1b033ce1a92dfcfc7607e930ce1ddd1f0344dee86a44dd92a991efca36."
                                      f" The files hash was {hash_}")
