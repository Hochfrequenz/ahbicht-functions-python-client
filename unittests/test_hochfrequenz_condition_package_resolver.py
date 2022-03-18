"""
Tests the HochfrequenzPackageResolver in special the get_condition_mapping function
"""
import asyncio
import datetime

import pytest  # type:ignore[import]
from ahbicht.mapping_results import ConditionKeyConditionTextMapping

# https://github.com/pnuckowski/aioresponses/issues/206
from aioresponses import CallbackResult, aioresponses  # type:ignore[import]
from maus.edifact import EdifactFormat, EdifactFormatVersion

from ahbichtfunctionsclient.hochfrequenzpackageresolver import HochfrequenzPackageResolver

# import src.ahbichtfunctionsclient.HochfrequenzPackageResolver as hpr
# from ahbichtfunctionsclient import HochfrequenzPackageResolver
# import src.ahbichtfunctionsclient.hochfrequenzpackageresolver as ahb
# import ahbichtfunctionsclient.hochfrequenzpackageresolver as ahb


pytestmark = pytest.mark.asyncio


class TestHochfrequenzPackageResolver:
    async def test_hochfrequenz_package_api_success(self):
        package_resolver = HochfrequenzPackageResolver(api_url="https://test.inv")
        package_resolver.edifact_format = EdifactFormat.UTILMD
        package_resolver.edifact_format_version = EdifactFormatVersion.FV2204
        with aioresponses() as mocked_server:
            mocked_server.get(
                "https://test.inv/FV2204/UTILMD/146",
                payload={
                    "condition_text": "[145] Wenn SG10 CCI+Z31++ZA8 (bereits ausg. Aggreg.verantw. in MaBiS: NB)  vor- handen",
                    "condition_key": "146",
                    "edifact_format": "UTILMD",
                },
            )
            actual = await package_resolver.get_condition_mapping("146")
            assert actual == ConditionKeyConditionTextMapping(
                edifact_format=EdifactFormat.UTILMD,
                condition_key="146",
                condition_text="[145] Wenn SG10 CCI+Z31++ZA8 (bereits ausg. Aggreg.verantw. in MaBiS: NB)  vor- handen",
            )

    async def test_hochfrequenz_package_api_failure(self):
        package_resolver = HochfrequenzPackageResolver(api_url="https://test.inv")
        package_resolver.edifact_format = EdifactFormat.UTILMD
        package_resolver.edifact_format_version = EdifactFormatVersion.FV2204

        def simulate_error(url, **kwargs):
            return CallbackResult(status=400, payload={"it is not": "important what's here, just that you had to wait"})

        with aioresponses() as mocked_server:
            mocked_server.get(url="https://test.inv/FV2204/UTILMD/406", callback=simulate_error, repeat=5)
            actual = await package_resolver.get_condition_mapping("406")
            assert actual == ConditionKeyConditionTextMapping(
                # see the documentation: if the package could not be resolved, you'll get a None package_expression
                # but the PackageKeyConditionExpressionMapping itself is _not_ None
                edifact_format=EdifactFormat.UTILMD,
                condition_key="406",
                condition_text=None,
            )

    async def test_async_behaviour(self):
        package_resolver = HochfrequenzPackageResolver(api_url="https://test.inv")
        package_resolver.edifact_format = EdifactFormat.UTILMD
        package_resolver.edifact_format_version = EdifactFormatVersion.FV2204

        async def wait_some_time(url, **kwargs):
            await asyncio.sleep(1)
            return CallbackResult(status=400, payload={"it is not": "important what's here, just that you had to wait"})

        with aioresponses() as mocked_server:
            tasks = []
            for x in range(1, 6):
                mocked_server.get(url=f"https://test.inv/FV2204/UTILMD/{x}", callback=wait_some_time)
                tasks.append(package_resolver.get_condition_mapping(f"{x}"))
            start_time = datetime.datetime.now()
            actual = await asyncio.gather(*tasks)
            end_time = datetime.datetime.now()
            assert (end_time - start_time).total_seconds() < 2  # meaning: significantly smaller than 5
            assert len(actual) == 5

    async def test_async_behaviour_against_real_api(self):
        """
        This test is skipped by default because it calls a real API. Asserting on real APIs is not really an unittest.
        Comment the skip to test locally (e.g. to create a concurrency diagram in local tests)
        """
        pytest.skip("This test uses the real API, we don't want to call eat in each CI run.")  # comment for local tests
        package_resolver = HochfrequenzPackageResolver()
        package_resolver.edifact_format = EdifactFormat.UTILMD
        package_resolver.edifact_format_version = EdifactFormatVersion.FV2204
        tasks = [package_resolver.get_condition_mapping(f"{x}") for x in range(100)]
        results = await asyncio.gather(*tasks)
        for result in results:
            assert isinstance(result, ConditionKeyConditionTextMapping)
