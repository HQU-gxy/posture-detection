# -*- coding:utf-8 -*-
import datetime
import decimal
import uuid

# https://stackoverflow.com/questions/76107450/flask-attributeerror-module-flask-json-has-no-attribute-jsonencoder/76325779#76325779
try:
  from flask.json import JSONEncoder as _JSONEncoder
except ImportError:
  from json import JSONEncoder as _JSONEncoder


class MyJSONEncoder(_JSONEncoder):

  def default(self, o):
    if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
      return dict(o)
    if isinstance(o, datetime.datetime):
      # 格式化时间
      return o.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(o, datetime.date):
      # 格式化日期
      return o.strftime('%Y-%m-%d')
    if isinstance(o, decimal.Decimal):
      # 格式化高精度数字
      return str(o)
    if isinstance(o, uuid.UUID):
      # 格式化uuid
      return str(o)
    if isinstance(o, bytes):
      # 格式化字节数据
      return o.decode("utf-8")
