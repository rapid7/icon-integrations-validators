from icon_validator.exceptions import ValidationException
from icon_validator.rules.validator import KomandPluginValidator


class EnableCacheValidator(KomandPluginValidator):
    # Triggers rely on caching on SDK 6.6.0+, so any plugin defining triggers must set
    # enable_cache: true. This applies to all plugins, hence it is separate from the
    # Cloud Ready, Dockerfile-dependent checks in CloudReadyValidator.

    @staticmethod
    def validate_enable_cache_with_triggers(plugin_spec: dict):
        has_triggers = bool(plugin_spec.get("triggers"))
        # strict: reject truthy strings like "false"
        enable_cache = plugin_spec.get("enable_cache") is True

        if has_triggers and not enable_cache:
            raise ValidationException(
                "'enable_cache' must be set to 'true' for a plugin with triggers. "
                "Please check this field in plugin.spec and try again."
            )

    def validate(self, spec):
        EnableCacheValidator.validate_enable_cache_with_triggers(spec.spec_dictionary())
