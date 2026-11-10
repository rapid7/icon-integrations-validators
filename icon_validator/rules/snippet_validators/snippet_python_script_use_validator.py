from typing import List

from icon_plugin_spec.plugin_spec import KomandPluginSpec

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.snippet.unmarshal import read_snippet
from icon_validator.styling import YELLOW


class SnippetPythonScriptUseValidator(KomandPluginValidator):

    _PLUGIN_TITLE = "Python 3 Script"
    # A .snpt file names a step's plugin by its spec name, not its title
    _PLUGIN_SPEC_NAME = "python_3_script"

    def python_plugin_used(self, snippet: dict) -> List[str]:
        """
        python_plugin_used finds the snippet steps that use the python plugin
        :param snippet: .snpt file contents
        :return: names of the steps that use the python plugin
        """
        step_names = []
        steps = snippet.get("steps")
        if not isinstance(steps, list):
            return step_names
        for step in steps:
            metadata = step.get("metadata") if isinstance(step, dict) else None
            plugin = metadata.get("plugin") if isinstance(metadata, dict) else None
            if isinstance(plugin, dict) and self._PLUGIN_SPEC_NAME in str(plugin.get("name")):
                step_names.append(step.get("name"))
        return step_names

    def validate(self, spec: KomandPluginSpec) -> None:
        """
        Checks if the snippet contains the usage of the python script plugin and warns
        of its use
        """
        step_names = self.python_plugin_used(read_snippet(spec.directory))

        if step_names:
            results = f"\t{YELLOW}{self._PLUGIN_TITLE} use found in these steps\n"

            for step_name in step_names:
                results += f"\t\t[-] Step Name - {step_name}\n"
            results += "\tPlease review these steps carefully before use"
            print(results)
