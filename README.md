# Rinse
Rinse is a web interface for [rembg](https://github.com/danielgatis/rembg) built with [Flask](https://flask.palletsprojects.com/) and [Tailwind](https://tailwindcss.com/).

## Installation
- Clone this repository
- Create a virtual invironment

`python3 -m venv /path/to/new/virtual/environment`

- Activate the virtual environtment

`source /path/to/new/virtual/environment/bin/activate`

- Install the requirements

`pip install -r requirements.txt`

- Run the flask app

`/path/to/new/virtual/environment/bin/flask --app app --debug run`

## File clean up
The way this works is the uploaded file is written to the filesystem (`./static/uploads`), converted, and then that converted file is also written to the filesystem. In my deployment of this app, I have a cron job that runs every hour to delete all uploaded and converted files.

Here is are some different solutions to deleting the files after download:

https://stackoverflow.com/questions/24612366/delete-an-uploaded-file-after-downloading-it-from-flask
