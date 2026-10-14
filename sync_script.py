import json
import os
import subprocess


def syncr(path_source):
    config_file = "config.json"

    use_saved = False

    if os.path.exists(config_file):
        ac=input("Do you want to load the configuration from config.json? (y/n): ").lower()

        if ac=="y" or ac=="yes":
            use_saved=True

    try:
        if use_saved!=False:

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
                        json.dump(config, f, indent=5)

        else:

            use_ssh=False

            ab = input("You log in server with SSH key? (y/n): ").lower()
            ssh_key=""
            ssh_pw=""

            if ab=="y" or ab=="yes":
                use_ssh=True
                ssh_key=input("Insert path for your private SSH key: ")
            else:
                af=input("Do you have a password ssh for your server? (y/n): ")
                if af=="y" or af=="yes":
                    ssh_pw=input("Insert your ssh password: ")

            server=input("Insert your server (user@server): ")
            remote_path = input("Insert remote destination path (start with /): ")

            config = {
                "use_ssh_key": use_ssh,
                "ssh_key": ssh_key,
                "ssh_pw":ssh_pw,
                "server": server,
                "remote_path": remote_path
            }

            save_config = input("Do you want save the current settings? (y/n): ").lower()

            if save_config == "y" or save_config == "yes":
                with open(config_file, "w", encoding="utf-8") as f:
                    json.dump(config, f, indent=5)

                print("Configuration saved successfully!!!")

        command = ["rsync", "-rltvP", "--delay-updates"]

    except Exception as  e:
        print(e)
        print()
        return main()

    if config["use_ssh_key"]:
        ssh_key = os.path.expanduser(config["ssh_key"])
        command.extend(["-e", f"ssh -i '{ssh_key}'"])
    else:
        if config["ssh_pw"]!="":
            command.extend(["-e",f"sshpass -e ssh"])
            os.environ["SSHPASS"] = config["ssh_key"]

    command.extend([path_source, f'{config["server"]}:{remote_path}'])

    subprocess.run(command, check=True)


def main():
    print("=== WELCOME ===\nSync files with rsync")
    print()
    path_source = input("Insert source path (use /* at the end to sync folder contents): ")
    syncr(path_source)


if __name__ == "__main__":
    main()
