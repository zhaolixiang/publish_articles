python版本：3.7

# 记得运行程序前，如果数据库还没有创建指定表，先执行下面语句创建：
```angular2
# 初始化
flask db init
flask db migrate -m "--update--"
# 更新数据库
flask db upgrade
```

### 1、前端页面在templates文件夹下的html文件

### 2、部署的时候不要跨域部署，富文本框架不支持跨域图片上传

### 3、在/templates/html/config.js文件进行相关配置