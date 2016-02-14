#!/usr/bin/env python
import os

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from base import app, db
app.config.from_object("config.prod")

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
