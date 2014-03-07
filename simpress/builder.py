#-*- coding: utf-8 -*-
"""
"""
import datetime
import logging
import os
import shutil
import subprocess
import sys

import settings
import simpress.blog


class Builder(object):
    deploy_dir = '_deploy'

    def __init__(self, client, no_push=None):
        self.client = client
        self.theme = 'default'
        self.logger = logging.getLogger(__name__)
        self.no_push = no_push

        handler = logging.StreamHandler(sys.stdout)
        format = '%(asctime)s [%(levelname)s] %(message)s'
        handler.setFormatter(logging.Formatter(format, '%Y-%m-%d %H:%M:%S'))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def build_all(self):
        if os.path.exists(self.deploy_dir):
            shutil.rmtree(self.deploy_dir)
        self.build_theme()
        self.copy_static_files()
        self.build_page('/', 'index.html')
        self.build_page('atom.xml', 'atom.xml')
        self.build_page('blog/archives', 'blog/archives/index.html')
        self.build_page('pages', 'pages/index.html')
        blog = simpress.blog.Blog()
        for post in blog.posts:
            self.build_page(post.fullpath,
                            '%sindex.html' % post.fullpath)
        for post in blog.pages:
            self.build_page(post.fullpath,
                            '%sindex.html' % post.fullpath)
        if not self.no_push:
            self.deploy()

    def build_theme(self):
        self.logger.info('build theme "%s"' % self.theme)
        theme_dir = os.path.join('themes', self.theme)
        shutil.copytree(theme_dir, self.deploy_dir,
                        ignore=shutil.ignore_patterns('_*'))

    def copy_static_files(self):
        self.logger.info('copy static files')
        for target in ('images',):
            src_dir = os.path.join('sources', 'static', target)
            dst_dir = os.path.join(self.deploy_dir, target)
            shutil.copytree(src_dir, dst_dir)

    def build_page(self, url, filename):
        dirname = os.path.join(self.deploy_dir, os.path.dirname(filename))
        if dirname and not os.path.isdir(dirname):
            os.makedirs(dirname)
        self.logger.info('build %s' % filename)
        html = self.client.get(url).data
        dest_file = os.path.join(self.deploy_dir, filename)
        with open(dest_file, 'w') as f:
            f.write(html)

    def deploy(self):
        try:
            self.logger.info('prepare git repository')
            self.execute('git init')
            self.execute('git add .')
            now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            self.execute('git commit -m "Update at %s UTC"' % now)
            self.execute('git remote add origin %s' % settings.repository)
            self.logger.info('push to master branch')
            self.execute('git push -f origin master')
        except Exception, e:
            self.logger.error(e)

    def execute(self, cmd):
        proc = subprocess.Popen(cmd, shell=True, cwd=self.deploy_dir,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        (out, err) = proc.communicate()
        self.logger.debug(out)
        if err:
            raise Exception(err)
