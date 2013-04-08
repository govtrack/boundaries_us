ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

SECRET_KEY = '.....'

DATABASES["default"]["NAME"] = "boundaries_us" # Postgres database name
DATABASES["default"]["USER"] = "boundaries_us" # Postgres user name w/ access to db
DATABASES["default"]["PASSWORD"] = "...."

ALLOWED_HOSTS = ["*"]
