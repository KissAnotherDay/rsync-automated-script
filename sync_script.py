import json
import os
import subprocess


def syncr(path_source):
    config_file = "config.json"

    use_saved = False

    if os.path.exists(config_file):
        use_saved = input("Do you want to load the configuration from config.json? (y/n): ").lower() in ("y", "yes")

    if use_saved:
        
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)

        
        use_current_path = input("Do you want to use the destination saved in config.json? (y/n): ").lower() in ("y", "yes")

        if use_current_path:
            remote_path = config["remote_path"]

        else:
            remote_path = input("Insert remote destination path (start with /): ")

            overwrite = input("Do you want to overwrite the saved destination in config.json? (y/n): ").lower() in ("y", "yes")

            if overwrite:
                config["remote_path"] = remote_path

                with open(config_file, "w", encoding="utf-8") as f:
                    json.dump(config, f, indent=4)

    else:
        
        ab = input("You log in server with SSH key? (y/n): ").lower()

        config = {
            "use_ssh_key": ab in ("y", "yes"),
            "ssh_key": "",
            "server": input("Insert your server (user@IP_server): "),
            "remote_path": ""
        }

        if config["use_ssh_key"]:
            config["ssh_key"] = input("Insert path for your private SSH key: ")

        remote_path = input("Insert remote destination path (start with /): ")

    command = ["rsync", "-rltvP", "--delay-updates"]

    if config["use_ssh_key"]:
        ssh_key = os.path.expanduser(config["ssh_key"])
        command.extend(["-e", f"ssh -i {ssh_key}"])

    command.extend([path_source,f'{config["server"]}:{remote_path}'])

    subprocess.run(command, check=True)


def main():
    print("== WELCOME ==")
    print("Sync files with rsync\n")
    print()
    path_source = input("Insert source path (use /* at the end to sync folder contents): ")
    syncr(path_source)


if __name__ == "__main__":
    main()
