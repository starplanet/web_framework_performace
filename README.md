# web_framework_performace
test various web framework performance


### 测试环境

Darwin 16.3.0 i386 Darwin Kernel Version 16.3.0: Thu Nov 17 20:23:58 PST 2016; root:xnu-3789.31.2~1/RELEASE_X86_64

Cpython：3.6.0
ujson：1.34
flask: 0.12
tornado: 4.4.2
gunicorn: 19.6.0
gevent: 1.2.0
sanic: 0.1.9
wrk: 4.0.1


### flask单独测试

```
import ujson
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return ujson.dumps({'test': True})

if __name__ == ‘__main__’:
    app.run()
```

测试命令：wrk -t12 -c400 -d30s http://127.0.0.1:5000

测试结果：

```
Running 30s test @ http://127.0.0.1:5000
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    79.91ms   58.35ms 583.07ms   91.72%
    Req/Sec   127.62     67.96   346.00     67.76%
  16034 requests in 30.08s, 2.57MB read
  Socket errors: connect 0, read 1223, write 5, timeout 0
Requests/sec:    532.97
Transfer/sec:     87.44KB
```

### flask+gunicorn测试

测试代码同上，只是运行命令改为：gunicorn -w 1 -b 127.0.0.1:5000 simple_server:app

```
Running 30s test @ http://127.0.0.1:5000
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    62.66ms    8.41ms 102.33ms   92.44%
    Req/Sec   157.03     77.42   330.00     64.53%
  16592 requests in 30.08s, 2.74MB read
  Socket errors: connect 151, read 1042, write 4, timeout 0
Requests/sec:    551.59
Transfer/sec:     93.19KB
```

### flask+gevent测试

```
import ujson
from flask import Flask
from gevent.wsgi import WSGIServer

app = Flask(__name__)

@app.route('/')
def index():
    return ujson.dumps({'test': True})

server = WSGIServer(('', 5000), app)
server.serve_forever()
```

测试命令：wrk -t12 -c400 -d30s http://127.0.0.1:5000

```
Running 30s test @ http://127.0.0.1:5000
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   310.61ms  432.68ms   2.00s    81.70%
    Req/Sec   351.39    502.45     3.20k    87.72%
  88556 requests in 30.10s, 10.89MB read
  Socket errors: connect 0, read 276, write 0, timeout 570
Requests/sec:   2941.96
Transfer/sec:    370.62KB
```

### flask+gunicorn+gevent测试

```
import ujson
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return ujson.dumps({'test': True})

if __name__ == ‘__main__’:
    app.run()
```

服务启动命令：gunicorn -w 1 -b 127.0.0.1:5000 -k gevent simple_server:app

测试命令：wrk -t12 -c400 -d30s http://127.0.0.1:5000

```
Running 30s test @ http://127.0.0.1:5000
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.32ms   30.55ms   1.99s    99.90%
    Req/Sec     1.87k   698.82     2.27k    85.89%
  64765 requests in 30.10s, 10.99MB read
  Socket errors: connect 0, read 274, write 0, timeout 24
Requests/sec:   2151.58
Transfer/sec:    374.01KB
```

这个在运行会报错：

```
[2016-12-30 16:21:47 +0800] [46679] [ERROR] Socket error processing request.
Traceback (most recent call last):
  File "/Users/zhangjinjie/.pyenv/versions/3.6.0/envs/canal/lib/python3.6/site-packages/gunicorn/workers/async.py", line 62, in handle
    six.reraise(*sys.exc_info())
  File "/Users/zhangjinjie/.pyenv/versions/3.6.0/envs/canal/lib/python3.6/site-packages/gunicorn/six.py", line 625, in reraise
    raise value
  File "/Users/zhangjinjie/.pyenv/versions/3.6.0/envs/canal/lib/python3.6/site-packages/gunicorn/workers/async.py", line 52, in handle
    self.handle_request(listener_name, req, client, addr)
  File "/Users/zhangjinjie/.pyenv/versions/3.6.0/envs/canal/lib/python3.6/site-packages/gunicorn/workers/ggevent.py", line 152, in handle_request
    super(GeventWorker, self).handle_request(*args)
  File "/Users/zhangjinjie/.pyenv/versions/3.6.0/envs/canal/lib/python3.6/site-packages/gunicorn/workers/async.py", line 125, in handle_request
    six.reraise(*sys.exc_info())
  File "/Users/zhangjinjie/.pyenv/versions/3.6.0/envs/canal/lib/python3.6/site-packages/gunicorn/six.py", line 625, in reraise
    raise value
  File "/Users/zhangjinjie/.pyenv/versions/3.6.0/envs/canal/lib/python3.6/site-packages/gunicorn/workers/async.py", line 111, in handle_request
    resp.write(item)
  File "/Users/zhangjinjie/.pyenv/versions/3.6.0/envs/canal/lib/python3.6/site-packages/gunicorn/http/wsgi.py", line 362, in write
    util.write(self.sock, arg, self.chunked)
  File "/Users/zhangjinjie/.pyenv/versions/3.6.0/envs/canal/lib/python3.6/site-packages/gunicorn/util.py", line 302, in write
    sock.sendall(data)
  File "/Users/zhangjinjie/.pyenv/versions/3.6.0/envs/canal/lib/python3.6/site-packages/gevent/_socket3.py", line 418, in sendall
    data_sent += self.send(data_memory[data_sent:], flags)
  File "/Users/zhangjinjie/.pyenv/versions/3.6.0/envs/canal/lib/python3.6/site-packages/gevent/_socket3.py", line 391, in send
    return _socket.socket.send(self._sock, data, flags)
OSError: [Errno 41] Protocol wrong type for socket
```

### tornado测试

```
import ujson
from tornado import ioloop, web


class MainHandler(web.RequestHandler):
    def get(self):
        self.write(ujson.dumps({'test': True}))


app = web.Application([
    (r'/', MainHandler)
],  debug=False,
    compress_response=False,
    static_hash_cache=True
)

app.listen(5000)
ioloop.IOLoop.current().start()
```

服务启动命令：python simple_server.py

测试命令：wrk -t12 -c400 -d30s http://127.0.0.1:5000

```
Running 30s test @ http://127.0.0.1:5000
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   149.15ms   23.97ms 198.65ms   87.15%
    Req/Sec   211.59     60.37   444.00     68.43%
  75978 requests in 30.09s, 15.07MB read
  Socket errors: connect 0, read 444, write 0, timeout 0
Requests/sec:   2524.80
Transfer/sec:    512.85KB
```

### sanic测试

```
from sanic import Sanic
from sanic.response import json

app = Sanic("test")


@app.route("/")
async def test(request):
    return json({"test": True})

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, workers=1)
```

测试命令：wrk -t12 -c400 -d30s http://127.0.0.1:5000

```
Running 30s test @ http://127.0.0.1:5000
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    12.92ms    4.60ms  34.93ms   59.14%
    Req/Sec     2.51k   283.30     4.88k    81.10%
  898041 requests in 30.02s, 113.05MB read
  Socket errors: connect 0, read 338, write 0, timeout 0
Requests/sec:  29909.87
Transfer/sec:      3.77MB
```

但是使用ps -p 57403 -M查看线程数时，发现设置workers=1时，sanic实际运行时，会占用4个线程。

```
PID   TT   %CPU STAT PRI     STIME     UTIME COMMAND
57403 s001    0.0 S    31T   0:00.02   0:00.11 python simple_server.py
57403         0.0 S    31T   0:00.00   0:00.00
57403         0.0 S    31T   0:00.00   0:00.00
57403         0.0 S    31T   0:00.00   0:00.00
57403         0.0 S    31T   0:00.00   0:00.00
```

### 性能总结

各框架在返回简单JSON数据情况下，单worker测试性能：

框架|Requests/sec|Transfer/sec|Latency
-----|----|----|----|
flask|532.97|87.44KB|79.91ms(+-91.72%)|
flask+gunicorn|551.59|93.19KB|62.66ms(+-92.44%)|
flask+gevent|2941.96|370.62KB|310.61ms(+-81.72%)|
flask+gunicorn+gevent（这个运行时会报错）|2151.58|374.01KB|1.32ms(+-99.90%)|
tornado|2524.80|512.85KB|149.15ms(+-87.15%)|
sanic(会占用4个线程)|29909.87|3.77MB|12.92ms(+-59.4%)
