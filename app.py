import os

from blog import Blog, Theme, logger, clean, build


blog = Blog(
    url='http://nekoya.github.io/',
    old_url='http://nekoya.github.com/',
    title='Nekoya press',
    description='',
    author='nekoya',
    posts_path=os.path.join('sources', 'posts'),
    pages_path=os.path.join('sources', 'pages')
)

theme = Theme(
    path='themes',
    name='default',
)

dist_path = '__dist'

logger.info('building blog: {}'.format(blog.title))
clean(dist_path)
build(dist_path, blog, theme)
