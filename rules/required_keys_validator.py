from .validator import KomandPluginValidator


class RequiredKeysValidator(KomandPluginValidator):

    missing_key_message = {
        'plugin_spec_version': 'Specifies the version of the spec. Current version is v1',
        'name': 'Name of the plugin, refers to the docker image name. Should be lower case',
        'title': 'Formatted name',
        'description': 'One sentence description',
        'version': 'Semantic version of the plugin',
        'vendor': 'Plugin vendor, refers to the docker image repository and komand marketplace user',
        'status': 'List of development statuses to apply to the plugin',
        'tags': 'List of tags to apply to the plugin',
    }

    def validate(self, spec):
        for required_key, message in self.missing_key_message.items():
            if required_key not in spec.spec_dictionary():
                raise Exception('Plugin spec is missing key "%s": %s' % (required_key, message))
