from icon_plugin_spec.plugin_spec import KomandPluginSpec

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class UseCaseValidator(KomandPluginValidator):
    use_case_ids = [
        "data_enrichment",
        "alerting_and_notifications",
        "application_management",
        "devops",
        "asset_inventory",
        "cloud_security",
        "credential_management",
        "data_utility",
        "offensive_security",
        "remediation_management",
        "reporting_and_analytics",
        "threat_detection_and_response",
        "user_management",
        "vulnerability_management"
    ]

    @staticmethod
    def validate_use_cases(use_cases: [str]) -> [str]:
        invalid_use_cases = []
        for use_case in use_cases:
            if use_case not in UseCaseValidator.use_case_ids:
                invalid_use_cases.append(use_case)
        return invalid_use_cases

    def validate(self, spec: KomandPluginSpec):
        try:
            result = UseCaseValidator.validate_use_cases(spec.spec_dictionary()["hub_tags"]["use_cases"])
            if len(result):
                err = ", ".join(result)
                raise ValidationException(f"Invalid use cases: {err}.")
        except KeyError:
            raise ValidationException("Missing required field 'use_cases' in key 'hub_tags'.")
