from .validator import KomandPluginValidator
from icon_plugin_spec.plugin_spec import KomandPluginSpec


class RequiredKeysValidator(KomandPluginValidator):

    missing_key_message = {
        'plugin_spec_version': 'Specifies the version of the spec. Current version is v1',
        'name': 'Name of the plugin, refers to the docker image name. Should be lower case',
        'title': 'Formatted name',
        'description': 'One sentence description',
        'version': 'Semantic version of the plugin',
        'vendor': 'Plugin vendor, refers to the docker image repository and komand marketplace user',
        'status': 'List of development statuses to apply to the plugin',
        'tags': 'List of tags to apply to the plugin',
    }

    @staticmethod
    def validate_support(spec_dict: dict):
        accepted_values = ["rapid7", "community", "partner"]
        if "support" not in spec_dict or spec_dict["support"] not in accepted_values:
            RequiredKeysValidator.raise_exception("support",
                                                  "Supporter of plugin. Either 'rapid7', 'community', or 'partner'",)

    @staticmethod
    def validate_resources(spec_dict: dict):
        if "resources" not in spec_dict or "source_url" not in spec_dict["resources"]\
                or "license_url" not in spec_dict["resources"] or "vendor_url" not in spec_dict["resources"]:
            RequiredKeysValidator.raise_exception(
                "resources", "Must have sub-keys 'source_url', 'license_url', and 'vendor_url'. "
                             "A URL must be provided for 'vendor_url'")

    @staticmethod
    def validate_extension(spec_dict: dict):
        if "extension" not in spec_dict or spec_dict["extension"] != "plugin":
            RequiredKeysValidator.raise_exception("extension", "extension should always be 'plugin'")

    @staticmethod
    def validate_product(spec_dict: dict):
        if "product" not in spec_dict or "insightconnect" not in spec_dict["product"]:
            RequiredKeysValidator.raise_exception(
                "product", "List of products the plugin is applicable to. Should always include 'insightconnect'")

    @staticmethod
    def validate_hub_tags(spec_dict: dict):
        if "hub_tags" in spec_dict:
            sub_keys = ["use_cases", "keywords", "features"]
            for key in sub_keys:
                if key not in spec_dict["hub_tags"]:
                    RequiredKeysValidator.raise_exception(
                        "hub_tags", "Must have sub-keys 'use_cases', 'keywords', and 'features'")
        else:
            RequiredKeysValidator.raise_exception(
                "hub_tags", "Key value mapping containing use cases, keywords, and features")

    @staticmethod
    def raise_exception(key: str, msg: str):
        raise Exception(f"Plugin spec has missing or invalid value for key '{key}': {msg}")

    def validate(self, spec: KomandPluginSpec):
        for required_key, message in self.missing_key_message.items():
            if required_key not in spec.spec_dictionary():
                RequiredKeysValidator.raise_exception(required_key, message)
        RequiredKeysValidator.validate_support(spec.spec_dictionary())
        RequiredKeysValidator.validate_resources(spec.spec_dictionary())
        RequiredKeysValidator.validate_extension(spec.spec_dictionary())
        RequiredKeysValidator.validate_product(spec.spec_dictionary())
        RequiredKeysValidator.validate_hub_tags(spec.spec_dictionary())
