from app import app, create_app, db
from app.home.models import Group, Project, Run, Process
from app.base.models import Settings
db.init_app(app)
app.app_context().push()

Run.query.with_entities(Run.status).all()
