from flask_migrate import Migrate

from app.main.flask_app import app
from app.models.base import db

migrate = Migrate(app=app, db=db)

if __name__ == '__main__':
  app.run()
