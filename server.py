from flask import request
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)
        return {'coucou': 'coucoutext'}
    else:
        return 'coucou'

@app.route('/paiement', methods=['POST'])
def paiement():
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data, request, type(request))
        return "Merci, c'est tout bon !"
    else:
        return 'Only POST supported'
