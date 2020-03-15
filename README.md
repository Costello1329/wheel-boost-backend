# WheelBoostBackend
Backend solution for WheelBoost app.

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
