
# InsightConnect Integrations Validators

Tooling with a bundled suite of validator rules for
ensuring quality across
[Rapid7 InsightConnect](https://www.rapid7.com/products/insightconnect/) integrations.

## Installation

```
$ pip install insightconnect-integrations-validators
```

## Use

Simple!

### Command

```
$ icon-validate my_plugin_directory/
```

### Python

```
from icon_validator.validate import validate


validate("/path/to/plugin/directory")
```

## Changelog

* 1.1.6 - Improved Output validator
* 1.1.5 - Remove Makefile validator rule, fix rules import
* 1.1.4 - Move `rules` package inside `icon_validator`
* 1.1.3 - Ignore unit test directories (/unit_test & /unit_tests) in Exception Validator
* 1.1.2 - Fix for Acronym and Output validators
* 1.1.1 - Removed breaking changes to Makefile validator
* 1.1.0 - Add validator rules: Check for Help.md, profanity check, acronym capitalization check, 
`print` usage check, JSON tests, exceptions, credentials, passwords | Updated rules: Makefiles, logging
* 1.0.0 - Initial release

PyPi.org link: [https://pypi.org/project/insightconnect-integrations-validators/](https://pypi.org/project/insightconnect-integrations-validators/)
