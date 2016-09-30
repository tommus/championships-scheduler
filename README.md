# Championships Scheduler - API

API for Championships Scheduler.

## Backend management

1. Create virtual environment:

    > virtualenv .venv -p python3

2. Activate virtual environment:

    > source .venv/bin/activate

3. Install requirements

    > pip install -r requirements.txt

## Frontend management

1. Install `nodeenv` package by running:

	> pip install nodeenv

   If you previously install packages from `requirements.txt` you can ignore this step.

2. Add NodeJS virtual environment:

	> nodeenv -p --prebuilt

3. Add NodeJS virtual environment to existing python virtual environment:

	> npm install -g bower

4. All necessary JavaScript plugins are listen as Bower dependencies in `requirements/bower.json` file. Install them by running:

	> bower install

## Database synchronization

1. When executing server for the first time, you have to synchronize database (and execute migrations):

    > python manage.py migrate

## Running server

1. Make sure the virtual environment has been activated:

    > source .venv/bin/activate

2. Start server by typing:

    > python manage.py runserver address:port

- I.e. start server at port 8000 to listen for connections from whatever source:

    > python manage.py runserver 0.0.0.0:8000

## Localization:

1. When preparing new localization files for translation, you have to run the command:

    > python manage.py makemessages -l <language_code>

2. Files to translate are put in:

    <project_root>/locale/<language_code>/LC_MESSAGES/django.po

3. After making changes in translations, you have to compile them:

    > python manage.py compilemessages -l <language_code>

## Dumping data:

1. If you would like to dump existing data, run the following command:

    > python manage.py dumpdata --indent=4 <app>.<Model> fixture/<app>_<model>.json

    For example:

    > python manage.py dumpdata --indent=4 championship.Team > fixture/championship_teams.json

2. If you would like to load fixture, run the following command:

    > python manage.py loaddata fixture/<app>_<model>.json

    For example:

    > python manage.py loaddata fixture/championship_teams.json
