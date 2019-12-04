from unittest import TestCase
from icon_validator.validate import validate


class TestValidate(TestCase):
    def test_validate(self):
        # This assumes a standard environment where everything is
        # go/src/github.com/rapid7/<projects>
        directory_to_test = "../../insightconnect-plugins/microsoft_teams"
        file_to_test = "plugin.spec.yaml"
        validate(directory_to_test, file_to_test, False, True)
