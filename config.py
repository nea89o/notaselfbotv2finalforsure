from cached_property import cached_property
from configlib import BaseConfig
from github import Github


class GithubConfig(object):
    access_token: str

    @cached_property
    def github(self):
        return Github(self.access_token)


class Config(BaseConfig):
    token: str
    github: GithubConfig


config = Config.get_instance()
