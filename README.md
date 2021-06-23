# File_Cleanup

Python script intended to run periodically via a crontab.

Moves files from Desktop to appropriate folders located in ~/Documents/Files

Removes files from Downloads and ~/Documents/Files/Screenshots that have not been accessed in more than 30 days

### Setup Crontab

* Enable cron: https://osxdaily.com/2020/04/27/fix-cron-permissions-macos-full-disk-access/

* Open crontab editor by opening your terminal and typing:

  ```
  crontab -e
  ```

* Next press "i" to edit the text (switch to insert mode).

* Copy the code below into your crontab editor while replacing the {CURLY BRACKETS} with the actual path to the file.

  NOTE: Using copy paste in VIM can be challenging, this will be easier to simply type it out yourself. However, if you're determined: https://vim.fandom.com/wiki/Copy,_cut_and_paste

  ~~~
  */5 * * * * {PATH TO PYTHON} {PATH TO SCRIPT} >> {PATH TO SCRIPT}/CleanUpLogs.txt 2>&1
  ~~~

  NOTE: Be sure to insert the correct file paths

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
*/5 * * * * python3 /Users/casey/Documents/Configurations/File_Cleanup/DesktopCleanUp.py >> /Users/casey/Documents/Configurations/File_Cleanup/CleanUpLogs.txt 2>&1
~~~

  * NOTE: I did not call python verbosely. I simply call the python that is in my $PATH. You may need to use the absolute path for your Python interpreter. (Being explicit is best practice.)

* This opens VIM; press 'i' to edit and use the attached Crontab Example to format the cron job to run the script every 5 minutes. Be sure to use the insert the absolute path in the indicated locations.

Want to change the frequency the script runs? https://crontab.guru/


### Editing the Script
