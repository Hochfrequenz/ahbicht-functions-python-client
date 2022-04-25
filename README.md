# AHBicht Functions Python Client

![Unittests status badge](https://github.com/Hochfrequenz/ahbicht-functions-python-client/workflows/Unittests/badge.svg)
![Coverage status badge](https://github.com/Hochfrequenz/ahbicht-functions-python-client/workflows/Coverage/badge.svg)
![Linting status badge](https://github.com/Hochfrequenz/ahbicht-functions-python-client/workflows/Linting/badge.svg)
![Black status badge](https://github.com/Hochfrequenz/ahbicht-functions-python-client/workflows/Black/badge.svg)
![PyPi Status Badge](https://img.shields.io/pypi/v/ahbichtfunctionsclient)

This repository contains a lightweight client for an [AHBicht](https://github.com/Hochfrequenz/ahbicht) powered backend by Hochfrequenz.
It does not duplicate the core AHBicht logic but provides a [PackageResolver](https://ahbicht.readthedocs.io/en/latest/api/ahbicht.expressions.html?highlight=PackageResolver#ahbicht.expressions.package_expansion.PackageResolver)
that accesses a database (via a REST API) that stores [`PackageKeyConditionExpressionMapping`s](https://ahbicht.readthedocs.io/en/latest/api/ahbicht.html#ahbicht.mapping_results.PackageKeyConditionExpressionMapping).
The database is maintained by Hochfrequenz.

Internally this client uses and requires [aiohttp](https://docs.aiohttp.org/en/stable/).

## How to use the Client
- Install using pip:
```bash
pip install ahbichtfunctionsclient
```
Then call it

```python
import asyncio

from ahbicht.mapping_results import PackageKeyConditionExpressionMapping, ConditionKeyConditionTextMapping
from ahbichtfunctionsclient import HochfrequenzPackageResolver
from maus.edifact import EdifactFormat, EdifactFormatVersion


async def retrieve_package_key_condition_expression_mapping():
    # for a documentation about the purpose of a package resolver, you should read the ahbicht docs
    package_resolver = HochfrequenzPackageResolver(EdifactFormatVersion.FV2204, EdifactFormat.UTILMD)
    # the following data are just hardcoded to provide you a minimal working example
    package_mapping = await package_resolver.get_condition_expression("10P")  # this does an HTTP GET request
    assert isinstance(package_mapping, PackageKeyConditionExpressionMapping)  # the result is ahbicht compatible


async def retrieve_condition_key_condition_text_mapping():
    condition_resolver = HochfrequenzPackageResolver(EdifactFormatVersion.FV2204, EdifactFormat.UTILMD)
    # the following data are just hardcoded to provide you a minimal working example
    condition_mapping = await condition_resolver.get_condition_expression("56")  # this does an HTTP GET request
    assert isinstance(condition_mapping, ConditionKeyConditionTextMapping)  # the result is ahbicht compatible


async def minimal_working_example():
    await retrieve_condition_key_condition_text_mapping()
    await retrieve_package_key_condition_expression_mapping()


loop = asyncio.get_event_loop()
loop.run_until_complete(minimal_working_example())
```

## Production Readiness
This AHBicht client has a 100% code coverage, is linted, statically type checked and PEP561 compatible.
It relies on a Hochfrequenz API which is, as of today (2022-03-17), free to use.
Hochfrequenz does not give any guarantees regarding the stability or uptime of the API.
Also at one point it might require authorization.

## How to use this Repository on Your Machine (for development)

Please follow the instructions in our [Python Template Repository](https://github.com/Hochfrequenz/python_template_repository#how-to-use-this-repository-on-your-machine).
And for futher information, see the [Tox Repository](https://github.com/tox-dev/tox).

You can also check out our [MIG AHB Utility Stack (MAUS)](https://github.com/Hochfrequenz/mig_ahb_utility_stack) and [AHBicht](https://github.com/Hochfrequenz/ahbicht) repositories.

## Contribute

You are very welcome to contribute to this template repository by opening a pull request against the main branch.
