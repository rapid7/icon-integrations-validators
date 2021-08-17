import unittest
from icon_validator.validate import validate
from icon_validator.rules.template_validators.template_id_validator import(
    TemplateIDValidator,
)

class TestTemplateValidator(unittest.TestCase):
    def test_workflow_id_missing_validator(self):
        # Test good workflow. This should pass all validation
        directory_to_test = "template_examples/id_tests"
        file_to_test = "workflow.spec.yaml"
        result = validate(
            directory=directory_to_test,
            spec_file_name=file_to_test,
            fail_fast=False,
            run_all=False,
            validators=[TemplateIDValidator]
        )
        self.assertFalse(result)