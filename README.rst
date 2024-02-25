Balkan Ultra
============


:License: MIT

--------

Balkan Ultra is a website for the Balkan Ultra mountain race which takes place
each year at the beginning of August in the Bulgarian Stara Planina mountain.

--------

The following environment variables need to be set before running the project:

* AWS_ACCESS_KEY_ID
* AWS_SECRET_ACCESS_KEY
* DEBUG
* DEVELOPMENT_MODE
* DB_USER
* DB_PASSWORD
* SENDINBLUE_API_KEY (API key to Sendin Blue mail service)
* IS_IN_CONTAINER (False)

To run the project in dev mode make sure you've:

- Created a python virtual environment
- Exported the environment variables mentioned above
- From the root directory run `docker-compose -f compose-dev/docker-compose.yml up -d`
- Run `pip install -r requirements.txt` to install python dependencies
- Run `python manage.py migrate` to apply the database migrations
- Run `npm i` to install node dependencies (make sure you use npm -v 6.14.18)
- Run `npm run build` to build the source staticfiles
- Run `python manage.py collectstatic` (Optional if DEVELOPMENT_MODE=False, will move staticfiles to S3 bucket)
- Start the development server `python manage.py runserver`

--------

The website can be found at `balkan-ultra.com
<http://www.balkan-ultra.com/>`_
