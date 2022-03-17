# AHBicht Functions Python Client

![Unittests status badge](https://github.com/Hochfrequenz/ahbicht-functions-python-client/workflows/Unittests/badge.svg)
![Coverage status badge](https://github.com/Hochfrequenz/ahbicht-functions-python-client/workflows/Coverage/badge.svg)
![Linting status badge](https://github.com/Hochfrequenz/ahbicht-functions-python-client/workflows/Linting/badge.svg)
![Black status badge](https://github.com/Hochfrequenz/ahbicht-functions-python-client/workflows/Black/badge.svg)

This repository contains a lightweight client for an [AHBicht](https://github.com/Hochfrequenz/ahbicht) powered backend by Hochfrequenz.

## How to use the Client
- Install using pip:
```bash
pip install ahbichtfunctionsclient
```
Then call it

```python
from ahbicht.mapping_results import PackageKeyConditionExpressionMapping
from ahbichtfunctionsclient import HochfrequenzPackageResolver
from maus.edifact import EdifactFormat, EdifactFormatVersion

package_resolver = HochfrequenzPackageResolver()
package_resolver.edifact_format = EdifactFormat.UTILMD
package_resolver.edifact_format_version = EdifactFormatVersion.FV2204
package_mapping = await package_resolver.get_condition_expression("10P")
assert isinstance(package_mapping, PackageKeyConditionExpressionMapping)
```

## How to use this Repository on Your Machine (for development)

Please follow the instructions in our [Python Template Repository](https://github.com/Hochfrequenz/python_template_repository#how-to-use-this-repository-on-your-machine).
tl;dr: tox.

## Contribute

You are very welcome to contribute to this template repository by opening a pull request against the main branch.
