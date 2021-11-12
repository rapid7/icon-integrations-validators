import json
import os
from hashlib import md5
from typing import Optional

from icon_validator.rules import KomandPluginSpec
from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException

MD5 = str
JSON = str
_CHECKSUM = ".CHECKSUM"


class SchemaHash(object):

    def __init__(self, identifier: str, hash_: MD5):
        """
        Hash of a schema. For Python, all schema.py files. For Go, all non *_custom.go files.
        :param identifier: Identifier of the schema hash, eg. encode/schema.py (for the Base64 plugin action)
        :param hash_: MD5 hash of the schema file
        """
        self.identifier = identifier
        self.hash = hash_

    def __lt__(self, other):
        return self.identifier < other.identifier

    def __eq__(self, other):
        equals_identifier = self.identifier == other.identifier
        equals_hash = self.hash == other.hash

        return equals_identifier and equals_hash

    @classmethod
    def from_dict(cls, dict_: {str: str}):
        if "identifier" not in dict_ or "hash" not in dict_:
            raise ValidationException(f"Fatal: Invalid dict provided for SchemaHash! Dict was: {dict_}")

        return cls(identifier=dict_["identifier"], hash_=dict_["hash"])


class Checksum(object):

    def __init__(self, spec: MD5, schemas: [SchemaHash], manifest: MD5, setup: MD5 = None):
        """
        Initializer for a Checksum
        :param spec: Hash of the plugin spec. Only relevant to Python plugins.
        :param schemas: List of hashed schema files
        :param manifest: Hash of plugin manifest: bin file for Python plugins, cmd/main.go for Go plugins
        :param setup: Hash of setup.py if relevant
        """

        self.spec = spec
        self.schemas = schemas
        self.manifest = manifest
        self.setup = setup

    def __eq__(self, other):
        self.schemas.sort()
        other.schemas.sort()

        equals = (self.spec == other.spec) and (self.manifest == other.manifest) and (self.setup == self.setup) \
                 and (self.schemas == other.schemas)
        return equals

    def to_json(self) -> JSON:
        """
        Returns a JSON-serialized string of the Checksum object
        :return: JSON-serialized string of the Checksum object
        """
        j: JSON = json.dumps(self, default=lambda o: o.__dict__)
        return j

    @classmethod
    def from_json(cls, json_string: str):
        """
        Creates a Checksum object from a JSON string
        :param json_string: JSON string of hashes
        :return: Checksum object created from JSON
        """
        hashes: {str: str} = json.loads(json_string)
        schemas = hashes.get("schemas")

        schema_hashes: [SchemaHash] = list(map(lambda h: SchemaHash.from_dict(dict_=h), schemas))
        return cls(
            spec=hashes.get("spec"),
            schemas=schema_hashes,
            manifest=hashes.get("manifest"),
            setup=hashes.get("setup")
        )

    @classmethod
    def from_plugin(cls, spec_hash: MD5, schema_hashes: [SchemaHash], manifest_hash: MD5, setup_hash: MD5 = None):
        """
        Creates a Checksum from a plugin
        :param spec_hash: Hash of the plugin spec. Only relevant to Python plugins.
        :param schema_hashes: List of hashed schema files
        :param manifest_hash: Hash of plugin manifest: bin file for Python plugins, cmd/main.go for Go plugins
        :param setup_hash: Hash of setup.py if relevant
        """

        return Checksum(spec=spec_hash, schemas=schema_hashes, manifest=manifest_hash, setup=setup_hash)


class ChecksumHandler(object):
    _SETUP_PY = "setup.py"

    def __init__(self, plugin_name: str, plugin_directory: str):
        self.plugin_name = plugin_name
        self.plugin_directory = plugin_directory

    def run_from_validator(self):
        checksum_file_contents: str = self._get_hashfile()
        if not checksum_file_contents:
            # print("No .CHECKSUM file found, skipping")
            return

        # Provided hashfile is the .CHECKSUM generated from icon-plugin
        # This should match what we create after regeneration.
        # Important to do this before regeneration so we don't lose it!
        provided_checksum_file: Checksum = Checksum.from_json(json_string=checksum_file_contents)

        # If it is a python plugin
        if self._SETUP_PY in os.listdir(self.plugin_directory):
            spec_hash: MD5 = self._hash_python_spec()
            schema_hashes: [SchemaHash] = self._hash_python_schemas()
            manifest_hash: MD5 = self._hash_python_manifest()
            setup_hash: MD5 = self._hash_python_setup()
            post_regen_checksum_file: Checksum = Checksum.from_plugin(
                spec_hash=spec_hash, schema_hashes=schema_hashes, manifest_hash=manifest_hash, setup_hash=setup_hash
            )
        else:
            spec_hash: MD5 = self._hash_python_spec()
            schema_hashes: [SchemaHash] = self._hash_go_schemas()
            manifest_hash: MD5 = self._hash_go_manifest()
            setup_hash = None
            post_regen_checksum_file: Checksum = Checksum.from_plugin(
                spec_hash=spec_hash, schema_hashes=schema_hashes, manifest_hash=manifest_hash, setup_hash=setup_hash
            )

        # Now that we have a post-regeneration Checksum, let's compare!
        # print(post_regen_checksum_file.to_json())
        if not (provided_checksum_file == post_regen_checksum_file):
            raise ValidationException("Error: Hashes between provided plugin and checksum were not equal. "
                            "Regenerate the plugin and push to working branch.")

    def _hash_python_schemas(self) -> [SchemaHash]:
        hashes: [SchemaHash] = []
        for root, dirs, files in os.walk(self.plugin_directory):
            if "schema.py" not in files:
                continue

            identifier = "%s/schema.py" % os.path.basename(root)
            filepath = os.path.join(root, "schema.py")

            with open(file=filepath, mode="rb") as f:
                contents: str = f.read()
                m = md5()
                m.update(contents)
                hash_: str = m.hexdigest()

                hashes.append(SchemaHash(identifier=identifier, hash_=hash_))
        return hashes

    def _hash_go_schemas(self) -> [SchemaHash]:
        schema_paths = self._enumerate_go_schema_files()
        hashes: [SchemaHash] = []

        for key in schema_paths:
            for path in schema_paths[key]:
                try:
                    with open(file=path, mode="rb") as schema:
                        hash_ = md5(schema.read()).hexdigest()
                        identifier = f"{key}/{os.path.basename(path)}"
                        hashes.append(SchemaHash(identifier=identifier, hash_=hash_))
                except FileNotFoundError:
                    continue
        return hashes

    def _hash_python_setup(self) -> MD5:
        setup_file: str = os.path.join(self.plugin_directory, self._SETUP_PY)

        try:
            with open(file=setup_file, mode="rb") as sf:
                return md5(sf.read()).hexdigest()

        except FileNotFoundError:
            raise ValidationException(f"Fatal: No {self._SETUP_PY} found in Python plugin.")

    def _hash_python_spec(self) -> MD5:
        spec_file: str = os.path.join(self.plugin_directory, "plugin.spec.yaml")

        try:
            with open(file=spec_file, mode="rb") as sf:
                return md5(sf.read()).hexdigest()

        except FileNotFoundError:
            raise ValidationException("Fatal: No plugin spec found in Python plugin.")

    def _hash_python_manifest(self) -> MD5:
        manifest_directory: str = os.path.join(self.plugin_directory, "bin")
        try:
            manifest_file: str = os.path.join(manifest_directory, os.listdir(manifest_directory)[0])
            with open(file=manifest_file, mode="rb") as mf:
                return md5(mf.read()).hexdigest()

        except (FileNotFoundError, IndexError):
            raise ValidationException("Fatal: No binfile found in Python plugin.")

    def _hash_go_manifest(self) -> MD5:
        manifest_file: str = os.path.join(self.plugin_directory, "cmd", "main.go")

        try:
            with open(file=manifest_file, mode="rb") as mf:
                return md5(mf.read()).hexdigest()
        except FileNotFoundError as e:
            raise ValidationException("Fatal: No main.go found in Go plugin.")

    def _enumerate_go_schema_files(self) -> [str]:
        """
        Parses a Go plugin directory and returns a list of file paths to all schema files
        :return: List of schema file paths
        """

        dir_actions = os.path.join(self.plugin_directory, "actions")
        dir_triggers = os.path.join(self.plugin_directory, "triggers")
        connection = os.path.join(self.plugin_directory, "connection", "connection.go")

        schemas = {
            "actions": [],
            "triggers": [],
            "connection": []
        }

        if os.path.exists(connection):
            schemas["connection"].append(connection)

        # Get all actions and triggers, filter out non-schema files, and add them to the list
        if os.path.isdir(dir_actions):
            schemas["actions"].extend(
                [os.path.join(dir_actions, a) for a in os.listdir(dir_actions) if "_custom.go" not in a])

        if os.path.isdir(dir_triggers):
            schemas["triggers"].extend(
                [os.path.join(dir_triggers, t) for t in os.listdir(dir_triggers) if "_custom.go" not in t])

        return schemas

    def _get_python_main_directory(self) -> str:
        """
        Parses a Python plugin and returns the main directory holding all the actions/triggers/tasks/connection/etc
        ie. 'komand_base64'. Note: This does NOT return the directory path - JUST the directory name!
        :return: Main Python plugin directory, ie. 'komand_base64'
        """

        all_ = os.listdir(self.plugin_directory)
        for a in all_:
            if os.path.isdir(a) and self.plugin_name in a:
                return a
        raise ValidationException("Fatal: Python plugin missing main directory.")

    def _get_hashfile(self) -> Optional[str]:
        """
        Reads a .CHECKSUM and returns the contents
        :return: String of contents if found, None otherwise
        """
        path = os.path.join(self.plugin_directory, _CHECKSUM)

        try:
            with open(file=path, mode="r+") as hf:
                return hf.read()
        except FileNotFoundError:
            return None


class RegenerationValidator(KomandPluginValidator):

    def validate(self, spec: KomandPluginSpec):
        handler: ChecksumHandler = ChecksumHandler(plugin_name=spec.plugin_name(),
                                                   plugin_directory=spec.directory)
        handler.run_from_validator()

    @staticmethod
    def is_run_from_jenkins() -> bool:
        directory_contents: [str] = os.listdir(".")
        if "Gopkg.lock" not in directory_contents and "setup.py" not in directory_contents:
            return True
        else:
            return False
