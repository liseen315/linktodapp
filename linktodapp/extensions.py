from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension
from flask_whooshee import Whooshee


db = SQLAlchemy()
toolbar = DebugToolbarExtension()
migrate = Migrate()
whooshee = Whooshee()
