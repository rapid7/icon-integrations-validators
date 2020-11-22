from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException
from icon_plugin_spec.plugin_spec import KomandPluginSpec


class ExampleInputValidator(KomandPluginValidator):
    def validate(self, spec: KomandPluginSpec):
        plugin_spec = spec.spec_dictionary()

        action_messages = self.get_all_empty_example_message(plugin_spec.get("actions", {}), "action", "input")
        trigger_messages = self.get_all_empty_example_message(plugin_spec.get("triggers", {}), "trigger", "input")
        connection_messages = self.get_empty_example_message(
            plugin_spec.get("connection", {}),
            "connection"
        )
        all_offenses = ""
        if action_messages:
            all_offenses += "\n" + "\n".join(action_messages)
        if trigger_messages:
            all_offenses += "\n" + "\n".join(trigger_messages)
        if connection_messages:
            all_offenses += "\n" + "\n".join(connection_messages)

        if all_offenses:
            raise ValidationException(
                f"All inputs should have example field in plugin.spec. {all_offenses}"
            )

    @staticmethod
    def get_all_empty_example_message(elements: dict, element_type: str, element_key: str):
        empty_example_messages = []
        for name, element in elements.items():
            empty_example_messages.extend(ExampleInputValidator.get_empty_example_message(
                element.get(element_key, {}),
                element_type,
                name
            ))
        return empty_example_messages

    @staticmethod
    def get_empty_example_message(elements: dict, element_type: str, name: str = None):
        empty_example_messages = []
        for input_name, input_item in elements.items():
            if not input_item.get("example"):
                msg = f"In {element_type}"
                if name:
                    msg += f" \"{name}\""
                msg += f": input \"{input_name}\", there is no example field."
                empty_example_messages.append(msg)
        return empty_example_messages
