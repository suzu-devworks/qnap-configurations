# qnap-configurations

- [qnap-configurations](#qnap-configurations)
  - [Envisonment](#envisonment)
  - [Create a container](#create-a-container)
  - [Clone repository](#clone-repository)
  - [Configuration Python](#configuration-python)
    - [Use python3 in debian package](#use-python3-in-debian-package)
    - [Use venv](#use-venv)
  - [Scheduling](#scheduling)

## Envisonment

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
docker exec -it <containerid> bash
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
git clone https://github.com/suzu-devworks/qnap-configurations.git
```

## Configuration Python

### Use python3 in debian package 

All you need in python3 are the following three packages:

```shell
sudo apt install -y python3 python3-pillow
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

## Scheduling

Crom and vim are also not included.

```shell
apt install -y cron vim
```

```shell
export EDITOR=vi
crontab -e
```

For example, if it starts every 12 hours:

```crontab
5 */12 * * * /home/admin/repos/qnap-configurations/bin/move_photo_files.sh > /dev/stdout 2>&1
```
