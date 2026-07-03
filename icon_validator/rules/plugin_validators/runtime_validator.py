import ast
import glob
import os
import re
from typing import List, Union

import requests
from icon_validator.constants import DEFAULT_TIMEOUT
from icon_validator.exceptions import ValidationException
from icon_validator.rules.validator import KomandPluginValidator


class RuntimeValidator(KomandPluginValidator):
    # Third party modules whose import indicates a real caching mechanism is in use
    CACHING_MODULES = {
        "cachetools",
        "cachelib",
        "diskcache",
        "aiocache",
        "beaker",
        "dogpile",
        "requests_cache",
    }

    # Functools members that provide caching when imported/used
    CACHING_FUNCTIONS = {"lru_cache", "cache", "cached_property"}

    # Decorator names that indicate caching (like @lru_cache, @cache, @cached)
    CACHING_DECORATORS = {"lru_cache", "cache", "cached", "cached_property", "memoize"}

    @staticmethod
    def validate_setup(spec):
        if "setup.py" in os.listdir(spec.directory):
            with open(f"{spec.directory}/setup.py", "r") as file:
                replace_dictionary = {"\n": "", " ": ""}
                setup_str = re.sub("|".join(replace_dictionary), lambda x: replace_dictionary[x.group(0)], file.read())
                if 'install_requires=["insightconnect-plugin-runtime"]' not in setup_str\
                        and "install_requires=['insightconnect-plugin-runtime']" not in setup_str:
                    raise ValidationException("Komand is no longer used for install_requires in setup.py. "
                                              "Use insightconnect-plugin-runtime instead.")

    @staticmethod
    def validate_imports(spec):
        for root, dirs, files in os.walk(spec.directory):
            for file in files:
                if file.endswith(".py"):
                    with open(os.path.join(root, file), "r") as open_file:
                        file_str = open_file.read()

                        if "import komand\n" in file_str or "from komand " in file_str or "from komand." in file_str:
                            raise ValidationException(f"Komand import found in {str(os.path.join(root, file))}. "
                                                      "Komand is no longer used here. "
                                                      "Use insightconnect-plugin-runtime instead.")

    @staticmethod
    def _module_root(name: str) -> str:
        # Just return top level package name like for example "dogpile.cache" -> "dogpile"
        return name.split(".")[0] if name else name

    @staticmethod
    def _decorator_name(decorator) -> Union[str, None]:
        # Search for generic decorators @cache
        if isinstance(decorator, ast.Name):
            return decorator.id
        # Search for decorators with arguments like @cache(...) or @cachetools.cached(...)
        if isinstance(decorator, ast.Call):
            return RuntimeValidator._decorator_name(decorator.func)
        if isinstance(decorator, ast.Attribute):
            return decorator.attr
        return None

    @staticmethod
    def _find_caching_usage(file_str: str) -> Union[str, None]:
        # Parse the Python source into an AST and look for genuine caching constructs
        # Using the AST (rather than a text search) means the word "cache" appearing in
        # comments, docstrings, string values or unrelated variable names does not cause
        # a false positive - only real imports, decorators and helpers are considered
        try:
            tree = ast.parse(file_str)
        except SyntaxError:
            # If the file is not valid Python we cannot reliably inspect it, so skip it.
            return None

        # For each node in object tree
        for node in ast.walk(tree):
            # Check for import cachetools etc
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if RuntimeValidator._module_root(alias.name) in RuntimeValidator.CACHING_MODULES:
                        return f"import of caching library '{alias.name}'"
            # Check for from functools import lru_cache / from cachetools import cached etc
            elif isinstance(node, ast.ImportFrom):
                module_root = RuntimeValidator._module_root(node.module or "")
                if module_root in RuntimeValidator.CACHING_MODULES:
                    return f"import from caching library '{node.module}'"
                if module_root == "functools":
                    for alias in node.names:
                        if alias.name in RuntimeValidator.CACHING_FUNCTIONS:
                            return f"import of caching helper 'functools.{alias.name}'"
            # Check for @lru_cache/@cache/@cached decorators on functions or classes
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                for decorator in node.decorator_list:
                    name = RuntimeValidator._decorator_name(decorator)
                    if name in RuntimeValidator.CACHING_DECORATORS:
                        return f"caching decorator '@{name}' on '{node.name}'"
        return None

    @staticmethod
    def validate_caching(spec):
        if spec.spec_dictionary().get("cloud_ready") is True:
            paths = []
            actions_path = glob.glob(f"{spec.directory}/*/actions")
            paths.append(actions_path[0])
            tasks_path = glob.glob(f"{spec.directory}/*/tasks")
            # It is possible for existing plugins to not have /tasks directory, It will be when code
            # needs not to be regenerated(e.g. update action/triggers run() method) using icon-plugin-tool.
            if tasks_path:
                paths.append(tasks_path[0])
            for path in paths:
                for root, dirs, files in os.walk(path):
                    for file_ in files:
                        # Caching is a code concern, so only inspect Python source files
                        if not file_.endswith(".py"):
                            continue

                        # Check for caching usage like import cachetools, @lru_cache, etc
                        file_path = os.path.join(root, file_)
                        with open(file_path, "r") as open_file:
                            if caching_usage := RuntimeValidator._find_caching_usage(open_file.read()):
                                raise ValidationException(
                                    f"Cloud ready plugins cannot contain caching. "
                                    f"Found {caching_usage} in {file_path}."
                                )

    def validate_dockerfile(self, spec, latest_images):
        if "setup.py" in os.listdir(spec.directory):
            with open(f"{spec.directory}/setup.py", "r") as setup_file:
                setup_str = setup_file.read().replace("\n", "")

                if "insightconnect-plugin-runtime" in setup_str:
                    with open(f"{spec.directory}/Dockerfile", "r") as docker_file:
                        docker_str = docker_file.read()
                        docker_image = next(
                            filter(lambda image: image in docker_str, latest_images),
                            None,
                        )

                        if not any(image in docker_str for image in latest_images):
                            raise ValidationException(
                                "insightconnect-plugin-runtime is being used in setup.py. "
                                "Update Dockerfile accordingly to use latest base image."
                            )

                        current_tag = self._parse_image_tag(docker_image, docker_str)
                        latest_tags = self._get_latest_runtime_tags(docker_image)
                        if current_tag and current_tag not in latest_tags:
                            raise ValidationException(
                                f"The current base image tag ({current_tag}) set is not latest. "
                                f"Please update Dockerfile accordingly to use latest base image."
                                f" Current latest tags are: {latest_tags}" if latest_tags else ""
                            )

    @staticmethod
    def _parse_image_tag(image_name: str, dockerfile_content: str) -> Union[str, None]:
        match = re.search(f"{image_name}:\s*([^ \n]+)", dockerfile_content)
        if match:
            return match.group(1)
        return None

    @staticmethod
    def _get_latest_runtime_tags(image_name: str) -> List[str]:
        latest_tags = ["latest"]
        try:
            response = requests.request(
                "GET",
                f"https://hub.docker.com/v2/repositories/{image_name}/tags",
                params={"page_size": 3, "ordering": "last_updated"},
                timeout=DEFAULT_TIMEOUT,
            )
            response.raise_for_status()
            return latest_tags + [tag.get("name") for tag in response.json().get("results", [])]
        except Exception:
            return latest_tags

    def validate(self, spec):
        latest_images = [
            "rapid7/insightconnect-python-3-plugin",
            "rapid7/insightconnect-python-3-slim-plugin",
        ]
        self.validate_dockerfile(spec, latest_images)

        with open(f"{spec.directory}/Dockerfile", "r") as file:
            docker_str = file.read().replace("\n", "")

            if any(image in docker_str for image in latest_images):
                RuntimeValidator.validate_setup(spec)
                RuntimeValidator.validate_imports(spec)
                RuntimeValidator.validate_caching(spec)
