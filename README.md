
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

* 2.47.20 - Bumping `requests` in requirements.txt and bumping `ldap` in the `version_pin_validator` requirements.txt
* 2.47.19 - `VersionBumpValidator` - Fixed issue where validator failed if plugin contained no actions or triggers
* 2.47.18 - `HelpInputOutputValidator` | `SpecPropertiesValidator` - Update to enable `placeholder` and `tooltip` validation | `RuntimeValidator` - Added SDK version validation
* 2.47.17 - `SpecPropertiesValidator` - Added new excludeProduct field validator
* 2.47.16 - `HelpInputOutputValidator` - Update error message from `icon-plugin` to `insight-plugin` | `DockerValidator` - Print full error message and change instances of `icon-plugin` to `insight-plugin`
* 2.47.15 - `TitleValidator` - Change validator to print all issues rather than break on the first 
* 2.47.14 - `OutputValidator` - Fix issue where `schema.py` files from the venv folder were being validated
* 2.47.13 - `HelpInputOutputValidator` - Fix validator to change single quotes to double quotes when an input field uses list values so that it does not break
* 2.47.12 - `VersionBumpValidator` - update validation for connection versions| Updated `GitPython` to version 3.1.41.
* 2.47.11 - Update PyYaml version to fix unrelated tooling installation bug.
* 2.47.10 - `HelpInputOutputValidator` - Improved error messaging around invalid action/trigger/task headings
* 2.47.9 - `DockerfileParentValidator` | `CloudReadyValidator` - update to support cloud plugins and SDK image with specified `--platform` flag | `VersionBumpValidator` - add validation for connection versions.
* 2.47.8 - `DockerfileParentValidator` | `RuntimeValidator` - update supported SDK images | Updated `GitPython` to version 3.1.37
* 2.47.7 - `ConfidentialValidator` - Changed email violation to a warning
* 2.47.6 - Updated `GitPython` to version 3.1.32
* 2.47.5 - Updated `requests` to version 2.31.0 | Updated `GitPython` to version 3.1.30
* 2.47.4 - New help validator to handle `Custom Types` title
* 2.47.3 - Fix HelpInputOutputValidator when output in plugin.spec.yaml not contain an example field | Fix validation when example contains list in object in HelpExampleValidator
* 2.47.2 - Allow hyphens in WorkflowTitleValidator
* 2.47.1 - Fix plugin spec properties validator for tasks
* 2.47.0 - Add name validator to ensure plugin name conforms to standards
* 2.46.4 - Fix InputOutputValidator so that it does not break on datetime input examples
* 2.46.3 - Update version validator to check v2 api call
* 2.46.2 - Fixed VersionValidator regex failing to validate x0.x.x semantic version strings
* 2.46.1 - Add null variable check to example input validator
* 2.46.0 - Add new help.md validator to ensure there are key features, links, and examples
* 2.45.0 - Separated UseCaseValidator for workflows as plugins and workflows now have different usecase tags
* 2.44.2 - Fixed (and tested) VersionBumpValidator on new plugin
* 2.44.1 - Fixed VersionBumpValidator bug on new plugins
* 2.44.0 - Update WorkflowTitleValidator to validate titles in `.icon` file
* 2.43.2 - Fixed breaking change that caused VersionBumpValidator to not get remote changes, made code safer
* 2.43.1 - Add GitPython dependency for using VersionBumpValidator
* 2.43.0 - Add VersionBumpValidator to check if a major or minor version increment is needed
* 2.42.0 - Add in WorkflowScreenshotValidator to check parenthesis in screenshot title
* 2.41.1 - Exit with proper return codes when ran independently via CLI 
* 2.41.0 - Add SupportedVersionValidator
* 2.40.0 - Add PythonScriptUseValidator for workflows
* 2.39.0 - Add HelpExampleValidator | Improve EncodingValidator by printing all forbidden characters at one time
* 2.38.0 - Remove LoggingValidator | Update dependency versions
* 2.37.0 - Add UnapprovedKeywordsValidator | Add unit tests for AcronymValidator
* 2.36.0 - Add CloudReadyValidator
* 2.35.0 - Update DescriptionValidator to print list of missing description field | Update VersionPinValidator to not fail when `git+` is in requirements.txt
* 2.34.0 - Fix issue where WorkflowParametersKeywordValidator was not being called
* 2.33.0 - Update HelpValidator to identify duplicate headings | Update ConfidentialValidator to allow more e-mail examples
* 2.32.0 - Fix problem when ExampleInputValidator fail if in `example` field are 0, False or None | Update WorkflowHelpPluginUtilizationValidator to not fail when plugin not in `help.md` and in `.icon` file
* 2.31.0 - Update UseCaseValidator to print valid use cases | Update UseCaseValidator to identify duplicate use cases in keywords
* 2.30.0 - Add WorkflowParametersKeywordValidator
* 2.29.0 - Remove Workflow Description Validator to validate that the workflow `description` in workflow .icon file matches the description in workflow.spec.yaml
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
