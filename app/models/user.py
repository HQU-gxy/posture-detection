from datetime import datetime

import sqlalchemy
from sqlalchemy import Column, Integer, String, DateTime, BigInteger
from sqlalchemy.exc import IntegrityError, NoResultFound
from werkzeug.security import generate_password_hash
from .base import Base, db
from app.exception import ResultError


class User(Base):
  __tablename__ = 'user'
  __table_args__ = {'comment': '用户表'}
  id = Column(BigInteger, primary_key=True, comment='主键')
  create_time = Column(DateTime, default=datetime.now(), comment='创建时间')
  name = Column(String(50), nullable=True, comment='用户姓名')
  username = Column(String(255), unique=True, nullable=True, comment='账号名')
  password = Column(String(300), nullable=True, comment='密码')
  role_id = Column(String(50), comment='角色ID,(admin)')
  age = Column(Integer, comment='用户年龄')


  def serialize(self, to_camel=True):
    s = super().serialize()
    del s['password']
    if to_camel:
      s = self.to_camel(s)
    return s

  @classmethod
  def get_by_username(cls, username):
    try:
      user = cls.query.filter_by(username=username).one()
      return user
    except NoResultFound:
      return None

  @classmethod
  def update(cls, data: dict, key='userId', err_msg='未找到用户'):
    super().update(data, key, err_msg)

  @classmethod
  def delete(cls, model_id, err_msg='未找到用户'):
    super().delete(model_id, err_msg)
