# -*- coding: utf-8 -*-
import datetime
import json

from bson import ObjectId
from flask import jsonify, g, make_response



def json_default(value):
    if isinstance(value, datetime.date):
        # return dict(year=value.year, month=value.month, day=value.day)
        result= value.strftime('%Y-%m-%d %H:%M')
        # result = str(value.year) + "-" + str(value.month) + "-" + str(value.day)
        return result
    elif isinstance(value,ObjectId):
        #对于ObjectId处理
        return str(value)
    else:
        return value.__dict__

def convert_to_dict(obj):
    '''把Object对象转换成Dict对象'''
    dict = {}
    dict.update(obj.__dict__)
    dict={key:str(dict[key]) for key in dict.keys()}
    return dict


class ResultJson(object):
    def __init__(self, data="", success=True, total=0,
                 pageSize=0, msg=None, page="0",*args, **kargs):
        self.success = success
        self.data = data
        self.total = total
        self.pageSize = pageSize
        if not msg:
            self.msg="成功"
        else:
            self.msg = msg

        self.page = page
        for k in kargs:
            setattr(self,k,kargs[k])

    def __str__(self):
        """lambda obj: obj.__dict__          会将任意的对象，转换成字典的方式
        sort_keys=True                    会按照字典中的键来按照ASCII方式来排序
        indent=4                          会按照键值对以间隔4来直观的显示"""
        return json.dumps(self, default=json_default, ensure_ascii=False)
    
    def toJson(self,test=False):
        print(json.loads(str(self)))
        response=make_response(json.dumps(self,default=json_default,ensure_ascii=False))
        response.mimetype='application/json'
        return response
        # if test:
        #     xxx = json.loads(str(self))
        #     g.logger.debug('返回数据xxx'+str(self))
        #     return xxx
        # else:
        #     xxx = jsonify(json.loads(str(self)))
        #     g.logger.debug('返回数据xxx'+str(self))
        #     return xxx

