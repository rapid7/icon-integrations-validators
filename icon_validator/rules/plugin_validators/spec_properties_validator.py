from icon_plugin_spec.plugin_spec import KomandPluginSpec, PluginComponent

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class SpecPropertiesValidator(KomandPluginValidator):
    _COMPONENT_WHITELIST = {
        "input",
        "output",
        "title",
        "description"
    }

    _PROPERTIES_WHITELIST = {
        "title",
        "type",
        "description",
        "required",
        "default",
        "enum",
        "order"
    }

    def __init__(self):
        super().__init__()
        self.property_offenses: [str] = []
        self.component_offenses: [str] = []

    def validate(self, spec: KomandPluginSpec):
        raw_connection, raw_actions, raw_triggers = spec.connection(), spec.actions(), spec.triggers()

        # Get components
        connection: PluginComponent = PluginComponent.new_connection(raw=raw_connection)
        actions: [PluginComponent] = \
            [PluginComponent.new_action(raw={k: v}) for k, v in raw_actions.items()] if raw_actions else []
        triggers: [PluginComponent] = \
            [PluginComponent.new_trigger(raw={k: v}) for k, v in raw_triggers.items()] if raw_triggers else []

        for input_ in connection.inputs:
            diff: {str} = input_.raw_parameters.difference(self._PROPERTIES_WHITELIST)
            if diff:
                self._add_property_offense_string(component=connection.identifier,
                                                  identifier=input_.identifier,
                                                  offenders=diff)

        for action in actions:
            diff: {str} = action.raw_parameters.difference(self._COMPONENT_WHITELIST)
            if diff:
                self._add_component_offense_string(component=action.identifier, offenders=diff)

            for input_ in action.inputs:
                diff: {str} = input_.raw_parameters.difference(self._PROPERTIES_WHITELIST)
                if diff:
                    self._add_property_offense_string(component=action.identifier,
                                                      identifier=input_.identifier,
                                                      offenders=diff)
            for output in action.outputs:
                diff: {str} = output.raw_parameters.difference(self._PROPERTIES_WHITELIST)
                if diff:
                    self._add_property_offense_string(component=action.identifier,
                                                      identifier=output.identifier,
                                                      offenders=diff)

        for trigger in triggers:
            diff: {str} = trigger.raw_parameters.difference(self._COMPONENT_WHITELIST)
            if diff:
                self._add_component_offense_string(component=trigger.identifier, offenders=diff)

            for input_ in trigger.inputs:
                diff: {str} = input_.raw_parameters.difference(self._PROPERTIES_WHITELIST)
                if diff:
                    self._add_property_offense_string(component=trigger.identifier,
                                                      identifier=input_.identifier,
                                                      offenders=diff)
            for output in trigger.outputs:
                diff: {str} = output.raw_parameters.difference(self._PROPERTIES_WHITELIST)
                if diff:
                    self._add_property_offense_string(component=trigger.identifier,
                                                      identifier=output.identifier,
                                                      offenders=diff)

        # Create a string of all offenses
        all_offenses: str = ""
        if self.component_offenses:
            all_offenses += "The follow invalid component properties were found:\n" + \
                            "\n".join(self.component_offenses) + "\n\n"
        if self.property_offenses:
            all_offenses += "The following invalid input/output properties were found:\n" + \
                            "\n".join(self.property_offenses) + "\n\n"

        # If there is an offense string at all (indicative of an offense), raise an Exception
        if all_offenses:
            raise ValidationException(all_offenses)

    def _add_component_offense_string(self, component: str, offenders: {str}):
        self.component_offenses.append("%s: %s" % (component, offenders))

    def _add_property_offense_string(self, component: str, identifier: str, offenders: {str}):
        self.property_offenses.append("%s:%s: %s" % (component, identifier, offenders))
