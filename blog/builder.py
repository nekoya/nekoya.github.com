import os
import shutil
from typing import List

from .blog import Blog, Theme
from .logging import logger
from .render import (
    render_top, render_post, render_archives, render_feed, render_pages_top,
)
from .post import Post, load_post, load_page

THEMES_PATH = 'themes'


def clean(path: str) -> None:
    clean_dist(path)


def build(dist_path: str, blog: Blog, theme: Theme) -> None:
    build_theme(theme, dist_path)
    copy_static_files(dist_path)
    posts = find_all_posts(blog)
    pages = find_all_pages(blog)

    build_top(dist_path, blog, posts[-1])
    build_archives(dist_path, blog, sorted(posts, reverse=True))
    build_pages_top(dist_path, blog)
    [publish_post(dist_path, blog, x) for x in pages]
    build_atom_feed(dist_path, blog, sorted(posts, reverse=True))
    [publish_post(dist_path, blog, x) for x in posts]


def find_all_posts(blog: Blog) -> List[Post]:
    all: List[str] = []
    for (root, dirs, files) in os.walk(blog.posts_path):
        relpath = os.path.relpath(root, blog.posts_path)
        all.extend([os.path.join(relpath, x) for x in files])
    return [load_post(blog, x) for x in sorted(all)]


def find_all_pages(blog: Blog) -> List[Post]:
    all: List[str] = []
    for (root, dirs, files) in os.walk(blog.pages_path):
        relpath = os.path.relpath(root, blog.pages_path)
        all.extend([os.path.join(relpath, x) for x in files])
    return [load_page(blog, x) for x in sorted(all)]


def _write_file(filename: str, content: str) -> None:
    with open(filename, 'w') as f:
        f.write(content)


def clean_dist(path: str) -> None:
    logger.info('cleaning up dist dir: {}'.format(path))
    shutil.rmtree(path, ignore_errors=True)


def publish_post(dist_path: str, blog: Blog, post: Post) -> bool:
    post_path = os.path.join(dist_path, post.path)
    os.makedirs(post_path, exist_ok=True)
    dest_file = os.path.join(post_path, 'index.html')
    html = render_post(blog, post)
    logger.info('publish {}'.format(post.path))
    _write_file(dest_file, html)
    return True


def build_theme(theme: Theme, dist: str) -> None:
    logger.info('building theme {}'.format(theme.name))
    theme_dir = os.path.join(theme.path, theme.name)
    shutil.copytree(theme_dir, dist, ignore=shutil.ignore_patterns('_*'))


def copy_static_files(dist: str) -> None:
    logger.info('copy static files')
    for target in ('images',):
        src_dir = os.path.join('sources', 'static', target)
        dst_dir = os.path.join(dist, target)
        shutil.copytree(src_dir, dst_dir)


def build_top(dist_path: str, blog: Blog, post: Post) -> None:
    logger.info('publish index.html')
    _build_page(dist_path, 'index.html', render_top(blog, post))


def build_archives(dist_path: str, blog: Blog, posts: List[Post]) -> None:
    logger.info('publish archives/index.html')
    archives_path = os.path.join(dist_path, 'blog', 'archives')
    _build_page(archives_path, 'index.html', render_archives(blog, posts))


def build_atom_feed(dist_path: str, blog: Blog, posts: List[Post]) -> None:
    logger.info('publish atom.xml')
    _build_page(dist_path, 'atom.xml', render_feed(blog, posts))


def build_pages_top(dist_path: str, blog: Blog) -> None:
    logger.info('publish pages/index.html')
    pages_path = os.path.join(dist_path, 'pages')
    _build_page(pages_path, 'index.html', render_pages_top(blog))


def _build_page(dist_path: str, filename: str, content: str) -> None:
    os.makedirs(dist_path, exist_ok=True)
    dest_file = os.path.join(dist_path, filename)
    _write_file(dest_file, content)
