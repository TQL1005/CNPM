from CNPM.models import ChuyenBay, TuyenBay, User, SanBay, ThoiDiemBay, MayBay, HangVe, Ve, KhachHang, ChuyenBayCoSanBayTrungGian, MayBayThuocChuyenBay, UserRole
from CNPM import db, app, admin
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask import redirect
from wtforms import TextAreaField
from wtforms.widgets import TextArea


class AuthenticatedModalView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class AuthenticatedModalViewNV(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class AuthenticatedBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class LogoutView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')



admin.add_view(AuthenticatedModalView(User, db.session, name='Người dùng'))
admin.add_view(AuthenticatedModalView(SanBay, db.session, name='Sân bay'))
admin.add_view(AuthenticatedModalViewNV(KhachHang, db.session, name='Khách hàng'))
admin.add_view(AuthenticatedModalView(ThoiDiemBay, db.session, name='Thời điểm bay'))
admin.add_view(AuthenticatedModalView(MayBay, db.session, name='Máy bay'))
admin.add_view(AuthenticatedModalViewNV(ChuyenBay, db.session, name='Chuyến bay'))
admin.add_view(AuthenticatedModalViewNV(TuyenBay, db.session, name='Tuyến bay'))
admin.add_view(AuthenticatedModalViewNV(HangVe, db.session, name='Hạng vé'))
admin.add_view(AuthenticatedModalViewNV(Ve, db.session, name='Vé'))
admin.add_view(LogoutView(name="Đăng xuất"))
# admin.add_view(ModelView(ChuyenBayCoSanBayTrungGian, db.session))
# admin.add_view(ModelView(MayBayThuocChuyenBay, db.session))


class StatsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')
