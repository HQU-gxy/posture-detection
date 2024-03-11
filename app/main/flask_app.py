import logging
import traceback

from flasgger import Swagger
from flask import Flask, jsonify, request
from flask_cors import CORS
import flask_excel as excel
from threading import Thread
from anyio import run

from app.exception import ResultError
from app.models import Result
from app.utils import ColoredLevelFormatter, NoANSIFormatter, MyJSONEncoder
from app.models.base import db
from app.api.user import api as user_api
from app.api.auth import bp as auth_bp
from app.api.video import api as video_api

# start_listen_serial 必须在 导入models后才能导入

logger = logging.getLogger(__name__)


# TODO: why don't you use a logging library?
def setup_logging():
  logging.basicConfig(level=logging.INFO)
  # console logger
  formatter = ColoredLevelFormatter(
      "\033[38;2;187;187;187m%(asctime)s\033[0m "
      "%(levelname)s "
      "\033[36m%(name)s\033[0m"
      "\033[38;2;187;187;187m: %(message)s\033[0m")
  console_handler = logging.StreamHandler()
  console_handler.setFormatter(fmt=formatter)

  # file logger
  file_formatter = NoANSIFormatter(
      "%(asctime)s %(levelname)s %(name)s %(message)s")
  log_folder = 'log'
  import os
  os.makedirs(f'{log_folder}/info', exist_ok=True)
  os.makedirs(f'{log_folder}/error', exist_ok=True)
  from logging.handlers import TimedRotatingFileHandler
  file_info_handler = TimedRotatingFileHandler(filename='./log/info/shoot.log',
                                               encoding='utf-8',
                                               interval=1,
                                               when='midnight',
                                               backupCount=7)
  file_info_handler.setLevel('INFO')
  file_info_handler.setFormatter(fmt=file_formatter)
  file_info_handler.flushTime = 5.0  # type: ignore
  file_info_handler.suffix = '%Y-%m-%d.log'

  file_error_handler = TimedRotatingFileHandler(
      filename='./log/error/shoot.log',
      encoding='utf-8',
      interval=1,
      when='midnight',
      backupCount=7)
  file_error_handler.setLevel('ERROR')

  file_error_handler.setFormatter(fmt=file_formatter)
  file_error_handler.flushTime = 5.0  # type: ignore
  file_error_handler.suffix = '%Y-%m-%d.log'

  logging.getLogger('').handlers.clear()
  logging.getLogger('').addHandler(file_info_handler)
  logging.getLogger('').addHandler(file_error_handler)
  logging.getLogger('').addHandler(console_handler)

  # fix: sqlalchemy log print twice.
  handler = logging.StreamHandler()
  handler.setLevel(logging.CRITICAL)
  logging.getLogger('sqlalchemy.engine.Engine').addHandler(handler)

  # auth_dir(log_folder)


def auth_dir(dir: str):
  import os
  import stat
  for root, dirs, files in os.walk(dir):
    for file in files:
      file_path = os.path.join(root, file)

      # 修改文件权限为所有用户可读可写
      os.chmod(
          file_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP |
          stat.S_IROTH | stat.S_IWOTH)


def create_app(test_config=None):
  app = Flask(__name__)

  excel.init_excel(app)

  Swagger(app=app, template_file='../doc/final.yml')

  CORS(app,
       resources={
           r'/*': {
               'supports_credentials': True,
               'expose_headers': ["Content-Disposition", "hide-msg"]
           }
       })

  setup_logging()

  def run_async():
    """
        blocking run async_main, this function should be called either in main thread or in a new thread
        """

  task = Thread(target=run_async, daemon=True)
  task.start()

  app.json_encoder = MyJSONEncoder

  app.config.from_mapping(
      SECRET_KEY='dev',
      SQLALCHEMY_DATABASE_URI=
      'mysql+pymysql://root:root@127.0.0.1:3306/posture_detection?charset=utf8',
      SQLALCHEMY_POOL_RECYCLE=1800,
      SQLALCHEMY_POOL_TIMEOUT=1500,
      SQLALCHEMY_ENGINE_OPTIONS={'pool_pre_ping': True},
      SQLALCHEMY_ECHO=True,
  )

  # error handlers

  @app.errorhandler(404)
  def handle_not_found(e):
    response = jsonify({'error': 'Not found'})
    response.status_code = 404
    return response

  @app.errorhandler(405)
  def handle_method_not_allowed(e):
    response = jsonify({'error': '405'})
    response.status_code = 405
    return response

  @app.errorhandler(400)
  def handle_bad_request(e):
    app.logger.error(
        f'Request to {request.path} failed with error: {"{}".format(e)}\n')
    return jsonify(Result.fail(msg='非法参数'))

  @app.errorhandler(Exception)
  def handle_runtime_error(e):
    app.logger.error(f'{"{}".format(e)}\n{traceback.format_exc()}')
    return jsonify(Result.fail(msg='未知异常'))

  @app.errorhandler(ResultError)
  def handle_result_error(e: ResultError):
    return jsonify(Result.fail_with_error(e))

  # db
  db.init_app(app)
  with app.app_context():
    db.create_all()

  # router
  app.register_blueprint(user_api)
  app.register_blueprint(auth_bp)
  app.register_blueprint(video_api)

  return app

app = create_app()
