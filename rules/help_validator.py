from .validator import KomandPluginValidator


class HelpValidator(KomandPluginValidator):

    @staticmethod
    def validate_help_exists(spec):
        if 'help' in spec:
            raise Exception('Help section should exist in help.md and not in the plugin.spec.yaml file')

    @staticmethod
    def validate_version_history(help_str):
        if '- Initial plugin' not in help_str:
            raise Exception("Initial plugin version line is missing: 1.0.0 - Initial plugin")

        if 'Support web server mode' not in help_str and '1.0.0 - Initial plugin' not in help_str:
            # Match legacy versioning which indicates this plugin came before web server mode existed
            if '* 0.' in help_str:
                # Takes advantage of the fact that versioning used to start from 0.1.0 instead of 1.0.0
                raise Exception(
                                "Initial plugin was released prior to schema V2 but versioning history "
                                "does not document the upgrade to web server mode: Support web server mode"
                                )

    @staticmethod
    def validate_same_plugin_title(spec, halp):
        if 'title' in spec:
            if '# {}'.format(spec['title']) not in halp:
                raise Exception('Help section is missing the top level title heading of: # {}'.format(spec['title']))

    @staticmethod
    def validate_same_actions_title(spec, halp):
        if 'actions' in spec:
            HelpValidator.validate_same_actions_loop(spec['actions'], halp)
        if 'triggers' in spec:
            HelpValidator.validate_same_actions_loop(spec['triggers'], halp)

    @staticmethod
    def validate_same_actions_loop(section, help_str):
        for i in section:
            if 'title' in section[i]:
                if '### {}'.format(section[i]['title']) not in help_str:
                    raise Exception('Help section is missing title of: ### {}'.format(section[i]['title']))

    @staticmethod
    def validate_title_spelling(spec, halp):
        if 'title' in spec:
            title = spec['title']
            lower_title = title.lower()
            for line in halp.split('\n'):
                lower_line = line.lower()
                if lower_title in lower_line:
                    if title not in line:
                        if lower_line[lower_line.find(title.lower())-1].isspace():
                            if line.startswith('$'):
                                pass
                            elif line.startswith('>>>'):
                                pass
                            else:
                                raise Exception('Help section contains non-matching title in line: {}'.format(line))

    @staticmethod
    def validate_help_headers(help_str):
        if '## About' not in help_str:
            raise Exception("Help section is missing header: ## About")
        if '## Actions' not in help_str:
            raise Exception("Help section is missing header: ## Actions")
        if '## Triggers' not in help_str:
            raise Exception("Help section is missing header: ## Triggers")
        if '## Connection' not in help_str:
            raise Exception("Help section is missing header: ## Connection")
        if '## Troubleshooting' not in help_str:
            raise Exception("Help section is missing header: ## Troubleshooting")
        if '## Workflows' not in help_str:
            raise Exception("Help section is missing header: ## Workflows")
        if '## Versions' not in help_str:
            raise Exception("Help section is missing header: ## Versions")
        if '## References' not in help_str:
            raise Exception("Help section is missing header: ## References")

    def validate(self, spec):
        HelpValidator.validate_help_exists(spec.spec_dictionary())
        HelpValidator.validate_help_headers(spec.raw_help())
        HelpValidator.validate_version_history(spec.raw_help())
        HelpValidator.validate_same_plugin_title(spec.spec_dictionary(), spec.raw_help())
        HelpValidator.validate_same_actions_title(spec.spec_dictionary(), spec.raw_help())
        HelpValidator.validate_title_spelling(spec.spec_dictionary(), spec.raw_help())
