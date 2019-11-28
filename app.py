import datetime
import os
import re
from flask_migrate import Migrate
from flask import Flask, redirect, url_for, render_template, make_response, json, request, jsonify

from UploadToWeb import go_upload
from model.Article import ArticleForm, Article
from model.db import db
from tools.ForString import isNotNull, isNull
from uploader import Uploader

app = Flask(__name__)
app.secret_key = 'asjajskgjkagfjkadsgfjkagf'
# json支持中文显示
app.config['JSON_AS_ASCII'] = False
file_path = os.path.abspath(os.getcwd())+"/article.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return redirect(url_for('add_article'))

@app.route('/detail_article<int:id>', methods=['get', 'post'])
def detail_article(id):
    article = Article.query.get(id)
    return render_template('article_detail.html', article=article)

@app.route('/all_article', methods=['get', 'post'])
def all_article():
    articles=Article.query.order_by(Article.oId.desc())
    return render_template('article_all.html', articles=articles)

@app.route('/delete_article/<int:id>', methods=['get', 'post'])
def delete_article(id):
    article = Article.query.get(id)
    article.delete()
    article.save()
    return redirect(url_for('all_article'))

@app.route('/add_article', methods=['get'])
def add_article():
    form = ArticleForm()
    return render_template('article_add.html', form=form)

@app.route('/upload_article', methods=['POST'])
def upload_article():
    img=request.values.get('img','')
    print("获取到的图片",img)
    if isNull(img):
        return jsonify(success=False,msg='请选择封面')
    title = request.form.get('title', '')
    if isNull(title):
        return jsonify(success=False, msg='请填写标题')
    label = request.form.get('label', '')
    content = request.form.get('content', '')
    if isNull(content):
        return jsonify(success=False, msg='请填写正文')

    article = Article()
    print("提交数据了", article)
    article.title =title
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

    if result.get('filePath',None):
        web_result = go_upload(result.get('filePath'))
        result['url'] = web_result.get('data').get('img_url')




    result = json.dumps(result)
    print("是",result)

    if 'callback' in request.args:
        callback = request.args.get('callback')
        if re.match(r'^[\w_]+$', callback):
            result = '%s(%s)' % (callback, result)
            mimetype = 'application/javascript'
        else:
            result = json.dumps({'state': 'callback参数不合法'})

    print(result)
    print("mimetype",mimetype)
    res = make_response(result)
    res.mimetype = mimetype
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Headers'] = 'X-Requested-With,X_Requested_With'
    return res

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=4001)
