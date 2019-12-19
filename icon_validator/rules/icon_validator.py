from .validator import KomandPluginValidator
import os
import filetype
from pathlib import Path


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
            raise Exception("icon.png file not included in plugin")

    @staticmethod
    def check_icon_less_than_equal_70kb(plugin_spec):
        directory = plugin_spec.directory
        icon_file = directory + "/" + "icon.png"

        info = os.stat(icon_file)
        if info.st_size >= 70000:
            raise Exception("Included icon (%d) file exceeds maximum size limitation of 70kb" % info.st_size)

    @staticmethod
    def check_if_icon_is_png(plugin_spec):
        directory = plugin_spec.directory
        icon_file = directory + "/" + "icon.png"
        kind = filetype.guess(icon_file)

        if kind.extension != "png":
            raise Exception("Included icon file (%s) is not PNG" % kind.extension)

    @staticmethod
    def check_if_extension_image_file_exists(plugin_spec):
        directory = plugin_spec.directory
        extension_image_file = directory + '/extension.png'

        file_item = Path(extension_image_file)
        if not file_item.is_file():
            raise Exception("extension.png file not included in plugin. Please include a color PNG image of a logo for this vendor or product.")

    @staticmethod
    def check_extension_image_file_is_nonzero_size(plugin_spec):
        directory = plugin_spec.directory
        extension_image_file = directory + '/extension.png'

        image_file = os.stat(extension_image_file)
        if not image_file.st_size > 0:
            raise Exception("Extension image file is size zero. Please include a color PNG image of a logo for this vendor or product.")

