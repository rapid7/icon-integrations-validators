import re

from icon_validator.rules.validator import KomandPluginValidator
from icon_plugin_spec.plugin_spec import KomandPluginSpec
from icon_validator.exceptions import ValidationException
import requests
from git import Repo
from git.exc import InvalidGitRepositoryError
import tempfile
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
    REQUIRED = "required"
    CONNECTIONS = "connection"
    TRIGGERS = "triggers"
    TASKS = "tasks"


class MajorVersionBumpValidator(KomandPluginValidator):
    TRIGGER_OR_TASK = ""

    @staticmethod
    def get_remote_spec(spec):
        directory = spec.directory.split("/" + RepoConstants.PLUGIN_DIRNAME + "/")[0]
        try:
            repo = Repo(directory)
        except InvalidGitRepositoryError:
            raise ValidationException("Incorrect directory passed- must be an individual plugin directory")

        remote_list = repo.remote().refs
        blob = None
        remote = None
        for _remote in remote_list:
            if _remote.name == "origin/master":
                remote = _remote
                # now get the blob representing the plugin folder and loop over until we find plugin spec
                for _blob in _remote.object.tree[RepoConstants.PLUGIN_DIRNAME][spec.spec_dictionary()["name"]]:
                    if _blob.name == RepoConstants.PLUGIN_SPEC:
                        blob = _blob
                        break
                if blob is None:
                    # throw error: no plugin spec found in remote
                    raise ValidationException("No plugin spec found in remote repo")
                break
        if remote is None:
            # throw exception : origin/master not found
            raise ValidationException("Remote origin/master not found.'master' branch name changed, update validator")

        # if all went well and no exceptions, we now have the blob of plugin spec
        # using a temp file because stream_data requires a data object
        with tempfile.TemporaryFile() as fp:
            blob.stream_data(fp)
            fp.seek(0)
            plugin_spec_string = fp.read().decode("utf-8")
            return yaml.safe_load(spec.spec_dictionary(plugin_spec_string))

    @staticmethod
    def validate_input_required(remote, local):
        MajorVersionBumpValidator.validate_no_input_new_or_required(remote, local, SpecConstants.ACTIONS)
        MajorVersionBumpValidator.validate_no_input_new_or_required(remote, local, SpecConstants.TRIGGERS)
        MajorVersionBumpValidator.validate_no_input_new_or_required(remote, local, SpecConstants.TASKS)
        MajorVersionBumpValidator.validate_no_input_new_or_required(remote, local, SpecConstants.CONNECTIONS)

    @staticmethod
    def validate_no_input_new_or_required(remote, local, enclosing):
        if enclosing in local and enclosing in remote:
            for key, value in local[enclosing].items():
                for input_key, enclosing_input in value[SpecConstants.INPUT].items():
                    if enclosing_input[SpecConstants.REQUIRED]:
                        if input_key not in remote[enclosing][key][SpecConstants.INPUT] or \
                          not remote[enclosing][key][SpecConstants.INPUT][input_key][SpecConstants.REQUIRED]:
                            raise ValidationException(f"Input has been added or changed to required in {enclosing} without"
                                                      " a major version bump. You may change the input back or bump "
                                                      "to the next major version")


    @staticmethod
    def validate_output_not_required(remote, local):
        MajorVersionBumpValidator.abstract_validate_output_not_required(remote, local, SpecConstants.ACTIONS)
        MajorVersionBumpValidator.abstract_validate_output_not_required(remote, local, SpecConstants.TRIGGERS)
        MajorVersionBumpValidator.abstract_validate_output_not_required(remote, local, SpecConstants.TASKS)

    @staticmethod
    def abstract_validate_output_not_required(remote, local, enclosing):
        if enclosing in remote and enclosing in local:
            for key, value in remote[enclosing].items():
                for output_key, action_output in value[SpecConstants.OUTPUT].items():
                    if action_output[SpecConstants.REQUIRED]:
                        # We know this output exists because this validator is called after verifying all outputs exist
                        local_spec_req = local[enclosing][key][SpecConstants.OUTPUT][output_key][
                            SpecConstants.REQUIRED]
                        if not local_spec_req:
                            raise ValidationException(f"Output has been changed to not required in {enclosing}"
                                                      "without a major version bump You may change"
                                                      " the output back or bump to the next major version")


    @staticmethod
    def validate_no_output_removed(remote, local):
        MajorVersionBumpValidator.abstract_check_existence(remote, local, SpecConstants.ACTIONS, SpecConstants.OUTPUT)
        MajorVersionBumpValidator.abstract_check_existence(remote, local, SpecConstants.TRIGGERS, SpecConstants.OUTPUT)
        MajorVersionBumpValidator.abstract_check_existence(remote, local, SpecConstants.TASKS, SpecConstants.OUTPUT)

    @staticmethod
    def validate_no_input_removed(remote, local):
        # action inputs
        MajorVersionBumpValidator.abstract_check_existence(remote, local, SpecConstants.ACTIONS, SpecConstants.INPUT)

        # connection inputs
        # if the union of the two is equal to each alone in length, they are the same. Done this way to be concise
        # otherwise we'd have to loop through both and check for existence in the other dict
        if SpecConstants.CONNECTIONS in remote:
            all_params = set(remote[SpecConstants.CONNECTIONS]).union(set(local[SpecConstants.CONNECTIONS]))
            if len(all_params) != len(remote[SpecConstants.CONNECTIONS]) or \
               len(all_params) != len(local[SpecConstants.CONNECTIONS]):
                raise ValidationException("Connection input does not match last version. Major version bump required")

        #trigger/task
        MajorVersionBumpValidator.abstract_check_existence(remote, local, SpecConstants.TRIGGERS, SpecConstants.INPUT)
        MajorVersionBumpValidator.abstract_check_existence(remote, local, SpecConstants.TASKS, SpecConstants.INPUT)

    @staticmethod
    def abstract_check_existence(remote, local, enclosing, item_to_check):
        if enclosing in remote and enclosing in local:
            for key, values in remote[enclosing].items():
                if item_to_check in values:
                    for named_value in values[item_to_check]:
                        if named_value not in local[enclosing][key][item_to_check]:
                            raise ValidationException(f"{item_to_check} has been removed from {enclosing} without major"
                                                      " version bump. Add it back or bump to next major version, X.0.0")
                else:
                    # this is an edge case. It means something like an action has no output tag. I think this is legal
                    # so as long as local and remote match its good as far as I'm concerned
                    if item_to_check in local[enclosing][key]:
                        raise ValidationException(f"I hope this never happens {enclosing} {item_to_check}")

    @staticmethod
    def validate_no_action_removed(remote, local):
        for action in remote[SpecConstants.ACTIONS]:
            if action not in local[SpecConstants.ACTIONS]:
                raise ValidationException("Action has been removed from spec without a major version bump"
                                          " You may add the action back or bump to the next major version, X.0.0")

    @staticmethod
    def validate_actions(remote, local):
        MajorVersionBumpValidator.validate_no_action_removed(remote, local)
        for action_key, action_dict in remote[SpecConstants.ACTIONS].items():
            local_dict = local[SpecConstants.ACTIONS][action_key]
            if local_dict[SpecConstants.TITLE] != action_dict[SpecConstants.TITLE]:
                raise ValidationException("Action title has changed without a major version bump. You may change"
                                          " the title back or bump to the next major version, X.0.0")

            MajorVersionBumpValidator.validate_inner_fields(action_dict, local_dict)

    @staticmethod
    def check_major_version_bump_needed(remote, local):
        local_version = local["version"].split('.')
        remote_version = remote["version"].split('.')
        if len(local_version) == 3 and len(remote_version) == 3:
            if int(local_version[0]) > int(remote_version[0]):
                if int(local_version[1]) > 0 or int(local_version[2]) > 0:
                    raise ValidationException("Major version bump should set minor and patch versions to 0 "
                                              "The resulting format should be X.0.0")
                return False
            else:
                return True
        else:
            raise ValidationException("Version does not match required semver format. "
                                      "Version should be in form X.Y.Z with X, Y, and Z "
                                      "being numbers. No special characters or spaces allowed. "
                                      "Versions start at 1.0.0, see https://semver.org/ for more information.")

    def validate(self, spec):
        remote_spec = MajorVersionBumpValidator.get_remote_spec(spec)
        local_spec = spec.spec_dictionary()
        # perform the different sections of validation
        # Check if we already did a major version bump- if so, no need to do all this checking
        if not MajorVersionBumpValidator.check_major_version_bump_needed(remote_spec, local_spec):
            # We already bumped the major version- skip the rest of the validation
            return
        else:
            MajorVersionBumpValidator.validate_no_action_removed(remote_spec, local_spec)
            MajorVersionBumpValidator.validate_no_input_removed(remote_spec, local_spec)
            MajorVersionBumpValidator.validate_no_output_removed(remote_spec, local_spec)
            MajorVersionBumpValidator.validate_input_required(remote_spec, local_spec)
            MajorVersionBumpValidator.validate_output_not_required(remote_spec, local_spec)
            MajorVersionBumpValidator.validate_types_unchanged(remote_spec, local_spec)
