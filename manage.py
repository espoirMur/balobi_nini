import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db
from app.config import app_config
from app.model import CleannedTweet

config_name = app_config.get(os.environ.get('APP_SETTINGS'))
app.config.from_object(config_name)
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
