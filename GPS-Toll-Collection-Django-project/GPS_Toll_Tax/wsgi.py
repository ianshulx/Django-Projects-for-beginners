import os
from django.core.wsgi import get_wsgi_application

# The WEBSITE_DEFAULT_HOSTNAME check might need to be adjusted
# This can be dynamically pulled from the environment variables or hardcoded as needed

# Define the default hostname
WEBSITE_DEFAULT_HOSTNAME = os.getenv('WEBSITE_DEFAULT_HOSTNAME', '')

# Use a conditional check for the settings module based on the environment variable
settings_module = "GPS_Toll_Tax.deployment" if WEBSITE_DEFAULT_HOSTNAME else "GPS_Toll_Tax.settings"

# Ensure the DJANGO_SETTINGS_MODULE is set based on the condition above
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()
