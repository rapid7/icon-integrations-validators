
# InsightConnect Integrations Validators

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Markdown Lint](https://github.com/rapid7/icon-integrations-validators/workflows/Markdown%20Lint/badge.svg)
![Unit testing](https://github.com/rapid7/icon-integrations-validators/workflows/Unit%20testing/badge.svg)

Tooling with a bundled suite of validator rules for
ensuring quality across
[Rapid7 InsightConnect](https://www.rapid7.com/products/insightconnect/) integrations.

## Installation

```
pip install insightconnect-integrations-validators
```

## Use

Simple!

### Command

```
icon-validate my_plugin_directory/
```

or

```
icon-validate my_plugin_directory/ --all
```

to run entire set of validators used in our CI.
Omitting `--all` is often helpful when developing.

### Python

```
from icon_validator.validate import validate


validate("/path/to/plugin/directory")
```

or

```
validate("/path/to/plugin/directory", run_all=True)
```

to simulate the `--all` flag.

## Contributions

Contributions are welcome! This project utilizes [black](https://github.com/psf/black)
and [pre-commit](https://pre-commit.com/) for handling code
style. Simply follow the instructions for installing pre-commit and 
run `pre-commit install` in the repository after cloning and you will
be on your way to contributing!

## Changelog

* 2.28.0 - Add Encoding Validators to look for problematic characters | Update Workflow Description Validator to validate existence of `description` in workflow .icon file | Update Workflow Description Validator to validate that the workflow `description` in workflow .icon file matches the description in workflow.spec.yaml | Update `title_validation_list` | Change error message in `title_validator` for capitalized word when it should not
* 2.27.0 - Add CloudReadyConnectionCredentialToken Validator
* 2.26.0 - Add Example Input Validator to validate if example field exist in plugin.spec | Remove Mitre from AcronymValidator
* 2.25.0 - Add Version Pin Validator to validate if dependency versions are pinned in requirements.txt
* 2.24.0 - Update validators to support validation of plugin tasks.
* 2.23.0 - Add Plugin Validator to identify missing version bump
* 2.22.2 - Fix incorrect detection of 'array' in help.md
* 2.22.1 - Revise Workflow Screenshots Validator
* 2.22.0 - Add workflow directory name and workflow file match validator | Fix incorrect detection of 'lowercase' numbers in filenames | Add additional words to title list
* 2.21.2 - Fix issue where numeric words in a title would break the title validator
* 2.21.1 - Update HelpInputOutputValidator to validate on new Example inputs
* 2.21.0 - Add new runtime validator to align with 4.0.0 release of InsightConnect Python Plugin Runtime 
* 2.20.0 - Add plugin utilization workflow validator | Fix issue where numbers in screenshot titles would cause validation to fail
* 2.19.0 - Add new `example` input to whitelist in SpecPropertiesValidator
* 2.18.0 - Add .icon file validator
* 2.17.2 - Fix to remove some common words from the profanity validator
* 2.17.1 - Fix broken package import
* 2.17.0 - Add workflow name validator, Bug fix for title filters
* 2.16.2 - Fix title validator where it would fail on titles with numbers in it.
* 2.16.1 - Fix profanity filters and title filters to pull from once place
* 2.16.0 - Add workflow description validator
* 2.15.0 - Fix issue in title validator, Add title validator for workflows, clean up requirements
* 2.14.0 - Fix issue where InputOutput validator would fail when missing required key
* 2.13.0 - Add screenshot validator
* 2.12.0 - Add validator to check that .icon filenames do not contain spaces
* 2.11.0 - Add PNG Hash validator
* 2.10.0 - Refactor of validate.py. Updates the validate method to use ValidationException and rework print statements to clean up unit testing
* 2.9.0 - Add unit testing support. Add support, workflow files, workflow vendor, workflow version, workflow changelog and workflow extension validators
* 2.8.1 - Bug fix for URLValidator when opening files
* 2.8.0 - Update ChangelogValidator to validate plugin's version history with latest version number |
Update HelpInputOutputValidator error messaging
* 2.7.0 - Add URL Validator
* 2.6.9 - Update HelpInputOutputValidator to fix error messaging |
Fix issue with HelpInputOutputValidator when help.md has action and trigger with same name
* 2.6.8 - Docker Validator to run with -a command line argument | Helpful message on failure
* 2.6.7 - Fix issue where OutputValidator was throwing error for plugins without any action
* 2.6.6 - Fix issue where HelpInputOutputValidator was not extracting complete output section of an action or trigger
* 2.6.5 - Update IconValidator to check for extension.png
* 2.6.4 - Remove invalid "JQ" entry from the Acronym Validator
* 2.6.3 - Update AcronymValidator and HelpValidator to skip validating example outputs of help.md
* 2.6.2 - Syntax error bug fix in validator order
* 2.6.1 - Fix issue where SSDEEP was listed as an acronym | Run the DockerValidator last
* 2.6.0 - Update to support workflow's help.md validation
* 2.5.0 - Add help input output validator
* 2.4.0 - Update to turn off ConfidentialValidator in code | Revised use case list 
for UseCase Validator
* 2.3.0 - Add changelog validator
* 2.2.0 - Using argparse module to handle arguments and provide -h option
* 2.1.6 - Fix issue where ID was an acronym
* 2.1.5 - Fix issue where confidential validator was not checking against provided whitelist
* 2.1.4 - Fix issue where confidential validator was triggering on remediated findings and updated formatting
* 2.1.3 - Update Exception Validator to throw warning
* 2.1.2 - Fix issue where resources validator would always raise an exception
* 2.1.1 - Update RequiredKeysValidator to validate the correct products key and empty resources keys
* 2.1.0 - Update Golang RegenerationValidator
* 2.0.2 - Update HelpValidator to fix error messaging
* 2.0.1 - Update UseCaseValidator valid use case list
* 2.0.0 - Update Help Validator to use new help format |
Update RequiredKeys Validator for new spec fields |
Add validator rule: use case validation
* 1.3.0 - Add --all flag to run entire set of validators,
add Confidential Validator, Regeneration Validator clean up
* 1.2.0 - Add regeneration validator jenkins support
* 1.1.8 - Add regeneration validator
* 1.1.7 - Remove false positive "SPAM" entry from the Acronym Validator
* 1.1.6 - Improved Output validator
* 1.1.5 - Remove Makefile validator rule, fix rules import
* 1.1.4 - Move `rules` package inside `icon_validator`
* 1.1.3 - Ignore unit test directories (/unit_test & /unit_tests) in Exception Validator
* 1.1.2 - Fix for Acronym and Output validators
* 1.1.1 - Removed breaking changes to Makefile validator
* 1.1.0 - Add validator rules: check for help.md, profanity check,
acronym capitalization check,
`print` usage check, JSON tests, exceptions, credentials, passwords
| Updated rules: Makefiles, logging
* 1.0.0 - Initial release

PyPi.org link: [https://pypi.org/project/insightconnect-integrations-validators/](https://pypi.org/project/insightconnect-integrations-validators/)
