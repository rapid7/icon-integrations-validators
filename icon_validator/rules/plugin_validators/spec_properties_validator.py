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

    _COMPONENT_TASK_WHITELIST = {
        "input",
        "output",
        "title",
        "description",
        "schedule",
        "state"
    }

    _TASK_STATE_PROPERTY_WHITELIST = {
        "title",
        "description",
        "type"
    }

    _TASK_SCHEDULE_PROPERTY_WHITELIST = {
        "title",
        "type",
        "enum",
        "default"
    }

    _TASK_OUTPUT_PROPERTY_WHITELIST = {
        "title",
        "type",
        "description",
        "required",
        "default",
        "enum",
        "order",
        "example",
        "persist_state"
    }

    _PROPERTIES_WHITELIST = {
        "title",
        "type",
        "description",
        "required",
        "default",
        "enum",
        "order",
        "example",
    }

    def __init__(self):
        super().__init__()
        self.property_offenses: [str] = []
        self.component_offenses: [str] = []
        self.component_task_offenses: [str] = []
        self.task_state_property_offenses: [str] = []
        self.task_schedule_property_offenses: [str] = []
        self.component_task_missing_state_schedule_offenses: [str] = []

    def validate(self, spec: KomandPluginSpec):
        raw_connection, raw_actions, raw_triggers, raw_tasks = spec.connection(), spec.actions(), \
                                                               spec.triggers(), spec.tasks()

        # Get components
        connection: PluginComponent = PluginComponent.new_connection(raw=raw_connection)
        actions: [PluginComponent] = \
            [PluginComponent.new_action(raw={k: v}) for k, v in raw_actions.items()] if raw_actions else []
        triggers: [PluginComponent] = \
            [PluginComponent.new_trigger(raw={k: v}) for k, v in raw_triggers.items()] if raw_triggers else []
        tasks: [PluginComponent] = \
            [PluginComponent.new_task(raw={k: v}) for k, v in raw_tasks.items()] if raw_tasks else []

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

        for task in tasks:
            # check for "state" and "schedule" in task
            diff: {str} = self._COMPONENT_TASK_WHITELIST.difference(task.raw_parameters)
            if "state" in diff or "schedule" in diff:
                self._add_component_task_missing_state_schedule_offense_string(component=task.identifier, offenders=diff)

            diff: {str} = task.raw_parameters.difference(self._COMPONENT_TASK_WHITELIST)
            if diff:
                self._add_component_task_offense_string(component=task.identifier, offenders=diff)

            for input_ in task.inputs:
                diff: {str} = input_.raw_parameters.difference(self._PROPERTIES_WHITELIST)
                if diff:
                    self._add_property_offense_string(component=task.identifier,
                                                      identifier=input_.identifier,
                                                      offenders=diff)
            for output in task.outputs:
                diff: {str} = output.raw_parameters.difference(self._TASK_OUTPUT_PROPERTY_WHITELIST)
                if diff:
                    self._add_property_offense_string(component=task.identifier,
                                                      identifier=output.identifier,
                                                      offenders=diff)
            for state in task.state:
                diff: {str} = state.raw_parameters.difference(self._TASK_STATE_PROPERTY_WHITELIST)
                if diff:
                    self._add_task_state_property_offense_string(component=task.identifier,
                                                                 identifier=state.identifier,
                                                                 offenders=diff)
            if task.schedule:
                diff: {str} = task.schedule[0].raw_parameters.difference(self._TASK_SCHEDULE_PROPERTY_WHITELIST)
                if diff:
                    self._add_task_schedule_property_offense_string(component=task.identifier,
                                                                    identifier=task.schedule[0].identifier,
                                                                    offenders=diff)

        # Create a string of all offenses
        all_offenses: str = ""
        if self.component_offenses:
            all_offenses += "The follow invalid component properties were found:\n" + \
                            "\n".join(self.component_offenses) + "\n\n"
        if self.property_offenses:
            all_offenses += "The following invalid input/output properties were found:\n" + \
                            "\n".join(self.property_offenses) + "\n\n"
        if self.component_task_offenses:
            all_offenses += "The following invalid component properties for task were found:\n" + \
                            "\n".join(self.component_task_offenses) + "\n\n"
        if self.task_state_property_offenses:
            all_offenses += "The following invalid task's state properties were found:\n" + \
                            "\n".join(self.task_state_property_offenses) + "\n\n"
        if self.task_schedule_property_offenses:
            all_offenses += "The following invalid task's schedule properties were found:\n" + \
                            "\n".join(self.task_schedule_property_offenses) + "\n\n"
        if self.component_task_missing_state_schedule_offenses:
            all_offenses += "The following tasks are missing properties:\n" + \
                            "\n".join(self.component_task_missing_state_schedule_offenses) + "\n\n"

        # If there is an offense string at all (indicative of an offense), raise an Exception
        if all_offenses:
            raise ValidationException(all_offenses)

    def _add_component_offense_string(self, component: str, offenders: {str}):
        self.component_offenses.append("%s: %s" % (component, offenders))

    def _add_property_offense_string(self, component: str, identifier: str, offenders: {str}):
        self.property_offenses.append("%s:%s: %s" % (component, identifier, offenders))

    def _add_component_task_offense_string(self, component: str, offenders: {str}):
        self.component_task_offenses.append("%s: %s" % (component, offenders))

    def _add_component_task_missing_state_schedule_offense_string(self, component: str, offenders: {str}):
        self.component_task_missing_state_schedule_offenses.append("%s: %s" % (component, offenders))

    def _add_task_state_property_offense_string(self, component: str, identifier: str, offenders: {str}):
        self.task_state_property_offenses.append("%s:%s: %s" % (component, identifier, offenders))

    def _add_task_schedule_property_offense_string(self, component: str, identifier: str, offenders: {str}):
        self.task_schedule_property_offenses.append("%s:%s: %s" % (component, identifier, offenders))
