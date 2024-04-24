# Description

[Base64](https://en.wikipedia.org/wiki/Base64) is a common binary-to-text encoding scheme used in various protocols and software such as MIME to carry data stored in binary formats across channels that only reliably support text content. This plugin allows data to be Base64-encoded or decoded using the standard Base64 alphabet.

# Key Features

* Encode data in Base64 to transfer binary data, image files, etc. in a text format
* Decode Base64 encoded text to reveal the plaintext

# Requirements

_This plugin does not contain any requirements._

# Supported Product Versions

* 1.0.0
* 1.0.1

# Documentation

## Setup

_This plugin does not contain a connection._

## Technical Details

### Actions

#### Decoder

This action is used to decode Base64 to data.

##### Input

|Name|Type|Default|Required|Description||Enum|Example|Placeholder|Tooltip|
|----|----|-------|--------|-----------|-----|-------|-----------|-------|
|base64|bytes|None|True|Data to decode|None|base64|None|None|
|errors|string|nothing|False|How errors should be handled when decoding Base64|["replace", "ignore", "nothing"]|replace|None|None|

Example input:

```
{
  "base64": "MQ==",
  "errors": "example"
}
```

##### Output

|Name|Type|Required|Description|Example|
|----|----|--------|-----------|-------|
|data|string|True|Decoded data result|base64|

Example output:

```
{
  "data": "MQ=="
}
```

#### Decoder with Array

Decode Base64 to data

##### Input

|Name|Type|Default|Required|Description||Enum|Example|Placeholder|Tooltip|
|----|----|-------|--------|-----------|-----|-------|-----------|-------|
|base64_array|[]string|None|True|Data to decode|None|["MQ==", "Mg=="]|None|None|

Example input:

```
{
  "base64_array": "MQ=="
}
```

##### Output

|Name|Type|Required|Description|Example|
|----|----|--------|-----------|-------|
|data|string|True|Decoded data result|==Md|

Example output:

```
{
  "data": "1"
}
```

#### Encoder

This action is used to encode data to Base64.

##### Input

|Name|Type|Default|Required|Description|Enum|Example|Placeholder|Tooltip|
|----|----|-------|--------|-----------|----|-------|-----------|-------|
|content|string|None|True|Data to encode|None|This is a string|None|None|

Example input:

```
{
  "content": "example"
}
```

##### Output

|Name|Type|Required|Description|Example|
|----|----|--------|-----------|-------|
|data|bytes|True|Encoded data result|This is a string|

Example output:

```
{
  "data": "MQ=="
}
```

### Triggers

_This plugin does not contain any triggers._

### Custom Output Types

_This plugin does not contain any custom output types._

## Troubleshooting

For the Base64 decode action, be sure that the input contains valid Base64 data.

If the Base64 you're decoding contains any non UTF-8 characters the plugin will fail. To remedy this issue, there's a
option to set how errors are to be handled. These options are "replace" and "ignore". Replace will change all non UTF-8
characters to `\uffd` or `?`. While ignore will drop the character from the output.

# Version History

* 1.1.2 - New spec and help.md format for the Hub
* 1.1.1 - Fixed issue where action Decode required error parameter
* 1.1.0 - Bug fix in decode action, added an option for error handling
* 1.0.0 - Support web server mode
* 0.2.2 - Generate plugin with new schema
* 0.2.1 - SSL bug fix in SDK
* 0.2.0 - Plugin variable naming and description improvements, add required outputs
* 0.1.1 - Bug fix in output variables
* 0.1.0 - Initial plugin

# Links

* [Base64](https://en.wikipedia.org/wiki/Base64)

## References

* [Base64](https://en.wikipedia.org/wiki/Base64)
* [Python Base64 Encode](https://docs.python.org/2/library/base64.html#base64.standard_b64encode)
* [Python Base64 Decode](https://docs.python.org/2/library/base64.html#base64.standard_b64decode)

