from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException

import os
import json
import re


class WorkflowHelpPluginUtilizationValidator(KomandPluginValidator):

    @staticmethod
    def extract_plugins_used(spec):
        value = spec.directory
        data = dict()
        for file_name in os.listdir(value):
            if file_name.endswith(".icon"):
                with open(f"{value}/{file_name}") as json_file:
                    try:
                        data = json.load(json_file)
                    except json.JSONDecodeError:
                        raise ValidationException(
                            "The .icon file is not in JSON format. Try exporting the .icon file again")
        try:
            plugins = data["kom"]["workflowVersions"][0]
        except KeyError:
            raise ValidationException("The .icon file is not formatted correctly. Try exporting the .icon file again")

        plugin_list = list()
        try:
            for step in plugins["steps"]:
                if "plugin" in plugins["steps"][step].keys():
                    if len(plugin_list):
                        for index, d in enumerate(plugin_list):
                            if d["Plugin"] == plugins["steps"][step]["plugin"]["name"] and d["Version"] == \
                                    plugins["steps"][step]["plugin"]["slugVersion"]:
                                plugin_list[index]["Count"] = plugin_list[index]["Count"] + 1

                            elif not any(d["Plugin"] == plugins["steps"][step]["plugin"]["name"] for d in
                                         plugin_list) or not any(
                                    d["Version"] == plugins["steps"][step]["plugin"]["slugVersion"] for d in
                                    plugin_list):
                                plugin_list.append({"Plugin": plugins["steps"][step]["plugin"]["name"],
                                                    "Version": plugins["steps"][step]["plugin"]["slugVersion"],
                                                    "Count": 1})
                                break
                    else:
                        plugin_list.append({"Plugin": plugins["steps"][step]["plugin"]["name"],
                                            "Version": plugins["steps"][step]["plugin"]["slugVersion"], "Count": 1})
        except KeyError:
            raise ValidationException("The .icon file is not formatted correctly. Try exporting the .icon file again")
        return plugin_list

    @staticmethod
    def extract_plugins_in_help(help_str):
        regex = r"\|Plugin\|Version\|Count\|.*?#"

        plugins_utilized = re.findall(regex, help_str, re.DOTALL)
        plugins_list = plugins_utilized[0].split("\n")
        plugins_list = list(
            filter(lambda item: item.startswith("|") and not (item.startswith("|P") or item.startswith("|-")),
                   plugins_list))
        plugins_dict_list = list()
        for plugin in plugins_list:
            temp = plugin.split("|")
            plugins_dict_list.append({"Plugin": temp[1], "Version": temp[2], "Count": int(temp[3])})
        return plugins_dict_list

    def validate(self, spec):
        plugins_used = WorkflowHelpPluginUtilizationValidator.extract_plugins_used(spec)
        plugin_in_help = WorkflowHelpPluginUtilizationValidator.extract_plugins_in_help(spec.raw_help())
        for plugin in plugins_used:
            if plugin not in plugin_in_help:
                raise ValidationException("The following plugin was found in the .icon file,"
                                          f" but not in the help file {plugin}")
        for plugin in plugin_in_help:
            if plugin not in plugins_used:
                raise ValidationException("The following plugin was found in the help file,"
                                          f" but not in the .icon file {plugin}")
