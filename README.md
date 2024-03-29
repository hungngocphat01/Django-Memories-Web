# Memories

## Description
This is a simple "image keeper" project created with Django 4.0.3 for practicing purposes.

A live demo has been deployed to Heroku and can be found here: ~~https://hnpmemories.herokuapp.com/~~  
Because I don't know if I will be charged for keeping S3 running like this or not, I shutted down the live demo website. 

Some demo images can be found in the `demo` directory.

Features:
- User can login with Facebook.
- User can create a new "post" with following fields:
    - Title.
    - Content (raw text only).
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

## Deployment

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

## Run this project locally
- Create your Meta dev app, setup OAuth.
- Create an S3 bucket.
- Create a volume for the database: `docker volume create hnp-memories-postgres`.
- Setup neccessary environment variables in `docker/django/.django.env`.
- Run `docker compose up`.  
- Access `localhost:8000`.
