# File_Cleanup

Python script intended to run periodically via a crontab.

Moves files from Desktop to appropriate folders located in ~/Documents/Files

Removes files from Downloads and ~/Documents/Files/Screenshots that have not been accessed in more than 30 days

### Setup Crontab

* Enable cron: https://osxdaily.com/2020/04/27/fix-cron-permissions-macos-full-disk-access/
* Open terminal and type: crontab -e
* This opens VIM; press 'i' to edit and use the attached Crontab Example to format the cron job to run the script every 5 minutes. Be sure to use the insert the absolute path in the indicated locations.

Want to change the frequency the script runs? https://crontab.guru/


### Editing the Script
