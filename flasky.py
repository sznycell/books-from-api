import os
from app import create_app, db
from flask_migrate import Migrate, upgrade
from app.models import Volumes


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Volumes=Volumes)


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    
    
@app.cli.command()
def deploy():
    """Run deployment tasks."""
    Volumes.create_table()
