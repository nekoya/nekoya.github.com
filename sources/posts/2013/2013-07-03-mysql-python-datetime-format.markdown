---
layout: post
title: "MySQL-python1.2.4でdatetimeから文字列の変換方法が変わった件"
date: 2013-07-03 10:32
comments: true
categories: python
---
MySQL-python（MySQLdb）を上げたら、今まで通ってたテストでwarningが出るようになりました。

[MySQLdb/times.py](https://github.com/farcepest/MySQLdb1/blob/MySQLdb-1.2.4/MySQLdb/times.py)で以前は

    def format_TIMESTAMP(d):
        return d.strftime("%Y-%m-%d %H:%M:%S")

こうなっていたものが、

    def format_TIMESTAMP(d):
        return d.isoformat(" ")

こうなったのが原因らしいのだけど、[Changelog](https://github.com/farcepest/MySQLdb1/blob/MySQLdb-1.2.4/HISTORY)を見てもそれらしい表記がないので少し経緯を追ってみました。

この変更で何が問題になったかというと、

    >> import datetime, pytz
    >>> datetime.datetime.now(pytz.utc).isoformat(' ')  # aware
    '2013-06-27 01:50:16.156481+00:00'
    >>> datetime.datetime.now().isoformat(' ')  # naive
    '2013-06-27 10:48:30.696072'

のように、microsecondや時差を含んだ文字列がSQLに渡って「Warning: Incorrect datetime value: '2013-06-27 01:50:16.156481+00:00' for column 〜」という警告が出るようになりました。

履歴を追っていくと、[http://sourceforge.net/p/mysql-python/svn/659/](http://sourceforge.net/p/mysql-python/svn/659/) で

>Use isoformat() instead of strftime() to avoid year limitations of the latter. Fixes #3296395

とあって、1900年以前の日付を扱えるようにこの変更を加えたことが分かります。strftime(3)の仕様的にそうなってたけど、そこの制限を外したぜってことらしいです。だけど、この#3296395ってどこのことだ…

該当するチケットは [#311 executing a datetime column update with year < 1900 fails](http://sourceforge.net/p/mysql-python/bugs/311/) っぽいけど、BTS移行とかしたんでしょうか。

最初はMySQL5.6でdatetime型がミリ秒対応したらしい（検証してない）ので、それに合わせた施策かなーと思ったらそんなことはなかった。

他にもmicrosecond周りでは [#325 Datetime fields with microsecond shows as None](http://sourceforge.net/p/mysql-python/bugs/325/) みたいなチケットが今も動いていたりして、なかなか予断を許さない印象を受けます。

DBのライブラリがdatetimeオブジェクトを適切に扱ってくれるのは素敵だと思ってたけど、なかなか難しいですね。取り急ぎの対処法としては、

- microsecondやtzinfoを含まないdatetimeオブジェクトだけを扱う
- 事前に自分で文字列にして渡す

のいずれかにわけで、自分のユースケースだとコネクション管理と[SQL::Maker](http://search.cpan.org/~tokuhirom/SQL-Maker-1.12/lib/SQL/Maker.pm)の簡易版みたいなことをするラッパーを通しているので、そこで時前でstrftimeして乗り切る感じになりました。

メロスには英語がわからぬ。だが、[issue](https://github.com/farcepest/MySQLdb1/issues/22)は切ってみた。
