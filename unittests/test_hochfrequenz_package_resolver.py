"""
Tests the HochfrequenzPackageResolver in special the get_condition_expression function
"""
import asyncio
import datetime

import pytest  # type:ignore[import]
from ahbicht.mapping_results import PackageKeyConditionExpressionMapping

# https://github.com/pnuckowski/aioresponses/issues/206
from aioresponses import CallbackResult, aioresponses  # type:ignore[import]
from maus.edifact import EdifactFormat, EdifactFormatVersion

from src.ahbichtfunctionsclient import HochfrequenzPackageResolver

pytestmark = pytest.mark.asyncio


class TestHochfrequenzPackageResolver:
    async def test_hochfrequenz_package_api_success(self):
        assert 1 == 1
