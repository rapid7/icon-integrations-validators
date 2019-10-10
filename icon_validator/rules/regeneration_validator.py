import os
import subprocess
import json
from typing import Optional, NoReturn
from hashlib import md5
from .validator import KomandPluginValidator
from . import KomandPluginSpec

MD5 = str
JSON = str

_CHECKSUM = ".CHECKSUM"


def log(s: str) -> NoReturn:
    print(f"RegenerationValidator: {s}\n")


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
            raise Exception("Fatal: Invalid dict provided for SchemaHash! Dict was: %s" % dict_)

        return cls(identifier=dict_["identifier"], hash_=dict_["hash"])


class Checksum(object):

    def __init__(self, schemas: [SchemaHash], manifest: MD5, setup: MD5 = None):
        """
        Initializer for a Checksum
        :param schemas: List of SchemaHash objects
        :param manifest: Hash of the plugin manifest. For Go, this is cmd/main.go. For Python, this is the binfile.
        :param setup: Hash of the setup.py. Only relevant to Python plugins.
        """
        self.schemas = schemas
        self.manifest = manifest
        self.setup = setup

    def __eq__(self, other):
        self.schemas.sort()
        other.schemas.sort()

        equals = (self.manifest == other.manifest) and (self.setup == self.setup) and (self.schemas == other.schemas)

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
            schemas=schema_hashes,
            manifest=hashes.get("manifest"),
            setup=hashes.get("setup")
        )

    @classmethod
    def from_plugin(cls, schema_hashes: [SchemaHash], manifest_hash: MD5, setup_hash: MD5 = None):
        """
        Creates a Checksum from a plugin
        :param schema_hashes: List of MD5 hashed-schemas
        :param manifest_hash: MD5 hash of a plugin manifest (binfile or cmd/main.go)
        :param setup_hash: Python-only, MD5 hash of a setup.py
        :return: Checksum representing a plugin
        """

        return Checksum(schemas=schema_hashes,
                        manifest=manifest_hash,
                        setup=setup_hash)


class ChecksumHandler(object):
    _SETUP_PY = "setup.py"

    def __init__(self, plugin_name: str, plugin_directory: str):
        self.plugin_name = plugin_name
        self.plugin_directory = plugin_directory

    def run_from_validator(self):
        checksum_file_contents: str = self._get_hashfile()
        if not checksum_file_contents:
            print("No .CHECKSUM file found, skipping")
            return

        # Provided hashfile is the .CHECKSUM that was packaged with the plugin.
        # This should match what we create after regeneration.
        # Important to do this before regeneration so we don't lose it!
        provided_checksum_file: Checksum = Checksum.from_json(json_string=checksum_file_contents)

        # Are we dealing with Python or Go?
        if self._SETUP_PY in os.listdir(self.plugin_directory):
            self._regenerate()  # First regenerate the plugin
            schema_hashes: [SchemaHash] = self._hash_python_schemas()
            manifest_hash: MD5 = self._hash_python_manifest()
            setup_hash: MD5 = self._hash_python_setup()

            post_regen_checksum_file: Checksum = Checksum.from_plugin(schema_hashes=schema_hashes,
                                                                      manifest_hash=manifest_hash,
                                                                      setup_hash=setup_hash)
        else:
            print("Skipping regeneration validation for Go plugin!")
            # Go plugin, so just pass it
            return

        # Now that we have a post-regeneration Checksum, let's compare!
        print(post_regen_checksum_file.to_json())
        if not (provided_checksum_file == post_regen_checksum_file):
            raise Exception("Error: Hashes between provided plugin and regenerated plugin were not equal!")

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
        schema_paths: [str] = self._enumerate_go_schema_files()
        hashes: [SchemaHash] = []

        for path in schema_paths:
            try:
                with open(file=path, mode="rb") as schema:
                    hash_ = md5(schema.read()).hexdigest()
                    identifier = os.path.basename(path)
                    hashes.append(SchemaHash(identifier=identifier, hash_=hash_))
            except FileNotFoundError:
                continue
        return hashes

    def _hash_python_setup(self) -> MD5:
        setup_file: str = os.path.join(self.plugin_directory, self._SETUP_PY)

        try:
            with open(file=setup_file, mode="rb") as sf:
                return md5(sf.read()).hexdigest()

        except FileNotFoundError as e:
            raise Exception("Fatal: No %s found in Python plugin!" % self._SETUP_PY) from e

    def _hash_python_manifest(self) -> MD5:
        manifest_directory: str = os.path.join(self.plugin_directory, "bin")

        try:
            manifest_file: str = os.path.join(manifest_directory, os.listdir(manifest_directory)[0])
            with open(file=manifest_file, mode="rb") as mf:
                return md5(mf.read()).hexdigest()

        except (FileNotFoundError, IndexError) as e:
            raise Exception("Fatal: No binfile found in Python plugin!") from e

    def _hash_go_manifest(self) -> MD5:
        manifest_file: str = os.path.join(self.plugin_directory, "cmd", "main.go")

        try:
            with open(file=manifest_file, mode="rb") as mf:
                return md5(mf.read()).hexdigest()
        except FileNotFoundError as e:
            raise Exception("Fatal: No main.go found in Go plugin!") from e

    def _enumerate_go_schema_files(self) -> [str]:
        """
        Parses a Go plugin directory and returns a list of file paths to all schema files
        :return: List of schema file paths
        """

        dir_actions = os.path.join(self.plugin_directory, "actions")
        dir_triggers = os.path.join(self.plugin_directory, "triggers")
        connection = os.path.join(self.plugin_directory, "connection", "connection.go")

        schemas: [str] = []

        if os.path.exists(connection):
            schemas.append(connection)

        # Get all actions and triggers, filter out non-schema files, and add them to the list
        schemas.extend([os.path.join(dir_actions, a) for a in os.listdir(dir_actions) if "_custom.go" not in a])
        schemas.extend([os.path.join(dir_triggers, t) for t in os.listdir(dir_triggers) if "_custom.go" not in t])

        return schemas

    def _get_python_main_directory(self) -> str:
        """
        Parses a Python plugin and returns the main directory holding all the actions/triggers/connection/etc
        ie. 'komand_base64'. Note: This does NOT return the directory path - JUST the directory name!
        :return: Main Python plugin directory, ie. 'komand_base64'
        """

        all_ = os.listdir(self.plugin_directory)
        for a in all_:
            if os.path.isdir(a) and self.plugin_name in a:
                return a
        raise Exception("Fatal: Python plugin missing main directory!")

    def _regenerate(self) -> NoReturn:
        """
        Regenerates a plugin
        :return: None
        """
        # REGEN_COMMAND: str = "make regenerate > /dev/null 2>&1"

        # Get current directory, change directories to the one with the correct Makefile
        current_directory = os.curdir
        os.chdir(self.plugin_directory)
        REGEN_COMMAND: str = "make regenerate"

        # Run the regeneration command
        subprocess.run(REGEN_COMMAND.split(" "))

        # Regen is done, change back to previous directory
        os.chdir(current_directory)

    def _write_hashfile(self, hashfile: Checksum) -> NoReturn:
        """
        Writes a .CHECKSUM file to a plugin directory
        :param hashfile: Checksum object to write to file
        :return:
        """
        path = os.path.join(self.plugin_directory, _CHECKSUM)
        with open(file=path, mode="w") as hf:
            hf.write(hashfile.to_json())

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
        is_jenkins: bool = self.is_run_from_jenkins()
        log(f"Run from Jenkins is: {is_jenkins}")

        if is_jenkins:
            path = os.path.join(".", "plugin")
        else:
            path = "."
        log(f"Path is: {path}")
        log("Directory contents are: %s" % os.listdir(path))

        log("ENVIRONMENT VARIABLES ARE: %s" % os.environ)

        log("Root directory contents are: %s" % os.listdir("."))

        with open(file=os.path.join(".", "Makefile"), mode="r+") as hf:
            log("MAKEFILES CONTENTS ARE: %s" % hf.read())

        handler: ChecksumHandler = ChecksumHandler(plugin_name=spec.plugin_name(),
                                                   plugin_directory=path)

        handler.run_from_validator()

    @staticmethod
    def is_run_from_jenkins() -> bool:
        directory_contents: [str] = os.listdir(".")
        if "Gopkg.lock" not in directory_contents and "setup.py" not in directory_contents:
            return True
        else:
            return False
