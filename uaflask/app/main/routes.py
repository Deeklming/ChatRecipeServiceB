from app.main import bp
from flask import render_template, redirect, url_for
from flask import jsonify
from config import r

@bp.route('/', methods=['GET'])
def index():
    return jsonify({"connection": "ok!!"})

@bp.get('/getallcache')
def getallcache():
    data = {}
    for k in r.scan_iter():
        try:
            data[k] = r.get(k)
        except:
            data[k] = r.hgetall(k)
    print('cache data:', data)
    return jsonify(data)

@bp.route('/test', methods=['POST'])
def test():
    print('---redis-test---')

    a = r.get('foo')
    b = r.set('foo', 'bar')
    c = r.get('foo')
    print(a, b, c)
    print(type(a), type(b), type(c))

    b = r.set('foo', 21)
    c = r.get('foo')
    print(a, b, c)
    print(type(a), type(b), type(c))

    a = r.hgetall('user')
    b = r.hset('user', mapping={
        'name': 'John',
        "surname": 'Smith',
        "company": 'Redis',
        "age": 29
    })
    c = r.hgetall('user')
    print(a, b, c)
    print(type(a), type(b), type(c))
    print(type(c['age']))
    r.flushdb()

    try:
        raise Exception('abc')
    except Exception as err:
        print(err.__str__())
        print(type(err.__str__()))

    return jsonify({"test": "ok!"})
