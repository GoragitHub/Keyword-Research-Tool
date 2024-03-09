# https://developers.google.com/google-ads/api/docs/best-practices/test-accounts
"""This example generates keyword ideas from a list of seed keywords."""
import sys
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

_DEFAULT_LOCATION_IDS = ["1023191"]  # location ID for New York, NY
_DEFAULT_LANGUAGE_ID = "1000"  # language ID for English

def main():
    googleads_client = GoogleAdsClient.load_from_storage(path="google-ads.yaml", version="v15")
    customer_id = "6697562731"
    location_ids = _DEFAULT_LOCATION_IDS
    language_id = _DEFAULT_LANGUAGE_ID
    keyword_texts = ["python", "java", "javascripts", "keywords"]
    page_url = "https://codewithharry.com"

    try:
        main_logic(                           #https://developers.google.com/google-ads/api/docs/start
            googleads_client,
            customer_id,
            location_ids,
            language_id,
            keyword_texts,
            page_url,
        )
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)

def main_logic(
    client, customer_id, location_ids, language_id, keyword_texts, page_url
):
    keyword_plan_idea_service = client.get_service("KeywordPlanIdeaService")
    keyword_competition_level_enum = (
        client.enums.KeywordPlanCompetitionLevelEnum
    )
    keyword_plan_network = (
        client.enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH_AND_PARTNERS
    )
    location_rns = map_locations_ids_to_resource_names(client, location_ids)
    language_rn = client.get_service("GoogleAdsService").language_constant_path(
        language_id
    )

    if not (keyword_texts or page_url):
        raise ValueError(
            "At least one of keywords or page URL is required, "
            "but neither was specified."
        )

    request = client.get_type("GenerateKeywordIdeasRequest")
    request.customer_id = customer_id
    request.language = language_rn
    request.geo_target_constants = location_rns
    request.include_adult_keywords = False
    request.keyword_plan_network = keyword_plan_network

    if not keyword_texts and page_url:
        request.url_seed.url = page_url

    if keyword_texts and not page_url:
        request.keyword_seed.keywords.extend(keyword_texts)

    if keyword_texts and page_url:
        request.keyword_and_url_seed.url = page_url
        request.keyword_and_url_seed.keywords.extend(keyword_texts)

    keyword_ideas = keyword_plan_idea_service.generate_keyword_ideas(
        request=request
    )

    for idea in keyword_ideas:
        competition_value = idea.keyword_idea_metrics.competition.name
        print(
            f'Keyword idea text "{idea.text}" has '
            f'"{idea.keyword_idea_metrics.avg_monthly_searches}" '
            f'average monthly searches and "{competition_value}" '
            "competition.\n"
        )

def map_locations_ids_to_resource_names(client, location_ids):
    build_resource_name = client.get_service(
        "GeoTargetConstantService"
    ).geo_target_constant_path
    return [build_resource_name(location_id) for location_id in location_ids]

if __name__ == "__main__":
    main()

