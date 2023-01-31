nohup python -u upload.py &
To execute upload.py in the background and won't hang up even if the terminal is shutted down.

ps ax | grep update.py
To search for a process whose ID is forgotten.

lsof -i
To search for a process who is using the port.

kill -9 12345
To kill the process 12345.

Output of upload.py will go to nohup.out due to nohup, must open .out file with default text editor.