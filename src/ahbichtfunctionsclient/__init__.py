"""
Contains two asynchronous Resolvers that, by default, use the Hochfrequenz API to retrieve a
condition expression or a condition text for a given package/condition key.


NOTE that both resolvers require an internet connection to work and the Hochfrequenz API to be up and running.
Consider using these resolvers to retrieve package/condition information once and then dump them into something
fast and stable like e.g. a JSON file, a database or feed its results into a hardcoded package resolver
once on startup. Relying on external web services is prone to be a bottleneck for your application.

"""
import aiohttp
from ahbicht.expressions.package_expansion import PackageResolver
from ahbicht.mapping_results import (
    ConditionKeyConditionTextMapping,
    ConditionKeyConditionTextMappingSchema,
    PackageKeyConditionExpressionMapping,
    PackageKeyConditionExpressionMappingSchema,
)
from maus.edifact import EdifactFormat, EdifactFormatVersion


# pylint: disable=too-few-public-methods
class HochfrequenzPackageResolver(PackageResolver):
    """
    A package resolver that uses a REST API (by Hochfrequenz) to retrieve a condition expression for a given package
    key.
    """

    _hochfrequenz_base_uri = "https://ahbicht.azurewebsites.net/api/ResolvePackageConditionExpression/"

    def __init__(self, api_url=_hochfrequenz_base_uri):
        """
        initializes the package resolver; you may overwrite the base url (e.g. for a test-system)
        """
        self.api_url = api_url

    async def get_condition_expression(self, package_key: str) -> PackageKeyConditionExpressionMapping:
        request_url = f"{self.api_url}/{self.edifact_format_version}/{self.edifact_format}/{package_key}"
        async with aiohttp.ClientSession() as session:
            async with session.get(request_url) as response:
                print("Status:", response.status)
                if response.status != 200:
                    return PackageKeyConditionExpressionMapping(
                        package_key=package_key, package_expression=None, edifact_format=self.edifact_format
                    )
                response_body = await response.json()
                result = PackageKeyConditionExpressionMappingSchema().load(response_body)
                return result


# pylint: disable=too-few-public-methods
class HochfrequenzConditionResolver:
    """
    Uses a REST API (by Hochfrequenz) to retrieve a condition text for a given condition key.
    """

    _hochfrequenz_base_condition_uri = "https://ahbicht.azurewebsites.net/api/ResolveConditionText/"

    def __init__(
        self,
        edifact_format_version: EdifactFormatVersion,
        edifact_format: EdifactFormat,
        api_url=_hochfrequenz_base_condition_uri,
    ):
        """
        initializes the condition resolver and collects the edifact format as well as the version of the format.
        """
        self.api_url = api_url
        self.edifact_format = edifact_format
        self.edifact_format_version = edifact_format_version

    async def get_condition_text(self, condition_key: str) -> ConditionKeyConditionTextMapping:
        """
        :param condition_key:
        :return: ConditionKeyConditionTextMapping
        """
        request_url = f"{self.api_url}/{self.edifact_format_version}/{self.edifact_format}/{condition_key}"
        async with aiohttp.ClientSession() as session:
            async with session.get(request_url) as response:
                if response.status != 200:
                    return ConditionKeyConditionTextMapping(
                        condition_key=condition_key, condition_text=None, edifact_format=self.edifact_format
                    )
                response_body = await response.json()
                result = ConditionKeyConditionTextMappingSchema().load(response_body)
                return result
