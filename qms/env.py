"""
Environment variables for the QMS application.
"""
import os
from dotenv import load_dotenv

ENVIRONMENT = os.getenv('ENVIRONMENT', 'production')

if ENVIRONMENT == 'development':
    load_dotenv('.env-dev')
else:
    load_dotenv()

# Database Variables
POSTGRES_DB=os.getenv('POSTGRES_DB')
POSTGRES_USER=os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD=os.getenv('POSTGRES_PASSWORD')
DB_HOST=os.getenv('DB_HOST')
DB_PORT=os.getenv('DB_PORT')
SECRET_KEY=os.getenv('SECRET_KEY')
DEBUG=os.getenv('DEBUG')
