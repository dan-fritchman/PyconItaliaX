
# Django Starter Blog 

## Courtesy Django Girls's [tutorial site](https://tutorial.djangogirls.org/en)

Worked through as the intro session to PyCon Italia 2019.

## Deployment

Running on Heroku at 
https://fritch-django-starter-blog.herokuapp.com/

A few other required bits of setup, if re-doing this:

```
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```
(Although both of these worked better in their web-console UI.)
Note since this is in a git-repo *sub* directory, Heroku requires `git subtree push` to deploy it, like so:

```
git subtree push --prefix DjangoStarter heroku master
```
