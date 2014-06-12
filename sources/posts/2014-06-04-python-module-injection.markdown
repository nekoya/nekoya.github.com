---
title: Pythonでimportの呼び出し元モジュールを操作する
date: 2014-06-04 10:43
---
「モジュールAをimportしたらBもCもまとめて入っちゃう」とか「importしたら俺の中の何かが変わった」みたいなのをやる方法。

お行儀のいいやり方ではないが、テストコードに限って言えばやってもいいかなと思って試してみた。

<pre class="prettyprint">
import inspect
caller = inspect.getmodule(inspect.stack()[1][0])
caller.hoge = fuga
</pre>

callerに呼び出し元のモジュールが入るので、あとはよしなに。

ただ、これやるとpyflakes（自分はflake8使用）とかに「未定義の名前を参照してるよ！」って怒られる。うーん微妙か…
