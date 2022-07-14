import os
import shutil
import time
import glob
import datetime
import logging

##############################################################################
#  CONFIGURATION
##############################################################################

current_time = time.time()  # Set current time to compare against.

# Home folder
home = os.path.expanduser('~')

# NOTE: normpath resolves the double forward slash in my path names.
#       So I use them to better indicate directories.
desktop_path = os.path.normpath(f'{home}/Desktop/')  # Path to Desktop
download_path = os.path.normpath(f'{home}/Downloads/')  # Path to Downloads
documents_path = os.path.normpath(f'{home}/Documents/')  # Path to Documents
trash_path = os.path.normpath((f'{home}/.Trash/'))  # Path to trash can
script_path = os.path.dirname(os.path.abspath(__file__))  # Path to Script location (Used for log file)

# Destination paths for moving files from Desktop.
screenshot_path = os.path.normpath(f'{documents_path}/Files/ScreenShots/')  # Path to move screenshots
pdf_path = os.path.normpath(f'{documents_path}/Files/PDFs/')  # Path to move PDFs
vid_path = os.path.normpath(f'{documents_path}/Files/Vids/')

# Logging path for stdout and stderr
log_path = os.path.normpath(f'{script_path}/CleanUpLogs.log')

# Logging config
logging.basicConfig(
    level=logging.INFO,
    filename=log_path,
    format='%(asctime)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S'
    )


##############################################################################
#  FUNCTIONS
##############################################################################

def make_dirs():
    if not os.path.isdir(screenshot_path):
        os.mkdir(screenshot_path)
        print("Screen Shot path not found: Creating directory")
    if not os.path.isdir(pdf_path):
        os.mkdir(pdf_path)
        print("PDF path not found: Creating directory")
    if not os.path.isdir(vid_path):
        os.mkdir(vid_path)
        print("Video path not found: Creating directory")


def minutes(num) -> int:
    # Returns seconds for the number of minutes given
    return 60*num


def hours(num) -> int:
    # Returns seconds for the number of hours given
    return minutes(60)*num


def days(num) -> int:
    # Returns seconds for the number of days given
    return hours(24)*num


def timestamp():
    return datetime.datetime.now()


def clean_desktop(time=hours(1)):
    '''If a file on the desktop hasn't been modified or opened in the specified time; move it to a specified folder'''

    images = glob.glob(f'{desktop_path}/*.png')  # List all png images in path
    videos = glob.glob(f'{desktop_path}/*.mov')  # List all mov videos in path
    pdfs = glob.glob(f'{desktop_path}/*.pdf')  # List all pdf files in path

    files = images + videos + pdfs  # Merge the image, video, and pdf lists

    for file in files:
        if os.stat(file).st_ctime < current_time - time:  # if change time was more than an hour ago
            if file in images:  # Check to see if we should move the file to the screenshot path
                if 'Screen Shot' in file:  # Double check that the file is a screen shot
                    shutil.move(file, screenshot_path)  # Move the file
                    logging.info(f'Moving {file}')  # Log the move
                else:
                    #  If a png is found, but is not a screen shot; log it. May comeback to address later.
                    logging.info(f"Found a png: {file}, but it's not a screenshot. Doing nothing" )
            elif file in pdfs:  # If the file is a pdf;
                shutil.move(file, pdf_path)  # Move it to the pdf path
                logging.info(timestamp(), f'Moving {file}')  # Log the move
            elif file in videos:
                    shutil.move(file, vid_path)
                    logging.info(timestamp(), f'Moving {file}')
            else:
                # If there is a file on the desktop, that is not in our list, log it. May address later.
                logging.info(f"Found {file}, but it's not a file type that I am moving. Doing nothing" )


def clean_folder(folder_path, time=days(30)):

    '''If a file in the specified path hasn't been accessed in the specified days; remove it.'''

    for file in os.listdir(folder_path):

        file_path = f"{folder_path}/{file}"

        if os.stat(file_path).st_atime < current_time - time:
            logging.info(timestamp(),f"{file} hasn't been accessed in 30 days; I'm removing")
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                else:
                    print("This is neither a file or a folder")  # Should never happen
            except PermissionError as permission:  # This shouldn't happen
                logging.exception(timestamp(), permission)
                continue
            except Exception as err:
                logging.exception(timestamp(), err)
                continue


def clean_logs(kb=100):
    kb *= 1000  # set kb to bytes
    if os.stat(log_path).st_size > kb:  # if file size is greater than the kB argument in bytes
        os.remove(log_path)
        logging.debug(timestamp(), 'Logs are too large, removing')


##############################################################################
#  MAIN
##############################################################################

if __name__ == '__main__':

    #  Removing print statement to clean up Logs, Now time stamp is with each removal instead
    #  print(timestamp(), 'Script starting!')  # Print script start time for logs
    try:
        make_dirs()  # Adding function to check for directories to move screenshots and pdfs into
        clean_logs()  # Moving this to be the first function to execute
        clean_desktop()
        clean_folder(download_path)
        clean_folder(screenshot_path, time=days(15))
        clean_folder(trash_path, time=hours(3))
    except Exception as err:
        logging.exception(f"Exception {err}: ")
