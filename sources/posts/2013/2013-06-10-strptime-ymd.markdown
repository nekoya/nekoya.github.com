---
layout: post
title: "本当は怖いstrptimeと%Y%m%dの関係"
date: 2013-06-10 10:33
comments: true
categories: dev
---
「%Y%m%d」をstrptimeで処理すると曖昧になることを今更ながらに知りました。

社内で「201312」を渡すとキモいという話が出て、

<blockquote class="twitter-tweet"><p>Pythonでdatetime.datetime.strptime('201312', '%Y%m%d')がエラーにならず1月2日として成立するの具合悪いと思うの</p>&mdash; nekoya (@nekoya) <a href="https://twitter.com/nekoya/status/342897090780876800">June 7, 2013</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

ってPostしたら[@hiratara](http://twitter.com/hiratara/)さんが「2013129と2013130もキモいぞ」と教えてくれました。

普段は%Y-%-%dを使うんだけど、URLに日付を埋め込む場合はデリミタ無しの方が自然だなーと思ったらご覧の有様だよ。

Python2.7.1

    >> datetime.strptime('201312', '%Y%m%d')
    datetime.datetime(2013, 1, 2, 0, 0)
    >> datetime.strptime('2013129', '%Y%m%d')
    datetime.datetime(2013, 12, 9, 0, 0)
    >> datetime.strptime('2013130', '%Y%m%d')
    datetime.datetime(2013, 1, 30, 0, 0)

なお、Pythonだけでなく他の言語でも見事にバラバラでﾜﾛﾀ。それぞれ最新版じゃないけど、そう変わらない気がする。

Perl5.12.2 Time::Piece

    $ perl -MTime::Piece -le 'print localtime->strptime("201312", "%Y%m%d")'
    Sun Dec  1 00:00:00 2013
    $ perl -MTime::Piece -le 'print localtime->strptime("2013129", "%Y%m%d")'
    Mon Dec  9 00:00:00 2013
    $ perl -MTime::Piece -le 'print localtime->strptime("2013130", "%Y%m%d")'
    Error parsing time at /Users/ryo/perl5/perlbrew/perls/perl-5.12.2/lib/5.12.2/darwin-2level/Time/Piece.pm line 469.

PHP5.3.15

    $ php -r 'var_dump(new DateTime("201312"));'
    object(DateTime)#1 (3) {
      ["date"]=>
      string(19) "2013-06-10 20:13:12"
      ["timezone_type"]=>
      int(3)
      ["timezone"]=>
      string(10) "Asia/Tokyo"
    }
    $ php -r 'var_dump(new DateTime("2013129"));'
    object(DateTime)#1 (3) {
      ["date"]=>
      string(19) "2013-05-09 00:00:00"
      ["timezone_type"]=>
      int(3)
      ["timezone"]=>
      string(10) "Asia/Tokyo"
    }
    $ php -r 'var_dump(new DateTime("2013130"));'
    object(DateTime)#1 (3) {
      ["date"]=>
      string(19) "2013-05-10 00:00:00"
      ["timezone_type"]=>
      int(3)
      ["timezone"]=>
      string(10) "Asia/Tokyo"
    }

Ruby1.9.3p194

    % irb
    irb(main):001:0> require 'date'
    => true
    irb(main):002:0> Date.strptime('201312', '%Y%m%d').to_s
    ArgumentError: invalid date
            from (irb):2:in `strptime'
            from (irb):2
            from /Users/ryo/.rbenv/versions/1.9.3-p194/bin/irb:12:in `<main>'
    irb(main):003:0> Date.strptime('2013129', '%Y%m%d').to_s
    => "2013-12-09"
    irb(main):004:0> Date.strptime('2013130', '%Y%m%d').to_s
    ArgumentError: invalid date
            from (irb):4:in `strptime'
            from (irb):4
            from /Users/ryo/.rbenv/versions/1.9.3-p194/bin/irb:12:in `<main>'

%Y%m%dを取る場合は、strptime任せにせず自分でフォーマットのチェックもしておかないと危険ですね。もしくは、おとなしくデリミタ挟むか。
