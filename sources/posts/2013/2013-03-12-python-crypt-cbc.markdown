---
layout: post
title: "PerlのCrypt::CBCとPythonのPyCryptoで暗号文字列をやりとりする"
date: 2013-03-12 09:49
comments: true
categories: python perl
old_post: true
---
ここ数年はPerlで暗号を扱う時は[Mcrypt](http://search.cpan.org/~jesus/Mcrypt-2.5.7.0/Mcrypt.pm)を使っていますが、少し前の時代だと[Crypt::CBC](http://search.cpan.org/~lds/Crypt-CBC-2.32/CBC.pm)を使ったりしてました。世間の流れは知らないけど、Mcrypt使っておけば他のシステムとデータをやりとりする時にお互いやりやすいよねという。

Crypt::CBCで作られた暗号文字列をPythonで復号するケースがあったのですが、そのまま素直にやるとうまくいきません。

padding周りかなと思ったけど、どうやらkeyがそのままでは使えないらしい。stackoverflowにズバリそのまま[Using PyCrypto to decrypt Perl encrypted password](http://stackoverflow.com/questions/14859006/using-pycrypto-to-decrypt-perl-encrypted-password)があったのでメモ。

{% gist 5088592 publish_hex_key.pl %}

こんな具合にして変換したkeyをPythonのコードに埋め込みます。

{% gist 5088592 decrypt.py %}

あとはpaddingをそれっぽく調整して、こんなもんでいけたっぽいです。
