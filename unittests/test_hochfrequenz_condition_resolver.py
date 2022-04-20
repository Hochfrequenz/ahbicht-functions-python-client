"""
Tests the HochfrequenzConditionResolver
"""
import asyncio
import datetime

import pytest  # type:ignore[import]
from ahbicht.mapping_results import ConditionKeyConditionTextMapping

# https://github.com/pnuckowski/aioresponses/issues/206
from aioresponses import CallbackResult, aioresponses  # type:ignore[import]
from maus.edifact import EdifactFormat, EdifactFormatVersion

from ahbichtfunctionsclient import HochfrequenzConditionResolver

pytestmark = pytest.mark.asyncio


class TestHochfrequenzConditionResolver:
    async def test_hochfrequenz_condition_api_success(self):
        condition_resolver = HochfrequenzConditionResolver(
            edifact_format_version=EdifactFormatVersion.FV2204,
            edifact_format=EdifactFormat.UTILMD,
            api_url="https://test.inv",
        )
        with aioresponses() as mocked_server:
            mocked_server.get(
                "https://test.inv/FV2204/UTILMD/123",
                payload={
                    "condition_text": "Wenn Foo",
                    "condition_key": "123",
                    "edifact_format": "UTILMD",
                },
            )
            actual = await condition_resolver.get_condition_text("123")
            assert actual == ConditionKeyConditionTextMapping(
                edifact_format=EdifactFormat.UTILMD,
                condition_key="123",
                condition_text="Wenn Foo",
            )

    async def test_hochfrequenz_condition_api_failure(self):
        condition_resolver = HochfrequenzConditionResolver(
            edifact_format_version=EdifactFormatVersion.FV2204,
            edifact_format=EdifactFormat.UTILMD,
            api_url="https://test.inv",
        )

        def simulate_error(url, **kwargs):
            return CallbackResult(status=400, payload={"it is not": "important what's here, just that you had to wait"})

        with aioresponses() as mocked_server:
            mocked_server.get(url="https://test.inv/FV2204/UTILMD/001", callback=simulate_error)
            actual = await condition_resolver.get_condition_text("001")
            assert actual == ConditionKeyConditionTextMapping(
                # see the documentation: if the condition could not be resolved, you'll get a None condition_text
                # but the ConditionKeyConditionTextMapping itself is _not_ None
                edifact_format=EdifactFormat.UTILMD,
                condition_key="001",
                condition_text=None,
            )

    async def test_async_behaviour(self):
        condition_resolver = HochfrequenzConditionResolver(
            edifact_format_version=EdifactFormatVersion.FV2204,
            edifact_format=EdifactFormat.UTILMD,
            api_url="https://test.inv",
        )

        async def wait_some_time(url, **kwargs):
            await asyncio.sleep(1)
            return CallbackResult(status=400, payload={"it is not": "important what's here, just that you had to wait"})

        with aioresponses() as mocked_server:
            tasks = []
            for x in range(1, 6):
                mocked_server.get(url=f"https://test.inv/FV2204/UTILMD/{x}", callback=wait_some_time)
                tasks.append(condition_resolver.get_condition_text(f"{x}"))
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
        condition_resolver = HochfrequenzConditionResolver(
            edifact_format_version=EdifactFormatVersion.FV2204,
            edifact_format=EdifactFormat.UTILMD,
            api_url="https://test.inv",
        )
        tasks = [condition_resolver.get_condition_text(f"{x}") for x in range(100)]
        results = await asyncio.gather(*tasks)
        for result in results:
            assert isinstance(result, ConditionKeyConditionTextMapping)
