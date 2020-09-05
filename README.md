# Automove Script
Automove (and sort) files after being dropped in a folder
d
Will read all files in User/Documents and then move it to a certain folder depending on file type.

In case of Images will move it to a subfolder depending on Year_Month

# Instructions to make it autoexecute  on startup (Debian)
Copy the python file to /bin:

sudo cp -i /path/to/your_script.py /bin

Add A New Cron Job:

sudo crontab -e

Scroll to the bottom and add the following line (after all the #'s):

@reboot python /bin/your_script.py &

The “&” at the end of the line means the command is run in the background and it won’t stop the system booting up.

Test it:

sudo reboot