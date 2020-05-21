# WheelBoostBackend
Backend solution for WheelBoost app.

## Build Requirements:
+ UNIX system (Mac OS / Ubuntu / etc)
+ python 3.6 or greater
+ pip3
+ venv
+ At least 1 CPU
+ 512MB RAM at least
+ [req.txt](https://github.com/Costello1329/WheelBoostBackend/blob/master/req.txt)

## How to init:
+ Clone this repository
+ Open project in PyCharm and run the next command in terminal: `python3 -m venv venv`.
+ Now you need to add an interpreter. Open project preferences:
    + `ctrl + alt + s` for win and linux.
    + `cmd + ,` for mac.
    + After that, add python 3.x interpreter (Preferences &rarr; Project:WheelBoostBacked &rarr; Project Interpreter).
+ Run the next command in terminal: `pip install -r req.txt`.

## How to make migrations:
+ Run the next command in terminal: `python3 manage.py makemigrations`.
+ Run the next command in terminal: `python3 manage.py migrate`.

## How to add superuser:
+ Run the next command in terminal: `python3 manage.py createsuperuser`.  
+ Now you can open `127.0.0.1:8000/admin`
