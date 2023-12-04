import os

secret_key = "SECRET"

connector = os.getenv('CONNECTOR')
user = os.getenv('USER')
password = os.getenv('PASSWORD')
host = os.getenv('HOST')
database = os.getenv('DATABASE')

SQLALCHEMY_DATABASE_URI = f'{connector}://{user}:{password}@{host}/{database}'
