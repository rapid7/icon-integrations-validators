from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class VendorValidator(KomandPluginValidator):

    @staticmethod
    def validate_vendor(vendor):
        lvendor = vendor.lower()
        if lvendor == "komand":
            raise ValidationException("Vendor 'komand' not allowed. It's likely you meant 'rapid7'.")
        if vendor.endswith("."):
            raise ValidationException("Vendor ends with period when it should not.")
        if not vendor[0].islower():
            raise ValidationException("Vendor starts with a capital letter when it should not.")
        if " " in vendor:
            raise ValidationException("Vendor should be separated by underscores, not spaces.")

    @staticmethod
    def validate_vendor_quotes(spec):
        """Requires raw spec to see the quotes"""
        for line in spec.splitlines():
            if line.startswith("vendor:"):
                val = line[line.find(" ") + 1:]
                if "'" in val or '"' in val:
                    raise ValidationException("Vendor is surrounded by or contains quotes when it should not.")

    @staticmethod
    def validate_plugin_vendor(spec):
        if "vendor" not in spec.spec_dictionary():
            raise ValidationException("Plugin vendor is missing.")
        if not isinstance(spec.spec_dictionary()["vendor"], str):
            raise ValidationException("Plugin vendor does not contain a string.")

    def validate(self, spec):
        VendorValidator.validate_plugin_vendor(spec)
        VendorValidator.validate_vendor(spec.spec_dictionary()["vendor"])
        VendorValidator.validate_vendor_quotes(spec.raw_spec())
