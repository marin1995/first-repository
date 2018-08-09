from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from zhiliao import app
from exts import db
from models import *

#1,初始化app
manager = Manager(app)

#2,将app和db绑定到flask_migrate上
migrate = Migrate(app,db)

#3将migratecommand添加到主命令中
manager.add_command("db",MigrateCommand)

if __name__ == "__main__":
    manager.run()
