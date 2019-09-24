
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
* 1.1.2 - Fix for Acronym and Output validators
* 1.1.1 - Removed breaking changes to Makefile validator
* 1.1.0 - Add validator rules: Check for Help.md, profanity check, acronym capitalization check, 
`print` usage check, JSON tests, exceptions, credentials, passwords | Updated rules: Makefiles, logging
* 1.0.0 - Initial release

PyPi.org link: [https://pypi.org/project/insightconnect-integrations-validators/](https://pypi.org/project/insightconnect-integrations-validators/)
