from .validator import KomandPluginValidator


class VersionValidator(KomandPluginValidator):

    @staticmethod
    def validate_version(version):
        if version.endswith('.'):
            raise Exception('Version ends with period when it should not.')
        if any(c.isalpha() for c in version):
            raise Exception('Version contains alphabet when it should not.')
        if "." not in version:
            raise Exception('Version should be separated by decimal point.')
        if " " in version:
            raise Exception('Version should not contain spaces.')
        if "_" in version:
            raise Exception('Version should not contain underscores.')
        if len(version.split('.')) != 3:
            raise Exception('Version should be of semver format: x.x.x.')
        if version.startswith("0"):
            raise Exception('Version should begin at an initial version of 1.0.0 to comply with semver.')

    @staticmethod
    def validate_version_quotes(spec):
        '''Requires raw spec to see the quotes'''
        for line in spec.splitlines():
            if line.startswith('version:'):
                val = line[line.find(' ')+1:]
                if '"' in val:
                    raise Exception('Version is surrounded by or contains quotes when it should not')
                if "'" in val:
                    raise Exception('Version is surrounded by or contains quotes when it should not')

    @staticmethod
    def validate_plugin_version(spec):
        if 'version' not in spec.spec_dictionary():
            raise Exception('Plugin version is missing')
        if not isinstance(spec.spec_dictionary()['version'], str):
            raise Exception('Plugin version does not contain a string')

    def validate(self, spec):
        VersionValidator.validate_plugin_version(spec)
        VersionValidator.validate_version(spec.spec_dictionary()['version'])
        VersionValidator.validate_version_quotes(spec.raw_spec())
