from CNPM.models import ChuyenBay, TuyenBay, User, SanBay, ThoiDiemBay, MayBay, HangVe, Ve, KhachHang, ChuyenBayCoSanBayTrungGian, MayBayThuocChuyenBay, UserRole
from CNPM import db, app, dao
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask import redirect, request, session
from wtforms import TextAreaField
from wtforms.widgets import TextArea
from datetime import datetime
import json


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


class StatsView(BaseView):
    @expose('/')
    def index(self):
        year = request.args.get('so_lieu', "all")
        loai_thoi_gian = request.args.get('thoi_gian', "1")
        so_lieu_year = request.args.get('so_lieu_year', 12)
        #stats = dao.tuyen_bay_count_stats(year=year)
        stats = dao.tuyen_bay_month_doanh_thu_stats(year=year, so_lieu_year=so_lieu_year, loai_thoi_gian=loai_thoi_gian)
        stats1 = []
        for s in stats:
            stats2 = {
                "id": s[0],
                "name": s[1],
                "price": s[2],
                "so_luot_bay": s[3],
                "tong_doanh_thu": s[4],
                "ty_le": 100 * (s[2] / s[4])
            }
            stats1.append(stats2)
        json_object = json.dumps(stats1)
        with open("data/sample.json", "w", encoding='utf-8') as outfile:
            outfile.write(json_object)
        return self.render('admin/stats.html', stats=stats)
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


admin = Admin(app=app, name='QUẢN LÝ CHUYẾN BAY', template_mode='bootstrap4')
admin.add_view(AuthenticatedModalViewAdmin(User, db.session, name='Người dùng'))
admin.add_view(AuthenticatedModalViewAdmin(SanBay, db.session, name='Sân bay'))
admin.add_view(AuthenticatedModalView(KhachHang, db.session, name='Khách hàng'))
admin.add_view(AuthenticatedModalViewAdmin(ThoiDiemBay, db.session, name='Thời điểm bay'))
admin.add_view(AuthenticatedModalViewAdmin(MayBay, db.session, name='Máy bay'))
admin.add_view(AuthenticatedModalView(ChuyenBay, db.session, name='Chuyến bay'))
admin.add_view(AuthenticatedModalViewAdmin(TuyenBay, db.session, name='Tuyến bay'))
admin.add_view(AuthenticatedModalView(HangVe, db.session, name='Hạng vé'))
admin.add_view(AuthenticatedModalView(Ve, db.session, name='Vé'))

admin.add_view(StatsView(name="Báo cáo thống kê"))
admin.add_view(LogoutView(name="Đăng xuất"))
# admin.add_view(ModelView(ChuyenBayCoSanBayTrungGian, db.session))
# admin.add_view(ModelView(MayBayThuocChuyenBay, db.session))


# class StatsView(BaseView):
#     @expose('/')
#     def index(self):
#         return self.render('admin/stats.html')
