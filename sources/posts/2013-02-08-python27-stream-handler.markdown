---
layout: post
title: "Python2.6と2.7でlogging.StreamHandlerのキーワード引数が違う"
date: 2013-02-08 09:12
comments: true
categories: python
old_post: true
---
CentOS5系からUbuntu12.04への移行を狙っていて、Pythonも2.6.5から2.7.3に上げようかという今日この頃。

logging周りでテストがコケて、何かと思ったらStreamHandlerのキーワード引数が変わっていた。

- [http://docs.python.org/2.6/library/logging.html?highlight=streamhandler#logging.StreamHandler](http://docs.python.org/2.6/library/logging.html?highlight=streamhandler#logging.StreamHandler)
- [http://docs.python.org/2.7/library/logging.handlers.html#streamhandler](http://docs.python.org/2.7/library/logging.handlers.html#streamhandler)

Python2.6で

    handler = logging.StreamHandler(strm=stream)

と書いていたところが、2.7では

    handler = logging.StreamHandler(stream=stream)

と書かないと動かなくなっています。StreamHandlerの__init__()では、

    def __init__(self, stream=None):
        """
        Initialize the handler.
        
        If stream is not specified, sys.stderr is used.
        """
        Handler.__init__(self)
        if stream is None:
            stream = sys.stderr
        self.stream = stream

として受け取っているだけで他の引数もないので、単に

    handler = logging.StreamHandler(stream)

とキーワード引数で渡すのをやめれば動くんだけど、こういう「短縮名じゃない方がいいよね」みたいな深い意味のなさそうな変更をあっさり入れられると萎える…

それとも2.6.5と2.7.3の間にはそういう変更を入れても問題ないとされるぐらいの隔たりがあるのだろうか。
