from icon_validator.rules.validator import KomandPluginValidator


class WorkflowVendorValidator(KomandPluginValidator):

    @staticmethod
    def validate_vendor(vendor):
        lvendor = vendor.lower()
        if lvendor == 'komand':
            raise Exception("Vendor 'komand' not allowed. It's likely you meant 'rapid7'.")
        if vendor.endswith('.'):
            raise Exception('Vendor ends with period when it should not.')
        if not vendor[0].islower():
            raise Exception('Vendor starts with a capital letter when it should not.')
        if " " in vendor:
            raise Exception('Vendor should be separated by underscores, not spaces.')

    @staticmethod
    def validate_vendor_quotes(spec):
        '''Requires raw spec to see the quotes'''
        for line in spec.splitlines():
            if line.startswith('vendor:'):
                val = line[line.find(' ') + 1:]
                if '"' in val:
                    raise Exception('Vendor is surrounded by or contains quotes when it should not')
                if "'" in val:
                    raise Exception('Vendor is surrounded by or contains quotes when it should not')

    @staticmethod
    def validate_workflow_vendor(spec):
        if 'vendor' not in spec.spec_dictionary():
            raise Exception('Plugin vendor is missing')
        if not isinstance(spec.spec_dictionary()['vendor'], str):
            raise Exception('Plugin vendor does not contain a string')

    def validate(self, spec):
        WorkflowVendorValidator.validate_workflow_vendor(spec)
        WorkflowVendorValidator.validate_vendor(spec.spec_dictionary()['vendor'])
        WorkflowVendorValidator.validate_vendor_quotes(spec.raw_spec())
