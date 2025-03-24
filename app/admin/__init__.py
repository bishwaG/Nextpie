from flask import Blueprint

from flask import Flask, redirect, request, url_for, render_template
from flask_admin import Admin
from app import app, db
from app.base.models import User
from app.home.models import Group, Project, Run, Process
from flask_admin.contrib.sqla import ModelView

from app.admin.models import MyModelAdminUser, MyModelAdminGroup, MyModelAdminProject, MyModelAdminRun, MyModelAdminProcess

from app.admin.models import DashboardView

from flask_admin.menu import MenuLink

## admin views
from app.admin.adminviews import MyHomeView
## Flask-admin
admin = Admin(app, 
              name='Admin Dashboard', 
              template_mode='bootstrap3', 
              index_view=MyHomeView( name="Home", template='admin/index.html', url="/admin")
              )

## add DB tabel views
admin.add_view(MyModelAdminUser(User, db.session))
admin.add_view(MyModelAdminGroup(Group, db.session))

admin.add_view(MyModelAdminProject(Project, db.session))
admin.add_view(MyModelAdminRun(Run, db.session))
admin.add_view(MyModelAdminProcess(Process, db.session))
admin.add_link(MenuLink(name='Logout', url='/logout'))

blueprint = Blueprint(
    'admin_blueprint',
    __name__,
    url_prefix='/admin',
    template_folder='templates',
    static_folder='static'
)

