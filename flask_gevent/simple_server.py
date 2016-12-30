import ujson
from flask import Flask
from gevent.wsgi import WSGIServer

app = Flask(__name__)

@app.route('/')
def index():
    return ujson.dumps({'test': True})

server = WSGIServer(('', 5000), app)
server.serve_forever()
