---
layout: post
title: "さくらのVPSにUbuntuを入れる初期設定手順"
date: 2013-01-24 10:15
comments: true
categories: ubuntu
old_post: true
---
さくらのVPSは初期設定はCentOS6だけど、Ubuntu入れるのも簡単でいいですね。

ただ、インストール直後は本当にOSを入れただけの無防備な状態で非常に危険です。

最低限の設定を定型化しておかないと怖いので、以下メモ。

手順はUbuntu12.04LTSを前提にしていますが、特別なことはしていないので多少の違いは問題ないはず。


## OSインストール直後の安全確保

インストール自体はマニュアルに沿ってやればOK。

ただし、パスワードは万が一抜かれてもいいように、普段使っていない捨てパスワードを使う。

起動したら急いでufwを使ってiptablesの設定を入れる。まずは全部閉じる。

```
sudo ufw enable
sudo ufw default DENY
```

念のためiptablesの設定を見ておく。

```
sudo iptables -L
```

いろいろ出てきたら個別のルールは精査しなくてもとりあえずはOK。

外からのアクセスを遮断したら、その時点で不審なログが無いことを確認する。

```
sudo less /var/log/auth.log
```


## SSHの設定

ひとまず安全が確保されたので、ここからは落ち着いて作業できる。

~/.ssh/が無いので作るところから。

```
mkdir .ssh
chmod 700 .ssh
```

リモートコンソールのコピペボタンを使って、~/.ssh/authorized_keysを作る。

```
cat > .ssh/authorized_keys
chmod 600 .ssh/authorized_keys
```

パーミッションは644とかでも怒られなかったが、落ち着かないので600にしておく。

SSHの設定もデフォルトのままなので、rootログインとパスワード認証をつぶす。

リモートコンソールでのコピペが結構面倒なので、viで直接編集した方が早いかも。

```
sudo sed -i 's/^PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sudo sed -i 's/^#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo /etc/init.d/ssh reload
```

外からのSSH接続を許可する。

```
sudo ufw allow ssh
```

外からrootと適当なユーザ名（user等）で入れないのを確認してから、自分のアカウントでSSH接続する。

これで最低限の安全性を確保したサーバが出来るので、あとはふつうに使う。
