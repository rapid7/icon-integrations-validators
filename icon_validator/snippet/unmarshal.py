import json
import os
from typing import List

from icon_validator.exceptions import ValidationException

SNPT_FILE_EXTENSION = ".snpt"


def snpt_file_names(directory: str) -> List[str]:
    """
    snpt_file_names lists the .snpt files in a snippet directory
    :param directory: snippet directory
    :return: sorted list of .snpt file names
    """
    return sorted(file_name for file_name in os.listdir(directory) if file_name.endswith(SNPT_FILE_EXTENSION))


def read_snippet(directory: str) -> dict:
    """
    read_snippet loads the snippet directory's .snpt file, the JSON file InsightConnect exports for a snippet
    :param directory: snippet directory
    :return: .snpt file contents
    :raises ValidationException: if the directory does not hold exactly one .snpt file, or it is not a JSON object
    """
    file_names = snpt_file_names(directory)
    if not file_names:
        raise ValidationException(
            f"No .snpt file was found in {directory}. Export the snippet from InsightConnect and add the .snpt file."
        )
    if len(file_names) > 1:
        raise ValidationException(
            f"A snippet directory must contain exactly one .snpt file, found {len(file_names)}: {', '.join(file_names)}"
        )

    with open(os.path.join(directory, file_names[0]), encoding="utf-8") as snpt_file:
        try:
            snippet = json.load(snpt_file)
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            raise ValidationException(
                f"{file_names[0]} is not in JSON format ({error}). Try exporting the snippet again."
            ) from error

    if not isinstance(snippet, dict):
        raise ValidationException(f"{file_names[0]} is not a JSON object. Try exporting the snippet again.")

    return snippet
