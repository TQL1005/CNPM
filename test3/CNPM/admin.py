from CNPM.models import ChuyenBay, TuyenBay, User, SanBay, ThoiDiemBay, MayBay, HangVe, Ve, KhachHang, ChuyenBayCoSanBayTrungGian, MayBayThuocChuyenBay, UserRole
from CNPM import db, app, admin
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask import redirect
from wtforms import TextAreaField
from wtforms.widgets import TextArea


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class AuthenticatedModalView(ModelView):
    column_searchable_list = ['name']
    column_filters = ['name']
    can_view_details = True
    can_export = True
    column_exclude_list = ['image']
    column_labels = {
        'name': 'Name'
    }
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'description': CKTextAreaField
    }
    def is_accessible(self):
        return current_user.is_authenticated


class AuthenticatedModalViewAdmin(AuthenticatedModalView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class AuthenticatedBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class LogoutView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')



admin.add_view(AuthenticatedModalViewAdmin(User, db.session, name='Người dùng'))
admin.add_view(AuthenticatedModalViewAdmin(SanBay, db.session, name='Sân bay'))
admin.add_view(AuthenticatedModalView(KhachHang, db.session, name='Khách hàng'))
admin.add_view(AuthenticatedModalViewAdmin(ThoiDiemBay, db.session, name='Thời điểm bay'))
admin.add_view(AuthenticatedModalViewAdmin(MayBay, db.session, name='Máy bay'))
admin.add_view(AuthenticatedModalViewAdmin(ChuyenBay, db.session, name='Chuyến bay'))
admin.add_view(AuthenticatedModalView(TuyenBay, db.session, name='Tuyến bay'))
admin.add_view(AuthenticatedModalView(HangVe, db.session, name='Hạng vé'))
admin.add_view(AuthenticatedModalView(Ve, db.session, name='Vé'))

admin.add_view(LogoutView(name="Đăng xuất"))
# admin.add_view(ModelView(ChuyenBayCoSanBayTrungGian, db.session))
# admin.add_view(ModelView(MayBayThuocChuyenBay, db.session))


class StatsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')
