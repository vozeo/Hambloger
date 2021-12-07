import os
from app import create_app, db
from app.models import User, Role
from flask_migrate import Migrate

app = create_app(os.getenv('HAMBLOGER_CONFIG') or 'default')
migrate = Migrate(app, db)

#添加一个shell上下文，使得shell可以自动导入对象
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

@app.cli.command()
def test():
    """Run the unit test."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)