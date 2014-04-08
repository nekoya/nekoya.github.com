---
title: tcptestにfluentdのテストサーバを追加しました
date: 2014-04-08 07:38
---

Pythonからテスト用の各種サーバを起動するライブラリ、tcptestにfluentdを起動するモジュールを追加しました。

- https://pypi.python.org/pypi/tcptest/0.4.0

こんな感じで使うと、server.logsに軽く整形されたログが溜まっていくのでテストがわりと楽に書けます。

<pre class="prettyprint">
import fluentd.sender
import fluentd.event

with tcptest.fluentd.Server() as server:
    fluent.sender.setup('app', port=server.port)
    fluent.event.Event('follow', {'foo': 'bar'})
    fluent.event.Event('label', {'hoge': 'fuga'})

print server.logs
# [('app.follow:', {u'foo': u'bar'}), ('app.label:', {u'hoge': u'fuga'})]
</pre>

やってることは単純で、[out_stdoutに投げてるだけ](https://github.com/nekoya/python-tcptest/blob/master/tcptest/fluentd.py)です。

サーバ停止前のウェイトとか何も考えてない感じですが、まぁとりあえずこれで。
