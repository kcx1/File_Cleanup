Copy / Paste the

code(
*/5 * * * * {PATH TO PYTHON} {PATH TO SCRIPT} >> {PATH TO SCRIPT}/CleanUpLogs.txt 2>&1
)


Example:

code(
*/5 * * * * python3 /Users/casey/Documents/Configurations/File_Cleanup/DesktopCleanUp.py >> /Users/casey/Documents/Configurations/File_Cleanup/CleanUpLogs.txt 2>&1
)
