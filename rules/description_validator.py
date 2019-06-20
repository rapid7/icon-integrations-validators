from .validator import KomandPluginValidator


class DescriptionValidator(KomandPluginValidator):

    @staticmethod
    def validate_description(description):
        if description.endswith('.'):
            raise Exception('Description ends with period when it should not')
        if description[0].islower():
            raise Exception('Description should not start with a lower case letter')
        if description[0].isspace():
            raise Exception('Description should not start with a whitespace character')

    @staticmethod
    def validate_actions(dict, dict_key):
        if dict_key in dict:
            DescriptionValidator.validate_dictionary(dict, dict_key)
            for key, value in dict[dict_key].items():
                if 'input' in value:
                    DescriptionValidator.validate_dictionary(value, 'input')
                if 'output' in value:
                    DescriptionValidator.validate_dictionary(value, 'output')

    @staticmethod
    def validate_dictionary(dict, dict_key):
        if dict_key in dict:
            if not dict[dict_key]:
                return

            for key, value in dict[dict_key].items():
                if 'description' not in value:
                    raise Exception('%s key "%s" is missing description field' % (dict_key, key))
                try:
                    DescriptionValidator.validate_description(value['description'])
                except Exception as e:
                    raise Exception('%s key "%s"\'s description ends with period when it should not'
                                    % (dict_key, key), e)

    @staticmethod
    def validate_plugin_description(spec):
        if 'description' not in spec.spec_dictionary():
            raise Exception('Plugin description is missing')

        try:
            DescriptionValidator.validate_description(spec.spec_dictionary()['description'])
        except Exception as e:
            raise Exception('Plugin description not valid', e)

    def validate(self, spec):
        DescriptionValidator.validate_plugin_description(spec)
        DescriptionValidator.validate_actions(spec.spec_dictionary(), 'actions')
        DescriptionValidator.validate_actions(spec.spec_dictionary(), 'triggers')

        # Types do not have descriptions but their keys do.
        # TODO: disabling type descriptions until better plugin autogen support exists (for swagger, wasdl, etc)
        # if 'types' in spec.spec_dictionary():
        #     for key, value in spec.spec_dictionary()['types'].items():
        #         DescriptionValidator.validate_dictionary(spec.spec_dictionary()['types'], key)
