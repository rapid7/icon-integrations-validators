from icon_validator.exceptions import ValidationException
from icon_validator.rules.validator import KomandPluginValidator


class CloudReadyConnectionCredentialTokenValidator(KomandPluginValidator):
    def validate(self, plugin_spec):
        cloud_ready = plugin_spec.spec_dictionary().get("cloud_ready")
        connection = plugin_spec.spec_dictionary().get("connection")
        if cloud_ready and connection:
            for key in connection:
                if connection[key].get("type") == "credential_token":
                    raise ValidationException("Cloud plugin connection does not support credential_token yet.")




