

[Base64](https://en.wikipedia.org/wiki/Base64) is a common binary-to-text encoding scheme used in various protocols and software such as MIME to carry data stored in binary formats across channels that only reliably support text content. This plugin allows data to be Base64-encoded or decoded using the standard Base64 alphabet.



* Encode data in Base64 to transfer binary data, image files, etc. in a text format
* Decode Base64 encoded text to reveal the plaintext



_This plugin does not contain any requirements._




_This plugin does not contain a connection._







This action is used to Base64 encode a `string` using the standard Base64 alphabet.


|Name|Type|Default|Required|Description|Enum|
|----|----|-------|--------|-----------|----|
|content|string|None|True|Data to encode|None|None|



|Name|Type|Required|Description|
|----|----|--------|-----------|
|data|bytes|False|Encoded data result|



This action is used to decode a Base64 `string` or file of type `bytes` using the standard Base64 alphabet.


|Name|Type|Default|Required|Description|Enum|
|----|----|-------|--------|-----------|----|
|base64|bytes|None|True|Data to decode|None|
|errors|string|nothing|False|How errors should be handled when decoding Base64|['replace', 'ignore', 'nothing']|



|Name|Type|Required|Description|
|----|----|--------|-----------|
|data|string|False|Decoded data result|



Decode Base64 to data


|Name|Type|Default|Required|Description||Enum|Example|
|----|----|-------|--------|-----------|-----|-------|
|base64_array|[]string|None|True|Data to decode|None|['MQ==', 'Mg==']|

Example input:

```
```


|Name|Type|Required|Description|
|----|----|--------|-----------|
|data|string|True|Decoded data result|

Example output:

```
```





_This plugin does not contain any triggers._



_This plugin does not contain any custom output types._



For the Base64 decode action, be sure that the input contains valid Base64 data.

If the Base64 you're decoding contains any non UTF-8 characters the plugin will fail. To remedy this issue, there's a
option to set how errors are to be handled. These options are "replace" and "ignore". Replace will change all non UTF-8
characters to `\uffd` or `?`. While ignore will drop the character from the output.


* 1.1.2 - New spec and help.md format for the Hub
* 1.1.1 - Fixed issue where action Decode required error parameter
* 1.1.0 - Bug fix in decode action, added an option for error handling
* 1.0.0 - Support web server mode
* 0.2.2 - Generate plugin with new schema
* 0.2.1 - SSL bug fix in SDK
* 0.2.0 - Plugin variable naming and description improvements, add required outputs
* 0.1.1 - Bug fix in output variables
* 0.1.0 - Initial plugin



* [Base64](https://en.wikipedia.org/wiki/Base64)
* [Python Base64 Encode](https://docs.python.org/2/library/base64.html#base64.standard_b64encode)
* [Python Base64 Decode](https://docs.python.org/2/library/base64.html#base64.standard_b64decode)

