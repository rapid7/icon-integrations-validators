from .validator import KomandPluginValidator


class AcronymValidator(KomandPluginValidator):

    acronyms = [
        'ACL', 'API', 'AMI', 'ANC', 'ANS', 'ARN', 'ASCII', 'ASN', 'AV', 'AWS',
        'BCC', 'BGP', 'BIOS',
        'CC', 'CEF', 'CI', 'CIDR', 'CIF', 'CLI', 'CNAME', 'CORS', 'CPU', 'CRLF', 'CRM', 'CSV', 'CVE', 'CVSS',
        'DB', 'DBMS', 'DHCP', 'DMARC', 'DNS', 
        'EDR', 'EML',
        'FIFO', 'FTP', 'FQDN',
        'GID', 'GUID', 'GMT', 'GNU', 'GPU',
        'HIBP', 'HIDS', 'HTML', 'HTTP', 'HTTPS',
        'IAM', 'IANA', 'IBM', 'ICANN', 'ICMP', 'ICIS', 'ID', 'IDNA', 'IMAP', 'IO', 'IOC', 'IP', 'IP2', 'IPA', 'ISE', 'ISO', 'ISP', 'ITIL',
        'JPEG', 'JQ', 'JQL', 'JSON', 'JWT',
        'KML', 'KMS',
        'LAN', 'LDAP',
        'MAC', 'MD5', 'MFA', 'MIME', 'MISP', 'MITRE', 'MIT', 'MHR', 'MSI', 'MSSQL', 'MX',
        'NFS', 'NOERROR', 'NTLM', 'NXDOMAIN',
        'OSSEC', 'OSI', 'OTRS',
        'PCI', 'PCAP', 'PDF', 'PEM', 'PHP', 'PKI', 'PID', 'PNG',
        'RAR', 'RBAC', 'REST', 'RFC', 'RPC', 'RPM', 'RPZ', 'RRS', 'RSA', 'RSS',
        'SAML', 'SCCM', 'SDK', 'SHA', 'SHA1', 'SHASUM', 'SHA1SUM', 'SHA256', 'SHA512', 'SIEM', 'SLA', 'SMB', 'SMS', 'SMTP', 'SPF', 'SQL', 'SNMP', 'SNS', 'SRV', 'SQS', 'SSH', 'SSDEEP', 'SSID', 'STIX', 'SSL', 'SUID',
        'TCP', 'TSV', 'TLD', 'TLP', 'TLS', 'TTL', 'TTP', 'TXT',
        'UBA', 'UDP', 'UI', 'UID', 'URI', 'URL', 'UTC', 'UUID', 'VPN',
        'VBA', 'VM', 'VPC', 'VNC', 'VT', 'VTI',
        'XML',
        'WAF', 'WHOIS', 'WINDOMAIN',
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
        if 'description' in section:
            AcronymValidator.validate_line(section['description'].split(), bad)
        if 'title' in section:
            AcronymValidator.validate_line(section['title'].split(), bad)
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
