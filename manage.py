from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app
from exts import db
from models import User, Comments, Life, Characters, Hobby

manager     =   Manager(app)
migtate     =   Migrate(app, db)#使用Migrate绑定app和db
manager.add_command('db', MigrateCommand)#添加迁移脚本命令到manager中

if __name__ == '__main__':
    manager.run()