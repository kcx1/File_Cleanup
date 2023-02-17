from pathlib import Path
from file_cleanup import normalize
from FileCleanup.config import config

# Path to installed config
config_file = Path("config/config.toml").absolute()
# Path declared in config
symlink = normalize(config["Config"]["location"]).absolute()


def main():
    config_file.symlink_to(symlink, True)


if __name__ == "__main__":
    main()
