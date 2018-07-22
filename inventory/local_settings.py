
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'inventory',
        'USER': 'root',
        'PASSWORD': 'mindfire',
        'HOST': '127.0.0.1',
        'PORT': '',
        'OPTIONS': {
                 "init_command": "SET foreign_key_checks = 0;",
            },
    }
}

