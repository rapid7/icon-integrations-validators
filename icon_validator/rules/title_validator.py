from .validator import KomandPluginValidator


class TitleValidator(KomandPluginValidator):

    @staticmethod
    def validate_title(title, plugin_title=False):
        if title.endswith('.'):
            raise Exception('Title ends with period when it should not')
        if title[0].islower() and not plugin_title:
            # This plugin title is OK: minFraud
            # This plugin title is OK: ifconfig.co
            raise Exception('Title should not start with a lower case letter')
        if title[0].isspace():
            raise Exception('Title should not start with a whitespace character')
        if len(title.split()) > 7:
            raise Exception('Title is too long, 6 words or less: contains ' + str(len(title.split())))
        for word in title.split():
            if not title.startswith(word):
                if 'The' == word:
                    raise Exception('Title contains a capitalized "The" when it should not')
                if 'By' == word and not title.endswith('By'):
                    # This is OK: Order By
                    # This is NOT OK: Search By String
                    raise Exception('Title contains a capitalized "By" when it should not')
                if 'From' == word:
                    raise Exception('Title contains a capitalized "From" when it should not')
                if 'A' == word:
                    raise Exception('Title contains a capitalized "A" when it should not')
                if 'An' == word:
                    raise Exception('Title contains a capitalized "An" when it should not')
                if 'Of' == word and not title.endswith('Of'):
                    # This is OK: Member Of
                    # This is NOT OK: Type Of String
                    raise Exception('Title contains a capitalized "Of" when it should not')

    @staticmethod
    def validate_actions(dict, dict_key):
        if dict_key in dict:
            TitleValidator.validate_dictionary(dict, dict_key)
            for key, value in dict[dict_key].items():
                if 'input' in value:
                    TitleValidator.validate_dictionary(value, 'input')
                if 'output' in value:
                    TitleValidator.validate_dictionary(value, 'output')

    @staticmethod
    def validate_dictionary(dict, dict_key):
        if dict_key in dict:
            if not dict[dict_key]:
                return

            for key, value in dict[dict_key].items():
                if 'name' in value:
                    raise Exception('Deprecated "name" key found when "title" should be used instead' % (dict_key, key))
                if 'title' in value:
                    try:
                        TitleValidator.validate_title(value['title'], plugin_title=False)
                    except Exception as e:
                        raise Exception('%s key "%s"\'s title ends with period when it should not'
                                        % (dict_key, key), e)

    @staticmethod
    def validate_plugin_title(spec):
        if 'title' not in spec.spec_dictionary():
            raise Exception('Plugin title is missing')

        try:
            TitleValidator.validate_title(spec.spec_dictionary()['title'], plugin_title=True)
        except Exception as e:
            raise Exception('Plugin title not valid', e)

    def validate(self, spec):
        TitleValidator.validate_plugin_title(spec)
        TitleValidator.validate_actions(spec.spec_dictionary(), 'actions')
        TitleValidator.validate_actions(spec.spec_dictionary(), 'triggers')
        TitleValidator.validate_actions(spec.spec_dictionary(), 'connection')
