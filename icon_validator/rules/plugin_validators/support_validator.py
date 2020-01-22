from icon_validator.rules.validator import KomandPluginValidator


class SupportValidator(KomandPluginValidator):

    @staticmethod
    def validate_support(support):
        lsupport = support.lower()
        if lsupport == "komand":
            raise Exception("Support 'komand' not allowed. It's likely you meant 'rapid7'.")
        if support.endswith("."):
            raise Exception("Support ends with period when it should not.")
        if not support[0].islower():
            raise Exception("Support starts with a capital letter when it should not.")
        if " " in support:
            raise Exception("Support should be separated by underscores, not spaces.")

    @staticmethod
    def validate_support_quotes(spec):
        """Requires raw spec to see the quotes"""
        for line in spec.splitlines():
            if line.startswith("support:"):
                val = line[line.find(" ") + 1:]
                if '"' in val or "'" in val:
                    raise Exception("Support is surrounded by or contains quotes when it should not.")

    @staticmethod
    def validate_plugin_support(spec):
        if "support" not in spec.spec_dictionary():
            raise Exception("Plugin supporter is missing.")
        if not isinstance(spec.spec_dictionary()["support"], str):
            raise Exception("Plugin supporter does not contain a string.")

    def validate(self, spec):
        SupportValidator.validate_plugin_support(spec)
        SupportValidator.validate_support(spec.spec_dictionary()["support"])
        SupportValidator.validate_support_quotes(spec.raw_spec())
