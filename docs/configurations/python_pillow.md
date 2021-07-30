# Python3 Pillow Install

## Introduction
QNAP の Python3 で Pillow を使いたいだけなのよ。

### Environmet

- QTS 4.5.1.1495 on TS-231K
    - Pillow 6.2.0-1
- QTS QTS 4.3.3.0868 on TS-219PⅡ
    - Pillow 6.0.0

## Installation Pillow from Opkg

最新なら pillow もあるじゃん。というハナシ。

### Install Entware

まず Entware をインストールして opkg を使えるようにします。

```console
[~] # opkg update
Downloading http://bin.entware.net/armv5sf-k3.2/Packages.gz
Updated list of available packages in /opt/var/opkg-lists/entware

[~] #  opkg upgrade
```
### Install Pillow

```console
[~] #  opkg install python3 python3-pip python3-pillow
```


## [OBSOLETE] Installation Pillow

### Install Entware

まず Entware をインストールして opkg を使えるようにします。

```console
# opkg update
Downloading http://bin.entware.net/armv5sf-k3.2/Packages.gz
Updated list of available packages in /opt/var/opkg-lists/entware

# opkg upgrade
```

### Install Dependency

Pillow のインストールには libjpeg-dev と zlib-dev が必要らしいです。
しかし、Entware には zlib-dev はありますが、libjpeg-devがありません。

Entwareに* -devパッケージはありません（いくつかの例外はありますが）。
Wikiに記述されているようにヘッダをインストールしてください。

> There are no *-dev packages in Entware(with few exceptions)!
Please install headers as described in the wiki:
>
> https://github.com/Entware/Entware/wiki

とりあえず実行用のライブラリを含めてインストールします。

```console
# opkg install libjpeg zlib zlib-dev
Installing libjpeg (9c-2) to root...
Downloading http://bin.entware.net/armv5sf-k3.2/libjpeg_9c-2_armv5-3.2.ipk
Installing zlib (1.2.11-3) to root...
Downloading http://bin.entware.net/armv5sf-k3.2/zlib_1.2.11-3_armv5-3.2.ipk
Installing zlib-dev (1.2.11-3) to root...
Downloading http://bin.entware.net/armv5sf-k3.2/zlib-dev_1.2.11-3_armv5-3.2.ipk
Configuring libjpeg.
Configuring zlib.
Configuring zlib-dev.
```

### Install development tools

```console
# 開発ツール一式？
# opkg install gcc make gawk sed diffutils patch
Installing gcc (6.3.0-1b) to root...
Downloading http://bin.entware.net/armv5sf-k3.2/gcc_6.3.0-1b_armv5-3.2.ipk
Installing libiconv-full (1.11.1-4) to root...
Downloading http://bin.entware.net/armv5sf-k3.2/libiconv-full_1.11.1-4_armv5-3.2.ipk
...

# opkg install autoconf automake libtool-bin
Installing autoconf (2.69-2a) to root...
Downloading http://bin.entware.net/armv5sf-k3.2/autoconf_2.69-2a_armv5-3.2.ipk
Installing m4 (1.4.18-1a) to root...
Downloading http://bin.entware.net/armv5sf-k3.2/m4_1.4.18-1a_armv5-3.2.ipk
Installing perl (5.28.1-1) to root...
```

### Setup temporary directory

QNAP は大きな容量が必要なものは /share/MD0_DATA へ逃がす必要があります。

```console
# df -h
Filesystem                Size      Used Available Use% Mounted on
/dev/ramdisk             32.9M     16.7M     16.2M  51% /
tmpfs                    64.0M    292.0k     63.7M   0% /tmp
/dev/sda4               371.0M    359.5M     11.5M  97% /mnt/ext
/dev/md9                509.5M    151.9M    357.6M  30% /mnt/HDA_ROOT
/dev/md0                  1.8T    118.1G      1.7T   6% /share/MD0_DATA
tmpfs                    16.0M     64.0k     15.9M   0% /share/MD0_DATA/.samba/lock/msg.lock
tmpfs                    16.0M         0     16.0M   0% /mnt/ext/opt/samba/private/msg.sock
tmpfs                     1.0M         0      1.0M   0% /mnt/rf/nd
/dev/sdq1               931.5G    204.7G    726.8G  22% /share/external/sdq1

# export TMPDIR=/share/MD0_DATA/.workspace/tmp/
# mkdir -p ${TMPDIR}/{cache,build}
```

### Configure libjpeg-dev from source code.

libjpeg-dev が無いため、libjpegソースコードからヘッダファイルを用意する必要があります。
次のサイトでバージョンが一致しそうなファイルを取得します。

* http://www.ijg.org/files/

「libjpeg_9c-2_armv5-3.2.ipk」に近いバージョン「jpegsrc.v9c.tar.gz 」を取得します。

```console
# mkdir -p /opt/usr/src
# cd /opt/usr/src
# wget http://www.ijg.org/files/jpegsrc.v9c.tar.gz   
--2019-06-17 21:58:01--  http://www.ijg.org/files/jpegsrc.v9c.tar.gz
Resolving www.ijg.org... 104.24.123.172, 104.24.122.172, 2606:4700:30::6818:7aac, ...
Connecting to www.ijg.org|104.24.123.172|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 1028134 (1004K) [application/x-gzip]
Saving to: ‘jpegsrc.v9c.tar.gz’

jpegsrc.v9c.tar.gz             100%[====================================================>]   1004K  1.16MB/s   in 0.8s   

2019-06-17 21:58:02 (1.16 MB/s) - ‘jpegsrc.v9c.tar.gz’ saved [1028134/1028134]

# tar -xvf jpegsrc.v9c.tar.gz 
# cd jpeg-9c/

# ./configure
checking build system type... armv5tel-unknown-linux-gnueabi
checking host system type... armv5tel-unknown-linux-gnueabi
checking target system type... armv5tel-unknown-linux-gnueabi
...
configure: creating ./config.status
config.status: creating Makefile
config.status: creating libjpeg.pc
config.status: creating jconfig.h
config.status: executing depfiles commands
config.status: executing libtool commands
```

And ...
マケタ感たっぷり。

```console
# ln -s arm-openwrt-linux-gnueabi-gcc /opt/bin/arm-none-linux-gnueabi-gcc
```

### Install Pillow by pip

```console
# . /etc/profile.d/python3.bash

# export TMPDIR=/opt/tmp/
# mkdir -p ${TMPDIR}/{cache,build}

# CC=gcc CFLAGS="-I/opt/include -I/opt/usr/src/jpeg-9c" pip3 install --no-cache-dir  --build=${TMPDIR}/build/ pillow
Collecting pillow
  Downloading https://files.pythonhosted.org/packages/81/1a/6b2971adc1bca55b9a53ed1efa372acff7e8b9913982a396f3fa046efaf8/Pillow-6.0.0.tar.gz (29.5MB)
     |████████████████████████████████| 29.5MB 1.4MB/s 
Installing collected packages: pillow
  Running setup.py install for pillow ... done
Successfully installed pillow-6.0.0

# pip3 list
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

きたー。


## Trace of hardship

### <SOLVED>ERROR: No space left on device

まずは 「App Center」で「Python3」がインストールされている状態で…

```console
# . /etc/profile.d/python3.bash

# mkdir -p ${TMPDIR}/{cache,build}

# . pip3 --version
pip 19.1.1 from /share/MD0_DATA/.qpkg/Python3/src/lib/python3.5/site-packages/pip (python 3.5)

# pip3 list                                                                                                                                                
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

pip だの setuptools だのがやたら新しい気がする。

```console
# pip3 install pillow
Collecting pillow
  Downloading https://files.pythonhosted.org/packages/81/1a/6b2971adc1bca55b9a53ed1efa372acff7e8b9913982a396f3fa046efaf8/c.tar.gz (29.5MB)
     |████████████████████████████████| 29.5MB 1.5MB/s 
ERROR: Could not install packages due to an EnvironmentError: [Errno 28] No space left on device
```

なんだと？
QTSは、ほぼramdiskなはずなので、大きな作業領域はHDDに取らないと無理なはずだ。

### <SOLVED>ERROR: The headers or library files could not be found for jpeg,

```console
# . /etc/profile.d/python3.bash

# export TMPDIR=/share/MD0_DATA/.workspace/tmp/
# mkdir -p ${TMPDIR}/{cache,build}

# pip3 install --cache-dir=${TMPDIR}/cache/ --build=${TMPDIR}/build/ pillow
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
ERROR: Command "/share/MD0_DATA/.qpkg/Python3/src/bin/python3 -u -c 'import setuptools, tokenize;__file__='"'"'/share/MD0_DATA/.workspace/tmp/build/pillow/setup.py'"'"';f=getattr(tokenize, '"'"'open'"'"', open)(__file__);code=f.read().replace('"'"'\r\n'"'"', '"'"'\n'"'"');f.close();exec(compile(code, __file__, '"'"'exec'"'"'))' install --record /share/MD0_DATA/.workspace/tmp/pip-record-49p4x2kz/install-record.txt --single-version-externally-managed --compile" failed with error code 1 in /share/MD0_DATA/.workspace/tmp/build/pillow/
```

ほう、libjpegが無いだと...
もう opkg いれるしかないじゃん。

### <SOLVED>ERROR: unable to execute 'arm-none-linux-gnueabi-gcc': No such file or directory

```console
# . /etc/profile.d/python3.bash

# mkdir -p /share/MD0_DATA/.workspace/tmp/build
# export TMPDIR=/share/MD0_DATA/.workspace/tmp/

# opkg install libjpeg
# opkg install zlib
# opkg install zlib-dev 

# jpeg-9c で ./configure しないと jconfig.h が無いヨ
# ln -s /share/MD0_DATA/.workspace/src/jconfig.h /opt/include/
# ln -s /share/MD0_DATA/.workspace/src/jmorecfg.h /opt/include/
# ln -s /share/MD0_DATA/.workspace/src/jpeglib.h /opt/include/

# CC=gcc CFLAGS="-I/opt/include -I" pip3 install --no-cache-dir --build=${TMPDIR}/build/ pillow
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
ERROR: Command "/share/MD0_DATA/.qpkg/Python3/src/bin/python3 -u -c 'import setuptools, tokenize;__file__='"'"'/share/MD0_DATA/.workspace/tmp/build/pillow/setup.py'"'"';f=getattr(tokenize, '"'"'open'"'"', open)(__file__);code=f.read().replace('"'"'\r\n'"'"', '"'"'\n'"'"');f.close();exec(compile(code, __file__, '"'"'exec'"'"'))' install --record /share/MD0_DATA/.workspace/tmp/pip-record-ktc23ife/install-record.txt --single-version-externally-managed --compile" failed with error code 1 in /share/MD0_DATA/.workspace/tmp/build/pillow/
```

少しだけ進みました。

'arm-none-linux-gnueabi-gcc' ってCROSSコンパイラが動いています。
でもそんなファイルはありません。

## Reference

* https://github.com/python-pillow/Pillow
* https://bin.entware.net/armv5sf-k3.2/Packages.html
* [Compile packages from sources - Entware](https://github.com/Entware/Entware/wiki/Compile-packages-from-sources)
