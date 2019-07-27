# Note2：Templates

[toc]



## 简介

```
from flask import render_template

@app.route('/theform', methods=['POST', 'GET'])
def theform():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        name = request.form['name']
        location = request.form['location']
        return redirect(url_for('home', name=name, location=location))
```

`templates/form.html`

```
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>地址</title>
</head>

<body>
    <h1>请填写地址</h1>
    <form method="POST" action="/theform">
        <input type="text" name="name"><br><br>
        <input type="text" name="location"><br><br>
        <input type="submit" value="输入">
    </form>
</body>
</html>
```



## 变量


### `{{}}`获取传递来的变量
```
@app.route('/home', defaults={'name': '张三'})
@app.route('/home/<string:name>', methods=['POST', 'GET'])
def home(name):
    session['name'] = name
    return render_template('home.html',name=name)
```

`templates/home.html`

```
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>home</title>
</head>

<body>
    <h1>你好:{{name}}，现在是主页</h1>
</body>

</html>
```
## 控制语句

### {% %}声明语句
```
@app.route('/home', defaults={'name': '张三'})
@app.route('/home/<string:name>', methods=['POST', 'GET'])
def home(name):
    session['name'] = name
    return render_template('home.html',name=name,disply=True)
```

模板中
```
<h1>你好:{{name}}，现在是主页</h1>
{% if disply %}
<h2>这个将被展示</h2>
{% else%}
<h2>这个不会被展示</h2>
{% endif%}
```

## for


```
@app.route('/home', defaults={'name': '张三'})
@app.route('/home/<string:name>', methods=['POST', 'GET'])
def home(name):
    session['name'] = name
    return render_template('home.html',name=name,disply=True,mylist=['one','two','three'])
```



```
{% for x in mylist%}
<h3>{{x}}</h3>
{%endfor%}
```

## 字典解析

```
return render_template('home.html',mydict=[{'name':'张五','location':'北京'},{'name':'赵六','location':'上海'}])
```

```
{% for x in mydict%}
<h3>{{x.name}}</h3>
<h3>{{x['location']}}</h3>
{%endfor%}
```

## 静态文件

新建文件
`static/img`

图片地址：`static/img/bee.png`
调用
```
<img src="{{ url_for('static',filename='img/bee.png')}}">
```

## 模板的继承

### 继承

`base.html`
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{%block title%}{%endblock%}</title>
</head>
<body>
<h1>基础模板</h1>
{%block content%}{%endblock%}
</body>
</html>
```

继承`base.html`
```
{%extends 'base.html'%}

{%block title%}主页{%endblock%}

{%block content%}
<h1>你好:{{name}}，现在是主页</h1>
{% if disply %}
<h2>这个将被展示</h2>
{% else%}
<h2>这个不会被展示</h2>
{% endif%}
{% for x in mylist%}
<h3>{{x}}</h3>
{%endfor%}
{% for x in mydict%}
<h3>{{x.name}}</h3>
<h3>{{x['location']}}</h3>
{%endfor%}
<img src="{{ url_for('static',filename='img/bee.png')}}">
{%endblock%}
```
### 子继承

使用方法：
```
{%extends 'base.html'%}
{%block content%}
{%endblock%}
{%endblock%}
```

案例：

`base.html`
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{%block title%}{%endblock%}</title>
</head>
<body>
<h1>基础模板</h1>
{%block content%}
<h2>基础模板中的元素</h2>
{%endblock%}
</body>
</html>
```
`home.html`
```
{%extends 'base.html'%}

{%block title%}主页{%endblock%}

{%block content%}
{{super()}}
<h1>你好:{{name}}，现在是主页</h1>
{% if disply %}
<h2>这个将被展示</h2>
{% else%}
<h2>这个不会被展示</h2>
{% endif%}
{% for x in mylist%}
<h3>{{x}}</h3>
{%endfor%}
{% for x in mydict%}
<h3>{{x.name}}</h3>
<h3>{{x['location']}}</h3>
{%endfor%}
<img src="{{ url_for('static',filename='img/bee.png')}}">
{%endblock%}
```

## include引用

`home.html`
```
{%block content%}
{{super()}}

……

<img src="{{ url_for('static',filename='img/bee.png')}}">

{% include 'include_this.html'%}
{%endblock%}

```
this.html'%}
{%endblock%}

```
<h1>包含此页</h1>           #静态
<h2>此页有：{{name}}</h2>   #变量
```
