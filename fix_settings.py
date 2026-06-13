import io
import re

settings_path = r"c:\Users\Bhoja\.gemini\antigravity-ide\scratch\panchapeetas\config\settings.py"

with io.open(settings_path, "r", encoding="utf-8") as f:
    content = f.read()

# Restore the deleted content
missing_content = """
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-4smj8x#l)v#otmxlqf7!0!oasv$3m9*=g@jovzs&a&8dx57)%b')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not os.environ.get('PRODUCTION', 'False') == 'True'

ALLOWED_HOSTS = ['gurubg.pythonanywhere.com', '.pythonanywhere.com', 'localhost', '127.0.0.1', '*']

# Application definition
"""

if "SECRET_KEY =" not in content:
    content = content.replace("    'django.contrib.admin',", missing_content + "\nINSTALLED_APPS = [\n    'django.contrib.admin',")
    with io.open(settings_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("settings.py restored and ALLOWED_HOSTS updated.")
else:
    print("settings.py already contains SECRET_KEY.")
