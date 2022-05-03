import komand
from .schema import DecodeWithArrayInput, DecodeWithArrayOutput, Input, Output, Component
# Custom imports below


class DecodeWithArray(komand.Action):

    def __init__(self):
        super(self.__class__, self).__init__(
                name='decode_with_array',
                description=Component.DESCRIPTION,
                input=DecodeWithArrayInput(),
                output=DecodeWithArrayOutput())

    def run(self, params={}):
        # TODO: Implement run function
        return {}
