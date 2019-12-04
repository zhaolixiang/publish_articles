import datetime
import os
import re
from flask_migrate import Migrate
from flask import Flask, make_response, json, request, jsonify

from tools.UploadToWeb import go_upload
from model.Article import Article
from model.db import db
from tools.ForString import isNull
from tools.uploader import Uploader
from flask_cors import *  # 导入模块

app = Flask(__name__)
CORS(app, supports_credentials=True)  # 设置跨域
app.secret_key = 'asjajskgjkagfjkadsgfjkagf'
# json支持中文显示
app.config['JSON_AS_ASCII'] = False
file_path = os.path.abspath(os.getcwd()) + "/article.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)


def convert_to_dict(obj):
    '''把Object对象转换成Dict对象'''
    dict = {}
    dict.update(obj.__dict__)
    dict = {key: str(dict[key]) for key in dict.keys()}
    return dict


@app.route('/')
def index():
    return "只是接口，请访问静态页面：templates->html->upload_article.html"


@app.route('/api/all_article', methods=['get', 'post'])
def api_all_article():
    articles = Article.query.order_by(Article.oId.desc()).all()
    articles = [convert_to_dict(article) for article in articles]
    return jsonify(data=articles)


@app.route('/api/detail_article/<int:id>', methods=['get', 'post'])
def api_detail_article(id):
    article = Article.query.get(id)
    return jsonify(data=convert_to_dict(article))


@app.route('/upload_article', methods=['POST'])
def upload_article():
    img = request.values.get('img', '')
    print("获取到的图片", img)
    if isNull(img):
        return jsonify(success=False, msg='请选择封面')
    title = request.form.get('title', '')
    if isNull(title):
        return jsonify(success=False, msg='请填写标题')
    label = request.form.get('label', '')
    content = request.form.get('content', '')
    if isNull(content):
        return jsonify(success=False, msg='请填写正文')

    article = Article()
    print("提交数据了", article)
    article.title = title
    article.content = content
    article.img = img
    article.label = label
    article.create_time = datetime.datetime.now()
    article.save()
    return jsonify(success=True)


@app.route('/upload/', methods=['GET', 'POST', 'OPTIONS'])
def upload():
    """UEditor文件上传接口

    config 配置文件
    result 返回结果
    """
    mimetype = 'application/json'
    result = {}
    action = request.args.get('action')

    # 解析JSON格式的配置文件
    with open(os.path.join(app.static_folder,
                           'config.json')) as fp:
        try:
            # 删除 `/**/` 之间的注释
            CONFIG = json.loads(re.sub(r'\/\*.*\*\/', '', fp.read()))
        except:
            CONFIG = {}

    if action == 'config':
        # 初始化时，返回配置文件给客户端
        result = CONFIG

    elif action in ('uploadimage'):
        # 图片、文件、视频上传
        fieldName = CONFIG.get('imageFieldName')
        config = {
            "pathFormat": CONFIG['imagePathFormat'],
            "maxSize": CONFIG['imageMaxSize'],
            "allowFiles": CONFIG['imageAllowFiles']
        }
        if fieldName in request.files:
            field = request.files[fieldName]
            uploader = Uploader(field, config, app.static_folder)
            result = uploader.getFileInfo()
        else:
            result['state'] = '上传接口出错'

    else:
        result['state'] = '不支持此上传'

    if result.get('filePath', None):
        web_result = go_upload(result.get('filePath'))
        result['url'] = web_result.get('data').get('img_url')
    result['filePath'] = result.get('url', '')

    result = json.dumps(result)
    print("是", result)

    if 'callback' in request.args:
        callback = request.args.get('callback')
        if re.match(r'^[\w_]+$', callback):
            result = '%s(%s)' % (callback, result)
            mimetype = 'application/javascript'
        else:
            result = json.dumps({'state': 'callback参数不合法'})

    print(result)
    print("mimetype", mimetype)
    result = "<html><head><script>document.domain='http://0.0.0.0:4001/'</script></head><body>" + result + "</body></html>"
    res = make_response(result)
    res.mimetype = mimetype
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Headers'] = 'X-Requested-With,X_Requested_With'
    return res


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4001)
