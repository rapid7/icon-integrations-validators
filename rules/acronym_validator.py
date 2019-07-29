from .validator import KomandPluginValidator


class AcronymValidator(KomandPluginValidator):

    acronyms = ['API', 'AWS', 'BCC', 'BIOS', 'CI', 'CLI', 'CPU', 'CRLF', 'CSV', 'FTP', 'GMT', 'GNU', 'GPU', 'HTML', 'HTTP', 'HTTPS', 'ID', 'IMAP', 'IO', 'IP', 'IP2', 'ISO', 'JPEG', 'JQ', 'JQL', 'JSON', 'LAN', 'MD5', 'MIME', 'PDF', 'PHP', 'PID', 'PNG', 'REST', 'RPM', 'RRS', 'RSA', 'SDK', 'SHA', 'SHA1', 'SHASUM', 'SHA1SUM', 'SHA256', 'SHA512', 'SMS', 'SMTP', 'SQL', 'SSH', 'SSL', 'TCP', 'UDP', 'UI', 'UID', 'URI', 'URL', 'UUID', 'VPN', 'XML', 'ZIP']

    @staticmethod
    def validate_acronym(s):
        if s.upper() in AcronymValidator.acronyms:
            for c in s:
                if c.isalpha() and not c.isupper():
                    return True
        return False

    def validate(self, spec):
        bad = []
        sections = [ 'title', 'description', 'help']
        for section in sections: # check title/desc of spec and whole of help.md
            if section is 'help':
                content = spec.raw_help().split()
            else:
                content = spec.spec_dictionary()[section].split()
            for word in content:
                if AcronymValidator.validate_acronym(word):
                    bad.append(word)
        

        if len(bad) > 0:
            raise Exception(f'Acronyms found in plugin.spec.yaml or help.md that should be capitalized: ', {str(bad)})
