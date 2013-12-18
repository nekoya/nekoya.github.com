---
layout: post
title: "Pythonの日付処理とTimeZone"
date: 2013-06-21 10:04
comments: true
categories: python
---
日付周りの処理というのはとても難しい問題で、特にTimeZoneが絡むと基本的に大変なことになります。

Pythonは標準で用意されているdatetimeモジュールが高機能なので、それを使っておけば間違いない感があって、そういう意味では安心感があります。

とは言え、その扱いにはやはり注意が必要で、現時点でこうするのがいいかなーと思っていることをつらつらと記録したエントリがこちらです。

基本的にはMacのPython2.7.1で検証して、おやっと思ったところはCentOS5.8のPython2.6.5やUbuntu12.04のPython2.7.3で追試しています。

なお、datetime.datetimeと書くのがだるいので本文中では、

    from datetime import datetime

を前提としています。

## naiveとaware

[公式ドキュメント](http://docs.python.jp/2/library/datetime.html)にそのまま載ってるけど、datetimeオブジェクトは自身がTimeZone情報を持つ（aware）場合と、持たない（naive）場合があります。

明示的に指定しない限りnaiveになるため、プログラマは自身が「そのオブジェクトがどのTimeZoneに属するか」を常に間違いなく扱う必要があります。

で、これは当然難しい。JSTとUTCぐらいならまだしも、様々なタイムゾーンを扱うシステムでは常に正しい値を扱うことは至難の業と言ってもいい。

「基本はUTCで扱い、localtimeの場合は変数名にlocalと付ける」みたいなルールで頑張っても、モジュールをまたぐ時に変換間違えて残念なことになりかねません。

これに対して、awareなオブジェクトは内部にTimeZone情報を持っているので、そういうケースでも安心できます。

    >>> import pytz
    >>> from datetime import datetime
    >>> datetime.now(pytz.utc)
    datetime.datetime(2013, 5, 10, 7, 38, 56, 442741, tzinfo=<UTC>)
    >>> datetime(2013, 5, 16, tzinfo=pytz.timezone('Asia/Tokyo'))
    datetime.datetime(2013, 5, 16, 0, 0, tzinfo=<DstTzInfo 'Asia/Tokyo' CJT+9:00:00 STD>)

こんな感じで、原則として全てのdatetimeオブジェクトはawareな状態で扱うようにしています。utcnow()はtzinfoを受け取れないので、UTCにする場合でも必ずnow()を使います。

### pytzの位置付け

TimeZoneを表すには[pytz](http://pytz.sourceforge.net/)を使っています。可能であればサードパーティのライブラリではなく、全て標準モジュールで済ませたいところですが、pytzは[Python3.3の公式ドキュメント](http://docs.python.jp/3.3/library/datetime.html#tzinfo-objects)でも、

>pytz は最新の情報を含み、使用を推奨されています。

とお墨付きが出ているので標準に近いモジュールということで利用しています。

### naiveとawareの変換、あるいはTimeZone変更

naiveとawareの変換は、~~公式にあるようにreplaceを使います~~。naiveなdatetimeオブジェクトとawareなそれでは比較や演算が出来ないので、意外と使う場面はあります。

（2013/07/05修正）replaceするとJSTがCJTと認識される問題があったので、naive→awareの変換にはlocalizeを使用します → [Pythonでdatetimeにtzinfoを付与するのにreplaceを使ってはいけない](http://nekoya.github.io/blog/2013/07/05/python-datetime-with-jst/)

naive→aware

    >>> now = datetime.now()
    >>> now
    datetime.datetime(2013, 6, 18, 2, 15, 2, 485439)
    >>> pytz.utc.localize(now)
    datetime.datetime(2013, 6, 18, 2, 15, 2, 485439, tzinfo=<UTC>)

aware→naive

    >>> now = datetime.now(pytz.utc)
    >>> now
    datetime.datetime(2013, 6, 17, 17, 15, 43, 157502, tzinfo=<UTC>)
    >>> now.replace(tzinfo=None)
    datetime.datetime(2013, 6, 17, 17, 15, 43, 157502)

awareなオブジェクトの持っているTimeZone情報の変更は、replaceではなくastimezoneで以下のように。

    >>> now = datetime.now(pytz.utc)
    >>> now
    datetime.datetime(2013, 5, 10, 7, 55, 30, 9529, tzinfo=<UTC>)
    >>> now.astimezone(pytz.timezone('Asia/Tokyo'))
    datetime.datetime(2013, 5, 10, 16, 55, 30, 9529, tzinfo=<DstTzInfo 'Asia/Tokyo' JST+9:00:00 STD>)


## UNIXTIMEを扱う

PythonでUNIXTIMEを得る方法として、よく紹介されるのが

    >>> int(time.mktime(datetime.now().timetuple()))
    1371682685

です。intでくくらないと「1371682685.0」のようなfloatが返ってきます。これはこれでいいのですが、datetimeオブジェクトからUNIXTIMEを得ようとすると、

    >>> int(time.mktime(datetime(1970, 1, 1).timetuple()))
    -32400
    >>> int(time.mktime(datetime(1970, 1, 1, tzinfo=pytz.utc).timetuple()))
    -32400
    >>> int(time.mktime(datetime(1970, 1, 1, tzinfo=pytz.timezone('Asia/Tokyo')).timetuple()))
    -32400

どうやってもUTCを認識してくれない。time.mktimeはtzinfoに対応しておらず、localtimeを受けることになっているのが原因です。

[timeモジュールのドキュメント](http://docs.python.jp/2/library/time.html)にそのあたりのルールが書いてあって、UTCを扱う場合はcalendar.timegm()を使えとのこと。

    >>> calendar.timegm(datetime(1970, 1, 1).timetuple())
    0
    >>> calendar.timegm(datetime(1970, 1, 1, tzinfo=pytz.utc).timetuple())
    0

今度はうまくいきましたが、入力値をUTCとして解釈するので

    >>> calendar.timegm(datetime(1970, 1, 1, tzinfo=pytz.timezone('Asia/Tokyo')).timetuple())
    0

こんな風にlocaltimeの1970-01-01 00:00:00を渡しても0が返ってきます。要注意。

ちなみに、[calendar.timegm()](http://docs.python.jp/2/library/calendar.html#calendar.timegm)は

>関連はありませんが便利な関数で、 time モジュールの gmtime() 関数の戻値のような時間のタプルを受け取り、 1970年を起点とし、POSIX規格のエンコードによるUnixのタイムスタンプに相当する値を返します。実際、 time.gmtime() と timegm() は反対の動作をします。
>バージョン 2.0 で追加.

なんて紹介されていて、昔はのどかだったんだなぁと思いを馳せる次第です。

### 結局どうすればいいのか

ベンチ取ってみたら、UTCなdatetimeオブジェクトをcalendar.timegm()にかけるのが一番速かったので、現時刻を表すUNIXTIMEを取得するには、

    calendar.timegm(datetime.utcnow().timetuple())

が最適解でしょう。

datetimeオブジェクトを変換する場合は何を優先するかによりますが、基本的には安全性を重視して

    calendar.timegm(dt.astimezone(pytz.utc).timetuple())

とawareなdatetimeオブジェクトを確実にUTCにした上でcalendar.timegm()にかけるのがいいでしょう。

dtが元々UTCの場合はastimezone()は不要ですが、その場合は実行コスト自体が小さくなるのでやはり上記の形式が最適と考えます。

速度を求める場合は、

- dtがUTCならcalendar.timegm()
- dtがlocalならtime.mktime()

と変換する時点でdtのTimeZoneを確実に制御してやる必要があります。この場合、datetimeオブジェクト自体もnaiveな方が若干速くなりました。

datetimeオブジェクトに、tzinfoを考慮してUNIXTIMEを算出してくれるメソッドが生えていればこんなに考えなくていいのに…

### strftimeでUNIXTIMEを取る

ちなみに、プラットフォーム依存なので公式ドキュメントには記載されていませんが、

    >>> datetime.now().strftime('%s')
    '1371683864'

strftimeで%sを使うことでUNIXTIMEが取れます。

    >>> datetime(1970, 1, 1).strftime('%s')
    '-32400'
    >>> datetime(1970, 1, 1, tzinfo=pytz.utc).strftime('%s')
    '-32400'

こいつも手元では、localtimeを前提としたtzinfo非対応の挙動を示しました。検証してないけど、strftime(3)を使っててWindows非対応とかそういうことですかね。

ベンチ取ったらcalendar.timegm()よりも遅かったので、特に使うメリットは無さそうです。

### UNIXTIME to datetime

次にUNIXTIMEからdatetimeオブジェクトを作る方法です。

    >>> datetime.utcfromtimestamp(1337914193)
    datetime.datetime(2012, 5, 25, 2, 49, 53)

するとnaiveになってしまいます。先のnow()とutcnow()の関係と同様、utcfromtimestamp()ではなくfromtimestamp()にtzinfoを渡すアプローチを採ります。

    >>> datetime.fromtimestamp(1337914193, pytz.utc)
    datetime.datetime(2012, 5, 25, 2, 49, 53, tzinfo=<UTC>)


## datetime.dateもtzinfo非対応

年・月・日で構成される、dateオブジェクトは残念ながらTimeZone情報を持つことができません。

日付だって時差の影響を受けるのに、どうしてこうなっているのでしょう。残念。

仕方がないので純粋に日付を扱いたい場合も、datetimeオブジェクトを作って時刻関連の情報をreplace()でつぶしています。

    >>> datetime.now(pytz.utc).replace(hour=0,minute=0,second=0,microsecond=0)
    datetime.datetime(2013, 6, 20, 0, 0, tzinfo=<UTC>)

replace漏れがあると悲劇につながりかねないのが不安要素ではある。

あと、datetimeもtoday()があって日付だけ取得できるように見えるけど、

    >>> datetime.today()
    datetime.datetime(2013, 6, 20, 12, 8, 14, 929174)

時刻も込みで返ってくるので、そういう用途には使えません。

>datetime.fromtimestamp(time.time()) と等価です
>http://docs.python.jp/2/library/datetime.html#datetime.datetime.today

>このメソッドは today() と同様ですが、可能ならば time.time() タイムスタンプを通じて得ることができる、より高い精度で時刻を提供します
>http://docs.python.jp/2/library/datetime.html#datetime.datetime.now

あたりの説明もなんだか微妙…


## strptimeがTimeZoneを無視する

先日「[本当は怖いstrptimeと%Y%m%dの関係](http://nekoya.github.io/blog/2013/06/10/strptime-ymd/)」でも登場したstrptimeですが、TimeZoneの情報を与えてもnaiveなdatetimeオブジェクトしか作ってくれません。

    >>> from datetime import datetime
    >>> datetime.strptime('2012-06-18 UTC', '%Y-%m-%d %Z')
    datetime.datetime(2012, 6, 18, 0, 0)

仕方がないので、strptimeの後に続けてtzinfoだけ埋め込んでやります。

    >>> import pytz
    >>> datetime.strptime('2012-06-18 12:31:07', '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.utc)
    datetime.datetime(2012, 6, 18, 12, 31, 7, tzinfo=<UTC>)


## まとめ

- datetimeオブジェクトはawareな状態で扱おう
- UNIXTIMEの扱いはTimeZoneを意識して
- UTCを基準にcalendar.timegmとdatetime.fromtimestampがよさそう
- dateやstrptimeはtzinfo非対応なので要注意

本稿での検証に使ったベンチマークスクリプトは[https://gist.github.com/nekoya/5819512](https://gist.github.com/nekoya/5819512)にまとめておきました。

1.4GHzのCore2Duoを積んだMacBookAirだと結構な差が付いたけど、SandyBridge Core i7-2600 @3.4GHzで走らせたら3倍ぐらい速くなってあまり気にならなくなってしまった。買い換え時？
