import ujson
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return ujson.dumps({'test': True})

if __name__ == '__main__':
    app.run()
