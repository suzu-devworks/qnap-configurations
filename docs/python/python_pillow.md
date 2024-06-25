# Python Pillow install on QNAP

QNAP で Python の Pillow を使いたい。

## Table of Contents <!-- omit in toc -->

- [Python Pillow install on QNAP](#python-pillow-install-on-qnap)
  - [Install Pillow on Container Station](#install-pillow-on-container-station)
    - [Use `Python:alpine` container](#use-pythonalpine-container)
    - [Use `Python:bookworm-slim` container](#use-pythonbookworm-slim-container)
    - [Use `debian:bookworm-slim` container](#use-debianbookworm-slim-container)
    - [\[ERROR\] The headers or library files could not be found for zlib](#error-the-headers-or-library-files-could-not-be-found-for-zlib)
    - [\[ERROR\] command 'gcc' failed: No such file or directory](#error-command-gcc-failed-no-such-file-or-directory)
    - [\[ERROR\] No module named 'PIL'](#error-no-module-named-pil)
  - [\[OBSOLETE\] Install Pillow with OPKG binary](#obsolete-install-pillow-with-opkg-binary)
    - [setup for python bynary](#setup-for-python-bynary)
    - [Install Pillow binaries](#install-pillow-binaries)
  - [\[OBSOLETE\] Install Pillow with OPKG develop tools](#obsolete-install-pillow-with-opkg-develop-tools)
    - [setup for develop tools](#setup-for-develop-tools)
    - [Install dependencies](#install-dependencies)
    - [Install development tools](#install-development-tools)
    - [Setup temporary directory](#setup-temporary-directory)
    - [Configure libjpeg-dev from source code](#configure-libjpeg-dev-from-source-code)
    - [Install Pillow by pip](#install-pillow-by-pip)
  - [\[UNSUCCESSFUL\] Install from App Center](#unsuccessful-install-from-app-center)
    - [\[ERROR\] No space left on device](#error-no-space-left-on-device)
    - [\[ERROR\] The headers or library files could not be found for jpeg](#error-the-headers-or-library-files-could-not-be-found-for-jpeg)
    - [\[ERROR\] unable to execute 'arm-none-linux-gnueabi-gcc': No such file or directory](#error-unable-to-execute-arm-none-linux-gnueabi-gcc-no-such-file-or-directory)

## Install Pillow on Container Station

- QTS 5.1.7.2770(2024-05-20) on TS-231K
- Container Station 3.0.7.891(2024/05/09)

さらに更新して Entware が　App Center　からインストールできなくなりました。

それなら、せっかくなので　Container Station (docker) でやれば苦労しないんじゃないとかと（浅はかにも）

### Use `Python:alpine` container

Dockerfile はこんな感じ

```dockerfile
FROM python:3-alpine as production
WORKDIR /app

RUN apk add --no-cache --virtual .build-deps build-base jpeg-dev zlib-dev
RUN apk add --no-cache libjpeg-turbo

COPY . .
RUN pip install --no-cache-dir -r requirements.lock

RUN apk del .build-deps

CMD [ "sh", "/app/scripts/exec.sh", "/mnt/dist", "/mnt/source" ]
```

これでビルドするとイメージサイズはこんな感じ

```shell
docker build . -t test-alpine
```

```shell
docker image ls test-alpine
```

```console
test-alpine   latest          06aec68c5c68   31 seconds ago   206MB
```

### Use `Python:bookworm-slim` container

Dockerfile はこんな感じ

```dockerfile
FROM python:3-slim as production
WORKDIR /app

RUN set -x \
        && apt update \
        && apt install -y gcc zlib1g-dev libjpeg-dev

COPY . .
RUN pip install --no-cache-dir -r requirements.lock

RUN set -x \
        && apt clean \
        && rm -rf /var/lib/apt/lists/*

CMD [ "sh", "/app/scripts/exec.sh", "/mnt/dist", "/mnt/source" ]
```

これでビルドするとイメージサイズはこんな感じ

```shell
docker build . -t test-slim
```

```shell
docker image ls test-slim
```

```console
test-slim     latest          4e6a35ce95e8   29 seconds ago   266MB
```

### Use `debian:bookworm-slim` container

Dockerfile はこんな感じ

```dockerfile
FROM debian:bookworm-slim as production
WORKDIR /app

RUN set -x \
        && apt update \
        && apt install -y python3 python-is-python3 python3-pillow
        && apt clean \
        && rm -rf /var/lib/apt/lists/*

COPY . .

CMD [ "sh", "/app/scripts/exec.sh", "/mnt/dist", "/mnt/source" ]
```

これでビルドするとイメージサイズはこんな感じ

```shell
docker build . -t test-debian
```

```shell
docker image ls test-debian
```

```console
test-debian   latest          0e0e09f96c5c   10 seconds ago   215MB
```

### [ERROR] The headers or library files could not be found for zlib

Dockerfile はこんな感じ

```dockerfile
FROM python:3-alpine as production
WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.lock

CMD [ "sh", "/app/scripts/exec.sh", "/mnt/dist", "/mnt/source" ]
```

そしてビルドすると

```shell
docker build . -t pillow-alpine
```

```console
      The headers or library files could not be found for zlib,
      a required dependency when compiling Pillow from source.
```

またもやヘッダ、このあと　`zlib-dev` をインストールしてもこんどは `jpeg`

```console
      The headers or library files could not be found for jpeg,
      a required dependency when compiling Pillow from source.
```

### [ERROR] command 'gcc' failed: No such file or directory

Dockerfile はこんな感じ

```dockerfile
FROM python:3-alpine as production
WORKDIR /app

RUN apk add --no-cache jpeg-dev zlib-dev

COPY . .
RUN pip install --no-cache-dir -r requirements.lock

CMD [ "sh", "/app/scripts/exec.sh", "/mnt/dist", "/mnt/source" ]
```

そしてビルドすると

```shell
docker build . -t pillow-alpine
```

```console
     error: command 'gcc' failed: No such file or directory
      [end of output]
  
    note: This error originates from a subprocess, and is likely not a problem with pip.
    ERROR: Failed building wheel for pillow
```

なるほどやはりビルドするための開発ツール一式が必要になるらしい。

### [ERROR] No module named 'PIL'

ビルドしないで基本パッケージですませたほうがイメージサイズが小さくなるような気がしたのでやってみた。

```dockerfile
FROM python:3-alpine as production
WORKDIR /app

RUN apk add --no-cache python3 py3-pillow

COPY . .

CMD [ "sh", "/app/scripts/exec.sh", "/mnt/dist", "/mnt/source" ]
```

```shell
docker build . -t pillow-alpine
```

これで image はできますが実行するとPILが読み込めないとエラーになります。

```shell
docker run -it --rm pillow-alpine
```

<!-- cSpell:disable -->
```console
Traceback (most recent call last):
  File "/app/scripts/move_photo_files.py", line 21, in <module>
    from PIL import Image
ModuleNotFoundError: No module named 'PIL'
```
<!-- cSpell:ensable -->

## [OBSOLETE] Install Pillow with OPKG binary

- QTS 4.5.1.1495 on TS-231K
- Pillow 6.2.0-1

最新の OPKG に pillow があるじゃん。

### setup for python bynary

- 「App Center」で「Python3」は **アンインストール** しておきます。
- Entware をインストールして opkg を使えるようにします。

### Install Pillow binaries

```shell
opkg install python3 python3-pip python3-pillow
```

## [OBSOLETE] Install Pillow with OPKG develop tools

- QTS QTS 4.3.3.0868 on TS-219PⅡ
- Pillow 6.0.0

### setup for develop tools

- 「App Center」で「Python3」をインストールしておきます。
- Entware をインストールして opkg を使えるようにします。

### Install dependencies

Pillow のインストールには libjpeg-dev と zlib-dev が必要らしいです。
しかし、Entware には zlib-dev はありますが、libjpeg-devがありません。

Entwareに* -devパッケージはありません（いくつかの例外はありますが）
Wikiに記述されているようにヘッダをインストールしてください。

> There are no *-dev packages in Entware(with few exceptions)!
Please install headers as described in the wiki:
>
> <https://github.com/Entware/Entware/wiki>

とりあえず実行用のライブラリを含めてインストールします。

```shell
opkg install libjpeg zlib zlib-dev
```

### Install development tools

開発ツール一式をインストール

```shell
opkg install gcc make gawk sed diffutils patch autoconf automake libtool-bin
```

### Setup temporary directory

QNAP は大きな容量が必要なものは /share/MD0_DATA へ逃がす必要があります。

```shell
export TMPDIR=/share/MD0_DATA/.workspace/tmp/
mkdir -p ${TMPDIR}/{cache,build}
```

### Configure libjpeg-dev from source code

libjpeg-dev が無いため、libjpegソースコードからヘッダファイルを用意する必要があります。
次のサイトでバージョンが一致しそうなファイルを取得します。

- <http://www.ijg.org/files/>

`libjpeg_9c-2_armv5-3.2.ipk` に近いバージョン `jpegsrc.v9c.tar.gz` を取得します。

```shell
mkdir -p /opt/usr/src
cd /opt/usr/src
wget http://www.ijg.org/files/jpegsrc.v9c.tar.gz   
```

<!-- cSpell:disable -->
```console
--2019-06-17 21:58:01--  http://www.ijg.org/files/jpegsrc.v9c.tar.gz
Resolving www.ijg.org... 104.24.123.172, 104.24.122.172, 2606:4700:30::6818:7aac, ...
Connecting to www.ijg.org|104.24.123.172|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 1028134 (1004K) [application/x-gzip]
Saving to: ‘jpegsrc.v9c.tar.gz’

jpegsrc.v9c.tar.gz             100%[====================================================>]   1004K  1.16MB/s   in 0.8s   

2019-06-17 21:58:02 (1.16 MB/s) - ‘jpegsrc.v9c.tar.gz’ saved [1028134/1028134]
```
<!-- cSpell:enable -->

解答して.configureでヘッダファイルを生成します。

```shell
tar -xvf jpegsrc.v9c.tar.gz 
cd jpeg-9c/
./configure
```
<!-- cSpell:word jpegsrc -->

それでも、そもそものgccがないのでやむなく...

```shell
ln -s arm-openwrt-linux-gnueabi-gcc /opt/bin/arm-none-linux-gnueabi-gcc
```
<!-- cSpell:word openwrt -->
<!-- cSpell:word gnueabi -->

### Install Pillow by pip

あらためてターミナルに環境を読み込みます。

```shell
. /etc/profile.d/python3.bash
```

ワークディレクトリを作成します。

```shell
export TMPDIR=/opt/tmp/
mkdir -p ${TMPDIR}/{cache,build}
```

Pillow のインストール(build)を実行します。

```shell
CC=gcc CFLAGS="-I/opt/include -I/opt/usr/src/jpeg-9c" pip3 install --no-cache-dir  --build=${TMPDIR}/build/ pillow
```

<!-- cSpell:disable -->
```console
Collecting pillow
  Downloading https://files.pythonhosted.org/packages/81/1a/6b2971adc1bca55b9a53ed1efa372acff7e8b9913982a396f3fa046efaf8/Pillow-6.0.0.tar.gz (29.5MB)
     |████████████████████████████████| 29.5MB 1.4MB/s 
Installing collected packages: pillow
  Running setup.py install for pillow ... done
Successfully installed pillow-6.0.0
```
<!-- cSpell:enable -->

確認してみよう。

```shell
pip3 list
```

<!-- cSpell:disable -->
```console
 Package      Version
------------ -------
Click        7.0    
Flask        1.0.3  
itsdangerous 1.1.0  
Jinja2       2.10.1 
MarkupSafe   1.1.1  
Pillow       6.0.0  
pip          19.1.1 
setuptools   41.0.1 
Werkzeug     0.15.4 
```
<!-- cSpell:enable -->

きたー♪───Ｏ（≧∇≦）Ｏ────♪

-----

## [UNSUCCESSFUL] Install from App Center

- QTS QTS 4.3.3.0868 on TS-219PⅡ
- Pillow 6.0.0

### [ERROR] No space left on device

「App Center」で「Python3」をインストールしておきます。

ターミナルに環境を読み込みます。

```shell
. /etc/profile.d/python3.bash
```

ワークディレクトリを作成します。

```shell
mkdir -p ${TMPDIR}/{cache,build}
```

pip でパッケージの状況を確認します。

```shell
pip3 --version
```

```console
pip 19.1.1 from /share/MD0_DATA/.qpkg/Python3/src/lib/python3.5/site-packages/pip (python 3.5)
```

```shell
pip list
```

<!-- cSpell:disable -->
```console
Package      Version
------------ -------
Click        7.0    
Flask        1.0.3  
itsdangerous 1.1.0  
Jinja2       2.10.1 
MarkupSafe   1.1.1  
pip          19.1.1 
setuptools   41.0.1 
Werkzeug     0.15.4 
```
<!-- cSpell:enable -->

Pillow のインストールを実行します。

```shell
pip3 install pillow
```

<!-- cSpell:disable -->
```console
Collecting pillow
  Downloading https://files.pythonhosted.org/packages/81/1a/6b2971adc1bca55b9a53ed1efa372acff7e8b9913982a396f3fa046efaf8/c.tar.gz (29.5MB)
     |████████████████████████████████| 29.5MB 1.5MB/s 
ERROR: Could not install packages due to an EnvironmentError: [Errno 28] No space left on device
```
<!-- cSpell:enable -->

空きスペースが足りない？

QTS は大きな作業領域は HDD に取らないと無理なはずです。

### [ERROR] The headers or library files could not be found for jpeg

「App Center」で「Python3」をインストールしておきます。

ターミナルに環境を読み込みます。

```shell
. /etc/profile.d/python3.bash
```

HDDへワークディレクトリを作成します。

```shell
export TMPDIR=/share/MD0_DATA/.workspace/tmp/
mkdir -p ${TMPDIR}/{cache,build}
```

Pillow のインストールを実行します。

```shell
pip3 install --cache-dir=${TMPDIR}/cache/ --build=${TMPDIR}/build/ pillow
```

<!-- cSpell:disable -->
```console
Collecting pillow
  Downloading https://files.pythonhosted.org/packages/81/1a/6b2971adc1bca55b9a53ed1efa372acff7e8b9913982a396f3fa046efaf8/Pillow-6.0.0.tar.gz (29.5MB)
     |████████████████████████████████| 29.5MB 112kB/s 
Installing collected packages: pillow
  Running setup.py install for pillow ... error
    ERROR: Complete output from command /share/MD0_DATA/.qpkg/Python3/src/bin/python3 -u -c 'import setuptools, tokenize;__file__='"'"'/share/MD0_DATA/.workspace/tmp/build/pillow/setup.py'"'"';f=getattr(tokenize, '"'"'open'"'"', open)(__file__);code=f.read().replace('"'"'\r\n'"'"', '"'"'\n'"'"');f.close();exec(compile(code, __file__, '"'"'exec'"'"'))' install --record /share/MD0_DATA/.workspace/tmp/pip-record-49p4x2kz/install-record.txt --single-version-externally-managed --compile:
    ERROR: running install

... 

    The headers or library files could not be found for jpeg,
    a required dependency when compiling Pillow from source.
    
    Please see the install instructions at:
       https://pillow.readthedocs.io/en/latest/installation.html
... 
    ----------------------------------------
ERROR: Command "..." failed with error code 1 in /share/MD0_DATA/.workspace/tmp/build/pillow/
```
<!-- cSpell:enable -->

libjpeg のヘッダーが無いとエラーになります。
開発ツールチェインが必要となると、App Center だけでは不可能ということでになります。

### [ERROR] unable to execute 'arm-none-linux-gnueabi-gcc': No such file or directory

「App Center」で「Python3」をインストールしておきます。

加えてEntware をインストールして opkg を使えるようにします。

- <https://github.com/Entware/Entware/wiki/Install-on-QNAP-NAS>

ターミナルに環境を読み込みます。

```shell
. /etc/profile.d/python3.bash
```

ワークディレクトリを作成します。

```shell
export TMPDIR=/share/MD0_DATA/.workspace/tmp/
mkdir -p ${TMPDIR}/{cache,build}
```

ビルドに必要なライブラリをインストールします。

```shell
opkg install libjpeg zlib zlib-dev 
```
<!-- cSpell:word libjpeg -->

ビルド途中でヘッダファイルが無いとエラーになるため適時ファイルを探して対応しました。

```shell
# jpeg-9c で ./configure しないと jconfig.h が無いヨ
ln -s /share/MD0_DATA/.workspace/src/jconfig.h /opt/include/
ln -s /share/MD0_DATA/.workspace/src/jmorecfg.h /opt/include/
ln -s /share/MD0_DATA/.workspace/src/jpeglib.h /opt/include/
```
<!-- cSpell:word jconfig -->
<!-- cSpell:word jmorecfg -->
<!-- cSpell:word jpeglib -->

Pillow のインストール(build)を実行します。

```shell
CC=gcc CFLAGS="-I/opt/include -I" pip3 install --no-cache-dir --build=${TMPDIR}/build/ pillow
```

<!-- cSpell:disable -->
```console
Collecting pillow
  Downloading https://files.pythonhosted.org/packages/81/1a/6b2971adc1bca55b9a53ed1efa372acff7e8b9913982a396f3fa046efaf8/Pillow-6.0.0.tar.gz (29.5MB)
     |████████████████████████████████| 29.5MB 1.5MB/s 
Installing collected packages: pillow
  Running setup.py install for pillow ... error
    ERROR: Complete output from command /share/MD0_DATA/.qpkg/Python3/src/bin/python3 -u -c 'import setuptools, tokenize;__file__='"'"'/share/MD0_DATA/.workspace/tmp/build/pillow/setup.py'"'"';f=getattr(tokenize, '"'"'open'"'"', open)(__file__);code=f.read().replace('"'"'\r\n'"'"', '"'"'\n'"'"');f.close();exec(compile(code, __file__, '"'"'exec'"'"'))' install --record /share/MD0_DATA/.workspace/tmp/pip-record-ktc23ife/install-record.txt --single-version-externally-managed --compile:
    ERROR: running install
    running build
    ...
    running build_ext
    building 'PIL._imaging' extension
    creating build/temp.linux-armv5tel-3.5
    creating build/temp.linux-armv5tel-3.5/src
    creating build/temp.linux-armv5tel-3.5/src/libImaging
    gcc -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -I/opt/include -I -fPIC -DHAVE_LIBJPEG -DHAVE_LIBZ -DPILLOW_VERSION="6.0.0" -I/share/MD0_DATA/.workspace/tmp/build/pillow/src/libImaging -I/share/MD0_DATA/.qpkg/Entware/include -I/share/MD0_DATA/.qpkg/Python3/src/include -I/mnt/ext/usr/local/include -I/share/MD0_DATA/.qpkg/Python3/src/include/python3.5m -c src/_imaging.c -o build/temp.linux-armv5tel-3.5/src/_imaging.o
    ...
    building 'PIL._imagingmorph' extension
    gcc -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -I/opt/include -I -fPIC -I/share/MD0_DATA/.workspace/tmp/build/pillow/src/libImaging -I/share/MD0_DATA/.qpkg/Entware/include -I/share/MD0_DATA/.qpkg/Python3/src/include -I/mnt/ext/usr/local/include -I/share/MD0_DATA/.qpkg/Python3/src/include/python3.5m -c src/_imagingmorph.c -o build/temp.linux-armv5tel-3.5/src/_imagingmorph.o
    arm-none-linux-gnueabi-gcc -shared -L/home/vagrant/python-x19/cross_build/lib -L/opt/cross-project/arm/marvell/arm-none-linux-gnueabi/lib -I/opt/include -I build/temp.linux-armv5tel-3.5/src/_imagingmorph.o -L/share/MD0_DATA/.qpkg/Python3/src/lib -L/lib -L/mnt/ext/usr/local/lib -L/mnt/ext/usr/lib -o build/lib.linux-armv5tel-3.5/PIL/_imagingmorph.cpython-35m-arm-linux-gnueabi.so
    unable to execute 'arm-none-linux-gnueabi-gcc': No such file or directory
    error: command 'arm-none-linux-gnueabi-gcc' failed with exit status 1
    ----------------------------------------

ERROR: Command "..." failed with error code 1 in /share/MD0_DATA/.workspace/tmp/build/pillow/
```
<!-- cSpell:enable -->

少しだけ進みました...が

`arm-none-linux-gnueabi-gcc` という CROSSコンパイラ を要求しています。
そんなファイルはありません。
