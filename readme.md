# Rsync File Sync

A simple Python command-line utility for synchronizing local files and directories with a remote server using **rsync over SSH**.

The script allows you to choose between a saved configuration and a temporary configuration, making it easy to transfer files without repeatedly entering the same connection details.

## Features

- **File and directory synchronization** using rsync.
- **SSH authentication** with a custom private key or an SSH password.
- **Persistent configuration** stored in a JSON file.
- **Temporary configurations** that do not modify saved settings.
- **Flexible remote destinations** that can be changed for individual transfers.
- **Optional configuration updates** when choosing a new remote destination.
- **Transfer progress and partial transfer support** through rsync's `-P` option.
- **No external Python packages required.**

## Requirements

Before using this script, make sure you have:

- Python 3.8 or later.
- `rsync` installed on the local machine.
- SSH client installed and available in your system's `PATH`.
- `sshpass` installed if you plan to authenticate using an SSH password instead of a private key.
- Access to a remote server with rsync installed.
- SSH authentication configured on the remote server.

On Debian or Ubuntu, install the required system packages with:

```bash
sudo apt update
sudo apt install rsync openssh-client python3 sshpass
```

## Installation

Clone the repository or download the Python script to your machine.

```bash
git clone <repository-url>
cd <repository-directory>
```

Replace the placeholders with the actual repository URL and directory name.

Run the script with:

```bash
python3 sync_script.py
```

On the first run, if no configuration file exists, the script will use a temporary configuration.

## Usage

When you start the program, you will be asked to enter the source path:

```text
Insert source path (use /* at the end to sync folder contents):
```

For example:

```text
/home/user/Videos/movie.mkv
```

You can then choose how to configure the transfer.

### 1. Use a saved configuration

If `config.json` exists, you can choose to load it.

The script will ask whether you want to use the remote destination already stored in the configuration.

- Answer `y` to use the saved destination.
- Answer `n` to enter a different destination.

If you enter a new destination, you can choose whether to overwrite the saved value. If you decline, the new destination will only be used for the current transfer.

### 2. Use a temporary configuration

Choose not to load the saved configuration to enter the connection details manually.

You will be asked for:

- Whether to use a custom SSH private key.
- If you don't use a key, whether you want to use an SSH password for your server.
- The remote server address, in `user@host` format.
- The remote destination directory.
- The local source path, which is requested at the beginning.

Temporary settings are not saved to `config.json`.

## Configuration

The configuration file is named `config.json` and is stored in the script's current working directory.

Example:

```json
{
    "use_ssh_key": false,
    "ssh_key": "",
    "ssh_pw": "your_ssh_password",
    "server": "guest@IP_server",
    "remote_path": "/home/user/movie/"
}
```

### Configuration options

| Option | Description |
|---|---|
| `use_ssh_key` | Enables the use of a custom SSH private key when set to `true`. |
| `ssh_key` | Path to the SSH private key. The `~` notation is supported. |
| `ssh_pw` | The SSH password used for authentication when `use_ssh_key` is false. This requires `sshpass` to be installed. |
| `server` | Remote server address in `user@host` format. |
| `remote_path` | Destination directory on the remote server. |

You can edit this file manually at any time.

**Important:** Keep your private SSH key and password secure. The configuration stores only its path or the cleartext password depending on the configuration.

## How synchronization works

The script builds and executes an rsync command equivalent to:

```bash
rsync -rltvP --delay-updates \
    -e "ssh -i ~/.ssh/priv_key" \
    /home/user/Videos/movie.mkv \
    guest@serverIP:/home/user/movie/
```

The SSH key option is included only when a custom private key is enabled. If a password is used instead, the script configures the `-e` option to use `sshpass -e ssh` to automatically provide the password during the transfer.

### Rsync options

| Option | Description |
|---|---|
| `-r` | Recursively transfers directories and their contents. |
| `-l` | Preserves symbolic links as symbolic links. |
| `-t` | Preserves modification times. |
| `-v` | Displays detailed transfer information. |
| `-P` | Shows transfer progress and keeps partially transferred files. |
| `--delay-updates` | Delays updating destination files until the transfer is near completion. |
| `-e` | Specifies the remote shell, in this case SSH. |

The script uses `subprocess.run()` to execute rsync and `check=True` to raise an exception if the command exits with an error.

## Examples

### Transfer a single file

Source:

```text
/home/user/Downloads/movie.mkv
```

Destination:

```text
user@serverIP:/home/user/movie/
```

### Transfer a directory

Provide the source directory path. The `-r` option allows rsync to transfer its contents recursively.

### Use a custom SSH key

Example key path:

```text
~/.ssh/priv_key
```

Make sure the key has appropriate permissions and that the corresponding public key is authorized on the remote server.

## Troubleshooting

### `rsync: command not found`

Install rsync and ensure it is available in your system's `PATH`.

### `Permission denied (publickey)`

Check that:

- The SSH key path is correct.
- The remote username is correct.
- The public key is authorized on the server.
- The SSH user has permission to write to the destination directory.

### `No such file or directory`

Verify that the source exists locally and that the remote destination directory exists or can be accessed by the remote user.

### `CalledProcessError`

The rsync process returned a non-zero exit status. Review the error output printed by rsync to identify the cause.

## Limitations

- The script requires rsync and SSH to be installed separately.
- Temporary configurations are not persisted.
- The configuration file is resolved relative to the current working directory, so running the script from different directories may use different configuration files.
- The current implementation does not automatically create missing remote directories or validate all configuration fields.