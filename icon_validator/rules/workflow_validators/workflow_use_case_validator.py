import requests
from icon_plugin_spec.plugin_spec import KomandPluginSpec

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class WorkflowUseCaseValidator(KomandPluginValidator):
    @staticmethod
    def get_approved_usecase_tags(response_json: dict) -> [str]:
        approved_usecases = []
        for result in response_json["results"]:
            if result["type"] == "usecase":
                approved_usecases.append(result["name"])

        return approved_usecases

    @staticmethod
    def get_approved_usecase_tags_with_paging() -> [str]:
        approved_usecases = []
        params = {
            "first": 1000,
            "types": "usecase"
        }
        has_next = True
        while has_next:
            response = requests.get(url=f"https://extensions-api.rapid7.com/v2/public/tags", params=params)
            response_json = response.json()
            approved_usecases.extend(WorkflowUseCaseValidator.get_approved_usecase_tags(response_json))
            if not response_json["pageInfo"]["hasNextPage"]:
                has_next = False

            params["after"] = response_json['pageInfo']['endCursor']

        return approved_usecases

    @staticmethod
    def validate_use_case_exists(spec: KomandPluginSpec):
        try:
            use_cases = spec.spec_dictionary()["hub_tags"]["use_cases"]
            if not use_cases:
                raise ValidationException("Empty required field 'use_cases' in key 'hub_tags'.")
        except KeyError:
            raise ValidationException("Missing required field 'use_cases' in key 'hub_tags'.")

    @staticmethod
    def validate_use_cases(use_cases: [str]) -> [str]:
        invalid_use_cases = []
        approved_use_cases = WorkflowUseCaseValidator.get_approved_usecase_tags_with_paging()
        for use_case in use_cases:
            if use_case not in approved_use_cases:
                invalid_use_cases.append(use_case)

        if len(invalid_use_cases):
            err = ", ".join(invalid_use_cases)
            raise ValidationException(
                f"Invalid use cases: {err}. "
                "Update the use_cases array with one or more of the following valid use cases: "
                f"{approved_use_cases}"
            )

    @staticmethod
    def validate_use_case_in_keywords(keywords: list) -> None:
        if not keywords:
            return

        invalid_keywords = []
        approved_use_cases = WorkflowUseCaseValidator.get_approved_usecase_tags_with_paging()
        for keyword in keywords:
            if keyword in approved_use_cases:
                invalid_keywords.append(keyword)

        if len(invalid_keywords):
            bad_keywords = ", ".join(invalid_keywords)
            raise ValidationException("The keywords array contains reserved use_cases, "
                                      f"please remove the following from the list: {bad_keywords}")

    def validate(self, spec: KomandPluginSpec):
        WorkflowUseCaseValidator.validate_use_case_exists(spec)
        WorkflowUseCaseValidator.validate_use_cases(spec.spec_dictionary()["hub_tags"]["use_cases"])
        WorkflowUseCaseValidator.validate_use_case_in_keywords(spec.spec_dictionary()["hub_tags"].get("keywords"))
