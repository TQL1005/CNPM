from CNPM.models import ChuyenBay, TuyenBay, User, SanBay, ThoiDiemBay, MayBay, HangVe, Ve, KhachHang
from CNPM import db, app, admin
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from wtforms import TextAreaField
from wtforms.widgets import TextArea


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(SanBay, db.session))
admin.add_view(ModelView(KhachHang, db.session))
admin.add_view(ModelView(ThoiDiemBay, db.session))
admin.add_view(ModelView(MayBay, db.session))
admin.add_view(ModelView(ChuyenBay, db.session))
admin.add_view(ModelView(TuyenBay, db.session))
admin.add_view(ModelView(HangVe, db.session))
admin.add_view(ModelView(Ve, db.session))


class StatsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')
