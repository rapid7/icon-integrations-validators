from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException
from icon_plugin_spec.plugin_spec import KomandPluginSpec

import os
import json
import re


class _Plugin(object):

    def __init__(self, name: str, version: str):
        self.plugin = name
        self.version = version

    def __eq__(self, other):
        return (self.plugin == other.plugin) and (self.version == other.version)

    def __hash__(self):
        return hash((self.plugin, self.version))


class WorkflowHelpPluginUtilizationValidator(KomandPluginValidator):

    @staticmethod
    def load_workflow_file(spec: KomandPluginSpec) -> dict:
        """
        Load a workflow file as KomandPluginSpec into a dictionary
        :param spec: .icon workflow
        :return: Workflow spec as a dictionary
        """
        workflow_directory = spec.directory

        for file_name in os.listdir(workflow_directory):
            if not (file_name.endswith(".icon")):
                continue

            with open(f"{workflow_directory}/{file_name}") as json_file:
                try:
                    workflow_file = json.load(json_file)
                except json.JSONDecodeError:
                    raise ValidationException(
                        "The .icon file is not in JSON format. Try exporting the .icon file again")

            return workflow_file

    @staticmethod
    def extract_workflow(workflow_file: dict) -> dict:
        """
        Returns a workflow with metadata and step information
        :param workflow_file: Dictionary containing workflow information
        :return: Workflow metadata and step information as a dict
        """
        try:
            workflow = workflow_file["kom"]["workflowVersions"][0]
        except KeyError:
            raise ValidationException("The .icon file is not formatted correctly. Try exporting the .icon file again")

        return workflow

    @staticmethod
    def extract_plugins_used(workflow: dict) -> [dict]:

        # Raw list of plugins
        plugin_list = list()
        try:
            for step_id in workflow["steps"]:
                step: dict = workflow["steps"][step_id]

                # We only care about plugin steps, so continue if it is not
                if "plugin" not in step.keys():
                    continue

                plugin_name = step["plugin"]["name"]
                plugin_version = step["plugin"]["slugVersion"]

                plugin = _Plugin(name=plugin_name, version=plugin_version)
                plugin_list.append(plugin)

            # Once the loop is done, count unique items
            plugins_and_counts = []

            for plugin in set(plugin_list):
                count = plugin_list.count(plugin)
                plugins_and_counts.append({**plugin.__dict__, "count": count})

            return plugins_and_counts

        except KeyError:
            raise ValidationException("The .icon file is not formatted correctly. Try exporting the .icon file again")

    @staticmethod
    def extract_plugins_in_help(help_str: str) -> list:
        """
        Takes the help.md file as a string and extracts plugin version and count as a list of dictionaries
        """
        # regex to isolate the plugin utilization table
        regex = r"\|Plugin\|Version\|Count\|.*?#"

        plugins_utilized = re.findall(regex, help_str, re.DOTALL)
        # Split each line into a sub string
        if not plugins_utilized:
            return []

        plugins_list = plugins_utilized[0].split("\n")
        # remove trailing and leading lines so that only plugin utilization data is left
        plugins_list = list(
            filter(lambda item: item.startswith("|") and not (item.startswith("|Plugin") or item.startswith("|-")),
                   plugins_list))
        plugins_dict_list = list()
        # Build dictionary for each plugin e.g. {'Plugin': 'ExtractIt', 'Version': '1.1.6', 'Count': 1}
        # then append to a list
        for plugin in plugins_list:
            temp = plugin.split("|")
            plugins_dict_list.append({"plugin": temp[1], "version": temp[2], "count": int(temp[3])})

        return plugins_dict_list

    def validate(self, spec):
        workflow_file = WorkflowHelpPluginUtilizationValidator.load_workflow_file(spec)
        workflow = WorkflowHelpPluginUtilizationValidator.extract_workflow(workflow_file)
        plugins_used = WorkflowHelpPluginUtilizationValidator.extract_plugins_used(workflow)
        plugin_in_help = WorkflowHelpPluginUtilizationValidator.extract_plugins_in_help(spec.raw_help())
        for plugin in plugins_used:
            if plugin not in plugin_in_help:
                raise ValidationException("The following plugin was found in the .icon file,"
                                          f" but not in the help file {plugin}")
        for plugin in plugin_in_help:
            if plugin not in plugins_used:
                raise ValidationException("The following plugin was found in the help file,"
                                          f" but not in the .icon file {plugin}")
