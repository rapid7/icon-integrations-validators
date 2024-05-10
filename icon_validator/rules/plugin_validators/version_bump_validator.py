import git

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException, NO_LOCAL_CON_VERSION, \
    NO_CON_VERSION_CHANGE, INVALID_CON_VERSION_CHANGE, INCORRECT_CON_VERSION_CHANGE, FIRST_TIME_CON_VERSION_ISSUE
from git import Repo
from git.exc import InvalidGitRepositoryError
import yaml


class RepoConstants:
    PLUGIN_DIRNAME = "plugins"
    PLUGIN_SPEC = "plugin.spec.yaml"


class SpecConstants:
    # normally you would use the pluginspec accessors...but we don't have pluginspec objects here
    # due to the fact that we don't actually have the "remote" plugin stored locally, comparing them this way is easy
    ACTIONS = "actions"
    TITLE = "title"
    INPUT = "input"
    OUTPUT = "output"
    TYPE = "type"
    TYPES = "types"
    REQUIRED = "required"
    CONNECTIONS = "connection"
    CONNECTION_VERSION = "connection_version"
    TRIGGERS = "triggers"
    TASKS = "tasks"
    VERSION = "version"


class VersionBumpValidator(KomandPluginValidator):

    def __init__(self):
        super().__init__()
        self.MAJOR_INSTRUCTIONS_STRING = ""
        self.MINOR_INSTRUCTIONS_STRING = ""
        self.name = "Version Increment Validator"
        self.local_version = None
        self.remote_version = None

    @staticmethod
    def get_remote_spec(spec):
        """
        Get the existing remote spec for this plugin from the repo
        """
        directory = spec.directory.split(f"/{RepoConstants.PLUGIN_DIRNAME}/")[0]
        try:
            repo = Repo(directory)
        except InvalidGitRepositoryError:
            raise ValidationException("Incorrect directory passed- must be an individual plugin directory")

        remote_list = repo.remote().refs
        blob = VersionBumpValidator.get_plugin_spec_blob(remote_list, spec.spec_dictionary()["name"])
        # case: remote spec not found
        if blob is None:
            return None

        # if all went well and no exceptions, we now have the blob of plugin spec
        # using a temp file because stream_data requires a data object
        try:
            remote_spec = yaml.safe_load(blob.data_stream.read())
        except yaml.YAMLError:
            raise ValidationException("Remote plugin.spec.yaml contains incorrect yaml and must be fixed. "
                                      "If this change fixes remote spec, disregard this error message")
        return remote_spec

    @staticmethod
    def get_plugin_spec_blob(remote_list: [git.RemoteReference], plugin_name: str):
        """
        Get the plugin spec blob from the remote repo
        """
        blob = None
        remote = None
        for _remote in remote_list:
            if _remote.name == "origin/master":
                remote = _remote
                # now get the blob representing the plugin folder and loop over until we find plugin spec
                try:
                    for _blob in _remote.object.tree[RepoConstants.PLUGIN_DIRNAME][plugin_name]:
                        if _blob.name == RepoConstants.PLUGIN_SPEC:
                            blob = _blob
                            break
                except KeyError:
                    # plugin name not found, so version increment is not really relevant
                    return None
                if blob is None:
                    # throw error: no plugin spec found in remote
                    raise ValidationException(f"{RepoConstants.PLUGIN_SPEC} not found in remote repo")
                break
        if remote is None:
            # throw exception : origin/master not found
            raise ValidationException("Remote origin/master not found.'master' branch name changed, update validator")
        return blob

    def validate_no_sections_removed(self, remote: dict, local: dict):
        # checks if either "input" or "output" was removed or added to a trigger or action
        # remote and local are dictionaries of an action or trigger
        if (SpecConstants.INPUT in remote) != (SpecConstants.INPUT in local):
            raise ValidationException(f"Input section was added or removed without a major version increment."
                                      f"{self.MAJOR_INSTRUCTIONS_STRING}")
        if (SpecConstants.OUTPUT in remote) != (SpecConstants.OUTPUT in local):
            raise ValidationException(f"Output section was added or removed without a major version increment."
                                      f"{self.MAJOR_INSTRUCTIONS_STRING}")

    def validate_all_types_exist(self, remote: dict, local: dict):
        # checks if an entire type has been removed from spec
        for type_key in remote[SpecConstants.TYPES]:
            if type_key not in local[SpecConstants.TYPES]:
                raise ValidationException(f"Type {type_key} has been removed without a major version increment."
                                          f"{self.MAJOR_INSTRUCTIONS_STRING}")

    def validate_no_types_changed(self, remote: dict, local: dict):
        # verifies that types have not been changed between spec versions
        if SpecConstants.TYPES in remote and SpecConstants.TYPES in local:
            self.validate_all_types_exist(remote, local)
            for type_key, type_value in remote[SpecConstants.TYPES].items():
                for type_inner_key, type_inner_val in type_value.items():
                    local_type_in = local[SpecConstants.TYPES][type_key]
                    if type_inner_key not in local_type_in:
                        raise ValidationException(f"Type {type_inner_key} removed from {type_key} without a major"
                                                  f" version increment."
                                                  f"{self.MAJOR_INSTRUCTIONS_STRING}")
                    if type_inner_val.get(SpecConstants.TYPE) != local_type_in[type_inner_key].get(SpecConstants.TYPE):
                        raise ValidationException(f"Type {type_inner_key} changed in type {type_key} without a major"
                                                  f" version increment."
                                                  f"{self.MAJOR_INSTRUCTIONS_STRING}")

                    if type_inner_val.get(SpecConstants.REQUIRED) != local_type_in[type_inner_key].get(SpecConstants.REQUIRED):
                        raise ValidationException(f"Type {type_inner_key} changed in type {type_key} without a major"
                                                  f"version increment."
                                                  f"{self.MAJOR_INSTRUCTIONS_STRING}")

    def validate_no_inner_type_changes(self, remote, local):
        self.abstract_validate_no_change(remote, local, SpecConstants.INPUT, SpecConstants.TYPE)
        self.abstract_validate_no_change(remote, local, SpecConstants.OUTPUT, SpecConstants.TYPE)

    def validate_no_titles_changed(self, remote, local):
        self.abstract_validate_no_change(remote, local, SpecConstants.INPUT, SpecConstants.TITLE)
        self.abstract_validate_no_change(remote, local, SpecConstants.OUTPUT, SpecConstants.TITLE)

    def abstract_validate_no_change(self, remote: dict, local: dict, input_or_output: str, field: str):
        # meant to validate type/title inside of individual inputs/outputs
        # input_or_output is the string spec constant for either "input" or "output"
        if input_or_output in remote:
            for key, value in remote[input_or_output].items():
                if field in value and key in local[input_or_output] and field in local[input_or_output][key]:
                    old_value = value[field]
                    new_value = local[input_or_output][key][field]
                    if old_value != new_value:
                        raise ValidationException(f"{field} has changed in {input_or_output} {key} without a major"
                                                  f"version increment."
                                                  f"{self.MAJOR_INSTRUCTIONS_STRING}")

    def validate_no_input_new_or_required(self, remote: dict, local: dict):
        # operates on dictionary of individual action/trigger/task
        for input_key, input_value in local[SpecConstants.INPUT].items():
            if input_value.get(SpecConstants.REQUIRED):
                if input_key not in remote[SpecConstants.INPUT] or \
                  not remote[SpecConstants.INPUT][input_key].get(SpecConstants.REQUIRED, False):
                    raise ValidationException(f"Input has been added or changed to required in {input_key} without"
                                              f" a major version increment."
                                              f"{self.MAJOR_INSTRUCTIONS_STRING}")

    def validate_no_output_no_longer_required(self, remote: dict, local: dict):
        # verifies that outputs have not been changed from required to optional
        # input: complete spec dictionary
        if SpecConstants.OUTPUT in remote and SpecConstants.OUTPUT in local:
            for output_key, output_vals in remote[SpecConstants.OUTPUT].items():
                if SpecConstants.REQUIRED in output_vals and \
                        SpecConstants.REQUIRED in local[SpecConstants.OUTPUT][output_key]:
                    if output_vals[SpecConstants.REQUIRED]:
                        # We know this output exists because this validator is called after verifying all outputs exist
                        local_spec_req = local[SpecConstants.OUTPUT][output_key].get(SpecConstants.REQUIRED)
                        if not local_spec_req:
                            raise ValidationException(f"Output {output_key} has been changed to not required in "
                                                      "without a major version increment."
                                                      f"{self.MAJOR_INSTRUCTIONS_STRING}")

    def validate_no_output_removed(self, remote: dict, local: dict):
        for item in remote[SpecConstants.OUTPUT]:
            if item not in local[SpecConstants.OUTPUT]:
                raise ValidationException("Output has been removed from an action or trigger. This requires "
                                          f"a major version increment.{self.MAJOR_INSTRUCTIONS_STRING}")

    def validate_no_input_removed(self, remote: dict, local: dict):
        for item in remote[SpecConstants.INPUT]:
            if item not in local[SpecConstants.INPUT]:
                raise ValidationException("Input has been removed from an action or trigger. This requires "
                                          f"a major version increment.{self.MAJOR_INSTRUCTIONS_STRING}")

    def validate_no_action_removed(self, remote: dict, local: dict):
        # input: complete spec dictionary
        for action in remote.get(SpecConstants.ACTIONS, []):
            if action not in local[SpecConstants.ACTIONS]:
                raise ValidationException(f"Action {action} has been removed from spec without major version increment."
                                          f"{self.MAJOR_INSTRUCTIONS_STRING}")

    def validate_no_trigger_removed(self, remote: dict, local: dict):
        # input: complete spec dictionary
        for trigger in remote.get(SpecConstants.TRIGGERS, []):
            if trigger not in local[SpecConstants.TRIGGERS]:
                raise ValidationException(f"Trigger {trigger} has been removed from {RepoConstants.PLUGIN_SPEC} without"
                                          f" a major version increment.{self.MAJOR_INSTRUCTIONS_STRING}")

    def validate_actions(self, remote: dict, local: dict):
        # input: complete spec dictionary
        if SpecConstants.ACTIONS in remote and SpecConstants.ACTIONS in local:
            self.validate_no_action_removed(remote, local)
            for action_key, remote_action_dict in remote[SpecConstants.ACTIONS].items():
                local_dict = local[SpecConstants.ACTIONS][action_key]
                if local_dict.get(SpecConstants.TITLE) != remote_action_dict.get(SpecConstants.TITLE):
                    raise ValidationException(f"Action {action_key} title has changed without a major version increment."
                                              f"{self.MAJOR_INSTRUCTIONS_STRING}")

                self.validate_inner_fields(remote_action_dict, local_dict)

    def validate_triggers(self, remote: dict, local: dict):
        # input: complete spec dictionary
        if SpecConstants.TRIGGERS in remote and SpecConstants.TRIGGERS in local:
            self.validate_no_trigger_removed(remote, local)
            for trigger_key, remote_trigger_dict in remote[SpecConstants.TRIGGERS].items():
                local_dict = local[SpecConstants.TRIGGERS][trigger_key]
                if local_dict.get(SpecConstants.TITLE) != remote_trigger_dict.get(SpecConstants.TITLE):
                    raise ValidationException(f"Trigger {trigger_key} title has changed without a major version "
                                              f"increment.{self.MAJOR_INSTRUCTIONS_STRING}")

                self.validate_inner_fields(remote_trigger_dict, local_dict)

    def validate_connections(self, remote: dict, local: dict):
        # This may well be deprecated almost immediately when versioned connections is released
        # input: complete spec dictionary
        if SpecConstants.CONNECTIONS in remote:
            if SpecConstants.CONNECTIONS not in local:
                raise ValidationException("Connection removed without a major version increment."
                                          f"{self.MAJOR_INSTRUCTIONS_STRING}")
            for key, value in remote[SpecConstants.CONNECTIONS].items():
                if key not in local[SpecConstants.CONNECTIONS]:
                    raise ValidationException(f"{key} removed from connection without a major version increment."
                                              f"{self.MAJOR_INSTRUCTIONS_STRING}")
            for key, value in local[SpecConstants.CONNECTIONS].items():
                if key not in remote[SpecConstants.CONNECTIONS] and value[SpecConstants.REQUIRED]:
                    raise ValidationException(f"{key} added to connection as required input without major version"
                                              f"increment.{self.MAJOR_INSTRUCTIONS_STRING}")
            # established the same keys/vals at this point. Check titles / types next
            for key, value in local[SpecConstants.CONNECTIONS].items():
                if key in remote[SpecConstants.CONNECTIONS]:
                    curr_compare = remote[SpecConstants.CONNECTIONS][key]
                    if value.get(SpecConstants.TITLE) != curr_compare.get(SpecConstants.TITLE):
                        raise ValidationException(f"Title changed in connection field {key}, requiring a major version"
                                                  f" increment.{self.MAJOR_INSTRUCTIONS_STRING}")
                    if value.get(SpecConstants.TYPE) != curr_compare.get(SpecConstants.TYPE):
                        raise ValidationException(f"Type changed in connection field {key}, requiring a major version"
                                                  f" increment.{self.MAJOR_INSTRUCTIONS_STRING}")
        else:
            if SpecConstants.CONNECTIONS in local:
                raise ValidationException(f"Connection newly added to {RepoConstants.PLUGIN_SPEC}. This requires a"
                                          f" major version increment.{self.MAJOR_INSTRUCTIONS_STRING}")

    def validate_connection_version(self, local_spec, remote_spec=None):
        # Check if a connection version needs to be specified
        if local_spec.get(SpecConstants.CONNECTIONS):
            err_info = f"Based on plugin version this should be '{self.local_version[0]}'."
            local_connection_version = local_spec.get(SpecConstants.CONNECTION_VERSION)
            if not local_connection_version:  # releasing and missing connection version
                raise ValidationException(f"{NO_LOCAL_CON_VERSION} {err_info}")
            elif remote_spec:
                old_connection_version = remote_spec.get(SpecConstants.CONNECTION_VERSION)
                if old_connection_version:
                    try:
                        self.validate_connections(remote_spec, local_spec)  # Check if connection details have changed
                    except ValidationException:
                        # Validation noticed a difference between remote and local; now check we bumped the version
                        if old_connection_version == local_connection_version:
                            raise ValidationException(f"{NO_CON_VERSION_CHANGE} {err_info}")
                        elif local_connection_version != (old_connection_version + 1):
                            raise ValidationException(f"{INCORRECT_CON_VERSION_CHANGE} {err_info}")
                        return  # validation happy that connection schema and version bumped
                    # no changes the connection version should not have changed
                    if int(local_connection_version) != int(remote_spec.get(SpecConstants.CONNECTION_VERSION)):
                        raise ValidationException(f"{INVALID_CON_VERSION_CHANGE}")
                elif int(local_connection_version) != int(self.local_version[0]):
                    # No version to compare against we should make sure one that is supplied matches our plugin version
                    raise ValidationException(f"{FIRST_TIME_CON_VERSION_ISSUE} {err_info}")

    def validate_inner_fields(self, remote, local):
        self.validate_no_sections_removed(remote, local)
        if SpecConstants.INPUT in remote and SpecConstants.INPUT in local:
            self.validate_no_input_removed(remote, local)
            self.validate_no_input_new_or_required(remote, local)
        if SpecConstants.OUTPUT in remote and SpecConstants.OUTPUT in local:
            self.validate_no_output_removed(remote, local)
            self.validate_no_output_no_longer_required(remote, local)

        self.validate_no_titles_changed(remote, local)
        self.validate_no_inner_type_changes(remote, local)

    def check_major_version_increment_needed(self):
        # Checks to see if version is valid sem-ver, and if we already bumped major version
        if int(self.local_version[0]) > int(self.remote_version[0]):
            if int(self.local_version[1]) > 0 or int(self.local_version[2]) > 0:
                raise ValidationException("Major version increment should set minor and patch versions to 0.")
            return False
        else:
            self.MAJOR_INSTRUCTIONS_STRING = f" Please change the plugin version to " \
                                             f"{int(self.remote_version[0])+1}.0.0"
            return True

    def check_minor_version_increment_needed(self):
        # Checks to see if version is valid sem-ver, and if we already bumped minor version
        if int(self.local_version[1]) > int(self.remote_version[1]):
            if int(self.local_version[2]) > 0:
                raise ValidationException("Minor version increment should set patch version to 0 "
                                          "The resulting format should be X.Y.0")
            return False
        else:
            self.MINOR_INSTRUCTIONS_STRING = f" Please change the plugin version to " \
                                             f"{int(self.remote_version[0])}." \
                                             f"{int(self.remote_version[1]) + 1}.0"
            return True

    @staticmethod
    def modify_version_array(version_arr: [str]):
        if version_arr[2].find('-') >= 0:
            # if there is a '-' such as in 1.0.4-beta we want to only leave the 4 but remove the '-beta'
            version_arr[2] = version_arr[2].split('-')[0]
        return version_arr

    def validate_minor_triggers(self, remote, local):
        self.check_for_new(remote, local, SpecConstants.TRIGGERS)
        self.validate_minor_inputs_outputs(remote, local, SpecConstants.TRIGGERS)

    def validate_minor_actions(self, remote, local):
        self.check_for_new(remote, local, SpecConstants.ACTIONS)
        self.validate_minor_inputs_outputs(remote, local, SpecConstants.ACTIONS)

    def check_for_new(self, remote: dict, local: dict, spec_type: str):
        # remote and local are the complete spec
        if spec_type in local:
            if spec_type not in remote:
                raise ValidationException(f"Plugin spec section {spec_type} added to {RepoConstants.PLUGIN_SPEC}."
                                          f"{self.MINOR_INSTRUCTIONS_STRING}")
            for key in local[spec_type]:
                if key not in remote[spec_type]:
                    raise ValidationException(f"Added {spec_type}: {key}."
                                              f"{self.MINOR_INSTRUCTIONS_STRING}")

    def validate_minor_inputs_outputs(self, remote, local, spec_type):
        # Because we passed major version bump validator, we know there are no new required inputs so any new inputs
        # ARE required. We also know that there is no removed input or output fields between the two specs
        # Here, we check for new output or new non-required input
        if spec_type in local and spec_type in remote:
            for key, value in local[spec_type].items():
                remote_val = remote[spec_type][key]
                self.check_new_inputs_outputs(remote_val, value, SpecConstants.INPUT)
                self.check_new_inputs_outputs(remote_val, value, SpecConstants.OUTPUT)

    def check_new_inputs_outputs(self, remote: dict, local: dict, input_output: str):
        # remote, local are dictionaries of action or trigger inputs or outputs
        if input_output in local:
            for inner_key in local[input_output]:
                if inner_key not in remote[input_output]:
                    raise ValidationException(f"New {input_output} added without incrementing minor version."
                                              f"{self.MINOR_INSTRUCTIONS_STRING}")

    @staticmethod
    def get_versions(local_spec, remote_spec):
        local_version = local_spec[SpecConstants.VERSION].split('.')
        remote_version = remote_spec[SpecConstants.VERSION].split('.') if remote_spec else ['0', '0', '0']
        if len(local_version) == 3 and len(remote_version) == 3:
            local_version = VersionBumpValidator.modify_version_array(local_version)
            remote_version = VersionBumpValidator.modify_version_array(remote_version)
        else:
            raise ValidationException("Version does not match required semver format. "
                                      "Version should be in form X.Y.Z with X, Y, and Z "
                                      "being numbers. No special characters or spaces allowed. "
                                      "Versions start at 1.0.0, see https://semver.org/ for more information.")

        return local_version, remote_version

    def validate(self, spec):
        remote_spec = VersionBumpValidator.get_remote_spec(spec)
        local_spec = spec.spec_dictionary()

        self.local_version, self.remote_version = self.get_versions(local_spec, remote_spec)

        # we should validate connection versions regardless of the version changes to ensure these remain stable
        self.validate_connection_version(local_spec, remote_spec)

        # case: new plugin with no remote spec
        if remote_spec is None:
            return
        # perform the different sections of validation
        # Check if we already did a major version bump- if so, no need to do all this checking
        if not self.check_major_version_increment_needed():
            return
        else:
            self.validate_actions(remote_spec, local_spec)
            self.validate_triggers(remote_spec, local_spec)
            self.validate_connections(remote_spec, local_spec)
            self.validate_no_types_changed(remote_spec, local_spec)

        # minor version validation (NOTE: It is important that minor comes AFTER major version due to assumptions made)
        if not self.check_minor_version_increment_needed():
            # already validated that no major bump was needed and we bumped minor version- skip further validation
            return
        else:
            self.validate_minor_triggers(remote_spec, local_spec)
            self.validate_minor_actions(remote_spec, local_spec)
