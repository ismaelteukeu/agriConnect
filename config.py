import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cle_secrete_par_defaut'

    # Récupère l'URL depuis les variables d'environnement
    db_url = (os.environ.get('DATABASE_URL') or 
              os.environ.get('MYSQL_URL') or
              os.environ.get('SQLALCHEMY_DATABASE_URI'))

    # Corrige le préfixe si nécessaire
    if db_url and db_url.startswith('mysql://'):
        db_url = db_url.replace('mysql://', 'mysql+pymysql://', 1)

    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False