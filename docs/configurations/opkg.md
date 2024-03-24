# Opkg Install

## Introduction

> 久しぶりに確認したら QTS 5.1.5 では　Entware-std がインストールできなくなっていました。

QNAP の NAS TS-219PⅡ では 「git」 すらインストールされていない。リソース的に「Container Station」ができたにしても「GitLab」は無理そうだし。

でも「Python3」があるからちょっとしたツールは動かせそう。。。

なんて思ったら、libjpeg が無いので Pillow がインストールできない。
これかぁ。 

### Environmet

- QTS 4.5.1.1495 on TS-231K
    - Entware-std 1.03
- QTS QTS 4.3.3.0868 on TS-219PⅡ
    - Entware-std 1.0 

### Check CPU Architecture

ARMv5 と ARMv7 があるらしいので調査。

```console
[~] # cat /proc/cpuinfo
Processor name	: Feroceon 88F6282 rev 1 (v5l) @ 2 GHz 
BogoMIPS	: 1980.82
Features	: swp half thumb fastmult edsp 
CPU implementer	: 0x56
CPU architecture: 5TE
CPU variant	: 0x2
CPU part	: 0x131
CPU revision	: 1

Hardware	: Feroceon-KW ARM
Revision	: 0000
Serial		: 0000000000000000
```

これが、"ARMv5TE" ってことらしいです。
 
## Installlation Entware

### Add QNAP Club repository

EU 圏の QNAP Club のリポジトリを追加します。
れによりコミュニティ版の QPKG アプリがインストールできるようになります。

「App Center」→「設定」→「アプリジポジトリ」

* 「追加」
    * 名前： QNAP Club（任意）
    * URL： https://www.qnapclub.eu/en/repo.xml
    * ユーザー名： （入力しない）
    * パスワード： （入力しない）

### Add Entware-std 

追加した QNAP Club から 「Entware-std」を探してインストールします。

### Update Package

```console
[~] # opkg update
Downloading http://bin.entware.net/armv5sf-k3.2/Packages.gz
Updated list of available packages in /opt/var/opkg-lists/entware

[~] # opkg upgrade


List installed packages
[~] # opkg list-installed
entware-opt - 227000-3
entware-release - 1.0-2
entware-upgrade - 1.0-1
findutils - 4.6.0-3
grep - 3.3-1
libc - 2.27-8
libgcc - 7.4.0-8
libpcre - 8.43-1
libpthread - 2.27-8
librt - 2.27-8
libssp - 7.4.0-8
libstdcpp - 7.4.0-8
locales - 2.27-8
opkg - 2019-01-31-d4ba162b-1
terminfo - 6.1-4
zoneinfo-asia - 2019a-1
zoneinfo-europe - 2019a-1
```

### List Available packages

```console
[~] # opkg list-upgradable
```

## Reference

* [[OpenWrt Wiki] packages:index:start](https://openwrt.org/packages/index/start)
* [[OpenWrt Wiki] Opkg Package Manager](https://openwrt.org/docs/guide-user/additional-software/opkg)
* [QNAP に git や nginx などをインストールする [2018年末版 Entware で Opkg 編] - Qiita](https://qiita.com/KEINOS/items/f832ada264257300e4d7)
