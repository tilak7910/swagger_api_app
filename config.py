import os

class Config:
    # Database connection details
    MYSQL_USER = os.getenv('MYSQL_USER', 'task_user')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'user123')
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'db')
    MYSQL_DB = os.getenv('MYSQL_DB', 'tasks_db')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))  # Optional, default is 3306

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'supersecretkey')
