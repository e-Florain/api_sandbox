from flask import Flask
app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)
        return {'coucou': 'coucoutext'}

@app.route('/hello')
def hello_json():
    return {'msg': 'Hello, World!'}
if __name__ == "__main__":
    app.run(host='0.0.0.0')
