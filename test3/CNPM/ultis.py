import json, os
from CNPM.models import ChuyenBay, TuyenBay, User, SanBay, ThoiDiemBay, MayBay, HangVe, Ve, KhachHang, \
    ChuyenBayCoSanBayTrungGian, MayBayThuocChuyenBay, UserRole
from flask_login import current_user
from CNPM import db, app


def read_json(path):
    with open(path, "r") as f:
        return json.load(f)


def load_chuyen_bay():
    return ChuyenBay.query.all()


def load_product():
    return read_json(os.path.join(app.root_path, 'data/products.json'))


def chuyentuyenve(tuyen):
    di = ''
    den = ''
    return {
        'di': di,
        'den': den
    }
