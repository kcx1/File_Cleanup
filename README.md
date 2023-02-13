# File Cleanup

###### Python script intended to run periodically via a crontab or service manager like launchd or systemd.

This script is driven by a TOML configuration to make it very flexible and customizable.

Users can configure any number of directories to be cleaned up routinely. Cleanup has 2 primary modes. "Move" and "Delete".
Deleteing is very simple. Users declare the directory that they would like the script to delete files. A time parameter can be set
so that the files only get deleted if they haven't been accessed within the time parameter given. The defualt is 30 days.

The move mode allows users to pick certain file types and have them automatically moved from one directory to another with optional
parameters and filters.

Below I've included an [example configuration](#example) to illustrate the possible options.


## Editing the Config


### EXAMPLE

```
[Example]

   path = "some/path/"                    If there is a leading slash an absolute path is assumed; otherwise it is relative to the user's /home
   operation = "move | delete"            Mode of cleanup; can move files or delete them.

   OPTIONAL
   time.number = int                      number is an integear multiplied by the unit; default is 30 d
   time.unit = "M | H | D"                Unit of time is defined in Minutes, Hours, Days. Whole words or abbreviations can be used.


   [[Example.move]]                       If you set the mode to move; you need to specify a few additional filter parameters
   name = "name"                          Currently not used programatically, but helpful to keep things organized. Not required.
   type = [".pdf", '.jpg', '.doc']        A list of the file extensions you want to include in this filter. ".*" to select all.
   destination = "some/path"

   OPTIONAL
   filter.name = "Name"                   Named for organization only; not used.
   filter.destination = "some/path/"
   filter.time.number = int               Define a time if you want a different time for your filter. Needs to be less time than the parent time.
   filter.time.unit = "M | H | D"
   filter.list = ["Extra", "filters"]     All of these get included in the filter.
                                          The additional filter help you have different parameters for files with the same extension. For EXAMPLE:
                                          You can have screenshots go to a different folder than all of the other .png files.

[Logs]
   enable = true | false                  Enable / disable logs
   path = "Documents/Files/Logs/"         Path to logs - not inluding log file name.
   name = "cleanup.log"                   Log file name
   max_size = 100                         KiloBytes - If not provided default of 100 is used.
   ```

## Install

I recommend creating a virtual environment so that you don't end up with conflicting system packages. There are many ways to do this.
[Virtualenv](https://virtualenv.pypa.io/en/latest/) is probably the most common. I tend to use [Miniconda](https://docs.conda.io/en/latest/miniconda.html)

Python 3.11 is required.

Once you have the virtual env setup and have activated it you can install it using:

```
pip install git+https://github.com/kcx1/File_Cleanup
```
This will install the FileCleanup package.



## Setup Crontab

* [Enable cron:](https://osxdaily.com/2020/04/27/fix-cron-permissions-macos-full-disk-access/)

* Open crontab editor by opening your terminal and typing:

```
crontab -e
```

* Next press "i" to edit the text (switch to insert mode).

* Copy the code below into your crontab editor while replacing the {CURLY BRACKETS} with the actual path to the file.

~~~
*/5 * * * * {PATH TO PYTHON} {PATH TO SCRIPT} >> /dev/null 2>&1
~~~

_NOTE: Be sure to insert the correct file paths; You may want to temporarily redirect to a file instead of `/dev/null` to debug._

* Once you have finished writing the cron job, press the esc key to leave "insert mode"

* Now press:

```
:wq
```
* Then press Enter. This will write and quit VIM.

* You will get a message _crontab: installing new crontab_
* You can double check your crontab:
```
crontab -l
```

Here's an example of what my crontab looks like.

Example:

~~~
*/5 * * * * python3 /Users/kcx1/Documents/Configurations/File_Cleanup/DesktopCleanUp.py >> /Users/kcx1/Documents/Configurations/File_Cleanup/CleanUpLogs.txt 2>&1
~~~

* NOTE: I did not call python verbosely. I simply call the python that is in my $PATH. You may need to use the absolute path for your Python interpreter. (Being explicit is best practice.)

__Want to change the frequency the script runs?__ https://crontab.guru/