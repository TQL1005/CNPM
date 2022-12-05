from CNPM.models import ChuyenBay
from CNPM import db, app
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from wtforms import TextAreaField
from wtforms.widgets import TextArea

class StatsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')
