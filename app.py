from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import ImageUploadField
from flask_mail import Mail, Message




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '2722'

# Configuração para upload de imagens
app.config['UPLOAD_FOLDER'] = 'static/img/'

# Configuração do Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'severinogouveia59@gmail.com'
app.config['MAIL_PASSWORD'] = 'tnum eqeu oetl zkpt'
app.config['MAIL_DEFAULT_SENDER'] = 'severinogouveia59@gmail.com'

mail = Mail(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class CarouselItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_filename = db.Column(db.String(100), nullable=False)
    caption = db.Column(db.String(200))
    link_text = db.Column(db.String(100))
    team_type = db.Column(db.String(50))
    link_url = db.Column(db.String(200))

class CarouselItemAdmin(ModelView):
    form_columns = ['image_filename', 'caption', 'link_text', 'team_type', 'link_url']
    
    form_extra_fields = {
        'image_filename': ImageUploadField('Image',
                                           base_path=app.config['UPLOAD_FOLDER'],
                                           thumbnail_size=(100, 100, True))
    }

class Resposta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    tocar = db.Column(db.Integer)
    cantar = db.Column(db.Integer)
    receber_email = db.Column(db.Integer)
    email = db.Column(db.String(100))
    evento = db.Column(db.String(100))

    carousel_item_id = db.Column(db.Integer, db.ForeignKey('carousel_item.id', name='fk_resposta_carousel_item'))
    carousel_item = db.relationship('CarouselItem', backref=db.backref('respostas', lazy=True))

class RespostaAdmin(ModelView):
    form_columns = ['nome', 'tocar', 'cantar', 'receber_email', 'email', 'evento', 'carousel_item']

class MensagemEmail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    assunto = db.Column(db.String(100), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)

class MensagemEmailAdmin(ModelView):
    column_list = ['nome', 'email', 'assunto', 'mensagem']
    form_columns = ['nome', 'email', 'assunto', 'mensagem']

admin = Admin(app, name='Painel de Administração', template_mode='bootstrap3')
admin.add_view(CarouselItemAdmin(CarouselItem, db.session))
admin.add_view(RespostaAdmin(Resposta, db.session))
admin.add_view(MensagemEmailAdmin(MensagemEmail, db.session))

@app.route('/')
def index():
    respostas = Resposta.query.all()
    carousel_items = CarouselItem.query.all()
    team_types = set([item.team_type for item in carousel_items])
    return render_template('index.html', respostas=respostas, carousel_items=carousel_items, team_types=team_types)

@app.route('/enviar', methods=['POST'])
def enviar():
    nome = request.form['nome']
    tocar = 1 if 'tocar' in request.form else 0
    cantar = 1 if 'cantar' in request.form else 0
    receber_email = 1 if 'receberEmailCheckbox' in request.form else 0
    email = request.form['email'] if receber_email else None
    evento = request.form.get('domingo')  
    carousel_item_id = request.form.get('carousel_item_id')

    # Recuperando o objeto CarouselItem correspondente ao carousel_item_id
    carousel_item = CarouselItem.query.get(carousel_item_id)

    # Envio do email de confirmação
    if receber_email and email and carousel_item:
        msg = Message('Confirmação de Registro',
                      sender='severinogouveia59@gmail.com',
                      recipients=[email])
        msg.body = f'Olá {nome}, obrigado por se registrar para a {evento} no dia {carousel_item.caption} | {carousel_item.team_type}!'

        mail.send(msg)

    resposta = Resposta(nome=nome, tocar=tocar, cantar=cantar, receber_email=receber_email, email=email, evento=evento, carousel_item_id=carousel_item_id)  # Adiciona o evento à resposta
    db.session.add(resposta)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/enviar_email', methods=['POST'])
def enviar_email():
    nome = request.form['nome']
    email = request.form['email']
    assunto = request.form['assunto']
    mensagem = request.form['mensagem']

    # Configuração da mensagem de e-mail
    msg = Message(assunto, sender=email, recipients=['severinogouveia59@gmail.com'])
    msg.body = f'De: {nome}\nEmail: {email}\n\n{mensagem}'

    # Envio do e-mail
    try:
        mail.send(msg)
        return redirect('/thanks')  # Redireciona para a rota '/thanks' após o envio bem-sucedido
    except Exception as e:
        return str(e)


@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

@app.route('/form.html/<domingo>', methods=['GET', 'POST'])
def form(domingo):
    if request.method == 'POST':
        return redirect(url_for('enviar', domingo=domingo))
 
    carousel_item = CarouselItem.query.filter_by(link_text=domingo).first()

    return render_template('form.html', domingo=domingo, carousel_item=carousel_item)

@app.route('/enviar_formulario_email', methods=['POST'])
def enviar_formulario_email():
    nome = request.form['nome']
    email = request.form['email']
    assunto = request.form['assunto']
    mensagem = request.form['mensagem']

    # Salvar as informações no banco de dados
    try:
        nova_mensagem = MensagemEmail(nome=nome, email=email, assunto=assunto, mensagem=mensagem)
        db.session.add(nova_mensagem)
        db.session.commit()

        # Imprimir as informações no terminal
        print("Nome:", nome)
        print("Email:", email)
        print("Assunto:", assunto)
        print("Mensagem:", mensagem)

        # Configuração da mensagem de e-mail
        msg = Message(assunto, sender=email, recipients=['severinogouveia59@gmail.com'])
        msg.body = f'De: {nome}\nEmail: {email}\n\n{mensagem}'

        # Envio do e-mail
        try:
            mail.send(msg)
            print("E-mail enviado com sucesso de:", email)
            return redirect('/thanks')  # Redireciona para a rota '/thanks' após o envio bem-sucedido
        except Exception as e:
            print("Erro ao enviar e-mail:", str(e))
            return str(e)

    except Exception as e:
        return redirect('/thanks')  # Redireciona para a rota '/thanks' após o envio bem-sucedido

    
if __name__ == '__main__':
    app.run(debug=True)
