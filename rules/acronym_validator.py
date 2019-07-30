from .validator import KomandPluginValidator


class AcronymValidator(KomandPluginValidator):

    acronyms = [
        'ACL', 'API', 'ANC', 'ARN', 'ASCII', 'ASN', 'AV', 'AWS',
        'BCC', 'BIOS',
        'CEF', 'CI', 'CIDR', 'CLI', 'CNAME', 'CPU', 'CRLF', 'CSV', 'CVE', 'CVSS',
        'DNS', 'DBMS',
        'EDR', 'EML',
        'FIFO', 'FTP',
        'GMT', 'GNU', 'GPU',
        'HIDS', 'HTML', 'HTTP', 'HTTPS',
        'IAM', 'IBM', 'ICANN', 'ID', 'IMAP', 'IO', 'IOC', 'IP', 'IP2', 'IPA', 'ISO',
        'JPEG', 'JQ', 'JQL', 'JSON',
        'KML', 'KMS',
        'LAN', 'LDAP',
        'MAC', 'MD5', 'MFA', 'MIME', 'MISP',
        'NFS', 'NOERROR', 'NTLM', 'NXDOMAIN',
        'OSSEC', 'OTRS',
        'PCI', 'PCAP', 'PDF', 'PHP', 'PID', 'PNG',
        'RAR', 'REST', 'RFC', 'RPM', 'RRS', 'RSA', 'RSS',
        'SAML', 'SCCM', 'SDK', 'SHA', 'SHA1', 'SHASUM', 'SHA1SUM', 'SHA256', 'SHA512', 'SLA', 'SMB', 'SMS', 'SMTP', 'SPAM', 'SQL', 'SNMP', 'SNS', 'SRV', 'SQS', 'SSH', 'SSDEEP', 'STIX', 'SSL',
        'TCP', 'TSV', 'TLP', 'TLS', 'TTL',
        'UDP', 'UI', 'UID', 'URI', 'URL', 'UTC', 'UUID', 'VPN',
        'VM', 'VTI',
        'XML',
        'WHOIS', 'WINDOMAIN',
        'ZIP',
    ]


    @staticmethod
    def validate_acronym(s):
        if s.upper() in AcronymValidator.acronyms:
            for c in s:
                if c.isalpha() and not c.isupper():
                    return True
        return False

    @staticmethod
    def validate_subsection(section, bad):
        if type(section) is not dict:
            return
        try:
            desc = section['description']
            AcronymValidator.validate_line(desc.split(), bad)
            # items in spec sometimes have a desc but no title
            title = section['title']
            AcronymValidator.validate_line(title.split(), bad)
        except KeyError:
            pass
        for subsection in section:
                AcronymValidator.validate_subsection(section[subsection], bad)

    @staticmethod
    def validate_line(content, bad):
        for word in content:
            if AcronymValidator.validate_acronym(word):
                bad.append(word)

    def validate(self, spec):
        bad = []
        sections = [ 'title', 'description', 'help']
        for section in sections: # check title/desc of spec and whole of help.md
            if section is 'help':
                content = spec.raw_help().split()
            else:
                content = spec.spec_dictionary()[section].split()
            AcronymValidator.validate_line(content, bad)

        subsections = ['actions', 'triggers', 'connection', 'types']
        for section in subsections:
            if section in spec.spec_dictionary():
                AcronymValidator.validate_subsection(spec.spec_dictionary()[section], bad)


        if len(bad) > 0:
            raise Exception(f'Acronyms found in plugin.spec.yaml or help.md that should be capitalized: ', {str(bad)})
