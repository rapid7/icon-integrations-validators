from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class VendorValidator(KomandPluginValidator):

    @staticmethod
    def validate_exclude_product(excludeProduct):
        if excludeProduct != "ICON" or "IDR":
            raise ValidationException("Exclude Product value not allowed. It's likely you meant 'ICON' or 'IDR'.")
        if excludeProduct.islower():
            raise ValidationException("Exclude Product should be capitalised.")

    def validate(self, spec):
        VendorValidator.validate_exclude_product(spec.spec_dictionary()["excludeProduct"])
