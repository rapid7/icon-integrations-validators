import unittest
from icon_validator.validate import validate
from icon_validator.rules.template_validators.template_id_validator import(
    TemplateIDValidator,
)

class TestTemplateValidator(unittest.TestCase): # this test is failing. add in id attribute to make a good test alidator "TemplateIDValidator" failed!
	# Cause: Template Validator: Template missing ID

    def test_workflow_validator_good(self):
        # Test good workflow. This should pass all validation
        directory_to_test = "template_examples/id_tests/good"
        file_to_test = "workflow.spec.yaml"
        result = validate(
            directory=directory_to_test,
            spec_file_name=file_to_test,
            fail_fast=False,
            run_all=False,
            validators=[TemplateIDValidator()]
        )
        self.assertEqual(result, 1)

    def test_workflow_validator_empty(self):
        # Test bad workflow. This should not pass
        directory_to_test = "template_examples/id_tests"
        file_to_test = "workflow.spec_empty.yaml"
        result = validate(
            directory=directory_to_test,
            spec_file_name=file_to_test,
            fail_fast=False,
            run_all=False,
            validators=[TemplateIDValidator()]
        )
        self.assertEqual(result, 0)

    def test_load_pydantic_model(self):
        directory_to_test = "template_examples/id_tests"
        file_to_test = "workflow.spec_empty.yaml"