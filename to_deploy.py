from flask import Flask
app = Flask(__name__)

@app.route('/hello.json')
def hello_world():
    return {'msg': 'Hello, World!'}
if __name__ == "__main__":
    app.run(host='0.0.0.0')
