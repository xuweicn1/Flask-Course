# Note1：Flask-Basics

[toc]



## Flask 虚拟环境

```
> py -m venv env
> .\env\Scripts\activate
> python -m pip install --upgrade pip
> pip install flask
> deactivate
```

## 两种启动方式

### 1. 脚本带`app.run()`

```
# app.py
from flask import Flask
app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello  Word</h1>'


if __name__ == '__main__':
    app.run()
```
运行：
```
> python app.py
```

### 2. `flask run`

```
#app.py
from flask import Flask
app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello  Word</h1>'
```

运行
```
# 声明环境
> set FLASK_APP=app.py
> flask run
```
> win 用set, linux：export

> 可以新建`.flaskenv`声明环境

```
# .flaskenv
FLASK_APP=app.py
```
## route 方法

### 1. 基本方法
```
from flask import Flask, jsonify
app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello  Word</h1>'


@app.route('/home')
def home():
    return '<h1>现在是主页</h1>'
```

### 2. JSON响应： jsonify
```

@app.route('/json')
def json():
    return jsonify({'key': 'value', 'key2': [1, 2, 3]})
```
### 3. POST和GET

```
# @app.route('/test')  # get only
# @app.route('/test', methods=['POST', 'GET'])   # get and post
# @app.route('/test', methods=['POST'])  # post only
# def test():
#     pass
```
    
### 4. 变量

```
@app.route('/home', defaults={'name':'张三'})
@app.route('/home/<string:name>', methods=['POST', 'GET'])
def home(name):
    print(type(name))
    return '<h1>你好:{}，现在是主页</h1>'.format(name)
```
> 定义默认值:`@app.route('/home', defaults={'name':'张三'})`



## 请求request


```
from flask import request
request.args['name']    # 需要参数
request.form['name']    # 表单
request.method          #方法中
request.cookies.get('cookie_name') #cookies
request.files['name']   #  文件中
```


### 1. 接收参数数据
```
from flask import request

@app.route('/query')
def query():
    name = request.args.get('name')
    location = request.args.get('location')
    return '<h1>姓名：{}位置：{}请求页面</h1>'.format(name, location)
```

### 2. 接收表单数据


```
@app.route('/theform')
def theform():
    return '''<form method="POST" action="/process">
                <input type="text" name="name">
                <input type="text" name="location">
                <input type="submit" value="输入">
                </form>'''


@app.route('/process', methods=['POST'])
def process():
    name = request.form['name']
    location = request.form['location']
    return '<h1>姓名：{} <br> 位置：{} <br>表单页面</h1>'.format(name, location)
```
### 3. 接收json数据

```
@app.route('/processjson', methods=['POST'])
def processjson():
    data = request.get_json()
    name = data['name']
    location = data['location']
    randomlist = data['randomlist']
    return jsonify({'name': name, 'location': location, 'randomlist': randomlist})
```
**postman工具**
![](https://img2018.cnblogs.com/blog/720033/201907/720033-20190727082254766-1876964305.png)
### 4. request.method

#### 方法1：if判定
```
@app.route('/theform', methods=['POST', 'GET'])
def theform():
    if request.method == 'GET':
        return '''<form method="POST" action="/theform">
                    <input type="text" name="name"><br><br>
                    <input type="text" name="location"><br><br>
                    <input type="submit" value="输入">
                    </form>'''
    else:
        name = request.form['name']
        location = request.form['location']
        return '<h1>姓名：{} <br> 位置：{} <br>表单页面</h1>'.format(name, location)
```

#### 方法2：对get、put不同解析
```
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
```


## 重定向 Redirects and url_for


重定向到home页，

- `home`函数名，name参数，会被解析；
- location不会被解析

```
return redirect(url_for('home', name=name, location=location))
```

```
from flask import url_for, redirect
……


@app.route('/theform', methods=['POST', 'GET'])
def theform():
    if request.method == 'GET':
        return '''<form method="POST" action="/theform">
                    <input type="text" name="name"><br><br>
                    <input type="text" name="location"><br><br>
                    <input type="submit" value="输入">
                    </form>'''
    else:
        name = request.form['name']
        location = request.form['location']
        return redirect(url_for('home', name=name, location=location))  #
```


## 配置config


### 1. 直接声明

```
app.config['CONFIG_NAME'] = 'config value'
app.config['DEBUG'] = True  #开启debug 相当于app.run(debug=True)

```


### 2. 导入配置文件

```
app.config.from_envvar('ENV_VAR_NAME')
```

## session会话

```
from flask import session

app.config['SECRET_KEY'] = 'This is a secret'   # 使用会话必须设置


@app.route('/login_success')
def login_success():
    """设置会话"""
    session['key_name'] = 'key_value'   # 从浏览器cookie获取
    return redirect(url_for('index'))


@app.route('/')
def index():
    """读取会话"""
    if 'key_name' in session:
        session_var = session['key_value']
    else:  # 会话不存在
```

### 1. 创建sesson

```
@app.route('/home', defaults={'name': '张三'})
@app.route('/home/<string:name>', methods=['POST', 'GET'])
def home(name):
    session['name'] = name
    return '<h1>你好:{}，<br>现在是主页</h1>'.format(name)
```

### 2.引用sesson
```
@app.route('/json')
def json():
    if 'name' in session:
        name = session['name']
    else:
        name = 'NotinS'
    return jsonify({'key': 'value', 'key2': [1, 2, 3], 'name': name})
```

### 3.删除sesson
```
@app.route('/')
def index():
    session.pop('name', None)
    return '<h1>Hello  Word</h1>'
```



## abort错误


```
from flask import abort


@app.route('/err')
def err():
    abort(406)  # 返回404错误，下面不执行
    return '这里不出现'

@app.errorhandler(406)
def page_not_found(error):
    return '定义错误页面'
    return render_template('page_not_found.html'), 404
```

## Cookie

### 存储Cookie

```
from flask import make_response


@app.route('/')
def index():
    resp = make_response(render_template('index.html'))
    resp.set_cookie('cookie_name', 'cookie_value')
    # resp.set_cookie('username', 'the username')
    return resp
```

### 读取Cookie

```
from flask import request

@app.route('/cok')
def cok():
    username = request.cookies.get('cookie_name')
    return username
```


## 本章代码


```
from flask import Flask, jsonify, request, redirect, url_for, session

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
    return '<h1>你好:{}，<br>现在是主页</h1>'.format(name)


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
        return '''<form method="POST" action="/theform">
                    <input type="text" name="name"><br><br>
                    <input type="text" name="location"><br><br>
                    <input type="submit" value="输入">
                    </form>'''
    else:
        name = request.form['name']
        location = request.form['location']
        return redirect(url_for('home', name=name, location=location))
        # return '<h1>姓名：{} <br> 位置：{} <br>表单页面</h1>'.format(name, location)


if __name__ == '__main__':
    app.run(debug=True)
```



## 常用库

[Flask-PyMongo](
https://flask-pymongo.readthedocs.io/en/latest/)

[Flask-SQLAlchemy](
https://pypi.org/project/Flask-SQLAlchemy/)

[Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/)


[Flask-Mail](https://pythonhosted.org/Flask-Mail/)

[Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/)

[Flask-Uploads](https://flask-uploads.readthedocs.io/en/latest/)

[Flask-Login](https://flask-login.readthedocs.io/en/latest/)

[Flask-User](https://flask-user.readthedocs.io/en/v0.6/)


## 网站

[Flask’s documentation](https://flask.palletsprojects.com/en/1.1.x/)

