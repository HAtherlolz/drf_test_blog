# DjangoRestFramework

Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

```bash
pip install -r /path/to/requirements.txt
```

## Usage
##Set your config there
```python
#Settings.py

SECRET_KEY = env("SECRET_KEY")

 DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_LOGIN')
EMAIL_HOST_PASSWORD = env('EMAIL_PASSWORD')
EMAIL_PORT = 587
```

#After run console commands
```bash

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver:port

```


```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)