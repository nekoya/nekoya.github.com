#-*- coding: utf-8 -*-
"""
"""
import simpress.web


class Application(object):
    def __init__(self, args):
        self.args = args

    def run(self):
        raise NotImplementedError()


class Publish(Application):
    def run(self):
        import simpress.builder
        builder = simpress.builder.Builder(simpress.web.app.test_client())
        builder.build_all()


class Preview(Application):
    def run(self):
        simpress.web.app.run(port=self.args.port, host='0.0.0.0')
