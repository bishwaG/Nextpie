## Admin view
from flask_admin.base import AdminIndexView
from flask_login import current_user
from flask_admin.base import expose

# Extend the AdminIndexView
class MyHomeView(AdminIndexView):
	@expose('/')
	def index(self):
		arg1 = 'Hello'
		return self.render('admin/main.html', arg1=arg1)
		
	def is_accessible(self):
		# only accessible if admin field is True
		if current_user.is_authenticated and current_user.super_user:
			return True

		return False
		
	def inaccessible_callback(self, name):
		#return redirect(url_for('base_blueprint.login', redirect=request.url))
		return redirect(url_for('base_blueprint.login'))
