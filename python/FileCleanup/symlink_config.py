from pathlib import Path
from FileCleanup.file_cleanup import normalize, configuration


# Path this script is running in
script_path = Path(__file__).parent
# Path to installed config
config_file = script_path.joinpath("config/config.toml").absolute()
# Path declared in config
symlink_dir = normalize(configuration["location"])
# File to be symlinked
symlink = symlink_dir.joinpath("config.toml").absolute()


def main() -> None:
    """
    Create a symlink to the user's configuration file to make editing the file easier.

    Returns:
        None
    """

    if symlink.exists():
        SystemExit("Config File Already Exisits")
    elif not symlink_dir.is_dir() and not symlink_dir.exists():
        symlink_dir.mkdir()
    elif not symlink_dir.is_dir() and symlink_dir.exists():
        SystemExit("Configuration location should be a directory not a file or symlink")

    symlink.symlink_to(config_file, True)


if __name__ == "__main__":
    main()
