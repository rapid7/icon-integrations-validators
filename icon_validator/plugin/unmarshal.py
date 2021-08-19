import json
from typing import List
from pydantic import parse_obj_as
from yaml import load, SafeLoader
from icon_validator.plugin.model import Plugin, Action, Trigger


def parse_actions(actions: dict) -> List[Action]:
    """
    Parser for actions extracted from a plugin spec
    :param actions: dictionary of actions
    :return: List of actions
    """
    a_list : List[Action] = []
    for key, value in actions.items():
        a = parse_obj_as(Action, value)
        a_list.append(a)
    return a_list


def parse_triggers(triggers: dict) -> List[Trigger]:
    """
    Parser for triggers extracted from a plugin spec
    :param triggers: dictionary of triggers
    :return: List of triggers
    """
    t_list: List[Trigger] = []
    for key, value in triggers.items():
        t = parse_obj_as(Trigger, value)
        t_list.append(t)
    return t_list


def from_file(spec_file_path: str) -> Plugin:
    with open(spec_file_path) as f:
        plug = load(f.read(), SafeLoader)
        print(json.dumps(plug))
        # Rip out Actions
        try:
            actions: dict = plug.pop("actions")
        except:
            print("no actions found")
        # Rip out triggers
        try:
            triggers: dict = plug.pop("triggers")
        except:
            print("no actions found")
        # Parse Plugin without action or triggers
        p = Plugin.parse_obj(plug)
        # we are building the plugin struct here and parsing the action and triggers later on

        # Parse Popped actions and triggers
        a_list = parse_actions(actions=actions)
        t_list = parse_triggers(triggers=triggers)

        # Cobble plugin and actions together
        p.actions = a_list
        p.triggers = t_list

        return p