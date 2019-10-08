from .validator import KomandPluginValidator


class RequiredValidator(KomandPluginValidator):

    @staticmethod
    def validate_required(required):
        if not isinstance(required, bool):
            raise Exception('required must be boolean')

    @staticmethod
    def validate_actions(dict, dict_key):
        if dict_key in dict:
            for key, value in dict[dict_key].items():
                if 'input' in value:
                    RequiredValidator.validate_dictionary(value, 'input')
                if 'output' in value:
                    RequiredValidator.validate_dictionary(value, 'output')

    @staticmethod
    def validate_connection(dict, dict_key):
        if dict_key in dict:
            RequiredValidator.validate_dictionary(dict, dict_key)

    @staticmethod
    def validate_dictionary(dict, dict_key):
        if dict_key in dict:
            if not dict[dict_key]:
                return

            for key, value in dict[dict_key].items():
                if 'required' not in value:
                    raise Exception('%s key "%s" is missing required field' % (dict_key, key))
                try:
                    RequiredValidator.validate_required(value['required'])
                except Exception as e:
                    raise Exception('%s key "%s"\'s required must be boolean'
                                    % (dict_key, key), e)

    def validate(self, spec):
        RequiredValidator.validate_actions(spec.spec_dictionary(), 'actions')
        RequiredValidator.validate_actions(spec.spec_dictionary(), 'triggers')
        RequiredValidator.validate_connection(spec.spec_dictionary(), 'connection')
