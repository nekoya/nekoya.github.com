---
title: nodejsをaptで入れたらnpmも入るようになってた
date: 2014-07-02 08:51
---
nodeで開発はしてないけど、フロントエンドを書く時にはnpmとか必要なので何かが変わるとうろたえる情弱です。

Ubuntu12.04で用意されている標準パッケージは古いので、公式のリポジトリを追加して入れる。

- [https://github.com/joyent/node/wiki/Installing-Node.js-via-package-manager#ubuntu-mint-elementary-os](https://github.com/joyent/node/wiki/Installing-Node.js-via-package-manager#ubuntu-mint-elementary-os)

で、新しいVMを作ってセットアップしてたらnpmのインストールでコケる症状が出たのです。

$ dpkg -l | grep nodejs
ii  nodejs                          0.10.29-1chl1~precise1            Node.js event-based server-side javascript engine

$ sudo apt-get install npm
Reading package lists... Done
Building dependency tree
Reading state information... Done
Some packages could not be installed. This may mean that you have
requested an impossible situation or if you are using the unstable
distribution that some required packages have not yet been created
or been moved out of Incoming.
The following information may help to resolve the situation:

The following packages have unmet dependencies:
 npm : Depends: nodejs but it is not going to be installed
       Depends: nodejs-dev
       Depends: node-request but it is not going to be installed
       Depends: node-mkdirp but it is not going to be installed
       Depends: node-minimatch but it is not going to be installed
       Depends: node-semver but it is not going to be installed
       Depends: node-ini but it is not going to be installed
       Depends: node-graceful-fs but it is not going to be installed
       Depends: node-abbrev but it is not going to be installed
       Depends: node-nopt but it is not going to be installed
       Depends: node-fstream but it is not going to be installed
       Depends: node-rimraf but it is not going to be installed
       Depends: node-tar but it is not going to be installed
       Depends: node-which but it is not going to be installed
E: Unable to correct problems, you have held broken packages.

アイエエエエエエエ

- [Upgrading from Node.js 0.8.x to 0.10.0 From my PPA](https://chrislea.com/2013/03/15/upgrading-from-node-js-0-8-x-to-0-10-0-from-my-ppa/)

> Also to note is that the nodejs-dev and npm packages don’t exist anymore. The new nodejs package contains everything that these separate packages used to

あっ、はい。うん、確かにそのままnpmって打ったら動きました。試しにコマンド叩いてみるなりすればよかったね…
