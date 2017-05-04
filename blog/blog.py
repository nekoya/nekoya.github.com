from typing import NamedTuple


class Blog(NamedTuple):
    url: str
    old_url: str
    title: str
    description: str
    author: str
    posts_path: str
    pages_path: str


class Theme(NamedTuple):
    path: str
    name: str
