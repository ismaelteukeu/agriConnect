import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cle_secrete_par_defaut'

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or
        os.environ.get('MYSQL_URL') or
        os.environ.get('DB_URL') or
        'sqlite:///agriconnect.db'  # Base locale temporaire
    )

    if SQLALCHEMY_DATABASE_URI.startswith('mysql://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            'mysql://', 'mysql+pymysql://', 1
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False