import os
import uuid
from datetime import datetime
from functools import wraps
from pathlib import Path
from email.message import EmailMessage
import smtplib

from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from wtforms import DateField, PasswordField, SelectField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')
UPLOAD_FOLDER = Path(os.environ.get('UPLOAD_FOLDER', BASE_DIR / 'uploads'))
DATABASE_PATH = Path(os.environ.get('DATABASE_PATH', BASE_DIR / 'data' / 'app.db'))

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-secret-key'),
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', f'sqlite:///{DATABASE_PATH}'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    UPLOAD_FOLDER=str(UPLOAD_FOLDER),
    MAIL_SERVER=os.environ.get('MAIL_SERVER', ''),
    MAIL_PORT=int(os.environ.get('MAIL_PORT', 25)),
    MAIL_USE_TLS=os.environ.get('MAIL_USE_TLS', 'false').lower() == 'true',
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER=os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@example.com'),
)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

ALLOWED_EXTENSIONS = {'pdf'}
CASE_TYPES = [
    ('fournitures_informatiques', 'Fournitures informatiques'),
    ('fournitures_telephoniques', 'Fournitures téléphoniques'),
    ('logiciel', 'Logiciel'),
    ('location_informatique', 'Location informatique'),
    ('maintenance', 'Maintenance'),
    ('entrep_materiel', 'Ent rép matériel'),
    ('liaisons_informatiques', 'Liaisons informatiques'),
    ('telephonie', 'Téléphonie'),
    ('abonnements', 'Abonnements'),
    ('prestations', 'Prestations'),
]

DOCUMENT_TYPES = {
    'quote': 'Devis',
    'purchase_order': 'Bon de commande',
    'reception': 'Bon de réception',
}


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(32), nullable=False)
    verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    cases_created = db.relationship('Case', backref='engineer', foreign_keys='Case.engineer_id')
    documents_uploaded = db.relationship('Document', backref='uploader', foreign_keys='Document.uploaded_by_id')
    documents_signed = db.relationship('Document', backref='signer', foreign_keys='Document.signer_id')

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def can_create_case(self) -> bool:
        return self.role == 'engineer'

    def can_upload(self, case) -> bool:
        if self.role == 'supplier':
            return self.email.lower() == (case.supplier_email or '').lower()
        if self.role == 'buyer':
            return case.has_signed_quote()
        return False

    def can_sign(self, document) -> bool:
        return self.role == 'engineer' and self.id == document.case.engineer_id


class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    type = db.Column(db.String(80), nullable=False)
    object_contract = db.Column(db.String(200), nullable=True)
    start_date = db.Column(db.String(20), nullable=True)
    duration = db.Column(db.String(100), nullable=True)
    market = db.Column(db.String(120), nullable=True)
    budget = db.Column(db.String(120), nullable=True)
    uf_number = db.Column(db.String(120), nullable=True)
    supplier_email = db.Column(db.String(120), nullable=False)
    provider_designation = db.Column(db.String(200), nullable=True)
    supplier_contact = db.Column(db.String(120), nullable=True)
    billing_terms = db.Column(db.String(120), nullable=True)
    invoice_on_delivery = db.Column(db.Boolean, default=False)
    invoice_on_order = db.Column(db.Boolean, default=False)
    account_number = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    engineer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    documents = db.relationship('Document', backref='case', lazy=True)

    def get_document(self, doc_type):
        return Document.query.filter_by(case_id=self.id, type=doc_type).order_by(Document.uploaded_at.desc()).first()

    def has_signed_quote(self):
        quote = self.get_document('quote')
        return bool(quote and quote.is_signed)

    def has_purchase_order(self):
        return bool(self.get_document('purchase_order'))

    def has_signed_reception(self):
        receipt = self.get_document('reception')
        return bool(receipt and receipt.is_signed)


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'), nullable=False)
    type = db.Column(db.String(32), nullable=False)
    filename = db.Column(db.String(250), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_signed = db.Column(db.Boolean, default=False)
    signed_at = db.Column(db.DateTime, nullable=True)
    signer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def display_type(self):
        return DOCUMENT_TYPES.get(self.type, self.type)


class VerificationToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('verification_token', uselist=False))


class LoginForm(FlaskForm):
    username = StringField('Nom d’utilisateur', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')


class RegisterForm(FlaskForm):
    username = StringField('Nom d’utilisateur', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Adresse e-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField('Confirmer le mot de passe', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Créer un compte fournisseur')


class CaseForm(FlaskForm):
    title = StringField('Titre de l’affaire', validators=[DataRequired()])
    description = TextAreaField('Description')
    type = SelectField('Type de prestation', choices=CASE_TYPES, validators=[DataRequired()])
    object_contract = StringField('Objet du contrat')
    start_date = StringField('Date d’effet')
    duration = StringField('Durée')
    market = StringField('Marché')
    budget = StringField('Budget investissement H')
    uf_number = StringField('N° UF')
    supplier_email = StringField('Courriel du fournisseur', validators=[DataRequired(), Email()])
    provider_designation = StringField('Désignation commande')
    supplier_contact = StringField('Adresse mail envoi commande')
    billing_terms = SelectField('Modalité de facturation', choices=[('mensuel', 'mensuel'), ('trimestriel', 'trimestriel'), ('autre', 'Autre')])
    invoice_on_delivery = SelectField('Facturation à réception de PV', choices=[('oui', 'Oui'), ('non', 'Non')])
    invoice_on_order = SelectField('Facturation à réception de commande', choices=[('oui', 'Oui'), ('non', 'Non')])
    account_number = StringField('N° de compte')
    submit = SubmitField('Créer l’affaire')


class UploadForm(FlaskForm):
    document = StringField('Document')
    submit = SubmitField('Téléverser le fichier PDF')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def ensure_directories():
    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)


def seed_users():
    created = False

    if not User.query.filter_by(username='engineer').first():
        engineer = User(username='engineer', email='engineer@example.com', role='engineer', verified=True)
        engineer.set_password('password')
        db.session.add(engineer)
        created = True

    if not User.query.filter_by(username='buyer').first():
        buyer = User(username='buyer', email='buyer@example.com', role='buyer', verified=True)
        buyer.set_password('password')
        db.session.add(buyer)
        created = True

    if not User.query.filter_by(username='supplier').first():
        supplier = User(username='supplier', email='supplier@example.com', role='supplier', verified=True)
        supplier.set_password('password')
        db.session.add(supplier)
        created = True

    if created:
        db.session.commit()
        app.logger.info('Created demo users: engineer/password, buyer/password and supplier/password')


def send_email(recipient: str, subject: str, body: str):
    if not app.config['MAIL_SERVER']:
        app.logger.info('Email stub to %s: %s', recipient, subject)
        app.logger.info(body)
        return

    message = EmailMessage()
    message['Subject'] = subject
    message['From'] = app.config['MAIL_DEFAULT_SENDER']
    message['To'] = recipient
    message.set_content(body)

    try:
        smtp = smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT'], timeout=10)
        if app.config['MAIL_USE_TLS']:
            smtp.starttls()
        if app.config['MAIL_USERNAME'] and app.config['MAIL_PASSWORD']:
            smtp.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        smtp.send_message(message)
        smtp.quit()
    except Exception as exc:
        app.logger.warning('Email send failed: %s', exc)


db_initialized = False


def user_required(role):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                flash('Accès refusé.', 'warning')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)

        return wrapped

    return decorator


def initialize_database():
    global db_initialized
    if db_initialized:
        return

    ensure_directories()
    db.create_all()
    seed_users()
    db_initialized = True


@app.before_request
def before_request():
    initialize_database()


@app.route('/')
@login_required
def dashboard():
    if current_user.role == 'engineer':
        cases = Case.query.filter_by(engineer_id=current_user.id).order_by(Case.created_at.desc()).all()
    elif current_user.role == 'supplier':
        cases = Case.query.filter(Case.supplier_email.ilike(f'%{current_user.email}%')).order_by(Case.created_at.desc()).all()
    else:
        cases = Case.query.order_by(Case.created_at.desc()).all()
    return render_template('dashboard.html', cases=cases)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            if not user.verified:
                flash('Votre compte n’est pas vérifié. Vérifiez votre email.', 'warning')
            else:
                login_user(user)
                return redirect(url_for('dashboard'))
        else:
            flash('Nom d’utilisateur ou mot de passe incorrect.', 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter((User.username == form.username.data) | (User.email == form.email.data)).first()
        if existing_user:
            flash('Le nom d’utilisateur ou l’adresse e-mail existe déjà.', 'warning')
        else:
            user = User(
                username=form.username.data,
                email=form.email.data,
                role='supplier',
                verified=False,
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            token = VerificationToken(user_id=user.id, token=str(uuid.uuid4()))
            db.session.add(token)
            db.session.commit()
            verify_url = url_for('verify_email', token=token.token, _external=True)
            send_email(
                user.email,
                'Vérifiez votre adresse e-mail',
                f'Bonjour {user.username},\n\nCliquez sur le lien pour vérifier votre compte:\n{verify_url}',
            )
            flash('Inscription réussie. Vérifiez votre email pour activer votre compte.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/verify/<token>')
def verify_email(token):
    verification = VerificationToken.query.filter_by(token=token).first()
    if verification and verification.user:
        verification.user.verified = True
        db.session.delete(verification)
        db.session.commit()
        flash('Compte vérifié, vous pouvez vous connecter.', 'success')
    else:
        flash('Lien de vérification invalide ou expiré.', 'danger')
    return redirect(url_for('login'))


@app.route('/cases/new', methods=['GET', 'POST'])
@login_required
@user_required('engineer')
def create_case():
    form = CaseForm()
    if form.validate_on_submit():
        case = Case(
            title=form.title.data,
            description=form.description.data,
            type=form.type.data,
            object_contract=form.object_contract.data,
            start_date=form.start_date.data,
            duration=form.duration.data,
            market=form.market.data,
            budget=form.budget.data,
            uf_number=form.uf_number.data,
            supplier_email=form.supplier_email.data,
            provider_designation=form.provider_designation.data,
            supplier_contact=form.supplier_contact.data,
            billing_terms=form.billing_terms.data,
            invoice_on_delivery=form.invoice_on_delivery.data == 'oui',
            invoice_on_order=form.invoice_on_order.data == 'oui',
            account_number=form.account_number.data,
            engineer_id=current_user.id,
        )
        db.session.add(case)
        db.session.commit()

        supplier = User.query.filter_by(email=case.supplier_email).first()
        if supplier and supplier.verified:
            send_email(
                supplier.email,
                'Un devis a été demandé pour une nouvelle affaire',
                f'Une nouvelle affaire a été créée et vous êtes invité à déposer un devis pour {case.title}.',
            )

        flash('Affaire créée. Le fournisseur peut déposer son devis.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('case_form.html', form=form)


@app.route('/cases/<int:case_id>')
@login_required
def case_detail(case_id):
    case = Case.query.get_or_404(case_id)
    quote = case.get_document('quote')
    purchase_order = case.get_document('purchase_order')
    reception = case.get_document('reception')
    return render_template(
        'case_detail.html',
        case=case,
        quote=quote,
        purchase_order=purchase_order,
        reception=reception,
        doc_types=DOCUMENT_TYPES,
    )


@app.route('/cases/<int:case_id>/upload/<string:doc_type>', methods=['GET', 'POST'])
@login_required
def upload_document(case_id, doc_type):
    if doc_type not in DOCUMENT_TYPES:
        flash('Type de document invalide.', 'danger')
        return redirect(url_for('case_detail', case_id=case_id))

    case = Case.query.get_or_404(case_id)
    if not current_user.can_upload(case):
        flash('Vous ne pouvez pas téléverser ce document.', 'warning')
        return redirect(url_for('case_detail', case_id=case_id))

    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '':
            flash('Aucun fichier sélectionné.', 'warning')
            return redirect(request.url)
        if not allowed_file(file.filename):
            flash('Seuls les fichiers PDF sont autorisés.', 'danger')
            return redirect(request.url)

        filename = secure_filename(file.filename)
        unique_name = f'{case.id}_{doc_type}_{uuid.uuid4().hex}_{filename}'
        file_path = UPLOAD_FOLDER / unique_name
        file.save(file_path)

        document = Document(
            case_id=case.id,
            type=doc_type,
            filename=unique_name,
            uploaded_by_id=current_user.id,
        )
        db.session.add(document)
        db.session.commit()

        subject = f'{DOCUMENT_TYPES[doc_type]} déposé pour l’affaire {case.title}'
        if current_user.role == 'supplier':
            recipients = [case.engineer.email]
            body = f'Le devis a été déposé par le fournisseur pour l’affaire {case.title}. Connectez-vous pour signer.'
        elif current_user.role == 'buyer':
            recipients = [case.engineer.email, case.supplier_email]
            body = f'Le {DOCUMENT_TYPES[doc_type].lower()} a été déposé pour l’affaire {case.title}. Connectez-vous pour le consulter.'
        else:
            recipients = [case.engineer.email]
            body = f'Le {DOCUMENT_TYPES[doc_type].lower()} a été déposé pour l’affaire {case.title}.'

        for recipient in set(recipients):
            send_email(recipient, subject, body)
        flash('Document téléchargé.', 'success')
        return redirect(url_for('case_detail', case_id=case.id))

    return render_template('upload.html', case=case, doc_type=doc_type, doc_label=DOCUMENT_TYPES[doc_type])


@app.route('/documents/<path:filename>')
@login_required
def document_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)


@app.route('/documents/<int:document_id>/view')
@login_required
def view_document(document_id):
    document = Document.query.get_or_404(document_id)
    return send_from_directory(UPLOAD_FOLDER, document.filename, as_attachment=False)


@app.route('/documents/<int:document_id>/sign')
@login_required
def sign_document(document_id):
    document = Document.query.get_or_404(document_id)
    case = document.case
    if current_user.role != 'engineer' or current_user.id != case.engineer_id:
        flash('Vous ne pouvez pas signer ce document.', 'warning')
        return redirect(url_for('case_detail', case_id=case.id))

    document.is_signed = True
    document.signed_at = datetime.utcnow()
    document.signer_id = current_user.id
    db.session.commit()

    recipients = [case.engineer.email, case.supplier_email]
    if case.has_signed_quote() and document.type == 'quote':
        subject = f'Devis signé pour l’affaire {case.title}'
        body = 'Le devis a été signé par l’ingénieur. Le service achats peut maintenant déposer le bon de commande.'
    elif document.type == 'purchase_order':
        subject = f'Bon de commande signé pour l’affaire {case.title}'
        body = 'Le bon de commande a été signé. Le bon de réception peut être déposé.'
    else:
        subject = f'Bon de réception signé pour l’affaire {case.title}'
        body = 'Le bon de réception a été signé par l’ingénieur. Le dossier est prêt pour la facturation.'

    for recipient in set(recipients):
        send_email(recipient, subject, body)

    flash('Document signé.', 'success')
    return redirect(url_for('case_detail', case_id=case.id))


if __name__ == '__main__':
    ensure_directories()
    db.create_all()
    app.run(host='0.0.0.0', port=8000, debug=True)
