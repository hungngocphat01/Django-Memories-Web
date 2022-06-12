# Memories

## Description
This is a simple "image keeper" project created with Django 4.0.3 for practicing purposes.

A live demo has been deployed to Heroku and can be found here:

Features:
- User can login with Facebook.
- User can create a new "post" with following fields:
    - Title
    - Content (raw text only)
    - Attach an image.  
        If the user does not attach one, a random image will be shown when loading that post.
    - Select a location from a map.

## Technologies
- Django
- PostgreSQL
- Amazon S3 (for image storing)
- Bootstrap 5
- Leaflet (map)
- Lorem Picsum
- Other Python dependencies listed in `requirements.txt`

## Environment

Following environment variables must be declared in a file called `.env` placed in the same directory as the `manage.py` file.

```
DATABASE_URL=
DJANGO_DEBUG=
DJANGO_SECRET=
SOCIAL_AUTH_FACEBOOK_KEY=
SOCIAL_AUTH_FACEBOOK_SECRET=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
AWS_S3_REGION_NAME=
```

## Run in development mode

Create new database:

```
psql ...
CREATE DATABASE ...;
exit;
```

Initialize project:

```
cd source 
pip install -r requirements.txt 
python manage.py makemigrations main 
python manage.py migrate 
```

Run application 

```
python manage.py runserver
```