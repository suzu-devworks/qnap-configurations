# qnap-configurations

- [qnap-configurations](#qnap-configurations)
  - [Environment](#environment)
  - [Create a container](#create-a-container)
  - [Clone repository](#clone-repository)
  - [Configuration Python](#configuration-python)
    - [Use python3 in debian package](#use-python3-in-debian-package)
    - [Use venv](#use-venv)
  - [Test Run](#test-run)
  - [File movement settings](#file-movement-settings)
  - [Scheduling](#scheduling)

## Environment

- QTS 5.1.5.2679(2024-02-29) on TS-231K

## Create a container

Create a container using Container Station: 

1. Creating a container
   - image: `debian:bookworm-slim`
2. Container settings
   - Advanced Settings
   - \> Storage
   - \> Add Volume (Bind path to mounted host)
     - Host: /Multimedia
     - Container: /mnt/Multimedia
     - Mode: RW
3. Create container 
   - wait until running


## Clone repository

Enter the Docker container you just ran and start a console session:

```shell
docker exec -it <container-id> bash
```

First update apt. All commands after this are for root user:

```shell
apt update 
```

And I don't have git.

```shell
apt install -y git
```

Once you have git installed, you can finally clone it.

```shell
mkdir -p /home/qnap
cd /home/qnap

git clone https://github.com/suzu-devworks/qnap-configurations.git
```

## Configuration Python

### Use python3 in debian package 

All you need in python3 are the following three packages:

```shell
apt install -y python3 python3-pillow
```

Check the python path settings in `move_photo_files.sh`

```shell
python=/usr/bin/python3
```

### Use venv

All you need in python3 are the following three packages:

```shell
sudo apt install -y python3 python3-venv python3-pip
```

I used venv, but the packaged python might be faster.

```shell
python -m venv .venv
. .venv/bin/activate

python -m pip install --upgrade pip
pip install -y pdm
```

Restore package.

```shell
pdm install
```

Check the python path settings in `move_photo_files.sh`

```shell
root_dir=$(cd $(dirname ${0})/../ && pwd)
python=${root_dir}/.venv/bin/python
```

## Test Run

I'll try running it anyway.

```shell
bin/move_photo_files.sh
```

The folder will be created (I'll do something about it eventually) but the files will not be moved and only a notification will be sent.


## File movement settings

File movement has been disabled in the python code, so enable it.

In `move_photo_files.py` and `move_other_image_files.py`

```py
def move_file(source: Path, dest: Path):
    """Moves source photo file to destination path.

    Args
        source: Source image file path
        dest: Destination directory path
    """
    dest.mkdir(mode=0o777, parents=True, exist_ok=True)

    try:
        # shutil.copy2(str(source), str(dest))
        # shutil.move(str(source), str(dest))　 # <- This one
        logger.debug("move: {} -> {}".format(source, dest))

    except shutil.Error as e:
        logger.warning(repr(e))
```

## Scheduling

cron and vim are also not included.

```shell
apt install -y cron vim
```

```shell
export EDITOR=vi
crontab -e
```

For example, if it starts every 12 hours:

```crontab
5 20/12 * * * /home/admin/repos/qnap-configurations/bin/move_photo_files.sh > /dev/stdout 2>&1
```
