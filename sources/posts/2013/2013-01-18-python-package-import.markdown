---
layout: post
title: "Pythonのパッケージimportで間接的に参照が生える"
date: 2013-01-18 07:25
comments: true
categories: python
old_post: true
---
社内のプロダクト開発がPythonに移行したはいいけど、調査・運用系のスクリプトは変わらずPerlで書いてDevsとOpsの分離が進みそうで老害化著しい今日この頃です。

これじゃいかんと思って、ワンライナー以外はPythonで書くようになりました。pull req送るとダメ出しもらえるのでありがたいです。

そんなPythonでパッケージをimportしたりfrom〜importしたりすると、自分のイメージと違う動作をすることがあって新鮮だったのでメモ。

（2013/01/19 barとbazが紛らわしいのでs/baz/hoge/gしました）

main.py
    import foo.bar
    print foo.hoge.var

foo/\__init__.py

foo/bar.py
    from foo.hoge import var

foo/hoge.py
    var = 'DEAAAAAAAATH'

これでmain.pyを実行すると

    $ python main.py
    DEAAAAAAAATH

main.pyではfoo.hogeをimportしていないのに、参照できる。Python 2.6.5, 2.7.1で確認。

- foo.barが走った時点でfooの名前空間にhogeが取り込まれる
- foo.barをimportするとfoo.barだけでなく、fooへの参照も取り込まれる
- foo以下のパッケージをimportするとfoo.hoge.varにアクセス可能

ということか。


以下追記（2013/01/19）

[@hiratara](http://twitter.com/hiratara)さんとお話ししたので、少し補足。

（2013/01/22 リンク追加）[https://www.facebook.com/hiratara/posts/10152460490030164](https://www.facebook.com/hiratara/posts/10152460490030164)

『初めてのPython』によると、from module import name1は

    import module
    name1 = module.name1
    del module

と理屈の上ではほぼ同じ意味を持ちます、というような記述があって、パッケージでないモジュールでは実際そういう動作をするので「fromで指定したモジュールへの参照は保持されない」と思っていました。

上記のサンプルでは、foo.hogeはどこからも直接importはされず、foo.bar内でfrom〜importの形で参照されているだけなので、foo.hogeへの参照が残ると思っていなかったのです。「ほぼ」であって同一でないのはこういうところなのか、と。

確かにdel foo.hoge的なことをしてしまうと、問題が起こりうるしそこを厳密に管理するのは大変すぎるのでこうなっているのは合理的だけど、今まで考えてなかったなぁというのがこちらのエントリでございます。
