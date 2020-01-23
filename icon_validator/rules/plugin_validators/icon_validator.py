import os
from pathlib import Path

import filetype

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class IconValidator(KomandPluginValidator):

    def validate(self, plugin_spec):
        """Base64 matches icon file valid base64, <=70kb in size, png"""
        IconValidator.check_icon_file_exists(plugin_spec)
        IconValidator.check_icon_less_than_equal_70kb(plugin_spec)
        IconValidator.check_if_icon_is_png(plugin_spec)
        IconValidator.check_if_extension_image_file_exists(plugin_spec)
        IconValidator.check_extension_image_file_is_nonzero_size(plugin_spec)

    @staticmethod
    def check_icon_file_exists(plugin_spec):
        directory = plugin_spec.directory
        icon_file = directory + "/" + "icon.png"

        f = Path(icon_file)
        if not f.is_file():
            raise ValidationException("icon.png file not included in plugin.")

    @staticmethod
    def check_icon_less_than_equal_70kb(plugin_spec):
        directory = plugin_spec.directory
        icon_file = directory + "/" + "icon.png"

        info = os.stat(icon_file)
        if info.st_size >= 70000:
            raise ValidationException(f"Included icon ({info.st_size}) file exceeds maximum size limitation of 70Kb.")

    @staticmethod
    def check_if_icon_is_png(plugin_spec):
        directory = plugin_spec.directory
        icon_file = directory + "/" + "icon.png"
        kind = filetype.guess(icon_file)

        if kind.extension != "png":
            raise ValidationException(f"Included icon file ({kind.extension}) is not 'PNG'.")

    @staticmethod
    def check_if_extension_image_file_exists(plugin_spec):
        directory = plugin_spec.directory
        extension_image_file = f"{directory}/extension.png"

        file_item = Path(extension_image_file)
        if not file_item.is_file():
            raise ValidationException(
                "extension.png file not included in plugin. Please include a color PNG image of a logo for this vendor or product.")

    @staticmethod
    def check_extension_image_file_is_nonzero_size(plugin_spec):
        directory = plugin_spec.directory
        extension_image_file = f"{directory}/extension.png"

        image_file = os.stat(extension_image_file)
        if not image_file.st_size > 0:
            raise ValidationException(
                "Extension image file is size zero. Please include a color PNG image of a logo for this vendor or product.")
