from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose
from app import app, db
from app.models import ChuyenBay, TuyenBay, SanBay, UserRole
from flask_login import logout_user, current_user
from flask import redirect

admin = Admin(app=app, name='QUẢN TRỊ CHUYẾN BAY', template_mode='bootstrap4')

class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

class MyFlightView(ModelView):
    column_list = ['id', 'tenCB', 'ngayBay', 'thoiGianBay']
    column_searchable_list = ['tenCB']
    column_filters = ['ngayBay', 'tenCB']
    can_export = True
    edit_modal = True
    column_labels = {
        'id': 'Danh mục',
        'tenCB': 'Tên chuyến bay',
        'ngayBay': 'Ngày Bay',
        'thoiGianBay': 'Thời gian bay'
    }



class MyRouteView(ModelView):
    column_list = ['id', 'tenTB', 'chuyen_bay']
    column_labels = {
        'id': 'Danh mục',
        'tenTB': 'Tên tuyến bay',
        'chuyen_bay': 'Chuyến bay'
    }

class MyAirpotView(ModelView):
    column_list = ['id','tenSB']
    column_labels = {
        'id': 'Danh mục',
        'tenSB': 'Tên sân bay'
    }
class StatsView(BaseView):
    @expose("/")
    def index(self):
        return self.render('admin/stats.html')


class LogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect("/")


admin.add_view(MyRouteView(TuyenBay, db.session))
admin.add_view(MyFlightView(ChuyenBay, db.session))
admin.add_view(MyAirpotView(SanBay, db.session))
admin.add_view(StatsView(name='Thống kê doanh thu'))
admin.add_view(LogoutView(name='Đăng Xuất'))