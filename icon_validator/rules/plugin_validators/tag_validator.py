from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class TagValidator(KomandPluginValidator):
    def validate(self, spec):
        tags = spec.spec_dictionary().get("tags")
        if not tags:
            raise ValidationException("Field 'tags' not found.")
        if not isinstance(tags, list):
            raise ValidationException("Field 'tags' is not a list.")
        if len(tags) < 2:
            raise ValidationException("Not enough tags. Each plugin should have at least 2 tags.")
        i = 0
        for tag in tags:
            if not isinstance(tag, str):
                raise ValidationException("Tag at index %d is not a string. All tags must be strings.", i)
            i = i + 1
