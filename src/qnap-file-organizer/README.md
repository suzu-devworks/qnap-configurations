# qnap-file-organizer

I created a tool for QNAP using Python but ran into some issues, which is why I ended up like this.

I think we can give it some more thought, such as stopping the use of python scripts.

---
[![Rye](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/rye/main/artwork/badge.json)](https://rye.astral.sh)


## Table of Contents <!-- omit in toc -->




## Environment

- QTS 5.1.7.2770(2024-05-20) on TS-231K
- Container Station 3.0.7.891(2024/05/09)
  - Docker version 20.10.27-qnap1, build 662936b
  - debian:bookworm-slim (bookworm-20240311-slim, 12.5-slim, 12-slim)


## Move photo files

Organize your jumbled photo files by date.

```
/Multimedia
  /Camera\ Uploads  ... source folder
  ...

  /Photo/ ... destination
    /2024-01/  
    ...
```

The shooting date is obtained from EXIF.<br>
That's why I'm using the Pillow library.

### Setup

...wmm



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

### build package

Not packaged yet.

