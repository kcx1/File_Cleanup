import pathlib


try:
    import tomllib  # Preferred lib
except ImportError or ModuleNotFoundError as err:  # ModuleNotFoundError
    raise SystemExit(err)

path = pathlib.Path(__file__).parent / "config.toml"
with path.open(mode="rb") as toml:
    config = tomllib.load(toml)
