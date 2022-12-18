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


def load_tuyen_bay():
    return TuyenBay.query.all()

def load_chuyen_bay():
    return ChuyenBay.query.all()


def load_hang_ve():
    return HangVe   .query.all()


def get_chuyen_bay_id(chuyen_bay_id):
    return ChuyenBay.query.get(chuyen_bay_id)


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


# def LapLich(name, diem_di_id, diem_den_id, ngay_gio, thoi_gian_bay, hang1, hang2, tgs, thoi_gian_dung, tb_id):
#     san_bay_di = SanBay.query.filter(SanBay.id.__eq__(int(diem_di_id))).first()
#     san_bay_den = SanBay.query.filter(SanBay.id.__eq__(int(diem_den_id))).first()
#     tuyen_bay = TuyenBay.query.filter(TuyenBay.id.__eq__(int(tb_id))).first()
#
#     mb = MayBay(name="test")
#     db.session.add(mb)
#     db.session.commit()
#
#     hv1 = HangVe(name="hang 1", price=500, so_luong_con_lai=hang1, mayBay_id = mb.id)
#     hv2 = HangVe(name="hang 2", price=500, so_luong_con_lai=hang2, mayBay_id = mb.id)
#     db.session.add_all([hv1,hv2])
#     db.session.commit()
#
#     tdb = ThoiDiemBay(name="test", ngay_gio_bay = ngay_gio, thoi_gian_bay = thoi_gian_bay, thoi_gian_dung=thoi_gian_dung)
#     db.session.add(tdb)
#     db.session.commit()
#
#     cb = ChuyenBay(name=name, sanBayDi_id = san_bay_di.id, sanBayDen_id = san_bay_den.id, tuyenBay_id=tuyen_bay.id)
#     db.session.add(cb)
#     db.session.commit()
#
#     mbtcb = MayBayThuocChuyenBay(mayBay_id=mb.id, chuyenBay_id=cb.id)
#     db.session.add(mbtcb)
#     db.session.commit()
#
#     for tg in tgs:
#         trung_gian = SanBay.query.filter(SanBay.id.__eq__(int(tg))).first()
#         cbcsbtg = ChuyenBayCoSanBayTrungGian(chuyenBay_id = cb.id, sanBayTrungGian_id = trung_gian.id)
#         db.session.add(cbcsbtg)
#         db.session.commit()


def tim_chuyen_bay(diem_di,diem_den):
    if diem_di is None and diem_den is None:
        return load_chuyen_bay()
    if diem_di == "all" and diem_den == "all":
        return load_chuyen_bay()
    return ChuyenBay.query.filter(ChuyenBay.sanBayDi_id.__eq__(int(diem_di)), ChuyenBay.sanBayDen_id.__eq__(int(diem_den)))


def dat_ve_online(name, lastname, cccd, hinh_cccd, sdt, chuyen_bay, hang_ve):
    chuyenbay=ChuyenBay.query.filter(ChuyenBay.id.__eq__(int(chuyen_bay))).first()
    hv = HangVe.query.filter(HangVe.id.__eq__(int(hang_ve))).first()
    kh = KhachHang(name=name, lastName=lastname, cccd=cccd, hinh_cccd=hinh_cccd, sdt=sdt, chuyenBay_id=chuyenbay.id)

    db.session.add(kh)
    db.session.commit()

    ve = Ve(name=chuyenbay.name, chuyenBay_id=chuyenbay.id, hangVe_id=hv.id, khachhang_id=kh.id)
    db.session.add(ve)
    db.session.commit()


# if __name__=='__main__':
#     with app.app_context():
#         print(tuyen_bay_month_doanh_thu_stats(2022, 1, "2"))