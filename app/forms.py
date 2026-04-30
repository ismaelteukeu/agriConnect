from wtforms import StringField, PasswordField, SelectField, TextAreaField, FloatField, BooleanField
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import Utilisateur

class FormulaireInscription(FlaskForm):
    nom = StringField('Nom complet',
        validators=[DataRequired(message='Le nom est obligatoire'),
                    Length(min=2, max=100)])

    email = StringField('Email',
        validators=[DataRequired(message='L\'email est obligatoire'),
                    Email(message='Email invalide')])

    telephone = StringField('Téléphone',
        validators=[DataRequired(message='Le téléphone est obligatoire')])

    localisation = StringField('Ville / Région',
        validators=[DataRequired(message='La localisation est obligatoire')])

    role = SelectField('Je suis un(e)',
        choices=[('agriculteur', '🧑‍🌾 Agriculteur'),
                 ('acheteur', '🛒 Acheteur')],
        validators=[DataRequired()])

    mot_de_passe = PasswordField('Mot de passe',
        validators=[DataRequired(),
                    Length(min=6, message='Minimum 6 caractères')])

    confirmation = PasswordField('Confirmer le mot de passe',
        validators=[DataRequired(),
                    EqualTo('mot_de_passe', message='Les mots de passe ne correspondent pas')])

    submit = SubmitField('Créer mon compte')

    # Vérifie que l'email n'est pas déjà utilisé
    def validate_email(self, email):
        utilisateur = Utilisateur.query.filter_by(email=email.data).first()
        if utilisateur:
            raise ValidationError('Cet email est déjà utilisé. Connectez-vous.')


class FormulaireConnexion(FlaskForm):
    email = StringField('Email',
        validators=[DataRequired(), Email(message='Email invalide')])

    mot_de_passe = PasswordField('Mot de passe',
        validators=[DataRequired()])

    submit = SubmitField('Se connecter')


from wtforms.validators import NumberRange

class FormulaireProduit(FlaskForm):
    nom = StringField('Nom du produit',
        validators=[DataRequired(message='Le nom est obligatoire'),
                    Length(min=2, max=100)])

    description = TextAreaField('Description',
        validators=[DataRequired(message='La description est obligatoire')])

    prix = FloatField('Prix (FCFA)',
        validators=[DataRequired(),
                    NumberRange(min=1, message='Le prix doit être positif')])

    unite = SelectField('Unité de vente',
        choices=[('kg', 'Kilogramme (kg)'),
                 ('sac', 'Sac'),
                 ('tonne', 'Tonne'),
                 ('litre', 'Litre'),
                 ('unite', 'Unité'),
                 ('regime', 'Régime')])

    quantite = FloatField('Quantité disponible',
        validators=[DataRequired(),
                    NumberRange(min=1, message='La quantité doit être positive')])

    categorie = SelectField('Catégorie',
        choices=[('cereales', '🌾 Céréales (maïs, riz, mil...)'),
                 ('tubercules', '🥔 Tubercules (manioc, igname...)'),
                 ('legumes', '🥬 Légumes (tomates, oignons...)'),
                 ('fruits', '🍌 Fruits (bananes, mangues...)'),
                 ('elevage', '🐄 Élevage (bœuf, poulet, porc...)'),
                 ('autres', '📦 Autres')])

    localisation = StringField('Lieu de vente',
        validators=[DataRequired(message='La localisation est obligatoire')],
        render_kw={"placeholder": "Ex: Bafoussam, Ouest"})

    submit = SubmitField('Publier le produit')

class FormulaireMessage(FlaskForm):
    contenu = TextAreaField('Votre message',
        validators=[DataRequired(message='Le message est obligatoire'),
                    Length(min=10, message='Minimum 10 caractères')],
        render_kw={"placeholder": 
            "Ex: Bonjour, je suis intéressé par votre produit. "
            "Est-il encore disponible ?"})

    submit = SubmitField('Envoyer le message')