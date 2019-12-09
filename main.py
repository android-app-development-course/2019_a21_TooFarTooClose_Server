from flask import Flask

from config.conf import *
from controllers.courseController import course

app = Flask(__name__)
# 注册蓝图
app.register_blueprint(blueprint=course, url_prefix='/course')


if __name__ == '__main__':
    app.run(host=HTTP_HOST, port=HTTP_PORT)
