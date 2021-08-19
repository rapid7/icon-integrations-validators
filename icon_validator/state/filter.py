from icon_validator.state.model import Tag


def filter_tag(tag: Tag, vendor: str = "", plugin_name: str = "", semver: str = "") -> bool:
    """
    filters tags by vendor, plugin_name or semver
    :param tag: Git Tag based off the state Tag model
    :param vendor: Name of vendor for plugin
    :param plugin_name: Name of Plugin
    :param semver: Git Tag Version
    :return:
    """
    if vendor != "":
        if tag.vendor == vendor:
            return True
    if plugin_name != "":
        if tag.plugin_name == plugin_name:
            return True
    if semver != "":
        if tag.plugin_name == semver:
            return True
    return False
