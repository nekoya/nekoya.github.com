#-*- coding: utf-8 -*-
"""
"""
import datetime
import os
import re

import misaka
import pytz

from simpress.errors import NotFoundException
from simpress.utils import cached_property


class Blog(object):
    def __init__(self):
        self.posts_dir = 'sources/posts'
        self.root_url = 'http://localhost/'

    @property
    def posts(self):
        posts = []
        for filename in os.listdir(self.posts_dir):
            posts.append(Post(blog=self, filename=filename))
        return sorted(posts, key=lambda x: x.url, reverse=True)


class Post(object):
    _filename_rule = re.compile(r'^(\d{4})\-(\d\d)\-(\d\d)\-(.+)\.markdown$')

    def __init__(self, blog, year=None, month=None, day=None, name=None,
                 filename=None):
        self.blog = blog

        if filename:
            m = re.match(self._filename_rule, filename)
            self.year = m.group(1)
            self.month = m.group(2)
            self.day = m.group(3)
            self.name = m.group(4)
            self.filename = filename
        else:
            self.year = year
            self.month = month
            self.day = day
            self.name = name
            self.filename = '%s-%s-%s-%s.markdown' % (year, month, day, name)

        self.fullname = os.path.join(blog.posts_dir, self.filename)
        if not os.path.exists(self.fullname):
            raise NotFoundException(self.filename)

    @cached_property
    def fullpath(self):
        return 'blog/%s/%s/%s/%s/' % (
            self.year, self.month, self.day, self.name)

    @cached_property
    def url(self):
        blog_root = self.blog.root_url
        if self.headers.get('old_post', ''):
            blog_root = blog_root.replace('github.io', 'github.com')
        return blog_root + self.fullpath

    @cached_property
    def headers(self):
        (headers, contents) = self._parse_post()
        return headers

    @cached_property
    def contents(self):
        (headers, contents) = self._parse_post()
        return misaka.html('\n'.join(contents))

    def _parse_post(self):
        headers = {}
        contents = []
        phases = ('comment', 'header', 'content')
        mode = 0
        for line in self._load_file():
            if line == '---':
                mode += 1
            elif phases[mode] == 'header':
                (k, v) = line.split(':', 1)
                v = v.strip(' "')
                if k == 'date':
                    v = self._parse_datetime(v)
                headers[k] = v
            elif phases[mode] == 'content':
                contents.append(line)
        return (headers, contents)

    def _load_file(self):
        with file(self.fullname) as lines:
            for line in lines:
                yield line.rstrip()

    def _parse_datetime(self, dt_str):
        dt = datetime.datetime.strptime(dt_str, '%Y-%m-%d %H:%M')
        return pytz.timezone('Asia/Tokyo').localize(dt)
