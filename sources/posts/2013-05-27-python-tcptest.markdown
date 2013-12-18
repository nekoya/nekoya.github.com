---
layout: post
title: "PythonでTest::TCP的なことをするライブラリをPyPIに上げました"
date: 2013-05-27 16:25
comments: true
categories: python
---

Perlでいうところの[Test::TCP](http://search.cpan.org/~tokuhirom/Test-TCP-1.27/lib/Test/TCP.pm)相当のことをPythonでやるライブラリをPyPIに上げました。ようやくPyPIデビューです。

- [https://github.com/nekoya/python-tcptest](https://github.com/nekoya/python-tcptest)
- [https://pypi.python.org/pypi/tcptest](https://pypi.python.org/pypi/tcptest)

Test::TCPはPerlでテスト時に一時的にサーバを起動したりする処理の基盤となるライブラリです。同等のことをPythonでやるのに適当なものが見当たらなかったので自分で書いたという経緯です。

社内では以前からこの仕組みを使ってテストを書いていたのですが、自社のconfig系のライブラリとの結合を排除して、再構成したものになります。今回こうして公開するにあたって、関数名をオリジナルのPerl版に近付けたり、TestServerの実装を全面的に見直したりしました。

tcptestパッケージにはTest::TCP本体だけでなく、memcachedとredisのテストサーバ実装も含まれています。Perlでは[Test::Memcached](http://search.cpan.org/~dmaki/Test-Memcached-0.00004/lib/Test/Memcached.pm)や[Test::RedisServer](http://search.cpan.org/~typester/Test-RedisServer-0.12/lib/Test/RedisServer.pm)のように別のライブラリとしてリリースされていますが、名前空間がバラバラになるのも微妙な気がしたので同一のパッケージにまとめました。

PyPIにアップロードすること自体は参考資料もたくさんあり難しくないのですが、どういう名前付けをすべきかなど運営上のルールが今ひとつ分からず、まだ戸惑っている面があります。大文字小文字とか-_.のどれで区切るのかとか。あと、bdistとかbdist_eggはPure Pythonのライブラリだと不要だと思うけどよく分からない。

なお、今回のtcptestは最初test.tcpという名前空間を使おうとしたのですが、Python標準のtestパッケージと干渉することが判明したので衝突回避のためこの名前になりました。

自社プロダクト間の名前空間であれば、pkgutil.extend_pathを使って回避するのですが、標準ライブラリはともかくとして、PyPIのライブラリ同士での衝突はどう回避してるんだろう。
