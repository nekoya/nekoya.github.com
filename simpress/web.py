# -*- coding: utf-8 -*-
"""
"""
from flask import Flask, g, render_template, abort
from flask import make_response

import settings
import simpress.blog
from simpress.errors import NotFoundException

app = Flask(__name__,
            static_url_path='',
            static_folder='../themes/default',
            template_folder='../themes/default/_templates')
app.config.from_object(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.before_request
def before_request():
    g.blog = simpress.blog.Blog()
    for (k, v) in settings.blog.items():
        setattr(g.blog, k, v)


@app.route('/')
def index():
    return render_template('index.html', blog=g.blog, post=g.blog.posts[0])


@app.route('/blog/archives')
def blog_archives():
    return render_template('archives.html', blog=g.blog, posts=g.blog.posts)


@app.route('/blog/<year>/<month>/<day>/<name>')
@app.route('/blog/<year>/<month>/<day>/<name>/')
def blog_post(year, month, day, name):
    try:
        post = simpress.blog.Post(blog=g.blog, year=year, month=month, day=day,
                                  name=name)
    except NotFoundException:
        abort(404)
    return render_template('post.html', blog=g.blog, post=post)


@app.route('/atom.xml')
def atom_feed():
    res = make_response(
        render_template('atom.xml', blog=g.blog, posts=g.blog.posts[:10]))
    res.headers['Content-Type'] = 'application/xml'
    return res
