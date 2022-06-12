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

Following environment variables must be declared in a file called `.env` placed in the root directory of this repo.

```
DJANGO_SECRET=
SOCIAL_AUTH_FACEBOOK_KEY=
SOCIAL_AUTH_FACEBOOK_SECRET=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
AWS_S3_REGION_NAME=
```