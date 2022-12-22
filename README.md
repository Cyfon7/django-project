- Create the project with:
python3 -m django startproject my_project

- Modify settings.py with the correct values for the connection with postgresql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_my_project',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

- Create the DB on postgresql 
CREATE DATABASE db_my_project;