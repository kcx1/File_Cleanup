from pathlib import Path
from FileCleanup.file_cleanup import normalize, configuration


# Path to installed config
script_path = Path(__file__).parent
config_file = script_path.joinpath("config/config.toml").absolute()
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
        symlink.symlink_to(config_file, True)


if __name__ == "__main__":
    main()
