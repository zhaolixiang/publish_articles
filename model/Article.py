from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, length

from model.db import db, MyModel


class Article(db.Model, MyModel):
    __tablename__ = 'article'
    # 主键
    oId = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(255))
    # 文章标题
    title = db.Column(db.String(255))
    # 文章正文
    content = db.Column(db.Text())
    # 文章创建时间戳
    create_time = db.Column(db.DateTime())
    # 标签
    label=db.Column(db.String())


class ArticleForm(FlaskForm):
    # 文章标题
    title = StringField('文章标题', validators=[DataRequired(message='标题不能为空'), length(max=255)])
    # 标签
    label = StringField('标签')
    img = StringField('封面')
    content = StringField('正文')
    submit = SubmitField('提交')
