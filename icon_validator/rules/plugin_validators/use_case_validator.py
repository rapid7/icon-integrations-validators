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
    def validate_use_case_exists(spec: KomandPluginSpec):
        try:
            ext_library_section = spec.spec_dictionary().get("hub_tags") or spec.spec_dictionary().get("extension_library")
            use_cases = ext_library_section["use_cases"]
            if not use_cases or not len(use_cases):
                raise ValidationException("Empty required field 'use_cases' in key 'hub_tags'.")
        except KeyError:
            raise ValidationException("Missing required field 'use_cases' in key 'hub_tags'.")

    @staticmethod
    def validate_use_cases(use_cases: [str]) -> [str]:
        invalid_use_cases = []
        for use_case in use_cases:
            if use_case not in UseCaseValidator.use_case_ids:
                invalid_use_cases.append(use_case)

        if len(invalid_use_cases):
            err = ", ".join(invalid_use_cases)
            raise ValidationException(
                f"Invalid use cases: {err}. "
                "Update the use_cases array with one or more of the following valid use cases: "
                f"{UseCaseValidator.use_case_ids}"
            )

    @staticmethod
    def validate_use_case_in_keywords(keywords: list) -> None:
        if not keywords:
            return

        invalid_keywords = []
        for keyword in keywords:
            if keyword in UseCaseValidator.use_case_ids:
                invalid_keywords.append(keyword)

        if len(invalid_keywords):
            bad_keywords = ", ".join(invalid_keywords)
            raise ValidationException("The keywords array contains reserved use_cases, "
                                      f"please remove the following from the list: {bad_keywords}")

    def validate(self, spec: KomandPluginSpec):
        UseCaseValidator.validate_use_case_exists(spec)

        ext_library_section = spec.spec_dictionary().get("hub_tags") or spec.spec_dictionary().get("extension_library")

        UseCaseValidator.validate_use_cases(ext_library_section["use_cases"])
        UseCaseValidator.validate_use_case_in_keywords(ext_library_section.get("keywords"))
