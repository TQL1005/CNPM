import datetime
import decimal

from CNPM.models import ChuyenBay, TuyenBay, User, SanBay, ThoiDiemBay, MayBay, HangVe, Ve, KhachHang, \
    ChuyenBayCoSanBayTrungGian, MayBayThuocChuyenBay, UserRole
from flask_login import current_user
from sqlalchemy import func  # chua ham tinh tong,... trong sql
from CNPM import db, app
from sqlalchemy.sql import extract
import hashlib
import datetime as dt


def load_san_bay():
    return SanBay.query.all()


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()), User.password.__eq__(password)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


# def tuyen_bay_count_stats(year):
#     return db.session.query(TuyenBay.id, TuyenBay.name, func.count(ChuyenBay.id))\
#              .join(ChuyenBay, ChuyenBay.tuyenBay_id.__eq__(TuyenBay.id))\
#              .filter(extract('year', ChuyenBay.created_date) == year).group_by(TuyenBay.id).all()


def tuyen_bay_month_doanh_thu_stats(year, so_lieu_year, loai_thoi_gian):
    if year == "all" and loai_thoi_gian == "1":
        doanh_thu_tung_dot = db.session.query(TuyenBay.id, TuyenBay.name, func.sum(HangVe.price),
                                             func.count(ChuyenBay.id)).join(ChuyenBay, ChuyenBay.tuyenBay_id.__eq__(
            TuyenBay.id)).join(Ve, Ve.chuyenBay_id.__eq__(ChuyenBay.id)).join(HangVe,
                                                                              HangVe.id.__eq__(Ve.hangVe_id)).group_by(
            TuyenBay.id).all()
        tong_doanh_thu = decimal.Decimal('0')
        for doanh_thu in doanh_thu_tung_dot:
            tong_doanh_thu += decimal.Decimal(doanh_thu[2])

        # import pdb;
        # pdb.set_trace()

        return db.session.query(TuyenBay.id, TuyenBay.name, func.sum(HangVe.price),
                                func.count(ChuyenBay.id), tong_doanh_thu).join(ChuyenBay, ChuyenBay.tuyenBay_id.__eq__(
            TuyenBay.id)).join(Ve, Ve.chuyenBay_id.__eq__(ChuyenBay.id)).join(HangVe,
                                                                              HangVe.id.__eq__(Ve.hangVe_id)).group_by(
            TuyenBay.id).order_by(TuyenBay.id).all()
    if loai_thoi_gian == "1":
        doanh_thu_tung_dot = db.session.query(TuyenBay.id, TuyenBay.name, func.sum(HangVe.price),
                                              func.count(ChuyenBay.id)).join(ChuyenBay, ChuyenBay.tuyenBay_id.__eq__(
            TuyenBay.id)).join(Ve, Ve.chuyenBay_id.__eq__(ChuyenBay.id)).join(HangVe, HangVe.id.__eq__(Ve.hangVe_id)).filter(
            extract('year', ChuyenBay.created_date) == year).group_by(TuyenBay.id).all()
        tong_doanh_thu = decimal.Decimal('0')
        for doanh_thu in doanh_thu_tung_dot:
            tong_doanh_thu += decimal.Decimal(doanh_thu[2])

        # import pdb;
        # pdb.set_trace()


        return db.session.query(TuyenBay.id, TuyenBay.name, func.sum(HangVe.price),
                                              func.count(ChuyenBay.id), tong_doanh_thu).join(ChuyenBay, ChuyenBay.tuyenBay_id.__eq__(
            TuyenBay.id)).join(Ve, Ve.chuyenBay_id.__eq__(ChuyenBay.id)).join(HangVe, HangVe.id.__eq__(Ve.hangVe_id)).filter(
            extract('year', ChuyenBay.created_date) == year).group_by(TuyenBay.id).order_by(TuyenBay.id).all()

    elif loai_thoi_gian == "2":
        if year == "all":
            doanh_thu_tung_dot = db.session.query(TuyenBay.id, TuyenBay.name, func.sum(HangVe.price),
                                                  func.count(ChuyenBay.id)).join(ChuyenBay,
                                                                                 ChuyenBay.tuyenBay_id.__eq__(
                                                                                     TuyenBay.id)).join(Ve,
                                                                                                        Ve.chuyenBay_id.__eq__(
                                                                                                            ChuyenBay.id)).join(
                HangVe,
                HangVe.id.__eq__(Ve.hangVe_id)).filter(
                extract('month', ChuyenBay.created_date) == so_lieu_year).group_by(TuyenBay.id).all()
            tong_doanh_thu = decimal.Decimal('0')
            for doanh_thu in doanh_thu_tung_dot:
                tong_doanh_thu += decimal.Decimal(doanh_thu[2])

            # import pdb;
            # pdb.set_trace()

            return db.session.query(TuyenBay.id, TuyenBay.name, func.sum(HangVe.price),
                                    func.count(ChuyenBay.id), tong_doanh_thu).join(ChuyenBay,
                                                                                   ChuyenBay.tuyenBay_id.__eq__(
                                                                                       TuyenBay.id)).join(Ve,
                                                                                                          Ve.chuyenBay_id.__eq__(
                                                                                                              ChuyenBay.id)).join(
                HangVe,
                HangVe.id.__eq__(Ve.hangVe_id)).filter(
                extract('month', ChuyenBay.created_date) == so_lieu_year).order_by(TuyenBay.id).group_by(
                TuyenBay.id).all()

        doanh_thu_tung_dot = db.session.query(TuyenBay.id, TuyenBay.name, func.sum(HangVe.price),
                                              func.count(ChuyenBay.id)).join(ChuyenBay, ChuyenBay.tuyenBay_id.__eq__(
            TuyenBay.id)).join(Ve, Ve.chuyenBay_id.__eq__(ChuyenBay.id)).join(HangVe,
                                                                              HangVe.id.__eq__(Ve.hangVe_id)).filter(
            extract('year', ChuyenBay.created_date) == year).filter(extract('month', ChuyenBay.created_date) == so_lieu_year).group_by(TuyenBay.id).all()
        tong_doanh_thu = decimal.Decimal('0')
        for doanh_thu in doanh_thu_tung_dot:
            tong_doanh_thu += decimal.Decimal(doanh_thu[2])

        # import pdb;
        # pdb.set_trace()

        return db.session.query(TuyenBay.id, TuyenBay.name, func.sum(HangVe.price),
                                func.count(ChuyenBay.id), tong_doanh_thu).join(ChuyenBay, ChuyenBay.tuyenBay_id.__eq__(
            TuyenBay.id)).join(Ve, Ve.chuyenBay_id.__eq__(ChuyenBay.id)).join(HangVe,
                                                                              HangVe.id.__eq__(Ve.hangVe_id)).filter(
            extract('year', ChuyenBay.created_date) == year).filter(extract('month', ChuyenBay.created_date) == so_lieu_year).order_by(TuyenBay.id).group_by(TuyenBay.id).all()



# if __name__=='__main__':
#     with app.app_context():
#         print(tuyen_bay_month_doanh_thu_stats(2022, 1, "2"))