from icon_validator.rules.validator import KomandPluginValidator


class PasswordValidator(KomandPluginValidator):
    def validate(self, plugin_spec):
        connection = plugin_spec.spec_dictionary().get("connection")
        if connection is None:
            return
        else:
            for key in connection:
                for sub_key in connection[key]:
                    if sub_key == "type":
                        if connection[key][sub_key] == "password":
                            raise Exception("Remove credentials using type 'password' in plugin spec connection."
                                            " Use 'credentials' types instead.")
