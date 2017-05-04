---
layout: post
title: "Pythonのdatetimeで夏時間を扱う"
date: 2013-07-02 15:07
comments: true
categories: python
---
「[Pythonの日付処理とTimeZone](http://nekoya.github.io/blog/2013/06/21/python-datetime/)」を書いた後、Twitterで指摘をもらっていたのを遅ればせながら検証したので、改めてエントリを起こしてみました。

<blockquote class="twitter-tweet"><p>Pythonの日付処理とTimeZone <a href="http://t.co/KK1B5Fot0V">http://t.co/KK1B5Fot0V</a> datetime を tzinfo 付きで生成する場合は pytz.tzinfo.normalize しないと DST 境界を超えるところで存在しない時刻を作りますよ</p>&mdash; Jun Omae⁽⁶⁶ʲ⁵⁾ (@jun66j5) <a href="https://twitter.com/jun66j5/statuses/348421676503011328">June 22, 2013</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

[@jun66j5](https://twitter.com/jun66j5)さんありがとうございました。

このへんの背景は[pytzのサイト](http://pytz.sourceforge.net/)にありますが、そもそもサマータイムに馴染みがないのでどうあるべきかがしっくりきません。

## 標準時と夏時間の切り替わり

ここでは、ニューヨークが属するTimeZoneを例に話を進めます。まずは基本的な用語の整理から。

- [DST](http://ja.wikipedia.org/wiki/%E5%A4%8F%E6%99%82%E9%96%93) … daylight saving time、夏時間（サマータイム）のこと
- [EST](http://ja.wikipedia.org/wiki/%E6%9D%B1%E9%83%A8%E6%A8%99%E6%BA%96%E6%99%82) … 東部標準時、UTCより5時間遅れ（-05:00）
- [EDT](http://ja.wikipedia.org/wiki/%E6%9D%B1%E9%83%A8%E5%A4%8F%E6%99%82%E9%96%93) … 東部夏時間、UTCより4時間遅れ（-04:00）

とりあえずWikipediaにリンクしときましたが、他にも「[Time-j.net 世界時計 - 世界の時間と時差](http://www.time-j.net/)」というサイトの「[アメリカ / ニューヨークの時差と現在時刻](http://www.time-j.net/WorldTime/Location/America/New_York)」がいろいろ参考になりました。

2013年は3月10日の午前2時から11月3日の午前2時までが夏時間らしいです。と一口に言っても、夏時間に突入すると同時に現時刻の定義が変わるし、標準時に戻った時も現時刻の定義が変わるのでややこしいんですよね。

正確には「標準時（EST）の3/10 02:00から」「夏時間（EDT）の11/3 02:00まで」が夏時間の適用期間で、その時刻を迎えた時に切り替わるのでこういうことになるようです。

    from datetime import datetime
    import pytz
    
    fmt = '%Y-%m-%d %H:%M:%S %z(%Z)'
    
    def dump(year, mon, day, hour, min, sec):
        dt = datetime(year, mon, day, hour, min, sec, tzinfo=pytz.utc)
        print dt.astimezone(ny).strftime(fmt)
    
    ny = pytz.timezone('America/New_York')
    
    dump(2013, 3, 10, 6, 59, 59)  # 2013-03-10 01:59:59 -0500(EST)
    dump(2013, 3, 10, 7, 0, 0)    # 2013-03-10 03:00:00 -0400(EDT)
    dump(2013, 11, 3, 5, 59, 59)  # 2013-11-03 01:59:59 -0400(EDT)
    dump(2013, 11, 3, 6, 0, 0)    # 2013-11-03 01:00:00 -0500(EST)

2013年3月10日の午前2時という時間は消し飛び、夏時間に突入したという結果だけが残る。と考えれば覚えやすいのではないでしょうか。

## datetimeオブジェクトの作り方

夏時間に該当するdatetimeオブジェクトを作る時、コンストラクタにtzinfoを渡すとこうなります。

    >>> from datetime import datetime
    >>> import pytz
    >>> ny_tz = pytz.timezone('America/New_York')
    >>> datetime(2013, 4, 10, 8, 0, tzinfo=ny_tz).strftime(fmt)
    '2013-04-10 08:00:00 EST(-0500)'

ESTなので夏時間になっていません。これは、pytz.timezone()を単体で呼んだだけでは夏時間の判定ができないため、

1. とりあえずESTのtzinfoを返す
2. datetimeは渡されたtzinfoを単純に取り込む

という動作をして、こういう結果を返してしまうものと思われます。

    >>> ny_tz.localize(datetime(2013, 4, 10, 8, 0)).strftime(fmt)
    '2013-04-10 08:00:00 EDT(-0400)'

こちらは日付が確定した後にTimeZone情報を与えているので、夏時間に属するawareなdatetimeオブジェクトが取れています。

    def localize(dt):
        print ny_tz.localize(dt).strftime(fmt)

    localize(datetime(2013, 3, 10, 1, 59, 59))  # 2013-03-10 01:59:59 EST(-0500)
    localize(datetime(2013, 3, 10, 2, 0, 0))    # 2013-03-10 02:00:00 EST(-0500)
    localize(datetime(2013, 3, 10, 2, 59, 59))  # 2013-03-10 02:59:59 EST(-0500)
    localize(datetime(2013, 3, 10, 3, 0, 0))    # 2013-03-10 03:00:00 EDT(-0400)

2時になったらキング・クリムゾン発動するんじゃないの…

    def normalize(dt):
        print ny_tz.normalize(ny_tz.localize(dt)).strftime(fmt)

    normalize(datetime(2013, 3, 10, 1, 59, 59))  # 2013-03-10 01:59:59 EST(-0500)
    normalize(datetime(2013, 3, 10, 2, 0, 0))    # 2013-03-10 03:00:00 EDT(-0400)
    normalize(datetime(2013, 3, 10, 2, 59, 59))  # 2013-03-10 03:59:59 EDT(-0400)
    normalize(datetime(2013, 3, 10, 3, 0, 0))    # 2013-03-10 03:00:00 EDT(-0400)

こちらは2時台も補正されました。ただし、3/10 02:00〜02:59は存在しない時間なので、02:00は03:00と同時刻として処理されます。

    >>> ny_tz.localize(datetime(2013, 3, 10, 2, 0, 0)).astimezone(pytz.utc)
    datetime.datetime(2013, 3, 10, 7, 0, tzinfo=<UTC>)
    >>> ny_tz.localize(datetime(2013, 3, 10, 3, 0, 0)).astimezone(pytz.utc)
    datetime.datetime(2013, 3, 10, 7, 0, tzinfo=<UTC>)

いずれもUTCに変換してしまえば補正されます。UTCではなくJSTにしても同様ですが、TimeZoneの変換をするなら基準はUTCに置いた方が混乱が少ないでしょう。

ただし、この場合でもコンストラクタにtzinfoを渡してしまうと、

    >>> datetime(2013, 3, 10, 2, 0, tzinfo=ny_tz).astimezone(pytz.utc)
    datetime.datetime(2013, 3, 10, 7, 0, tzinfo=<UTC>)
    >>> datetime(2013, 3, 10, 3, 0, tzinfo=ny_tz).astimezone(pytz.utc)
    datetime.datetime(2013, 3, 10, 8, 0, tzinfo=<UTC>)

このように、後者もESTをベースとして処理されてしまいます。pytzの公式にもあるように、datetimeの実装が今の仕様である以上どうにもならないようです。

夏時間を考慮してdatetimeオブジェクトを作る場合は、以下を基本方針とするのがいいでしょう。

- コンストラクタにはtzinfoを渡さず、naiveなdatetimeオブジェクトをlocalizeする
- 存在しない時刻が渡る可能性がある時はnormalizeするかUTCに変換する

## timedeltaによる演算と夏時間

tzinfoが夏時間を考慮してくれない問題は、datetimeオブジェクトを作る時だけでなく、timedeltaによる演算時も同様です。

    from datetime import timedelta
    
    def offset(seconds):
        dt = ny_tz.localize(datetime(2013, 3, 10, 1, 59, 59))
        dt += timedelta(seconds=seconds)
        print dt.strftime(fmt)
    
    offset(0)     # 2013-03-10 01:59:59 EST(-0500)
    offset(1)     # 2013-03-10 02:00:00 EST(-0500)
    offset(3600)  # 2013-03-10 02:59:59 EST(-0500)
    offset(3601)  # 2013-03-10 03:00:00 EST(-0500)

夏時間に突入しても、TimeZoneはESTのままです。

    def offset_n(seconds):
        dt = ny_tz.localize(datetime(2013, 3, 10, 1, 59, 59))
        dt += timedelta(seconds=seconds)
        print ny_tz.normalize(dt).strftime(fmt)

    offset_n(0)     # 2013-03-10 01:59:59 EST(-0500)
    offset_n(1)     # 2013-03-10 03:00:00 EDT(-0400)
    offset_n(3600)  # 2013-03-10 03:59:59 EDT(-0400)
    offset_n(3601)  # 2013-03-10 04:00:00 EDT(-0400)

normalizeしてやると、補正されてEDTになります。

ただ、夏時間のように時間の定義が途中で変わるような条件で演算するのはあまりに複雑なので、事前にUTCに変換してしまった方が安全でしょう。

    >>> datetime(2013, 3, 10, 6, 59, 59, tzinfo=pytz.utc).astimezone(ny_tz).strftime(fmt)
    '2013-03-10 01:59:59 EST(-0500)'
    >>> datetime(2013, 3, 10, 7, 0, 0, tzinfo=pytz.utc).astimezone(ny_tz).strftime(fmt)
    '2013-03-10 03:00:00 EDT(-0400)'

astimezoneで変換した場合はnormalizeは不要なので、夏時間を意識する必要はありません。

特にテストを書く場合に、夏時間とその期間外でUTCからの時差が変わってテストケースに影響が出るのは好ましくないと考えます。

本件に限らず複数のTimeZoneを扱う場合は、「内部ではUTCで保持し、出力する段階でlocaltimeに変換する」のが間違いが起きにくいでしょう。文字コードで「内部ではUnicodeで保持し、出力する段階でUTF-8等に変換する」というのと同じですね。

## まとめ

- 夏時間がある場合はコンストラクタにtzinfoを渡さない
- 時刻を扱う場合は内部ではUTCで持つと混乱が少ない（はず）
