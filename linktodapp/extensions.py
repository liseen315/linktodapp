from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension
from flask_whooshee import Whooshee
from flask_wtf.csrf import CSRFProtect
from flask_babel import Babel,lazy_gettext as _l


db = SQLAlchemy()
toolbar = DebugToolbarExtension()
migrate = Migrate()
whooshee = Whooshee()
csrf = CSRFProtect()
babel = Babel()
