from flask import Flask, jsonify, request, redirect, url_for, session,render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'This is a secret'


@app.route('/')
def index():
    session.pop('name', None)
    return '<h1>Hello  Word</h1>'


@app.route('/home', defaults={'name': '张三'})
@app.route('/home/<string:name>', methods=['POST', 'GET'])
def home(name):
    session['name'] = name
    return render_template('home.html',name=name,disply=True,mylist=['one','two','three'],mydict=[{'name':'张五','location':'北京'},{'name':'赵六','location':'上海'}])


@app.route('/json')
def json():
    if 'name' in session:
        name = session['name']
    else:
        name = 'NotinS'
    return jsonify({'key': 'value', 'key2': [1, 2, 3], 'name': name})

# @app.route('/json')
# def json():
#     return jsonify({'key': 'value', 'liskey': [1, 2, 3]})


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

"""
@app.route('/theform')
def theform():
    return '''<form method="POST" action="/theform">
                <input type="text" name="name">
                <input type="text" name="location">
                <input type="submit" value="输入">
                </form>'''
@app.route('/theform', methods=['POST'])
def process():
    name = request.form['name']
    location = request.form['location']
    return '<h1>姓名：{} <br> 位置：{} <br>表单页面</h1>'.format(name, location)
"""

@app.route('/theform', methods=['POST', 'GET'])
def theform():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        name = request.form['name']
        location = request.form['location']
        return redirect(url_for('home', name=name, location=location))
        # return '<h1>姓名：{} <br> 位置：{} <br>表单页面</h1>'.format(name, location)


if __name__ == '__main__':
    app.run(debug=True)
