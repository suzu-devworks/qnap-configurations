# qnap-file-organizer

I created a tool for QNAP using Python but ran into some issues, which is why I ended up like this.

I think we can give it some more thought, such as stopping the use of python scripts.

---
[![Rye](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/rye/main/artwork/badge.json)](https://rye.astral.sh)

## Table of Contents <!-- omit in toc -->

- [qnap-file-organizer](#qnap-file-organizer)
  - [Environment](#environment)
  - [Move photo files](#move-photo-files)
    - [Setup](#setup)
    - [Fix directory permissions](#fix-directory-permissions)
    - [Build container image](#build-container-image)
    - [Run manually](#run-manually)
  - [Scheduling](#scheduling)
  - [Development](#development)
    - [Install package manager](#install-package-manager)
    - [Create project](#create-project)
    - [First Sync](#first-sync)
    - [install dependency package](#install-dependency-package)
    - [build package](#build-package)

## Environment

- QTS 5.1.7.2770(2024-05-20) on TS-231K
- Container Station 3.0.7.891(2024/05/09)
- Docker version 20.10.27-qnap1, build 662936b

## Move photo files

Organize your jumbled photo files by date.

```console
/Multimedia
  /Camera\ Uploads  ... source folder
  ...

  /Photo/ ... destination
    /2024-01/  
    ...
```

The shooting date is obtained from EXIF.  
That's why I'm using the Pillow library.

### Setup

Enter qnap via ssh.

```shell
cd /share/homes/qnap

mkdir repos
cd repos
```

I want to get the repository, but I don't have git.

I found a useful image:

```shell
docker run -it --rm -v $(pwd):/git alpine/git clone https://github.com/suzu-devworks/qnap-configurations.git
```

### Fix directory permissions

```shell
sudo chown qnap -R qnap-configurations
cd qnap-configurations
```

### Build container image

```shell
cd src/qnap-file-organizer/
docker build . -t qnap-file-organizer
```

### Run manually

```shell
docker run -it --rm \
  -v "/share/Multimedia/Photo:/mnt/dist" \
  -v "/share/Multimedia/Camera Uploads:/mnt/source" \
  qnap-file-organizer 
```

## Scheduling

This configuration is done in docker host.

Even if you set it with `crontab -e`, it seems to disappear.

```shell
sudo vi /etc/config/crontab
```

For example, to start at 15:05 and 20:05 every day:

```crontab
5 15,20 * * * docker run -it -v "/share/Multimedia/Photo:/mnt/dist" -v "/share/Multimedia/Camera Uploads:/mnt/source" qnap-file-organizer >/dev/pts/0 2>&1
```

Redirects to the console device `/dev/pts/0` to output to the container log.

Restarting crond

```shell
sudo crontab /etc/config/crontab
sudo /etc/init.d/crond.sh restart
```

Check the settings

```shell
sudo crontab -l
```

## Development

For actual development, we used python devcontainers, but anything that uses python will do.

### Install package manager

I used [rye](https://rye.astral.sh/guide/installation/), but I plan on only using pip in the container.

```shell
curl -sSf https://rye.astral.sh/get | RYE_TOOLCHAIN=`which python` RYE_INSTALL_OPTION="--yes" bash
```

Since there is no need to download cpython into the container, specify `RYE_TOOLCHAIN`.

Enable it with the following command:

```shell
source $HOME/.rye/env
```

### Create project

First, create a base project.
I'm specifying `--script` options because I might turn it into a command later.

```shell
rye init qnap-file-organizer --script
cd qnap-file-organizer
```

### First Sync

you can use rye sync to get the first synchronization. After that,
Rye will have created a virtualenv in `.venv` and written lockfiles into `requirements.lock` and `requirements-dev.lock`.
<!-- cSpell:word virtualenv -->
<!-- cSpell:word venv -->
<!-- cSpell:word lockfiles -->

```shell
rye sync
```

### install dependency package

Add dependencies with the following command.
Please guess what changes were made to `pyprojecy.toml` after adding the development tools.

```shell
rye add --dev flake8 mypy black isort pyclean
rye add pillow
```
<!-- cSpell:word mypy -->
<!-- cSpell:word isort -->
<!-- cSpell:word pyclean -->

### build package

Not packaged yet.
