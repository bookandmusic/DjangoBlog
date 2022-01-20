# DjangoBlog

🌍 *English ∙ 简体中文*

基于`python3.7`和`Django2.2`的博客。

## 主要功能：

-   文章，页面，教程，归档，标签的添加，删除，编辑等。
-   文章及页面支持`Markdown`，支持代码高亮，支持目录点击跳转。
-   支持文章全文搜索。
-   侧边栏功能，最新文章，归档，标签云等。
-   集成了简单的图床功能。

## 安装

依赖环境，使用pip安装： `pip install -Ur requirements.txt`

如果你没有pip，使用如下方式安装：

-   OS X / Linux 电脑，终端下执行:

    ```
    curl http://peak.telecommunity.com/dist/ez_setup.py | python
    curl https://bootstrap.pypa.io/get-pip.py | python
    ```

-   Windows电脑：

    下载 http://peak.telecommunity.com/dist/ez_setup.py 和 https://raw.github.com/pypa/pip/master/contrib/get-pip.py 这两个文件，双击运行。

## 运行

修改`DjangoBlog/setting.py` 修改数据库配置，如下所示：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'DjangoBlog',
        'HOST': 'localhost',
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': 'password',
        'OPTIONS': {
            "charset": "utf8mb4"
        }
    }
}
```

### 创建数据库

mysql数据库中执行:

```sql
create database DjangoBlog  charset=utf8mb4;
```

然后终端下执行:

```shell
./manage.py makemigrations
./manage.py migrate
```

**注意：** 在使用 `./manage.py` 之前需要确定你系统中的 `python` 命令是指向 `python 3.6` 及以上版本的。如果不是如此，请使用以下两种方式中的一种：

-   修改 `manage.py` 第一行 `#!/usr/bin/env python` 为 `#!/usr/bin/env python3`
-   直接使用 `python3 ./manage.py makemigrations`

### 创建超级用户

终端下执行:

```shell
./manage.py createsuperuser
```

### 收集静态文件

终端下执行:  

```shell
./manage.py collectstatic --noinput
```

### 生成索引文件

终端下执行:  

```shell
./manage.py rebuild_index
```

### 开始运行：

执行： `./manage.py runserver`

浏览器打开: http://127.0.0.1:8000/ 就可以看到效果了。

