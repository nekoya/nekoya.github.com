from typing import List

from jinja2 import Environment, PackageLoader

from .blog import Blog
from .post import Post

env = Environment(
    loader=PackageLoader('themes', 'default/_templates'),
)


def render_top(blog: Blog, post: Post) -> str:
    template = env.get_template('index.html')
    html = template.render(blog=blog, post=post)
    return html


def render_post(blog: Blog, post: Post) -> str:
    template = env.get_template('page.html')
    html = template.render(blog=blog, post=post)
    return html


def render_archives(blog: Blog, posts: List[Post]) -> str:
    template = env.get_template('archives.html')
    html = template.render(blog=blog, posts=posts)
    return html


def render_feed(blog: Blog, posts: List[Post]) -> str:
    template = env.get_template('atom.xml')
    html = template.render(blog=blog, posts=posts)
    return html


def render_pages_top(blog: Blog) -> str:
    template = env.get_template('pages.html')
    html = template.render(blog=blog)
    return html
