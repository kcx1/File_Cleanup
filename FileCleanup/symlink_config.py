from pathlib import Path
import os
from FileCleanup.file_cleanup import normalize, configuration


# Path to installed config
config_file = Path("config/config.toml").absolute()
# Path declared in config
symlink_dir = normalize(configuration["location"])
symlink = symlink_dir.joinpath("config.toml").absolute()


def main():
    if not symlink_dir.is_dir() and not symlink_dir.exists():
        symlink_dir.mkdir()
    elif not symlink_dir.is_dir() and symlink_dir.exists():
        SystemExit("Configuration location should be a directory not a file or symlink")
    elif symlink.exists():
        SystemExit("Config File Already Exisits")

    if symlink.is_absolute() and config_file.is_absolute():
        print(Path.cwd(), symlink, config_file)
        symlink.symlink_to(config_file, True)
        # os.link(config_file.__str__(), symlink.__str__())


if __name__ == "__main__":
    main()
