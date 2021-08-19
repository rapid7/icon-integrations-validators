from git import TagReference
from typing import List
from pydantic import parse_obj_as
from model import Tag


def parse_tags(tags: List[TagReference], plugin_name: str = "") -> List[Tag]:
    """
    Takes a collection of tag name and serializes them to a Tag object
    :param tags: list of tags
    :return: List of
    """
    parsed_tags = []
    for tag in tags:
        ss = tag.name.split("_")
        if len(ss) < 3:
            raise f"parsing tag {tag} failed, please make sure the plugin is properly named " # link to formatting guide
        try:
            o = {
                "vendor": ss[0],
                "plugin_name": ss[1],
                "semver": ss[2]
            }
        except:
            #TODO: Better expection handling
            raise f"tag {tag} was missing a section"
        parsed_tags.append(parse_obj_as(Tag, o))
    return parsed_tags

