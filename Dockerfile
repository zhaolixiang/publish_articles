FROM oldmark/p37

EXPOSE 4001
ADD . /publish_articles
RUN pip install -r /publish_articles/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

