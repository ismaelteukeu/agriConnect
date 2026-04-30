from app import create_app, db
from app.models import Utilisateur, Produit, Message

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    print("✅ Tables créées avec succès !")
    print("Tables disponibles:",db.engine.table_names())