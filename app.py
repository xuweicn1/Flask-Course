from flask import Flask, jsonify, request, redirect, url_for, session,render_template,g
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'This is a secret'

def connect_db():
    """连接数据库"""
    rv = sqlite3.connect('data.db')
    rv.row_factory = sqlite3.Row #以字典形式访问,默认是元组
    return rv

def get_db():
    """如果会话中没有数据库连接，启用新连接 """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """请求后关闭连接"""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def index():
    session.pop('name', None)
    return '<h1>Hello  Word</h1>'


@app.route('/home', defaults={'name': '张三'})
@app.route('/home/<string:name>', methods=['POST', 'GET'])
def home(name):
    """模板展示所有数据"""
    session['name'] = name
    db = get_db()
    cur = db.execute('select id,name,location from users')
    results = cur.fetchall()
    return render_template('home.html',name=name,disply=True,\
        mylist=['one','two','three'],\
        mydict=[{'name':'张五','location':'北京'},{'name':'赵六','location':'上海'}],\
        results=results
        )


@app.route('/json')
def json():
    if 'name' in session:
        name = session['name']
    else:
        name = 'NotinS'
    return jsonify({'key': 'value', 'key2': [1, 2, 3], 'name': name})


@app.route('/query')
def query():
    name = request.args.get('name')
    location = request.args.get('location')
    return '<h1>姓名：{}<br>位置：{}<br>请求页面</h1>'.format(name, location)


@app.route('/processjson', methods=['POST'])
def processjson():
    data = request.get_json()
    name = data['name']
    location = data['location']
    randomlist = data['randomlist']
    return jsonify({'name': name, 'location': location, 'randomlist': randomlist})

@app.route('/theform', methods=['POST', 'GET'])
def theform():
    """插入数据"""
    if request.method == 'GET':
        return render_template('form.html')
    else:
        name = request.form['name']
        location = request.form['location']
        db = get_db()
        db.execute('insert into users(name,location) values (?,?)',[name,location])
        db.commit()
        return redirect(url_for('home', name=name, location=location))

@app.route('/viewresults')
def viewresults():
    """表单查询"""
    db=get_db()
    cur = db.execute('select id,name,location from users')
    results = cur.fetchall()
    return '<h1>id:{} ,name:{},location:{}</h1>'.format(results[1]['id'],results[1]['name'],results[1]['location'])


if __name__ == '__main__':
    app.run(debug=True)
