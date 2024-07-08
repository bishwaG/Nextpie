from app import app, create_app, db
from app.home.models import Group, Project, Run, Process
from app.base.models import Settings
db.init_app(app)
app.app_context().push()

from app.home.utils import Utils

x = Utils.parseTraceFiles(["test-group-name", "test_proj_name", "test-pipeline", "0.0.1"],"assets/example-workflow/test-runs/results/pipeline_info/Trace.txt","CLI")
print()
