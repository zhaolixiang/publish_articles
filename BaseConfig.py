import os


class BaseConfig(object):
    #
    webUrl = "http://news.handsomemark.com/"
    # 程序的密钥
    SECRET_KEY = 'asjajskgjkagfjkadsgfjkagf'
    # json中文正常显示
    JSON_AS_ASCII = False
    # 配置sqlite的路径
    # 默认是当前项目下的article.db
    # 要改成项目外的路径，可以这样设置：
    # file_path ="/a/b/c/x.db"
    file_path = os.path.abspath(os.getcwd()) + "/article.db"
    if os.path.exists('/home/deploy/project/sqlite'):
        file_path = os.path.join('/home/deploy/project/sqlite', 'article.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + file_path
    SQLALCHEMY_TRACK_MODIFICATIONS = False
