from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import ImageUploadField

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '2722'

# Configuração para upload de imagens
app.config['UPLOAD_FOLDER'] = 'static/img/'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define o modelo para os itens do carrossel
class CarouselItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_filename = db.Column(db.String(100), nullable=False)
    caption = db.Column(db.String(200))
    link_text = db.Column(db.String(100))
    team_type = db.Column(db.String(50))  # Adicionando o tipo de equipe
    link_url = db.Column(db.String(200))

# Define a visualização para o Flask-Admin
class CarouselItemAdmin(ModelView):
    form_columns = ['image_filename', 'caption','link_text', 'team_type', 'link_url']
    
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
    evento = db.Column(db.String(100))  # Adicione o campo evento

    carousel_item_id = db.Column(db.Integer, db.ForeignKey('carousel_item.id', name='fk_resposta_carousel_item'))
    carousel_item = db.relationship('CarouselItem', backref=db.backref('respostas', lazy=True))



# Define a visualização para o Flask-Admin para o modelo Resposta
class RespostaAdmin(ModelView):
    form_columns = ['nome', 'tocar', 'cantar', 'receber_email', 'email', 'evento', 'carousel_item']

# Registra os modelos e as visualizações no Flask-Admin
admin = Admin(app, name='Painel de Administração', template_mode='bootstrap3')
admin.add_view(CarouselItemAdmin(CarouselItem, db.session))
admin.add_view(RespostaAdmin(Resposta, db.session))

from flask import request

@app.route('/')
def index():
    respostas = Resposta.query.all()
    print("Respostas encontradas:")
    for resposta in respostas:
        print(f"Nome: {resposta.nome}, Evento: {resposta.evento}, Tocar: {resposta.tocar}, Cantar: {resposta.cantar}")  
        # Imprime o nome, evento, tocar e cantar de cada resposta
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

    resposta = Resposta(nome=nome, tocar=tocar, cantar=cantar, receber_email=receber_email, email=email, evento=evento, carousel_item_id=carousel_item_id)  # Adiciona o evento à resposta
    db.session.add(resposta)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')



@app.route('/form.html/<domingo>', methods=['GET', 'POST'])
def form(domingo):
    if request.method == 'POST':
        return redirect(url_for('enviar', domingo=domingo))  # Passa o valor de domingo para a função enviar()

 
    # Por exemplo:
    carousel_item = CarouselItem.query.filter_by(link_text=domingo).first()

    return render_template('form.html', domingo=domingo, carousel_item=carousel_item)

if __name__ == '__main__':
    app.run(debug=True)
