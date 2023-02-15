#! /usr/bin/env python

import shutil
import time
import logging
from pathlib import Path
from functools import wraps
from .config import config

##############################################################################
#  CONFIGURATION
##############################################################################

current_time = time.time()  # Set current time to compare against.

logs = config.pop("Logs")


def normalize(path):
    if path[0] == "/":
        return Path(path).resolve()
    return Path.home().joinpath(path).resolve()


def logpath():
    path = normalize(logs["path"])
    if not path.is_dir():
        path.mkdir()
    file = path.joinpath(logs["name"])
    if not file.exists():
        file.touch()
    return file


# Logging config
logging.basicConfig(
    level=logging.INFO,
    filename=logpath(),
    format='%(asctime)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S'
)


# Wrappers
def log(severity):
    def decorartor(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Log the results of a function prefixed with the timestamp
            if logs["enable"]:
                log_func = getattr(logging, severity)
                func_result = func(*args, **kwargs)
                if func_result:
                    log_func(func_result)
                return None
        return wrapper
    return decorartor


##############################################################################
#  FUNCTIONS
##############################################################################
def minutes(num: int) -> int:
    # Returns seconds for the number of minutes given
    return 60*num


def hours(num: int) -> int:
    # Returns seconds for the number of hours given
    return minutes(60)*num


def days(num: int) -> int:
    # Returns seconds for the number of days given
    return hours(24)*num


def set_time(t: dict):
    num = t["number"]

    match t["unit"].upper()[0]:
        case "M":
            return minutes(num)
        case "H":
            return hours(num)
        case "D":
            return days(num)
        case _:
            logging.exception("Invalid time settings in the config")
            return


def get_time(config_entry, optional_time=None):
    # Use time setting from config if defined
    if "time" in config_entry.keys():
        return set_time(config_entry["time"])
    else:
        # Fallback timsetting
        return optional_time or days(30)


def expired(file, expiration):
    return file.stat().st_atime < current_time - expiration


@log("info")
def make_dir(path):
    Path.mkdir(path)
    return f"{path} not found: Creating Directory"


@log("info")
def rm_files(file):
    if file.is_file():
        file.unlink()
    elif file.is_dir():
        shutil.rmtree(file)
    return f"Removing {file}"


@log("info")
def clean_logs(kb=100):
    kb *= 1000  # set kb to bytes
    if logpath().stat().st_size > kb:  # if file size is greater than the kB argument in bytes
        logpath().unlink()
        return 'Logs are too large, removing'


@log("info")
def check_dirs(destination_path):
    path = Path(destination_path)
    if not path.is_dir():
        path.mkdir(parents=True)
        return f"Creating Path: {path}"


@log("info")
def move_file(file, dest):
    return f"Moving: {file.rename(dest.joinpath(file.name))}"


def filter_files(path, _config, extension):
    if 'filter' in _config:
        for _filter in _config["filter"]["list"]:
            for file in path.glob(f'*{extension}'):
                if _filter in file.__str__():
                    yield file


def clean_folder(folder, _time=days(30)):

    """If a file in the specified path hasn't been accessed in the specified days; remove it."""

    for file in folder.iterdir():
        if expired(file, _time):
            try:
                rm_files(file)
            except PermissionError as permission:  # This shouldn't happen
                logging.exception(permission)
                continue
            except Exception as _err:
                logging.exception(_err)
                continue


def cleanup():
    for entry in config.values():
        path = normalize(entry['path'])
        if entry["operation"].lower() == "move":
            for move in entry["move"]:
                for extension in move["type"]:
                    # Filter Files First
                    for file in filter_files(path, move, extension):
                        if expired(file, get_time(move["filter"], get_time(entry))):
                            move_file(file, normalize(move["filter"]["destination"]))
                    # Move all that weren't Filtered; if expired
                    for file in path.glob(f'*{extension}'):
                        if expired(file, get_time(entry)):
                            move_file(file, normalize(move["destination"]))

        elif entry["operation"].lower() == "delete":
            clean_folder(path, _time=get_time(entry))

    if "max_size" in logs.keys():
        clean_logs(kb=logs["max_size"])
    else:
        clean_logs()


def main():
    try:
        cleanup()
    except Exception as err:
        logging.exception(f"Exception {err}: ")


##############################################################################
#  MAIN
##############################################################################

if __name__ == '__main__':
    main()
