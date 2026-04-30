from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db, bcrypt
from app.models import Utilisateur, Produit
from app.forms import FormulaireInscription, FormulaireConnexion, FormulaireProduit
from app.forms import (FormulaireInscription, FormulaireConnexion,
                       FormulaireProduit, FormulaireMessage)
from app.models import Utilisateur, Produit, Message


main = Blueprint('main', __name__)

# ─────────────────────────────
# PAGE ACCUEIL
# ─────────────────────────────
@main.route('/')
def index():
    produits = Produit.query.filter_by(disponible=True)\
                            .order_by(Produit.date_publication.desc())\
                            .limit(6).all()
    return render_template('index.html', produits=produits)

# ─────────────────────────────
# INSCRIPTION
# ─────────────────────────────
@main.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = FormulaireInscription()
    if form.validate_on_submit():
        # Chiffrement du mot de passe
        mdp_chiffre = bcrypt.generate_password_hash(form.mot_de_passe.data).decode('utf-8')

        utilisateur = Utilisateur(
            nom=form.nom.data,
            email=form.email.data,
            telephone=form.telephone.data,
            localisation=form.localisation.data,
            role=form.role.data,
            mot_de_passe=mdp_chiffre
        )
        db.session.add(utilisateur)
        db.session.commit()

        flash(f'Compte créé avec succès ! Bienvenue {utilisateur.nom} 🎉', 'success')
        return redirect(url_for('main.connexion'))

    return render_template('inscription.html', form=form)

# ─────────────────────────────
# CONNEXION
# ─────────────────────────────
@main.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = FormulaireConnexion()
    if form.validate_on_submit():
        utilisateur = Utilisateur.query.filter_by(email=form.email.data).first()

        if utilisateur and bcrypt.check_password_hash(utilisateur.mot_de_passe, form.mot_de_passe.data):
            login_user(utilisateur)
            flash(f'Bienvenue {utilisateur.nom} ! 👋', 'success')
            # Redirige vers la page demandée ou le dashboard
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.dashboard'))
        else:
            flash('Email ou mot de passe incorrect.', 'danger')

    return render_template('connexion.html', form=form)

# ─────────────────────────────
# DÉCONNEXION
# ─────────────────────────────
@main.route('/deconnexion')
@login_required
def deconnexion():
    logout_user()
    flash('Vous êtes déconnecté(e).', 'info')
    return redirect(url_for('main.index'))

# ─────────────────────────────
# DASHBOARD
# ─────────────────────────────
@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'agriculteur':
        mes_produits = Produit.query.filter_by(
            utilisateur_id=current_user.id
        ).order_by(Produit.date_publication.desc()).all()
        return render_template('dashboard_agriculteur.html',
                               produits=mes_produits)
    else:
        derniers_produits = Produit.query.filter_by(disponible=True)\
                                        .order_by(Produit.date_publication.desc())\
                                        .limit(8).all()
        return render_template('dashboard_acheteur.html',
                               produits=derniers_produits)


@main.route('/produit/supprimer/<int:id>')
@login_required
def supprimer_produit(id):
    produit = Produit.query.get_or_404(id)
    if produit.utilisateur_id != current_user.id:
        flash('Action non autorisée.', 'danger')
        return redirect(url_for('main.dashboard'))
    db.session.delete(produit)
    db.session.commit()
    flash(f'Produit "{produit.nom}" supprimé.', 'info')
    return redirect(url_for('main.dashboard'))


@main.route('/produit/toggle/<int:id>')
@login_required
def toggle_disponibilite(id):
    produit = Produit.query.get_or_404(id)
    if produit.utilisateur_id != current_user.id:
        flash('Action non autorisée.', 'danger')
        return redirect(url_for('main.dashboard'))
    produit.disponible = not produit.disponible
    db.session.commit()
    statut = 'disponible' if produit.disponible else 'indisponible'
    flash(f'Produit "{produit.nom}" marqué comme {statut}.', 'success')
    return redirect(url_for('main.dashboard'))

# ─────────────────────────────
# LISTE DES PRODUITS
# ─────────────────────────────
@main.route('/produits')
def produits():
    categorie = request.args.get('categorie', '')
    recherche = request.args.get('recherche', '')

    query = Produit.query.filter_by(disponible=True)

    if categorie:
        query = query.filter_by(categorie=categorie)
    if recherche:
        query = query.filter(Produit.nom.contains(recherche))

    tous_produits = query.order_by(Produit.date_publication.desc()).all()
    return render_template('produits.html', produits=tous_produits,
                           categorie=categorie, recherche=recherche)

# ─────────────────────────────
# DÉTAIL D'UN PRODUIT
# ─────────────────────────────
@main.route('/produit/<int:id>')
def detail_produit(id):
    produit = Produit.query.get_or_404(id)
    return render_template('detail_produit.html', produit=produit)

# ─────────────────────────────
# PUBLIER UN PRODUIT
# ─────────────────────────────
@main.route('/publier', methods=['GET', 'POST'])
@login_required
def publier_produit():
    if current_user.role != 'agriculteur':
        flash('Seuls les agriculteurs peuvent publier des produits.', 'warning')
        return redirect(url_for('main.index'))

    form = FormulaireProduit()
    if form.validate_on_submit():
        produit = Produit(
            nom=form.nom.data,
            description=form.description.data,
            prix=form.prix.data,
            unite=form.unite.data,
            quantite=form.quantite.data,
            categorie=form.categorie.data,
            localisation=form.localisation.data,
            utilisateur_id=current_user.id
        )
        db.session.add(produit)
        db.session.commit()
        flash(f'Produit "{produit.nom}" publié avec succès ! 🌽', 'success')
        return redirect(url_for('main.produits'))

    return render_template('publier_produit.html', form=form)


# ─────────────────────────────
# ENVOYER UN MESSAGE
# ─────────────────────────────
@main.route('/contacter/<int:produit_id>', methods=['GET', 'POST'])
@login_required
def contacter(produit_id):
    produit = Produit.query.get_or_404(produit_id)

    if current_user.role != 'acheteur':
        flash('Seuls les acheteurs peuvent envoyer des messages.', 'warning')
        return redirect(url_for('main.detail_produit', id=produit_id))

    if current_user.id == produit.utilisateur_id:
        flash('Vous ne pouvez pas vous contacter vous-même.', 'warning')
        return redirect(url_for('main.detail_produit', id=produit_id))

    form = FormulaireMessage()
    if form.validate_on_submit():
        message = Message(
            contenu=form.contenu.data,
            expediteur_id=current_user.id,
            produit_id=produit.id
        )
        db.session.add(message)
        db.session.commit()
        flash('✅ Message envoyé à l\'agriculteur !', 'success')
        return redirect(url_for('main.detail_produit', id=produit_id))

    return render_template('contacter.html', form=form, produit=produit)


# ─────────────────────────────
# VOIR SES MESSAGES (agriculteur)
# ─────────────────────────────
@main.route('/mes-messages')
@login_required
def mes_messages():
    if current_user.role != 'agriculteur':
        flash('Accès réservé aux agriculteurs.', 'warning')
        return redirect(url_for('main.index'))

    # Récupère tous les messages liés aux produits de l'agriculteur
    messages = Message.query\
        .join(Produit, Message.produit_id == Produit.id)\
        .filter(Produit.utilisateur_id == current_user.id)\
        .order_by(Message.date_envoi.desc()).all()

    # Marque tous les messages comme lus
    for msg in messages:
        if not msg.lu:
            msg.lu = True
    db.session.commit()

    return render_template('mes_messages.html', messages=messages)