from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

# Flask-Login a besoin de cette fonction pour charger un utilisateur
@login_manager.user_loader
def load_user(user_id):
    return Utilisateur.query.get(int(user_id))


# ─────────────────────────────────────────
# MODÈLE UTILISATEUR
# ─────────────────────────────────────────
class Utilisateur(db.Model, UserMixin):
    __tablename__ = 'utilisateurs'

    id          = db.Column(db.Integer, primary_key=True)
    nom         = db.Column(db.String(100), nullable=False)
    email       = db.Column(db.String(150), unique=True, nullable=False)
    mot_de_passe= db.Column(db.String(256), nullable=False)
    role        = db.Column(db.String(20), nullable=False)  # 'agriculteur' ou 'acheteur'
    telephone   = db.Column(db.String(20))
    localisation= db.Column(db.String(150))
    date_inscription = db.Column(db.DateTime, default=datetime.utcnow)

    # Un utilisateur peut avoir plusieurs produits
    produits    = db.relationship('Produit', backref='vendeur', lazy=True)
    # Un utilisateur peut envoyer plusieurs messages
    messages_envoyes = db.relationship('Message', back_populates='expediteur', lazy=True)

    def __repr__(self):
        return f'<Utilisateur {self.nom} - {self.role}>'


# ─────────────────────────────────────────
# MODÈLE PRODUIT
# ─────────────────────────────────────────
class Produit(db.Model):
    __tablename__ = 'produits'

    id          = db.Column(db.Integer, primary_key=True)
    nom         = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    prix        = db.Column(db.Float, nullable=False)
    unite       = db.Column(db.String(20))       # ex: kg, sac, tonne
    quantite    = db.Column(db.Float, nullable=False)
    categorie   = db.Column(db.String(50))       # ex: céréales, légumes, tubercules
    localisation= db.Column(db.String(150))
    disponible  = db.Column(db.Boolean, default=True)
    date_publication = db.Column(db.DateTime, default=datetime.utcnow)

    # Clé étrangère vers Utilisateur
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), nullable=False)

    def __repr__(self):
        return f'<Produit {self.nom} - {self.prix} FCFA>'


# ─────────────────────────────────────────
# MODÈLE MESSAGE
# ─────────────────────────────────────────
class Message(db.Model):
    __tablename__ = 'messages'

    id          = db.Column(db.Integer, primary_key=True)
    contenu     = db.Column(db.Text, nullable=False)
    date_envoi  = db.Column(db.DateTime, default=datetime.utcnow)
    lu          = db.Column(db.Boolean, default=False)

    expediteur_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), nullable=False)
    produit_id    = db.Column(db.Integer, db.ForeignKey('produits.id'), nullable=False)

    # Relations
    expediteur = db.relationship('Utilisateur', foreign_keys=[expediteur_id], back_populates='messages_envoyes')
    produit    = db.relationship('Produit', foreign_keys=[produit_id])

    def __repr__(self):
        return f'<Message de {self.expediteur_id} sur produit {self.produit_id}>'