import os

from icon_plugin_spec.plugin_spec import KomandPluginSpec

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.rules.workflow_validators.workflow_screenshot_validator import WorkflowScreenshotValidator


class SnippetScreenshotValidator(KomandPluginValidator):

    def validate(self, spec: KomandPluginSpec) -> None:
        """
        Screenshots are optional for snippets. When the spec lists screenshots or the snippet
        directory has a screenshots directory, the workflow screenshot rules apply.
        """
        resources = spec.spec_dictionary().get("resources")
        screenshots_listed = isinstance(resources, dict) and bool(resources.get("screenshots"))
        screenshots_included = os.path.isdir(os.path.join(spec.directory, "screenshots"))

        if screenshots_listed or screenshots_included:
            # A new instance per run, because WorkflowScreenshotValidator collects file names on the instance
            WorkflowScreenshotValidator().validate(spec)
