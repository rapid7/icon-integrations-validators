from icon_plugin_spec.plugin_spec import KomandPluginSpec

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException
from icon_validator.styling import YELLOW
import requests


class UnapprovedKeywordsValidator(KomandPluginValidator):

    @staticmethod
    def get_approved_keywords_tags(response_json: dict) -> [str]:
        approved_keywords = []
        for result in response_json["results"]:
            if result["type"] == "keyword":
                approved_keywords.append(result["name"])

        return approved_keywords

    @staticmethod
    def get_approved_keywords_tags_with_paging() -> [str]:
        approved_keywords = []
        query = ""
        for i in range(0, 9999):
            response = requests.get(url=f"https://extensions-api.rapid7.com/v2/public/tags?first=1000&{query}")
            response_json = response.json()
            approved_keywords.extend(UnapprovedKeywordsValidator.get_approved_keywords_tags(response_json))
            if not response_json["pageInfo"]["hasNextPage"]:
                break

            query = f"after={response_json['pageInfo']['endCursor']}"

        return approved_keywords

    @staticmethod
    def validate_keywords_exists(spec: KomandPluginSpec):
        try:
            keywords = spec.spec_dictionary()["hub_tags"]["keywords"]
            if not keywords or not len(keywords):
                raise ValidationException("Empty required field 'keywords' in key 'hub_tags'.")
        except KeyError:
            raise ValidationException("Missing required field 'keywords' in key 'hub_tags'.")

    @staticmethod
    def validate_keywords(keywords: [str]) -> [str]:
        invalid_keywords = []
        approved_keywords = UnapprovedKeywordsValidator.get_approved_keywords_tags_with_paging()
        for keyword in keywords:
            if keyword not in approved_keywords:
                invalid_keywords.append(keyword)

        if invalid_keywords:
            err = ", ".join(invalid_keywords)
            print(f"{YELLOW}WARNING: Unsupported keywords found: {err}. The following keywords will not be searchable by the Extension Library. Please remove or update the invalid keywords from the keywords array in the plugin.spec.yaml file.")

    def validate(self, spec: KomandPluginSpec):
        UnapprovedKeywordsValidator.validate_keywords_exists(spec)
        UnapprovedKeywordsValidator.validate_keywords(spec.spec_dictionary()["hub_tags"]["keywords"])
