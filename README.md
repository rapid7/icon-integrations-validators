
# InsightConnect Integrations Validators

## What this is

Tooling with a bundled suite of validators for
ensuring quality across
[Rapid7 InsightConnect](https://www.rapid7.com/products/insightconnect/) integrations.

## Installation

### Install the module via `pip`

```
$ pip install insightconnect-integrations-validators
```

## Okay great, but how do I use it

Simple!

TODO: UPDATE USAGE

```
from typing import Any
from icon_plugin_spec.plugin_spec import KomandPluginSpec, PluginComponent

spec: KomandPluginSpec = KomandPluginSpec(directory="path_to_my_plugin")
raw_connection: {str: Any} = spec.connection()  # Dictionary of connection properties

print(raw_connection)  # Prints out list of inputs on the connection

# or, do the following
connection: PluginComponent = PluginComponent.new_connection(raw=raw_connection)
print(connection.inputs)
```

