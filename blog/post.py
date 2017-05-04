import datetime
import os
import re
from typing import Any, Dict, Generator, List, NamedTuple
from typing import Callable  # noqa (to avoid flake8 misdetection)

import markdown

from .blog import Blog


class Headers(NamedTuple):
    title: str
    date: datetime.datetime
    categories: List[str]
    old_post: bool


class Post(NamedTuple):
    filename: str
    path: str
    url: str
    headers: Headers
    contents: str


default_headers = Headers('', datetime.datetime.now(), [], False)


def _create_headers(**kwargs: Any) -> Headers:
    return default_headers._replace(**kwargs)


def _load_file(filename: str) -> Generator[str, None, None]:
    with open(filename, 'r') as lines:
        for line in lines:
            yield line.rstrip()


def load_post(blog: Blog, filename: str) -> Post:
    g = _load_file(os.path.join(blog.posts_path, filename))
    next(g)  # skip the first line, treat as a comment
    headers = _create_headers(**parse_headers(g))
    path = post_path(filename)
    return Post(filename=filename,
                path=path,
                url=_post_url(blog, path, headers.old_post),
                headers=headers,
                contents=parse_content(g))


def load_page(blog: Blog, filename: str) -> Post:
    g = _load_file(os.path.join(blog.pages_path, filename))
    next(g)  # skip the first line, treat as a comment
    headers = _create_headers(**parse_headers(g))
    path = post_path(filename)
    return Post(filename=filename,
                path=path,
                url=_post_url(blog, path, headers.old_post),
                headers=headers,
                contents=parse_content(g))


def _post_url(blog: Blog, path: str, is_old_post: bool) -> str:
    root = blog.old_url if is_old_post else blog.url
    return ''.join((root, path))


def parse_headers(g: Generator[str, None, None]) -> Dict:
    def parse_title(x: str) -> str:
        return x.strip('"')

    def parse_date(x: str) -> datetime.datetime:
        return datetime.datetime.strptime(x, '%Y-%m-%d %H:%M')

    def parse_categories(x: str) -> List[str]:
        return x.split(' ')

    def parse_old_post(x: str) -> bool:
        return x == 'true'

    filter: Dict[str, Callable] = {
        'title': parse_title,
        'date': parse_date,
        'categories': parse_categories,
        'old_post': parse_old_post,
    }
    h = {}
    for x in g:
        if x == '---':
            break
        (k, v) = tuple(map(str.strip, x.split(':', 1)))
        if k in filter.keys():
            f = filter[k]
            h[k] = f(v)
    return h


def parse_content(g: Generator[str, None, None]) -> str:
    return str(markdown.markdown('\n'.join(g), extensions=['gfm']))


post_filename_rule = re.compile(r'^(\d{4})\-(\d\d)\-(\d\d)\-(.+)\.markdown$')


def post_path(filename: str) -> str:
    basename = os.path.basename(filename)
    m = re.match(post_filename_rule, basename)
    if bool(m):
        url = 'blog/%s/%s/%s/%s/' % (
            m.group(1),
            m.group(2),
            m.group(3),
            m.group(4),
        )
        return url
    return 'pages/{}/'.format(basename.replace('.markdown', ''))
