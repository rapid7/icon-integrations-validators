
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