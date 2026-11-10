from icon_plugin_spec.plugin_spec import KomandPluginSpec

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class SnippetExtensionValidator(KomandPluginValidator):

    @staticmethod
    def validate_extension(extension: str) -> None:
        """
        Checks that the extension key in .yaml has a value of snippet
        """
        if not extension == "snippet":
            raise ValidationException("Extension key must have a value of snippet.")

    @staticmethod
    def validate_extension_exists(spec: KomandPluginSpec) -> None:
        """
        Checks that the extension key in .yaml exists.
        """
        if "extension" not in spec.spec_dictionary():
            raise ValidationException("Snippet extension key is missing.")

    @staticmethod
    def validate_products(spec: KomandPluginSpec) -> None:
        """
        Checks that the products key in .yaml is a list that includes insightconnect,
        the product a snippet is imported into
        """
        products = spec.spec_dictionary().get("products")
        if not isinstance(products, list) or "insightconnect" not in products:
            raise ValidationException("Products key must be a list that includes insightconnect.")

    def validate(self, spec: KomandPluginSpec) -> None:
        SnippetExtensionValidator.validate_extension_exists(spec)
        SnippetExtensionValidator.validate_extension(spec.spec_dictionary()["extension"])
        SnippetExtensionValidator.validate_products(spec)
