# File Cleanup

###### Python script intended to run periodically via a crontab or service manager like launchd or systemd.

This script is driven by a TOML configuration to make it very flexible and customizable.

Users can configure any number of directories to be cleaned up routinely. Cleanup has 2 primary modes. "Move" and "Delete".
Deleteing is very simple. Users declare the directory that they would like the script to delete files. A time parameter can be set
so that the files only get deleted if they haven't been accessed within the time parameter given. The defualt is 30 days.

The move mode allows users to pick certain file types and have them automatically moved from one directory to another with optional
parameters and filters.

Finally there is a logging parameter that you can set so that you can easily look back at the history of the script.

###### NOTE: Both the 'Configuration' and the 'Logs' parameter are required.

Below I've included an [example configuration](#example) to illustrate the possible options.


## Editing the Config


### EXAMPLE

```
[Configuration]                            ** Required **
    location = "Documents"                 Directory in which to symlink the configuration file.

[Example]
    path = "some/path/"                    If not absolute, it is assumed to be relative to the user's /home
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
        filter.list = ["Extra", "filters"]    All of these get included in the filter.
                                              The additional filter help you have different parameters for files with the same extension. For EXAMPLE:
                                              You can have screenshots go to a different folder than all of the other .png files.

[Logs]                                    ** Required **
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
python -m pip install git+https://github.com/kcx1/File_Cleanup
```
This will install the FileCleanup package. Once installed before you leave your virtual environment; I suggest that you type: ```which fclean``` and copy the path. (We'll use it to setup the crontab)

## Using the script

The package create a convenient shell command that will allow you to run the script manually. Simply invoke the new ```fclean``` command, and the script will run manually.

## Configuring the script

You'll need access to the _config.toml_ file in order to setup your own custom congfiguration. The file I've included should work out of the box and is the configuration that I currently use.
However, I wanted to provide an easy way to edit the config so that the behavior of the script could be easily modified and customized.

This package includes a second binary ```fclean-config``` This command will generate a symbolic link to you the package's config.toml fle. When running for the first time the script will
install the symlink file into the user's Documents folder. Once linked - you can set location parameter and re-run the command and the scrpt will install it in the new location. You can
then safely delete the original symlink.

You can also dig into the site-packages from your python interperter and locate the source file here:

```../site-packages/FileCleanup/config/config.toml```


## Setup Crontab

* [Enable cron on MacOS:](https://osxdaily.com/2020/04/27/fix-cron-permissions-macos-full-disk-access/)

* Open crontab editor by opening your terminal and typing:

```
crontab -e
```

* Next press "i" to edit the text (switch to insert mode).

* Paste the results of ```which fclean``` into the curly brackets bellow. _NOTE: If you decided to install FileCleanup as a global package you could just use:_ ```"${which fclean}"``` Additionally you could also call the script in python directly if you prefer.

~~~
*/5 * * * * {RESULTS OF WHICH FCLEAN} >> /dev/null 2>&1
~~~

_NOTE: Be sure to insert the correct file paths; You may want to temporarily redirect to a file instead of `/dev/null` to debug._

* Once you have finished writing the cron job, press the esc key to leave "insert mode" and press:```:wq```  and Enter. This will write and quit VIM.
* You will get a message _crontab: installing new crontab_
* You can double check your crontab:
```
crontab -l
```

Here's an example of what my crontab looks like.

Example:

~~~
*/5 * * * *  /Users/kcx1/miniforge3/envs/dev/bin/fclean >> /dev/null 2>&1
~~~

* There you go - the script will run every 5 minutes and will keep your folders clean. 

__Want to change the frequency the script runs?__ [Crontab calculator](https://crontab.guru/)

## Uninstall

To remove the script activate the virtual environment that you used to pip install (Hint: You cna find the path in your crontab) and type:

```
python -m pip uninstall FileClean
```