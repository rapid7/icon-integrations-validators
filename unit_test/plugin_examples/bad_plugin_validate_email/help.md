# Description

Encode and decode data using the base64 alphabet

# Key Features

Identify key features of plugin.

# Requirements

* Example: Requires an API Key from the product
* Example: API must be enabled on the Settings page in the product's user interface

# Documentation

## Setup

_This plugin does not contain a connection._

## Technical Details

### Actions

#### Decoder

This action is used to decode Base64 to data.

##### Input

|Name|Type|Default|Required|Description|Enum|Example|
|----|----|-------|--------|-----------|----|-------|
|base64|bytes|None|True|Data to decode|None|base64|
|errors|string|nothing|False|How errors should be handled when decoding Base64|['replace', 'ignore', 'nothing']|replace|

Example input:

```
```

##### Output

|Name|Type|Required|Description|
|----|----|--------|-----------|
|data|string|True|Decoded data result|

Example output:

```
```

#### Decoder with Array

This action is used to decode Base64 to data.

##### Input

|Name|Type|Default|Required|Description|Enum|Example|
|----|----|-------|--------|-----------|----|-------|
|base64_array|[]string|None|True|Data to decode|None|["user@example.com", "user_dominika@example.com"]|

Example input:

```
```

##### Output

|Name|Type|Required|Description|
|----|----|--------|-----------|
|data|string|True|Decoded data result|

Example output:

```
```

#### Encoder

This action is used to encode data to Base64.

##### Input

|Name|Type|Default|Required|Description|Enum|Example|
|----|----|-------|--------|-----------|----|-------|
|content|string|None|True|Data to encode|None|anna.kwiatkowska@test.com|

Example input:

```
```

##### Output

|Name|Type|Required|Description|
|----|----|--------|-----------|
|data|bytes|True|Encoded data result|

Example output:

```
```

### Triggers

_This plugin does not contain any triggers._

### Tasks

_This plugin does not contain any tasks._

### Custom Output Types

_This plugin does not contain any custom output types._

## Troubleshooting

_This plugin does not contain any troubleshooting information._

# Version History

* 1.0.0 - Initial plugin

# Links

## References

* [Base64](LINK TO PRODUCT/VENDOR WEBSITE)
