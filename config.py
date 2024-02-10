import os
from dotenv import load_dotenv

# load environment variables from .env file (.env used to hide sensitive content such as database username & password)
load_dotenv()

# Set Database configuration
DATABASE_CONFIG = {
    'DATABASE': os.getenv('DATABASE'),
    'USER': os.getenv('USER'),
    'PASSWORD': os.getenv('PASSWORD'),
    'HOST': os.getenv('HOST'),
    'DRIVER': os.getenv('DRIVER'),
}