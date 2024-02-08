import shutil
import time
import logging
from collections.abc import Generator
from pathlib import Path
from functools import wraps
from FileCleanup.config import config

##############################################################################
#  CONFIGURATION
##############################################################################

current_time = time.time()  # Set current time to compare against.
configuration = config.pop("Configuration")  # Remove the configuration parameter; imported in the symlink_config.py
logs = config.pop("Logs")  # Remove log snippet from rest of config.toml


def normalize(path: str) -> Path:
    """
    Create a path object based on the provided path. If the provided is absolute return it.
    Otherwise join it to the user's home folder.

    Args:
        path (str): Path in string format
    Return:
        Path: path object
    """
    if Path(path).is_absolute():
        return Path(path).resolve()
    return Path.home().joinpath(path).resolve()


def logpath() -> Path:
    """
    Create a path object representing the log file path. If the file doesn't exist then create one and
    then return the file.

    Returns:
        Path: path object representing the loggin file.
    """
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
def log(severity: str):
    def decorator(func):
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
    return decorator


##############################################################################
#  FUNCTIONS
##############################################################################
def minutes(num: int) -> int:
    """
    Returns number of seconds within the provided number of minutes.

    Args:
        num (int): integer representing the number of minutes

    Returns:
        int: number of seconds in given minutes
    """
    return 60*num


def hours(num: int) -> int:
    """
    Returns number of seconds within the provided number of hours.

    Args:
        num (int): integer representing the number of hours

    Returns:
        int: number of seconds in given hours
    """
    return minutes(60)*num


def days(num: int) -> int:
    """
    Returns number of seconds within the provided number of days.

    Args:
        num (int): integer representing the number of days

    Returns:
        int: number of seconds in given days
    """
    return hours(24)*num


def set_time(t: dict) -> int:
    """
    Returns the number of seconds within provided configuration snippit. Where 'unit' sets the unit of time
    and 'number' sets the quantity. Only the first character of the unit is concidered; which allows users to
    use abbreviations or whole words. An example dictionary is as follows:

    {"number": int, "unit": str}

    Args:
        t (dict):   Dictionary representing the user's time configuration settings from the config.


    Returns:
        int or None: Number of seconds in the provided time dictionary; None logs an Error
    """
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
            raise Exception("Invalid time settings in the config")


def get_time(config_entry: dict, optional_time: int | None = None) -> int:
    """
    Use the time settings from the user's config or fallback to the default settings.
    User settings have priority, then optional_time defined at the function call, and
    finally if none of the above were specified; use the hardcoded fallback.

    Args:
        config_entry:           dictionary snippit from the user's config.toml
        optional_time (int):    Optional number of seconds instead of the hardcoded fallback
    Returns:
        int: number of seconds
    """
    if "time" in config_entry.keys():
        return set_time(config_entry["time"])
    else:
        return optional_time or days(30)


def expired(file: Path, expiration: int) -> bool:
    """
    Checks to see if a given file has been accessed within the given expiration period.

    Args:
        file (Path):        Path of the file to check.
        expiration (int):   Number of seconds since a file was accessed before it expires.

    Returns:
        bool: If file hasn't been accessed in a period longer than the provided expiration
    """
    return file.stat().st_atime < current_time - expiration


# @log("info")
# def make_dir(path):
#     Path.mkdir(path)
#     return f"{path} not found: Creating Directory"


@log("info")
def rm_files(file: Path) -> str:
    """
    Remove the given  file or folder

    Args:
        file (Path): Path of the file or dir to remove

    Returns:
        str: String for logging.
    """
    if file.is_file():
        file.unlink()
    elif file.is_dir():
        shutil.rmtree(file)
    return f"Removing {file}"


@log("info")
def clean_logs(kb: int = 100) -> str | None:
    """
    If the log file exceeds the maximium size then remove it. The maximum size specified in the config.toml
    will ahve priority. Otherwise use the one provided in the function call.

    Args:
        kb: Number of kilobytes for the maximum size

    Returns:
        str: String for logging
    """
    # Use user settings if set
    if "max_size" in logs.keys():
        kb = logs["max_size"]
    kb *= 1000  # set kb to bytes
    if logpath().stat().st_size > kb:  # if file size is greater than the kB argument in bytes
        logpath().unlink()
        return 'Logs are too large, removing'
    return None


@log("info")
def move_file(file: Path, dest: Path) -> str:
    """
    Move the given file to the given destination; If destination doesn't exit, create it.

    Args:
        file (Path): File to move
        dest (Path): New location directory

    Returns:
        str: String for logging
    """
    if not dest.exists():
        dest.mkdir(parents=True, exist_ok=True)
    return f"Moving: {file.rename(dest.joinpath(file.name))}"


def filter_files(path: Path, _config: dict, extension: str) -> Generator[Path, None, None]:
    """
    Generator function. Yields a path object if it meets the parameters of the filter.

    Args:
        path (Path):        Directory to itereate through
        _config (dict):     Dictionary containing filter parameters
        extension (str):    file extension for file globbing.

    Yields:
        Path:               file that meets the filter parameters.
    """
    if 'filter' in _config:
        for _filter in _config["filter"]["list"]:
            for file in path.glob(f'*{extension}'):
                if _filter in file.__str__():
                    yield file


def clean_folder(folder: Path, _time: int = days(30)) -> None:
    """
    If a file in the specified path hasn't been accessed in the specified days; remove it.

    Args:
        folder (Path): Path to folder to iterate through
        _time (int): optional time parameter to pass as expiration time.

    Returns:
        None
    """

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


def cleanup() -> None:
    """
    Perform main cleanup functions. Iterate through the user config and preform tasks such as move, filter, and delete
    as needed.

    Returns:
        None
    """

    clean_logs()  # Clear the logs before running rest of script.

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


def main() -> None:
    """
    Main script wrapped in a function with error handling.
    """
    try:
        cleanup()
    except Exception as err:
        logging.exception(f"Exception {err}: ")


##############################################################################
#  MAIN
##############################################################################

if __name__ == '__main__':
    main()
