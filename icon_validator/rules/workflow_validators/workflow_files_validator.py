import os

from icon_validator.rules.validator import KomandPluginValidator


class WorkflowFilesValidator(KomandPluginValidator):

    def validate(self, spec):
        d = spec.directory

        if not os.path.isfile('{}/{}'.format(d, 'workflow.spec.yaml')):
            raise Exception('File workflow.spec.yaml does not exist in: ', d)
        if not os.path.isfile('{}/{}'.format(d, 'help.md')):
            raise Exception('File help.md does not exist in: ', d)
        if not os.path.isfile('{}/{}'.format(d, 'extension.png')):
            raise Exception('File extension.png does not exist in: ', d)
        # TODO check for .icon file
