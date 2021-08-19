from git import Repo
from typing import Optional
from icon_validator.state.filter import filter_tag
from icon_validator.state.parse import parse_tags
from icon_validator.plugin.model import Plugin
from icon_validator.workflow.model import Workflow



class State:
    """
    State of the plugin or workflow based on Git.
    """

    ## Master
    def __init__(self, dir: str, plugin: Plugin, workflow: Workflow):
        self.plugin = Plugin
        self.workflow = Workflow
        self.directory = dir
        self.repo: Repo
        self.master: Repo
        self.branch: str
        if self.is_repo():
            self.set_repo()
            self.set_branch()
            self.set_master()
        else:
            raise f"{dir} is not a git repo"

    def set_repo(self):
        """
        Sets a git repo object for in the State
        :return:
        """
        self.repo = Repo(self.directory)

    def set_master(self):
        """
        Sets a git repo object that is master for State
        :return:
        """
        self.master = self.repo.heads.master

    def set_branch(self):
        """
        Sets the branch name
        :return:
        """
        self.branch = self.repo.head.ref

    def is_repo(self, repo_dir: str) -> bool:
        """
        Checks if directory supplied is a git repo
        :param repo_dir: location of git repo
        :return: bool
        """
        try:
            Repo(repo_dir)
        except Exception:
            return False
        return True

    def get_master_spec(self, plugin:str):
        """
        gets plugins spec from master branch
        :param plugin: plugin to pull master spec from
        :return:
        """
        master_tree = self.master.tree
        # loop through location in the plugin for the files we are looking for, we want to get into the plugin directory we are working on
        # master_tree[pluigns][plugin_name]
        for branch in master_tree["plugins"][plugin]:
            if branch.name == "plugin.spec.yaml":
                return branch
            raise "plugin.spec.yaml is missing from master, this is a new plugin. Nothing to compare."


    # def get_latest_tag(self):
    #     tags = self.repo.tags
    #     pt = filter(
    #         filter_tag,
    #         parse_tags(tags=tags, plugin_name=self.plugin.name)
    #     )
    #     return
    #
    #
    # def get_file_from_tag(self, tag, file_name):
