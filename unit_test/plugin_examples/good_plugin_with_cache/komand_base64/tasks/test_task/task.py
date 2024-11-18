import insightconnect_plugin_runtime
from .schema import TestTaskInput, TestTaskOutput, TestTaskState, Input, Output, Component
# Custom imports below


class TestTask(insightconnect_plugin_runtime.Task):

    def __init__(self):
        super(self.__class__, self).__init__(
                name='test_task',
                description=Component.DESCRIPTION,
                input=TestTaskInput(),
                output=TestTaskOutput(),
                state=TestTaskState())

    def run(self, params={}):
        # TODO: Implement run function
        return {}, {}
