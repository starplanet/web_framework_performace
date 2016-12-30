from sanic import Sanic
from sanic.response import json

app = Sanic("test")


@app.route("/")
async def test(request):
    return json({"test": True})

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, workers=1)
