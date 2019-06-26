
# InsightConnect Integrations Validators

## What this is

Tooling with a bundled suite of validator rules for
ensuring quality across
[Rapid7 InsightConnect](https://www.rapid7.com/products/insightconnect/) integrations.

## Installation

### Install the module via `pip`

```
$ pip install insightconnect-integrations-validators
```

## Okay great, but how do I use it

Simple!

### Standalone via CLI

```
$ icon-validate my_plugin_directory/
```

### Or via Python

```
from icon_validator.validate import validate


validate("/path/to/plugin/directory")
```

