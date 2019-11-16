from .validator import KomandPluginValidator
from icon_plugin_spec.plugin_spec import KomandPluginSpec


class UseCaseValidator(KomandPluginValidator):
    use_case_ids = [
        "alert_enrichment",
        "alerting_and_notifications",
        "application_management",
        "application_security",
        "asset_containment",
        "asset_inventory",
        "automation_and_orchestration",
        "chat_ops",
        "ci_cd",
        "container_and_cloud_security",
        "credential_management",
        "data_aggregation",
        "data_ingestion",
        "data_utility",
        "external_enrichment",
        "investigations",
        "log_search",
        "network_containment",
        "patch_management",
        "penetration_testing",
        "phishing_investigations",
        "policy_management",
        "remediation_prioritization",
        "remediation_ticketing",
        "reporting_and_analytics",
        "siem",
        "soar",
        "soc_automation",
        "threat_hunting",
        "threat_intel",
        "threat_detection_and_response",
        "user_management",
        "vulnerability_management",
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
                err = ', '.join(result)
                raise Exception(f"Invalid use cases: {err}")
        except KeyError:
            raise Exception("Missing required field 'use_cases' in key 'hub_tags'")
