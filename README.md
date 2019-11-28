# 发布文章

pipenv shell

# 初始化
flask db init

flask db migrate -m "--update--"

# 更新数据库
flask db upgrade