为了将使用 Flask 开发的网站部署到 Linux 服务器上，并且使用 `virtualenv` 创建虚拟环境进行部署，同时 **不使用 Nginx 反向代理**，我们可以按照以下步骤来完成：

### **步骤 1：本地导出项目依赖**
```plain
# 导出网站项目所用的全部依赖，cmd输入
pip freeze > requirements.txt
```

然后将整个项目上传到linux服务器，我上传的地址是/usr/local/myflask

### **步骤 2：创建和激活虚拟环境**
1. **安装virtualenv**

`virtualenv` 是一个创建虚拟环境的工具。可以通过 pip 安装它：

```bash
sudo pip3 install virtualenv
```

2. **创建虚拟环境**  
在你的 Flask 项目目录中创建一个新的虚拟环境：

```bash
cd /path/to/your/project
virtualenv ENV
```

这将创建一个名为 `ENV` 的虚拟环境。你可以替换 `ENV` 为你喜欢的名称。

3. **激活虚拟环境**在 Linux 中，激活虚拟环境可以使用以下命令：

```bash
source ENV/bin/activate
```

激活后，命令行提示符通常会显示虚拟环境的名称，表明你已经进入了虚拟环境。

4. **安装依赖**  
在虚拟环境中，使用 `pip` 安装项目的依赖。确保你有一个 `requirements.txt` 文件，它列出了所有需要的包。如果没有，首先安装 Flask 和其他必要的库。

```bash
pip install -r requirements.txt
```

5. 测试flask网站项目，确认正常运行。

```bash
python3 app.py
```

警告：生产环境要使用WSGI部署

### 步骤 3：部署到生产环境
1. 安装 Gunicorn

Gunicorn 是一个 Python WSGI HTTP 服务器，可以通过 `pip` 安装：

```bash
pip install flask gunicorn
```

2. gunicorn运行测试

在项目根目录下，确保你的 Flask 应用（假设为 `app.py`）定义了应用实例。然后，你可以使用 Gunicorn 来运行 Flask 应用，而不使用 Nginx 反向代理。启动 Flask 应用，使用 Gunicorn 启动服务：

```bash
gunicorn --workers 3 app:app
```

这样，Gunicorn 将启动 Flask 应用并监听 HTTP 请求，默认情况下监听 8000 端口。

    - `app:app` 表示 `app.py` 文件中的 `app` Flask 实例。
    - `--workers 3` 指定使用 3 个工作进程，你可以根据服务器的性能进行调整。

### **步骤 4：开通flask网站到公网**
1. **开放端口**  
默认情况下，Gunicorn 会监听 `127.0.0.1:8000`，这意味着只有本地机器能够访问该端口。如果你希望外部用户能够访问 Flask 应用，需要修改 Gunicorn 启动命令，指定 `0.0.0.0` 作为主机地址：

```bash
gunicorn --workers 3 --bind 0.0.0.0:8000 app:app
```

这将使 Flask 应用可以接受来自任何 IP 的请求。

2. **确保防火墙允许访问端口 8000**  
如果服务器启用了防火墙，你需要确保允许外部访问 8000 端口：

```bash
sudo firewall-cmd --zone=public --add-port=8000/tcp --permanent
sudo firewall-cmd --reload
```

_<u>因为没有使用nginx反向代理，所以要手动开启防火墙的8000端口</u>_

### **步骤 5：配置 Gunicorn 为系统服务（可选）**
你可以使用 `systemd` 将 Gunicorn 设置为系统服务，以便在服务器重启时自动启动 Flask 应用。

1. **创建 systemd 服务文件**在 `/etc/systemd/system/` 目录下创建一个新的服务文件：

```bash
sudo nano /etc/systemd/system/flaskapp.service
```

2. **添加以下内容**

```properties
[Unit]
Description=Gunicorn instance to serve Flask app
After=network.target

[Service]
User=youruser
Group=yourgroup
WorkingDirectory=/path/to/your/project
Environment="PATH=/path/to/your/project/ENV/bin"
ExecStart=/path/to/your/project/ENV/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 app:app

[Install]
WantedBy=multi-user.target
```

确保将 `youruser`, `yourgroup` 和 `/path/to/your/project` 替换为实际值。

3. **重新加载 systemd 配置并启动服务**

```bash
sudo systemctl daemon-reload
sudo systemctl start flaskapp
sudo systemctl enable flaskapp
```

这将确保你的 Flask 应用在系统启动时自动运行。

---

**检查网站：**

1. **验证 Flask 应用是否正在运行**你可以通过访问 `http://your-server-ip:8000` 来验证 Flask 应用是否正常工作。
2. **查看服务状态**如果你配置了 `systemd` 服务，可以使用以下命令查看服务状态：

```bash
sudo systemctl status flaskapp
```

---

### 总结：
+ 导出依赖包requirements.txt，上传网站项目
+ 在 Linux 服务器上，使用 `virtualenv` 创建一个虚拟环境
+ 在虚拟环境里安装requirements.txt里项目所需依赖
+ 使用 Gunicorn 部署到生产环境
+ 开放到公网，配置防火墙等
+ 如果需要，可以使用 `systemd` 将 Gunicorn 配置为服务，确保 Flask 应用在重启后自动启动。

这样，你就可以在没有 Nginx 反向代理的情况下成功部署 Flask 网站了。

